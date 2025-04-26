from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class DeliveryMethod(Enums.KnownString):
    WEBHOOK = "WEBHOOK"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "DeliveryMethod":
        if not isinstance(val, str):
            raise ValueError(f"Value of DeliveryMethod must be a string (encountered: {val})")
        newcls = Enum("DeliveryMethod", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(DeliveryMethod, getattr(newcls, "_UNKNOWN"))
