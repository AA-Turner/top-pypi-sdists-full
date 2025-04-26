from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class CanvasInteractionWebhookV2Type(Enums.KnownString):
    V2_CANVASUSERINTERACTED = "v2.canvas.userInteracted"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "CanvasInteractionWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(f"Value of CanvasInteractionWebhookV2Type must be a string (encountered: {val})")
        newcls = Enum("CanvasInteractionWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(CanvasInteractionWebhookV2Type, getattr(newcls, "_UNKNOWN"))
