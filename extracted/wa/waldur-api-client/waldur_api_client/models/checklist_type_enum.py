from enum import Enum


class ChecklistTypeEnum(str, Enum):
    OFFERING_COMPLIANCE = "offering_compliance"
    ONBOARDING_CUSTOMER = "onboarding_customer"
    ONBOARDING_INTENT = "onboarding_intent"
    PROJECT_COMPLIANCE = "project_compliance"
    PROJECT_METADATA = "project_metadata"
    PROPOSAL_COMPLIANCE = "proposal_compliance"
    WORKFLOW_STEP = "workflow_step"

    def __str__(self) -> str:
        return str(self.value)
