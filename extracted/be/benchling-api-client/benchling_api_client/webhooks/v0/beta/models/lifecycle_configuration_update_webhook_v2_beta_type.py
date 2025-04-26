from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class LifecycleConfigurationUpdateWebhookV2BetaType(Enums.KnownString):
    V2_BETAAPPCONFIGURATIONUPDATED = "v2-beta.app.configuration.updated"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "LifecycleConfigurationUpdateWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of LifecycleConfigurationUpdateWebhookV2BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("LifecycleConfigurationUpdateWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(LifecycleConfigurationUpdateWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
