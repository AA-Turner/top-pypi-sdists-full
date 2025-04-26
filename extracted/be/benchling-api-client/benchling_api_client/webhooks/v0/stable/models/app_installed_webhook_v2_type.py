from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AppInstalledWebhookV2Type(Enums.KnownString):
    V2_APPINSTALLED = "v2.app.installed"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AppInstalledWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(f"Value of AppInstalledWebhookV2Type must be a string (encountered: {val})")
        newcls = Enum("AppInstalledWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AppInstalledWebhookV2Type, getattr(newcls, "_UNKNOWN"))
