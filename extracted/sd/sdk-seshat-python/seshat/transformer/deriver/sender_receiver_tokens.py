import pandas as pd
from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame
from pyspark.sql.types import StructType, StructField

from seshat.data_class import SPFrame
from seshat.general import configs
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
    safe_import_testcase,
)
from seshat.transformer.deriver.base import SFrameDeriver
from seshat.transformer.vectorizer import CosineSimilarityVectorizer


class SenderReceiverTokensDeriver(SFrameDeriver):
    """
    This will find tokens that in at least one record be from_address or to_address.
    The result will save in another sf.

    Parameters
    ----------
    address_cols : tuple of str
        A tuple containing the names of the 'from address' and 'to address' columns in the default SFrame.
    contract_address_col : str
        The name of the column containing contract addresses (tokens) in the default SFrame.
    result_col : str
        The name of the column in the resulting SFrame that will store the identified sender/receiver tokens.
    """

    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "other": configs.OTHER_SF_KEY,
    }

    def __init__(
        self,
        group_keys=None,
        address_cols=(configs.FROM_ADDRESS_COL, configs.TO_ADDRESS_COL),
        contract_address_col=configs.CONTRACT_ADDRESS_COL,
        result_col=configs.CONTRACT_ADDRESS_COL,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.address_cols = address_cols
        self.contract_address = contract_address_col
        self.result_col = result_col

    def calculate_complexity(self):
        return 2

    def derive_df(self, default: DataFrame, *args, **kwargs):
        all_tokens = set(default[self.contract_address].tolist())
        addresses = set()
        for address_col in self.address_cols:
            addresses |= set(default[address_col].tolist())

        sender_receiver_tokens = list(addresses & all_tokens)
        other = pd.DataFrame(data={self.result_col: sender_receiver_tokens})
        return {"default": default, "other": other}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        all_tokens = set(
            default.select(self.contract_address).rdd.flatMap(lambda x: x).collect()
        )
        addresses = set()
        for address_col in self.address_cols:
            addresses |= set(
                default.select(address_col).rdd.flatMap(lambda x: x).collect()
            )

        sender_receiver_tokens = list(addresses & all_tokens)
        schema = StructType(
            [
                StructField(
                    self.result_col, default.schema[self.contract_address].dataType
                )
            ]
        )

        data = [{self.result_col: addr} for addr in sender_receiver_tokens]
        other = SPFrame.get_spark().createDataFrame(schema=schema, data=data)
        return {"default": default, "other": other}


class SenderReceiverTokensDeriverStory(BaseTransformerStory):
    transformer = SenderReceiverTokensDeriver
    use_cases = ["Extract contracts that take part directly in transfers."]
    logic_overview = (
        "A token contract sometimes appears in the sender or receiver field of a "
        "transaction. This deriver pinpoints such contracts by comparing the set "
        "of all contract addresses with the set of all participants in the address "
        "columns."
    )
    steps = [
        "Collect the full list of contract addresses recorded for the transactions.",
        "Collect the distinct addresses that appear in the specified sender and receiver columns.",
        (
            "Compute the intersection of these two lists to isolate contracts that "
            "also occur as transaction participants."
        ),
        (
            "Create a new SFrame (labelled by the ‘other’ group key) that holds one "
            "row per matched contract address under result_col."
        ),
        (
            "Return the untouched default SFrame together with the new SFrame of "
            "sender‑receiver token contracts."
        ),
    ]
    validation_summaries = [
        (
            "Ensure group_keys maps a key named 'other' where the resulting token "
            "list will be stored."
        ),
    ]
    tags = ["deriver", "multi-sf-operation"]

    def get_scenarios(self):
        testcase = safe_import_testcase("test", "SenderReceiverTokensDFTestCase")
        if testcase is None:
            return []
        return TransformerScenario.from_testcase(testcase, transformer=self.transformer)

    interactions = [
        (
            CosineSimilarityVectorizer,
            "The tokens that this deriver founded, are used when using CosineSimilarityVectorizer, "
            "this vectorizer accept a exclusion, the tokens that drop from the vector. "
            "So it usually should placed before CosineSimilarityVectorizer to the vectorizer can use it's result",
        )
    ]
