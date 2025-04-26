from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class LifecycleActivateWebhookV0Type(Enums.KnownString):
    V0_APPACTIVATEREQUESTED = "v0.app.activateRequested"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "LifecycleActivateWebhookV0Type":
        if not isinstance(val, str):
            raise ValueError(f"Value of LifecycleActivateWebhookV0Type must be a string (encountered: {val})")
        newcls = Enum("LifecycleActivateWebhookV0Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(LifecycleActivateWebhookV0Type, getattr(newcls, "_UNKNOWN"))
