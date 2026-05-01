from unittest.mock import patch

import pytest
from pika.spec import PERSISTENT_DELIVERY_MODE, BasicProperties

import utf_queue_client.clients.http_producer
from utf_queue_client.clients.base_producer import (
    ConnectionError as QueueServerConnectionError,
)
from utf_queue_client.clients.http_producer import (
    CompositeHTTPProducer,
    HTTPChannel,
)

FAKE_CREDS = "notarealusername:notarealpassword"


def test_basic_properties_to_json():
    assert HTTPChannel.basic_properties_to_json(BasicProperties(app_id="foo")) == {
        "app_id": "foo"
    }
    assert HTTPChannel.basic_properties_to_json(
        BasicProperties(app_id="foo", delivery_mode=PERSISTENT_DELIVERY_MODE)
    ) == {"app_id": "foo", "delivery_mode": 2}
    assert HTTPChannel.basic_properties_to_json(None) == {}


def test_http_channel_connection_error():
    channel = HTTPChannel(
        "https://localshmost", ("user", "pass"), "/", retries=0, retry_delay=0
    )
    with pytest.raises(QueueServerConnectionError):
        channel.queue_declare("queue")
    with pytest.raises(QueueServerConnectionError):
        channel.basic_publish("exchange", "routing_key", b"foo", None)


def test_composite_producer_errors():
    with patch.object(
        utf_queue_client.clients.http_producer, "DEFAULT_NUM_CONNECTION_RETRIES", 0
    ):
        composite_producer = CompositeHTTPProducer(
            f"amqps://{FAKE_CREDS}@localshmost:443/%2F", "app_id"
        )
        composite_producer.producers.append(composite_producer.producers[0])
        with pytest.raises(QueueServerConnectionError):
            composite_producer.queue_declare("queue")
        with pytest.raises(QueueServerConnectionError):
            composite_producer.publish("exchange", "routing_key", {"foo": "bar"}, True)


@pytest.mark.parametrize(
    ("amqp_url", "expected_http_urls"),
    [
        (
            f"amqps://{FAKE_CREDS}@localshmost:443/%2F",
            ["https://localshmost-admin:443"],
        ),
        (
            f"amqps://{FAKE_CREDS}@utf-queue-central:443/%2F",
            ["https://utf-queue-central-admin:443"],
        ),
        (
            f"amqps://{FAKE_CREDS}@utf-queue-central.silabs.net:443/%2F",
            [
                "https://utf-queue-central-admin.silabs.net:443",
                "https://utf-queue-aus-admin.silabs.net:443",
                "https://utf-queue-bos-admin.silabs.net:443",
                "https://utf-queue-bud-admin.silabs.net:443",
                "https://utf-queue-hyd-admin.silabs.net:443",
                "https://utf-queue-yul-admin.silabs.net:443",
            ],
        ),
        (
            f"amqps://{FAKE_CREDS}@utf-queue-aus.silabs.net:443/%2F",
            [
                "https://utf-queue-central-admin.silabs.net:443",
                "https://utf-queue-aus-admin.silabs.net:443",
                "https://utf-queue-bos-admin.silabs.net:443",
                "https://utf-queue-bud-admin.silabs.net:443",
                "https://utf-queue-hyd-admin.silabs.net:443",
                "https://utf-queue-yul-admin.silabs.net:443",
            ],
        ),
    ],
)
def test_composite_producer_creation(amqp_url, expected_http_urls):
    composite_producer = CompositeHTTPProducer(amqp_url, "app_id")
    assert len(composite_producer.producers) == len(expected_http_urls)
    for index, value in enumerate(expected_http_urls):
        assert composite_producer.producers[index].channel.url == value
