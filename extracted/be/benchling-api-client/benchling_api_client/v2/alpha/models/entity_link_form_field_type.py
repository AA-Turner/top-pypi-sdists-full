from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntityLinkFormFieldType(Enums.KnownString):
    ENTITY_LINK = "ENTITY_LINK"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntityLinkFormFieldType":
        if not isinstance(val, str):
            raise ValueError(f"Value of EntityLinkFormFieldType must be a string (encountered: {val})")
        newcls = Enum("EntityLinkFormFieldType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntityLinkFormFieldType, getattr(newcls, "_UNKNOWN"))
