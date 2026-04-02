import pandas as pd
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F

from seshat.data_class import SFrame
from seshat.general import configs
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.transformer.deriver.base import SFrameDeriver
from seshat.utils.validation import NumericColumnValidator


class FractionDeriver(SFrameDeriver):
    """
    Find fraction that each rows have from sum of all calculation columns values.

    Parameters
    ----------
    calculation_col : str
        The column that every value of it divide by sum of it over all rows
    result_fraction_col : str
        The column name for result fraction values
    group_keys
        Group keys for the parent Transformer class.
    *args
        Additional positional arguments.
    **kwargs
        Additional keyword arguments.
    """

    DEFAULT_GROUP_KEYS = {
        "default": configs.TOKEN_SF_KEY,
    }

    def __init__(
        self,
        calculation_col: str,
        result_fraction_col: str = "weight",
        group_keys=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.calculation_col = calculation_col
        self.result_fraction_col = result_fraction_col

    def calculate_complexity(self):
        return 2

    def validate(self, sf: SFrame):
        super().validate(sf)
        self._validate_columns(sf, self.default_sf_key, self.calculation_col)

    def derive_df(self, default: pd.DataFrame, *args, **kwargs):
        default = NumericColumnValidator().validate(default, self.calculation_col)
        default[self.calculation_col] = default[self.calculation_col].fillna(0)
        total_value = default[self.calculation_col].sum()

        default[self.result_fraction_col] = default[self.calculation_col] / total_value
        return {"default": default}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        default = NumericColumnValidator().validate(default, self.calculation_col)
        default = default.fillna(0, subset=[self.calculation_col])
        total_value = default.agg(F.sum(self.calculation_col)).collect()[0][0]
        default = default.withColumn(
            self.result_fraction_col, F.col(self.calculation_col) / F.lit(total_value)
        )
        return {"default": default}


class FractionDeriverStory(BaseTransformerStory):
    transformer = FractionDeriver
    use_cases = [
        (
            "We have an SFrame that contains tokens and the count of people who "
            "interacted with each one."
        ),
        (
            "This transformer can calculate what proportion of the total interactions "
            "each token represents"
        ),
    ]
    logic_overview = (
        "Based on the self.calculation_col, find the sum of them and for each row "
        "divide the value of it with calculated sum."
    )
    steps = [
        "First validate that the `calculation_col` is numeric",
        "Fill nan values to 0",
        "Find the sum of them",
        "For each row divide the value of it with calculated sum",
    ]
    tags = ["deriver", "single-sf-operation"]

    def get_scenarios(self):
        from test.transformer.deriver.test_fraction import FractionDeriverDFTestCase

        return TransformerScenario.from_testcase(
            FractionDeriverDFTestCase, transformer=self.transformer
        )
