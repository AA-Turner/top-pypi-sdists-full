from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyConcatenationMethodParametersPolymerType(Enums.KnownString):
    DNA = "DNA"
    RNA = "RNA"
    AA = "AA"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyConcatenationMethodParametersPolymerType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AssemblyConcatenationMethodParametersPolymerType must be a string (encountered: {val})"
            )
        newcls = Enum("AssemblyConcatenationMethodParametersPolymerType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblyConcatenationMethodParametersPolymerType, getattr(newcls, "_UNKNOWN"))
