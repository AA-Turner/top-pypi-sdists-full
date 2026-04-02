from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.utils.mixin import RawHandlerDispatcherMixin
from seshat.utils.singleton import Singleton


class ColToList(RawHandlerDispatcherMixin, metaclass=Singleton):
    HANDLER_NAME = "get_col_ls"

    def get_ls(self, raw: object, col: str):
        return self.call_handler(raw, col)

    def get_col_ls_df(self, raw: DataFrame, col: str):
        return list(raw[col].tolist())

    def get_col_ls_spf(self, raw: PySparkDataFrame, col: str):
        return raw.select(col).rdd.flatMap(lambda x: x).collect()
