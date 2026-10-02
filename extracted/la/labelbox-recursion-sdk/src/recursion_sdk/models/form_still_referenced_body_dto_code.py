from enum import StrEnum

class FormStillReferencedBodyDtoCode(StrEnum):
    FORM_STILL_REFERENCED = "form_still_referenced"

    def __str__(self) -> str:
        return str(self.value)
