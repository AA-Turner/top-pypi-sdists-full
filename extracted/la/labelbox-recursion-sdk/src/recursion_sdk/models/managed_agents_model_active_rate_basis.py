from enum import StrEnum

class ManagedAgentsModelActiveRateBasis(StrEnum):
    OBSERVED = "observed"
    PRIOR = "prior"
    SCALED_LIST_PRICE = "scaled_list_price"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
