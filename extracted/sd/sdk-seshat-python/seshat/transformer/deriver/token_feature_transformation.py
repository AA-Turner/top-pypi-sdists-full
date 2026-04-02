from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.general import configs
from seshat.transformer.deriver.base import SFrameDeriver


class TokenFeatureTransformationDeriver(SFrameDeriver):
    """
    This will create a dataframe with different token features from price and swap trades.
    """

    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "token_price_df": "token_price_df",
    }

    def __init__(
        self,
        group_keys=None,
        output_name=None,
        time_intervals_trade=None,
        time_intervals_price=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        if output_name is None:
            self.output_name = "token_feature_transformation_df"
        else:
            self.output_name = output_name
        self.time_intervals_trade = time_intervals_trade
        self.time_intervals_price = time_intervals_price

    def derive_df(self, default: DataFrame, token_price_df: DataFrame, *args, **kwargs):
        epsilon = 1e-10  # Small constant to prevent division by zero

        df = token_price_df.copy()

        for interval_label in self.time_intervals_price["ago_labels"]:
            df[f"Price_Change_Percentage_{interval_label}"] = (
                df["CURRENT_PRICE"] - df[f"PRICE_{interval_label}"]
            ) / df[f"PRICE_{interval_label}"]

        for interval_label in self.time_intervals_trade["last_labels"]:
            df[f"Buy_to_Sell_Volume_Ratio_{interval_label}"] = df[
                f"VOLUME_INFLOW_{interval_label}"
            ] / (df[f"VOLUME_OUTFLOW_{interval_label}"] + epsilon)

            df[f"Buy_to_Sell_Trade_Count_Ratio_{interval_label}"] = df[
                f"TRADE_COUNT_INFLOW_{interval_label}"
            ] / (df[f"TRADE_COUNT_OUTFLOW_{interval_label}"] + epsilon)

            df[f"TRADE_COUNT_TOTAL_{interval_label}"] = (
                df[f"TRADE_COUNT_INFLOW_{interval_label}"]
                + df[f"TRADE_COUNT_OUTFLOW_{interval_label}"]
            )

            df[f"TRADE_COUNT_PERCENTAGE_OVERALL_{interval_label}"] = (
                df[f"TRADE_COUNT_TOTAL_{interval_label}"]
                / df[f"TRADE_COUNT_TOTAL_{interval_label}"].sum()
            )

            # this is the column I will use to filter and remove low liquidity tokens, so pick top 200
            df[f"TRADE_COUNT_RANK_OVERALL_{interval_label}"] = (
                df[f"TRADE_COUNT_PERCENTAGE_OVERALL_{interval_label}"]
                .rank(ascending=False, method="dense")
                .astype(int)
            )

        # this is the one that is used to rank tokens
        df["Profitability_Score"] = (
            0.5 * df["Price_Change_Percentage_6_hours_ago"]
            + 0.3 * df["Buy_to_Sell_Volume_Ratio_last_6_hours"]
            + 0.2 * df["Buy_to_Sell_Trade_Count_Ratio_last_6_hours"]
        )

        df = df.fillna(0)

        # Round all decimal values to four decimal places
        df = df.round(4)

        # Filter and remove all tokens with the Price of 0
        df = df[df["CURRENT_PRICE"] > 0]

        # Convert all column names to lowercase
        df.columns = df.columns.str.lower()

        return {"default": default, self.output_name: df}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        # ToDo: add spf
        return {"default": default}
