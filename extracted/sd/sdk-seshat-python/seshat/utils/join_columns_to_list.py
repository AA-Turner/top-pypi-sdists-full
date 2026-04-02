from typing import List

import pandas as pd
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F

from seshat.utils.mixin import RawHandlerDispatcherMixin
from seshat.utils.singleton import Singleton


class JoinColumnsToList(RawHandlerDispatcherMixin, metaclass=Singleton):
    HANDLER_NAME = "join"

    def join(self, raw: object, selected_cols: List[str], result_col: str):
        return self.call_handler(raw, selected_cols, result_col)

    def join_df(self, raw: pd.DataFrame, selected_cols: List[str], result_col: str):
        raw[result_col] = raw.apply(
            lambda row: [row[col] for col in selected_cols], axis=1
        )
        return raw

    def join_spf(
        self, raw: PySparkDataFrame, selected_cols: List[str], result_col: str
    ):
        raw = raw.withColumn(
            result_col,
            F.array([F.col(c) for c in selected_cols]),
        )
        return raw
