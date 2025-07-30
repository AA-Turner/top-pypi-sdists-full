from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class RunCreatedWebhookV3Type(Enums.KnownString):
    V3_RUNCREATED = "v3.run.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "RunCreatedWebhookV3Type":
        if not isinstance(val, str):
            raise ValueError(f"Value of RunCreatedWebhookV3Type must be a string (encountered: {val})")
        newcls = Enum("RunCreatedWebhookV3Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(RunCreatedWebhookV3Type, getattr(newcls, "_UNKNOWN"))
