from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ProjectUpdatedWebhookV3Type(Enums.KnownString):
    V3_PROJECTUPDATED = "v3.project.updated"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ProjectUpdatedWebhookV3Type":
        if not isinstance(val, str):
            raise ValueError(f"Value of ProjectUpdatedWebhookV3Type must be a string (encountered: {val})")
        newcls = Enum("ProjectUpdatedWebhookV3Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ProjectUpdatedWebhookV3Type, getattr(newcls, "_UNKNOWN"))
