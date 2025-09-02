from crownstone_core.packets.assetFilter.FilterCommandPackets import *
from crownstone_core.protocol.BlePackets import ControlPacket, FactoryResetPacket
from crownstone_core.protocol.BluenetTypes import ControlType
from crownstone_core.util.BufferWriter import BufferWriter
from crownstone_core.util.Conversion import Conversion

"""
TODO: rename functions to getXxxArray or so, as they output a serialized array, not a typed packet.
"""

class ControlPacketsGenerator:

    @staticmethod
    def getFactoryResetPacket():
        return Conversion.uint32_to_uint8_array(0xdeadbeef)


    @staticmethod
    def getCommandFactoryResetPacket():
        return FactoryResetPacket().serialize()

    @staticmethod
    def getSwitchCommandPacket(switchVal: int):
        """
        :param switchVal: percentage [0..100] or special value (SwitchValSpecial).
        """
        return ControlPacket(ControlType.SWITCH).loadUInt8(switchVal).serialize()

    @staticmethod
    def getResetPacket():
        return ControlPacket(ControlType.RESET).serialize()

    @staticmethod
    def getPutInDFUPacket():
        return ControlPacket(ControlType.GOTO_DFU).serialize()

    @staticmethod
    def getDisconnectPacket():
        return ControlPacket(ControlType.DISCONNECT).serialize()

    @staticmethod
    def getRelaySwitchPacket(turnOn: bool):
        """
        :param turnOn: True to turn relay on.
        """
        switchVal = 0
        if turnOn:
            switchVal = 1

        return ControlPacket(ControlType.RELAY).loadUInt8(switchVal).serialize()

    @staticmethod
    def getDimmerSwitchPacket(intensity: int):
        """
        :param intensity: percentage [0..100]
        """
        return ControlPacket(ControlType.PWM).loadUInt8(intensity).serialize()


    @staticmethod
    def getResetErrorPacket(errorMask):
        return ControlPacket(ControlType.RESET_ERRORS).loadUInt32(errorMask).serialize()

    @staticmethod
    def getSetTimePacket(time):
        """
        This is a LOCAL timestamp since epoch in seconds

        so if you live in GMT + 1 add 3600 to the timestamp
        :param time:
        :return:
        """
        return ControlPacket(ControlType.SET_TIME).loadUInt32(time).serialize()

    @staticmethod
    def getAllowDimmingPacket(allow: bool):
        """

        :param allow: bool
        :return:
        """

        allowByte = 0
        if allow:
            allowByte = 1

        return ControlPacket(ControlType.ALLOW_DIMMING).loadUInt8(allowByte).serialize()

    @staticmethod
    def getLockSwitchPacket(lock: bool):
        """
        :param lock: bool
        :return:
        """

        lockByte = 0
        if lock:
            lockByte = 1

        return ControlPacket(ControlType.LOCK_SWITCH).loadUInt8(lockByte).serialize()

    @staticmethod
    def getSetupPacket(
        crownstoneId: int,
        sphereId: int,
        adminKey,
        memberKey,
        basicKey,
        serviceDataKey,
        localizationKey,
        meshDeviceKey,
        meshAppKey,
        meshNetworkKey,
        ibeaconUUID: str,
        ibeaconMajor: int,
        ibeaconMinor: int
    ):
        """
        :param crownstoneId:  		uint8 number
        :param sphereId:  	     	uint8 number
        :param adminKey:      		byteString (no conversion required)
        :param memberKey:     		byteString (no conversion required)
        :param basicKey:      		byteString (no conversion required)
        :param serviceDataKey: 	    byteString (no conversion required)
        :param localizationKey: 	byteString (no conversion required)
        :param meshDeviceKey: 	    byteString (no conversion required)
        :param meshAppKey: 	        byteString (no conversion required)
        :param meshNetworkKey: 	    byteString (no conversion required)
        :param ibeaconUUID: 		string  (ie. "1843423e-e175-4af0-a2e4-31e32f729a8a")
        :param ibeaconMajor:        uint16 number
        :param ibeaconMinor:        uint16 number
        :return:
        """
        data = []
        data.append(crownstoneId)
        data.append(sphereId)

        data += list(adminKey)
        data += list(memberKey)
        data += list(basicKey)
        data += list(serviceDataKey)
        data += list(localizationKey)

        MDKey = meshDeviceKey
        if type(meshDeviceKey) is str:
            MDKey = Conversion.ascii_or_hex_string_to_16_byte_array(meshDeviceKey)

        data += list(MDKey)
        data += list(meshAppKey)
        data += list(meshNetworkKey)

        data += Conversion.ibeaconUUIDString_to_reversed_uint8_array(ibeaconUUID)
        data += Conversion.uint16_to_uint8_array(ibeaconMajor)
        data += Conversion.uint16_to_uint8_array(ibeaconMinor)

        return ControlPacket(ControlType.SETUP).loadByteArray(data).serialize()


    @staticmethod
    def getIBeaconConfigIdPacket(id, timestamp, interval):
        data = []
        data.append(id)
        data += Conversion.uint32_to_uint8_array(timestamp)
        data += Conversion.uint16_to_uint8_array(interval)

        return ControlPacket(ControlType.SET_IBEACON_CONFIG_ID).loadByteArray(data).serialize()

    @staticmethod
    def getPowerSamplesRequestPacket(samplesType, index):
        buffer = BufferWriter()
        buffer.putUInt8(samplesType)
        buffer.putUInt8(index)
        data = buffer.getBuffer()
        return ControlPacket(ControlType.GET_POWER_SAMPLES).loadByteArray(data).serialize()


    @staticmethod
    def getRemoveFilterPacket(filterId: int) -> [int]:
        removecommand = RemoveFilterPacket(filterId)
        return ControlPacket(ControlType.ASSET_FILTER_REMOVE).loadByteArray(removecommand.serialize()).serialize()


    @staticmethod
    def getGetFilterSummariesPacket() -> [int]:
        return ControlPacket(ControlType.ASSET_FILTER_GET_SUMMARIES).serialize()

    @staticmethod
    def getCommitFilterChangesPacket(masterVersion: int, masterCrc: int) -> [int]:
        commitcommand = CommitFilterChangesPacket(masterVersion, masterCrc)
        return ControlPacket(ControlType.ASSET_FILTER_COMMIT_CHANGES).loadByteArray(commitcommand.serialize()).serialize()

    @staticmethod
    def getUploadFilterPacket(chunk: [int]) -> [int]:
        """
        TODO: type chunk param
        """
        return ControlPacket(ControlType.ASSET_FILTER_UPLOAD).loadByteArray(chunk).serialize()