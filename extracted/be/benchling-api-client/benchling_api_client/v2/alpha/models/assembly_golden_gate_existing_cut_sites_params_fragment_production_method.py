from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyGoldenGateExistingCutSitesParamsFragmentProductionMethod(Enums.KnownString):
    EXISTING_CUT_SITES = "EXISTING_CUT_SITES"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyGoldenGateExistingCutSitesParamsFragmentProductionMethod":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AssemblyGoldenGateExistingCutSitesParamsFragmentProductionMethod must be a string (encountered: {val})"
            )
        newcls = Enum("AssemblyGoldenGateExistingCutSitesParamsFragmentProductionMethod", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(
            AssemblyGoldenGateExistingCutSitesParamsFragmentProductionMethod, getattr(newcls, "_UNKNOWN")
        )
