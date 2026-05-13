from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class CustomEntityCreatedWebhookV3Type(Enums.KnownString):
    V3_CUSTOMENTITYCREATED = "v3.customEntity.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "CustomEntityCreatedWebhookV3Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of CustomEntityCreatedWebhookV3Type must be a string (encountered: {val})"
            )
        newcls = Enum("CustomEntityCreatedWebhookV3Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(CustomEntityCreatedWebhookV3Type, getattr(newcls, "_UNKNOWN"))
