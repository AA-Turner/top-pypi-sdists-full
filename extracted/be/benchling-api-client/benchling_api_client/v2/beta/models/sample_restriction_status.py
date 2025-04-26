from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class SampleRestrictionStatus(Enums.KnownString):
    RESTRICTED = "RESTRICTED"
    UNRESTRICTED = "UNRESTRICTED"
    NOT_APPLICABLE = "NOT_APPLICABLE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "SampleRestrictionStatus":
        if not isinstance(val, str):
            raise ValueError(f"Value of SampleRestrictionStatus must be a string (encountered: {val})")
        newcls = Enum("SampleRestrictionStatus", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(SampleRestrictionStatus, getattr(newcls, "_UNKNOWN"))
