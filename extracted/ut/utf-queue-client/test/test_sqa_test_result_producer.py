import os

import pytest

from utf_queue_client.clients.sqa_test_result_producer import (
    DummySqaTestResultProducer,
    SqaTestResultProducer,
    SqaTestResultProducerFactory,
)


def test_result_producer_empty_url():
    with pytest.raises(RuntimeError):
        _ = SqaTestResultProducer()


@pytest.mark.parametrize("queue_consumer", [60, 120], indirect=True)
@pytest.mark.parametrize("use_http_producer", [True, False])
def test_result_producer_central_queue(
    request,
    sqa_app_build_result,
    sqa_test_result,
    sqa_test_session,
    amqp_url,
    queue_consumer,
    use_http_producer,
):
    os.environ["UTF_PRODUCER_APP_ID"] = request.node.name
    os.environ["UTF_QUEUE_USE_HTTP_PRODUCER"] = "true" if use_http_producer else "false"
    producer = SqaTestResultProducerFactory.create_producer(
        use_http_producer=use_http_producer
    )
    producer.publish_app_build_result(sqa_app_build_result)
    queue_consumer.expect_messages(1)
    producer.publish_test_session_start(sqa_test_session)
    queue_consumer.expect_messages(2)
    producer.publish_test_session_stop(sqa_test_session)
    queue_consumer.expect_messages(3)
    producer.publish_test_result(sqa_test_result)
    queue_consumer.expect_messages(4)


def test_dummy_producer(sqa_app_build_result, sqa_test_result, sqa_test_session):
    producer = DummySqaTestResultProducer()
    producer.publish_app_build_result(sqa_app_build_result)
    producer.publish_test_session_start(sqa_test_session)
    producer.publish_test_session_stop(sqa_test_session)
    producer.publish_test_result(sqa_test_result)
