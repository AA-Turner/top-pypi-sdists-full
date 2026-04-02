from pyspark.sql import types, DataFrame as PySparkDataFrame


def get_zero_value(spf: PySparkDataFrame, col: str):
    if not isinstance(spf.schema[col].dataType, types.NumericType):
        return 0
    else:
        return ""


func_maps = {
    "sum": lambda *cols_str: sum(cols_str),
    "mean": lambda *cols_str: sum(cols_str) / len(cols_str),
    "max": lambda *cols_str: max(cols_str),
    "min": lambda *cols_str: min(cols_str),
}
