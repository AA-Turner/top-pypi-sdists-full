
"""
 We will assume that there is a dictionary format which is used to provide the system with the behaviour data. We will raise an error on incorrect format. Otherwise we will parse it and return the Behaviour object.
 Expected format:
 {
    type: "BEHAVIOUR" | "TWILIGHT",
    data: {
        action: { data: number },
        time: TIME_PARSER_INPUT,
        presence: PRESENCE_PARSER_INPUT
        endCondition: ENDCONDITION_PARSER_INPUT
    },
    activeDays: {
      Mon: boolean,
      Tue: boolean,
      Wed: boolean,
      Thu: boolean,
      Fri: boolean,
      Sat: boolean,
      Sun: boolean
    },
    idOnCrownstone: number,
    profileIndex: number
 }
 """
import json

from crownstone_core.Exceptions import CrownstoneError, CrownstoneException
from crownstone_core.packets.behaviour.ActiveDays import ActiveDays
from crownstone_core.packets.behaviour.BehaviourBase import BehaviourBase
from crownstone_core.packets.behaviour.BehaviourTypes import BehaviourType, DAY_START_TIME_SECONDS_SINCE_MIDNIGHT
from crownstone_core.packets.behaviour.PresenceDescription import BehaviourPresenceType, BehaviourPresence
from crownstone_core.packets.behaviour.TimeDescription import BehaviourTimeContainer, BehaviourTime, BehaviourTimeType


def getFromDict(dict, key):
    val = None
    if key in dict: val = dict[key]
    return val

def BehaviourDictionaryParser(dict, dayStartTimeSecondsSinceMidnight = DAY_START_TIME_SECONDS_SINCE_MIDNIGHT):
    # optional variables
    profileIndex   = getFromDict(dict, "profileIndex")
    typeString     = getFromDict(dict, "type")
    data           = getFromDict(dict, "data")
    activeDays     = getFromDict(dict, "activeDays")
    idOnCrownstone = getFromDict(dict, "idOnCrownstone")
    
    if profileIndex  is None: raise CrownstoneException(CrownstoneError.PROFILE_INDEX_MISSING)
    if typeString    is None: raise CrownstoneException(CrownstoneError.TYPE_MISSING)
    if data          is None: raise CrownstoneException(CrownstoneError.DATA_MISSING)
    if activeDays    is None: raise CrownstoneException(CrownstoneError.ACTIVE_DAYS_MISSING)
    
    behaviourType = BehaviourType.behaviour
    if   typeString == "BEHAVIOUR": behaviourType = BehaviourType.behaviour
    elif typeString == "TWILIGHT":  behaviourType = BehaviourType.twilight

    if type(data) == str:
        data = json.loads(data)

    # optional variables
    actionDict   = getFromDict(data, "action")
    timeDict     = getFromDict(data, "time")
    presence     = getFromDict(data, "presence")
    endCondition = getFromDict(data, "endCondition")

    if actionDict is None: raise CrownstoneException(CrownstoneError.BEHAVIOUR_ACTION_MISSING)
    if timeDict   is None: raise CrownstoneException(CrownstoneError.BEHAVIOUR_TIME_MISSING)

  
    intensity = getFromDict(actionDict, "data")
    
    if intensity is None: raise CrownstoneException(CrownstoneError.BEHAVIOUR_INTENSITY_MISSING)
    
    activeDayObject = ActiveDayParser(activeDays)
    timeObject      = TimeParser(timeDict, dayStartTimeSecondsSinceMidnight)
    
    behaviour = BehaviourBase(
        profileIndex  = profileIndex,
        behaviourType = behaviourType,
        intensity     = intensity,
        activeDays    = activeDayObject,
        time          = timeObject
    )
    
    if idOnCrownstone is not None:
        behaviour.idOnCrownstone = idOnCrownstone
        
    if presence is not None:
        if behaviourType == BehaviourType.twilight:
            raise CrownstoneException(CrownstoneError.TWILIGHT_CANT_HAVE_PRESENCE)
        
        presenceObject = PresenceParser(presence)
        behaviour.presence = presenceObject
    
    
    if endCondition is not None:
        if behaviourType == BehaviourType.twilight:
            raise CrownstoneException(CrownstoneError.TWILIGHT_CANT_HAVE_END_CONDITION)
        
        endConditionObject = EndConditionParser(endCondition)
        behaviour.endCondition = endConditionObject
        behaviour.type = BehaviourType.smartTimer
    
    
    return behaviour


"""
 There are a few possible formats. We will parse and validate
"""
def ActiveDayParser(dict):
    Monday    = getFromDict(dict, "Mon")
    Tuesday   = getFromDict(dict, "Tue")
    Wednesday = getFromDict(dict, "Wed")
    Thursday  = getFromDict(dict, "Thu")
    Friday    = getFromDict(dict, "Fri")
    Saturday  = getFromDict(dict, "Sat")
    Sunday    = getFromDict(dict, "Sun")
    
    activeDays = ActiveDays()
    
    if Monday is not None and Tuesday is not None and Wednesday is not None and Thursday is not None and Friday is not None and Saturday is not None and Sunday is not None:
        activeDays.Monday    = Monday
        activeDays.Tuesday   = Tuesday
        activeDays.Wednesday = Wednesday
        activeDays.Thursday  = Thursday
        activeDays.Friday    = Friday
        activeDays.Saturday  = Saturday
        activeDays.Sunday    = Sunday
        
        if activeDays.getMask() == 0:
            raise CrownstoneException(CrownstoneError.NO_ACTIVE_DAYS)
        
        return activeDays
    else:
        raise CrownstoneException(CrownstoneError.ACTIVE_DAYS_INVALID)
    


"""
 There are a few possible formats. We will parse and validate
"""
def TimeParser(dict, dayStartTimeSecondsSinceMidnight):
    type = getFromDict(dict, "type")

    if type is None: raise CrownstoneException(CrownstoneError.NO_TIME_TYPE)

    if type == "ALL_DAY":
        return BehaviourTimeContainer(
            BehaviourTime().fromType(BehaviourTimeType.afterMidnight, dayStartTimeSecondsSinceMidnight),
            BehaviourTime().fromType(BehaviourTimeType.afterMidnight, dayStartTimeSecondsSinceMidnight)
        )
    
    elif type == "RANGE":
        fromTime = getFromDict(dict, "from")
        toTime   = getFromDict(dict, "to")

        if fromTime is None: raise CrownstoneException(CrownstoneError.MISSING_FROM_TIME)
        if toTime   is None: raise CrownstoneException(CrownstoneError.MISSING_TO_TIME)

        fromTimeType = getFromDict(fromTime, "type")
        toTimeType   = getFromDict(toTime,   "type")

        if fromTimeType is None: raise CrownstoneException(CrownstoneError.MISSING_FROM_TIME_TYPE)
        if toTimeType   is None: raise CrownstoneException(CrownstoneError.MISSING_TO_TIME_TYPE)

        fromResult = None
        toResult   = None
        
        if fromTimeType == "CLOCK":
            fromData = getFromDict(fromTime, "data")
        
            if fromData is None: raise CrownstoneException(CrownstoneError.MISSING_FROM_TIME_DATA)

            hours   = getFromDict(fromData, "hours")
            minutes = getFromDict(fromData, "minutes")

            if hours   is None: raise CrownstoneException(CrownstoneError.MISSING_FROM_TIME_DATA)
            if minutes is None: raise CrownstoneException(CrownstoneError.MISSING_FROM_TIME_DATA)

            fromResult = BehaviourTime().fromTime(hours, minutes)

        elif fromTimeType == "SUNSET":
            offsetSeconds = 0
            offsetMinutes = getFromDict(fromTime, "offsetMinutes")
            if offsetMinutes is not None:
                offsetSeconds = 60*offsetMinutes

            fromResult = BehaviourTime().fromType(BehaviourTimeType.afterSunset, offsetSeconds)
        
        elif fromTimeType == "SUNRISE":
            offsetSeconds = 0
            offsetMinutes = getFromDict(fromTime, "offsetMinutes")
            if offsetMinutes is not None:
                offsetSeconds = 60 * offsetMinutes
            
            fromResult = BehaviourTime().fromType(BehaviourTimeType.afterSunrise, offsetSeconds)
        
        else:
            raise CrownstoneException(CrownstoneError.INVALID_TIME_FROM_TYPE)
        
        
        
        if toTimeType == "CLOCK":
            toData = getFromDict(toTime, "data")

            if toData is None: raise CrownstoneException(CrownstoneError.MISSING_TO_TIME_DATA)

            hours = getFromDict(toData, "hours")
            minutes = getFromDict(toData, "minutes")

            if hours is None: raise CrownstoneException(CrownstoneError.INVALID_TO_DATA)
            if minutes is None: raise CrownstoneException(CrownstoneError.INVALID_TO_DATA)

            toResult = BehaviourTime().fromTime(hours, minutes)

        elif toTimeType == "SUNSET":
            offsetSeconds = 0
            offsetMinutes = getFromDict(toTime, "offsetMinutes")
            if offsetMinutes is not None:
                offsetSeconds = 60 * offsetMinutes

            toResult = BehaviourTime().fromType(BehaviourTimeType.afterSunset, offsetSeconds)

        elif toTimeType == "SUNRISE":
            offsetSeconds = 0
            offsetMinutes = getFromDict(toTime, "offsetMinutes")
            if offsetMinutes is not None:
                offsetSeconds = 60 * offsetMinutes

            toResult = BehaviourTime().fromType(BehaviourTimeType.afterSunrise, offsetSeconds)
        
        else:
            raise CrownstoneException(CrownstoneError.INVALID_TIME_TO_TYPE)
        
        return BehaviourTimeContainer(fromResult, toResult)
    else:
        raise CrownstoneException(CrownstoneError.INVALID_TIME_TYPE)
    
    


"""
 There are a few possible formats. We will parse and validate
"""
def PresenceParser(dict):
    type = getFromDict(dict, "type")
    if type is None: raise CrownstoneException(CrownstoneError.NO_PRESENCE_TYPE)

    if type == "IGNORE":
        return BehaviourPresence()
    elif type == "SOMEBODY" or type == "NOBODY":
        data = getFromDict(dict, "data")
        if data is None: raise CrownstoneException(CrownstoneError.NO_PRESENCE_DATA)

        delay = getFromDict(dict, "delay")
        if delay is None: raise CrownstoneException(CrownstoneError.NO_PRESENCE_DELAY)

        dataType = getFromDict(data, "type")
        if dataType is None: raise CrownstoneException(CrownstoneError.NO_PRESENCE_TYPE)

        if dataType == "SPHERE":
            if type == "SOMEBODY":
                return BehaviourPresence().setSpherePresence(BehaviourPresenceType.someoneInSphere, delayInSeconds = delay)
            else:
                return BehaviourPresence().setSpherePresence(BehaviourPresenceType.nobodyInSphere, delayInSeconds = delay)

        elif dataType == "LOCATION":
            locationIdArray = getFromDict(data, "locationIds")
            if locationIdArray is None: raise CrownstoneException(CrownstoneError.NO_PRESENCE_LOCATION_IDS)

            if type == "SOMEBODY":
                return BehaviourPresence().setLocationPresence(BehaviourPresenceType.somoneInLocation, locationIds=locationIdArray, delayInSeconds=delay)
            
            else:
                return BehaviourPresence().setLocationPresence(BehaviourPresenceType.nobodyInLocation, locationIds=locationIdArray, delayInSeconds=delay)
        else:
            raise CrownstoneException(CrownstoneError.NO_PRESENCE_DATA)
    else:
        raise CrownstoneException(CrownstoneError.INVALID_PRESENCE_TYPE)
    
    
    


"""
 There are a few possible formats. We will parse and validate
"""
def EndConditionParser(dict):
    type     = getFromDict(dict, "type")
    presence = getFromDict(dict, "presence")
    if type     is None: raise CrownstoneException(CrownstoneError.NO_END_CONDITION_TYPE)
    if presence is None: raise CrownstoneException(CrownstoneError.NO_END_CONDITION_PRESENCE)

    presenceObject = PresenceParser(presence)
    
    return presenceObject

