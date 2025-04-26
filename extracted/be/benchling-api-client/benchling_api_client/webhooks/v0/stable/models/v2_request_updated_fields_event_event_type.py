from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class V2RequestUpdatedFieldsEventEventType(Enums.KnownString):
    V2_REQUESTUPDATEDFIELDS = "v2.request.updated.fields"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "V2RequestUpdatedFieldsEventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of V2RequestUpdatedFieldsEventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("V2RequestUpdatedFieldsEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(V2RequestUpdatedFieldsEventEventType, getattr(newcls, "_UNKNOWN"))
