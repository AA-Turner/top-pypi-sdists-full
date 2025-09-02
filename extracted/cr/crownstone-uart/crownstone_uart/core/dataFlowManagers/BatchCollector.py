import asyncio
from crownstone_uart.core.UartEventBus import UartEventBus

class BatchCollector:
    
    def __init__(self, topic= None, timeout = 15, interval = 0.05):
        self.response = None
        self.timeout = timeout
        self.interval = interval

        self.cleanupId = None
        if topic is not None:
            self.cleanupId = UartEventBus.subscribe(topic, self.collect)

    def __del__(self):
        UartEventBus.unsubscribe(self.cleanupId)

    def cleanup(self):
        UartEventBus.unsubscribe(self.cleanupId)

    def clear(self):
        self.response = None

    async def receive(self):
        counter = 0
        while counter < self.timeout:
            if self.response is not None:
                return self.response

            await asyncio.sleep(self.interval)
            counter += self.interval
        return None


    def collect(self, data):
        self.response = data

