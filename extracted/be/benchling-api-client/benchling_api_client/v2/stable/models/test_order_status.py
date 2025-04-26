from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class TestOrderStatus(Enums.KnownString):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"
    INVALID = "INVALID"
    COMPLETED = "COMPLETED"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "TestOrderStatus":
        if not isinstance(val, str):
            raise ValueError(f"Value of TestOrderStatus must be a string (encountered: {val})")
        newcls = Enum("TestOrderStatus", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(TestOrderStatus, getattr(newcls, "_UNKNOWN"))
