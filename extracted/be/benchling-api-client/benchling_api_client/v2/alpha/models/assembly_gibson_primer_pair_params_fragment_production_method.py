from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyGibsonPrimerPairParamsFragmentProductionMethod(Enums.KnownString):
    PRIMER_PAIR = "PRIMER_PAIR"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyGibsonPrimerPairParamsFragmentProductionMethod":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AssemblyGibsonPrimerPairParamsFragmentProductionMethod must be a string (encountered: {val})"
            )
        newcls = Enum("AssemblyGibsonPrimerPairParamsFragmentProductionMethod", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblyGibsonPrimerPairParamsFragmentProductionMethod, getattr(newcls, "_UNKNOWN"))
