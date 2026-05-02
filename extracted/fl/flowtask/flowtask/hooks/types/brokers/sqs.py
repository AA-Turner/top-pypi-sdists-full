from typing import Optional, Any
from navigator.brokers.sqs import SQSConnection
from .base import BaseMQTrigger

class SQSTrigger(BaseMQTrigger):
    def __init__(
        self,
        *args,
        queue_name: str,
        credentials: Optional[dict] = None,
        actions: list = None,
        **kwargs
    ):
        super().__init__(
            *args,
            actions=actions,
            queue_name=queue_name,
            **kwargs
        )
        self._connection = SQSConnection(credentials=credentials)
        self.max_messages = kwargs.get('max_messages', 10)
        self.wait_time = kwargs.get('wait_time', 10)
        self.idle_sleep = kwargs.get('idle_sleep', 5)

    async def connect(self):
        await self._connection.connect()
        self._logger.info(
            "AWS SQS connection established."
        )

    async def disconnect(self):
        await self._connection.disconnect()
        self._logger.info(
            "AWS SQS connection closed."
        )

    async def start_consuming(self):
        await self._connection.consume_messages(
            queue_name=self._queue_name,
            callback=self._consumer_callback,
            max_messages=self.max_messages,
            wait_time=self.wait_time,
            idle_sleep=self.idle_sleep
        )
