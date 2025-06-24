from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AutomationTransformStatusRunningEventV2EventEventType(Enums.KnownString):
    V2_AUTOMATIONFILETRANSFORMUPDATEDSTATUSRUNNING = "v2.automationFileTransform.updated.status.running"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AutomationTransformStatusRunningEventV2EventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AutomationTransformStatusRunningEventV2EventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("AutomationTransformStatusRunningEventV2EventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AutomationTransformStatusRunningEventV2EventEventType, getattr(newcls, "_UNKNOWN"))
