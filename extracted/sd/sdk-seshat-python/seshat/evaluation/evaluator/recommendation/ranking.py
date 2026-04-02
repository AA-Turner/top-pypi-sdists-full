from typing import Iterable

import numpy as np
import pandas as pd
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.evaluation.evaluator import Evaluator
from seshat.general import configs
from seshat.utils.col_to_list import ColToList


class MRRRankingEvaluator(Evaluator):
    def __init__(
        self,
        test_value_col: str = configs.CONTRACT_ADDRESS_COL,
        k: int = 10,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.test_value_col = test_value_col
        self.k = k

    def evaluate(self, test: object, prediction: Iterable, size: int):
        total_reciprocal_rank = 0
        for true_ls, pred_ls in zip(
            ColToList().get_ls(test, self.test_value_col), prediction
        ):
            true_set = set(true_ls)
            reciprocal_rank = 0

            for rank, pred_value in enumerate(pred_ls[: self.k]):
                if pred_value in true_set:
                    reciprocal_rank = 1 / (rank + 1)
                    break
            total_reciprocal_rank += reciprocal_rank

        return {"MRR": total_reciprocal_rank / size}

    def evaluate_df(self, test: pd.DataFrame, prediction: Iterable, *args, **kwargs):
        return self.evaluate(test, prediction, len(test))

    def evaluate_spf(
        self, test: PySparkDataFrame, prediction: Iterable, *args, **kwargs
    ):
        return self.evaluate(test, prediction, test.count())


class DCGRankingEvaluator(Evaluator):
    def __init__(
        self,
        test_value_col: str = configs.CONTRACT_ADDRESS_COL,
        k: int = 10,
        normalized: bool = True,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.test_value_col = test_value_col
        self.k = k
        self.normalized = normalized

    def evaluate(self, test: object, prediction: Iterable, size: int, *args, **kwargs):
        sum_dcg = 0
        for true_ls, pred_ls in zip(
            ColToList().get_ls(test, self.test_value_col), prediction
        ):
            true_set = set(true_ls)
            binary_relevance = np.asfarray(
                [1 if val in true_set else 0 for val in pred_ls[: self.k]]
            )
            dcg = self._calculate_ndcg(binary_relevance)
            if self.normalized:
                ideal_relevance = np.asfarray([1] * min(len(true_set), self.k))
                idcg = self._calculate_ndcg(ideal_relevance)
                sum_dcg += dcg / idcg
            else:
                sum_dcg += dcg

        return {"NDCG" if self.normalized else "DCG": sum_dcg / size}  # TODO:

    def evaluate_spf(
        self, test: PySparkDataFrame, prediction: Iterable, *args, **kwargs
    ):
        return self.evaluate(test, prediction, test.count())

    def evaluate_df(self, test: pd.DataFrame, prediction: Iterable, *args, **kwargs):
        return self.evaluate(test, prediction, len(test))

    @staticmethod
    def _calculate_ndcg(relevance: np.ndarray) -> float:
        if relevance.size:
            return np.sum(relevance / np.log2(np.arange(2, relevance.size + 2)))

        return 0.0
