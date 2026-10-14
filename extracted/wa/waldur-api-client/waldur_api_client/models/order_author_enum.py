from enum import Enum


class OrderAuthorEnum(str, Enum):
    APPLICANT = "applicant"
    CALL_MANAGER = "call_manager"
    PROJECT_MANAGER = "project_manager"
    SPECIFIC_USER = "specific_user"

    def __str__(self) -> str:
        return str(self.value)
