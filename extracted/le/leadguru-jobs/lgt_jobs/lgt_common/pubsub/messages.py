import os
import time
from google.cloud import pubsub_v1
from loguru import logger

project_id = os.environ.get('PUBSUB_PROJECT_ID')


def publish_message2_pubsub(topic_name, message_json):
    def callback(message_future):
        try:
            pubsub_result = message_future.result()
            # When timeout is unspecified, the exception method waits indefinitely.
            if message_future.exception(timeout=60):
                logger.error(f'Publishing message on {topic_name} threw an Exception {message_future.exception()}.')
            else:
                logger.info('lgt-metric:lgt-slack-aggregator:pub-sub:message-sent')
                logger.info(pubsub_result)
        except Exception:
            logger.error(f'Error has happening during getting result of future message')

    attempt = 0
    while True:
        try:
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(project_id, topic_name)
            logger.info(f'Json: {message_json}')
            message = publisher.publish(topic_path, data=bytes(message_json, "utf8"))
            message.add_done_callback(callback)
            result = message.result()
            logger.info(f'Message has been sent {result}')
            return
        except:
            attempt = attempt + 1
            if attempt >= 3:
                raise
            time.sleep(3)
