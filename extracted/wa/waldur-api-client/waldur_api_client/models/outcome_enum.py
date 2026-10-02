from enum import Enum


class OutcomeEnum(str, Enum):
    ACCEPTED = "accepted"
    APPROVED = "approved"
    DECLINED = "declined"
    ELIGIBLE = "eligible"
    EXPIRED = "expired"
    FEASIBLE = "feasible"
    INELIGIBLE = "ineligible"
    INFEASIBLE = "infeasible"
    REJECTED = "rejected"
    REVIEWED = "reviewed"

    def __str__(self) -> str:
        return str(self.value)
