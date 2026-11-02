from enum import Enum


class WebhookFiltersUserOrFolderRegex(str, Enum):
    F = "f"
    U = "u"
    VALUE_0 = "*"

    def __str__(self) -> str:
        return str(self.value)
