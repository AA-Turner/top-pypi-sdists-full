from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AutomationFileTransformRunningWebhookV2Type(Enums.KnownString):
    V2_AUTOMATIONFILETRANSFORMUPDATEDSTATUSRUNNING = "v2.automationFileTransform.updated.status.running"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AutomationFileTransformRunningWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AutomationFileTransformRunningWebhookV2Type must be a string (encountered: {val})"
            )
        newcls = Enum("AutomationFileTransformRunningWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AutomationFileTransformRunningWebhookV2Type, getattr(newcls, "_UNKNOWN"))
