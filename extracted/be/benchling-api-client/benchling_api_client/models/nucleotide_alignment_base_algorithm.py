from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class NucleotideAlignmentBaseAlgorithm(Enums.KnownString):
    MAFFT = "mafft"
    CLUSTALO = "clustalo"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "NucleotideAlignmentBaseAlgorithm":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of NucleotideAlignmentBaseAlgorithm must be a string (encountered: {val})"
            )
        newcls = Enum("NucleotideAlignmentBaseAlgorithm", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(NucleotideAlignmentBaseAlgorithm, getattr(newcls, "_UNKNOWN"))
