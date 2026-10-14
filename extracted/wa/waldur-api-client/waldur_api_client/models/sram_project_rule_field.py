from enum import Enum


class SramProjectRuleField(str, Enum):
    BACKEND_ID = "backend_id"
    SLUG = "slug"

    def __str__(self) -> str:
        return str(self.value)
