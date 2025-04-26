from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyHomologyMethodParametersFragmentProductionMethod(Enums.KnownString):
    EXISTING_HOMOLOGY_REGIONS = "EXISTING_HOMOLOGY_REGIONS"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyHomologyMethodParametersFragmentProductionMethod":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AssemblyHomologyMethodParametersFragmentProductionMethod must be a string (encountered: {val})"
            )
        newcls = Enum("AssemblyHomologyMethodParametersFragmentProductionMethod", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblyHomologyMethodParametersFragmentProductionMethod, getattr(newcls, "_UNKNOWN"))
