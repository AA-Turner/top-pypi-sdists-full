from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class RnaSequenceCreatedWebhookV3Type(Enums.KnownString):
    V3_RNASEQUENCECREATED = "v3.rnaSequence.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "RnaSequenceCreatedWebhookV3Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of RnaSequenceCreatedWebhookV3Type must be a string (encountered: {val})"
            )
        newcls = Enum("RnaSequenceCreatedWebhookV3Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(RnaSequenceCreatedWebhookV3Type, getattr(newcls, "_UNKNOWN"))
