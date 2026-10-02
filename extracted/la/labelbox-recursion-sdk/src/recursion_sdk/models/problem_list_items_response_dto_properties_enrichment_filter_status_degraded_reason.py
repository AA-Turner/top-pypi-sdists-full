from enum import StrEnum

class ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusDegradedReason(StrEnum):
    AUTH = "auth"
    INVALID_RESPONSE = "invalid-response"
    TIMEOUT = "timeout"
    TOO_MANY_CANDIDATES = "too-many-candidates"
    UNAVAILABLE = "unavailable"

    def __str__(self) -> str:
        return str(self.value)
