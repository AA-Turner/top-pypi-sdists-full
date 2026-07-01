from enum import Enum

class RunMode(str, Enum):
    Sync = "sync",
    Async_ = "async",
    Channel = "channel",
    Heartbeat = "heartbeat",
    Webhook = "webhook",

