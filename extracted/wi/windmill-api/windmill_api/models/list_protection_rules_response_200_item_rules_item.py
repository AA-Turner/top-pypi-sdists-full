from enum import Enum


class ListProtectionRulesResponse200ItemRulesItem(str, Enum):
    DISABLEDIRECTDEPLOYMENT = "DisableDirectDeployment"
    DISABLEWORKSPACEFORKING = "DisableWorkspaceForking"
    RESTRICTANONYMOUSAPPDEPLOYMENT = "RestrictAnonymousAppDeployment"
    RESTRICTDEPLOYTODEPLOYERS = "RestrictDeployToDeployers"
    RESTRICTPUBLICRUNSHARING = "RestrictPublicRunSharing"

    def __str__(self) -> str:
        return str(self.value)
