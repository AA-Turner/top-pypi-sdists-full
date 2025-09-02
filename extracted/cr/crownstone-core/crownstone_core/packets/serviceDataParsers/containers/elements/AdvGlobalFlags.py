from crownstone_core.util.Conversion import Conversion
from crownstone_core.packets.serviceDataParsers.containers.elements.AdvTypes import AdvType

class AdvGlobalFlags:

    def __init__(self, byte):
        self.type = AdvType.MICROAPP_FLAGS

        bitmaskArray = Conversion.uint8_to_bit_array(byte)

        self.behaviourEnabled = bitmaskArray[0]

    def __str__(self):
        return \
           f"    behaviourEnabled: {self.behaviourEnabled}"