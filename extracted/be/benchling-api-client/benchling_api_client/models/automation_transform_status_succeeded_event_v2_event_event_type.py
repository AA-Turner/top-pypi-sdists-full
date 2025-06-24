from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AutomationTransformStatusSucceededEventV2EventEventType(Enums.KnownString):
    V2_AUTOMATIONFILETRANSFORMUPDATEDSTATUSSUCCEEDED = "v2.automationFileTransform.updated.status.succeeded"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AutomationTransformStatusSucceededEventV2EventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AutomationTransformStatusSucceededEventV2EventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("AutomationTransformStatusSucceededEventV2EventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AutomationTransformStatusSucceededEventV2EventEventType, getattr(newcls, "_UNKNOWN"))
