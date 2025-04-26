from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ReviewChangeAction(Enums.KnownString):
    SEND_FOR_REVIEW = "SEND_FOR_REVIEW"
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    COMMENT = "COMMENT"
    RETRACT = "RETRACT"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ReviewChangeAction":
        if not isinstance(val, str):
            raise ValueError(f"Value of ReviewChangeAction must be a string (encountered: {val})")
        newcls = Enum("ReviewChangeAction", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ReviewChangeAction, getattr(newcls, "_UNKNOWN"))
