from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntitySchemaBaseContainableType(Enums.KnownString):
    NONE = "NONE"
    ENTITY = "ENTITY"
    BATCH = "BATCH"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntitySchemaBaseContainableType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of EntitySchemaBaseContainableType must be a string (encountered: {val})"
            )
        newcls = Enum("EntitySchemaBaseContainableType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntitySchemaBaseContainableType, getattr(newcls, "_UNKNOWN"))
