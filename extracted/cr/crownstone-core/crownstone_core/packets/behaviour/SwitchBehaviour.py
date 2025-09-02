from crownstone_core.packets.behaviour.BehaviourBase import BehaviourBase
from crownstone_core.packets.behaviour.BehaviourTypes import BehaviourType
from crownstone_core.packets.behaviour.PresenceDescription import BehaviourPresence, BehaviourPresenceType, \
    DEFAULT_PRESENCE_DELAY

DEFAULT_PRESENCE = BehaviourPresence().setSpherePresence(BehaviourPresenceType.someoneInSphere)


class SwitchBehaviour(BehaviourBase):
    """
    Implements packet generation for SwitchBehaviours
    """

    def __init__(self, profileIndex=0, behaviourType=BehaviourType.behaviour, intensity=None, activeDays=None,
                 time=None, presence=None, endCondition=None, idOnCrownstone=None):
        super().__init__(profileIndex, behaviourType, intensity, activeDays, time, presence, endCondition,
                         idOnCrownstone)

    def ignorePresence(self):
        self.presence = None
        return self

    def setPresenceIgnore(self):
        return self.ignorePresence()

    def setPresenceSomebody(self):
        self.setPresenceSomebodyInSphere()
        return self

    def setPresenceNobody(self):
        self.setPresenceNobodyInSphere()
        return self

    def setPresenceSomebodyInSphere(self):
        self.presence = BehaviourPresence().setSpherePresence(BehaviourPresenceType.someoneInSphere)
        return self

    def setPresenceNobodyInSphere(self):
        self.presence = BehaviourPresence().setSpherePresence(BehaviourPresenceType.nobodyInSphere)
        return self

    def setPresenceInSphere(self):
        self.setPresenceSomebodyInSphere()
        return self

    def setPresenceInLocations(self, locationIds):
        self.setPresenceSomebodyInLocations(locationIds)
        return self

    def setPresenceSomebodyInLocations(self, locationIds, delay=DEFAULT_PRESENCE_DELAY):
        self.presence = BehaviourPresence().setLocationPresence(BehaviourPresenceType.somoneInLocation, locationIds,
                                                                delay)
        return self

    def setPresenceNobodyInLocations(self, locationIds, delay=DEFAULT_PRESENCE_DELAY):
        self.presence = BehaviourPresence().setLocationPresence(BehaviourPresenceType.nobodyInLocation, locationIds,
                                                                delay)
        return self

    def serialize(self):
        arr = super().serialize()

        if self.presence is not None:
            arr += self.presence.serialize()
        else:
            anypresence = BehaviourPresence()
            arr += anypresence.serialize()

        return arr

