from enum import Enum


class CreateProtectionRuleJsonBodyRulesItem(str, Enum):
    DISABLEDIRECTDEPLOYMENT = "DisableDirectDeployment"
    DISABLEWORKSPACEFORKING = "DisableWorkspaceForking"
    RESTRICTANONYMOUSAPPDEPLOYMENT = "RestrictAnonymousAppDeployment"
    RESTRICTDEPLOYTODEPLOYERS = "RestrictDeployToDeployers"
    RESTRICTGUESTAPPDEPLOYMENT = "RestrictGuestAppDeployment"
    RESTRICTPUBLICRUNSHARING = "RestrictPublicRunSharing"

    def __str__(self) -> str:
        return str(self.value)
