from enum import Enum

class ChannelStatus(str, Enum):
    Active = "active",
    Disabled = "disabled",
    Needs_configuration = "needs_configuration",

