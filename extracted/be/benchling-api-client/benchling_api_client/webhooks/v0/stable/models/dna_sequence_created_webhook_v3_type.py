from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class DnaSequenceCreatedWebhookV3Type(Enums.KnownString):
    V3_DNASEQUENCECREATED = "v3.dnaSequence.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "DnaSequenceCreatedWebhookV3Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of DnaSequenceCreatedWebhookV3Type must be a string (encountered: {val})"
            )
        newcls = Enum("DnaSequenceCreatedWebhookV3Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(DnaSequenceCreatedWebhookV3Type, getattr(newcls, "_UNKNOWN"))
