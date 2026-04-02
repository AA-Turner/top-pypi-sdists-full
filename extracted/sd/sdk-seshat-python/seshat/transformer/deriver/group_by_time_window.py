import pandas as pd
from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.transformer.deriver.base import SFrameDeriver


class GroupByTimeWindowDeriver(SFrameDeriver):
    """
    GroupBy Time Window Deriver will provide aggregation over different columns and different time windows.
    """

    def __init__(
        self,
        group_keys=None,
        by_columns=None,
        agg_column=None,
        time_column=None,
        window_list=None,
        func_list=None,
        new_agg_column_list=None,
        output_name=None,
    ):
        super().__init__(group_keys)

        self.by_columns = by_columns
        self.agg_column = agg_column
        self.time_column = time_column
        self.window_list = window_list
        self.func_list = func_list
        self.new_agg_column_list = new_agg_column_list
        if output_name is None:
            self.output_name = "agg_window_time"
        else:
            self.output_name = output_name

    def derive_df(self, default: DataFrame, *args, **kwargs):
        if (
            self.by_columns is not None
            and self.agg_column is not None
            and self.time_column is not None
            and self.window_list is not None
            and self.func_list is not None
        ):

            merged_df = None
            for window, func, new_agg_column in zip(
                self.window_list,
                self.func_list,
                self.new_agg_column_list,
            ):

                # Set the start time of the window
                latest_time = default[self.time_column].max()
                start_time = latest_time - window
                filtered_df = default[(default[self.time_column] >= start_time)]

                if func == "count":
                    agg_df = (
                        filtered_df.groupby(self.by_columns)[self.agg_column]
                        .count()
                        .reset_index()
                    )
                elif func == "max":
                    agg_df = (
                        filtered_df.groupby(self.by_columns)[self.agg_column]
                        .max()
                        .reset_index()
                    )
                else:
                    agg_df = (
                        filtered_df.groupby(self.by_columns)[self.agg_column]
                        .mean()
                        .reset_index()
                    )

                agg_df = agg_df.fillna(0)

                agg_df.rename(columns={self.agg_column: new_agg_column}, inplace=True)

                if merged_df is None:
                    merged_df = agg_df
                else:
                    merged_df = pd.merge(
                        merged_df, agg_df, on=self.by_columns, how="outer"
                    ).fillna(0)

            return {"default": default, self.output_name: merged_df}
        else:
            return {"default": default}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        # ToDo: add spf
        return {"default": default}
