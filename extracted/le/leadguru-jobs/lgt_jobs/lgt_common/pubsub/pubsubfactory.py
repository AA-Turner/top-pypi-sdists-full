from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPICallError
from google.auth.transport.grpc import *


class PubSubFactory:

    def __init__(self, project_id):
        self.project_id = project_id
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def get_topic_path(self, topic_name):
        return self.publisher.api.topic_path(self.project_id, f'{topic_name}')

    def get_subscription_path(self, subscriber_name, topic_name):
        return self.subscriber.api.subscription_path(self.project_id, f'{topic_name}_{subscriber_name}')

    def create_topic_if_doesnt_exist(self, topic_name) -> pubsub_v1.types.pubsub_gapic_types.Topic:
        topic_path = self.get_topic_path(topic_name)
        try:
            return self.publisher.api.get_topic(topic=topic_path)
        except GoogleAPICallError as ex:
            if ex.grpc_status_code == grpc.StatusCode.NOT_FOUND:
                return self.publisher.api.create_topic(name=topic_path)
            else:
                raise

    def delete_topic(self, topic_name: str):
        topic_path = self.get_topic_path(topic_name)
        self.publisher.api.delete_topic(topic=topic_path)

    def create_subscription_if_doesnt_exist(self, subscriber_name, topic_name,
                                            ack_deadline_seconds=60) -> pubsub_v1.types.pubsub_gapic_types.Subscription:
        subscription_path = self.get_subscription_path(subscriber_name, topic_name)
        self.create_topic_if_doesnt_exist(topic_name)

        try:
            return self.subscriber.api.get_subscription(subscription=subscription_path)
        except GoogleAPICallError as ex:
            if ex.grpc_status_code == grpc.StatusCode.NOT_FOUND:
                return self.subscriber.api.create_subscription(name=subscription_path,
                                                               topic=self.get_topic_path(topic_name),
                                                               push_config=None,
                                                               ack_deadline_seconds=ack_deadline_seconds)
            else:
                raise
