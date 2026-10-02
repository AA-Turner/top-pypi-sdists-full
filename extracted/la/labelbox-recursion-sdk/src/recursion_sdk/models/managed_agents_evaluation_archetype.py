from enum import StrEnum

class ManagedAgentsEvaluationArchetype(StrEnum):
    ARTIFACT = "artifact"
    AUTOMATION = "automation"
    BENCHMARK = "benchmark"
    CONVERSATION = "conversation"
    CRITIQUE = "critique"
    EXTERNAL = "external"
    INTERACTIVE = "interactive"

    def __str__(self) -> str:
        return str(self.value)
