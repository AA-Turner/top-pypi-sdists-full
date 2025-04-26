import logging
import os
import ssl
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Optional

import msgpack
import pika
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from otel_extensions import instrumented
from pika.adapters.utils.connection_workflow import AMQPConnectorException
from pika.exceptions import AMQPConnectionError
from pika.spec import PERSISTENT_DELIVERY_MODE, TRANSIENT_DELIVERY_MODE, BasicProperties
from typing_extensions import Protocol

from utf_queue_client import DISABLE_SSL_VERIFICATION_DEFAULT

from . import Loggable

__all__ = ["BaseProducer", "BlockingProducer", "PikaChannel", "ConnectionError"]

NUM_CONNECTION_TRIES = 6
CONNECTION_RETRY_DELAY = 10


class ConnectionError(Exception):
    def __init__(self, inner):
        self.inner = inner

    def __repr__(self):
        return repr(self.inner)

    def __str__(self):
        return str(self.inner)


class PikaChannel(Protocol):
    def basic_publish(
        self,
        exchange: str,
        routing_key: str,
        body: bytes,
        properties: Optional[BasicProperties] = None,
        mandatory: bool = False,
    ): ...

    def queue_declare(
        self,
        queue,
        passive=False,
        durable=False,
        exclusive=False,
        auto_delete=False,
        arguments=None,
        callback=None,
    ): ...


class BaseProducer(ABC, Loggable):
    def __init__(self, url=None, producer_app_id: str = None):
        if url is None:
            try:
                url = os.environ["UTF_QUEUE_SERVER_URL"]
            except KeyError as e:
                raise RuntimeError(
                    "Queue server URL must be provided through parameter or UTF_QUEUE_SERVER_URL variable"
                ) from e
        self.producer_app_id = os.environ.get("UTF_PRODUCER_APP_ID", producer_app_id)
        self.url = url
        self._connection = None
        self._connect()

    @abstractmethod
    def _connect(self):
        pass

    @property
    @abstractmethod
    def is_connected(self):
        pass

    @property
    @abstractmethod
    def channel(self) -> PikaChannel:
        pass

    @instrumented
    def queue_declare(
        self,
        queue,
        **kwargs,
    ):
        span = trace.get_current_span()
        span.set_attribute("queue", queue)
        self.channel.queue_declare(queue, **kwargs)

    def publish(self, exchange: str, routing_key: str, payload: dict, persistent: bool):
        delivery_mode = (
            PERSISTENT_DELIVERY_MODE if persistent else TRANSIENT_DELIVERY_MODE
        )
        body = msgpack.dumps(payload)
        carrier = {}
        TraceContextTextMapPropagator().inject(carrier)
        properties = pika.BasicProperties(
            delivery_mode=delivery_mode, app_id=self.producer_app_id, headers=carrier
        )
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=body,
            properties=properties,
        )


class BlockingProducer(BaseProducer):
    def __init__(self, url=None, producer_app_id: str = None):
        logging.getLogger("pika").setLevel(logging.WARNING)
        self._channel = None
        super().__init__(url, producer_app_id)

    def _connect(self):
        # connection will be made lazily
        self._connection = None
        self._channel = None

    @property
    def channel(self) -> PikaChannel:
        return self._channel  # noqa

    @property
    def is_connected(self):
        return self._connection.is_open

    @contextmanager
    def __connect(self):
        try:
            url_params = pika.URLParameters(self.url)
            url_params.connection_attempts = NUM_CONNECTION_TRIES
            url_params.retry_delay = CONNECTION_RETRY_DELAY
            if (
                os.environ.get(
                    "DISABLE_SSL_VERIFICATION", DISABLE_SSL_VERIFICATION_DEFAULT
                )
                == "true"
            ) and url_params.ssl_options is not None:
                ssl_context = ssl.create_default_context()  # NOSONAR
                ssl_context.check_hostname = False  # NOSONAR
                ssl_context.verify_mode = ssl.CERT_NONE  # NOSONAR
                url_params.ssl_options = pika.SSLOptions(ssl_context)
            with pika.BlockingConnection(url_params) as connection:
                self._connection = connection
                self._channel = self._connection.channel()
                yield
        except (AMQPConnectionError, AMQPConnectorException) as e:
            raise ConnectionError(e) from e

    def queue_declare(self, queue, **kwargs):
        with self.__connect():
            super().queue_declare(queue, **kwargs)

    def publish(self, exchange: str, routing_key: str, payload: dict, persistent: bool):
        with self.__connect():
            super().publish(exchange, routing_key, payload, persistent)
