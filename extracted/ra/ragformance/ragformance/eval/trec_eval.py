from __future__ import annotations

import pytrec_eval

from ragformance.models.answer import AnswerModel


def trec_eval_metrics(
    answers: list[AnswerModel], k_values: list[int] = [1, 3, 5, 10, 20]
) -> tuple[dict[str, float]]:
    """
    Calculate TREC evaluation metrics for the given answers.

    Args:
        answers (list[dict]): List of answers containing query and relevant documents.
        k_values (list[int]): List of k values for evaluation metrics.

    Returns:
        tuple[dict[str, float]]: Tuple containing dictionaries for NDCG, MAP, Recall, and Precision.
    """
    # Check if answers is empty
    if not answers:
        raise ValueError("The answers list is empty. Please provide valid answers.")

    # Initialize qrels and qrels_run dictionaries

    qrels = {}
    qrels_run = {}
    for a in answers:
        qrels[a.query.id] = {}
        for i, doc in enumerate(a.query.relevant_document_ids):
            qrels[a.query.id][doc.corpus_id] = doc.score

        qrels_run[a.query.id] = {}
        for doc_id in a.retrieved_documents_ids:
            qrels_run[a.query.id][doc_id] = 1

    ndcg = {}
    _map = {}
    recall = {}
    precision = {}

    for k in k_values:
        ndcg[f"NDCG@{k}"] = 0.0
        _map[f"MAP@{k}"] = 0.0
        recall[f"Recall@{k}"] = 0.0
        precision[f"P@{k}"] = 0.0

    map_string = "map_cut." + ",".join([str(k) for k in k_values])
    ndcg_string = "ndcg_cut." + ",".join([str(k) for k in k_values])
    recall_string = "recall." + ",".join([str(k) for k in k_values])
    precision_string = "P." + ",".join([str(k) for k in k_values])
    evaluator = pytrec_eval.RelevanceEvaluator(
        qrels, {map_string, ndcg_string, recall_string, precision_string}
    )
    scores = evaluator.evaluate(qrels_run)

    for query_id in scores.keys():
        for k in k_values:
            ndcg[f"NDCG@{k}"] += scores[query_id]["ndcg_cut_" + str(k)]
            _map[f"MAP@{k}"] += scores[query_id]["map_cut_" + str(k)]
            recall[f"Recall@{k}"] += scores[query_id]["recall_" + str(k)]
            precision[f"P@{k}"] += scores[query_id]["P_" + str(k)]

    for k in k_values:
        ndcg[f"NDCG@{k}"] = round(ndcg[f"NDCG@{k}"] / len(scores), 5)
        _map[f"MAP@{k}"] = round(_map[f"MAP@{k}"] / len(scores), 5)
        recall[f"Recall@{k}"] = round(recall[f"Recall@{k}"] / len(scores), 5)
        precision[f"P@{k}"] = round(precision[f"P@{k}"] / len(scores), 5)

    return ndcg, _map, recall, precision
