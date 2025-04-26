from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntityRegisteredWebhookV2Type(Enums.KnownString):
    V2_ENTITYREGISTERED = "v2.entity.registered"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntityRegisteredWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(f"Value of EntityRegisteredWebhookV2Type must be a string (encountered: {val})")
        newcls = Enum("EntityRegisteredWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntityRegisteredWebhookV2Type, getattr(newcls, "_UNKNOWN"))
