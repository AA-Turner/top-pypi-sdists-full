from datetime import timedelta

import pandas as pd
from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.transformer.deriver.base import SFrameDeriver


class TokenSwapTradeDeriver(SFrameDeriver):
    """
    This will create a dataframe with aggregated trade data per token.
    """

    def __init__(
        self,
        group_keys=None,
        output_name=None,
        time_intervals_trade=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        if output_name is None:
            self.output_name = "token_swap_trade_df"
        else:
            self.output_name = output_name
        self.time_intervals_trade = time_intervals_trade

    def derive_df(self, default: DataFrame, *args, **kwargs):

        # SWAP DATA
        df = default.copy()
        # Change columns names to make them compatible with general trading approach
        df.rename(
            columns={
                "AMOUNT_IN": "AMOUNT_OUTFLOW",
                "AMOUNT_OUT": "AMOUNT_INFLOW",
                "TOKEN_IN": "TOKEN_OUTFLOW",
                "TOKEN_OUT": "TOKEN_INFLOW",
                "SYMBOL_IN": "SYMBOL_OUTFLOW",
                "SYMBOL_OUT": "SYMBOL_INFLOW",
            },
            inplace=True,
        )
        df = df[
            [
                "BLOCK_TIMESTAMP",
                "AMOUNT_OUTFLOW",
                "AMOUNT_INFLOW",
                "TOKEN_OUTFLOW",
                "TOKEN_INFLOW",
                "SYMBOL_OUTFLOW",
                "SYMBOL_INFLOW",
            ]
        ]

        # Convert BLOCK_TIMESTAMP to datetime
        df["BLOCK_TIMESTAMP"] = pd.to_datetime(df["BLOCK_TIMESTAMP"])

        # Get the last timestamp in the dataframe
        last_timestamp = df["BLOCK_TIMESTAMP"].max()

        intervals = {}
        for interval_label, hour_value in zip(
            self.time_intervals_trade["last_labels"],
            self.time_intervals_trade["hour_values"],
        ):
            intervals[interval_label] = last_timestamp - timedelta(hours=hour_value)

        # Initialize the final dataframe
        final_df = pd.DataFrame()

        # Function to calculate metrics for a given time interval
        def calculate_metrics(interval_start, interval_label):
            filtered_df = df[df["BLOCK_TIMESTAMP"] >= interval_start]

            # Group by TOKEN_INFLOW and calculate metrics
            token_in_df = filtered_df.groupby("TOKEN_INFLOW", as_index=False).agg(
                VOLUME_INFLOW=("AMOUNT_INFLOW", "sum"),
                TRADE_COUNT_INFLOW=("TOKEN_INFLOW", "size"),
            )
            token_in_df.rename(columns={"TOKEN_INFLOW": "TOKEN"}, inplace=True)

            # Group by TOKEN_OUTFLOW and calculate metrics
            token_out_df = filtered_df.groupby("TOKEN_OUTFLOW", as_index=False).agg(
                VOLUME_OUTFLOW=("AMOUNT_OUTFLOW", "sum"),
                TRADE_COUNT_OUTFLOW=("TOKEN_OUTFLOW", "size"),
            )
            token_out_df.rename(columns={"TOKEN_OUTFLOW": "TOKEN"}, inplace=True)

            # Merge the two dataframes on TOKEN
            merged_df = pd.merge(token_in_df, token_out_df, on="TOKEN", how="outer")

            # Add SYMBOL using the first appearance of SYMBOL_INFLOW or SYMBOL_OUTFLOW
            symbol_map_in = (
                filtered_df.groupby("TOKEN_INFLOW")["SYMBOL_INFLOW"].first().to_dict()
            )
            symbol_map_out = (
                filtered_df.groupby("TOKEN_OUTFLOW")["SYMBOL_OUTFLOW"].first().to_dict()
            )
            symbol_map = {**symbol_map_out, **symbol_map_in}
            merged_df["SYMBOL"] = merged_df["TOKEN"].map(symbol_map)

            # Fill NaN values with 0 for counts and metrics
            merged_df.fillna(0, inplace=True)

            # Rename columns to include the interval label
            for column in [
                "VOLUME_INFLOW",
                "TRADE_COUNT_INFLOW",
                "VOLUME_OUTFLOW",
                "TRADE_COUNT_OUTFLOW",
            ]:
                merged_df.rename(
                    columns={column: f"{column}_{interval_label}"}, inplace=True
                )

            return merged_df

        # Process each interval and merge the results
        for interval_label, interval_start in intervals.items():
            metrics_df = calculate_metrics(interval_start, interval_label)
            if final_df.empty:
                final_df = metrics_df
            else:
                # Merge new metrics into the final dataframe
                final_df = pd.merge(
                    final_df, metrics_df, on=["TOKEN", "SYMBOL"], how="outer"
                )

        # Fill any remaining NaN values with 0
        final_df.fillna(0, inplace=True)

        # ToDo: remove duplicate token SYMBOLS: only keep the one with higher number of transactions

        return {"default": default, self.output_name: final_df}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        # ToDo: add spf
        return {"default": default}
