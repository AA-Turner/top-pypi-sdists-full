from enum import Enum

class ConnectorProvider(str, Enum):
    Slack = "slack",
    Teams = "teams",
    Discord = "discord",
    Telegram = "telegram",
    Google_chat = "google_chat",
    Whatsapp = "whatsapp",

