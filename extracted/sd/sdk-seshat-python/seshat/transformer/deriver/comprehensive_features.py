from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.general import configs
from seshat.transformer.deriver.base import SFrameDeriver


class ComprehensiveFeaturesDeriver(SFrameDeriver):
    """
    OneColumnPercentileFilterDeriver
    """

    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "count_aggregated_df": "count_aggregated_df",
        "filtered_count_aggregated_df": "filtered_count_aggregated_df",
    }

    def __init__(
        self,
        group_keys=None,
        output_name=None,
    ):
        super().__init__(group_keys)

        if output_name is None:
            self.output_name = "comprehensive"
        else:
            self.output_name = output_name

    def derive_df(
        self,
        default: DataFrame,
        count_aggregated_df: DataFrame,
        filtered_count_aggregated_df: DataFrame,
        *args,
        **kwargs,
    ):
        def calculate_features(df):
            # Group by TOKEN_ADDRESS to calculate features
            features = (
                df.groupby("TOKEN_ADDRESS")
                .agg(
                    SYMBOL=("SYMBOL", "first"),
                    total_transactions=("TOKEN_ADDRESS", "count"),
                    unique_from_wallets=("FROM_WALLET", "nunique"),
                    unique_to_wallets=("TO_WALLET", "nunique"),
                    total_volume_precise=("AMOUNT_PRECISE", "sum"),
                    total_volume_usd=("AMOUNT_USD", "sum"),
                    avg_transaction_size_precise=("AMOUNT_PRECISE", "mean"),
                    avg_transaction_size_usd=("AMOUNT_USD", "mean"),
                    median_transaction_size_precise=("AMOUNT_PRECISE", "median"),
                    median_transaction_size_usd=("AMOUNT_USD", "median"),
                    min_transaction_size_precise=("AMOUNT_PRECISE", "min"),
                    max_transaction_size_precise=("AMOUNT_PRECISE", "max"),
                    min_transaction_size_usd=("AMOUNT_USD", "min"),
                    max_transaction_size_usd=("AMOUNT_USD", "max"),
                    price_change=(
                        "TOKEN_PRICE",
                        lambda x: (x.iloc[-1] - x.iloc[0]) if len(x) > 1 else 0,
                    ),
                    price_volatility=("TOKEN_PRICE", "std"),
                    first_price=("TOKEN_PRICE", "first"),
                    last_price=("TOKEN_PRICE", "last"),
                    transaction_count_hourly=(
                        "BLOCK_TIMESTAMP",
                        lambda x: (
                            len(x) / ((x.max() - x.min()).total_seconds() / 3600)
                            if (x.max() > x.min())
                            else len(x)
                        ),
                    ),
                )
                .reset_index()
            )

            # Add calculated features that need multiple steps
            features["whale_transactions"] = (
                df[df["AMOUNT_USD"] > 10000].groupby("TOKEN_ADDRESS").size()
            )
            features["whale_transactions"] = (
                features["whale_transactions"].fillna(0).astype(int)
            )

            features["unique_wallets"] = (
                features["unique_from_wallets"] + features["unique_to_wallets"]
            )

            # Replace NaN with 0
            features = features.fillna(0)

            # Round all float columns to 2 decimal places
            features = features.round(2)

            return features

        default = default[
            default["TOKEN_ADDRESS"].isin(
                set(filtered_count_aggregated_df["TOKEN_ADDRESS"])
            )
        ]

        features_df = calculate_features(default)

        features_df = features_df.drop(columns=["TOKEN_ADDRESS"])

        return {"default": default, self.output_name: features_df}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        # ToDo: add spf
        return {"default": default}
