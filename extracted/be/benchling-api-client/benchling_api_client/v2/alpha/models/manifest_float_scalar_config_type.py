from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ManifestFloatScalarConfigType(Enums.KnownString):
    FLOAT = "float"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ManifestFloatScalarConfigType":
        if not isinstance(val, str):
            raise ValueError(f"Value of ManifestFloatScalarConfigType must be a string (encountered: {val})")
        newcls = Enum("ManifestFloatScalarConfigType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ManifestFloatScalarConfigType, getattr(newcls, "_UNKNOWN"))
