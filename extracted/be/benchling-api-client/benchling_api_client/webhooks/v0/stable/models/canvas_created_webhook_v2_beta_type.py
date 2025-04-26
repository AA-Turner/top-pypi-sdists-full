from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class CanvasCreatedWebhookV2BetaType(Enums.KnownString):
    V2_BETACANVASCREATED = "v2-beta.canvas.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "CanvasCreatedWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(f"Value of CanvasCreatedWebhookV2BetaType must be a string (encountered: {val})")
        newcls = Enum("CanvasCreatedWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(CanvasCreatedWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
