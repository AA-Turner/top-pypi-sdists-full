from enum import StrEnum

class ForgeHealthCause(StrEnum):
    SLOW = "slow"
    STARTING = "starting"

    def __str__(self) -> str:
        return str(self.value)
