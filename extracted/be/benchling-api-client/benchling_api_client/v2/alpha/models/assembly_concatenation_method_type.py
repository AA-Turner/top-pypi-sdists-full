from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyConcatenationMethodType(Enums.KnownString):
    CONCATENATION = "CONCATENATION"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyConcatenationMethodType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AssemblyConcatenationMethodType must be a string (encountered: {val})"
            )
        newcls = Enum("AssemblyConcatenationMethodType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblyConcatenationMethodType, getattr(newcls, "_UNKNOWN"))
