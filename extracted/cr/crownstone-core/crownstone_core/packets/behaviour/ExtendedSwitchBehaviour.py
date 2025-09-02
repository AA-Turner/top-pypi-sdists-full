from crownstone_core.packets.behaviour.PresenceDescription import BehaviourPresenceType, BehaviourPresence
from crownstone_core.packets.behaviour.SwitchBehaviour import SwitchBehaviour


class ExtendedSwitchBehaviour(SwitchBehaviour):
    def __init__(self, *args):
        super().__init__(*args)
        self.endCondition = None

    def setNoEndCondition(self):
        self.endCondition = None
        return self

    def setEndConditionWhilePeopleInSphere(self):
        self.endCondition = BehaviourPresence().setSpherePresence(BehaviourPresenceType.someoneInSphere)
        return self

    def setEndConditionWhilePeopleInLocation(self, locationId):
        self.endCondition = BehaviourPresence().setLocationPresence(BehaviourPresenceType.somoneInLocation,
                                                                    [locationId])
        return self

    def serialize(self):
        arr = super().serialize()

        if self.endCondition is not None:
            arr += self.endCondition.serialize()
        else:
            anyPresence = BehaviourPresence()
            arr += anyPresence.serialize()

        return arr
