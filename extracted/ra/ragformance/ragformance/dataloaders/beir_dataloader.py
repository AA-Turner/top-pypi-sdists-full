from .downloads import download_and_unzip

import logging

import json
import csv
import os
from tqdm.autonotebook import tqdm

from typing import List

from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel

from pydantic import TypeAdapter

ta = TypeAdapter(List[DocModel])
taq = TypeAdapter(List[AnnotatedQueryModel])

logger = logging.getLogger(__name__)


# Function imported from BEIR : https://github.com/beir-cellar/beir/blob/main/beir/datasets/data_loader.py
def check(fIn: str, ext: str):
    if not os.path.exists(fIn):
        raise ValueError(f"File {fIn} not present! Please provide accurate file.")

    if not fIn.endswith(ext):
        raise ValueError(f"File {fIn} must be present with extension {ext}")


def load_custom(
    data_folder: str = None,
    split: str = "test",
    filter_corpus: bool = False,
) -> tuple[dict[str, dict[str, str]], dict[str, str], dict[str, dict[str, int]]]:
    corpus_file = (
        os.path.join(data_folder, "corpus.jsonl") if data_folder else "corpus.jsonl"
    )
    query_file = (
        os.path.join(data_folder, "queries.jsonl") if data_folder else "queries.jsonl"
    )
    qrels_folder = os.path.join(data_folder, "qrels") if data_folder else None
    qrels_file = os.path.join(qrels_folder, split + ".tsv")

    check(fIn=corpus_file, ext="jsonl")
    check(fIn=query_file, ext="jsonl")
    check(fIn=qrels_file, ext="tsv")

    logger.info("Loading Corpus...")
    corpus: List[DocModel] = []
    num_lines = sum(1 for i in open(corpus_file, "rb"))
    with open(corpus_file, encoding="utf8") as fIn:
        for line in tqdm(fIn, total=num_lines):
            line = json.loads(line)
            corpus.append(line)
        logger.info("Loaded %d Documents.", len(corpus))

    logger.info("Loading Queries...")
    queries = {}
    with open(query_file, encoding="utf8") as fIn:
        for line in fIn:
            line = json.loads(line)

            line["query_text"] = line.get("text", "")
            line["relevant_document_ids"] = []
            line["ref_answer"] = "_"
            line.pop("text", None)
            queries[line["_id"]] = line

    if os.path.exists(qrels_file):
        reader = csv.reader(
            open(qrels_file, encoding="utf-8"),
            delimiter="\t",
            quoting=csv.QUOTE_MINIMAL,
        )
    next(reader)

    for id, row in enumerate(reader):
        query_id, corpus_id, score = row[0], row[1], int(row[2])

        if query_id in queries:
            answer = queries[query_id].get("relevant_document_ids", [])
            answer.append(
                {
                    "corpus_id": corpus_id,
                    "score": score,
                }
            )
            new_query = queries[query_id]
            new_query["relevant_document_ids"] = answer
            new_query["ref_answer"] = "_"
            queries[query_id] = new_query

    # remove queries without answers
    queries = {
        k: v
        for k, v in queries.items()
        if "relevant_document_ids" in v and len(v["relevant_document_ids"]) > 0
    }

    queries_as_array = list(queries.values())

    logger.info("Loaded %d Queries.", len(queries))

    if filter_corpus:
        filtered_ids = {
            a["corpus_id"] for q in queries_as_array for a in q["relevant_document_ids"]
        }
        filtered_corpus = [
            document for document in corpus if document["_id"] in filtered_ids
        ]
        corpus = filtered_corpus
        logger.info("Filtered Corpus to %d Documents.", len(corpus))

    return ta.validate_python(corpus), taq.validate_python(queries_as_array)


def load_beir_dataset(
    dataset="scifact", url=None, folder_path="data", filter_corpus=False
) -> tuple:
    """
    Load a BEIR dataset for evaluation.
    """

    # Download and unzip the dataset
    if url is None:
        url = f"https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{dataset}.zip"
    else:
        # Check if the URL is valid
        if not url.startswith("https://") and not url.startswith("http://"):
            raise ValueError("Invalid URL. Please provide a valid URL.")

    data_path = download_and_unzip(url, folder_path)

    return load_custom(data_path, filter_corpus=filter_corpus)
