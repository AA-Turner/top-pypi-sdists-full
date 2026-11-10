from enum import Enum


class PolicyGateEnum(str, Enum):
    COST_BELOW_LIMIT = "cost_below_limit"
    COST_OVER_LIMIT = "cost_over_limit"
    CREDIT_EXHAUSTED = "credit_exhausted"
    CREDIT_IGNORED = "credit_ignored"
    HELD_BY_CUSTOMER_CREDIT = "held_by_customer_credit"
    HELD_BY_PROJECT_CREDIT = "held_by_project_credit"
    NO_CREDIT = "no_credit"

    def __str__(self) -> str:
        return str(self.value)
