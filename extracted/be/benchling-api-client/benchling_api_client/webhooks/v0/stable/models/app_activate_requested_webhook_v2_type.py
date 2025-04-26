from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AppActivateRequestedWebhookV2Type(Enums.KnownString):
    V2_APPACTIVATEREQUESTED = "v2.app.activateRequested"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AppActivateRequestedWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AppActivateRequestedWebhookV2Type must be a string (encountered: {val})"
            )
        newcls = Enum("AppActivateRequestedWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AppActivateRequestedWebhookV2Type, getattr(newcls, "_UNKNOWN"))
