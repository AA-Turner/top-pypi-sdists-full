#
#  BluenetLib
#
#  Created by Alex de Mulder on 22/10/2019.
#  Copyright © 2019 Alex de Mulder. All rights reserved.
#
from crownstone_core.packets.behaviour.BehaviourBase import BehaviourBase
from crownstone_core.packets.behaviour.BehaviourTypes import BehaviourType


class TwilightBehaviour(BehaviourBase):
    """
    Implements packet generation for TwilightBehaviour
    """
    def __init__(self, profileIndex=None, behaviourType=BehaviourType.twilight, intensity=None, activeDays=None, time=None, idOnCrownstone=None):
        super().__init__(profileIndex, behaviourType, intensity, activeDays, time, None, None, idOnCrownstone)


