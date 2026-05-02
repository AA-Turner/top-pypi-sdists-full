"""
Script for converting the EvENT annotations to the shared SPP format.
"""
import argparse
import csv
from dataclasses import dataclass
from difflib import SequenceMatcher
import json
import os
from pathlib import Path
from typing import List
import zipfile

import requests
import spacy

from tokenise import tokenise

spacy.tokens.Token.set_extension("event_anno_id", default=None)
spacy.tokens.Token.set_extension("event_kind", default=None)

DATASET_URL = "https://github.com/forTEXT/EvENT_Dataset/archive/refs/tags/v.1.1.zip"
CACHE_PATH = Path(".cache")
EVENT_ZIP_PATH = CACHE_PATH / "events.zip"

parser = argparse.ArgumentParser("Create event data from event ")
parser.add_argument("tsv_input_path")
parser.add_argument("tsv_output_path")
parser.add_argument("text_name", default="Die Judenbuche", nargs="?")
parser.add_argument("zip_path", default=EVENT_ZIP_PATH, nargs="?")


class TSVDialect(csv.excel_tab):
    # We had \r\n line endings but they disappeared in our process
    # likely some over eager text editor... So let's just do newlines
    lineterminator = "\n"


@dataclass
class UniversalAnnotation:
    id: int
    text: str
    start: int
    end: int

    @classmethod
    def from_row(cls, row):
        id, text, start, end = row
        return UniversalAnnotation(
            id,
            text,
            int(start),
            int(end),
        )

    @staticmethod
    def to_text(sentence: List["UniversalAnnotation"]):
        out = []
        for element in sentence:
            out.append(element.text)
        return "\t".join(out)


def load_dataset(zip_file: zipfile.ZipFile):
    data = json.load(zip_file.open("EvENT_Dataset-v.1.1/Annotations_EvENT.json"))
    text_dir = zipfile.Path(zip_file, "EvENT_Dataset-v.1.1/Plain_Texts/")
    for full_path in text_dir.iterdir():
        full_text = full_path.read_text()
        path = Path(full_path.filename)
        simple_name = path.name.split("_")[-1][:-4]
        for work_name in data.keys():
            if simple_name.lower() in work_name.lower():
                data[work_name]["full_text"] = full_text
    return data



def get_json_dataset(zip_path: Path):
    if os.path.isfile(zip_path):
        data = load_dataset(zipfile.ZipFile(str(zip_path)))
    else:
        os.makedirs(zip_path.parent, exist_ok=True)
        response = requests.get(DATASET_URL)
        out_file = open(zip_path, "wb")
        assert response.status_code == 200
        try:
            for chunk in response.iter_content(chunk_size=512 * 1024):
                if chunk is not None:
                    out_file.write(chunk)
        except Exception as err:
            os.unlink(zip_path)
            raise err
        out_file.close()
        zip_file = zipfile.ZipFile(str(zip_path))
        data = load_dataset(zip_file)
    return data


def add_annotation_to_tokens(doc, gold_standard):
    spans = []
    for i, annotation in enumerate(gold_standard):
        for span in annotation["spans"]:
            spans.append(((span[0], span[1]), (i, annotation["tag"])))
    # This is quadratic and could be heavily optmized but ¯\_(ツ)_/¯
    for token in doc:
        for (start, end), (anno_id, tag) in spans:
            if start <= token.idx and end >= (token.idx + len(token)):
                token._.event_anno_id = anno_id
                token._.event_kind = tag


def get_reference_token_annotations(op_codes, our_doc, strs_reference):
    annotations = [] # Triple: (was_annotated, annnotation_id, annotation_tag)
    for op, reference_start, reference_end, ours_start, ours_end in op_codes:
        if op == "insert":
            # We don't really care, our annotations are just not added
            pass
        elif op == "delete":
            # We need to set the output tokens to unseen/unannotated
            for i in range(reference_start, reference_end):
                annotations.append((False, "-", "-"))
        elif op == "replace":
            # We just transfer the annotation to the new tokens
            if len(set(t._.event_anno_id for t in our_doc[ours_start:ours_end])) == 1:
                for _ in range(reference_start, reference_end):
                    annotations.append((True, our_doc[ours_start]._.event_anno_id or "-", our_doc[ours_start]._.event_kind or "-"))
            elif (reference_end - reference_start > 5) and reference_end - reference_start == ours_end - ours_start:
                # They are the same length, we are okay up to 5 and with the same length
                for i in range(ours_start, ours_end):
                    annotations.append((True, our_doc[i]._.event_anno_id or "-", our_doc[i]._.event_kind or "-"))
            else:
                for _ in range(reference_start, reference_end):
                    annotations.append((False, "-", "-"))
        elif op == "equal":
            for i_ours, i_ref in zip(range(ours_start, ours_end), range(reference_start, reference_end)):
                assert our_doc[i_ours].text.strip() == strs_reference[i_ref].strip()
                annotations.append((True, our_doc[i_ours]._.event_anno_id or "-", our_doc[i_ours]._.event_kind or "-"))
    assert len(annotations) == len(strs_reference)
    return annotations


def main(input_json: Path, reference_tsv: Path, text_name: str, out_path: Path):
    nlp = spacy.load("de_core_news_lg")
    data = get_json_dataset(input_json)
    gold_standard_annos = data[text_name]["gold_standard"]
    tsv_infile = open(reference_tsv)
    next(tsv_infile) #  Skip header
    reader = csv.reader(tsv_infile, dialect=TSVDialect)
    all_annotations_reference = []
    for row in reader:
        if len(row) == 1:
            continue
        else:
            all_annotations_reference.append(UniversalAnnotation.from_row(row))

    doc = nlp(data[text_name]["full_text"])
    add_annotation_to_tokens(doc, gold_standard_annos)
    lines = tokenise.tokenise(data[text_name]["full_text"])

    all_annotations_new = []
    for row in lines:
        if len(row) == 1:
            continue
        else:
            all_annotations_new.append(UniversalAnnotation.from_row(row))

    strs_reference = [a.text for a in all_annotations_reference]
    strs_new = [a.text for a in all_annotations_new]

    matches = SequenceMatcher(None, strs_reference, strs_new)
    codes = matches.get_opcodes()
    annotations = get_reference_token_annotations(codes, doc, strs_reference)

    reader = csv.reader(open(reference_tsv), dialect=TSVDialect)
    i = 0
    with open(out_path, "w") as out_file:
        writer = csv.writer(out_file, dialect=TSVDialect)
        # Skip header
        writer.writerow(next(reader) + ["isAnnotated", "annotationId", "eventKind"])
        for row in reader:
            if len(row) == 1:
                writer.writerow(row)
            else:
                writer.writerow(row + list(annotations[i]))
                i += 1



if __name__ == "__main__":
    args = parser.parse_args()
    main(Path(args.zip_path), Path(args.tsv_input_path), args.text_name, args.tsv_output_path)
