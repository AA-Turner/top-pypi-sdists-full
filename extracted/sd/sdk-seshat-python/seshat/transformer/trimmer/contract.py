from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F

from seshat.general import configs
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
    safe_import_testcase,
)
from seshat.transformer.trimmer import SFrameTrimmer


class ContractTrimmer(SFrameTrimmer):
    """
    This trimmer will be used to based on the function find the top contract address and just
    keep these contract addresses and drop all others.

    Parameters
    ----------
    contract_list_fn : callable
        The function that is used to find contract addresses
    contract_list_args : tuple
        The args that passed to contract list func
    contract_list_kwargs : dict
        The awards that must be passed to the contract list func
    exclude: bool
        The flag that shows the condition computed contract address must be kept to exclude
    contract_address_col : str
        The column of contract address in default sframe
    """

    def __init__(
        self,
        contract_list_fn,
        group_keys=None,
        contract_list_args=(),
        contract_list_kwargs=None,
        exclude=False,
        contract_address_col=configs.CONTRACT_ADDRESS_COL,
    ):
        super().__init__(group_keys)

        if contract_list_kwargs is None:
            contract_list_kwargs = {}

        self.contract_list_fn = contract_list_fn
        self.contract_list_args = contract_list_args
        self.contract_list_kwargs = contract_list_kwargs
        self.exclude = exclude
        self.contract_address_col = contract_address_col

    def calculate_complexity(self):
        return 1

    def trim_df(self, default: DataFrame, *args, **kwargs):
        contract_list = self.contract_list_fn(
            default, *self.contract_list_args, **self.contract_list_kwargs
        )
        condition = default[self.contract_address_col].isin(contract_list)
        if self.exclude:
            condition = ~condition
        default = default[condition]
        return {"default": default}

    def trim_spf(self, default: PySparkDataFrame, *args, **kwargs):
        contract_list = self.contract_list_fn(
            default, *self.contract_list_args, **self.contract_list_kwargs
        )

        condition = F.col(self.contract_address_col).isin(contract_list)
        if self.exclude:
            condition = ~condition
        default = default.filter(condition)
        return {"default": default}


class ContractTrimmerStory(BaseTransformerStory):
    transformer = ContractTrimmer
    use_cases = [
        "In Ethereum transaction data, retain only popular contract addresses or "
        "exclude them depending on the configuration."
    ]
    logic_overview = (
        "Run the `contract_list_fn` on the raw DataFrame from the default key in "
        "the input SFrame. This function returns a list of contract addresses. "
        "Rows are then filtered based on this list: either kept or removed "
        "depending on the `exclude` flag."
    )
    steps = [
        "Call `contract_list_fn` with the default data, along with "
        "`contract_list_args` and `contract_list_kwargs`.",
        "If `exclude=True`, remove all rows where the contract address is in the "
        "returned list.",
        "If `exclude=False`, keep only the rows where the contract address is in "
        "the returned list.",
    ]
    tags = ["trimmer", "single-sf-operation"]

    def get_scenarios(self):
        testcase = safe_import_testcase("test", "ContractTrimmerDFTestCase")
        if testcase is None:
            return []
        return TransformerScenario.from_testcase(testcase, transformer=self.transformer)
