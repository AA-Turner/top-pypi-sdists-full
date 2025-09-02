from crownstone_core.util.BufferReader import BufferReader

from crownstone_core.protocol.BluenetTypes import ControlType, SetPersistenceMode, GetPersistenceMode, StateType
from crownstone_core.util.Conversion import Conversion

SUPPORTED_PROTOCOL_VERSION = 5

# TODO: get rid of this class; move to ControlPacket or some base packet that has a payload.
class BLEPacket:

    def __init__(self, packetType):
        self.lengthAsUint8Array = [0, 0]
        self.payload = []
        self.type = packetType.value

    def loadKey(self, keyString):
        self.payload = Conversion.ascii_or_hex_string_to_16_byte_array(keyString)
        return self._process()
    
    def loadString(self, string):
        self.payload = Conversion.string_to_uint8_array(string)
        return self._process()

    def loadInteger(self, integer):
        self.payload = [Conversion.int8_to_uint8(integer)]
        return self._process()

    def loadInt8(self, int8):
        self.payload = [Conversion.int8_to_uint8(int8)]
        return self._process()

    def loadUInt8(self, uint8):
        self.payload = [uint8]
        return self._process()

    def loadUInt16(self, uint16):
        self.payload = Conversion.uint16_to_uint8_array(uint16)
        return self._process()

    def loadInt16(self, uint16):
        self.payload = Conversion.int16_to_uint8_array(uint16)
        return self._process()

    def loadUInt32(self, uint32):
        self.payload = Conversion.uint32_to_uint8_array(uint32)
        return self._process()

    def loadInt32(self, int32):
        self.payload = Conversion.int32_to_uint8_array(int32)
        return self._process()

    def loadFloat(self, float):
        self.payload = Conversion.float_to_uint8_array(float)
        return self._process()

    def loadByteArray(self, byteArray):
        self.payload = byteArray
        return self._process()

    def appendByteArray(self, byteArray):
        self.payload += byteArray
        return self._process()

    def _process(self):
        self.length = len(self.payload)
        self.lengthAsUint8Array = Conversion.uint16_to_uint8_array(len(self.payload))
        return self

    def serialize(self):
        packet = [SUPPORTED_PROTOCOL_VERSION]
        packet += Conversion.uint16_to_uint8_array(self.type)
        packet += self.lengthAsUint8Array
        packet += self.payload

        return packet



class ControlPacket(BLEPacket):

    def __init__(self, packetType):
        super().__init__(packetType)



class FactoryResetPacket(ControlPacket):

    def __init__(self):
        super().__init__(ControlType.FACTORY_RESET)
        self.loadUInt32(0xdeadbeef)



class ControlStateGetPacket(ControlPacket):

    def __init__(self, stateType: StateType, id = 0, persistenceMode = GetPersistenceMode.CURRENT):
        super().__init__(ControlType.GET_STATE)
        self.id = id
        self.loadUInt16(stateType)
        self.persistenceMode = persistenceMode.value


    def serialize(self):
        # TODO: make use of the base class, now there is a double implementation of the control packet.
        arr = [SUPPORTED_PROTOCOL_VERSION]
        arr += Conversion.uint16_to_uint8_array(self.type)
        arr += Conversion.uint16_to_uint8_array(self.length + 6) # the + 2 is for the stateType uint16, +2 for the id, +2 for persistenceMode and reserved
        arr += self.payload # this is the state type
        arr += Conversion.uint16_to_uint8_array(self.id)
        arr.append(self.persistenceMode)
        arr.append(0)
        return arr

class ControlStateGetResultPacket:
    def __init__(self, data):
        self.stateType = StateType.UNKNOWN
        self.id = 0
        self.persistenceMode = GetPersistenceMode.CURRENT
        self.payload = []
        self.load(data)

    def load(self, data):
        reader = BufferReader(data)
        self.stateType = reader.getUInt16()
        self.id = reader.getUInt16()
        self.persistenceMode = reader.getUInt8()
        reserved = reader.getUInt8()
        self.payload = reader.getRemainingBytes()



class ControlStateSetPacket(ControlPacket):

    def __init__(self, stateType: StateType, id=0, persistenceMode = SetPersistenceMode.STORED):
        super().__init__(ControlType.SET_STATE)
        self.stateType = stateType
        self.id = id
        self.persistenceMode = persistenceMode.value


    def serialize(self):
        # TODO: make use of the base class, now there is a double implementation of the control packet.
        arr = [SUPPORTED_PROTOCOL_VERSION]
        arr += Conversion.uint16_to_uint8_array(self.type)
        arr += Conversion.uint16_to_uint8_array(self.length + 6) # the + 2 is for the stateType uint16, +2 for the id, +2 for persistenceMode and reserved
        arr += Conversion.uint16_to_uint8_array(self.stateType)
        arr += Conversion.uint16_to_uint8_array(self.id)
        arr.append(self.persistenceMode)
        arr.append(0)
        arr += self.payload
        return arr
