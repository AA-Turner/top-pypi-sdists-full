from enum import IntEnum

from crownstone_core.util.Conversion import Conversion
from crownstone_core.util.BufferReader import BufferReader


class BehaviourTimeType(IntEnum):
    afterMidnight = 0
    afterSunrise  = 1
    afterSunset   = 2

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)




class BehaviourTimeContainer:
    def __init__(self, fromTime, untilTime):
        self.fromTime  = fromTime
        self.untilTime = untilTime

class BehaviourTime:

    def __init__(self):
        self.timeType = None
        self.offset = 0
        self.valid = True

    def fromTime(self, hours, minutes):
        self.timeType = BehaviourTimeType.afterMidnight
        self.offset = 3600 * hours + 60 * minutes
        return self

    def fromType(self, timeType, offsetSeconds=0):
        self.timeType = timeType
        self.offset = offsetSeconds
        return self

    def fromData(self, data):
        if len(data) != 5:
            self.valid = False
            return self

        payload = BufferReader(data)

        firstByte = payload.getUInt8()
        if not BehaviourTimeType.has_value(firstByte):
            self.valid = False
            return self

        self.timeType = BehaviourTimeType(firstByte)
        self.offset = payload.getInt32()
        self.valid = True

        return self

    def serialize(self):
        arr = []

        arr.append(self.timeType.value)
        arr += Conversion.int32_to_uint8_array(self.offset)

        return arr

    def getDictionary(self):
        returnDict = {}

        if self.timeType == BehaviourTimeType.afterSunset:
            returnDict["type"] = "SUNSET"
            returnDict["offsetMinutes"] = self.offset / 60
        elif self.timeType == BehaviourTimeType.afterSunrise:
            returnDict["type"] = "SUNRISE"
            returnDict["offsetMinutes"] = self.offset / 60
        else:
            returnDict["type"] = "CLOCK"
            returnDict["data"] = {"hours": (self.offset - self.offset % 3600) / 3600,
                                  "minutes": (self.offset % 3600) / 60}

        return returnDict

