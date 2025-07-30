from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class DnaSequenceUpdatedWebhookV3Type(Enums.KnownString):
    V3_DNASEQUENCEUPDATED = "v3.dnaSequence.updated"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "DnaSequenceUpdatedWebhookV3Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of DnaSequenceUpdatedWebhookV3Type must be a string (encountered: {val})"
            )
        newcls = Enum("DnaSequenceUpdatedWebhookV3Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(DnaSequenceUpdatedWebhookV3Type, getattr(newcls, "_UNKNOWN"))
