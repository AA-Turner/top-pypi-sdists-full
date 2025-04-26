from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class RequestUpdatedStatusWebhookV2Type(Enums.KnownString):
    V2_REQUESTUPDATEDSTATUS = "v2.request.updated.status"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "RequestUpdatedStatusWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of RequestUpdatedStatusWebhookV2Type must be a string (encountered: {val})"
            )
        newcls = Enum("RequestUpdatedStatusWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(RequestUpdatedStatusWebhookV2Type, getattr(newcls, "_UNKNOWN"))
