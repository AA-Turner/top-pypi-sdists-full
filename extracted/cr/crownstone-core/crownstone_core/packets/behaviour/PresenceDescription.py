from enum import IntEnum

from crownstone_core.util.Conversion import Conversion
from crownstone_core.util.BufferReader import BufferReader

DEFAULT_PRESENCE_DELAY = 300 # seconds = 5 minutes

class BehaviourPresenceType(IntEnum):
    ignorePresence   = 0
    somoneInLocation = 1
    nobodyInLocation = 2
    someoneInSphere  = 3
    nobodyInSphere   = 4

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class BehaviourPresence:

    def __init__(self):
        self.presenceType = BehaviourPresenceType.ignorePresence
        self.locationIds = []
        self.delayInSeconds = 0
        self.valid = True

    def setSpherePresence(self, presenceType, delayInSeconds=DEFAULT_PRESENCE_DELAY):
        self.presenceType = presenceType
        self.delayInSeconds = delayInSeconds
        return self

    def setLocationPresence(self, presenceType, locationIds, delayInSeconds=DEFAULT_PRESENCE_DELAY):
        self.presenceType = presenceType
        self.locationIds = locationIds
        self.delayInSeconds = delayInSeconds
        return self

    def fromData(self, data):
        if len(data) != 13:
            self.valid = False
            return self

        payload = BufferReader(data)
        firstByte = payload.getUInt8()
        if not BehaviourPresenceType.has_value(firstByte):
            self.valid = False
            return self

        self.behaviourType = BehaviourPresenceType(firstByte)
        self.locationIds = self.unpackMask(payload.getUInt64())
        self.delayInSeconds = payload.getUInt32()

        return self

    def getMask(self, locationIds):
        result = 0
        bit = 1
        for locationId in locationIds:
            if locationId < 64:
                result = result | bit << locationId

        return result

    def unpackMask(self, mask):
        result = []
        bit = 1
        for i in range(0, 64):
            if (mask >> i & bit) == 1:
                result.append(i)

        return result

    def serialize(self):
        arr = []

        arr.append(self.presenceType.value)
        arr += Conversion.uint64_to_uint8_array(self.getMask(self.locationIds))
        arr += Conversion.uint32_to_uint8_array(self.delayInSeconds)

        return arr

    def getDictionary(self):
        returnDict = {}

        if self.presenceType == BehaviourPresenceType.ignorePresence:
            returnDict["type"] = "IGNORE"

        elif self.presenceType == BehaviourPresenceType.somoneInLocation:
            returnDict["type"] = "SOMEBODY"
            returnDict["data"] = {"type": "LOCATION", "locationIds": self.locationIds}

        elif self.presenceType == BehaviourPresenceType.someoneInSphere:
            returnDict["type"] = "SOMEBODY"
            returnDict["data"] = {"type": "SPHERE"}

        elif self.presenceType == BehaviourPresenceType.nobodyInLocation:
            returnDict["type"] = "NOBODY"
            returnDict["data"] = {"type": "LOCATION", "locationIds": self.locationIds}

        elif self.presenceType == BehaviourPresenceType.nobodyInSphere:
            returnDict["type"] = "NOBODY"
            returnDict["data"] = {"type": "SPHERE"}

        if self.presenceType != BehaviourPresenceType.ignorePresence:
            returnDict["delay"] = self.delayInSeconds

        return returnDict

