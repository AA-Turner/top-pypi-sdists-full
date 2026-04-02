from typing import Dict

from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F
from pyspark.sql.functions import coalesce, array, array_distinct, array_union

from seshat.data_class import SFrame, GroupSFrame, DFrame, SPFrame
from seshat.general import configs
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.transformer.deriver.base import SFrameDeriver
from seshat.transformer.deriver.feature_for_address import FeatureForAddressDeriver

SYMBOLS_RECEIVED_COL = "symbols_received"
SYMBOLS_SENT_COL = "symbols_sent"


class InteractedSymbolsToSentenceDeriver(SFrameDeriver):
    """
    This deriver joins symbols that each user in address sframe
    be interacted with it into a new column in string type.
    If already sent symbols or received symbols are calculated as an array of symbol strings
    deriver use them otherwise compute these columns.

    Parameters
    ----------
    symbol_col: str
        Column name of a symbol column in default sframe
    from_address_col: str
        Column name of from address column in default sframe
    to_address_col: str
        Column name of to address column in default sframe
    address_address_col: str
        Column name of address column in address sframe. This column
        consider as a joining condition between default and address sframe
    sent_symbols_col : str
        Column name for the result of sent symbols column in address sframe. If this parameter is set to None
        sent symbols are computed and this value as a new column name.
    received_symbols_col : str
        Column name for the result of received symbols column in address sframe. If this parameter is set to None
        received symbols are computed and this value is a new column name.
    total_symbols_col : str
        Column name for merged two columns sent_symbols and received_symbols.
    result_col: str
        Column name of interacted symbols column
    """

    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "address": configs.ADDRESS_SF_KEY,
    }

    def __init__(
        self,
        group_keys=None,
        symbol_col: str = configs.SYMBOL_COL,
        from_address_col: str = configs.FROM_ADDRESS_COL,
        to_address_col: str = configs.TO_ADDRESS_COL,
        address_address_col: str = configs.ADDRESS_COL,
        sent_symbols_col: str = None,
        received_symbols_col: str = None,
        total_symbols_col: str = None,
        result_col: str = None,
    ):
        super().__init__(group_keys)

        self.symbol_col = symbol_col
        self.from_address_col = from_address_col
        self.to_address_col = to_address_col
        self.address_address_col = address_address_col
        self.sent_symbols_col = sent_symbols_col
        self.received_symbols_col = received_symbols_col
        self.total_symbols_col = total_symbols_col
        self.result_col = result_col

    def calculate_complexity(self):
        return 5

    def validate(self, sf: SFrame):
        super().validate(sf)
        if self.sent_symbols_col is None:
            self._validate_columns(sf, self.default_sf_key, self.from_address_col)
        if self.received_symbols_col is None:
            self._validate_columns(sf, self.default_sf_key, self.to_address_col)

    def derive_df(
        self, address: DataFrame, default: DataFrame = None, *args, **kwargs
    ) -> Dict[str, DataFrame]:
        if self.sent_symbols_col is None:
            group_sf = GroupSFrame(
                children={
                    "default": DFrame.from_raw(default),
                    "address": DFrame.from_raw(address),
                }
            )

            address = (
                FeatureForAddressDeriver(
                    self.symbol_col,
                    self.group_keys,
                    self.from_address_col,
                    self.address_address_col,
                    SYMBOLS_SENT_COL,
                    "unique",
                    is_numeric=False,
                )(group_sf)
                .get(self.group_keys["address"])
                .to_raw()
            )

        if self.received_symbols_col is None:
            group_sf = GroupSFrame(
                children={
                    "default": DFrame.from_raw(default),
                    "address": DFrame.from_raw(address),
                }
            )
            address = (
                FeatureForAddressDeriver(
                    self.symbol_col,
                    self.group_keys,
                    self.to_address_col,
                    self.address_address_col,
                    SYMBOLS_RECEIVED_COL,
                    "unique",
                    is_numeric=False,
                )(group_sf)
                .get(self.group_keys["address"])
                .to_raw()
            )

        final_sent_col = self.sent_symbols_col or SYMBOLS_SENT_COL
        final_received_col = self.received_symbols_col or SYMBOLS_RECEIVED_COL

        address[final_sent_col] = address[final_sent_col].fillna("").apply(list)
        address[final_received_col] = address[final_received_col].fillna("").apply(list)

        address[self.result_col] = address.apply(
            lambda row: ", ".join(set(row[final_sent_col] + row[final_received_col])),
            axis=1,
        )
        return {"default": default, "address": address}

    def derive_spf(
        self,
        address: PySparkDataFrame,
        default: PySparkDataFrame = None,
        *args,
        **kwargs,
    ) -> Dict[str, PySparkDataFrame]:
        if self.sent_symbols_col is None:
            group_sframe = GroupSFrame(
                children={
                    "default": SPFrame.from_raw(default),
                    "address": SPFrame.from_raw(address),
                }
            )

            address = (
                FeatureForAddressDeriver(
                    self.symbol_col,
                    self.group_keys,
                    self.from_address_col,
                    self.address_address_col,
                    SYMBOLS_SENT_COL,
                    "collect_set",
                    is_numeric=False,
                )(group_sframe)
                .get(self.group_keys["address"])
                .to_raw()
            )

        if self.received_symbols_col is None:
            group_sframe = GroupSFrame(
                children={
                    "default": SPFrame.from_raw(default),
                    "address": SPFrame.from_raw(address),
                }
            )
            address = (
                FeatureForAddressDeriver(
                    self.symbol_col,
                    self.group_keys,
                    self.to_address_col,
                    self.address_address_col,
                    SYMBOLS_RECEIVED_COL,
                    "collect_set",
                    is_numeric=False,
                )(group_sframe)
                .get(self.group_keys["address"])
                .to_raw()
            )
        final_sent_col = self.sent_symbols_col or SYMBOLS_SENT_COL
        final_received_col = self.received_symbols_col or SYMBOLS_RECEIVED_COL

        address = address.withColumn(
            final_sent_col, coalesce(final_received_col, array())
        )

        address = address.withColumn(
            self.result_col,
            F.concat_ws(
                ", ",
                array_distinct(array_union(final_received_col, final_sent_col)),
            ),
        )

        return {"default": default, "address": address}


class InteractedSymbolsToSentenceDeriverStory(BaseTransformerStory):
    transformer = InteractedSymbolsToSentenceDeriver
    use_cases = [
        "Combine pre‑computed arrays of sent and received symbols into a single descriptive string per wallet"
    ]
    logic_overview = (
        "For each address, identify the complete set of token symbols it has touched "
        "as either a sender or a receiver, remove duplicates, and join the unique "
        "symbols into a comma‑separated sentence stored in a new column."
    )
    steps = [
        (
            "Check the presence of prerequisite columns. If arrays of sent or received "
            "symbols are not provided, fall back on the raw transaction SFrame to "
            "build them by grouping transfers on the address field and collecting "
            "unique symbols."
        ),
        (
            "Ensure both interaction arrays exist in the address SFrame. Missing ones "
            "are created and filled with empty lists when no data are available."
        ),
        (
            "For each address, merge the two arrays, discard duplicate symbols, sort "
            "or otherwise stabilise the order if desired, and concatenate the symbols "
            "with commas and spaces to form a human‑readable sentence."
        ),
        (
            "Store this sentence in the column named by result_col and return the "
            "updated address SFrame together with the untouched default SFrame."
        ),
    ]
    validation_summaries = [
        (
            "If sent_symbols_col is absent, verify that from_address_col and "
            "symbol_col exist in the transaction (default) SFrame in order to "
            "compute the sent list."
        ),
        (
            "If received_symbols_col is absent, verify that to_address_col and "
            "symbol_col exist in the transaction SFrame."
        ),
    ]
    tags = ["deriver", "single-sf-operation", "ethereum"]

    def get_scenarios(self):
        from test.transformer.deriver.test_interacted_symbols_to_sentence import (
            InteractedSymbolsToSentenceDFTestCase,
        )

        return TransformerScenario.from_testcase(
            InteractedSymbolsToSentenceDFTestCase, transformer=self.transformer
        )

    interactions = [
        (
            "FeatureForAddressDeriver, "
            "This deriver need a interacted tokens, this data usually come from "
            "FeatureForAddressDeriver. So usually this deriver is placed after that "
            "FeatureForAddressDeriver find the interacted tokens for each address",
        )
    ]
