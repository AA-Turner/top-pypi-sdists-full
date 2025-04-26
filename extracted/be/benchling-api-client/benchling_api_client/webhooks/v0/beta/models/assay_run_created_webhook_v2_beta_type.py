from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssayRunCreatedWebhookV2BetaType(Enums.KnownString):
    V2_BETAASSAYRUNCREATED = "v2-beta.assayRun.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssayRunCreatedWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AssayRunCreatedWebhookV2BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("AssayRunCreatedWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssayRunCreatedWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
