from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class RequestUpdatedStatusWebhookV2BetaType(Enums.KnownString):
    V2_BETAREQUESTUPDATEDSTATUS = "v2-beta.request.updated.status"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "RequestUpdatedStatusWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of RequestUpdatedStatusWebhookV2BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("RequestUpdatedStatusWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(RequestUpdatedStatusWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
