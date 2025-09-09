from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AutomationFileTransformSucceededWebhookV2Type(Enums.KnownString):
    V2_AUTOMATIONFILETRANSFORMUPDATEDSTATUSSUCCEEDED = "v2.automationFileTransform.updated.status.succeeded"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AutomationFileTransformSucceededWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AutomationFileTransformSucceededWebhookV2Type must be a string (encountered: {val})"
            )
        newcls = Enum("AutomationFileTransformSucceededWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AutomationFileTransformSucceededWebhookV2Type, getattr(newcls, "_UNKNOWN"))
