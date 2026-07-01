from enum import Enum

class ChannelConnector_status(str, Enum):
    Active = "active",
    Disabled = "disabled",
    Error = "error",

