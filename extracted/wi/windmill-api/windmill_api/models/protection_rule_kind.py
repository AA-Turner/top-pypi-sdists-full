from enum import Enum


class ProtectionRuleKind(str, Enum):
    DISABLEDIRECTDEPLOYMENT = "DisableDirectDeployment"
    DISABLEWORKSPACEFORKING = "DisableWorkspaceForking"
    RESTRICTDEPLOYTODEPLOYERS = "RestrictDeployToDeployers"

    def __str__(self) -> str:
        return str(self.value)
