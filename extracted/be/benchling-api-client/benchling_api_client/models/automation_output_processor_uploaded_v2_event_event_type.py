from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AutomationOutputProcessorUploadedV2EventEventType(Enums.KnownString):
    V2_AUTOMATIONOUTPUTPROCESSORUPLOADED = "v2.automationOutputProcessor.uploaded"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AutomationOutputProcessorUploadedV2EventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AutomationOutputProcessorUploadedV2EventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("AutomationOutputProcessorUploadedV2EventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AutomationOutputProcessorUploadedV2EventEventType, getattr(newcls, "_UNKNOWN"))
