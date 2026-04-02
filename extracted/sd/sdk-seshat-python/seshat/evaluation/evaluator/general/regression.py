from typing import Iterable

import numpy as np
import pandas as pd
from pyspark.sql import DataFrame as PySparkDataFrame
from sklearn.metrics import (
    r2_score,
    mean_squared_error,
)

from seshat.data_class import DFrame
from seshat.evaluation.evaluator import Evaluator
from seshat.general import configs
from seshat.utils.col_to_list import ColToList


class RegressionEvaluator(Evaluator):
    def __init__(self, test_value_col: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_value_col = test_value_col

    def evaluate(self, test: object, prediction: Iterable, *args, **kwargs):
        r2_list = []
        mse_list = []
        rmse_list = []
        for true_ls, pred_ls in zip(
            ColToList().get_ls(test, self.test_value_col), prediction
        ):
            r2_list.append(r2_score(true_ls, pred_ls))
            mse = mean_squared_error(true_ls, pred_ls)
            mse_list.append(mse)
            rmse_list.append(np.sqrt(mse))

        return {
            "r2": np.mean(r2_list),
            "mse": np.mean(mse_list),
            "rmse": np.mean(rmse_list),
        }

    def evaluate_df(self, test: pd.DataFrame, prediction: Iterable, *args, **kwargs):
        return self.evaluate(test, prediction)

    def evaluate_spf(
        self, test: PySparkDataFrame, prediction: Iterable, *args, **kwargs
    ):
        return self.evaluate(test, prediction)


class RegressionWithFeatureMapEvaluator(Evaluator):
    DEFAULT_GROUP_KEYS = {"test": configs.DEFAULT_SF_KEY, "feature_map": "feature_map"}

    def __init__(
        self,
        feature_map_index_col: str,
        feature_map_value_col: str,
        test_value_col: str,
        group_keys=None,
    ):
        super().__init__(group_keys)
        self.feature_map_index_col = feature_map_index_col
        self.feature_map_value_col = feature_map_value_col
        self.test_value_col = test_value_col

    def evaluate(self, feature_map_dict, test: object, prediction: Iterable):
        mapped_test = []
        for value_list in ColToList().get_ls(test, self.test_value_col):
            index_mapped_values = []
            for value in value_list:
                index_mapped_values.append(feature_map_dict[value])
            mapped_test.append(index_mapped_values)

        mapped_prediction = []
        for pred_list in prediction:
            index_mapped_values = []
            for value in pred_list:
                index_mapped_values.append(feature_map_dict[value])
            mapped_prediction.append(index_mapped_values)
        mapped_sf = DFrame.from_raw(data=[{"feature": row} for row in mapped_test])
        return RegressionEvaluator(test_value_col="feature")(
            mapped_sf, prediction=mapped_prediction
        )

    def evaluate_df(
        self,
        test: pd.DataFrame,
        feature_map: pd.DataFrame,
        prediction: Iterable,
        *args,
        **kwargs
    ):
        feature_map_dict = {
            row[self.feature_map_index_col]: row[self.feature_map_value_col]
            for row in feature_map.to_dict("records")
        }
        return self.evaluate(feature_map_dict, test, prediction)

    def evaluate_spf(
        self,
        test: PySparkDataFrame,
        feature_map: PySparkDataFrame,
        prediction: Iterable,
        *args,
        **kwargs
    ):
        selected = feature_map.select(
            self.feature_map_index_col, self.feature_map_value_col
        ).distinct()
        feature_map_dict = {
            row[self.feature_map_index_col]: row[self.feature_map_value_col]
            for row in [row.asDict() for row in selected.collect()]
        }
        return self.evaluate(feature_map_dict, test, prediction)
