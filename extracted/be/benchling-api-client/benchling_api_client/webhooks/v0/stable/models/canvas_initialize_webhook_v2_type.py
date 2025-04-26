from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class CanvasInitializeWebhookV2Type(Enums.KnownString):
    V2_CANVASINITIALIZED = "v2.canvas.initialized"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "CanvasInitializeWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(f"Value of CanvasInitializeWebhookV2Type must be a string (encountered: {val})")
        newcls = Enum("CanvasInitializeWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(CanvasInitializeWebhookV2Type, getattr(newcls, "_UNKNOWN"))
