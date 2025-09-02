from crownstone_core.packets.serviceDataParsers.containers.elements.AdvCrownstoneErrorBitmask import AdvCrownstoneErrorBitmask

from crownstone_core.protocol.SwitchState import SwitchState
from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.packets.serviceDataParsers.containers.AdvCrownstoneSetupState import AdvCrownstoneSetupState
from crownstone_core.packets.serviceDataParsers.containers.elements.AdvFlags import AdvFlags


def parseSetupState(reader: BufferReader):
    packet = AdvCrownstoneSetupState()

    packet.switchState  = SwitchState(reader.getUInt8())
    packet.flags        = AdvFlags(reader.getUInt8())
    packet.temperature  = reader.getInt8()
    powerFactor         = reader.getInt8()
    realPower           = reader.getInt16()

    packet.powerFactor = float(powerFactor) / 127.0

    # we cannot have a 0 for a power factor.To avoid division by 0, we set it to be either 0.01 or -0.01
    if 0 <= packet.powerFactor < 0.01:
        packet.powerFactor = 0.01
    elif -0.01 < packet.powerFactor < 0:
        packet.powerFactor = -0.01

    packet.powerUsageReal     = float(realPower) / 8.0
    packet.powerUsageApparent = packet.powerUsageReal / packet.powerFactor
    packet.errorsBitmask      = AdvCrownstoneErrorBitmask(reader.getUInt32())
    packet.uniqueIdentifier   = reader.getUInt8()

    return packet