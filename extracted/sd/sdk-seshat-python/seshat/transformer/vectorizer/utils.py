from typing import List

from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame
from pyspark.sql import functions as F

from seshat.data_class import SFrame
from seshat.general import configs
from seshat.utils.mixin import SFHandlerDispatcherMixin


class AggregationStrategy(SFHandlerDispatcherMixin):
    HANDLER_NAME = "run"

    def __init__(
        self,
        address_col=configs.ADDRESS_COL,
        pivot_columns: List[str] = (configs.CONTRACT_ADDRESS_COL,),
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.address_col = address_col
        self.pivot_columns = pivot_columns

    def __call__(self, sf: SFrame, index_col, token_column=None, *args, **kwargs):
        return self.call_handler(
            sf,
            index_col,
            token_column,
            *args,
            **kwargs,
        )

    def run_df(
        self, raw: DataFrame, index_col, token_column, *args, **kwargs
    ) -> DataFrame:
        pivot = self._run_df(raw, index_col, *args, **kwargs)
        pivot = pivot.reset_index()
        pivot.columns.name = None

        prefix = self.get_columns_prefix(token_column)
        pivot.columns = [self.address_col] + [
            f"{prefix}{value}" for value in pivot.columns[1:]
        ]
        return pivot

    def run_spf(
        self,
        raw: PySparkDataFrame,
        index_col,
        token_column,
        *args,
        **kwargs,
    ):
        pivot = self._run_spf(raw, index_col, *args, **kwargs)
        prefix = self.get_columns_prefix(token_column)
        new_cols = [self.address_col] + [f"{prefix}{c}" for c in pivot.columns[1:]]
        for old_col, new_col in zip(pivot.columns, new_cols):
            pivot = pivot.withColumnRenamed(old_col, new_col)
        return pivot

    def _run_df(self, raw: DataFrame, index_col, *args, **kwargs):
        raise NotImplementedError()

    def _run_spf(self, raw: PySparkDataFrame, index_col, *args, **kwargs):
        raise NotImplementedError()

    def call_handler(self, sf: SFrame, *args, **kwargs):
        raw = sf.to_raw()
        return super().call_handler(sf, raw, *args, **kwargs)

    @staticmethod
    def get_columns_prefix(token_column):
        return f"{token_column}_" if token_column else ""


class CountStrategy(AggregationStrategy):
    def _run_df(self, raw: DataFrame, index_col, *args, **kwargs):
        return raw.pivot_table(
            index=index_col, columns=self.pivot_columns, aggfunc="size", fill_value=0
        )

    def _run_spf(self, raw: PySparkDataFrame, index_col, *args, **kwargs):
        return (
            raw.groupby(index_col)
            .pivot(*self.pivot_columns)
            .agg(F.count("*"))
            .na.fill(0)
        )


class SumStrategy(AggregationStrategy):
    def __init__(self, value_column: str = configs.AMOUNT_PRICE_COL, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value_column = value_column

    def _run_df(self, raw: DataFrame, index_col, *args, **kwargs):
        return raw.pivot_table(
            index=index_col,
            columns=self.pivot_columns,
            aggfunc="sum",
            values=self.value_column,
            fill_value=0,
        )

    def _run_spf(self, raw: PySparkDataFrame, index_col, *args, **kwargs):
        return (
            raw.groupby(index_col)
            .pivot(*self.pivot_columns)
            .agg(F.sum(self.value_column))
            .na.fill(0)
        )


class BoolStrategy(AggregationStrategy):

    def _run_df(self, raw: DataFrame, index_col, *args, **kwargs):
        pivot = raw.pivot_table(
            index=index_col, columns=self.pivot_columns, aggfunc="size", fill_value=0
        )
        pivot = pivot.apply(lambda col: col.map(lambda x: 1 if x > 0 else 0))
        return pivot

    def _run_spf(self, raw: PySparkDataFrame, index_col, *args, **kwargs):
        pivot = (
            raw.groupby(index_col)
            .pivot(*self.pivot_columns)
            .agg(F.count("*"))
            .na.fill(0)
        )
        for column in pivot.columns[1:]:
            pivot = pivot.withColumn(column, F.when(F.col(column) > 0, 1).otherwise(0))
        return pivot
