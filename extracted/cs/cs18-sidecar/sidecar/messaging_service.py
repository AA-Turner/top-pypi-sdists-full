import uuid
import requests
import base64
from urllib.parse import urlparse, ParseResult
from requests.auth import HTTPBasicAuth
from logging import Logger
from jsonpickle import json

from sidecar.utils import CallsLogger


class MessagingConnectionProperties:
    def __init__(self, address: str, exchange: str):
        # address passed in base64
        address_bytes = address.encode('utf-16')
        base64_bytes = base64.b64decode(address_bytes)
        self.address = base64_bytes.decode('utf-16')
        self.exchange = exchange

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.address == other.address and \
                   self.exchange == other.exchange
        return False

    def __repr__(self):
        return f"address={self.address} exchange={self.exchange}"


class MessagingService:
    def __init__(self, props: MessagingConnectionProperties, logger: Logger):
        self._logger = logger

        url: ParseResult = urlparse(props.address)

        self._auth = requests.auth.HTTPBasicAuth(url.username, url.password)
        self._exchange = props.exchange
        self._vhost = url.path
        self._destination = f"rabbitmq://{url.hostname}{url.path}/"
        self._base = f"{url.scheme}://{url.netloc}"

    @CallsLogger.wrap
    def publish(self, message_type: str, message):
        try:
            message_id = uuid.uuid1()
            payload = {
                "messageId": str(message_id),
                "conversationId": str(message_id),
                "destinationAddress": self._destination + message_type,
                "messageType": [
                    "urn:message:{}".format(message_type)
                ],
                "message": message,
                "headers": {}
            }

            data = {
                "properties": {},
                "routing_key": "",
                "payload": json.dumps(payload),
                "payload_encoding": "string"
            }

            # virtual_host already starts with / to support no virtual host
            url = f"{self._base}/api/exchanges{self._vhost}/{self._exchange}/publish"
            response = requests.post(url=url, json=data, auth=self._auth)
            if not response.ok:
                raise Exception(f'Failed to send message to {self._base}{self._vhost}/{self._exchange}')

        except Exception as exc:
            self._logger.exception("an error occurred while connecting to a queue {exc}".format(exc=exc))
