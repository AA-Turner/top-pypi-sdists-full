from enum import StrEnum

class EnvironmentFormAlreadyAttachedErrorDtoCode(StrEnum):
    ENVIRONMENT_FORM_ALREADY_ATTACHED = "environment_form_already_attached"

    def __str__(self) -> str:
        return str(self.value)
