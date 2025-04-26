from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyGibsonExistingHomologyRegionsParamsFragmentProductionMethod(Enums.KnownString):
    EXISTING_HOMOLOGY_REGIONS = "EXISTING_HOMOLOGY_REGIONS"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyGibsonExistingHomologyRegionsParamsFragmentProductionMethod":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AssemblyGibsonExistingHomologyRegionsParamsFragmentProductionMethod must be a string (encountered: {val})"
            )
        newcls = Enum("AssemblyGibsonExistingHomologyRegionsParamsFragmentProductionMethod", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(
            AssemblyGibsonExistingHomologyRegionsParamsFragmentProductionMethod, getattr(newcls, "_UNKNOWN")
        )
