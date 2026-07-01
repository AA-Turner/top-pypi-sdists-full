from enum import Enum

class Connector_status(str, Enum):
    Disconnected = "disconnected",
    Connecting = "connecting",
    Connected = "connected",
    Error = "error",

