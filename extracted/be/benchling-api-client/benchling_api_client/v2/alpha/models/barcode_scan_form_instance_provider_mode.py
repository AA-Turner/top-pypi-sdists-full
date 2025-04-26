from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class BarcodeScanFormInstanceProviderMode(Enums.KnownString):
    MULTIPLE_SCAN = "MULTIPLE_SCAN"
    SINGLE_SCAN = "SINGLE_SCAN"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "BarcodeScanFormInstanceProviderMode":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of BarcodeScanFormInstanceProviderMode must be a string (encountered: {val})"
            )
        newcls = Enum("BarcodeScanFormInstanceProviderMode", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(BarcodeScanFormInstanceProviderMode, getattr(newcls, "_UNKNOWN"))
