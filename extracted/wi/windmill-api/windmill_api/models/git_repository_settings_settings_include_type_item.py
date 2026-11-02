from enum import Enum


class GitRepositorySettingsSettingsIncludeTypeItem(str, Enum):
    APP = "app"
    DATATABLEMIGRATION = "datatablemigration"
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
    WORKSPACEDEPENDENCIES = "workspacedependencies"

    def __str__(self) -> str:
        return str(self.value)
