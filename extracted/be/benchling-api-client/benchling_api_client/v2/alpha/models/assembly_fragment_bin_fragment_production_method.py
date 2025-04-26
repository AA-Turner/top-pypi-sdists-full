from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyFragmentBinFragmentProductionMethod(Enums.KnownString):
    EXISTING_CUT_SITES = "EXISTING_CUT_SITES"
    EXISTING_HOMOLOGY_REGIONS = "EXISTING_HOMOLOGY_REGIONS"
    PRIMER_PAIR = "PRIMER_PAIR"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyFragmentBinFragmentProductionMethod":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AssemblyFragmentBinFragmentProductionMethod must be a string (encountered: {val})"
            )
        newcls = Enum("AssemblyFragmentBinFragmentProductionMethod", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblyFragmentBinFragmentProductionMethod, getattr(newcls, "_UNKNOWN"))
