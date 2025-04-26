from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblySequenceReferencePolymerType(Enums.KnownString):
    NUCLEOTIDE_SEQUENCE = "NUCLEOTIDE_SEQUENCE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblySequenceReferencePolymerType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AssemblySequenceReferencePolymerType must be a string (encountered: {val})"
            )
        newcls = Enum("AssemblySequenceReferencePolymerType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblySequenceReferencePolymerType, getattr(newcls, "_UNKNOWN"))
