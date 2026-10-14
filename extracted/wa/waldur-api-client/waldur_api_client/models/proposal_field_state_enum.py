from enum import Enum


class ProposalFieldStateEnum(str, Enum):
    HIDDEN = "hidden"
    OPTIONAL = "optional"
    REQUIRED = "required"

    def __str__(self) -> str:
        return str(self.value)
