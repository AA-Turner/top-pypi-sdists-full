from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyGibsonExistingCutSitesParamsFragmentProductionMethod(Enums.KnownString):
    EXISTING_CUT_SITES = "EXISTING_CUT_SITES"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyGibsonExistingCutSitesParamsFragmentProductionMethod":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AssemblyGibsonExistingCutSitesParamsFragmentProductionMethod must be a string (encountered: {val})"
            )
        newcls = Enum("AssemblyGibsonExistingCutSitesParamsFragmentProductionMethod", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblyGibsonExistingCutSitesParamsFragmentProductionMethod, getattr(newcls, "_UNKNOWN"))
