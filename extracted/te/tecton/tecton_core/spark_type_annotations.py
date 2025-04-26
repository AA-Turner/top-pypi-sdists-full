from typing import Union

# The `pyspark.sql.connect.*` classes are the default for the Notebooks on Databricks Shared Access Mode Clusters of
# Version 14.3 or higher. That's why we need to support them.
from pyspark.sql import SparkSession


try:
    from pyspark.sql.connect.session import SparkSession as ConnectSparkSession
except ImportError:
    ConnectSparkSession = SparkSession

from pyspark.sql.dataframe import DataFrame


try:
    from pyspark.sql.connect.dataframe import DataFrame as ConnectDataFrame
except ImportError:
    ConnectDataFrame = DataFrame

from pyspark.sql import Column


try:
    from pyspark.sql.connect.column import Column as ConnectColumn
except ImportError:
    ConnectColumn = Column

PySparkSession = Union[SparkSession, ConnectSparkSession]
PySparkDataFrame = Union[DataFrame, ConnectDataFrame]
PySparkColumn = Union[Column, ConnectColumn]


#################
# It is invalid to isinstance check a subscripted generic type (e.g. a Union[foo,bar]), so here are some
# convenience methods.
#################
def is_pyspark_session(inst):
    return isinstance(inst, (ConnectSparkSession, SparkSession))


def is_pyspark_df(inst):
    return isinstance(inst, (ConnectDataFrame, DataFrame))


def is_pyspark_column(inst):
    return isinstance(inst, (Column, ConnectColumn))
