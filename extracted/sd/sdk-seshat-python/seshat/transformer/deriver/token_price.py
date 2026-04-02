import pandas as pd
from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.general import configs
from seshat.transformer.deriver.base import SFrameDeriver


class tokenPriceDeriver(SFrameDeriver):
    """
    This will create a dataframe with aggregated price data per token.
    """

    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "token_swap_trade_df": "token_swap_trade_df",
    }

    def __init__(
        self,
        group_keys=None,
        output_name=None,
        time_intervals_price=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        if output_name is None:
            self.output_name = "token_price_df"
        else:
            self.output_name = output_name
        self.time_intervals_price = time_intervals_price

    def derive_df(
        self, default: DataFrame, token_swap_trade_df: DataFrame, *args, **kwargs
    ):

        # PRICE DATA
        # ToDo Fix this: how to read multiple source files at the beginning?
        import os

        df = pd.read_csv(os.getenv("CSV_EZ_PRICES_HOURLY"))
        df.rename(columns={"TOKEN_ADDRESS": "TOKEN", "HOUR": "TIME"}, inplace=True)
        df = df[["TOKEN", "TIME", "PRICE"]]

        # Ensure data is sorted by TOKEN and TIME
        df = df.sort_values(by=["TOKEN", "TIME"]).reset_index(drop=True)

        # Create the new dataframe with the required columns
        result = df.copy()
        result["CURRENT_PRICE"] = result["PRICE"]

        for interval_label, hour_value in zip(
            self.time_intervals_price["ago_labels"],
            self.time_intervals_price["hour_values"],
        ):
            result[f"PRICE_{interval_label}"] = result.groupby("TOKEN")["PRICE"].shift(
                hour_value
            )

        # Keep only the latest row for each TOKEN
        final_df_price = result.groupby("TOKEN").last().reset_index()

        # Remove TIME and PRICE from the final result
        final_df_price = final_df_price.drop(columns=["TIME", "PRICE"])

        # MERGE price and trade

        # Merge the two dataframes on TOKEN
        final_merged_df = pd.merge(
            token_swap_trade_df, final_df_price, on="TOKEN", how="inner"
        )
        final_merged_df.rename(columns={"TOKEN": "TOKEN_ADDRESS"}, inplace=True)
        final_merged_df.rename(
            columns={"SYMBOL": "TOKEN_COIN_NAME_SYMBOL"}, inplace=True
        )

        return {"default": default, self.output_name: final_merged_df}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        # ToDo: add spf
        return {"default": default}
