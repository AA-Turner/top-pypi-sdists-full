from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class FreeFormTextFormFieldCannedResponsesBehavior(Enums.KnownString):
    ADDITIVE = "ADDITIVE"
    REPLACE = "REPLACE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "FreeFormTextFormFieldCannedResponsesBehavior":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of FreeFormTextFormFieldCannedResponsesBehavior must be a string (encountered: {val})"
            )
        newcls = Enum("FreeFormTextFormFieldCannedResponsesBehavior", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(FreeFormTextFormFieldCannedResponsesBehavior, getattr(newcls, "_UNKNOWN"))
