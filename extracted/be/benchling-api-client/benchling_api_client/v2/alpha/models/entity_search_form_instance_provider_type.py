from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntitySearchFormInstanceProviderType(Enums.KnownString):
    ENTITY_SEARCH = "ENTITY_SEARCH"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntitySearchFormInstanceProviderType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of EntitySearchFormInstanceProviderType must be a string (encountered: {val})"
            )
        newcls = Enum("EntitySearchFormInstanceProviderType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntitySearchFormInstanceProviderType, getattr(newcls, "_UNKNOWN"))
