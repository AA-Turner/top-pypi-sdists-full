from enum import StrEnum

class CreateEnvironmentFileUploadUrlsRequestDtoType(StrEnum):
    AGENT_INPUT = "agent-input"
    INSTRUCTIONS = "instructions"

    def __str__(self) -> str:
        return str(self.value)
