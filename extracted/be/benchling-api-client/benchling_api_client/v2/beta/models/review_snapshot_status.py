from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ReviewSnapshotStatus(Enums.KnownString):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ReviewSnapshotStatus":
        if not isinstance(val, str):
            raise ValueError(f"Value of ReviewSnapshotStatus must be a string (encountered: {val})")
        newcls = Enum("ReviewSnapshotStatus", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ReviewSnapshotStatus, getattr(newcls, "_UNKNOWN"))
