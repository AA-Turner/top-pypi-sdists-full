from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyGoldenGatePrimerPairParamsFragmentProductionMethod(Enums.KnownString):
    PRIMER_PAIR = "PRIMER_PAIR"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyGoldenGatePrimerPairParamsFragmentProductionMethod":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AssemblyGoldenGatePrimerPairParamsFragmentProductionMethod must be a string (encountered: {val})"
            )
        newcls = Enum("AssemblyGoldenGatePrimerPairParamsFragmentProductionMethod", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblyGoldenGatePrimerPairParamsFragmentProductionMethod, getattr(newcls, "_UNKNOWN"))
