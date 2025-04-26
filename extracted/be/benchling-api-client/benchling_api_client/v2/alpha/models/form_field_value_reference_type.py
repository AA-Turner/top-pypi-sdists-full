from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class FormFieldValueReferenceType(Enums.KnownString):
    FORM_FIELD_VALUE = "FORM_FIELD_VALUE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "FormFieldValueReferenceType":
        if not isinstance(val, str):
            raise ValueError(f"Value of FormFieldValueReferenceType must be a string (encountered: {val})")
        newcls = Enum("FormFieldValueReferenceType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(FormFieldValueReferenceType, getattr(newcls, "_UNKNOWN"))
