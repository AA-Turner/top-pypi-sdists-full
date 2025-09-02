import time
from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.util.Timestamp import reconstructTimestamp
from crownstone_core.packets.serviceDataParsers.containers.elements.AdvHubFlags import AdvHubFlags
from crownstone_core.packets.serviceDataParsers.containers.AdvHubState import AdvHubState


def parseHubData(reader: BufferReader):
    packet = AdvHubState()

    packet.crownstoneId = reader.getUInt8()
    packet.flags        = AdvHubFlags(reader.getUInt8())
    packet.hubData      = reader.getBytes(9)
    partialTimestamp    = reader.getUInt16()
    reader.skip()
    packet.validation   = reader.getUInt8()

    packet.uniqueIdentifier = partialTimestamp
    if packet.flags.timeIsSet:
        packet.timestamp = reconstructTimestamp(time.time(), partialTimestamp)
    else:
        packet.timestamp = partialTimestamp # this is now a counter

    return packet