from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class RnaOligoCreatedWebhookV3Type(Enums.KnownString):
    V3_RNAOLIGOCREATED = "v3.rnaOligo.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "RnaOligoCreatedWebhookV3Type":
        if not isinstance(val, str):
            raise ValueError(f"Value of RnaOligoCreatedWebhookV3Type must be a string (encountered: {val})")
        newcls = Enum("RnaOligoCreatedWebhookV3Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(RnaOligoCreatedWebhookV3Type, getattr(newcls, "_UNKNOWN"))
