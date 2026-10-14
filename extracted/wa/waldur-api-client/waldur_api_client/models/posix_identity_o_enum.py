from enum import Enum


class PosixIdentityOEnum(str, Enum):
    CREATED = "created"
    GID = "gid"
    RELEASED_AT = "released_at"
    UID = "uid"
    VALUE_0 = "-created"
    VALUE_1 = "-gid"
    VALUE_2 = "-released_at"
    VALUE_3 = "-uid"

    def __str__(self) -> str:
        return str(self.value)
