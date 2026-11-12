from enum import StrEnum

class ForgeErrorKind(StrEnum):
    CONFLICT = "conflict"
    NOT_FOUND = "not_found"
    RATE_LIMITED = "rate_limited"
    UNAUTHORIZED = "unauthorized"
    UNKNOWN = "unknown"
    UNREACHABLE = "unreachable"
    UPSTREAM_ERROR = "upstream_error"

    def __str__(self) -> str:
        return str(self.value)
