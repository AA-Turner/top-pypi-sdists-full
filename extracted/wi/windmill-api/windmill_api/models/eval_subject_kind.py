from enum import Enum


class EvalSubjectKind(str, Enum):
    AGENT = "agent"
    AGENT_DRAFT = "agent_draft"
    AGENT_VERSION = "agent_version"

    def __str__(self) -> str:
        return str(self.value)
