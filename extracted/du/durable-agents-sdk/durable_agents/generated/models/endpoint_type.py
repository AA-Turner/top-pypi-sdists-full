from enum import Enum

class EndpointType(str, Enum):
    Channel = "channel",
    Inbox = "inbox",
    Conversation = "conversation",
    Messaging = "messaging",
    Voice = "voice",

