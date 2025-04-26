from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntryUpdatedReviewRecordWebhookV2BetaType(Enums.KnownString):
    V2_BETAENTRYUPDATEDREVIEWRECORD = "v2-beta.entry.updated.reviewRecord"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntryUpdatedReviewRecordWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of EntryUpdatedReviewRecordWebhookV2BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("EntryUpdatedReviewRecordWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntryUpdatedReviewRecordWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
