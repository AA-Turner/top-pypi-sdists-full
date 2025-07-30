from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class RnaOligoUpdatedWebhookV3Type(Enums.KnownString):
    V3_RNAOLIGOUPDATED = "v3.rnaOligo.updated"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "RnaOligoUpdatedWebhookV3Type":
        if not isinstance(val, str):
            raise ValueError(f"Value of RnaOligoUpdatedWebhookV3Type must be a string (encountered: {val})")
        newcls = Enum("RnaOligoUpdatedWebhookV3Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(RnaOligoUpdatedWebhookV3Type, getattr(newcls, "_UNKNOWN"))
