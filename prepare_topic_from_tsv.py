import os
from argparse import ArgumentParser
from prepare_corpus_crys import prepare_feature_from_math

import sys
sys.path.insert(0, '/tuna1/scratch/w32zhong/a0-engine/pya0')
import pya0


def get_args():
    parser = ArgumentParser()
    parser.add_argument("--input_file", "-i", required=True, type=str)
    parser.add_argument("--output_file", "-o", required=True, type=str)
    return parser.parse_args()


def topic_to_trectxt(qno, title, desc=None, narr=None):
    return (
        f"<top>\n\n"
        f"<num> Number: {qno}\n"
        f"<title> {title}\n\n"
        f"<desc> Description:\n{desc or ''}\n\n"
        f"<narr> Narrative:\n{narr or ''}\n\n"
        f"</top>\n\n\n"
    )


def from_tsv(inp_fn, outp_fn, task):
    with open(inp_fn) as f, open(outp_fn, "w") as fout:
        for line in f:
            if line.startswith('#') or not (line.startswith('A.') or line.startswith('B.')):
                print('skip line:', line)
                continue
            line = line.rstrip().split("\t")
            if task == 1:
                qid, terms, tex_s = line[0], line[1], line[2:]
                title = " ".join([prepare_feature_from_math(tex) for tex in tex_s])
                desc = pya0.preprocess_text(terms)

            else:
                qid, tex_s = line[0], line[1:]
                title = " ".join([prepare_feature_from_math(tex) for tex in tex_s])
                desc = ""

            title = " ".join(title.split()[:400])
            desc = " ".join(desc.split()[:1000])
            fout.write(topic_to_trectxt(qid, title=title, desc=desc))


def main():
    args = get_args()
    inp_fn, outp_fn = args.input_file, args.output_file
    assert os.path.exists(inp_fn)
    outp_dir = os.path.dirname(outp_fn)
    if outp_dir != "":
        os.makedirs(outp_dir, exist_ok=True)
    task = 1 if 'task1' in args.input_file else 2
    from_tsv(inp_fn, outp_fn, task)
    print("finished")


if __name__ == "__main__":
    main()
