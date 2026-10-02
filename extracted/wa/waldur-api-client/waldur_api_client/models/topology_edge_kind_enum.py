from enum import Enum


class TopologyEdgeKindEnum(str, Enum):
    ATTACHED_TO = "attached_to"
    CONTAINS = "contains"
    FLOATING_FOR = "floating_for"
    GATEWAY = "gateway"
    HAS_INTERFACE = "has_interface"
    HAS_PORT = "has_port"
    HAS_SUBNET = "has_subnet"
    SHARED_WITH = "shared_with"

    def __str__(self) -> str:
        return str(self.value)
