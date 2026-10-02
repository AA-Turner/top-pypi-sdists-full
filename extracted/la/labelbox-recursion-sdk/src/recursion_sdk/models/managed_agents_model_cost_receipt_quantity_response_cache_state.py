from enum import StrEnum

class ManagedAgentsModelCostReceiptQuantityResponseCacheState(StrEnum):
    NONE = "none"
    READ = "read"
    WRITE_1H = "write_1h"
    WRITE_5M = "write_5m"

    def __str__(self) -> str:
        return str(self.value)
