from enum import Enum


class ExportableQueuedJobJobKind(str, Enum):
    AIAGENT = "aiagent"
    APPDEPENDENCIES = "appdependencies"
    APPSCRIPT = "appscript"
    DEPENDENCIES = "dependencies"
    DEPLOYMENTCALLBACK = "deploymentcallback"
    FLOW = "flow"
    FLOWDEPENDENCIES = "flowdependencies"
    FLOWNODE = "flownode"
    FLOWPREVIEW = "flowpreview"
    FLOWSCRIPT = "flowscript"
    IDENTITY = "identity"
    PREVIEW = "preview"
    SCRIPT = "script"
    SCRIPT_HUB = "script_hub"
    SINGLESTEPFLOW = "singlestepflow"
    UNASSIGNED_FLOW = "unassigned_flow"
    UNASSIGNED_SCRIPT = "unassigned_script"
    UNASSIGNED_SINGLESTEPFLOW = "unassigned_singlestepflow"

    def __str__(self) -> str:
        return str(self.value)
