

# voltage is channel 0
# current is channel 1
from crownstone_core.util.Conversion import Conversion

from crownstone_uart.core.uart.uartPackets.AdcChannelPacket import AdcChannelPacket


class AdcConfigPacket:
    amountOfChannels = 2
    channelSize = 6 
    packetSize = amountOfChannels * channelSize + 1 + 4 # 4 for sampling period, 1 for count

    def __init__(self, payload):
        if len(payload) < 1:
            print("ERROR: INVALID PAYLOAD LENGTH", len(payload), payload)
            return
        
        self.channels = []
        
        index = 0
        self.amountOfChannels = payload[index]
        index += 1
        self.packetSize = self.amountOfChannels * self.channelSize + 1 + 4 # 4 for sampling period, 1 for count
        
        if len(payload) < self.packetSize:
            print("ERROR: INVALID PAYLOAD LENGTH", len(payload), payload)
            return
        
        for i in range(0,self.amountOfChannels):
            self.channels.append(AdcChannelPacket(payload[ index : index+self.channelSize ], i))
            index += self.channelSize
        
        self.samplingPeriod = Conversion.uint8_array_to_uint32(payload[index:index+4])



    def getDict(self):
        data = {}
        
        data["amountOfChannels"] = self.amountOfChannels
        data["channels"] = {}
        for i in range(0, self.amountOfChannels):
            type = 'unknown'
            if i == 0:
                type = 'voltage'
            elif i == 1:
                type = 'current'
            data["channels"][type] = self.channels[i].getDict()
            
        data["samplingPeriod"] = self.samplingPeriod
        
        return data