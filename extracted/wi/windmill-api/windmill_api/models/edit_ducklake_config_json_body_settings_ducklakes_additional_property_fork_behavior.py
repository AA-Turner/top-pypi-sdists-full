from enum import Enum


class EditDucklakeConfigJsonBodySettingsDucklakesAdditionalPropertyForkBehavior(str, Enum):
    ISOLATED = "isolated"
    SHARED = "shared"

    def __str__(self) -> str:
        return str(self.value)
