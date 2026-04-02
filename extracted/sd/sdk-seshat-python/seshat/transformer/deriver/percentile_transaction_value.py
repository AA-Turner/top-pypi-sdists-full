from typing import Dict

from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F
from pyspark.sql.types import IntegerType

from seshat.data_class import SFrame
from seshat.general import configs
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.transformer.deriver.base import SFrameDeriver
from seshat.utils import pandas_func
from seshat.utils.validation import NumericColumnValidator


class PercentileTransactionValueDeriver(SFrameDeriver):
    """
    Used to compute percentile of the specific column and insert result as a new column.

    Parameters
    ----------
    value_col: str
        The column that computing percentile will execute on it.
    quantile_probabilities: list of float
        List of quantile probabilities
    result_col: str
        Column name of result column
    """

    def __init__(
        self,
        group_keys=None,
        value_col=configs.AMOUNT_COL,
        result_col="percentile",
        quantile_probabilities=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9),
    ):
        super().__init__(group_keys)

        self.value_col = value_col
        self.result_col = result_col
        self.quantile_probabilities = quantile_probabilities

    def calculate_complexity(self):
        return 2

    def validate(self, sf: SFrame):
        super().validate(sf)
        self._validate_columns(sf, self.default_sf_key, self.value_col)

    def derive_df(self, default: DataFrame, *args, **kwargs) -> Dict[str, DataFrame]:
        default = NumericColumnValidator().validate(default, self.value_col)

        quantiles = default[self.value_col].quantile(
            self.quantile_probabilities, interpolation="linear"
        )
        percentile = pandas_func.PandasPercentile(
            quantiles, self.quantile_probabilities
        )
        default[self.result_col] = default[self.value_col].apply(percentile)
        return {"default": default}

    def derive_spf(
        self, default: PySparkDataFrame, *args, **kwargs
    ) -> Dict[str, PySparkDataFrame]:
        default = NumericColumnValidator().validate(default, self.value_col)

        quantiles = default.approxQuantile(
            self.value_col, self.quantile_probabilities, 0.05
        )

        def get_percentile(value):
            for i, quantile in enumerate(quantiles):
                if value <= quantile:
                    return int(self.quantile_probabilities[i] * 100)
            return 100

        get_percentile_udf = F.udf(get_percentile, IntegerType())
        default = default.withColumn(
            self.result_col, get_percentile_udf(F.col(self.value_col))
        )
        return {"default": default}


class PercentileTransactionValueDeriverStory(BaseTransformerStory):
    transformer = PercentileTransactionValueDeriver
    use_cases = [
        "Assign a percentile rank to each wallet based on its average interaction amount.",
        (
            "Flag token contracts whose transaction counts meet or exceed the "
            "80th‑percentile threshold (selection of the flagged tokens for further "
            "analysis or trimming is performed by a separate transformer)."
        ),
    ]
    logic_overview = (
        "The deriver turns a continuous numeric column into an ordinal feature that "
        "indicates where each value sits within the overall distribution (for "
        "example, bottom 10%, median, top 10%)."
    )
    steps = [
        "Verify that the chosen value column exists and contains numbers or can be converted to numbers.",
        (
            "Determine the threshold values that split the data into equal‑probability "
            "segments according to the quantile list provided (for example deciles "
            "at 10% intervals)."
        ),
        (
            "Create a mapping that assigns each raw value the percentile label "
            "corresponding to the smallest threshold it meets or exceeds; the "
            "greatest values receive 100."
        ),
        "Apply this mapping to every row and store the resulting label in a new column named by result_col.",
        "Return the modified default SFrame, leaving any other SFrames unchanged.",
    ]
    tags = ["deriver", "multi-sf-operation"]

    def get_scenarios(self):
        from test.transformer.deriver.test_percentile_transaction_value import (
            PercentileTransactionValueDFTestCase,
        )

        return TransformerScenario.from_testcase(
            PercentileTransactionValueDFTestCase, transformer=self.transformer
        )
