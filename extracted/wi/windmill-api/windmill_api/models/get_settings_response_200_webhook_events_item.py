from enum import Enum


class GetSettingsResponse200WebhookEventsItem(str, Enum):
    ARCHIVEFLOW = "ArchiveFlow"
    CREATEAPP = "CreateApp"
    CREATEFLOW = "CreateFlow"
    CREATEFOLDER = "CreateFolder"
    CREATERESOURCE = "CreateResource"
    CREATERESOURCETYPE = "CreateResourceType"
    CREATESCRIPT = "CreateScript"
    CREATEVARIABLE = "CreateVariable"
    DELETEAPP = "DeleteApp"
    DELETEFLOW = "DeleteFlow"
    DELETEFOLDER = "DeleteFolder"
    DELETERESOURCE = "DeleteResource"
    DELETERESOURCETYPE = "DeleteResourceType"
    DELETESCRIPT = "DeleteScript"
    DELETESCRIPTPATH = "DeleteScriptPath"
    DELETEVARIABLE = "DeleteVariable"
    TOKENEXPIRED = "TokenExpired"
    TOKENEXPIRINGSOON = "TokenExpiringSoon"
    UPDATEAPP = "UpdateApp"
    UPDATEFLOW = "UpdateFlow"
    UPDATEFOLDER = "UpdateFolder"
    UPDATERESOURCE = "UpdateResource"
    UPDATERESOURCETYPE = "UpdateResourceType"
    UPDATESCRIPT = "UpdateScript"
    UPDATEVARIABLE = "UpdateVariable"

    def __str__(self) -> str:
        return str(self.value)
