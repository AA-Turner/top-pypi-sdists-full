from enum import Enum

class ChannelMessageAccess(str, Enum):
    Addressed = "addressed",
    Ambient = "ambient",

