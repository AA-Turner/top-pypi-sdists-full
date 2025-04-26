from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class FilterContext:
    """`FilterContext` is passed as an argument to the data source function when `supports_time_filtering` is set to `True`. Using these parameters enables optimized query patterns for improved performance:

     - The method `<data source>.get_dataframe()` can be invoked with the arguments `start_time` or `end_time`.
     - When defining a Feature View, a FilteredSource can be paired with a Data Source. The Feature View will then pass FilterContext into the Data Source Function

    Note that Data Source Functions are expected to implement their own filtering logic.

    ```python
    from tecton import spark_batch_config
    from pyspark.sql.functions import col

    @spark_batch_config(supports_time_filtering=True)
    def hive_data_source_function(spark, filter_context):
        spark.sql(f"USE {hive_db_name}")
        df = spark.table(user_hive_table)
        ts_column = "timestamp"

        # Data Source Function handles its own filtering logic here
        if filter_context:
            if filter_context.start_time:
                df = df.where(col(ts_column) >= filter_context.start_time)
            if filter_context.end_time:
                df = df.where(col(ts_column) < filter_context.end_time)
        return df
    ```

    :param start_time: If specified, data source will only include items with timestamp column >= start_time
    :param end_time: If specified, data source will only include items with timestamp column < end_time


    """

    start_time: Optional[datetime]
    end_time: Optional[datetime]
