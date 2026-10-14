from enum import Enum


class ChangelogEntryListScopeEnum(str, Enum):
    CORE = "core"
    DEV = "dev"
    INFRA = "infra"
    PLUGIN = "plugin"

    def __str__(self) -> str:
        return str(self.value)
