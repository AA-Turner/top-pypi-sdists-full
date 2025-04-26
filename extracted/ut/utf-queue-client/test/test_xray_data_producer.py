from unittest.mock import MagicMock

import pytest

from utf_queue_client.clients.xray_data_producer import (
    DummyXrayDataProducer,
    LocalXrayDataProducer,
    XrayDataProducer,
    XrayDataProducerFactory,
)


def test_xray_data_producer_empty_url():
    with pytest.raises(RuntimeError):
        _ = XrayDataProducer()


def test_xray_data_producer_create_connect_error(mocker):
    mock_class = mocker.patch(
        "utf_queue_client.clients.xray_data_producer.LocalXrayDataProducer"
    )
    mock_instance = MagicMock()
    mock_class.return_value = mock_instance
    mock_class.side_effect = ConnectionError("failing for test")
    with pytest.raises(ConnectionError):
        _ = XrayDataProducerFactory.create_producer()


def test_dummy_producer(xray_import_test_execution_data):
    producer = DummyXrayDataProducer()
    producer.publish_test_execution(xray_import_test_execution_data)


def test_local_xray_producer(xray_import_test_execution_data, mocker):
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
    producer = LocalXrayDataProducer()
    producer.producer_app_id = "DUMMY"
    producer.publish_test_execution(xray_import_test_execution_data)
    assert mock_producer_publish.called
    kwargs = mock_producer_publish.call_args.kwargs
    payload = kwargs.get("payload")
    assert payload.get("recordSubType") == "IMPORT_TEST_EXECUTION"
    assert payload.get("tenantKey") == "DUMMY"
    payload_data = payload.get("payload")
    assert payload_data.get("test_execution_key") == "DUMMY_EXEC"
    assert payload_data.get("add_tests_to_plan") is True
    assert payload_data.get("info").get("project") == "DUMMY"
    assert payload_data.get("info").get("test_plan_key") == "DUMMY_PLAN"
    assert len(payload_data.get("tests")) == 1
    test = payload_data.get("tests")[0]
    assert test.get("comment") == ""
    assert test.get("executed_by") == "test"
    assert test.get("finish") == "2025-02-11T07:39:25+00:00"
    assert test.get("start") == "2025-02-11T07:39:23+00:00"
    assert test.get("status") == "PASS"
    assert test.get("test_key") == "TC1234567890"
