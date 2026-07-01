from enum import Enum

class ChannelSetupGuide_required_credentials(str, Enum):
    Bot_token = "bot_token",
    Signing_secret = "signing_secret",

