from crownstone_core.util.Conversion import Conversion
from crownstone_core.packets.serviceDataParsers.containers.elements.AdvTypes import AdvType


class AdvFlags:

    def __init__(self, byte):
        self.type = AdvType.CROWNSTONE_FLAGS

        bitmaskArray = Conversion.uint8_to_bit_array(byte)

        self.dimmerReady         = bitmaskArray[0]
        self.dimmingAllowed      = bitmaskArray[1]
        self.hasError            = bitmaskArray[2]
        self.switchLocked        = bitmaskArray[3]
        self.timeIsSet           = bitmaskArray[4]
        self.switchCraftEnabled  = bitmaskArray[5]
        self.tapToToggleEnabled  = bitmaskArray[6]
        self.behaviourOverridden = bitmaskArray[7]

    def __str__(self):
        return \
           f"    dimmerReady:         {self.dimmerReady        }\n" \
           f"    dimmingAllowed:      {self.dimmingAllowed     }\n" \
           f"    hasError:            {self.hasError           }\n" \
           f"    switchLocked:        {self.switchLocked       }\n" \
           f"    timeIsSet:           {self.timeIsSet          }\n" \
           f"    switchCraftEnabled:  {self.switchCraftEnabled }\n" \
           f"    tapToToggleEnabled:  {self.tapToToggleEnabled }\n" \
           f"    behaviourOverridden: {self.behaviourOverridden}"
