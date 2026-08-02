
# voltage is channel 0
# current is channel 1
from crownstone_core.util.Conversion import Conversion


class AdcChannelPacket:
    packetSize = 6

    def __init__(self, payload, channelIndex):
        if len(payload) < self.packetSize:
            print("ERROR: INVALID PAYLOAD LENGTH", len(payload), payload)
            return
        
        self.channelIndex = channelIndex
        
        self.pin    = payload[0]
        self.range  = Conversion.uint8_array_to_uint32(payload[1:1+4])
        self.refPin = payload[5]

    def getDict(self):
        data = {}

        data["pin"] = self.pin
        data["range"] = self.range
        data["refPin"] = self.refPin
        data["channelIndex"] = self.channelIndex

        return data