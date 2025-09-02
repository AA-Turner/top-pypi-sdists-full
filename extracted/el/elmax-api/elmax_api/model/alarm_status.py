from enum import Enum


class AlarmArmStatus(Enum):
    ARMED_TOTALLY = 4
    ARMED_P1_P2 = 3
    ARMED_P2 = 2
    ARMED_P1 = 1
    NOT_ARMED = 0


class AlarmStatus(Enum):
    TRIGGERED = 3
    ARMED_STANDBY = 2
    NOT_ARMED_NOT_ARMABLE = 1
    NOT_ARMED_NOT_TRIGGERED = 0
