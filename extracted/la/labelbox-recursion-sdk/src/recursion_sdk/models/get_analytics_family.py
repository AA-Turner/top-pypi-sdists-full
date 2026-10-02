from enum import StrEnum

class GetAnalyticsFamily(StrEnum):
    MANAGED_AGENT_COMPLETION = "managed_agent_completion"
    MANAGED_AGENT_ENVIRONMENT = "managed_agent_environment"
    MANAGED_AGENT_QUALITY = "managed_agent_quality"
    MANAGED_AGENT_TURN = "managed_agent_turn"
    MANAGED_AGENT_USAGE = "managed_agent_usage"

    def __str__(self) -> str:
        return str(self.value)
