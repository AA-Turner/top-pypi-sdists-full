from enum import Enum


class ProficiencyLevelEnum(str, Enum):
    BASIC = "basic"
    EXPERT = "expert"
    FAMILIAR = "familiar"

    def __str__(self) -> str:
        return str(self.value)
