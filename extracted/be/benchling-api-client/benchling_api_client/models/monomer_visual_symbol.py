from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class MonomerVisualSymbol(Enums.KnownString):
    DIAMOND_FILLED = "DIAMOND_FILLED"
    DIAMOND_HOLLOW = "DIAMOND_HOLLOW"
    DIAMOND_DASHED = "DIAMOND_DASHED"
    STAR_FILLED = "STAR_FILLED"
    STAR_HOLLOW = "STAR_HOLLOW"
    TRIANGLE_FILLED = "TRIANGLE_FILLED"
    TRIANGLE_HOLLOW = "TRIANGLE_HOLLOW"
    DYAD_FILLED = "DYAD_FILLED"
    DYAD_HOLLOW = "DYAD_HOLLOW"
    CLOVER_FILLED = "CLOVER_FILLED"
    CLOVER_HOLLOW = "CLOVER_HOLLOW"
    TRIAD_FILLED = "TRIAD_FILLED"
    TRIAD_HOLLOW = "TRIAD_HOLLOW"
    RECTANGLE_FILLED = "RECTANGLE_FILLED"
    RECTANGLE_HOLLOW = "RECTANGLE_HOLLOW"
    LETTERS_P = "LETTERS_P"
    LETTERS_PS = "LETTERS_PS"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "MonomerVisualSymbol":
        if not isinstance(val, str):
            raise ValueError(f"Value of MonomerVisualSymbol must be a string (encountered: {val})")
        newcls = Enum("MonomerVisualSymbol", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(MonomerVisualSymbol, getattr(newcls, "_UNKNOWN"))
