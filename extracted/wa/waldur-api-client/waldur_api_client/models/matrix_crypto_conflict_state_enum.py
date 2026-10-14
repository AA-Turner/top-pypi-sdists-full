from enum import Enum


class MatrixCryptoConflictStateEnum(str, Enum):
    IN_PROGRESS = "in_progress"
    LOCKED = "locked"
    NOT_LOCKED = "not_locked"
    NO_LEASE = "no_lease"
    SET_UP = "set_up"
    WRONG_KEY = "wrong_key"

    def __str__(self) -> str:
        return str(self.value)
