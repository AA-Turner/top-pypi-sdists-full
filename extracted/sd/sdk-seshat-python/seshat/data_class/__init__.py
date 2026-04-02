from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame

from .base import SFrame, GroupSFrame
from .pandas import DFrame
from .pyspark import SPFrame

SF_MAP = {DFrame.frame_name: DFrame, SPFrame.frame_name: SPFrame}
RAW_MAP = {DFrame.frame_name: DataFrame, SPFrame.frame_name: PySparkDataFrame}
