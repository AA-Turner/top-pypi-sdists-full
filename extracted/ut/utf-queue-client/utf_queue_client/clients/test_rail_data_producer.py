import os
from abc import ABC, abstractmethod
from datetime import datetime
from socket import gethostname
from typing import Optional
from uuid import uuid4

from otel_extensions import instrumented

from ..models import QueueMessage, TestRailResult
from . import Loggable
from .base_producer import BlockingProducer as AMQPBlockingProducer
from .base_producer import ConnectionError
from .http_producer import CompositeHTTPProducer

__all__ = [
    "TestRailDataProducer",
    "DummyTestRailDataProducer",
    "ConnectionError",
    "TestRailDataProducerFactory",
]


class BaseTestRailDataProducer(ABC):
    @abstractmethod
    def publish_add_test_result(self, test_result: TestRailResult):
        """publish a test result object"""


class TestRailDataProducer(BaseTestRailDataProducer):
    RECORD_TYPE = "TEST_RAIL_EVENT"

    def __init__(
        self,
        url=None,
        producer_app_id: str = None,
        producer_class: Optional[type] = None,
    ):
        if producer_class is None:
            producer_class = AMQPBlockingProducer
        self.queue_name = "default"
        self.__producer_client = producer_class(url, producer_app_id)
        self.__producer_client.queue_declare(queue=self.queue_name, durable=True)
        self.producer_app_id = producer_app_id

    @instrumented
    def publish_add_test_result(self, test_result: TestRailResult):
        queue_message = QueueMessage(
            payload=test_result,
            recordType=self.RECORD_TYPE,
            recordSubType="TEST_RESULT",
            tenantKey=self.producer_app_id,
            recordTimestamp=datetime.now().isoformat(),
            messageId=str(uuid4()),
        )
        self.__producer_client.publish(
            exchange="",
            routing_key=self.queue_name,
            payload=queue_message.as_dict(),
            persistent=True,
        )


class LocalTestRailDataProducer(TestRailDataProducer):
    def __init__(self):
        super().__init__(
            "amqp://guest:guest@localhost:5672/%2f",
            os.environ.get(
                "UTF_PRODUCER_APP_ID", f"LocalTestRailDataProducer at {gethostname()}"
            ),
        )


class DummyTestRailDataProducer(BaseTestRailDataProducer):
    def publish_add_test_result(self, test_result: TestRailResult):
        # noqa
        pass


class TestRailDataProducerFactory(Loggable):
    @classmethod
    def create_producer(cls, raise_on_connection_error=False):
        try:
            queue_server_url = os.environ.get("UTF_QUEUE_SERVER_URL")
            if queue_server_url is not None:
                return TestRailDataProducer(
                    url=queue_server_url,
                    producer_app_id=os.environ.get("UTF_PRODUCER_APP_ID"),
                    producer_class=CompositeHTTPProducer,
                )
            else:
                return LocalTestRailDataProducer()
        except ConnectionError as e:
            cls.logger.warning(f"Unable to connect to queue server: {repr(e)}")
            if raise_on_connection_error:
                raise
            return DummyTestRailDataProducer()
