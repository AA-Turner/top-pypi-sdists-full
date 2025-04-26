from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class InventoryPlateTableNotePartType(Enums.KnownString):
    INVENTORY_PLATE_TABLE = "inventory_plate_table"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "InventoryPlateTableNotePartType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of InventoryPlateTableNotePartType must be a string (encountered: {val})"
            )
        newcls = Enum("InventoryPlateTableNotePartType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(InventoryPlateTableNotePartType, getattr(newcls, "_UNKNOWN"))
