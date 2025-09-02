from crownstone_core.Enums import CrownstoneOperationMode

from crownstone_core.Exceptions import CrownstoneException, CrownstoneError

from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.packets.serviceDataParsers.parsers import parseOpCode6, parseOpcode7
from crownstone_core.protocol.BluenetTypes import DeviceType
from crownstone_core.util.EncryptionHandler import EncryptionHandler
from crownstone_core.packets.serviceDataParsers.containers.AdvUnknownData import AdvUnknownData


class ServiceData:
    
    def __init__(self, data):
        """
        The parsed data ends up in the self.payload. These will be one of the Adv* classes defined in the ./containers/ folder.
        """
        self.opCode        = 0
        self.deviceType    = DeviceType.UNDEFINED
        self.operationMode = CrownstoneOperationMode.UNKNOWN
        self.payload       = None
        self.decrypted     = False

        self._data = data

        reader = BufferReader(self._data)
        self.opCode = reader.getUInt8()
        if self.opCode == 7:
            self.operationMode = CrownstoneOperationMode.NORMAL
        elif self.opCode == 6:
            self.operationMode = CrownstoneOperationMode.SETUP

        deviceType = reader.getUInt8()
        if DeviceType.has_value(deviceType):
            self.deviceType = DeviceType(deviceType)

    def parse(self, decryptionKey = None):
        if decryptionKey is not None:
            self.decrypt(decryptionKey)

        reader = BufferReader(self._data)
        reader.skip(2)

        if self.opCode == 7:
            try:
                self.payload = parseOpcode7(reader.getRemainingBytes())
            except CrownstoneException:
                self.payload = AdvUnknownData()
                self.payload.data = self._data
                raise CrownstoneException(CrownstoneError.INVALID_SERVICE_DATA, "Protocol not supported. Unknown data type. Could be because decryption failed.")
        elif self.opCode == 6:
            self.payload = parseOpCode6(reader.getRemainingBytes())
        else:
            self.payload = AdvUnknownData()
            self.payload.data = self._data
            raise CrownstoneException(CrownstoneError.INVALID_SERVICE_DATA, "Protocol not supported. Unknown opcode.")


    def getOperationMode(self):
        return self.operationMode

    def decrypt(self, keyHexString):
        if len(keyHexString) >= 16 and len(self._data) == 18:
            if self.operationMode == CrownstoneOperationMode.NORMAL:
                reader = BufferReader(self._data)
                encryptedData = reader.skip(2).getRemainingBytes()
                result = EncryptionHandler.decryptECB(encryptedData, keyHexString)

                for i in range(0, len(encryptedData)):
                    # the first 2 bytes are opcode and device type
                    self._data[i + 2] = result[i]

                self.decrypted = True
        else:
            raise CrownstoneException(CrownstoneError.COULD_NOT_DECRYPT, "ServiceData decryption failed. Invalid key or invalid data.")

