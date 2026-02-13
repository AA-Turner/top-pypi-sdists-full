from enum import Enum


class UpdateProtectionRuleJsonBodyRulesItem(str, Enum):
    DISABLEDIRECTDEPLOYMENT = "DisableDirectDeployment"
    DISABLEWORKSPACEFORKING = "DisableWorkspaceForking"

    def __str__(self) -> str:
        return str(self.value)
