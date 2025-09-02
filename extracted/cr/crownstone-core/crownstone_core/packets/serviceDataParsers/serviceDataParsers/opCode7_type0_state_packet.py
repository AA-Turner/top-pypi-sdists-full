import time
from crownstone_core.util.Timestamp         import reconstructTimestamp
from crownstone_core.protocol.SwitchState   import SwitchState
from crownstone_core.util.BufferReader       import BufferReader
from crownstone_core.packets.serviceDataParsers.containers.AdvCrownstoneState import AdvCrownstoneState
from crownstone_core.packets.serviceDataParsers.containers.elements.AdvFlags import AdvFlags
from crownstone_core.packets.serviceDataParsers.containers.AdvExternalCrownstoneState import AdvExternalCrownstoneState
from crownstone_core.packets.serviceDataParsers.containers.elements.AdvGlobalFlags import AdvGlobalFlags


def parseStatePacket(reader: BufferReader):
    packet = AdvCrownstoneState()
    _parseStatePacket(packet, reader)
    packet.globalFlags = AdvGlobalFlags(reader.getUInt8())
    packet.validation = reader.getUInt8()
    return packet


def parseExternalStatePacket(reader: BufferReader):
    packet = AdvExternalCrownstoneState()
    _parseStatePacket(packet, reader)
    # position 13 on the state packet is the global flags, it is used in the external state for rssi
    packet.rssiOfExternalCrownstone = reader.getInt8()
    packet.validation = reader.getUInt8()
    return packet


def _parseStatePacket(packet, reader):
    packet.crownstoneId = reader.getUInt8()
    packet.switchState = SwitchState(reader.getUInt8())
    packet.flags = AdvFlags(reader.getUInt8())
    packet.temperature = reader.getInt8()
    powerFactor = reader.getInt8()
    realPower = reader.getInt16()

    packet.powerFactor = float(powerFactor) / 127.0

    # we cannot have a 0 for a power factor.To avoid division by 0, we set it to be either 0.01 or -0.01
    if 0 <= packet.powerFactor < 0.01:
        packet.powerFactor = 0.01
    elif -0.01 < packet.powerFactor < 0:
        packet.powerFactor = -0.01

    packet.powerUsageReal = float(realPower) / 8.0
    packet.powerUsageApparent = packet.powerUsageReal / packet.powerFactor

    packet.accumulatedEnergy = reader.getInt32()
    packet.accumulatedEnergy = packet.accumulatedEnergy * 64  # correction to display in J

    partialTimestamp        = reader.getUInt16()
    packet.uniqueIdentifier = partialTimestamp

    if packet.flags.timeIsSet:
        packet.timestamp = reconstructTimestamp(time.time(), partialTimestamp)
    else:
        packet.timestamp = partialTimestamp  # this is now a counter
