from enum import StrEnum

class FormVersionAlreadyPublishedErrorDtoCode(StrEnum):
    FORM_VERSION_ALREADY_PUBLISHED = "form_version_already_published"

    def __str__(self) -> str:
        return str(self.value)
