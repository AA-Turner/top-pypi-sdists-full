from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F

from seshat.general import configs
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
    safe_import_testcase,
)
from seshat.transformer.trimmer import SFrameTrimmer


class ZeroAddressTrimmer(SFrameTrimmer):
    """
    This trimmer will remove zero address from input sframe.
    """

    def __init__(
        self,
        group_keys=None,
        address_cols=None,
        zero_address=configs.ZERO_ADDRESS,
    ):
        super().__init__(group_keys, address_cols)

        self.zero_address = zero_address
        if address_cols is None:
            self.address_cols = [configs.FROM_ADDRESS_COL, configs.TO_ADDRESS_COL]
        else:
            self.address_cols = address_cols

    def calculate_complexity(self):
        return 1

    def trim_df(self, default: DataFrame, *args, **kwargs):
        for address_col in self.address_cols:
            default = default[default[address_col] != self.zero_address]

        default.reset_index(inplace=True, drop=True)
        return {"default": default}

    def trim_spf(self, default: PySparkDataFrame):
        for address_col in self.address_cols:
            default = default.filter(F.col(address_col) != self.zero_address)

        return {"default": default}


class ZeroAddressTrimmerStory(BaseTransformerStory):
    transformer = ZeroAddressTrimmer
    use_cases = ["Remove zero address of ethereum network from transactions data"]
    logic_overview = (
        "Remove rows that one of their `address_cols` are equal to zero address"
    )
    steps = [
        "Loop over each address in `address_cols` and remove the rows that their "
        "address_col are equal to zero address",
    ]
    tags = ["trimmer", "single-sf-operation"]

    def get_scenarios(self):
        testcase = safe_import_testcase("test", "ZeroAddressTrimmerDFTestCase")
        if testcase is None:
            return []
        return TransformerScenario.from_testcase(testcase, transformer=self.transformer)
