from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class InaccessibleResourceResourceType(Enums.KnownString):
    INACCESSIBLE_RESOURCE = "inaccessible_resource"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "InaccessibleResourceResourceType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of InaccessibleResourceResourceType must be a string (encountered: {val})"
            )
        newcls = Enum("InaccessibleResourceResourceType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(InaccessibleResourceResourceType, getattr(newcls, "_UNKNOWN"))
