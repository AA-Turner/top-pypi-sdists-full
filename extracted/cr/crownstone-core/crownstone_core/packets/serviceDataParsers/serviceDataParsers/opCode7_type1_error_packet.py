import time

from crownstone_core.packets.serviceDataParsers.containers.elements.AdvCrownstoneErrorBitmask import AdvCrownstoneErrorBitmask
from crownstone_core.util.Timestamp           import reconstructTimestamp
from crownstone_core.util.BufferReader        import BufferReader
from crownstone_core.packets.serviceDataParsers.containers.AdvErrorPacket import AdvErrorPacket
from crownstone_core.packets.serviceDataParsers.containers.elements.AdvFlags import AdvFlags
from crownstone_core.packets.serviceDataParsers.containers.AdvExternalErrorPacket import AdvExternalErrorPacket


def parseErrorPacket(reader: BufferReader):
    packet = AdvErrorPacket()
    _parseErrorPacket(packet, reader)
    realPower = reader.getInt16()
    packet.powerUsageReal = float(realPower) / 8.0
    return packet


def parseExternalErrorPacket(reader: BufferReader):
    packet = AdvExternalErrorPacket()
    _parseErrorPacket(packet, reader)
    packet.powerUsageReal = reader.getUInt8()
    packet.validation     = reader.getUInt8()
    return packet


def _parseErrorPacket(packet, reader: BufferReader):
    packet.crownstoneId     = reader.getUInt8()
    packet.errorsBitmask    = AdvCrownstoneErrorBitmask(reader.getUInt32())
    packet.errorTimestamp   = reader.getUInt32()
    packet.flags            = AdvFlags(reader.getUInt8())
    packet.temperature      = reader.getInt8()
    partialTimestamp        = reader.getUInt16()
    packet.uniqueIdentifier = partialTimestamp

    if packet.flags.timeIsSet:
        packet.timestamp = reconstructTimestamp(time.time(), partialTimestamp)
    else:
        packet.timestamp = partialTimestamp  # this is now a counter
