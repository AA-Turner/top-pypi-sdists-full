from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class BarcodeScanFormInstanceProviderType(Enums.KnownString):
    BARCODE_SCAN = "BARCODE_SCAN"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "BarcodeScanFormInstanceProviderType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of BarcodeScanFormInstanceProviderType must be a string (encountered: {val})"
            )
        newcls = Enum("BarcodeScanFormInstanceProviderType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(BarcodeScanFormInstanceProviderType, getattr(newcls, "_UNKNOWN"))
