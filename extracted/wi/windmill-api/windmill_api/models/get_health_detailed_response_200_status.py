from enum import Enum


class GetHealthDetailedResponse200Status(str, Enum):
    DEGRADED = "degraded"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"

    def __str__(self) -> str:
        return str(self.value)
