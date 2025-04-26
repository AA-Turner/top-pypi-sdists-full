from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class FormBarcodeValueReferenceType(Enums.KnownString):
    BARCODE_VALUE = "BARCODE_VALUE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "FormBarcodeValueReferenceType":
        if not isinstance(val, str):
            raise ValueError(f"Value of FormBarcodeValueReferenceType must be a string (encountered: {val})")
        newcls = Enum("FormBarcodeValueReferenceType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(FormBarcodeValueReferenceType, getattr(newcls, "_UNKNOWN"))
