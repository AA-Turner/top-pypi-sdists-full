import logging

from crownstone_core import Conversion
from crownstone_core.protocol.ControlPackets import ControlPacketsGenerator

from crownstone_uart.core.modules.ControlHandler import ControlHandler

_LOGGER = logging.getLogger(__name__)

class SetupHandler:
    def __init__(self, control: ControlHandler):
        self.control = control
        pass

    async def setup(self,
                    sphereId: int,
                    crownstoneId: int,
                    meshDeviceKey: bytearray or list,
                    ibeaconUUID: str,
                    ibeaconMajor: int,
                    ibeaconMinor: int,
                    keysDict: dict):
        """
        Perform the setup of the Crownstone we are connected to via UART.
        
        :param sphereId:      An ID (0-255) that is the same for each Crownstone within the sphere.
        :param crownstoneId:  An ID (1-255) that is unique within the sphere.
        :param meshDeviceKey: A 16 byte key that is different for each Crownstone.
        :param ibeaconUUID:   The iBeacon UUID. Should be the same for each Crownstone in the sphere.
                              Provided as string, like: "1843423e-e175-4af0-a2e4-31e32f729a8a".
        :param ibeaconMajor:  The iBeacon major. Together with the minor, should be unique per sphere.
        :param ibeaconMinor:  The iBeacon minor. Together with the major, should be unique per sphere.
        :param keysDict:      Dictionary with the sphere keys.
        """
        controlPacket = ControlPacketsGenerator.getSetupPacket(
            crownstoneId,
            sphereId,
            Conversion.ascii_or_hex_string_to_16_byte_array(keysDict["admin"]),
            Conversion.ascii_or_hex_string_to_16_byte_array(keysDict["member"]),
            Conversion.ascii_or_hex_string_to_16_byte_array(keysDict["basic"]),
            Conversion.ascii_or_hex_string_to_16_byte_array(keysDict["serviceDataKey"]),
            Conversion.ascii_or_hex_string_to_16_byte_array(keysDict["localizationKey"]),
            meshDeviceKey,
            Conversion.ascii_or_hex_string_to_16_byte_array(keysDict["meshApplicationKey"]),
            Conversion.ascii_or_hex_string_to_16_byte_array(keysDict["meshNetworkKey"]),
            ibeaconUUID,
            ibeaconMajor,
            ibeaconMinor
        )
        await self.control._writeControlAndWaitForSuccess(controlPacket)
