from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntryCreatedWebhookV3Type(Enums.KnownString):
    V3_ENTRYCREATED = "v3.entry.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntryCreatedWebhookV3Type":
        if not isinstance(val, str):
            raise ValueError(f"Value of EntryCreatedWebhookV3Type must be a string (encountered: {val})")
        newcls = Enum("EntryCreatedWebhookV3Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntryCreatedWebhookV3Type, getattr(newcls, "_UNKNOWN"))
