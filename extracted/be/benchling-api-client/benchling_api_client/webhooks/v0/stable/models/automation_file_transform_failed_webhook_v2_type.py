from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AutomationFileTransformFailedWebhookV2Type(Enums.KnownString):
    V2_AUTOMATIONFILETRANSFORMUPDATEDSTATUSFAILED = "v2.automationFileTransform.updated.status.failed"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AutomationFileTransformFailedWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AutomationFileTransformFailedWebhookV2Type must be a string (encountered: {val})"
            )
        newcls = Enum("AutomationFileTransformFailedWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AutomationFileTransformFailedWebhookV2Type, getattr(newcls, "_UNKNOWN"))
