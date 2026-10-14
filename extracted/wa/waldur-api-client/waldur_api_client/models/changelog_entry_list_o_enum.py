from enum import Enum


class ChangelogEntryListOEnum(str, Enum):
    CATEGORY = "category"
    RISK = "risk"
    TITLE = "title"
    TYPE = "type"
    VALUE_0 = "-category"
    VALUE_1 = "-risk"
    VALUE_2 = "-title"
    VALUE_3 = "-type"
    VALUE_4 = "-version"
    VERSION = "version"

    def __str__(self) -> str:
        return str(self.value)
