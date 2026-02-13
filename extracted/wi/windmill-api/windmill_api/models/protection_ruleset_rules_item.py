from enum import Enum


class ProtectionRulesetRulesItem(str, Enum):
    DISABLEDIRECTDEPLOYMENT = "DisableDirectDeployment"
    DISABLEWORKSPACEFORKING = "DisableWorkspaceForking"

    def __str__(self) -> str:
        return str(self.value)
