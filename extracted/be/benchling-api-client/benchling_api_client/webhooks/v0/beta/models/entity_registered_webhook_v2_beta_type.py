from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntityRegisteredWebhookV2BetaType(Enums.KnownString):
    V2_BETAENTITYREGISTERED = "v2-beta.entity.registered"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntityRegisteredWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of EntityRegisteredWebhookV2BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("EntityRegisteredWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntityRegisteredWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
