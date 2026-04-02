from enum import Enum


class OpenStackPortOEnum(str, Enum):
    ADMIN_STATE_UP = "admin_state_up"
    CREATED = "created"
    DEVICE_OWNER = "device_owner"
    INSTANCE_NAME = "instance_name"
    MAC_ADDRESS = "mac_address"
    NAME = "name"
    NETWORK_NAME = "network_name"
    STATUS = "status"
    SUBNET_NAME = "subnet_name"
    VALUE_0 = "-admin_state_up"
    VALUE_1 = "-created"
    VALUE_2 = "-device_owner"
    VALUE_3 = "-instance_name"
    VALUE_4 = "-mac_address"
    VALUE_5 = "-name"
    VALUE_6 = "-network_name"
    VALUE_7 = "-status"
    VALUE_8 = "-subnet_name"

    def __str__(self) -> str:
        return str(self.value)
