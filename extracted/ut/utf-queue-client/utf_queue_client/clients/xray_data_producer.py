import os
from abc import ABC, abstractmethod
from datetime import datetime
from socket import gethostname
from typing import Optional

from otel_extensions import instrumented

from ..models import QueueMessage, XrayImportTestExecution
from . import Loggable
from .base_producer import BlockingProducer as AMQPBlockingProducer
from .base_producer import ConnectionError
from .http_producer import CompositeHTTPProducer

__all__ = [
    "XrayDataProducer",
    "LocalXrayDataProducer",
    "ConnectionError",
    "XrayDataProducerFactory",
]


class BaseXrayDataProducer(ABC):
    @abstractmethod
    def publish_test_execution(self, import_test_exec: dict):
        """publish a test execution object"""


class XrayDataProducer(BaseXrayDataProducer):
    RECORD_TYPE = "XRAY_EVENT"

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
    def publish_test_execution(self, import_test_exec: XrayImportTestExecution):
        queue_message = QueueMessage(
            payload=import_test_exec,
            recordType=self.RECORD_TYPE,
            recordSubType="IMPORT_TEST_EXECUTION",
            tenantKey=self.producer_app_id,
            recordTimestamp=datetime.now().isoformat(),
        )
        self.__producer_client.publish(
            exchange="",
            routing_key=self.queue_name,
            payload=queue_message.as_dict(),
            persistent=True,
        )


class DummyXrayDataProducer(BaseXrayDataProducer):
    def publish_test_execution(self, import_test_exec: XrayImportTestExecution):
        # noqa
        pass


class LocalXrayDataProducer(XrayDataProducer):
    def __init__(self):
        super().__init__(
            "amqp://guest:guest@localhost:5672/%2f",
            os.environ.get(
                "UTF_PRODUCER_APP_ID", f"LocalXrayDataProducer at {gethostname()}"
            ),
        )


class XrayDataProducerFactory(Loggable):
    @classmethod
    def create_producer(cls, raise_on_connection_error=False):
        try:
            queue_server_url = os.environ.get("UTF_QUEUE_SERVER_URL")
            if queue_server_url is not None:
                return XrayDataProducer(
                    url=queue_server_url,
                    producer_app_id=os.environ.get("UTF_PRODUCER_APP_ID"),
                    producer_class=CompositeHTTPProducer,
                )
            else:
                return LocalXrayDataProducer()
        except ConnectionError as e:
            cls.logger.warning(f"Unable to connect to queue server: {repr(e)}")
            if raise_on_connection_error:
                raise
            return DummyXrayDataProducer()
