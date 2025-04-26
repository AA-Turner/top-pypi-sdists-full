from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class BarcodeFormFieldType(Enums.KnownString):
    BARCODE = "BARCODE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "BarcodeFormFieldType":
        if not isinstance(val, str):
            raise ValueError(f"Value of BarcodeFormFieldType must be a string (encountered: {val})")
        newcls = Enum("BarcodeFormFieldType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(BarcodeFormFieldType, getattr(newcls, "_UNKNOWN"))
