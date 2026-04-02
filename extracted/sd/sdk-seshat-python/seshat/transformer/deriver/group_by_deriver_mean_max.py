from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.transformer.deriver.base import SFrameDeriver


class GroupByDeriverMeanMax(SFrameDeriver):
    """
    GroupBy Deriver will provide aggregation over different columns.
    """

    def __init__(
        self,
        group_keys=None,
        function=None,
        by_columns=None,
        agg_column=None,
        output_name=None,
    ):
        super().__init__(group_keys)

        if function is None:
            self.function = "mean"
        else:
            self.function = function
        self.by_columns = by_columns
        self.agg_column = agg_column
        if output_name is None:
            self.output_name = "agg_" + self.function
        else:
            self.output_name = output_name

    def derive_df(self, default: DataFrame, *args, **kwargs):
        if self.by_columns is not None and self.agg_column is not None:

            # ToDo: cover more aggregated function
            if self.function == "max":
                agg_df = (
                    default.groupby(self.by_columns)[self.agg_column]
                    .max()
                    .reset_index()
                )
            else:
                agg_df = (
                    default.groupby(self.by_columns)[self.agg_column]
                    .mean()
                    .reset_index()
                )
            agg_df = agg_df.fillna(0)

            agg_df = agg_df.rename(
                columns={self.agg_column: self.agg_column + "-" + self.function}
            )

            return {"default": default, self.output_name: agg_df}
        else:
            return {"default": default}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        # ToDo: add spf
        return {"default": default}
