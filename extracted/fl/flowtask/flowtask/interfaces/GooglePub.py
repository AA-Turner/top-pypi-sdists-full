from google.cloud import pubsub_v1
from google.auth.exceptions import GoogleAuthError
import asyncio
from .GoogleClient import GoogleClient
from ..exceptions import ComponentError

class GooglePubSubClient(GoogleClient):
    """
    Google Pub/Sub Client for managing topics, subscriptions, and message handling.
    """

    def __init__(self, *args, project_id: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_id = project_id
        self._publisher = None
        self._subscriber = None

    async def get_publisher(self):
        if not self._publisher:
            try:
                self._publisher = await asyncio.to_thread(pubsub_v1.PublisherClient, credentials=self.credentials)
            except GoogleAuthError as e:
                raise ComponentError(f"Google Pub/Sub authentication error: {e}")
        return self._publisher

    async def get_subscriber(self):
        if not self._subscriber:
            try:
                self._subscriber = await asyncio.to_thread(pubsub_v1.SubscriberClient, credentials=self.credentials)
            except GoogleAuthError as e:
                raise ComponentError(f"Google Pub/Sub authentication error: {e}")
        return self._subscriber

    async def create_topic(self, topic_name: str):
        publisher = await self.get_publisher()
        topic_path = publisher.topic_path(self.project_id, topic_name)
        await asyncio.to_thread(publisher.create_topic, name=topic_path)
        print(f"Topic '{topic_name}' created.")

    async def publish_message(self, topic_name: str, message: str):
        publisher = await self.get_publisher()
        topic_path = publisher.topic_path(self.project_id, topic_name)
        future = await asyncio.to_thread(publisher.publish, topic_path, message.encode("utf-8"))
        print(f"Published message ID: {future.result()}")

    async def create_subscription(self, topic_name: str, subscription_name: str):
        subscriber = await self.get_subscriber()
        topic_path = subscriber.topic_path(self.project_id, topic_name)
        subscription_path = subscriber.subscription_path(self.project_id, subscription_name)
        await asyncio.to_thread(subscriber.create_subscription, name=subscription_path, topic=topic_path)
        print(f"Subscription '{subscription_name}' created for topic '{topic_name}'.")

    async def pull_messages(self, subscription_name: str, max_messages: int = 10):
        subscriber = await self.get_subscriber()
        subscription_path = subscriber.subscription_path(self.project_id, subscription_name)
        response = await asyncio.to_thread(
            subscriber.pull, request={"subscription": subscription_path, "max_messages": max_messages}
        )
        for message in response.received_messages:
            print(f"Received message: {message.message.data}")
            await asyncio.to_thread(subscriber.acknowledge, subscription=subscription_path, ack_ids=[message.ack_id])
