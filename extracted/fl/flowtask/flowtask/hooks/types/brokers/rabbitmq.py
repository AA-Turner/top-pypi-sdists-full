from typing import Optional, Any
import aiormq
from navigator.brokers.rabbitmq import RabbitMQConnection
from .base import BaseMQTrigger


class RabbitMQTrigger(BaseMQTrigger):
    def __init__(
        self,
        *args,
        queue_name: str,
        routing_key: str = '',
        exchange_name: str = '',
        exchange_type: str = 'topic',
        credentials: Optional[str] = None,
        actions: list = None,
        **kwargs
    ):
        super().__init__(
            *args,
            actions=actions,
            queue_name=queue_name,
            **kwargs
        )
        self._queue_name = queue_name
        self._routing_key = routing_key
        self._exchange_name = exchange_name
        self._exchange_type = exchange_type
        self._connection = RabbitMQConnection(
            credentials=credentials
        )
        self.prefetch_count = kwargs.get('prefetch_count', 1)

    async def connect(self):
        await self._connection.connect()
        self._logger.info("RabbitMQ connection established.")
        # Ensure the exchange exists
        await self._connection.ensure_exchange(
            exchange_name=self._exchange_name or self._queue_name,
            exchange_type=self._exchange_type
        )
        # Ensure the queue exists and bind it to the exchange
        await self._connection.ensure_queue(
            queue_name=self._queue_name,
            exchange_name=self._exchange_name or self._queue_name,
            routing_key=self._routing_key
        )

    async def disconnect(self):
        await self._connection.disconnect()
        self._logger.info("RabbitMQ connection closed.")

    async def start_consuming(self):
        await self._connection.consume_messages(
            queue_name=self._queue_name,
            callback=self._consumer_callback,
            prefetch_count=self.prefetch_count
        )

    async def _consumer_callback(
        self,
        message: aiormq.abc.DeliveredMessage,
        body: Any
    ) -> None:
        """
        Callback from Consumer.

        Used to call actions based on consumer messages received.
        """
        try:
            message_id = message.delivery_tag
            self._logger.info(f"Received Message ID: {message_id} Body: {body}")
            # Call run_actions with the received message
            await self.run_actions(
                message_id=message_id,
                payload=message,
                message=body
            )
        except Exception as e:
            self._logger.error(f"Error in _consumer_callback: {e}")
            # Handle message rejection or requeueing if necessary
            await self._connection.reject_message(message, requeue=False)
