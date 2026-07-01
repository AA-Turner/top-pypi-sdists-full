from enum import Enum


class OrganizationPlanType(str, Enum):
    PAID = "paid"
    TRIAL = "trial"

    def __str__(self) -> str:
        return str(self.value)
