import os
import re
import json
import copy
import logging
from argparse import ArgumentParser
from tqdm import tqdm

import sys
sys.path.insert(0, '/tuna1/scratch/w32zhong/a0-engine/pya0')
import pya0


FORMAT = "%(asctime)-15s %(message)s"
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)
logging.basicConfig(format=FORMAT)

WIDTH = 64
join, listdir = os.path.join, os.listdir


def iter_imath_splits(content):
    last = None
    splits = re.split("(\[imath\]|\[/imath\])", content)
    for i, cur in enumerate(splits):
        next_ = splits[i + 1] if i + 1 < len(splits) else None
        trim = lambda x: None if x is None else x.strip()
        if cur.strip() == "":
            continue
        elif trim(cur) in ("[imath]", "[/imath]"):
            last = cur
            continue
        elif trim(last) == None and trim(next_) == "[imath]":
            yield ("text", cur, None, None)
        elif trim(next_) == None and trim(last) == "[/imath]":
            yield ("text", cur, None, None)
        elif trim(last) == "[imath]" and trim(next_) == "[/imath]":
            yield ("math", cur, last, next_)
        else:
            yield ("text", cur, None, None)
        last = cur


def get_args():
    parser = ArgumentParser()
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--output_dir", "-o", required=True)
    return parser.parse_args()


def documents_iterator(directory, add_fid):
    files = listdir(directory)
    for file in files:
        if not file.endswith(".json"):
            continue

        fn = join(directory, file)
        doc = json.load(open(fn))
        if not add_fid:
            yield doc["extern_id"], doc["content"]  # docid, contents
        else:
            extern_id, url = doc["extern_id"], doc["url"]
            url = url.split(",")
            url_fid, url_post_id = url[0], url[1]
            assert url_fid == extern_id
            yield f"{url_fid}-{url_post_id}", doc["content"]  # docid, contents


def parse_contents(original_content):
    expand_set = set()
    parsed_content = ""
    # pya0.expand_math(original_content, expand_set)

    # parse the original contents into math features
    for type, content, _, _ in iter_imath_splits(original_content):
        if type == "math":
            content = prepare_feature_from_math(content)
        else:
            assert (
                type == "text"
            ), f"Unexpected type: should be either math or text, got {type}"
            #content = " ".join(analyzer.analyze(content))
        parsed_content += f" {content}"

    # expansion
    ''' 
    expands = " ".join(list(expand_set))
    parsed_content += "__EXPAND__"
    for type, content, _, _ in iter_imath_splits(expands):
        if type == "math":
            continue
        parsed_content += " ".join(analyzer.analyze(content))
    ''' 

    return parsed_content


def prepare_feature_from_math(math_equation):
    res, OPT = pya0.parse(math_equation, insert_rank_node=True)
    if res == "OK":
        full_pathes = [path for path in leaf_to_root_path_generator(OPT)]
        if len(full_pathes) > WIDTH:
            # logger.warning(f"Detected {len(full_pathes)} from the tree, keep the first {WIDTH} only")
            full_pathes = full_pathes[:WIDTH]

        all_pathes = []

        for full_path in full_pathes:
            for prefix_path in prefix_path_generator(full_path):
                all_pathes.append(prefix_path)
        return " ".join(["_" + "_".join(path) for path in all_pathes])

        #for pathes in prefix_path_generator(full_pathes):
        #    all_pathes.extend(pathes)
        #return " ".join(["_" + "_".join(path) for path in all_pathes])

    else:
        # print("Error: ", res, "Use original math form: ", math_equation)
        return ""


def leaf_to_root_path_generator(OPT, cur_path=None):
    nodeID, token, symbol, children = OPT
    if cur_path is None:
        cur_path = []

    cur_path.insert(0, token)
    if len(children) == 0:
        yield copy.deepcopy(cur_path)
        symbol = re.sub("[^0-9a-zA-Z]+", "__", symbol)
        yield [symbol] + cur_path[1:]

    if nodeID > 2000:
        yield copy.deepcopy(cur_path)
        symbol = re.sub("[^0-9a-zA-Z]+", "__", symbol)
        yield [symbol] + cur_path[1:]
        return

    for child_OPT in children:
        try:
            for path in leaf_to_root_path_generator(child_OPT, cur_path=cur_path):
                yield path
        except RecursionError:
            logger.warning(f"Encounter Recusive Error with {OPT}")
            return
    cur_path.pop(0)


def prefix_path_generator(full_path):
    for i in range(len(full_path), 1, -1):
        yield full_path[0:i]


def main():
    N = -1
    args = get_args()
    root_path = args.corpus
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    subfolders = sorted(listdir(root_path), key=lambda k: int(k))
    add_fid = 'task2' in args.corpus
    for subfolder in tqdm(subfolders, desc="Looping over each folders"):
        if int(subfolder) < N:
            continue

        with open(join(output_dir, subfolder + ".json"), "w") as fout:
            directory = join(root_path, subfolder)
            for docid, contents in documents_iterator(
                directory, add_fid=add_fid
            ):
                new_contents = {"id": docid, "contents": parse_contents(contents)}
                fout.write(json.dumps(new_contents) + "\n")
    print("finished")


if __name__ == "__main__":
    main()
