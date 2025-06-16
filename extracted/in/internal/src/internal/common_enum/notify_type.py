from enum import Enum


class NotifyTypeEnum(str, Enum):
    LINE = "line"
    SMS = "sms"
    APP = "app"
    USER_BELL_NOTIFICATION = "user_bell_notification"
    WEBSOCKET = "websocket"