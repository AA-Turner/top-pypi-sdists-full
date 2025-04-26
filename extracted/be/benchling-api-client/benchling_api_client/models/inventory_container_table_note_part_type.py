from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class InventoryContainerTableNotePartType(Enums.KnownString):
    INVENTORY_CONTAINER_TABLE = "inventory_container_table"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "InventoryContainerTableNotePartType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of InventoryContainerTableNotePartType must be a string (encountered: {val})"
            )
        newcls = Enum("InventoryContainerTableNotePartType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(InventoryContainerTableNotePartType, getattr(newcls, "_UNKNOWN"))
