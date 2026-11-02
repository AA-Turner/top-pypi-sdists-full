from enum import Enum


class CreateWorkspaceForkDevWorkspaceLabel(str, Enum):
    DEMO = "demo"
    DEV = "dev"
    PREPROD = "preprod"
    QA = "qa"
    SANDBOX = "sandbox"
    STAGING = "staging"
    TEST = "test"
    UAT = "uat"

    def __str__(self) -> str:
        return str(self.value)
