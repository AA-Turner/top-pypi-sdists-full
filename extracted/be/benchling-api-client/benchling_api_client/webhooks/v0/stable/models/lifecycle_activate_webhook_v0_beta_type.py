from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class LifecycleActivateWebhookV0BetaType(Enums.KnownString):
    V0_BETALIFECYCLEACTIVATEREQUESTED = "v0-beta.lifecycle.activateRequested"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "LifecycleActivateWebhookV0BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of LifecycleActivateWebhookV0BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("LifecycleActivateWebhookV0BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(LifecycleActivateWebhookV0BetaType, getattr(newcls, "_UNKNOWN"))
