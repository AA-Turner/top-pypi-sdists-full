from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class RequestUpdatedFieldsWebhookV2BetaType(Enums.KnownString):
    V2_BETAREQUESTUPDATEDFIELDS = "v2-beta.request.updated.fields"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "RequestUpdatedFieldsWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of RequestUpdatedFieldsWebhookV2BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("RequestUpdatedFieldsWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(RequestUpdatedFieldsWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
