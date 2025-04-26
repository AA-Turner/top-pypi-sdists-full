from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ManifestIntegerScalarConfigType(Enums.KnownString):
    INTEGER = "integer"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ManifestIntegerScalarConfigType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of ManifestIntegerScalarConfigType must be a string (encountered: {val})"
            )
        newcls = Enum("ManifestIntegerScalarConfigType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ManifestIntegerScalarConfigType, getattr(newcls, "_UNKNOWN"))
