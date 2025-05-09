from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class CanvasCreatedWebhookV2Type(Enums.KnownString):
    V2_CANVASCREATED = "v2.canvas.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "CanvasCreatedWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(f"Value of CanvasCreatedWebhookV2Type must be a string (encountered: {val})")
        newcls = Enum("CanvasCreatedWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(CanvasCreatedWebhookV2Type, getattr(newcls, "_UNKNOWN"))
