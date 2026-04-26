import re
from typing import List, Tuple


# ==========================================================
# 1. Bible Reference Patterns
# ==========================================================

BIBLE_BOOKS = [
    "gen", "genesis", "exo", "exodus", "lev", "leviticus",
    "num", "numbers", "deut", "deuteronomy",
    "josh", "judg", "ruth",
    "sam", "kings", "chron", "ezra", "neh", "est",
    "job", "ps", "psalm", "psalms", "prov", "proverbs",
    "eccl", "song", "isa", "jer", "lam", "ezek", "dan",
    "hos", "joel", "amos", "obad", "jonah", "mic", "nah",
    "hab", "zeph", "hag", "zech", "mal",
    "matt", "mark", "luke", "john", "acts", "rom",
    "cor", "gal", "eph", "phil", "col",
    "thess", "tim", "titus", "philem", "heb",
    "james", "peter", "jude", "rev", "revelation"
]

books_pattern = r'(' + '|'.join(BIBLE_BOOKS) + r')\.?'

# Full references like: "prov. 20:18", "1 cor 13:4"
bible_ref_pattern = re.compile(
    rf'\b(?:read\s+)?(?:\d\s*)?{books_pattern}\s*\d+\s*:\s*\d+\b\.?',
    re.IGNORECASE
)

# Simple references like: "5:10"
simple_ref_pattern = re.compile(r'\b\d+\s*:\s*\d+\b')


# ==========================================================
# 2. Core Logic
# ==========================================================

def is_reference_only(sentence: str, min_remaining_words: int = 2) -> bool:
    """
    Returns True if sentence is mostly a Bible reference.
    Keeps sentences that still contain meaningful words.
    """
    if not isinstance(sentence, str):
        return True

    # Remove references
    cleaned = bible_ref_pattern.sub('', sentence)
    cleaned = simple_ref_pattern.sub('', cleaned)

    cleaned = cleaned.strip()
    remaining_words = cleaned.split()

    return len(remaining_words) < min_remaining_words


# ==========================================================
# 3. Parallel Filtering (SAFE)
# ==========================================================

def remove_bible_reference_pairs(
    src_lines: List[str],
    tgt_lines: List[str],
    min_remaining_words: int = 2
) -> Tuple[List[str], List[str]]:
    """
    Removes ONLY pairs where source is reference-only.
    Keeps alignment intact.
    """
    assert len(src_lines) == len(tgt_lines), "Files are misaligned"

    new_src = []
    new_tgt = []

    removed = 0

    for s, t in zip(src_lines, tgt_lines):
        if is_reference_only(s, min_remaining_words):
            removed += 1
            continue

        new_src.append(s)
        new_tgt.append(t)

    print(f"Removed {removed} Bible reference-only pairs")
    print(f"Remaining pairs: {len(new_src)}")

    return new_src, new_tgt


# ==========================================================
# 4. File-Level Utility
# ==========================================================

def filter_bible_from_files(
    src_path: str,
    tgt_path: str,
    src_out: str,
    tgt_out: str,
    min_remaining_words: int = 2
):
    # Load
    with open(src_path, 'r', encoding='utf-8') as f:
        src_lines = [line.strip() for line in f]

    with open(tgt_path, 'r', encoding='utf-8') as f:
        tgt_lines = [line.strip() for line in f]

    print(f"Loaded pairs: {len(src_lines)}")

    # Filter
    src_clean, tgt_clean = remove_bible_reference_pairs(
        src_lines,
        tgt_lines,
        min_remaining_words
    )

    # Save
    with open(src_out, 'w', encoding='utf-8') as f:
        for line in src_clean:
            f.write(line + '\n')

    with open(tgt_out, 'w', encoding='utf-8') as f:
        for line in tgt_clean:
            f.write(line + '\n')

    print("Bible filtering completed.")


# ==========================================================
# 5. Example Usage
# ==========================================================

if __name__ == "__main__":
    filter_bible_from_files(
        src_path="/Users/elbethelzewdie/Downloads/Telegram Lite/el-workspace/el-workspace/data/processed/cleaned.en",
        tgt_path="/Users/elbethelzewdie/Downloads/Telegram Lite/el-workspace/el-workspace/data/processed/cleaned.am",
        src_out="/Users/elbethelzewdie/Downloads/Telegram Lite/el-workspace/el-workspace/data/processed/final_cleaned.en",
        tgt_out="/Users/elbethelzewdie/Downloads/Telegram Lite/el-workspace/el-workspace/data/processed/final_cleaned.am",
        min_remaining_words=2
    )