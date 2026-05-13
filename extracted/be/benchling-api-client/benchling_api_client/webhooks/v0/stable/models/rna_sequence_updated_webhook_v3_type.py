from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class RnaSequenceUpdatedWebhookV3Type(Enums.KnownString):
    V3_RNASEQUENCEUPDATED = "v3.rnaSequence.updated"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "RnaSequenceUpdatedWebhookV3Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of RnaSequenceUpdatedWebhookV3Type must be a string (encountered: {val})"
            )
        newcls = Enum("RnaSequenceUpdatedWebhookV3Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(RnaSequenceUpdatedWebhookV3Type, getattr(newcls, "_UNKNOWN"))
