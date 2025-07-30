from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class CustomEntityUpdatedWebhookV3Type(Enums.KnownString):
    V3_CUSTOMENTITYUPDATED = "v3.customEntity.updated"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "CustomEntityUpdatedWebhookV3Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of CustomEntityUpdatedWebhookV3Type must be a string (encountered: {val})"
            )
        newcls = Enum("CustomEntityUpdatedWebhookV3Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(CustomEntityUpdatedWebhookV3Type, getattr(newcls, "_UNKNOWN"))
