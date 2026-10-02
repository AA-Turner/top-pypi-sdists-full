from enum import Enum


class BillingSourceEnum(str, Enum):
    PLACEMENT = "placement"
    QUOTA = "quota"

    def __str__(self) -> str:
        return str(self.value)
