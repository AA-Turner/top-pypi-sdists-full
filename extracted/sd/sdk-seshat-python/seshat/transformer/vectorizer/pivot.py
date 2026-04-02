from typing import Dict, List

import pandas as pd
from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import (
    FloatType,
)
from sklearn.preprocessing import MinMaxScaler

from seshat.data_class import SPFrame
from seshat.data_class.pandas import DFrame
from seshat.general import configs
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.transformer.vectorizer.base import SFrameVectorizer
from seshat.transformer.vectorizer.utils import AggregationStrategy, CountStrategy


class TokenPivotVectorizer(SFrameVectorizer):
    """
    Vectorizes SFrame data by pivoting based on specified address columns and
    aggregating token counts or values using a given strategy.

    This transformer takes an SFrame and by default transforms it into a vector representation
    where rows represent addresses and columns represent tokens (e.g., contract addresses). The aggregation
    method (e.g., count, sum, boolean) is determined by the `strategy` parameter.
    Optionally, the resulting vectors can be normalized.

    Parameters
    ----------
    strategy : AggregationStrategy
        The aggregation strategy to use for pivoting (default is CountStrategy).
    address_cols : List[str
        A list of column names in the input SFrame that contain addresses to pivot on
        (default is configs.FROM_ADDRESS_COL, configs.TO_ADDRESS_COL).
    result_address_col : str
        The name of the column in the output vector SFrame that will contain the
        unique addresses (default is configs.ADDRESS_COL).
    should_normalize : bool
        Whether to normalize the resulting vectors using MinMaxScaler (default is True).
    col_prefix : str
        A prefix to add to the generated token columns in the output vector SFrame
        (default is "token_").
    """

    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "vector": configs.VECTOR_SF_KEY,
    }

    def __init__(
        self,
        strategy: AggregationStrategy = CountStrategy(),
        address_cols: List[str] = (configs.FROM_ADDRESS_COL, configs.TO_ADDRESS_COL),
        result_address_col: str = configs.ADDRESS_COL,
        should_normalize: bool = False,  # Change default to False
        col_prefix: str = "token_",
        group_keys=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.strategy = strategy
        self.address_cols = address_cols
        self.should_normalize = should_normalize
        self.col_prefix = col_prefix
        self.result_address_col = result_address_col

    def vectorize_df(
        self, default: DataFrame = None, *args, **kwargs
    ) -> Dict[str, DataFrame]:
        pivots = [
            self.strategy(
                DFrame.from_raw(default), addr, token_column=f"{self.col_prefix}{addr}"
            )
            for addr in self.address_cols
        ]

        vector = (
            pivots[0].fillna(0)
            if len(pivots) == 1
            else pd.merge(*pivots, on=self.result_address_col, how="outer").fillna(0)
        )

        if self.should_normalize:
            vector = self.normalize_df(vector)

        return {"default": default, "vector": vector}

    def vectorize_spf(
        self, default: PySparkDataFrame, *args, **kwargs
    ) -> Dict[str, DataFrame]:
        pivots = [
            self.strategy(
                SPFrame.from_raw(default), addr, token_column=f"{self.col_prefix}{addr}"
            )
            for addr in self.address_cols
        ]
        vector = pivots[0]
        for pivot in pivots[1:]:
            vector = vector.join(pivot, on=self.result_address_col, how="outer")
        vector = vector.na.fill(0)
        if self.should_normalize:
            vector = self.normalize_spf(vector)

        return {"default": default, "vector": vector}

    @staticmethod
    def normalize_df(vector: DataFrame) -> DataFrame:
        scaler = MinMaxScaler()
        columns_to_normalize = vector.columns[1:]
        normalized = scaler.fit_transform(vector[columns_to_normalize])
        normalized = pd.DataFrame(normalized, columns=columns_to_normalize)
        vector = pd.concat(
            [vector.drop(columns=columns_to_normalize), normalized], axis=1
        )
        return vector

    @staticmethod
    def normalize_spf(vector: PySparkDataFrame) -> PySparkDataFrame:
        columns_to_normalize = [
            col for col in vector.columns if col != configs.ADDRESS_COL
        ]

        agg_exprs = [F.min(col).alias(f"{col}_min") for col in columns_to_normalize] + [
            F.max(col).alias(f"{col}_max") for col in columns_to_normalize
        ]
        min_max_row = vector.agg(*agg_exprs).collect()[0]

        for col_name in columns_to_normalize:
            min_val = min_max_row[f"{col_name}_min"]
            max_val = min_max_row[f"{col_name}_max"]
            range_val = max_val - min_val

            if range_val == 0:
                vector = vector.withColumn(col_name, F.lit(0.0).cast(FloatType()))
            else:
                vector = vector.withColumn(
                    col_name,
                    ((F.col(col_name) - min_val) / range_val).cast(FloatType()),
                )

        return vector


class PivotVectorizerStory(BaseTransformerStory):
    transformer = TokenPivotVectorizer
    use_cases = [
        "To transform transaction data into a vector representation where rows are addresses and columns "
        "represent tokens (e.g., contract addresses). To prepare data for similarity calculations "
    ]
    logic_overview = (
        "Pivots the input SFrame based on specified address columns and aggregates "
        "values from pivot columns (default: contract addresses) using a defined strategy "
        "(count, sum, boolean). The result is a new SFrame where addresses are rows "
        "and aggregated token values are columns. Optionally, the resulting vectors can be normalized."
    )
    steps = [
        "Iterate through the specified `address_cols`.",
        "For each address column, pivot the input SFrame using the address column as the index "
        "and the `pivot_columns` (default: contract address) as columns.",
        "Aggregate the values using the configured `strategy` (Count, Sum, or Bool).",
        "Merge the pivoted results from all `address_cols` based on the resulting address column.",
        "Fill any missing values (NaN) with 0.",
        "If `should_normalize` is True, apply MinMaxScaler to the vector columns.",
        "Return the original default SFrame and the newly created vector SFrame.",
    ]
    tags = ["vectorizer", "single-sf-operation"]

    def get_scenarios(self):
        from test.transformer.vectorizer import TokenPivotVectorizerDFTestCase

        return TransformerScenario.from_testcase(
            TokenPivotVectorizerDFTestCase, transformer=self.transformer
        )
