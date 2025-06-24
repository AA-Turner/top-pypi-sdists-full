from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AutomationTransformStatusPendingEventV2EventEventType(Enums.KnownString):
    V2_AUTOMATIONFILETRANSFORMUPDATEDSTATUSPENDING = "v2.automationFileTransform.updated.status.pending"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AutomationTransformStatusPendingEventV2EventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AutomationTransformStatusPendingEventV2EventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("AutomationTransformStatusPendingEventV2EventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AutomationTransformStatusPendingEventV2EventEventType, getattr(newcls, "_UNKNOWN"))
