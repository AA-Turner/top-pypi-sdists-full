from enum import Enum


class GetSettingsResponse200DucklakeDucklakesAdditionalPropertyForkBehavior(str, Enum):
    ISOLATED = "isolated"
    SHARED = "shared"

    def __str__(self) -> str:
        return str(self.value)
