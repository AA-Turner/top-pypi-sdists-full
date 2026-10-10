from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AgentCollaboratorType(Enums.KnownString):
    AGENT = "AGENT"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AgentCollaboratorType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AgentCollaboratorType must be a string (encountered: {val})")
        newcls = Enum("AgentCollaboratorType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AgentCollaboratorType, getattr(newcls, "_UNKNOWN"))
