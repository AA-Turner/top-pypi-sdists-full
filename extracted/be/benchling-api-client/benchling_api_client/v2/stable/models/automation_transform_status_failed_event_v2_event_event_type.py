from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AutomationTransformStatusFailedEventV2EventEventType(Enums.KnownString):
    V2_AUTOMATIONFILETRANSFORMUPDATEDSTATUSFAILED = "v2.automationFileTransform.updated.status.failed"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AutomationTransformStatusFailedEventV2EventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AutomationTransformStatusFailedEventV2EventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("AutomationTransformStatusFailedEventV2EventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AutomationTransformStatusFailedEventV2EventEventType, getattr(newcls, "_UNKNOWN"))
