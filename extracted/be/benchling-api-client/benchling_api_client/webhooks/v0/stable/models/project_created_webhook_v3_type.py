from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ProjectCreatedWebhookV3Type(Enums.KnownString):
    V3_PROJECTCREATED = "v3.project.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ProjectCreatedWebhookV3Type":
        if not isinstance(val, str):
            raise ValueError(f"Value of ProjectCreatedWebhookV3Type must be a string (encountered: {val})")
        newcls = Enum("ProjectCreatedWebhookV3Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ProjectCreatedWebhookV3Type, getattr(newcls, "_UNKNOWN"))
