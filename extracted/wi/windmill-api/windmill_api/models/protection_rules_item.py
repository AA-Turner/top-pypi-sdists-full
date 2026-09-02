from enum import Enum


class ProtectionRulesItem(str, Enum):
    DISABLEDIRECTDEPLOYMENT = "DisableDirectDeployment"
    DISABLEWORKSPACEFORKING = "DisableWorkspaceForking"
    RESTRICTANONYMOUSAPPDEPLOYMENT = "RestrictAnonymousAppDeployment"
    RESTRICTDEPLOYTODEPLOYERS = "RestrictDeployToDeployers"
    RESTRICTPUBLICRUNSHARING = "RestrictPublicRunSharing"

    def __str__(self) -> str:
        return str(self.value)
