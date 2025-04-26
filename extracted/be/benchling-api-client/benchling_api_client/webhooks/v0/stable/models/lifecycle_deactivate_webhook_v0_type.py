from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class LifecycleDeactivateWebhookV0Type(Enums.KnownString):
    V0_APPDEACTIVATED = "v0.app.deactivated"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "LifecycleDeactivateWebhookV0Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of LifecycleDeactivateWebhookV0Type must be a string (encountered: {val})"
            )
        newcls = Enum("LifecycleDeactivateWebhookV0Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(LifecycleDeactivateWebhookV0Type, getattr(newcls, "_UNKNOWN"))
