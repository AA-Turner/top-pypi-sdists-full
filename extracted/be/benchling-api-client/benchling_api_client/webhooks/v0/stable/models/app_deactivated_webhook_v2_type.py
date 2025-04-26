from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AppDeactivatedWebhookV2Type(Enums.KnownString):
    V2_APPDEACTIVATED = "v2.app.deactivated"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AppDeactivatedWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(f"Value of AppDeactivatedWebhookV2Type must be a string (encountered: {val})")
        newcls = Enum("AppDeactivatedWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AppDeactivatedWebhookV2Type, getattr(newcls, "_UNKNOWN"))
