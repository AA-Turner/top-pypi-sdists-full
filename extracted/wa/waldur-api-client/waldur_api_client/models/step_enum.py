from enum import Enum


class StepEnum(str, Enum):
    ADMINISTRATIVE_CHECK = "administrative_check"
    ALLOCATION_DECISION = "allocation_decision"
    AWARD_RESPONSE = "award_response"
    EXPERT_REVIEW = "expert_review"
    PANEL_REVIEW = "panel_review"
    TECHNICAL_ASSESSMENT = "technical_assessment"

    def __str__(self) -> str:
        return str(self.value)
