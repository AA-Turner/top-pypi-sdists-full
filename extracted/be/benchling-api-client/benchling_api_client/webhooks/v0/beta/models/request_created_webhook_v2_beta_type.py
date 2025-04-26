from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class RequestCreatedWebhookV2BetaType(Enums.KnownString):
    V2_BETAREQUESTCREATED = "v2-beta.request.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "RequestCreatedWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of RequestCreatedWebhookV2BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("RequestCreatedWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(RequestCreatedWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
