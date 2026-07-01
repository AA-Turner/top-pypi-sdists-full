from enum import Enum

class DiscordSetupGuide_required_credentials(str, Enum):
    Application_id = "application_id",
    Public_key = "public_key",
    Bot_token = "bot_token",

