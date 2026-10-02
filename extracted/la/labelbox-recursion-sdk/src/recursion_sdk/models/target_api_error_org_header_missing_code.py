from enum import StrEnum

class TargetApiErrorOrgHeaderMissingCode(StrEnum):
    ORG_HEADER_MISSING = "org_header_missing"

    def __str__(self) -> str:
        return str(self.value)
