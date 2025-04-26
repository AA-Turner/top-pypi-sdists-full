from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyValidationStatusType(Enums.KnownString):
    ERROR = "ERROR"
    WARNING = "WARNING"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyValidationStatusType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AssemblyValidationStatusType must be a string (encountered: {val})")
        newcls = Enum("AssemblyValidationStatusType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblyValidationStatusType, getattr(newcls, "_UNKNOWN"))
