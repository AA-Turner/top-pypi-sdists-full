from enum import IntEnum


class PermissionLevel(IntEnum):
    NONE = 0
    READ = 1
    WRITE = 2
    ADMIN = 4
