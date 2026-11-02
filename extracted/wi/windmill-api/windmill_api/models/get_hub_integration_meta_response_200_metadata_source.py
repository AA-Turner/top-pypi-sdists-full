from enum import Enum


class GetHubIntegrationMetaResponse200MetadataSource(str, Enum):
    CURATED = "curated"
    DERIVED = "derived"

    def __str__(self) -> str:
        return str(self.value)
