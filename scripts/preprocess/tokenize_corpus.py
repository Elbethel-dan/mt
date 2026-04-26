"""
Improved Tokenization (English + Amharic)

Fixes:
- Avoids re-creating tokenizer per line
- Handles Amharic punctuation properly
- Normalizes whitespace
"""

import sys
from pathlib import Path
import re

try:
    from sacremoses import MosesTokenizer
except ImportError:
    MosesTokenizer = None


# -----------------------------
# Initialize tokenizers ONCE
# -----------------------------
tokenizer_en = MosesTokenizer(lang='en') if MosesTokenizer else None


# -----------------------------
# Regex for punctuation
# -----------------------------
# Includes BOTH English + Amharic punctuation
PUNCT = r"[።፣፤፥፦፧፨.,!?;:\"'()\[\]]"


# -----------------------------
# Tokenization functions
# -----------------------------
def tokenize_english_line(line: str) -> str:
    """Tokenize English using Moses (preferred) or fallback regex."""
    line = line.strip()

    if tokenizer_en is not None:
        tokens = tokenizer_en.tokenize(line, return_str=False)
        return " ".join(tokens)

    # Fallback (basic punctuation split)
    line = re.sub(f"({PUNCT})", r" \1 ", line)
    line = re.sub(r"\s+", " ", line)
    return line.strip()


def tokenize_amharic_line(line: str) -> str:
    """
    Tokenize Amharic:
    - Separate punctuation (Amharic + standard)
    - Normalize spacing
    """
    line = line.strip()

    # Separate punctuation
    line = re.sub(f"({PUNCT})", r" \1 ", line)

    # Normalize whitespace
    line = re.sub(r"\s+", " ", line)

    return line.strip()


# -----------------------------
# File-level processing
# -----------------------------
def tokenize_file(input_path: str, output_path: str, lang: str = 'en') -> None:
    """Tokenize file line by line. lang ∈ ('en', 'am')."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    tokenize_line = tokenize_english_line if lang == 'en' else tokenize_amharic_line

    with open(input_path, 'r', encoding='utf-8') as f_in, \
         open(output_path, 'w', encoding='utf-8') as f_out:

        for line in f_in:
            tokenized = tokenize_line(line)
            f_out.write(tokenized + '\n')


# -----------------------------
# CLI usage
# -----------------------------
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python tokenize_corpus.py <input> <output> <en|am>')
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    lang = sys.argv[3].lower()[:2]

    if lang not in ('en', 'am'):
        raise ValueError("Language must be 'en' or 'am'")

    tokenize_file(input_path, output_path, lang)