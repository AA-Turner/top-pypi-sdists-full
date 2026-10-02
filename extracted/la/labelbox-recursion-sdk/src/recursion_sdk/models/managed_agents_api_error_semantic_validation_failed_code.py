from enum import StrEnum

class ManagedAgentsApiErrorSemanticValidationFailedCode(StrEnum):
    SEMANTIC_VALIDATION_FAILED = "semantic_validation_failed"

    def __str__(self) -> str:
        return str(self.value)
