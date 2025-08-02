from enum import Enum


class GetJobResponse200Type0JobKind(str, Enum):
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
    SINGLESCRIPTFLOW = "singlescriptflow"

    def __str__(self) -> str:
        return str(self.value)
