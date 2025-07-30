from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class DnaOligoUpdatedWebhookV3Type(Enums.KnownString):
    V3_DNAOLIGOUPDATED = "v3.dnaOligo.updated"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "DnaOligoUpdatedWebhookV3Type":
        if not isinstance(val, str):
            raise ValueError(f"Value of DnaOligoUpdatedWebhookV3Type must be a string (encountered: {val})")
        newcls = Enum("DnaOligoUpdatedWebhookV3Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(DnaOligoUpdatedWebhookV3Type, getattr(newcls, "_UNKNOWN"))
