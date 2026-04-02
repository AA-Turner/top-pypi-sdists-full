from enum import Enum


class OpenStackInstanceAggregateGroupByEnum(str, Enum):
    AVAILABILITY_ZONE = "availability_zone"
    CUSTOMER = "customer"
    FLAVOR_NAME = "flavor_name"
    HYPERVISOR_HOSTNAME = "hypervisor_hostname"
    IMAGE_NAME = "image_name"
    RUNTIME_STATE = "runtime_state"
    SERVICE_SETTINGS = "service_settings"

    def __str__(self) -> str:
        return str(self.value)
