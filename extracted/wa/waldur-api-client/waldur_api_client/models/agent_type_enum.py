from enum import Enum


class AgentTypeEnum(str, Enum):
    EVENT_PROCESSING = "Event processing"
    GLAUTH_SYNC = "Glauth sync"
    ORDER_PROCESSING = "Order processing"
    RESOURCE_SYNC = "Resource sync"
    UNKNOWN = "unknown"
    USAGE_REPORTING = "Usage reporting"

    def __str__(self) -> str:
        return str(self.value)
