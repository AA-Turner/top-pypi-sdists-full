from enum import Enum


class DeviceCodeEnum(str, Enum):
    DOOR_IN = "door_in"
    DOOR_OUT = "door_out"
    REPAIR_IN = "repair_in"
    REPAIR_OUT = "repair_out"
    DETAIL_IN = "detail_in"
    DETAIL_OUT = "detail_out"
