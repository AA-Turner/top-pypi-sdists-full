from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ManifestDateScalarConfigType(Enums.KnownString):
    DATE = "date"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ManifestDateScalarConfigType":
        if not isinstance(val, str):
            raise ValueError(f"Value of ManifestDateScalarConfigType must be a string (encountered: {val})")
        newcls = Enum("ManifestDateScalarConfigType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ManifestDateScalarConfigType, getattr(newcls, "_UNKNOWN"))
