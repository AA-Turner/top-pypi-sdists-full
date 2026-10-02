from enum import StrEnum

class ManagedAgentsEvaluationOverviewResponseChangeMarkersStatus(StrEnum):
    COMPLETE = "complete"
    SELECT_TARGET_AGENT = "select_target_agent"

    def __str__(self) -> str:
        return str(self.value)
