from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyConcatenationMethodParametersFragmentProductionMethod(Enums.KnownString):
    SLICE = "SLICE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyConcatenationMethodParametersFragmentProductionMethod":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AssemblyConcatenationMethodParametersFragmentProductionMethod must be a string (encountered: {val})"
            )
        newcls = Enum("AssemblyConcatenationMethodParametersFragmentProductionMethod", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(
            AssemblyConcatenationMethodParametersFragmentProductionMethod, getattr(newcls, "_UNKNOWN")
        )
