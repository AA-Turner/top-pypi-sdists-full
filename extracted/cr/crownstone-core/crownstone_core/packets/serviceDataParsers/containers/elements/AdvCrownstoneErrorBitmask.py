from crownstone_core.packets.serviceDataParsers.containers.elements.AdvTypes import AdvType
from crownstone_core.util.Conversion import Conversion


class AdvCrownstoneErrorBitmask:
    
    def __init__(self, bitMask):
        self.type = AdvType.CROWNSTONE_ERRORS

        self.bitMask = bitMask
    
        bitArray = Conversion.uint32_to_bit_array_reversed(bitMask)
    
        self.overCurrent        = bitArray[0]
        self.overCurrentDimmer  = bitArray[1]
        self.temperatureChip    = bitArray[2]
        self.temperatureDimmer  = bitArray[3]
        self.dimmerOnFailure    = bitArray[4]
        self.dimmerOffFailure   = bitArray[5]

    def __str__(self):
        return \
               f"    bitmask:           {self.bitMask}\n" \
               f"    overCurrent:       {self.overCurrent       }\n"\
               f"    overCurrentDimmer: {self.overCurrentDimmer }\n"\
               f"    temperatureChip:   {self.temperatureChip   }\n"\
               f"    temperatureDimmer: {self.temperatureDimmer }\n"\
               f"    dimmerOnFailure:   {self.dimmerOnFailure   }\n"\
               f"    dimmerOffFailure:  {self.dimmerOffFailure  }\n"