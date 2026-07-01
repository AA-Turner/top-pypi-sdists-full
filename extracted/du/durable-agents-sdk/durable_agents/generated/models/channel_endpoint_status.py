from enum import Enum

class ChannelEndpoint_status(str, Enum):
    Available = "available",
    Bound = "bound",
    Needs_configuration = "needs_configuration",

