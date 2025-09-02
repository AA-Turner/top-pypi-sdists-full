import asyncio
import time
import logging
from queue import Queue
from typing import Callable, Any

from crownstone_uart.core.UartEventBus import UartEventBus

_LOGGER = logging.getLogger(__name__)

class Collector:
    """
    Class that waits for data from the given topic.
    """
    def __init__(self, topic= None, timeout = 10, interval = 0.05):
        """
        :param topic:        The topic to receive data from.
        :param timeout:      Timeout in seconds.
        :param interval:     Polling interval.
        """
        # Config variables
        self.topic = topic
        self.timeout = timeout
        self.interval = interval

        # State variables
        self.response = None
        self.responses = Queue()
        self.timeLeft = -1
        self.callback = None
        self.cleanupId = None

    def __del__(self):
        self._cleanup()

    def _start(self):
        self.response = None
        self.responses = Queue()
        self.timeLeft = self.timeout
        if self.topic is not None:
            self.cleanupId = UartEventBus.subscribe(self.topic, self._onData)
        _LOGGER.debug(f"Start result collector with timeLeft={self.timeLeft} and topic={self.topic}")

    def _cleanup(self):
        _LOGGER.debug(f"Cleanup result collector")
        if self.cleanupId is not None:
            UartEventBus.unsubscribe(self.cleanupId)

        # Don't clean up response yet, they are used as return data.
        self.timeLeft = -1
        self.callback = None
        self.cleanupId = None

    # def clear(self):
    #     self.response = None

    async def receive(self):
        """
        Wait for data from the given topic.

        :return: The received data, in the format specified by the topic, or None on timeout.
        """
        self._start()
        while self.timeLeft > 0:
            if self.response is not None:
                self._cleanup()
                return self.response

            await asyncio.sleep(self.interval)
            self.timeLeft -= self.interval

        self._cleanup()
        return None

    def receive_sync(self):
        """
        Wait for data from the given topic.

        :return: The received data, in the format specified by the topic.
        """
        self._start()
        while self.timeLeft > 0:
            if self.response is not None:
                self._cleanup()
                return self.response

            time.sleep(self.interval)
            self.timeLeft -= self.interval

        self._cleanup()
        return None

    async def receiveNext(self):
        """
        Wait for data from the given topic.

        :return: The received data, in the format specified by the topic, or None on timeout.
        """
        if self.cleanupId is None:
            self._start()

        while self.timeLeft > 0:
            if not self.responses.empty():
                return self.responses.get()

            await asyncio.sleep(self.interval)
            self.timeLeft -= self.interval

        self._cleanup()
        return None

    async def receiveMultiple(self, callback: Callable[[Any], bool]):
        """
        Wait for data and let the callback handle the data.
        :param callback:          Function that handles the data and returns True to continue collecting, or False to stop collecting.
        """
        self._start()
        self.callback = callback
        await asyncio.sleep(self.timeLeft)
        callback(None)
        self._cleanup()

    def _onData(self, data):
        _LOGGER.debug(f"Result collector received {data}")
        if self.callback is None:
            self.response = data
            self.responses.put(data)
        else:
            if not self.callback(data):
                self._cleanup()

        # To be sure: always clean up when timed out.
        if self.timeLeft < 0:
            self._cleanup()

