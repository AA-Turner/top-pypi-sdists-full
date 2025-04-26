from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssayRunCreatedWebhookV2Type(Enums.KnownString):
    V2_ASSAYRUNCREATED = "v2.assayRun.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssayRunCreatedWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(f"Value of AssayRunCreatedWebhookV2Type must be a string (encountered: {val})")
        newcls = Enum("AssayRunCreatedWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssayRunCreatedWebhookV2Type, getattr(newcls, "_UNKNOWN"))
