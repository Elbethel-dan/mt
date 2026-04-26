"""
Improved BLEU evaluation for MT:
- Removes BPE (@@)
- Normalizes whitespace
- Uses sacreBLEU properly
"""

import argparse
import re

try:
    import sacrebleu
except ImportError:
    sacrebleu = None


def remove_bpe(line: str) -> str:
    """Remove BPE artifacts (e.g., 'word@@ ')."""
    return re.sub(r'@@ ?', '', line)


def normalize(line: str) -> str:
    """Basic normalization: strip + collapse spaces."""
    return re.sub(r'\s+', ' ', line.strip())


def load_file(path: str, remove_bpe_flag: bool = False):
    lines = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if remove_bpe_flag:
                line = remove_bpe(line)
            line = normalize(line)
            lines.append(line)
    return lines


def compute_bleu(hyp_path: str, ref_path: str, remove_bpe_flag: bool = True):
    # Load hypothesis (remove BPE)
    hyps = load_file(hyp_path, remove_bpe_flag=remove_bpe_flag)

    # Load references (DO NOT remove BPE unless needed)
    refs = [load_file(ref_path, remove_bpe_flag=False)]

    if sacrebleu is None:
        raise RuntimeError("Please install sacrebleu: pip install sacrebleu")

    bleu = sacrebleu.corpus_bleu(hyps, refs)

    return bleu


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--hyp', required=True, help='Hypothesis file')
    parser.add_argument('--ref', required=True, help='Reference file')
    parser.add_argument('--no-bpe-removal', action='store_true', help='Disable BPE removal')
    args = parser.parse_args()

    bleu = compute_bleu(
        args.hyp,
        args.ref,
        remove_bpe_flag=not args.no_bpe_removal
    )

    print("BLEU score: {:.2f}".format(bleu.score))
    print("Detailed:", bleu)