from enum import Enum

class DiscordCommandRegistration_scope(str, Enum):
    Global_ = "global",
    Guild = "guild",

