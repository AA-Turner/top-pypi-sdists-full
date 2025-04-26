from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class BarcodeScanFormInstanceProviderIdentifierType(Enums.KnownString):
    NAME_ONLY = "NAME_ONLY"
    REGISTRY_ID_ONLY = "REGISTRY_ID_ONLY"
    ANY_IDENTIFIER = "ANY_IDENTIFIER"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "BarcodeScanFormInstanceProviderIdentifierType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of BarcodeScanFormInstanceProviderIdentifierType must be a string (encountered: {val})"
            )
        newcls = Enum("BarcodeScanFormInstanceProviderIdentifierType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(BarcodeScanFormInstanceProviderIdentifierType, getattr(newcls, "_UNKNOWN"))
