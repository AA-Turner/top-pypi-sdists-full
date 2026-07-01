from enum import Enum

class AuditEvent_actor(str, Enum):
    Api_key = "api_key",
    Session = "session",
    System = "system",
    Stripe = "stripe",
    Webhook = "webhook",

