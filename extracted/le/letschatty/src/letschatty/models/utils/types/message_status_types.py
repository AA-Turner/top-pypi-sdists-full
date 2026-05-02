from enum import StrEnum

class Status(StrEnum):
    READ = "read"
    DELIVERED = "delivered"
    SENT = "sent"
    WAITING = "waiting" #user started the action but we still haven't received the confirmation from the external API
    FAILED = "failed"
    META_API_CALL_SUCCESS = "success" #The META api call was succesfull but still haven't received a webhook notification with a new status
    PENDING = "pending" #For template campaigns, when the recipient is pending to be processed
    # ANSWERED = "answered"
    # INTERACTION = "interaction"