from enum import Enum


class ProtectionRulesItem(str, Enum):
    DISABLEDIRECTDEPLOYMENT = "DisableDirectDeployment"
    DISABLEWORKSPACEFORKING = "DisableWorkspaceForking"

    def __str__(self) -> str:
        return str(self.value)
