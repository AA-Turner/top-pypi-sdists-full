from enum import Enum


class AccountNameGenerationPolicyEnum(str, Enum):
    PROJECT_SLUG = "project_slug"

    def __str__(self) -> str:
        return str(self.value)
