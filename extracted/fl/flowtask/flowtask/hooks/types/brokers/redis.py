from typing import Optional, Any
from navigator.brokers.redis import RedisConnection
from .base import BaseMQTrigger


class RedisTrigger(BaseMQTrigger):
    """Redis Trigger.

    Trigger that listens to a Redis Stream and calls actions based on the received messages.
    """
    def __init__(
        self,
        *args,
        stream_name: str,
        group_name: str = 'default_group',
        consumer_name: str = 'default_consumer',
        credentials: Optional[dict] = None,
        actions: list = None,
        **kwargs
    ):
        super().__init__(
            *args,
            actions=actions,
            queue_name=stream_name,
            **kwargs
        )
        self._stream_name = stream_name
        self._group_name = group_name
        self._consumer_name = consumer_name
        self._connection = RedisConnection(
            credentials=credentials,
            group_name=group_name,
            consumer_name=consumer_name,
            queue_name=stream_name
        )
        self.count = kwargs.get('count', 1)
        self.block = kwargs.get('block', 1000)

    async def connect(self):
        await self._connection.connect()
        self._logger.info(
            "Redis connection established."
        )

    async def disconnect(self):
        await self._connection.disconnect()
        self._logger.info(
            "Redis connection closed."
        )

    async def start_consuming(self):
        await self._connection.consume_messages(
            queue_name=self._stream_name,
            callback=self._consumer_callback,
            count=self.count,
            block=self.block,
            consumer_name=self._consumer_name
        )

    async def _consumer_callback(
        self,
        data: dict,
        processed_message: Any
    ) -> None:
        """
        Callback from Consumer.

        Used to call actions based on consumer messages received.
        """
        try:
            message_id = data.get('message_id')
            self._logger.info(
                f"Received Message ID: {message_id} Body: {processed_message}"
            )
            # Call run_actions with the received message
            await self.run_actions(
                payload=data,
                message_id=message_id,
                message=processed_message
            )
        except Exception as e:
            self._logger.error(f"Error in _consumer_callback: {e}")
            raise
