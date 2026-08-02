from dataclasses import dataclass
import json

from python_agent import __version__ as VERSION


@dataclass
class SLMetadata:
    agentId: str = ""
    agentTechnology: str = "python"
    agentVersion: str = VERSION
    agentType: str = ""
    labId: str = ""
    buildSessionId: str = ""
    appName: str = ""
    branchName: str = ""
    buildName: str = ""
    executionId: str = ""
    messageType: str = ""

    def to_json(self) -> str:
        """Convert the SLMetadata object to a JSON string."""
        data = {
            "agentId": self.agentId,
            "agentTechnology": self.agentTechnology,
            "agentVersion": self.agentVersion,
            "agentType": self.agentType,
            "labId": self.labId,
            "buildSessionId": self.buildSessionId,
            "appName": self.appName,
            "branchName": self.branchName,
            "buildName": self.buildName,
            "executionId": self.executionId,
            "messageType": self.messageType,
        }
        return json.dumps(data)

    @staticmethod
    def from_config_data(config_data) -> "SLMetadata":
        def get_value_or_default(attr, default):
            if hasattr(config_data, attr):
                value = config_data.__getattribute__(attr)
                if value:
                    return value
                else:
                    return default
            else:
                return default

        sl_metadata = SLMetadata()
        sl_metadata.agentId = get_value_or_default("agentId", "")
        sl_metadata.agentTechnology = get_value_or_default("agentTechnology", "python")
        sl_metadata.agentVersion = get_value_or_default("agentVersion", VERSION)
        sl_metadata.agentType = get_value_or_default("agentType", "")
        sl_metadata.labId = get_value_or_default("labId", "")
        sl_metadata.executionId = get_value_or_default("executionId", "")
        sl_metadata.buildSessionId = get_value_or_default("buildSessionId", "")
        sl_metadata.appName = get_value_or_default("appName", "")
        sl_metadata.branchName = get_value_or_default("branchName", "")
        sl_metadata.buildName = get_value_or_default("buildName", "")
        sl_metadata.messageType = get_value_or_default("messageType", "")
        return sl_metadata
