try:
    from huggingface_hub import login
except ImportError:

    def login(*args, **kwargs):
        raise ImportError(
            "'huggingface_hub' module is not installed. "
            "Please install ragformance with the [huggingface] or [all] option:\n"
            "    pip install ragformance[huggingface]\n"
            "or\n"
            "    pip install ragformance[all]"
        )


try:
    from datasets import load_dataset
except ImportError:

    def load_dataset(*args, **kwargs):
        raise ImportError(
            "'datasets' module is not installed. "
            "Please install ragformance with the [huggingface] or [all] option:\n"
            "    pip install ragformance[huggingface]\n"
            "or\n"
            "    pip install ragformance[all]"
        )


import os
import json
import logging

logger = logging.getLogger(__name__)


# package and upload to huggingface
def push_to_hub(
    HFpath,
    folderpath,
    hf_token=None,
    corpus_file="corpus.jsonl",
    queries_file="queries.jsonl",
    split="train",
):
    if hf_token is None and os.environ.get("HF_TOKEN") is None:
        # try to load the token from the config.json file
        with open("config.json") as f:
            config = json.load(f)
        hf_token = config["HF_TOKEN"]
    else:
        hf_token = os.environ["HF_TOKEN"]
    if hf_token is None:
        # log error
        logger.error("hf.hf_token is not set. Please set it in the config.json file.")
        return

    login(token=hf_token)
    corpuspath = os.path.join(folderpath, corpus_file)
    queriespath = os.path.join(folderpath, queries_file)

    dataset = load_dataset(
        "json",
        data_files=corpuspath,
        split="train",
    )
    dataset.push_to_hub(HFpath, "corpus", private=True)

    datasetqueries = load_dataset("json", data_files=queriespath, split=split)
    datasetqueries.push_to_hub(HFpath, "queries")

    from huggingface_hub.repocard import RepoCard

    card = RepoCard.load(HFpath, repo_type="dataset")

    card.text = """
    # RAGformance Dataset
    This is a dataset for evaluating RAG models generated with RAGFORmance. The dataset contains a set of queries and a corpus of documents. The queries are designed to test the performance of RAG models on a specific dataset with questions generated syntheticallly.


    ## Dataset Structure
    The dataset consists of two files:
    - `corpus.jsonl`: A jsonl file containing the corpus of documents. Each document is represented as a json object with the following fields:
        - `_id`: The id of the document.
        - `title`: The title of the document.
        - `text`: The text of the document.
        - `metadata`: A dictionary containing the metadata for the document. The metadata can contain any additional information about the document, such as the author, publication date, etc.
    - `queries.jsonl`: A jsonl file containing the queries. Each query is represented as a json object with the following fields:
        - `_id`: The id of the query.
        - `query_text`: The text of the query.
        - `relevant_document_ids`: A list of references to the documents in the corpus. Each reference is represented as a json object with the following fields:
            - `corpus_id`: The id of the document.
            - `score`: The score of the reference.
        - `ref_answer`: The reference answer for the query.
        - `metadata`: A dictionary containing the metadata for the query.


    [RAGFORmance library](https://github.com/FOR-sight-ai/ragformance)

    ## Acknowledgement

    This project received funding from the French ”IA Cluster” program within the Artificial and Natural Intelligence Toulouse Institute (ANITI) and from the "France 2030" program within IRT Saint Exupery. The authors gratefully acknowledge the support of the FOR projects.

    ## License
    This dataset is licensed under the MIT license. See the LICENSE file for more details.
    """
    card.push_to_hub(HFpath, repo_type="dataset")
