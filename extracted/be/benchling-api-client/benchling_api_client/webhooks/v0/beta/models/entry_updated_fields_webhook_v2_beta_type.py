from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntryUpdatedFieldsWebhookV2BetaType(Enums.KnownString):
    V2_BETAENTRYUPDATEDFIELDS = "v2-beta.entry.updated.fields"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntryUpdatedFieldsWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of EntryUpdatedFieldsWebhookV2BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("EntryUpdatedFieldsWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntryUpdatedFieldsWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
