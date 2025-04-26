from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntitySchemaAppConfigItemType(Enums.KnownString):
    ENTITY_SCHEMA = "entity_schema"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntitySchemaAppConfigItemType":
        if not isinstance(val, str):
            raise ValueError(f"Value of EntitySchemaAppConfigItemType must be a string (encountered: {val})")
        newcls = Enum("EntitySchemaAppConfigItemType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntitySchemaAppConfigItemType, getattr(newcls, "_UNKNOWN"))
