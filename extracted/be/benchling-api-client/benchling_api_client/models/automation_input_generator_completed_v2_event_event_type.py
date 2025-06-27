from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AutomationInputGeneratorCompletedV2EventEventType(Enums.KnownString):
    V2_AUTOMATIONINPUTGENERATORCOMPLETED = "v2.automationInputGenerator.completed"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AutomationInputGeneratorCompletedV2EventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AutomationInputGeneratorCompletedV2EventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("AutomationInputGeneratorCompletedV2EventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AutomationInputGeneratorCompletedV2EventEventType, getattr(newcls, "_UNKNOWN"))
