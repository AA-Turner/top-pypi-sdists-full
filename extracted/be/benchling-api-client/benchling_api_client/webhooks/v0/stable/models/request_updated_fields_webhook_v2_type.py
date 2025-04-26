from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class RequestUpdatedFieldsWebhookV2Type(Enums.KnownString):
    V2_REQUESTUPDATEDFIELDS = "v2.request.updated.fields"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "RequestUpdatedFieldsWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of RequestUpdatedFieldsWebhookV2Type must be a string (encountered: {val})"
            )
        newcls = Enum("RequestUpdatedFieldsWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(RequestUpdatedFieldsWebhookV2Type, getattr(newcls, "_UNKNOWN"))
