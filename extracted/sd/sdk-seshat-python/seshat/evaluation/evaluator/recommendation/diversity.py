from typing import List, Iterable

import numpy as np
import pandas as pd
from pyspark.sql import DataFrame as PySparkDataFrame
from sklearn.metrics.pairwise import cosine_similarity

from seshat.evaluation.evaluator import Evaluator
from seshat.general import configs
from seshat.utils.col_to_list import ColToList


class IntraListDiversityEvaluator(Evaluator):
    def __init__(
        self,
        token_col: str = configs.CONTRACT_ADDRESS_COL,
        feature_cols: List[str] = (configs.AMOUNT_COL,),
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.feature_cols = feature_cols
        self.token_col = token_col

    def evaluate_df(self, test: pd.DataFrame, prediction: Iterable, *args, **kwargs):
        feature_mapping = {
            row[1]: list(row[2:])
            for row in test[[self.token_col, *self.feature_cols]].itertuples()
        }
        return self._calculate_ild(feature_mapping, prediction)

    def evaluate_spf(
        self, test: PySparkDataFrame, prediction: Iterable, *args, **kwargs
    ):
        feature_mapping = {
            row[self.token_col]: [row[col] for col in self.feature_cols]
            for row in test.collect()
        }
        return self._calculate_ild(feature_mapping, prediction)

    @staticmethod
    def _calculate_ild(feature_mapping, prediction):
        total_ipd = 0
        for pred_list in prediction:
            features = []
            for val in pred_list:
                features.append(feature_mapping[val])
            features = np.array(features)
            dissimilarity_matrix = 1 - cosine_similarity(features)
            dissimilarity = dissimilarity_matrix[np.triu_indices(len(features), k=1)]
            total_ipd += np.mean(dissimilarity)

        return {"ILD": total_ipd / len(prediction)}


class ItemCoverageEvaluator(Evaluator):
    def __init__(self, token_col: str = configs.CONTRACT_ADDRESS_COL, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token_col = token_col

    def evaluate(self, test: pd.DataFrame, prediction: Iterable, *args, **kwargs):
        unique_items = set(ColToList().get_ls(test, self.token_col))
        unique_items_prediction = set(token for pred in prediction for token in pred)
        covered_items = unique_items & unique_items_prediction
        return {"Item Coverage": len(covered_items) / len(unique_items)}

    def evaluate_df(self, test: pd.DataFrame, prediction: Iterable, *args, **kwargs):
        return self.evaluate(test, prediction, *args, **kwargs)

    def evaluate_spf(
        self, test: PySparkDataFrame, prediction: Iterable, *args, **kwargs
    ):
        return self.evaluate(test, prediction, *args, **kwargs)
