from enum import Enum


class PublicErrorCode(str, Enum):
    ALREADY_EXISTS = "already_exists"
    COMMAND_FAILED = "command_failed"
    DEADLINE_EXCEEDED = "deadline_exceeded"
    FAILED_PRECONDITION = "failed_precondition"
    FEATURE_TEMPORARILY_DISABLED = "FEATURE_TEMPORARILY_DISABLED"
    INTERNAL = "internal"
    INVALID_ARGUMENT = "invalid_argument"
    NOT_FOUND = "not_found"
    PERMISSION_DENIED = "permission_denied"
    RATE_LIMITED = "rate_limited"
    UNAUTHENTICATED = "unauthenticated"
    UNAVAILABLE = "unavailable"
    UNIMPLEMENTED = "unimplemented"

    def __str__(self) -> str:
        return str(self.value)
