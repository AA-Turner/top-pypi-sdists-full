from enum import Enum


class PlanBillingMode(str, Enum):
    INHERIT = "inherit"
    LIMIT = "limit"
    USAGE = "usage"

    def __str__(self) -> str:
        return str(self.value)
