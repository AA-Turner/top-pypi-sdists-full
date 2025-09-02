from enum import IntEnum

DAY_START_TIME_SECONDS_SINCE_MIDNIGHT = 4*3600

class BehaviourType(IntEnum):
    behaviour  = 0
    twilight   = 1
    smartTimer = 2

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

