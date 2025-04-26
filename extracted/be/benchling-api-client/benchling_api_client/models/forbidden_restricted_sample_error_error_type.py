from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ForbiddenRestrictedSampleErrorErrorType(Enums.KnownString):
    INVALID_REQUEST_ERROR = "invalid_request_error"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ForbiddenRestrictedSampleErrorErrorType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of ForbiddenRestrictedSampleErrorErrorType must be a string (encountered: {val})"
            )
        newcls = Enum("ForbiddenRestrictedSampleErrorErrorType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ForbiddenRestrictedSampleErrorErrorType, getattr(newcls, "_UNKNOWN"))
