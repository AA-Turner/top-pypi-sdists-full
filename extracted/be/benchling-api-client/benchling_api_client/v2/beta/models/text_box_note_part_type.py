from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class TextBoxNotePartType(Enums.KnownString):
    TEXT_BOX = "text_box"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "TextBoxNotePartType":
        if not isinstance(val, str):
            raise ValueError(f"Value of TextBoxNotePartType must be a string (encountered: {val})")
        newcls = Enum("TextBoxNotePartType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(TextBoxNotePartType, getattr(newcls, "_UNKNOWN"))
