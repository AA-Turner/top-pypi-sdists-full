from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ConstraintStatusStatus(Enums.KnownString):
    ACTIVE = "ACTIVE"
    COMPUTING = "COMPUTING"
    INACTIVE = "INACTIVE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ConstraintStatusStatus":
        if not isinstance(val, str):
            raise ValueError(f"Value of ConstraintStatusStatus must be a string (encountered: {val})")
        newcls = Enum("ConstraintStatusStatus", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ConstraintStatusStatus, getattr(newcls, "_UNKNOWN"))
