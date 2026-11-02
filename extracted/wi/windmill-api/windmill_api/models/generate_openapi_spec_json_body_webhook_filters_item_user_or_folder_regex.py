from enum import Enum


class GenerateOpenapiSpecJsonBodyWebhookFiltersItemUserOrFolderRegex(str, Enum):
    F = "f"
    U = "u"
    VALUE_0 = "*"

    def __str__(self) -> str:
        return str(self.value)
