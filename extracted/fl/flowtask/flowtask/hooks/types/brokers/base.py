import asyncio
from typing import Optional, Any
from aiohttp import web
from abc import abstractmethod
from ..base import BaseTrigger

class BaseMQTrigger(BaseTrigger):
    def __init__(self, *args, actions: list = None, **kwargs):
        super().__init__(*args, actions=actions, **kwargs)
        self.consumer_task: Optional[asyncio.Task] = None
        self._connection = None  # To be set in subclass
        self._queue_name = kwargs.get('queue_name', 'default_queue')

    @abstractmethod
    async def connect(self):
        """Establish the connection."""
        pass

    @abstractmethod
    async def disconnect(self):
        """Disconnect the connection."""
        pass

    async def on_startup(self, app):
        self._logger.info(
            f"Starting MQ Broker {self.__class__.__name__}"
        )
        await self.connect()
        self.consumer_task = asyncio.create_task(self.start_consuming())

    async def on_shutdown(self, app):
        self._logger.info(
            f"Shutting down MQ Broker {self.__class__.__name__}"
        )
        if self.consumer_task:
            self.consumer_task.cancel()
            try:
                await self.consumer_task
            except asyncio.CancelledError:
                self._logger.info("Consumer task cancelled.")
            self.consumer_task = None
        await self.disconnect()

    @abstractmethod
    async def start_consuming(self):
        """Start consuming messages."""
        pass

    def setup(self, app: web.Application):
        super().setup(app)

    @abstractmethod
    async def _consumer_callback(self, *args, **kwargs) -> None:
        pass
