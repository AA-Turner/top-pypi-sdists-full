from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class LifecycleDeactivateWebhookV0BetaType(Enums.KnownString):
    V0_BETALIFECYCLEDEACTIVATED = "v0-beta.lifecycle.deactivated"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "LifecycleDeactivateWebhookV0BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of LifecycleDeactivateWebhookV0BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("LifecycleDeactivateWebhookV0BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(LifecycleDeactivateWebhookV0BetaType, getattr(newcls, "_UNKNOWN"))
