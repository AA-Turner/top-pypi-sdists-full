import base64
from dataclasses import dataclass
from typing import Optional, Tuple
from urllib.parse import urlparse

import pika
from pika.spec import BasicProperties
from requests import RequestException
from requests import Session as RequestsSession
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from utf_queue_client.clients.base_producer import (
    BaseProducer,
    ConnectionError,
    PikaChannel,
)
from utf_queue_client.utils import get_queue_url_list

from . import Loggable

__all__ = ["HTTPProducer", "HTTPChannel", "CompositeHTTPProducer"]

DEFAULT_NUM_CONNECTION_RETRIES = 6
DEFAULT_CONNECTION_RETRY_DELAY = 10


@dataclass
class UrlInfo:
    amqp_url: str
    http_url: str
    virtual_host: str
    username: str
    password: str


class HTTPChannel(PikaChannel):
    def __init__(
        self,
        url: str,
        credentials: Tuple[str, str],
        virtual_host: str,
        retries=None,
        retry_delay=None,
    ):
        if retries is None:
            retries = DEFAULT_NUM_CONNECTION_RETRIES
        if retry_delay is None:
            retry_delay = DEFAULT_CONNECTION_RETRY_DELAY
        self.client = RequestsSession()
        self.client.verify = False
        self.client.auth = credentials
        self.client.mount(
            "https://",
            HTTPAdapter(
                max_retries=Retry(
                    total=retries,
                    backoff_factor=retry_delay,
                    status_forcelist=[404, 429, 500, 502, 503, 504],
                )
            ),
        )
        self.url = url
        self.virtual_host = virtual_host
        if self.virtual_host == "/":
            self.virtual_host = "%2F"

    @classmethod
    def basic_properties_to_json(cls, properties: Optional[BasicProperties]) -> dict:
        props_json = {}
        if properties:
            for key in [
                "app_id",
                "content_type",
                "content_encoding",
                "correlation_id",
                "cluster_id",
                "delivery_mode",
                "expiration",
                "headers",
                "message_id",
                "priority",
                "reply_to",
                "timestamp",
                "type",
                "user_id",
            ]:
                val = getattr(properties, key)
                if val is not None:
                    props_json[key] = val
        return props_json

    def basic_publish(
        self,
        exchange: str,
        routing_key: str,
        body: bytes,
        properties: Optional[BasicProperties] = None,
        mandatory: bool = False,
    ):
        if not exchange:
            exchange = "amq.default"
        publish_url = f"{self.url}/api/exchanges/{self.virtual_host}/{exchange}/publish"
        try:
            r = self.client.post(
                publish_url,
                json={
                    "properties": self.basic_properties_to_json(properties),
                    "routing_key": routing_key,
                    "payload": base64.b64encode(body).decode("utf-8"),
                    "payload_encoding": "base64",
                },
            )
            r.raise_for_status()
        except RequestException as e:
            raise ConnectionError(e) from e

    def queue_declare(
        self,
        queue,
        passive=False,
        durable=False,
        exclusive=False,
        auto_delete=False,
        arguments=None,
        callback=None,
    ):
        declare_url = f"{self.url}/api/queues/{self.virtual_host}/{queue}"
        try:
            r = self.client.put(
                declare_url, json={"auto_delete": auto_delete, "durable": durable}
            )
            r.raise_for_status()
        except RequestException as e:
            raise ConnectionError(e) from e


class HTTPProducer(BaseProducer):
    def __init__(
        self,
        url_info: UrlInfo,
        producer_app_id: Optional[str] = None,
    ):
        super().__init__(url_info.amqp_url, producer_app_id)
        self._channel = HTTPChannel(
            url_info.http_url,
            (url_info.username, url_info.password),
            url_info.virtual_host,
        )
        self.hostname = urlparse(url_info.http_url).hostname

    def _connect(self):
        # no long-lived connection
        pass

    def is_connected(self):
        return True  # pragma: nocover

    @property
    def channel(self) -> HTTPChannel:
        return self._channel


class CompositeHTTPProducer(Loggable):
    def __init__(self, url: str, producer_app_id: str = None):
        url_list = get_queue_url_list(url)
        self.producers = [
            HTTPProducer(self.convert_amqp_url_to_http_url(alt_url), producer_app_id)
            for alt_url in url_list
        ]

    @classmethod
    def convert_amqp_url_to_http_url(cls, amqp_url: str) -> UrlInfo:
        url_params = pika.URLParameters(amqp_url)
        host, delim, domain = url_params.host.partition(".")
        hostname = f"{host}-admin{delim}{domain}:{url_params.port}"
        scheme = "https" if url_params.ssl_options else "http"
        return UrlInfo(
            amqp_url=amqp_url,
            http_url=f"{scheme}://{hostname}",
            virtual_host=url_params.virtual_host,
            username=url_params.credentials.username,
            password=url_params.credentials.password,
        )

    def queue_declare(self, queue, **kwargs):
        for index, producer in enumerate(self.producers):
            if index:
                self.logger.warning(
                    f"Failed to execute queue_declare for host {self.producers[index - 1].hostname}, retrying with {producer.hostname}..."
                )
            try:
                return producer.queue_declare(queue, **kwargs)
            except ConnectionError:
                if index == len(self.producers) - 1:
                    raise
                continue

    def publish(self, exchange: str, routing_key: str, payload: dict, persistent: bool):
        for index, producer in enumerate(self.producers):
            if index:
                self.logger.warning(
                    f"Failed to execute publish for host {self.producers[index - 1].hostname}, retrying with {producer.hostname}..."
                )
            try:
                return producer.publish(exchange, routing_key, payload, persistent)
            except ConnectionError:
                if index == len(self.producers) - 1:
                    raise
                continue
