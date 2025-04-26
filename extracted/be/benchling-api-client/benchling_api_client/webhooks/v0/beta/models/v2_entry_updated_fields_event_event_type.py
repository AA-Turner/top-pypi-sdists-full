from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class V2EntryUpdatedFieldsEventEventType(Enums.KnownString):
    V2_ENTRYUPDATEDFIELDS = "v2.entry.updated.fields"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "V2EntryUpdatedFieldsEventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of V2EntryUpdatedFieldsEventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("V2EntryUpdatedFieldsEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(V2EntryUpdatedFieldsEventEventType, getattr(newcls, "_UNKNOWN"))
