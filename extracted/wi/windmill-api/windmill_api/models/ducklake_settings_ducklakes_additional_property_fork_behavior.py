from enum import Enum


class DucklakeSettingsDucklakesAdditionalPropertyForkBehavior(str, Enum):
    ISOLATED = "isolated"
    SHARED = "shared"

    def __str__(self) -> str:
        return str(self.value)
