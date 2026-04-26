import argparse
from pathlib import Path
import os
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))


from scripts.preprocess.truecase import (
    train_truecaser,
    truecase_file_with_model
)

from scripts.preprocess.tokenize_corpus import tokenize_file


# --------------------------------------------------
# Utility: Alignment Check
# --------------------------------------------------
def count_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return sum(1 for _ in f)


def validate_alignment(src_path, tgt_path):
    src_count = count_lines(src_path)
    tgt_count = count_lines(tgt_path)

    print("\nFinal alignment check:")
    print(f"English lines: {src_count}")
    print(f"Amharic lines: {tgt_count}")

    if src_count != tgt_count:
        raise ValueError("Mismatch detected! Parallel files are misaligned.")
    else:
        print("Alignment OK.")


# --------------------------------------------------
# Main Pipeline
# --------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description="Post-process cleaned English-Amharic corpus (truecase + tokenize)"
    )

    ap.add_argument('--src', required=True, help='Cleaned English file')
    ap.add_argument('--tgt', required=True, help='Cleaned Amharic file')
    ap.add_argument('--out-dir', default='data/final', help='Output directory')
    ap.add_argument('--truecase-model', default=None, help='Path to truecase model (optional)')

    args = ap.parse_args()

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------
    # Step 1: TRUECASING (ENGLISH ONLY)
    # --------------------------------------------------
    print("Step 1: Truecasing English...")

    truecase_model = args.truecase_model or (out / 'truecase.en.model')

    # Train model if not exists
    if not Path(truecase_model).exists():
        print("Training Moses truecase model...")
        train_truecaser(args.src, str(truecase_model))

    src_tc = out / 'src.tc.en'

    # STRICT: no fallback (important for reproducibility)
    print("Applying Moses truecaser...")

    try:
        truecase_file_with_model(
            args.src,
            str(src_tc),
            str(truecase_model)
        )
    except Exception as e:
        raise RuntimeError(f"Truecasing failed (no fallback allowed): {e}")

    # --------------------------------------------------
    # Step 2: TOKENIZATION
    # --------------------------------------------------
    print("Step 2: Tokenization...")

    src_tok = out / 'corpus.tok.en'
    tgt_tok = out / 'corpus.tok.am'

    tokenize_file(str(src_tc), str(src_tok), 'en')
    tokenize_file(args.tgt, str(tgt_tok), 'am')

    # --------------------------------------------------
    # FINAL OUTPUT
    # --------------------------------------------------
    print("\nPost-processing completed.")
    print(f"English (truecased + tokenized): {src_tok}")
    print(f"Amharic (tokenized): {tgt_tok}")

    # --------------------------------------------------
    # ALIGNMENT CHECK (CRITICAL)
    # --------------------------------------------------
    validate_alignment(src_tok, tgt_tok)


# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------
if __name__ == "__main__":
    main()