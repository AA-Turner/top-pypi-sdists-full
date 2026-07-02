from enum import Enum

class EndpointProvider(str, Enum):
    Email = "email",
    Imessage = "imessage",
    Voice = "voice",
    Slack = "slack",
    Teams = "teams",
    Discord = "discord",
    Telegram = "telegram",
    Google_chat = "google_chat",
    Whatsapp = "whatsapp",

