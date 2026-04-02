import pandas as pd
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F

from seshat.data_class import SFrame, SPFrame
from seshat.general import configs
from seshat.transformer.deriver.base import SFrameDeriver
from seshat.transformer.schema import Schema, Col


class ProfitLossDeriver(SFrameDeriver):
    """
    Find the profit and loss of addresses with this logic:
    Sum over all buying and selling amount & amount USD, then find the difference between
    buy & sell amount for each address & token. By using the token price sframe the current amount
    of address property will be calculated. The difference between USD that address paid and
    the current amount is the PL for that address & token.

    Parameters
    ----------
    from_address_col : str
        The name of from address column in default sf.
    to_address_col : str
        The name of to address column in default sf.
    contract_address_col : str
        The name of contract address column in default sf.
    timestamp_col : str
        The name of block_timestamp column in default sf.
    amount_col : str
        The name of amount column in default sf.
    amount_usd_col : str
        The name of USD amount column of transactions in default sf.
    token_price_col : str
        The name of price column in price sf.
    address_col : str
        The name of address column in result sf.
    net_amount_col : str
        The name of net amount column in result sf.
    net_amount_usd_col : str
        The name of USD net amount column in result sf.
    current_amount_usd_col : str
        The name of USD amount column in result sf.
    pl_col : str
        The name of profit & loss column in result sf.
    group_keys
        Group keys for the parent Transformer class.
    *args
        Additional positional arguments.
    **kwargs
        Additional keyword arguments.
    """

    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "price": configs.TOKEN_PRICE_SF_KEY,
        "result": configs.PROFIT_LOSS_SF_KEY,
    }

    def __init__(
        self,
        from_address_col=configs.FROM_ADDRESS_COL,
        to_address_col=configs.TO_ADDRESS_COL,
        contract_address_col=configs.CONTRACT_ADDRESS_COL,
        timestamp_col=configs.BLOCK_TIMESTAMP_COL,
        amount_col=configs.AMOUNT_COL,
        amount_usd_col=configs.AMOUNT_USD_COL,
        token_price_col=configs.TOKEN_PRICE_COL,
        address_col=configs.ADDRESS_COL,
        net_amount_col="net_amount",
        net_amount_usd_col="net_amount_usd",
        current_amount_usd_col="current_amount_usd",
        pl_col="pl",
        group_keys=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.from_address_col = from_address_col
        self.to_address_col = to_address_col
        self.contract_address_col = contract_address_col
        self.timestamp_col = timestamp_col
        self.amount_col = amount_col
        self.amount_usd_col = amount_usd_col
        self.token_price_col = token_price_col
        self.address_col = address_col
        self.net_amount_col = net_amount_col
        self.net_amount_usd_col = net_amount_usd_col
        self.current_amount_usd_col = current_amount_usd_col
        self.pl_col = pl_col

    def calculate_complexity(self):
        return 15

    def validate(self, sf: SFrame):
        super().validate(sf)
        self._validate_columns(
            sf,
            "default",
            self.from_address_col,
            self.to_address_col,
            self.contract_address_col,
            self.timestamp_col,
            self.amount_col,
            self.amount_usd_col,
        )

    def derive_df(self, default: pd.DataFrame, price: pd.DataFrame, *args, **kwargs):
        clean_default = default[default[self.amount_col] != 0]
        selling = (
            clean_default.groupby([self.from_address_col, self.contract_address_col])
            .agg({self.amount_col: "sum", self.amount_usd_col: "sum"})
            .reset_index()
            .rename(
                columns={
                    self.from_address_col: self.address_col,
                    self.amount_col: "sell_amount",
                    self.amount_usd_col: "sell_amount_usd",
                }
            )
        )
        buying = (
            clean_default.groupby([self.to_address_col, self.contract_address_col])
            .agg({self.amount_col: "sum", self.amount_usd_col: "sum"})
            .reset_index()
            .rename(
                columns={
                    self.to_address_col: self.address_col,
                    self.amount_col: "buy_amount",
                    self.amount_usd_col: "buy_amount_usd",
                }
            )
        )
        investing = pd.merge(
            selling, buying, on=[self.address_col, self.contract_address_col]
        )
        del selling
        del buying
        investing[self.net_amount_col] = (
            investing["buy_amount"] - investing["sell_amount"]
        )
        investing[self.net_amount_usd_col] = (
            investing["buy_amount_usd"] - investing["sell_amount_usd"]
        )
        investing = investing[
            [
                self.address_col,
                self.contract_address_col,
                self.net_amount_col,
                self.net_amount_usd_col,
            ]
        ]
        investing = investing[investing[self.net_amount_col] >= 0]

        investing = investing.merge(price, on=self.contract_address_col)
        investing[self.current_amount_usd_col] = (
            investing[self.net_amount_col] * investing[self.token_price_col]
        )

        investing[self.pl_col] = (
            investing[self.current_amount_usd_col] - investing[self.net_amount_usd_col]
        )
        investing = investing.drop(columns=[self.token_price_col])

        return {"default": default, "price": price, "result": investing}

    def derive_spf(
        self, default: PySparkDataFrame, price: PySparkDataFrame, *args, **kwargs
    ):
        clean_default = default.filter(F.col(self.amount_col) != 0)
        selling = (
            clean_default.groupBy([self.from_address_col, self.contract_address_col])
            .agg({self.amount_col: "sum", self.amount_usd_col: "sum"})
            .withColumnRenamed(self.from_address_col, self.address_col)
            .withColumnRenamed(f"sum({self.amount_col})", "sell_amount")
            .withColumnRenamed(f"sum({self.amount_usd_col})", "sell_amount_usd")
        )

        buying = (
            clean_default.groupBy([self.to_address_col, self.contract_address_col])
            .agg({self.amount_col: "sum", self.amount_usd_col: "sum"})
            .withColumnRenamed(self.to_address_col, self.address_col)
            .withColumnRenamed(f"sum({self.amount_col})", "buy_amount")
            .withColumnRenamed(f"sum({self.amount_usd_col})", "buy_amount_usd")
        )

        investing = selling.join(
            buying, on=[self.address_col, self.contract_address_col]
        )

        investing = investing.withColumn(
            self.net_amount_col, investing["buy_amount"] - investing["sell_amount"]
        ).withColumn(
            self.net_amount_usd_col,
            investing["buy_amount_usd"] - investing["sell_amount_usd"],
        )

        investing = investing.select(
            self.address_col,
            self.contract_address_col,
            self.net_amount_col,
            self.net_amount_usd_col,
        )
        investing = investing.filter(F.col(self.net_amount_col) >= 0)
        investing = investing.join(price, on=self.contract_address_col)

        investing = Schema(
            exclusive=False,
            cols=[
                Col(self.net_amount_col, dtype="double"),
                Col(self.net_amount_usd_col, dtype="double"),
                Col(self.token_price_col, dtype="double"),
            ],
        )(SPFrame.from_raw(investing)).to_raw()

        investing = investing.withColumn(
            self.current_amount_usd_col,
            investing[self.net_amount_col] * investing[self.token_price_col],
        )
        investing = investing.withColumn(
            self.pl_col,
            investing[self.current_amount_usd_col] - investing[self.net_amount_usd_col],
        )
        investing = investing.drop(self.token_price_col)
        return {"default": default, "price": price, "result": investing}
