from enum import Enum


class AgreementTypeEnum(str, Enum):
    PP = "PP"
    TOS = "TOS"

    def __str__(self) -> str:
        return str(self.value)
