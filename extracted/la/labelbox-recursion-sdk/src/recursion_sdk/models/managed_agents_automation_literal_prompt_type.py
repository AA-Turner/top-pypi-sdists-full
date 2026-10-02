from enum import StrEnum

class ManagedAgentsAutomationLiteralPromptType(StrEnum):
    LITERAL = "literal"

    def __str__(self) -> str:
        return str(self.value)
