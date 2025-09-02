from crownstone_core.Enums import CrownstoneOperationMode

from crownstone_core.packets.ServiceData import ServiceData
from crownstone_core.protocol.Services import DFU_ADVERTISEMENT_SERVICE_UUID
from crownstone_core.util.Conversion import Conversion


class Advertisement:
    
    def __init__(self, address, rssi, nameText, serviceData, serviceUUID=None):
        self.address = address
        self.rssi = rssi
        self.name = nameText

        usedUUID = serviceUUID
        if isinstance(serviceUUID, str):
            usedUUID = serviceUUID.lower()

        self.serviceUUID = usedUUID
        self.serviceData = None
        self.operationMode = CrownstoneOperationMode.UNKNOWN

        dataString = serviceData
        
        if serviceData is not None:
            if isinstance(serviceData, str):
                dataArray = Conversion.hex_string_to_uint8_array(dataString)
                self.serviceUUID = Conversion.uint8_array_to_uint16([dataArray[0], dataArray[1]])
                # pop the service UUID
                dataArray.pop(0)
                dataArray.pop(0)
            else:
                dataArray = serviceData

            if dataArray:
                self.serviceData = ServiceData(dataArray)

            if self.serviceUUID == DFU_ADVERTISEMENT_SERVICE_UUID:
                self.operationMode = CrownstoneOperationMode.DFU
            else:
                self.operationMode = self.serviceData.getOperationMode()


    def isCrownstoneFamily(self):
        return self.serviceUUID == 0xC001 or self.serviceUUID == DFU_ADVERTISEMENT_SERVICE_UUID

    def hasServiceData(self):
        return self.serviceData is not None
    
    def getCrownstoneId(self):
        if self.hasServiceData() and self.isCrownstoneFamily():
            return self.serviceData.payload.crownstoneId
    
    def parse(self, decryptionKey = None):
        if self.hasServiceData() and self.isCrownstoneFamily():
            return self.serviceData.parse(decryptionKey = decryptionKey)

    # def getDictionary(self):
    #     data = {}
    #
    #     data["name"] = self.name
    #     data["rssi"] = self.rssi
    #     data["address"] = self.address
    #
    #     if self.serviceUUID is not None:
    #         data["serviceUUID"] = self.serviceUUID
    #
    #     if self.serviceData is not None:
    #         data["serviceData"] = self.serviceData.getDictionary()
    #
    #     return data
    #
    # def getSummary(self):
    #     data = {}
    #     if self.serviceData is not None:
    #         data = self.serviceData.getSummary(self.address)
    #     return data

    
