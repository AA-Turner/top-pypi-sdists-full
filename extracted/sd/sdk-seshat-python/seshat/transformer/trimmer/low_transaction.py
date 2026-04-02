from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F

from seshat.general import configs
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
    safe_import_testcase,
)
from seshat.transformer.trimmer import SFrameTrimmer


class LowTransactionTrimmer(SFrameTrimmer):
    """
    Responsible for drop addresses that has low transaction based on specified minimum.
    """

    def __init__(
        self,
        group_keys=None,
        address_cols=None,
        exclusive_on_each: bool = False,
        min_transaction_num: int = None,
        min_quantile: float = None,
    ):
        super().__init__(group_keys)
        if address_cols is None:
            self.address_cols = [configs.FROM_ADDRESS_COL, configs.TO_ADDRESS_COL]
        else:
            self.address_cols = address_cols
        self.exclusive_on_each = exclusive_on_each
        self.min_transaction_num = min_transaction_num
        self.min_quantile = min_quantile

    def calculate_complexity(self):
        return 1

    def trim_df(self, default: DataFrame, *args, **kwargs):
        unique_user_set = {}
        for address_col in self.address_cols:
            df_agg = default.groupby(address_col).size().reset_index(name="count")
            if self.min_transaction_num:
                df_agg = df_agg[df_agg["count"] >= self.min_transaction_num]
            elif self.min_quantile:
                threshold_min = df_agg["count"].quantile(self.min_quantile)
                df_agg = df_agg[df_agg["count"] > threshold_min]

            if self.exclusive_on_each:
                default = default[default[address_col].isin(df_agg[address_col])]
            else:
                unique_user_set = (
                    set(df_agg[address_col].unique())
                    if len(unique_user_set) == 0
                    else unique_user_set.intersection(set(df_agg[address_col].unique()))
                )

        if not self.exclusive_on_each:
            for address_col in self.address_cols:
                default = default[default[address_col].isin(unique_user_set)]
        default.reset_index(inplace=True, drop=True)
        return {"default": default}

    def trim_spf(self, default: PySparkDataFrame, *args, **kwargs):
        unique_user_set = set()
        for address_col in self.address_cols:
            agg = default.groupby(address_col).agg(F.count("*").alias("count"))

            if self.min_transaction_num:
                agg = agg.filter(F.col("count") >= self.min_transaction_num)
            elif self.min_transaction_num:
                threshold_min = agg.approxQuantile("count", [self.min_quantile], 0.05)[
                    0
                ]
                agg = agg.filter(F.col("count") > threshold_min)

            filtered = set(agg.select(address_col).rdd.flatMap(lambda x: x).collect())

            if self.exclusive_on_each:
                default = default.filter(F.col(address_col).isin(filtered))
            else:
                unique_user_set = (
                    filtered
                    if len(unique_user_set) == 0
                    else unique_user_set.intersection(filtered)
                )

        if not self.exclusive_on_each:
            unique_user_ls = list(unique_user_set)
            for address_col in self.address_cols:
                default = default.filter(F.col(address_col).isin(unique_user_ls))

        return {"default": default}


class LowTransactionTrimmerStory(BaseTransformerStory):
    transformer = LowTransactionTrimmer
    use_cases = [
        "In Ethereum transaction data, some addresses have very few transactions and should be "
        "removed to clean the dataset.",
    ]
    logic_overview = (
        "There are two filtering options: one based on a minimum number of "
        "transactions, and another based on a minimum quantile threshold. "
        "Addresses typically appear in two columns (`from_address` and `to_address`). "
        "You can choose to retain only addresses that meet the condition in both "
        "columns, or in either column. This behavior is controlled by the "
        "`exclusive_on_each` argument."
    )
    steps = [
        "Loop over each address and perform the following:",
        "If `min_transaction_num` is provided, keep only the rows where the address "
        "has at least this number of transactions.",
        "Otherwise, if `min_quantile` is provided, compute the transaction threshold "
        "based on the quantile, and keep rows with more transactions than this threshold.",
        "If `exclusive_on_each` is set to `True`, filter the SFrame separately for "
        "each column (e.g., `from_address`, `to_address`) during the iteration.",
        "If `exclusive_on_each` is set to `False`, store addresses that meet the "
        "condition in a hash set, then filter the SFrame by checking whether the "
        "address in each row is in this set.",
        "When `exclusive_on_each` is `False`, addresses passing the threshold in "
        "either column will be retained; others will be dropped.",
        "When `exclusive_on_each` is `True`, the filtering is already applied during "
        "the iteration step.",
    ]
    tags = ["trimmer", "single-sf-operation"]

    def get_scenarios(self):
        testcase = safe_import_testcase("test", "LowTransactionDFTestCase")
        if testcase is None:
            return []
        return TransformerScenario.from_testcase(testcase, transformer=self.transformer)
