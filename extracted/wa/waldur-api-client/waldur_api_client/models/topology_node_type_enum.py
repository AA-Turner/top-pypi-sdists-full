from enum import Enum


class TopologyNodeTypeEnum(str, Enum):
    EXTERNAL_NETWORK = "external_network"
    FLOATING_IP = "floating_ip"
    INSTANCE = "instance"
    NETWORK = "network"
    PORT = "port"
    RBAC_SHARE = "rbac_share"
    ROUTER = "router"
    SUBNET = "subnet"
    TENANT = "tenant"

    def __str__(self) -> str:
        return str(self.value)
