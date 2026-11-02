from enum import StrEnum


class Platform(StrEnum):
    WEB = "web"
    IOS = "ios"
    ANDROID = "android"


class DeviceStatus(StrEnum):
    ACTIVE = "active"
    LOGGED_OUT = "logged_out"
    DISABLED = "disabled"


class TokenStatus(StrEnum):
    VALID = "valid"
    INVALID = "invalid"
    UNKNOWN = "unknown"


class NotificationIntentType(StrEnum):
    CHAT_ASSIGNED = "chat_assigned"
    CHAT_MESSAGE_RECEIVED = "chat_message_received"
    CHAT_ESCALATED = "chat_escalated"


class NotificationChannel(StrEnum):
    PUSH = "push"
