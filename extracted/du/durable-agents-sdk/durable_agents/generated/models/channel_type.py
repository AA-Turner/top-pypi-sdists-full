from enum import Enum

class ChannelType(str, Enum):
    Discord = "discord",
    Email = "email",
    Google_chat = "google_chat",
    Messaging = "messaging",
    Slack = "slack",
    Teams = "teams",
    Telegram = "telegram",
    Voice = "voice",
    Whats_app = "whats_app",

