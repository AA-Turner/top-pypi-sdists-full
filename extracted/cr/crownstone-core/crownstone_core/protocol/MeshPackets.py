

from enum import IntEnum
from typing import List


# broadcast to all:
# value: 1
#
# broadcast to all, but retry until ID's in list have acked or timeout
# value: 3
#
# 1:1 message to N crownstones with acks (only N = 1 supported for now)
# value: 2
from crownstone_core.util.BufferWriter import BufferWriter


class MeshModes(IntEnum):
    BROADCAST           = 1
    SINGLE_TARGET_ACKED = 2
    BROADCAST_ACKED_IDS = 3


class _MeshCommandPacket:

    def __init__(self, crownstoneIds : List[int], payload, mesh_command_mode: MeshModes, timeout_or_transmissions):
        self.type = 0 # reserved
        self.crownstoneIds = crownstoneIds
        self.payload = payload
        self.flags = mesh_command_mode.value
        self.timeout_or_transmissions = timeout_or_transmissions

    def serialize(self):
        writer = BufferWriter()
        writer.putUInt8(self.type)
        writer.putUInt8(self.flags)
        writer.putUInt8(self.timeout_or_transmissions)
        writer.putUInt8(len(self.crownstoneIds))
        for stoneId in self.crownstoneIds:
            writer.putUInt8(stoneId)
        writer.putBytes(self.payload)
        return writer.getBuffer()

class MeshBroadcastPacket(_MeshCommandPacket):

    def __init__(self, payload, number_of_transmissions : int = 0):
        """
            number_of_transmissions 0 uses the default number_of_transmissions which is 3
        """
        super().__init__([], payload, MeshModes.BROADCAST, number_of_transmissions)

class MeshSetStatePacket(_MeshCommandPacket):

    def __init__(self, crownstoneId : int, setStatePacket, timeout_seconds : int = 0 ):
        """
        timeout_seconds 0 uses the default timeout of 10 seconds
        """
        super().__init__([crownstoneId], setStatePacket, MeshModes.SINGLE_TARGET_ACKED, timeout_seconds)

class MeshBroadcastAckedPacket(_MeshCommandPacket):
    """
    This is currently only supported for type setIBeaconConfig
    """
    def __init__(self, crownstoneIds: List[int], payload, timeout_seconds : int = 0):
        """
        timeout_seconds 0 uses the default timeout of 10 seconds
        """
        super().__init__(crownstoneIds, payload, MeshModes.BROADCAST_ACKED_IDS, timeout_seconds)


class StoneMultiSwitchPacket:

    def __init__(self, crownstoneId: int, switchVal: int):
        """
        :param crownstoneId:
        :param switchVal:  percentage [0..100] or special value (SwitchValSpecial).

        """
        self.crownstoneId = crownstoneId
        self.state = switchVal


    def serialize(self):
        writer = BufferWriter()
        writer.putUInt8(self.crownstoneId)
        writer.putUInt8(self.state)
        return writer.getBuffer()


class MeshMultiSwitchPacket:

    def __init__(self, packets=None):
        if packets is None:
            packets = []
        self.packets = packets

    def serialize(self):
        writer = BufferWriter()
        writer.putUInt8(len(self.packets))
        for stonePacket in self.packets:
            writer.putBytes(stonePacket.serialize())
        return writer.getBuffer()
