import os

import pytest

from utf_queue_client.clients.test_rail_data_producer import (
    DummyTestRailDataProducer,
    LocalTestRailDataProducer,
    TestRailDataProducer,
    TestRailDataProducerFactory,
)


def test_result_producer_empty_url():
    with pytest.raises(RuntimeError):
        _ = TestRailDataProducer()


@pytest.mark.parametrize("queue_consumer", [60, 120], indirect=True)
def test_result_producer_central_queue(
    request,
    test_rail_add_test_result,
    amqp_url,
    queue_consumer,
):
    os.environ["UTF_PRODUCER_APP_ID"] = request.node.name
    producer = TestRailDataProducerFactory.create_producer()
    producer.publish_add_test_result(test_rail_add_test_result)
    queue_consumer.expect_messages(1)


def test_dummy_producer(test_rail_add_test_result):
    producer = DummyTestRailDataProducer()
    producer.publish_add_test_result(test_rail_add_test_result)


def test_local_test_rail_producer(test_rail_add_test_result, mocker):
    mocker.patch(
        "utf_queue_client.clients.base_producer.BlockingProducer.__init__",
        return_value=None,
    )
    mocker.patch(
        "utf_queue_client.clients.base_producer.BlockingProducer.queue_declare"
    )
    mock_producer_publish = mocker.patch(
        "utf_queue_client.clients.base_producer.BlockingProducer.publish"
    )
    producer = LocalTestRailDataProducer()
    producer.producer_app_id = "DUMMY"
    producer.publish_add_test_result(test_rail_add_test_result)
    assert mock_producer_publish.called
    kwargs = mock_producer_publish.call_args.kwargs
    payload = kwargs.get("payload")
    assert payload.get("recordType") == "TEST_RAIL_EVENT"
    assert payload.get("recordSubType") == "TEST_RESULT"
    assert payload.get("tenantKey") == "DUMMY"
    payload_data = payload.get("payload")
    assert payload_data.get("version") == "v1"
    assert payload_data.get("comment") == "testing"
    assert payload_data.get("status") == "pass"
    assert payload_data.get("run_id") == 1234
    assert payload_data.get("id") == "C123"
    custom_props = payload_data.get("custom_props")
    assert custom_props.get("custom_interface_type") == "gcc"
    assert custom_props.get("custom_evk_version") == "v2"
