from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class SearchInputUiBlockItemType(Enums.KnownString):
    DNA_SEQUENCE = "dna_sequence"
    DNA_OLIGO = "dna_oligo"
    AA_SEQUENCE = "aa_sequence"
    CUSTOM_ENTITY = "custom_entity"
    MIXTURE = "mixture"
    BOX = "box"
    CONTAINER = "container"
    LOCATION = "location"
    PLATE = "plate"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "SearchInputUiBlockItemType":
        if not isinstance(val, str):
            raise ValueError(f"Value of SearchInputUiBlockItemType must be a string (encountered: {val})")
        newcls = Enum("SearchInputUiBlockItemType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(SearchInputUiBlockItemType, getattr(newcls, "_UNKNOWN"))
