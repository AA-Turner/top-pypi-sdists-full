from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.general import configs
from seshat.transformer.deriver.base import SFrameDeriver


class OneColumnPercentileFilterDeriver(SFrameDeriver):
    """
    OneColumnPercentileFilterDeriver
    """

    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "count_aggregated_df": "count_aggregated_df",
    }

    def __init__(
        self,
        group_keys=None,
        column_name=None,
        percentile=0.9,
        output_name=None,
    ):
        super().__init__(group_keys)

        self.column_name = column_name
        self.percentile = percentile
        if output_name is None:
            self.output_name = "percentile_filter"
        else:
            self.output_name = output_name

    def derive_df(
        self, default: DataFrame, count_aggregated_df: DataFrame, *args, **kwargs
    ):
        if self.column_name is not None:
            # Calculate the percentile
            percentile_value = count_aggregated_df[self.column_name].quantile(
                self.percentile
            )

            # Filter the DataFrame
            top_percent_df = count_aggregated_df[
                count_aggregated_df[self.column_name] >= percentile_value
            ]

            return {"default": default, self.output_name: top_percent_df}
        else:
            return {"default": default}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        # ToDo: add spf
        return {"default": default}
