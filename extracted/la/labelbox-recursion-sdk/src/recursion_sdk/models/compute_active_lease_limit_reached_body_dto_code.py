from enum import StrEnum

class ComputeActiveLeaseLimitReachedBodyDtoCode(StrEnum):
    COMPUTE_ACTIVE_LEASE_LIMIT_REACHED = "compute_active_lease_limit_reached"

    def __str__(self) -> str:
        return str(self.value)
