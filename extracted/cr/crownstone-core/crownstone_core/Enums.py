from enum import Enum


class CrownstoneOperationMode(Enum):
    NORMAL = 0
    SETUP  = 1
    DFU    = 2
    UNKNOWN = 255

