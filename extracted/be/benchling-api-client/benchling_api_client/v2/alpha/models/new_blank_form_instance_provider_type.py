from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class NewBlankFormInstanceProviderType(Enums.KnownString):
    BLANK_FORM = "BLANK_FORM"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "NewBlankFormInstanceProviderType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of NewBlankFormInstanceProviderType must be a string (encountered: {val})"
            )
        newcls = Enum("NewBlankFormInstanceProviderType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(NewBlankFormInstanceProviderType, getattr(newcls, "_UNKNOWN"))
