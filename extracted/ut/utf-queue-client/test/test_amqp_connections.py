import logging
import os
import time
from urllib.parse import quote

import pika
import pytest

from utf_queue_client.clients.base_producer import BlockingProducer
from utf_queue_client.utils import UTF_QUEUE_REGION_MAP

regions = list(UTF_QUEUE_REGION_MAP.values())
servers = [f"utf-queue-{region}" for region in regions]


@pytest.fixture(params=servers)
def queue_server(request):
    yield request.param


@pytest.mark.parametrize(
    "username, password",
    [
        (os.environ["UTF_QUEUE_USERNAME_LDAP"], os.environ["UTF_QUEUE_PASSWORD_LDAP"]),
        (os.environ["UTF_QUEUE_USERNAME"], os.environ["UTF_QUEUE_PASSWORD"]),
    ],
)
def test_producer(queue_server, username, password):
    suffix = ".silabs.net"
    queue_server = f"{queue_server}{suffix}"
    logger = logging.getLogger("test_producer")
    logger.info("Creating producer...")
    p = BlockingProducer(
        url=f"amqps://{username}:{quote(password)}@{queue_server}:443/testing?stack_timeout=30",
    )
    logger.info(f"{queue_server}: Created producer")
    params = pika.URLParameters(p.url)
    logger.info(f"stack timeout: {params.stack_timeout}")
    begin = time.time()
    for _ in range(0, 3):
        logger.info(f"{queue_server}: declaring queue...")
        start = time.time()
        p.queue_declare("default", durable=True)
        stop = time.time()
        logger.info(
            f"{queue_server}: done declaring queue in {stop - start} sec.  Total time: {stop - begin}"
        )
