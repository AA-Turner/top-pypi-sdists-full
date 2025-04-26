from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssayRunUpdatedFieldsWebhookV2BetaType(Enums.KnownString):
    V2_BETAASSAYRUNUPDATEDFIELDS = "v2-beta.assayRun.updated.fields"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssayRunUpdatedFieldsWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AssayRunUpdatedFieldsWebhookV2BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("AssayRunUpdatedFieldsWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssayRunUpdatedFieldsWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
