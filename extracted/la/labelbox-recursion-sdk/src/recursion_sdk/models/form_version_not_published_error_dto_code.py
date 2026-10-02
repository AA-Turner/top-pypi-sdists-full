from enum import StrEnum

class FormVersionNotPublishedErrorDtoCode(StrEnum):
    FORM_VERSION_NOT_PUBLISHED = "form_version_not_published"

    def __str__(self) -> str:
        return str(self.value)
