from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ManifestDatetimeScalarConfigType(Enums.KnownString):
    DATETIME = "datetime"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ManifestDatetimeScalarConfigType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of ManifestDatetimeScalarConfigType must be a string (encountered: {val})"
            )
        newcls = Enum("ManifestDatetimeScalarConfigType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ManifestDatetimeScalarConfigType, getattr(newcls, "_UNKNOWN"))
