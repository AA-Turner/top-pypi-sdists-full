import json

from crownstone_core.packets.behaviour.ActiveDays import ActiveDays
from crownstone_core.packets.behaviour.BehaviourTypes import BehaviourType, DAY_START_TIME_SECONDS_SINCE_MIDNIGHT
from crownstone_core.packets.behaviour.PresenceDescription import BehaviourPresence
from crownstone_core.packets.behaviour.TimeDescription import BehaviourTimeContainer, BehaviourTime, BehaviourTimeType
from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.util.Fletcher import fletcher32_uint8Arr


def DEFAULT_ACTIVE_DAYS():
    return ActiveDays()


def DEFAULT_TIME():
    return BehaviourTimeContainer(
        BehaviourTime().fromType(BehaviourTimeType.afterSunset),
        BehaviourTime().fromType(BehaviourTimeType.afterSunrise),
    )



class BehaviourBase:

    def __init__(self, profileIndex=None, behaviourType=BehaviourType.behaviour, intensity=None, activeDays=None, time=None, presence=None, endCondition=None, idOnCrownstone=None):
        self.profileIndex = 0 if profileIndex is None else profileIndex
        self.behaviourType = behaviourType
        self.intensity = 100 if intensity is None else max(0, min(100, intensity))
        self.activeDays = DEFAULT_ACTIVE_DAYS() if activeDays is None else activeDays
        self.fromTime = DEFAULT_TIME().fromTime if time is None else time.fromTime
        self.untilTime = DEFAULT_TIME().untilTime if time is None else time.untilTime
        self.presence = presence
        self.endCondition = endCondition
        self.idOnCrownstone = idOnCrownstone

        self.valid = True


    def setDimPercentage(self, value):
        self.intensity = value
        return self

    def setTimeAllday(self, dayStartTimeSecondsSinceMidnight=DAY_START_TIME_SECONDS_SINCE_MIDNIGHT):
        self.fromTime  = BehaviourTime().fromType(BehaviourTimeType.afterMidnight,  dayStartTimeSecondsSinceMidnight)
        self.untilTime = BehaviourTime().fromType(BehaviourTimeType.afterMidnight, dayStartTimeSecondsSinceMidnight)
        return self
    
    def setTimeWhenDark(self):
        self.fromTime  = BehaviourTime().fromType(BehaviourTimeType.afterSunset)
        self.untilTime = BehaviourTime().fromType(BehaviourTimeType.afterSunrise)
        return self
    
    def setTimeWhenSunUp(self):
        self.fromTime  = BehaviourTime().fromType(BehaviourTimeType.afterSunrise)
        self.untilTime = BehaviourTime().fromType(BehaviourTimeType.afterSunset)
        return self
    
    def setTimeFromSunrise(self, offsetMinutes = 0):
        self.fromTime = BehaviourTime().fromType(BehaviourTimeType.afterSunrise, offsetSeconds=60*offsetMinutes)
        return self
    
    def setTimeFromSunset(self, offsetMinutes = 0):
        self.fromTime  = BehaviourTime().fromType(BehaviourTimeType.afterSunset, offsetSeconds=60*offsetMinutes)
        return self
    
    def setTimeToSunrise(self, offsetMinutes = 0):
        self.untilTime = BehaviourTime().fromType(BehaviourTimeType.afterSunrise, offsetSeconds=60*offsetMinutes)
        return self
    
    
    def setTimeToSunset(self, offsetMinutes = 0):
        self.untilTime = BehaviourTime().fromType(BehaviourTimeType.afterSunset, offsetSeconds=60 * offsetMinutes)
        return self
    
    def setTimeFrom(self, hours, minutes): 
        self.fromTime  = BehaviourTime().fromTime(hours, minutes)
        return self
    
    
    def setTimeTo(self, hours, minutes):
        self.untilTime  = BehaviourTime().fromTime(hours, minutes)
        return self
        

    """
    The payload is made up from
     - BehaviourType  1B
     - Intensity      1B
     - profileIndex   1B
     - ActiveDays     1B
     - From           5B
     - Until          5B

     - Presence       13B --> for Switch Behaviour and Smart Timer
     - End Condition  17B --> for Smart Timer
     """

    def fromData(self, data):
        payload = BufferReader(data)

        firstByte = payload.getUInt8()
        if not BehaviourType.has_value(firstByte):
            self.valid = False
            return self

        self.behaviourType = BehaviourType(firstByte)
        self.intensity = payload.getUInt8()
        self.profileIndex = payload.getUInt8()
        self.activeDays   = ActiveDays().fromData(payload.getUInt8())
        self.fromTime     = BehaviourTime().fromData(payload.getBytes(5))  # 4 5 6 7 8
        self.untilTime    = BehaviourTime().fromData(payload.getBytes(5))  # 9 10 11 12 13

        if self.fromTime.valid == False or self.untilTime.valid == False:
            self.valid = False
            return self

        if self.behaviourType == BehaviourType.behaviour:
            if payload.length >= 14 + 13:
                self.presence = BehaviourPresence().fromData(
                    payload.getBytes(13))  # 14 15 16 17 18 19 20 21 22 23 24 25 26
                if not self.presence.valid:
                    self.valid = False
                    return self
            else:
                self.valid = False
                return self

        if self.behaviourType == BehaviourType.smartTimer:
            if payload.length >= 14 + 13 + 17:
                presence = BehaviourPresence().fromData(payload.getBytes(17))
                if not presence.valid:
                    self.valid = False
                    return self

                self.endCondition = presence

            else:
                self.valid = False
                return self


    def serialize(self):
        arr = []

        arr.append(self.behaviourType.value)
        arr.append(self.intensity)
        arr.append(self.profileIndex)

        arr.append(self.activeDays.getMask())

        arr += self.fromTime.serialize()
        arr += self.untilTime.serialize()

        return arr


    def getHash(self):
        return fletcher32_uint8Arr(self._getPaddedPacket())

    def getDictionary(self, dayStartTimeSecondsSinceMidnight=DAY_START_TIME_SECONDS_SINCE_MIDNIGHT):
        typeString = "BEHAVIOUR"
        if self.behaviourType == BehaviourType.twilight:
            typeString = "TWILIGHT"

        dataDictionary = {}
        if self.behaviourType == BehaviourType.twilight:
            dataDictionary["action"] = {"type": "DIM_WHEN_TURNED_ON", "data": self.intensity}
            dataDictionary["time"] = self._getTimeDictionary(dayStartTimeSecondsSinceMidnight)

        else:
            # behaviour and smart timer have the same format
            dataDictionary["action"] = {"type": "BE_ON", "data": self.intensity}
            dataDictionary["time"] = self._getTimeDictionary(dayStartTimeSecondsSinceMidnight)

            if self.presence is not None:
                dataDictionary["presence"] = self.presence.getDictionary()

            if self.endCondition is not None:
                endConditionDictionary = {}
                endConditionDictionary["type"] = "PRESENCE_AFTER"
                endConditionDictionary["presence"] = self.endCondition.getDictionary()

                dataDictionary["endCondition"] = endConditionDictionary

        returnDict = {"type": typeString, "data": dataDictionary, "activeDays": self.activeDays.getDictionary(),
                      "idOnCrownstone": self.idOnCrownstone, "profileIndex": self.profileIndex}

        return returnDict

    def _getTimeDictionary(self, dayStartTimeSecondsSinceMidnight=DAY_START_TIME_SECONDS_SINCE_MIDNIGHT):
        returnDict = {}

        # check if always
        if self.fromTime.timeType == BehaviourTimeType.afterMidnight and self.fromTime.offset == dayStartTimeSecondsSinceMidnight and self.untilTime.timeType == BehaviourTimeType.afterMidnight and self.untilTime.offset == dayStartTimeSecondsSinceMidnight:
            returnDict["type"] = "ALL_DAY"
            return returnDict

        # its not always! construct the from and to parts.
        returnDict["type"] = "RANGE"
        returnDict["from"] = self.fromTime.getDictionary()
        returnDict["to"] = self.untilTime.getDictionary()

        return returnDict

    def _getPaddedPacket(self):
        packet = self.serialize()
        if len(packet) % 2 != 0:
            packet.append(0)

        return packet


    def __str__(self):
        return json.dumps(self.getDictionary())