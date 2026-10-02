from enum import Enum


class UsageLimitRestrictionEnum(str, Enum):
    DOWNSCALED = "downscaled"
    PAUSED = "paused"

    def __str__(self) -> str:
        return str(self.value)
