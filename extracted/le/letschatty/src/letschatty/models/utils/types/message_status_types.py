from enum import StrEnum

class Status(StrEnum):
    READ = "read"
    DELIVERED = "delivered"
    SENT = "sent"
    WAITING = "waiting" #user started the action but we still haven't received the confirmation from the external API
    FAILED = "failed"
    # ANSWERED = "answered"
    # INTERACTION = "interaction"