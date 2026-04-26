"""
Split preprocessed parallel corpus into train / dev / test (paper Section 4.1).

Default:
- Dev: 3,121 sentences
- Test: 2,500 sentences
- Train: remaining
"""

import argparse
import random
from pathlib import Path


def split_corpus(
    src_path: str,
    tgt_path: str,
    out_dir: str,
    dev_size: int = 3121,
    test_size: int = 2500,
    seed: int = 42,
) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    with open(src_path, 'r', encoding='utf-8') as f:
        src_lines = [l.rstrip('\n') for l in f]
    with open(tgt_path, 'r', encoding='utf-8') as f:
        tgt_lines = [l.rstrip('\n') for l in f]

    if len(src_lines) != len(tgt_lines):
        raise ValueError(f'Mismatch: {len(src_lines)} src vs {len(tgt_lines)} tgt lines')

    n = len(src_lines)

    if n < (dev_size + test_size + 10):
        raise ValueError(
            f'Corpus too small ({n}) for requested split: '
            f'dev={dev_size}, test={test_size}'
        )

    # Shuffle indices
    rng = random.Random(seed)
    indices = list(range(n))
    rng.shuffle(indices)

    # Assign splits
    dev_idx = set(indices[:dev_size])
    test_idx = set(indices[dev_size:dev_size + test_size])
    train_idx = set(indices[dev_size + test_size:])

    def write_split(name: str, idx_set: set) -> None:
        s_path = out / f'{name}.en'
        t_path = out / f'{name}.am'

        with open(s_path, 'w', encoding='utf-8') as fs, \
            open(t_path, 'w', encoding='utf-8') as ft:

            for i in idx_set:
                fs.write(src_lines[i] + '\n')
                ft.write(tgt_lines[i] + '\n')

    write_split('train', train_idx)
    write_split('dev', dev_idx)
    write_split('test', test_idx)

    print(
        f'Split written: train={len(train_idx)}, '
        f'dev={len(dev_idx)}, test={len(test_idx)}'
    )


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--src', required=True, help='Preprocessed English corpus')
    p.add_argument('--tgt', required=True, help='Preprocessed Amharic corpus')
    p.add_argument('--out-dir', default='data/split')
    p.add_argument('--dev-size', type=int, default=3121)
    p.add_argument('--test-size', type=int, default=2500)
    p.add_argument('--seed', type=int, default=42)

    args = p.parse_args()

    split_corpus(
        args.src,
        args.tgt,
        args.out_dir,
        dev_size=args.dev_size,
        test_size=args.test_size,
        seed=args.seed,
    )