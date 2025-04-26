from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ManifestArrayConfigType(Enums.KnownString):
    ARRAY = "array"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ManifestArrayConfigType":
        if not isinstance(val, str):
            raise ValueError(f"Value of ManifestArrayConfigType must be a string (encountered: {val})")
        newcls = Enum("ManifestArrayConfigType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ManifestArrayConfigType, getattr(newcls, "_UNKNOWN"))
