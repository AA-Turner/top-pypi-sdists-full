import os
from typing import List
import unittest
import json
from ragformance.models.answer import (
    AnswerModel,
    AnnotatedQueryModel,
    RelevantDocumentModel,
)
from ragformance.models.corpus import DocModel
from ragformance.rag.naive_rag import NaiveRag
from ragformance.rag.openwebui_rag import OpenwebuiRag


class TestAskQueriesCorpus(unittest.TestCase):
    def test_naive_rag_ask_queries(self):
        corpus: List[DocModel] = [
            DocModel(
                _id="c_1",
                title="France",
                text="The capital of France is Paris",
            )
        ]

        naive_rag = NaiveRag()
        naive_rag.upload_corpus(corpus=corpus)

        queries: List[AnnotatedQueryModel] = [
            AnnotatedQueryModel(
                _id="q_1",
                query_text="What is the capital of France",
                relevant_document_ids=[RelevantDocumentModel(corpus_id="c_1", score=1)],
                ref_answer="Paris is the capital of France",
            )
        ]

        config = {
            "LLM_endpoint": os.environ["LLM_ENDPOINT"],
            "LLM_key": os.environ["LLM_KEY"],
            "LLM_model": os.environ["LLM_MODEL"],
        }
        answers: List[AnswerModel] = naive_rag.ask_queries(queries, config)
        assert (
            len(answers) == 1
            and answers[0].retrieved_documents_ids == ["c_1"]
            and "Paris" in answers[0].model_answer
        )

    # Need to create a user with client_email and client_mpd before running the test
    def test_openwebui_rag_ask_queries(self):
        corpus: List[DocModel] = [
            DocModel(
                _id="c_1",
                title="France",
                text="The capital of France is Paris",
            )
        ]

        # config = {
        #     "llm_name": "qwen2.5:0.5b-instruct",
        #     "dataset_name" : "test",
        #     "client_email" : "admin@example.com",
        #     "client_mdp" : "admin",
        # }

        with open("tests/test_config_ollama.json") as jsonfile:
            config = json.load(jsonfile)

        openwebui_rag = OpenwebuiRag()
        nb_docs_processed, config_updated = openwebui_rag.upload_corpus(
            corpus=corpus, config=config
        )

        queries: List[AnnotatedQueryModel] = [
            AnnotatedQueryModel(
                _id="q_1",
                query_text="What is the capital of France",
                relevant_document_ids=[RelevantDocumentModel(corpus_id="c_1", score=1)],
                ref_answer="Paris is the capital of France",
            )
        ]

        answers: List[AnswerModel] = openwebui_rag.ask_queries(
            queries, config=config_updated
        )
        assert len(answers) == 1 and answers[0].retrieved_documents_ids == ["c_1"]
