import logging
import logging.handlers

import pytest

from utf_queue_client.clients.base_producer import ConnectionError
from utf_queue_client.clients.sqa_test_result_producer import (
    SqaTestResultProducer,
)


@pytest.fixture()
def pika_logging_handler():
    """Add a handler to the pika logger to capture its output."""
    pika_logger = logging.getLogger("pika.adapters.utils.connection_workflow")
    handler = logging.handlers.BufferingHandler(capacity=100)
    pika_logger.addHandler(handler)
    yield handler
    pika_logger.removeHandler(handler)


@pytest.mark.parametrize(
    "set_environment_variable",
    [("UTF_QUEUE_SERVER_URL", "amqps://utfsilabs:utfsilabs@12.34.56.78:5671/%2f")],
    indirect=True,
)
def test_result_producer_connection_retry(
    set_environment_variable, mocker, pika_logging_handler
):
    """Test that the connection retry logic works as expected."""
    mocker.patch("utf_queue_client.clients.base_producer.NUM_CONNECTION_TRIES", 2)
    with pytest.raises(ConnectionError):
        _ = SqaTestResultProducer()
    error_records = [
        record
        for record in pika_logging_handler.buffer
        if record.levelno == logging.ERROR
    ]
    # The assertion below depends on the logging output of the pika library (version 1.3.2 as of this writing)
    # so if that changes, the message below may need to be updated.
    assert "2 exceptions in all" in error_records[-1].message
