from typing import Dict, Callable

from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.source.database import SQLDBSource
from seshat.transformer.deriver.base import SFrameDeriver


class FromSQLDBDeriver(SFrameDeriver):
    """
    This transformer derive new column by fetching data from sql database source find
    """

    DEFAULT_GROUP_KEYS = {"default": "default", "result": "result"}

    def __init__(
        self,
        source: SQLDBSource,
        base_col: str = None,
        query: str = None,
        get_query_fn: Callable = None,
        get_query_fn_kwargs=None,
        filters: dict = None,
        merge_result: bool = True,
        merge_how: str = "left",
        group_keys=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        if get_query_fn_kwargs is None:
            get_query_fn_kwargs = {}
        if filters is None:
            filters = {}
        self.get_query_fn_kwargs = get_query_fn_kwargs
        self.source = source
        self.get_query_fn = get_query_fn
        self.query = query
        self.filters = filters
        self.base_col = base_col
        self.merge_result = merge_result
        self.merge_how = merge_how

    def derive_df(self, default: DataFrame, *args, **kwargs) -> Dict["str", DataFrame]:
        db_result = self.get_from_source(default, *args, **kwargs)
        if self.merge_result:
            default = default.merge(
                right=db_result, on=self.base_col, how=self.merge_how
            )
            return {"default": default}
        return {"default": default, "result": db_result}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        db_result = self.get_from_source(default, *args, **kwargs)
        if self.merge_result:
            default = default.join(db_result, on=self.base_col, how=self.merge_how)
            return {"default": default}
        return {"default": default, "result": db_result}

    def get_from_source(self, default, *args, **kwargs):
        self.source.query = self.query or self.get_query_fn(
            default, *args, **kwargs, **self.get_query_fn_kwargs
        )
        self.source.filters = self.filters
        return self.source().to_raw()

    def calculate_complexity(self):
        return 30
