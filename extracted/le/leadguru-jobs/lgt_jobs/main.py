import json
import traceback

from concurrent.futures import ThreadPoolExecutor

from lgt_common.pubsub.pubsubfactory import PubSubFactory
import logging as log
from lgt_jobs.env import project_id, background_jobs_topic, background_jobs_subscriber
from lgt_jobs.runner import BackgroundJobRunner
from lgt_jobs import jobs_map, env
import google.cloud.logging
from google.cloud.pubsub_v1 import SubscriberClient
from google.cloud.pubsub_v1.types import FlowControl
from google.cloud.pubsub_v1.subscriber.scheduler import ThreadScheduler


def callback(message):
    try:
        data = json.loads(message.data)
        log.info(f"[JOB]: {data} [START]")
        BackgroundJobRunner.run(jobs_map=jobs_map, data=data)
        log.info(f"[JOB]: {data} [FINISHED]")
    except Exception as exception:
        log.error(f"[ERROR][JOB]: {message.data} [ERROR] {traceback.format_exception(exception)} ")
        traceback.print_exception(exception)
    finally:
        # accept message any way
        message.ack()


if __name__ == '__main__':
    client = google.cloud.logging.Client()
    client.setup_logging()
    factory = PubSubFactory(project_id)
    factory.create_topic_if_doesnt_exist(background_jobs_topic)
    factory.create_subscription_if_doesnt_exist(background_jobs_subscriber, background_jobs_topic, 600)
    subscription_path = factory.get_subscription_path(background_jobs_subscriber, background_jobs_topic)
    # Launching a subscription
    future = SubscriberClient().subscribe(
        subscription_path,
        callback=callback,
        flow_control=FlowControl(max_messages=env.max_messages),
        scheduler=ThreadScheduler(executor=ThreadPoolExecutor(max_workers=env.pool_size))
    )

    log.info(f"Subscription to {subscription_path} started. We are waiting for a message..\n")

    try:
        future.result()  # Block the current thread until an exception occurs
    except Exception as exception:
        log.error(f"[ERROR][SUBSCRIBER]: {traceback.format_exception(exception)}")
        traceback.print_exception(exception)
        future.cancel()
