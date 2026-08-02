from enum import Enum


class ShutdownMode(Enum):
    ON_DISCONNECT = "on_disconnect"
    ON_INACTIVITY_TIMEOUT = "on_inactivity_timeout"
