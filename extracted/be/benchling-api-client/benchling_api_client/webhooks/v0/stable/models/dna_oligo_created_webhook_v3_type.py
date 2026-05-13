from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class DnaOligoCreatedWebhookV3Type(Enums.KnownString):
    V3_DNAOLIGOCREATED = "v3.dnaOligo.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "DnaOligoCreatedWebhookV3Type":
        if not isinstance(val, str):
            raise ValueError(f"Value of DnaOligoCreatedWebhookV3Type must be a string (encountered: {val})")
        newcls = Enum("DnaOligoCreatedWebhookV3Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(DnaOligoCreatedWebhookV3Type, getattr(newcls, "_UNKNOWN"))
