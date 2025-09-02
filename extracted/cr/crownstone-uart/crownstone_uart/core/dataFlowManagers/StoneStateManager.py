from crownstone_uart.core.UartEventBus import UartEventBus
from crownstone_uart.topics.SystemTopics import SystemTopics
from crownstone_uart.topics.UartTopics import UartTopics


class StoneStateManager:
    def __init__(self):
        self.stones = {}
        UartEventBus.subscribe(SystemTopics.stateUpdate, self.handleStateUpdate)

    def handleStateUpdate(self, data):
        stoneId    = data[0]
        advPayload = data[1]

        if stoneId in self.stones:
            if hasattr(advPayload, 'timestamp'):
                if self.stones[stoneId].timestamp < advPayload.timestamp:
                    self.stones[stoneId] = advPayload
                    self.emitNewData(advPayload)
        else:
            UartEventBus.emit(SystemTopics.newCrownstoneFound, stoneId)
            self.stones[stoneId] = advPayload
            self.emitNewData(advPayload)
    
    def emitNewData(self, advPayload):
        UartEventBus.emit(UartTopics.newDataAvailable, advPayload)

    def getIds(self):
        ids = []
        for stoneId, stoneData in self.stones.items():
            ids.append(stoneId)

        return ids
