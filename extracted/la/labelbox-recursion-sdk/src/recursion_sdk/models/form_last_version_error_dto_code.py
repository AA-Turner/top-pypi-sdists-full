from enum import StrEnum

class FormLastVersionErrorDtoCode(StrEnum):
    FORM_LAST_VERSION = "form_last_version"

    def __str__(self) -> str:
        return str(self.value)
