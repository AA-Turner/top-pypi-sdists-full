from enum import Enum


class GetHubIntegrationMetaResponse200DerivedStyle(str, Enum):
    FETCH = "fetch"
    MIXED = "mixed"
    SDK = "sdk"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
