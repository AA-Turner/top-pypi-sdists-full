from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntitySchemaBaseAuthParentOption(Enums.KnownString):
    FOLDER = "FOLDER"
    PROJECT_FOLDER = "PROJECT_FOLDER"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntitySchemaBaseAuthParentOption":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of EntitySchemaBaseAuthParentOption must be a string (encountered: {val})"
            )
        newcls = Enum("EntitySchemaBaseAuthParentOption", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntitySchemaBaseAuthParentOption, getattr(newcls, "_UNKNOWN"))
