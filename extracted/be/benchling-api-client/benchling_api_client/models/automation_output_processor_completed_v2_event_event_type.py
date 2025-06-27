from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AutomationOutputProcessorCompletedV2EventEventType(Enums.KnownString):
    V2_AUTOMATIONOUTPUTPROCESSORCOMPLETED = "v2.automationOutputProcessor.completed"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AutomationOutputProcessorCompletedV2EventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AutomationOutputProcessorCompletedV2EventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("AutomationOutputProcessorCompletedV2EventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AutomationOutputProcessorCompletedV2EventEventType, getattr(newcls, "_UNKNOWN"))
