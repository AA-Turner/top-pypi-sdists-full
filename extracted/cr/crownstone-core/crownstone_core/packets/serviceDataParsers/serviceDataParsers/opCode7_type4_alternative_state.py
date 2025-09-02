import time

from crownstone_core.protocol.SwitchState import SwitchState
from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.util.Timestamp import reconstructTimestamp
from crownstone_core.packets.serviceDataParsers.containers.AdvAlternativeState import AdvAlternativeState
from crownstone_core.packets.serviceDataParsers.containers.elements.AdvFlags import AdvFlags


def parseAlternativeState(reader: BufferReader):
    packet = AdvAlternativeState()
    packet.crownstoneId             = reader.getUInt8()
    packet.switchState              = SwitchState(reader.getUInt8())
    packet.flags                    = AdvFlags(reader.getUInt8())
    packet.behaviourMasterHash      = reader.getUInt16()
    packet.assetFilterMasterVersion = reader.getUInt16()
    packet.assetFilterMasterCRC     = reader.getUInt32()
    partialTimestamp                = reader.getUInt16()
    reader.skip()
    packet.validation               = reader.getUInt8()
    packet.uniqueIdentifier         = partialTimestamp
    
    if packet.flags.timeIsSet:
        packet.timestamp = reconstructTimestamp(time.time(), partialTimestamp)
    else:
        packet.timestamp = partialTimestamp # this is now a counter

    return packet