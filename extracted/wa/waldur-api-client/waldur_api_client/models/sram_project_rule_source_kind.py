from enum import Enum


class SramProjectRuleSourceKind(str, Enum):
    ANY = "any"
    CO = "co"
    GROUP = "group"

    def __str__(self) -> str:
        return str(self.value)
