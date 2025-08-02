from enum import Enum


class EditWorkspaceGitSyncConfigJsonBodyGitSyncSettingsRepositoriesItemSettingsIncludeTypeItem(str, Enum):
    APP = "app"
    FLOW = "flow"
    FOLDER = "folder"
    GROUP = "group"
    KEY = "key"
    RESOURCE = "resource"
    RESOURCETYPE = "resourcetype"
    SCHEDULE = "schedule"
    SCRIPT = "script"
    SECRET = "secret"
    SETTINGS = "settings"
    TRIGGER = "trigger"
    USER = "user"
    VARIABLE = "variable"

    def __str__(self) -> str:
        return str(self.value)
