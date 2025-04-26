from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyCreatedPrimerType(Enums.KnownString):
    BULK_ASSEMBLY_CREATED_PRIMER = "BULK_ASSEMBLY_CREATED_PRIMER"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyCreatedPrimerType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AssemblyCreatedPrimerType must be a string (encountered: {val})")
        newcls = Enum("AssemblyCreatedPrimerType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblyCreatedPrimerType, getattr(newcls, "_UNKNOWN"))
