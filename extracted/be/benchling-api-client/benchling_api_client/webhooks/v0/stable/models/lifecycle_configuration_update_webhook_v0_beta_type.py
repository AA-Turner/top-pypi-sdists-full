from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class LifecycleConfigurationUpdateWebhookV0BetaType(Enums.KnownString):
    V0_BETAAPPCONFIGURATIONUPDATED = "v0-beta.app.configuration.updated"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "LifecycleConfigurationUpdateWebhookV0BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of LifecycleConfigurationUpdateWebhookV0BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("LifecycleConfigurationUpdateWebhookV0BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(LifecycleConfigurationUpdateWebhookV0BetaType, getattr(newcls, "_UNKNOWN"))
