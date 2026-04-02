import pandas as pd
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F, Window

from seshat.general import configs
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
    safe_import_testcase,
)
from seshat.transformer.deriver.base import SFrameDeriver
from seshat.utils.validation import TimeStampColumnValidator


class TokenLastPriceDeriver(SFrameDeriver):
    """
    This deriver finds the last usd unit price for every token if there is not zero and no null amount USD.
    To find the last price deriver needs to sort values based on the timestamp column.
    If dtype of this column is something
    except for valid datetime type, the column values will be converted to the proper type.

    Parameters
    ----------
    contract_address_col : str
        The name of the column containing contract addresses (tokens) in the default SFrame.
    timestamp_col : str
        The name of the timestamp column in the default SFrame, used for ordering.
    amount_col : str
        The name of the column representing the token amount in the default SFrame.
    amount_usd_col : str
        The name of the column representing the USD amount of the token in the default SFrame.
    result_unit_price_col : str
        The name of the column in the resulting SFrame that will store the calculated unit price.
    """

    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "result": configs.TOKEN_PRICE_SF_KEY,
    }

    def __init__(
        self,
        contract_address_col=configs.CONTRACT_ADDRESS_COL,
        timestamp_col=configs.BLOCK_TIMESTAMP_COL,
        amount_col=configs.AMOUNT_COL,
        amount_usd_col=configs.AMOUNT_USD_COL,
        result_unit_price_col=configs.TOKEN_PRICE_COL,
        group_keys=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.contract_address_col = contract_address_col
        self.timestamp_col = timestamp_col
        self.amount_col = amount_col
        self.amount_usd_col = amount_usd_col
        self.result_unit_price_col = result_unit_price_col

    def calculate_complexity(self):
        return 1

    def derive_df(self, default: pd.DataFrame, *args, **kwargs):
        default = TimeStampColumnValidator().validate(default, self.timestamp_col)
        price = default[default[self.amount_usd_col] != 0]
        price = price.sort_values(self.timestamp_col, ascending=False)
        price = price.dropna(subset=[self.amount_usd_col])
        last_price = (
            price.groupby([self.contract_address_col]).head(1).reset_index(drop=True)
        ).reset_index(drop=True)

        last_price[self.result_unit_price_col] = (
            last_price["amount_usd"] / last_price["amount"]
        )
        last_price = last_price[[self.contract_address_col, self.result_unit_price_col]]
        return {"default": default, "result": last_price}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        default = TimeStampColumnValidator().validate(default, self.timestamp_col)
        price: PySparkDataFrame = default.filter(
            F.col(self.amount_usd_col) != 0
        ).select(
            self.timestamp_col,
            self.contract_address_col,
            self.amount_usd_col,
            self.amount_col,
        )
        price = price.dropna(subset=[self.amount_usd_col])
        window = Window.partitionBy(self.contract_address_col).orderBy(
            F.col(self.timestamp_col).desc()
        )
        last_price = (
            price.withColumn("_row_number", F.row_number().over(window))
            .filter(F.col("_row_number") == 1)
            .drop("_row_number")
        )
        last_price = last_price.withColumn(
            self.result_unit_price_col,
            last_price[self.amount_usd_col] / last_price[self.amount_col],
        )
        last_price = last_price.select(
            self.contract_address_col, self.result_unit_price_col
        )
        return {"default": default, "result": last_price}


class TokenLastPriceDeriverStory(BaseTransformerStory):
    transformer = TokenLastPriceDeriver
    use_cases = ["Find the last price of a token in transactions data"]
    logic_overview = (
        "Each token in transactions data seen one or several times, first transformer "
        "should make sure that there is timestamp column and sort the data descending "
        "based on it. Then for each contract address find head and this is the last "
        "price."
    )
    steps = [
        "Validate the `timestamp_col` is a column with datetime type",
        "Remove rows that their amount_usd_col are zero or null, their are invalid rows.",
        "Sort the data descending based on timestamp_col",
        "Group by the data on contract address and get the head for each one.",
        "Now to finding the unit price, divide amount_usd with amount for each token",
        (
            "Store the result in different sframe with two columns: contract_address "
            "and result_unit_price, these two are defines by user as args of "
            "transformer"
        ),
    ]
    tags = ["deriver", "multi-sf-operation"]

    def get_scenarios(self):
        testcase = safe_import_testcase("test", "TokenLastPriceDeriverDFTestCase")
        if testcase is None:
            return []
        return TransformerScenario.from_testcase(testcase, transformer=self.transformer)
