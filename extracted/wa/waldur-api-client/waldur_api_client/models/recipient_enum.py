from enum import Enum


class RecipientEnum(str, Enum):
    ALL_POOL_REVIEWERS = "all_pool_reviewers"
    APPLICANT = "applicant"
    ASSIGNED_REVIEWERS = "assigned_reviewers"
    CALL_MANAGERS = "call_managers"
    PANEL_CHAIR = "panel_chair"
    RESPONSIBLE_ROLE = "responsible_role"

    def __str__(self) -> str:
        return str(self.value)
