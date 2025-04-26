from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntryCreateAttachmentsReviewRecordStatus(Enums.KnownString):
    ACCEPTED = "ACCEPTED"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntryCreateAttachmentsReviewRecordStatus":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of EntryCreateAttachmentsReviewRecordStatus must be a string (encountered: {val})"
            )
        newcls = Enum("EntryCreateAttachmentsReviewRecordStatus", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntryCreateAttachmentsReviewRecordStatus, getattr(newcls, "_UNKNOWN"))
