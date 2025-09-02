from crownstone_core.packets.serviceDataParsers.serviceDataParsers.opCode6_type0_setupState        import parseSetupState
from crownstone_core.packets.serviceDataParsers.serviceDataParsers.opCode7_type4_alternative_state import parseAlternativeState
from crownstone_core.packets.serviceDataParsers.serviceDataParsers.opCode7_type6_microapp          import parseMicroappServiceData
from crownstone_core.packets.serviceDataParsers.serviceDataParsers.opCode7_type0_state_packet      import parseStatePacket, parseExternalStatePacket
from crownstone_core.packets.serviceDataParsers.serviceDataParsers.opCode7_type1_error_packet      import parseErrorPacket, parseExternalErrorPacket
from crownstone_core.packets.serviceDataParsers.serviceDataParsers.opCode7_type5_hubData           import parseHubData
from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.Exceptions import CrownstoneException, CrownstoneError


def parseOpCode6(data):
    reader = BufferReader(data)
    dataType = reader.getUInt8()
    
    if dataType == 0:
        return parseSetupState(reader)
    elif dataType == 5:
        return parseHubData(reader)
    else:
        raise CrownstoneException(CrownstoneError.UNKNOWN_SERVICE_DATA, "Could not parse this dataType")
        


def parseOpcode7(data):
    reader = BufferReader(data)
    dataType = reader.getUInt8()

    if dataType == 0:
        return parseStatePacket(reader)
    elif dataType == 1:
        return parseErrorPacket(reader)
    elif dataType == 2:
        return parseExternalStatePacket(reader)
    elif dataType == 3:
        return parseExternalErrorPacket(reader)
    elif dataType == 4:
        return parseAlternativeState(reader)
    elif dataType == 5:
        return parseHubData(reader)
    elif dataType == 6:
        return parseMicroappServiceData(reader)
    else:
        raise CrownstoneException(CrownstoneError.UNKNOWN_SERVICE_DATA, "Could not parse this dataType")

