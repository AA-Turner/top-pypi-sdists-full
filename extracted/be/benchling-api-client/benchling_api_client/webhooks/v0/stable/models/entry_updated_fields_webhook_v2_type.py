from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntryUpdatedFieldsWebhookV2Type(Enums.KnownString):
    V2_ENTRYUPDATEDFIELDS = "v2.entry.updated.fields"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntryUpdatedFieldsWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of EntryUpdatedFieldsWebhookV2Type must be a string (encountered: {val})"
            )
        newcls = Enum("EntryUpdatedFieldsWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntryUpdatedFieldsWebhookV2Type, getattr(newcls, "_UNKNOWN"))
