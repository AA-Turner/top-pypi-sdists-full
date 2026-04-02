import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype
from pyspark.sql import functions as F
from pyspark.sql.types import NumericType

from seshat.utils.mixin import RawHandlerDispatcherMixin
from seshat.utils.singleton import Singleton


class Validator(RawHandlerDispatcherMixin, metaclass=Singleton):
    HANDLER_NAME = "validate"

    def validate(self, raw: object, col: str):
        return self.call_handler(raw, col)


class NumericColumnValidator(Validator):
    HANDLER_NAME = "validate"

    def validate_df(self, raw, col):
        if not is_numeric_dtype(raw[col]):
            raw[col] = pd.to_numeric(raw[col], errors="coerce")
        return raw

    def validate_spf(self, raw, col):
        if not isinstance(raw.schema[col].dataType, NumericType):
            raw = raw.withColumn(col, F.col(col).cast("double"))
        return raw


class TimeStampColumnValidator(Validator):
    def validate_df(self, raw, col):
        raw[col] = pd.to_datetime(raw[col], errors="raise")
        return raw

    def validate_spf(self, raw, col):
        raw = raw.withColumn(col, F.to_timestamp(F.col(col)))
        return raw
