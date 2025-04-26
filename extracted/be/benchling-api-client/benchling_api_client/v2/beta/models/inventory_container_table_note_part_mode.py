from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class InventoryContainerTableNotePartMode(Enums.KnownString):
    CREATE_AND_FILL = "create_and_fill"
    FILL = "fill"
    UPDATE = "update"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "InventoryContainerTableNotePartMode":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of InventoryContainerTableNotePartMode must be a string (encountered: {val})"
            )
        newcls = Enum("InventoryContainerTableNotePartMode", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(InventoryContainerTableNotePartMode, getattr(newcls, "_UNKNOWN"))
