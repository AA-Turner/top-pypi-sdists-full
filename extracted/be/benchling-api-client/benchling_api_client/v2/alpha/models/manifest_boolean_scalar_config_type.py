from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ManifestBooleanScalarConfigType(Enums.KnownString):
    BOOLEAN = "boolean"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ManifestBooleanScalarConfigType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of ManifestBooleanScalarConfigType must be a string (encountered: {val})"
            )
        newcls = Enum("ManifestBooleanScalarConfigType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ManifestBooleanScalarConfigType, getattr(newcls, "_UNKNOWN"))
