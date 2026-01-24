from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class MoleculeWithEntityTypeEntityType(Enums.KnownString):
    MOLECULE = "molecule"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "MoleculeWithEntityTypeEntityType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of MoleculeWithEntityTypeEntityType must be a string (encountered: {val})"
            )
        newcls = Enum("MoleculeWithEntityTypeEntityType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(MoleculeWithEntityTypeEntityType, getattr(newcls, "_UNKNOWN"))
