from enum import IntEnum


class UserLevel(IntEnum):
    admin   = 0
    member  = 1
    basic   = 2
    setup   = 100
    unknown = 255

