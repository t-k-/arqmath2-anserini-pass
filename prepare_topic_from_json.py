import json
from argparse import ArgumentParser
from prepare_corpus_crys import prepare_feature_from_math

import sys
sys.path.insert(0, '/tuna1/scratch/w32zhong/a0-engine/pya0')
import pya0

def get_args():
    parser = ArgumentParser()
    parser.add_argument("--input_json", "-i", required=True)
    parser.add_argument("--output_fn", "-o", required=True)
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


def trec_topic_generator(fn):
    topics = json.load(open(fn))
    for topic_dict in topics:
        qid = topic_dict["qid"]
        title, desc = "", ""  # title == tex; desc == tex
        for kw in topic_dict["kw"]:
            if kw["type"] == "term":
                desc = pya0.preprocess_text(kw["str"])
            elif kw["type"] == "tex":
                title = prepare_feature_from_math(kw["str"])
        yield topic_to_trectxt(qno=qid, title=title, desc=desc)


def main():
    args = get_args()
    with open(args.output_fn, "w") as fout:
        for topic in trec_topic_generator(args.input_json):
            fout.write(topic)
    print("finished")


if __name__ == "__main__":
    main()
