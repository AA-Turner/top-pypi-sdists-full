import unittest
from ragformance.eval.metrics.trec_eval import trec_eval_metrics
from ragformance.models.answer import (
    AnswerModel,
    AnnotatedQueryModel,
    RelevantDocumentModel,
)


class TestEval(unittest.TestCase):
    def test_eval(self):
        answers = [
            AnswerModel(
                _id="a_1",
                query=AnnotatedQueryModel(
                    _id="q_1",
                    query_text="What is the capital of France",
                    relevant_document_ids=[
                        RelevantDocumentModel(corpus_id="c_1", score=1)
                    ],
                    ref_answer="Paris is the capital of France",
                ),
                model_answer="Paris",
                retrieved_documents_ids=["c_1"],
                retrieved_documents_distances=[0.5],
            )
        ]

        # json_answers = [a.model_dump(by_alias=True) for a in answers]

        ndcg, _map, recall, precision = trec_eval_metrics(answers)

        assert ndcg["NDCG@1"] == 1.0 and _map["MAP@1"] == 1.0
