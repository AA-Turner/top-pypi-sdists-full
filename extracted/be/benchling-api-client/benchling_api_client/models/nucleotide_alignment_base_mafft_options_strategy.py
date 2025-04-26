from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class NucleotideAlignmentBaseMafftOptionsStrategy(Enums.KnownString):
    AUTO = "auto"
    SIXMER = "sixmer"
    LOCALPAIR = "localpair"
    GLOBALPAIR = "globalpair"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "NucleotideAlignmentBaseMafftOptionsStrategy":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of NucleotideAlignmentBaseMafftOptionsStrategy must be a string (encountered: {val})"
            )
        newcls = Enum("NucleotideAlignmentBaseMafftOptionsStrategy", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(NucleotideAlignmentBaseMafftOptionsStrategy, getattr(newcls, "_UNKNOWN"))
