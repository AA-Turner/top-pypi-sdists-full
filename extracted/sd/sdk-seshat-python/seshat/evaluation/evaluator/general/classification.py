from typing import Iterable

import numpy as np
import pandas as pd
from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame
from pyspark.sql import functions as F
from sklearn.metrics import (
    precision_score,
    recall_score,
)

from seshat.data_class import SPFrame
from seshat.evaluation.evaluator import Evaluator
from seshat.general import configs
from seshat.utils.col_to_list import ColToList


class ClassificationEvaluator(Evaluator):
    ONLY_GROUP = True
    DEFAULT_GROUP_KEYS = {
        "test": configs.DEFAULT_SF_KEY,
        "weight": configs.TOKEN_SF_KEY,
    }

    def __init__(
        self,
        test_value_col: str = configs.CONTRACT_ADDRESS_COL,
        k: int = None,
        weight_token_col: str = configs.CONTRACT_ADDRESS_COL,
        weight_value_col: str = "weight",
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.test_value_col = test_value_col
        self.k = k
        self.weight_token_col = weight_token_col
        self.weight_value_col = weight_value_col

    def evaluate_df(
        self,
        test: DataFrame,
        prediction: Iterable,
        weight: DataFrame = None,
        *args,
        **kwargs
    ):
        precisions = []
        recalls = []

        for true_values, pred_values in zip(
            ColToList().get_ls(test, self.test_value_col), prediction
        ):
            if self.k:
                true_values = true_values[: self.k]
                pred_values = pred_values[: self.k]

            true_df = pd.DataFrame(data=true_values, columns=["token"])
            true_df["true"] = 1
            pred_df = pd.DataFrame(data=pred_values, columns=["token"])
            pred_df["pred"] = 1

            eval_precision_df = pd.merge(true_df, pred_df, on="token", how="right")
            eval_precision_df["true"] = eval_precision_df["true"].fillna(0)
            eval_recall_df = pd.merge(true_df, pred_df, on="token", how="left")
            eval_recall_df["pred"] = eval_recall_df["pred"].fillna(0)
            if weight is not None:
                eval_precision_df = eval_precision_df.merge(
                    weight, left_on="token", right_on=self.weight_token_col, how="left"
                )
                eval_precision_df[self.weight_value_col] = eval_precision_df[
                    self.weight_value_col
                ].fillna(0)
                eval_recall_df = eval_recall_df.merge(
                    weight, left_on="token", right_on=self.weight_token_col, how="left"
                )
                eval_recall_df[self.weight_value_col] = eval_recall_df[
                    self.weight_value_col
                ].fillna(0)
            else:
                eval_precision_df[self.weight_value_col] = 1
                eval_recall_df[self.weight_value_col] = 1

            precision = precision_score(
                eval_precision_df["true"],
                eval_precision_df["pred"],
                sample_weight=eval_precision_df[self.weight_value_col],
            )
            recall = recall_score(
                eval_recall_df["true"],
                eval_recall_df["pred"],
                sample_weight=eval_recall_df[self.weight_value_col],
            )
            precisions.append(precision)
            recalls.append(recall)

        precision = np.mean(precisions)
        recall = np.mean(recalls)
        f1_score = 2 * precision * recall / (precision + recall)
        return {"precision": precision, "recall": recall, "f1_score": f1_score}

    def evaluate_spf(
        self,
        test: PySparkDataFrame,
        prediction: Iterable,
        weight: PySparkDataFrame = None,
        *args,
        **kwargs
    ):
        precisions = []
        recalls = []

        for true_ls, pred_ls in zip(
            ColToList().get_ls(test, self.test_value_col), prediction
        ):
            if self.k:
                true_ls = true_ls[: self.k]
                pred_ls = pred_ls[: self.k]
            true_df = (
                SPFrame.get_spark()
                .createDataFrame([(token,) for token in true_ls], ["token"])
                .withColumn("true", F.lit(1))
            )
            pred_df = (
                SPFrame.get_spark()
                .createDataFrame([(token,) for token in pred_ls], ["token"])
                .withColumn("pred", F.lit(1))
            )

            eval_precision = pred_df.join(true_df, on="token", how="left")
            eval_precision = eval_precision.fillna(0, subset=["true"])

            eval_recall = true_df.join(pred_df, on="token", how="left")
            eval_recall = eval_recall.fillna(0, subset=["pred"])

            if weight is not None:
                eval_precision = eval_precision.join(
                    weight,
                    on=eval_precision["token"] == weight[self.weight_token_col],
                    how="left",
                )
                eval_precision = eval_precision.fillna({self.weight_value_col: 0})
                eval_recall = eval_recall.join(
                    weight,
                    on=eval_recall["token"] == weight[self.weight_token_col],
                    how="left",
                )
                eval_recall = eval_recall.fillna({self.weight_value_col: 0})
            else:
                eval_precision = eval_precision.withColumn(
                    self.weight_value_col, F.lit(1)
                )
                eval_recall = eval_recall.withColumn(self.weight_value_col, F.lit(1))

            precision = precision_score(
                ColToList().get_ls(eval_precision, "true"),
                ColToList().get_ls(eval_precision, "pred"),
                sample_weight=ColToList().get_ls(eval_precision, self.weight_value_col),
            )
            recall = recall_score(
                ColToList().get_ls(eval_recall, "true"),
                ColToList().get_ls(eval_recall, "pred"),
                sample_weight=ColToList().get_ls(eval_recall, self.weight_value_col),
            )
            precisions.append(precision)
            recalls.append(recall)

        precision = np.mean(precisions)
        recall = np.mean(recalls)
        f1_score = 2 * precision * recall / (precision + recall)
        return {"precision": precision, "recall": recall, "f1_score": f1_score}
