from typing import List
import unittest
from ragformance.models.corpus import DocModel
from ragformance.rag.naive_rag import NaiveRag
from ragformance.rag.openwebui_rag import OpenwebuiRag
import json


class TestUploadCorpus(unittest.TestCase):
    def test_naive_rag_upload_corpus(self):
        corpus: List[DocModel] = [
            DocModel(
                _id="c_1",
                title="France",
                text="The capital of France is Paris",
            )
        ]

        naive_rag = NaiveRag()
        doc_uploaded_num = naive_rag.upload_corpus(corpus=corpus)
        assert doc_uploaded_num == 1

    def test_openwebui_rag_upload_corpus(self):
        corpus: List[DocModel] = [
            DocModel(
                _id="c_1",
                title="France",
                text="The capital of France is Paris",
            )
        ]

        openwebui_rag = OpenwebuiRag()

        with open("tests/test_config_ollama.json") as jsonfile:
            config = json.load(jsonfile)
        doc_uploaded_num, config_updated = openwebui_rag.upload_corpus(
            corpus=corpus, config=config
        )

        assert doc_uploaded_num == 1
