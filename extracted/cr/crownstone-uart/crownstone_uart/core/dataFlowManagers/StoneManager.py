from crownstone_uart.core.UartEventBus import UartEventBus
from crownstone_uart.core.dataFlowManagers.StoneStateManager import StoneStateManager
from crownstone_uart.topics.SystemTopics import SystemTopics


class StoneManager:
    
    def __init__(self):
        self.stones = {}
        self.stateManager = StoneStateManager()
        UartEventBus.subscribe(SystemTopics.newCrownstoneFound, self.handleNewStoneFromScan)

    def getIds(self):
        ids = []
        for stoneId, data in self.stones.items():
            ids.append(stoneId)

        return ids
    
    
    def getStones(self):
        return self.stones
    
    
    def handleNewStoneFromScan(self, stoneId):
        if stoneId in self.stones:
            self.stones[stoneId]["available"] = True
        else:
            self.stones[stoneId] = {"available": True, "id": stoneId}