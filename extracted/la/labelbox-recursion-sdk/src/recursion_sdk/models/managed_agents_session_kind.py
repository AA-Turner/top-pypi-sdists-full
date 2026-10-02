from enum import StrEnum

class ManagedAgentsSessionKind(StrEnum):
    API_CALL = "api_call"
    BENCHMARK = "benchmark"
    CHAT = "chat"
    EVALUATION = "evaluation"
    REFLECTION = "reflection"
    ROLLOUT = "rollout"
    SESSION_ANALYST = "session_analyst"
    SUBAGENT = "subagent"

    def __str__(self) -> str:
        return str(self.value)
