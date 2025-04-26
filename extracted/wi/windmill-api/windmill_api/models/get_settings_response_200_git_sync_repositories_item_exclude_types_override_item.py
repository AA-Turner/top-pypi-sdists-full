from enum import Enum


class GetSettingsResponse200GitSyncRepositoriesItemExcludeTypesOverrideItem(str, Enum):
    APP = "app"
    FLOW = "flow"
    FOLDER = "folder"
    GROUP = "group"
    RESOURCE = "resource"
    RESOURCETYPE = "resourcetype"
    SCHEDULE = "schedule"
    SCRIPT = "script"
    SECRET = "secret"
    USER = "user"
    VARIABLE = "variable"

    def __str__(self) -> str:
        return str(self.value)
