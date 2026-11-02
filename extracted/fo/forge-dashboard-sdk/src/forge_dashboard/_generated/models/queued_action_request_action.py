from enum import StrEnum

class QueuedActionRequestAction(StrEnum):
    DEPENDABOT_REBASE = "dependabot_rebase"
    RENOVATE_REBASE = "renovate_rebase"
    UPDATE_BRANCH = "update_branch"

    def __str__(self) -> str:
        return str(self.value)
