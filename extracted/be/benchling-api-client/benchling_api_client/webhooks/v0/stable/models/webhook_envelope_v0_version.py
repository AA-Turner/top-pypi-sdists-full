from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WebhookEnvelopeV0Version(Enums.KnownString):
    VALUE_0 = "0"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WebhookEnvelopeV0Version":
        if not isinstance(val, str):
            raise ValueError(f"Value of WebhookEnvelopeV0Version must be a string (encountered: {val})")
        newcls = Enum("WebhookEnvelopeV0Version", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WebhookEnvelopeV0Version, getattr(newcls, "_UNKNOWN"))
