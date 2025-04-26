from typing import Any
from typing import Dict

import pandas
import pyspark
import pyspark.sql.types


def pandas_to_spark(
    spark: pyspark.sql.session.SparkSession, pandas_df: pandas.DataFrame, **kwargs: Dict[str, Any]
) -> pyspark.sql.DataFrame:
    # Prior to Spark 3.4, pyspark attempts to call iteritems when converting a pandas DF to a Spark DF. In Pandas 2.0,
    # iteritems() has been deleted, but items() does the same thing. We can patch over this incompatibility by copying
    # the pandas DF and aliasing iteritems to items.
    #
    # We can't easily check pyspark.__version__ directly, because databricks-connect installs a version of the pyspark
    # module which uses a different versioning scheme. Instead, we check for the existence of a symbol which was first
    # introduced in pyspark 3.4
    # TODO(liangqi): Check pyspark.__version__ directly when we migrate off of databricks-connect.
    is_old_pyspark = not hasattr(pyspark.sql.types, "JVMView")
    if not hasattr(pandas_df, "iteritems") and is_old_pyspark:
        pandas_df = pandas_df.copy(deep=False)
        pandas_df.iteritems = pandas_df.items
    return spark.createDataFrame(pandas_df, **kwargs)
