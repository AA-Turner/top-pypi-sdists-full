from enum import Enum

class AgentMode(str, Enum):
    Interactive = "interactive",
    Heartbeat = "heartbeat",
    Scheduled = "scheduled",
    Triggered = "triggered",
    Webhook = "webhook",

