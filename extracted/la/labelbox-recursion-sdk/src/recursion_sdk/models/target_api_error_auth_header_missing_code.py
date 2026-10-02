from enum import StrEnum

class TargetApiErrorAuthHeaderMissingCode(StrEnum):
    AUTH_HEADER_MISSING = "auth_header_missing"

    def __str__(self) -> str:
        return str(self.value)
