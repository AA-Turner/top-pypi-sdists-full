from typing import List, Dict

from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F

from seshat.data_class import SFrame
from seshat.general import configs
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.transformer.deriver.base import SFrameDeriver
from seshat.utils import pandas_func, pyspark_func
from seshat.utils.validation import NumericColumnValidator


class FeatureForAddressDeriver(SFrameDeriver):
    """
    This class is responsible for adding a new column as a new feature to address the sframe
    based on the default sframe.

    Parameters
    ----------
    default_index_col : str
        Columns that group by default will be applied based on this column.
    address_index_col: str
        Column in the address that must be matched to address_col in default sframe.
        Joining default and address sframe using this column and address_col to
        join new column to address.
    result_col : str
        Column name for a new column in address sframe
    agg_func: str
        Function name that aggregation operates based on it. For example count, sum, mean, etc.
    """

    ONLY_GROUP = True
    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "address": configs.ADDRESS_SF_KEY,
    }

    def __init__(
        self,
        value_col,
        group_keys=None,
        default_index_col: str | List[str] = configs.FROM_ADDRESS_COL,
        address_index_col: str | List[str] = configs.ADDRESS_COL,
        result_col="result_col",
        agg_func="mean",
        is_numeric=True,
    ):
        super().__init__(group_keys)

        self.value_col = value_col
        self.default_index_col = default_index_col
        self.address_index_col = address_index_col
        self.result_col = result_col
        self.agg_func = agg_func
        self.is_numeric = is_numeric

    def calculate_complexity(self):
        return 5

    def validate(self, sf: SFrame):
        super().validate(sf)
        self._validate_columns(sf, self.group_keys["default"], self.value_col)
        if isinstance(self.address_index_col, list):
            self._validate_columns(
                sf, self.group_keys["address"], *self.address_index_col
            )
        else:
            self._validate_columns(
                sf, self.group_keys["address"], self.address_index_col
            )

    def derive_df(
        self, default: DataFrame, address: DataFrame, *args, **kwargs
    ) -> Dict[str, DataFrame]:
        if self.is_numeric:
            NumericColumnValidator().validate(default, self.value_col)

        zero_value = pandas_func.get_zero_value(default[self.value_col])
        default.fillna({self.value_col: zero_value}, inplace=True)

        df_agg = (
            default.groupby(self.default_index_col)[self.value_col]
            .agg(self.agg_func)
            .reset_index(name=self.result_col)
        )

        if isinstance(self.default_index_col, str):
            should_dropped = [self.default_index_col]
        else:
            should_dropped = set(self.default_index_col) - set(self.address_index_col)

        address = address.merge(
            df_agg,
            right_on=self.default_index_col,
            left_on=self.address_index_col,
            how="left",
        ).drop(should_dropped, axis=1)

        result_zero_value = pandas_func.get_zero_value(address[self.result_col])
        address.fillna({self.result_col: result_zero_value}, inplace=True)
        return {"default": default, "address": address}

    def derive_spf(
        self, default: PySparkDataFrame, address: PySparkDataFrame, *args, **kwargs
    ) -> Dict[str, PySparkDataFrame]:
        try:
            func = getattr(F, self.agg_func)
        except AttributeError:
            raise AttributeError(
                "agg func %s not available for pyspark dataframe" % self.agg_func
            )
        if self.is_numeric:
            default = NumericColumnValidator().validate(default, self.value_col)

        zero_value = pyspark_func.get_zero_value(default, self.value_col)
        default = default.fillna({self.value_col: zero_value})

        agg_value = (
            default.groupBy(self.default_index_col)
            .agg(func(F.col(self.value_col)).alias(self.result_col))
            .withColumnRenamed(self.default_index_col, self.address_index_col)
        )
        address = address.join(agg_value, on=self.address_index_col, how="left")
        zero_value = pyspark_func.get_zero_value(address, self.result_col)
        address = address.fillna(zero_value, subset=[self.result_col])

        return {"default": default, "address": address}


class FeatureForAddressDeriverStory(BaseTransformerStory):
    transformer = FeatureForAddressDeriver
    use_cases = [
        "Count unique token‑transfer transactions initiated or received by each wallet address.",
        "Compute the average value of tokens sent or received by each wallet address.",
        (
            "For every token contract, count the number of unique receiver addresses, "
            "distinct transfer transactions it has interacted with or the average "
            "transfer amount across all its transactions"
        ),
    ]
    logic_overview = (
        "default sframe is the sframe that describe the transactions and address "
        "sframe is a sframe that contains addresses. In fact is use aggregations "
        "on transactions and merge the result to address sframe."
    )
    steps = [
        (
            "Because it use aggregations to derive feature, shuold know that this "
            "aggregation is on numeric values or not. If are it validate that columns "
            "are numeric and if they're not try to convert them."
        ),
        (
            "After the value columns that feature will derive from it should fill "
            "the null values with zero value. The zero value automatically find from "
            "the type of columns. For number it's 0 and for other they're ''"
        ),
        (
            "Start to aggregating. Group the default sframe (transactions data) on "
            "default_index_col. This index col can be single col or list of them. "
            "By default it is FROM_ADDRESS column. After that run agregation on "
            "value_col. The reuslt are save on new column that names is `result_col`."
        ),
        (
            "Now it's time to merge the driverd feature with address sframe. In this "
            "case the default_index_col is left_on and the address_index_col is "
            "right_on. The default_index_col and address_index_col are the those "
            "that connect default and address sframe to each other."
        ),
    ]
    tags = ["deriver", "multi-sf-operation"]

    def get_scenarios(self):
        from test.transformer.deriver.test_feature_for_address import (
            FeatureForAddressDeriverDFTestCase,
        )

        return TransformerScenario.from_testcase(
            FeatureForAddressDeriverDFTestCase, transformer=self.transformer
        )

    interactions = [
        (
            "SFrameFromColsDeriver",
            "Feature for address deriver needs a address sframe to find the feature for it. "
            "So deriving this transformer usually happens by SFrameFromColsDeriver first. "
            "So often FeatureFOrAddressDeriver is used after SFrameFromColsDeriver.",
        ),
    ]
