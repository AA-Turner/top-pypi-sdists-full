from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.transformer.deriver.base import SFrameDeriver


class GroupByDeriverCount(SFrameDeriver):
    """
    GroupBy Deriver Count will provide aggregation over different columns.
    """

    def __init__(
        self,
        group_keys=None,
        by_columns: list = None,
        kept_column: list = None,
        output_name=None,
    ):
        super().__init__(group_keys)

        self.by_columns = by_columns
        self.kept_column = kept_column
        if output_name is None:
            self.output_name = "agg_count"
        else:
            self.output_name = output_name

    def derive_df(self, default: DataFrame, *args, **kwargs):
        if self.by_columns is not None:

            kept_column_tuples = [(item, "first") for item in self.kept_column]

            # Creating the aggregation dictionary dynamically
            agg_dict = {
                result_name: (col_name, agg_func)
                for (col_name, agg_func), result_name in zip(
                    kept_column_tuples, self.kept_column
                )
            }

            # Adding COUNT to the aggregation
            agg_dict["COUNT"] = (self.by_columns[0], "size")

            # Aggregating
            aggregated_df = (
                default.groupby(self.by_columns).agg(**agg_dict).reset_index()
            )

            return {"default": default, self.output_name: aggregated_df}
        else:
            return {"default": default}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        # ToDo: add spf
        return {"default": default}
