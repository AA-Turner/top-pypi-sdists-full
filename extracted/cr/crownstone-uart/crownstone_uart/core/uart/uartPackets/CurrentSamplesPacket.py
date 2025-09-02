from crownstone_core.util.Conversion import Conversion

COUNTER_FREQUENCY = 1.0 / 32768.0

class CurrentSamplesPacket:

    amountOfSamples = 100
    sampleSize = 2
    timestampSize = 4
    packetSize = amountOfSamples * sampleSize + timestampSize

    typeDescription = 'current'


    def __init__(self, payload):
        if len(payload) < self.packetSize:
            print("ERROR: INVALID PAYLOAD LENGTH", len(payload), payload)
            return
        
        self.timestampCounter = Conversion.uint8_array_to_uint32(payload[0:4])
        self.samples = []
        for i in range(4, self.packetSize, self.sampleSize):
            self.samples.append(Conversion.uint8_array_to_int16(payload[i:i+self.sampleSize]))

    def getDict(self):
        data = {}

        data["id"] = 0 # TODO: get the Crownstone ID here.
        data["type"] = self.typeDescription
        data["timestamp"] = self.timestampCounter
        data["data"] = self.samples

        return data