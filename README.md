# EL Workspace: English–Amharic Machine Translation

Implementation of **"Parallel Corpora Preparation for English-Amharic Machine Translation"** (Biadgline & Smaïli, IWANN 2021).

## Overview

- **Corpus:** 225,304 parallel sentences (Religion, Law, News); after cleaning → 218,365.
- **SMT:** Moses + KenLM 3-gram (target: Amharic). BLEU ~26.47.
- **NMT:** OpenNMT RNN + attention, BPE. BLEU ~32.44.

## Directory layout

```
el-workspace/
├── README.md
├── requirements.txt
├── config/                 # SMT/NMT configs
├── data/                   # Put raw/preprocessed corpora here
│   ├── raw/                # raw.en, raw.am (aligned line-by-line)
│   ├── processed/          # after preprocessing
│   └── split/              # train/dev/test
├── scripts/
│   ├── preprocess/         # normalize, tokenize, truecase, clean
│   ├── split_data.py       # train/dev/test split
│   ├── train_smt.sh        # Moses + KenLM
│   ├── train_nmt.sh        # OpenNMT-py
│   └── evaluate.py        # BLEU
└── run_pipeline.py         # Run full pipeline (preprocess → split → train → eval)
```

## Setup

### 1. Python environment

```bash
cd el-workspace
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 2. Optional: Moses (for SMT)

- Install [Moses](http://www.statmt.org/moses/) and add to `PATH`.
- Install [KenLM](https://kheafield.com/code/kenlm/).

### 3. Optional: OpenNMT-py (for NMT)

```bash
pip install OpenNMT-py
```

### 4. Data

Place parallel corpus as two files, one sentence per line, aligned by line:

- `data/raw/corpus.en` — English
- `data/raw/corpus.am` — Amharic

**Option A:** Download the [English-Amharic parallel corpus](https://github.com/yohannesb/English-Amharic-parallel-corpus) and copy into `data/raw/` as `corpus.en` and `corpus.am`.

**Option B:** Create a small sample for testing (no download):

```bash
python scripts/create_sample_data.py 500
```
This creates `data/raw/corpus.en` and `corpus.am` with 500 lines for pipeline testing.

## Usage

### Preprocessing only

```bash
python scripts/preprocess/run_preprocessing.py --src data/raw/corpus.en --tgt data/raw/corpus.am --out-dir data/processed
```

### Full pipeline (preprocess → split → train SMT/NMT → evaluate)

```bash
python run_pipeline.py --data-dir data --mode all
```

### Modes

- `preprocess` — normalize, tokenize, truecase, clean
- `split` — train / dev / test
- `smt` — train SMT (requires Moses/KenLM)
- `nmt` — train NMT (requires OpenNMT-py)
- `eval` — compute BLEU
- `all` — run all steps that have data and tools

## References

- Paper: Biadgline, Y., Smaïli, K. (2021). Parallel Corpora Preparation for English-Amharic Machine Translation. IWANN 2021. Springer.
- Corpus: https://github.com/yohannesb/English-Amharic-parallel-corpus
