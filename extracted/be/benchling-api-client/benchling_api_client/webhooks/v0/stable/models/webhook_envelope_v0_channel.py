from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WebhookEnvelopeV0Channel(Enums.KnownString):
    EVENTS = "events"
    APP_SIGNALS = "app_signals"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WebhookEnvelopeV0Channel":
        if not isinstance(val, str):
            raise ValueError(f"Value of WebhookEnvelopeV0Channel must be a string (encountered: {val})")
        newcls = Enum("WebhookEnvelopeV0Channel", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WebhookEnvelopeV0Channel, getattr(newcls, "_UNKNOWN"))
