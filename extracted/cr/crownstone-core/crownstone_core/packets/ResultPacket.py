from crownstone_core.protocol.BluenetTypes import ResultValue, ControlType
from crownstone_core.util.BufferReader import BufferReader


class ResultPacket:
    
    def __init__(self, data) :
        self.commandType = ControlType.UNSPECIFIED
        self.protocol = 0
        self.size = 0
        self.commandTypeUInt16 = 0
        self.resultCode = 0
        self.valid = True

        self.payload = []
        self.load(data)
    

    def load(self, data) :
        # TODO: remove minSize, and use: self.payload = payload.getRemainingBytes()
        # TODO: raise error instead of setting self.valid.
        minSize = 7

        if len(data) >= minSize:
            payload = BufferReader(data)

            self.protocol = payload.getUInt8()
            self.commandTypeUInt16 = payload.getUInt16()
            resultNumber  = payload.getUInt16()

            if ControlType.has_value(self.commandTypeUInt16) and ResultValue.has_value(resultNumber):
                self.commandType = ControlType(self.commandTypeUInt16)
                self.resultCode  = ResultValue(resultNumber)
                self.size        = payload.getUInt16()

                totalSize = minSize + self.size
                if len(data) >= totalSize:
                    if self.size == 0:
                        return

                    for i in range(minSize, totalSize):
                        self.payload.append(data[i])
                else:
                    self.valid = False
            else:
                self.valid = False
        else:
            self.valid = False

    def __repr__(self):
        return F"{self.__class__}({self.__dict__})"

