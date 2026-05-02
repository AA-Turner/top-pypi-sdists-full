import asyncio
from gmqtt import Client as MQTTClient
from ..base import BaseTrigger

class MQTTTrigger(BaseTrigger):
    def __init__(self, *args, broker_url: str, topics: list, **kwargs):
        super().__init__(*args, **kwargs)
        self.broker_url = broker_url
        self.topics = topics
        self.client = MQTTClient(client_id='')
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

    async def on_startup(self, app):
        self._logger.info(f"Connecting to MQTT broker at {self.broker_url}")
        await self.client.connect(self.broker_url)

    async def on_shutdown(self, app):
        self._logger.info("Disconnecting from MQTT broker")
        await self.client.disconnect()

    def on_connect(self, client, flags, rc, properties):
        self._logger.info("Connected to MQTT broker")
        for topic in self.topics:
            client.subscribe(topic)
            self._logger.info(f"Subscribed to topic: {topic}")

    def on_disconnect(self, client, packet, exc=None):
        self._logger.warning("Disconnected from MQTT broker")
        # Implement reconnection logic if needed

    def on_message(self, client, topic, payload, qos, properties):
        self._logger.info(f"Received message on topic {topic}: {payload}")
        asyncio.create_task(self.run_actions(topic=topic, payload=payload))
