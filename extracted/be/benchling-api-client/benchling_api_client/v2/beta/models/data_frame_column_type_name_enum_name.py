from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class DataFrameColumnTypeNameEnumName(Enums.KnownString):
    STRING = "String"
    INT = "Int"
    FLOAT = "Float"
    JSON = "JSON"
    DATETIME = "DateTime"
    DATE = "Date"
    BOOLEAN = "Boolean"
    OBJECTLINK = "ObjectLink"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "DataFrameColumnTypeNameEnumName":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of DataFrameColumnTypeNameEnumName must be a string (encountered: {val})"
            )
        newcls = Enum("DataFrameColumnTypeNameEnumName", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(DataFrameColumnTypeNameEnumName, getattr(newcls, "_UNKNOWN"))
