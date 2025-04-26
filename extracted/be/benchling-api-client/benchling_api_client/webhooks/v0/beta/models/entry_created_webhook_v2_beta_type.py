from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntryCreatedWebhookV2BetaType(Enums.KnownString):
    V2_BETAENTRYCREATED = "v2-beta.entry.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntryCreatedWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(f"Value of EntryCreatedWebhookV2BetaType must be a string (encountered: {val})")
        newcls = Enum("EntryCreatedWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntryCreatedWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
