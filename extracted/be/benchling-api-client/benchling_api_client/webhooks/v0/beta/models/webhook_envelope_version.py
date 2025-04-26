from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WebhookEnvelopeVersion(Enums.KnownString):
    VALUE_0 = "0"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WebhookEnvelopeVersion":
        if not isinstance(val, str):
            raise ValueError(f"Value of WebhookEnvelopeVersion must be a string (encountered: {val})")
        newcls = Enum("WebhookEnvelopeVersion", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WebhookEnvelopeVersion, getattr(newcls, "_UNKNOWN"))
