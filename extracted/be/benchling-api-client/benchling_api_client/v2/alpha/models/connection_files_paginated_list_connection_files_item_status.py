from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ConnectionFilesPaginatedListConnectionFilesItemStatus(Enums.KnownString):
    NOT_UPLOADED = "NOT_UPLOADED"
    UPLOADED = "UPLOADED"
    ARCHIVED = "ARCHIVED"
    ERRORED = "ERRORED"
    FORMAT_ERROR = "FORMAT_ERROR"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ConnectionFilesPaginatedListConnectionFilesItemStatus":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of ConnectionFilesPaginatedListConnectionFilesItemStatus must be a string (encountered: {val})"
            )
        newcls = Enum("ConnectionFilesPaginatedListConnectionFilesItemStatus", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ConnectionFilesPaginatedListConnectionFilesItemStatus, getattr(newcls, "_UNKNOWN"))
