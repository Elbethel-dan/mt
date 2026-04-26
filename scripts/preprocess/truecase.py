from sacremoses import MosesTruecaser
from pathlib import Path


def train_truecaser(corpus_path: str, model_path: str):
    truecaser = MosesTruecaser()

    with open(corpus_path, "r", encoding="utf-8") as f:
        sentences = [line.strip() for line in f if line.strip()]

    truecaser.train(sentences)

    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    truecaser.save_model(model_path)


def truecase_file_with_model(input_path: str, output_path: str, model_path: str):
    """
    Correct sacremoses 0.1.1 workflow
    """

    from sacremoses import MosesTruecaser
    from pathlib import Path

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Load model via constructor (required by sacremoses)
    truecaser = MosesTruecaser(model_path)

    with open(input_path, "r", encoding="utf-8") as f_in, \
         open(output_path, "w", encoding="utf-8") as f_out:

        for line in f_in:
            tokens = line.strip().split()
            if tokens:
                tc_tokens = truecaser.truecase(" ".join(tokens))
                f_out.write(" ".join(tc_tokens) + "\n")
            else:
                f_out.write("\n")