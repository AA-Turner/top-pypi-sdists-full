from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.general import configs
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
    safe_import_testcase,
)
from seshat.transformer.trimmer import SFrameTrimmer


class FeatureTrimmer(SFrameTrimmer):
    """
    Feature Trimmer will drop all columns except the feature columns that get as params.
    """

    def __init__(self, group_keys=None, columns=None):
        super().__init__(group_keys)

        if columns is None:
            self.columns = [
                configs.CONTRACT_ADDRESS_COL,
                configs.FROM_ADDRESS_COL,
                configs.TO_ADDRESS_COL,
                configs.AMOUNT_PRICE_COL,
                configs.BLOCK_NUM_COL,
            ]
        else:
            self.columns = columns

    def calculate_complexity(self):
        return 1

    def trim_df(self, default: DataFrame, *args, **kwargs):
        default = default.drop(
            [col for col in default.columns if col not in set(self.columns)],
            axis=1,
        )
        return {"default": default}

    def trim_spf(self, default: PySparkDataFrame, *args, **kwargs):
        default = default.select(*self.columns)
        return {"default": default}


class FeatureTrimmerStory(BaseTransformerStory):
    transformer = FeatureTrimmer
    use_cases = ["There is large sframe and just few of columns needed"]
    logic_overview = "Simple drop on input sframe that just keep the input columns"
    steps = ["Drop the columns that are not present in self.columns from input sframe"]
    tags = ["trimmer", "single-sf-operation"]

    def get_scenarios(self):
        testcase = safe_import_testcase("test", "FeatureTrimmerDFTestCase")
        if testcase is None:
            return []
        return TransformerScenario.from_testcase(testcase, transformer=self.transformer)
