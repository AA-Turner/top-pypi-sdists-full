from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AutomationFileTransformPendingWebhookV2Type(Enums.KnownString):
    V2_AUTOMATIONFILETRANSFORMUPDATEDSTATUSPENDING = "v2.automationFileTransform.updated.status.pending"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AutomationFileTransformPendingWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AutomationFileTransformPendingWebhookV2Type must be a string (encountered: {val})"
            )
        newcls = Enum("AutomationFileTransformPendingWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AutomationFileTransformPendingWebhookV2Type, getattr(newcls, "_UNKNOWN"))
