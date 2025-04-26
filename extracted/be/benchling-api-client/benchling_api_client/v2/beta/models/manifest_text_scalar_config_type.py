from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ManifestTextScalarConfigType(Enums.KnownString):
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ManifestTextScalarConfigType":
        if not isinstance(val, str):
            raise ValueError(f"Value of ManifestTextScalarConfigType must be a string (encountered: {val})")
        newcls = Enum("ManifestTextScalarConfigType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ManifestTextScalarConfigType, getattr(newcls, "_UNKNOWN"))
