import json
import os
import certifi

from .agilicus_api.api_client import ApiClient
from .agilicus_api.configuration import Configuration

from agilicus.pagination.auto_iterator import get_page_on, patch_endpoint


class _ApiClientWrapper(ApiClient):
    def __init__(self, configuration: Configuration = None, **kwargs):
        if not configuration:
            configuration = Configuration()

        cert_path = os.environ.get("SSL_CERT_FILE")

        if cert_path and not configuration.ssl_ca_cert:
            configuration.ssl_ca_cert = cert_path
        elif configuration.ssl_ca_cert is None:
            configuration.ssl_ca_cert = certifi.where()

        super().__init__(configuration=configuration, **kwargs)

    def deserialize_dict(self, data: dict, response_type):
        return self.deserialize_json(json.dumps(data), response_type)

    def deserialize_json(self, json_data: str, response_type):
        response = _Response(json_data)
        return self.deserialize(response, response_type, True)

    def request(self, *args, headers=None, **kwargs):
        decorate_func = getattr(self.configuration, "decorate_request", None)
        if decorate_func:
            headers = (headers or {}).copy()
            decorate_func(headers)

        return super().request(*args, headers=headers, **kwargs)


def patched_api_client():
    return _ApiClientWrapper


class _Response:
    def __init__(self, data):
        self.data = data


def patch_endpoint_class(endpoint_class):
    """
    patches the Endpoint class to inject the AutoIterator into itself if needed.
    """
    original_init = endpoint_class.__init__

    def init_wrapper(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        if not get_page_on(self):
            return
        patch_endpoint(self)

    endpoint_class.__init__ = init_wrapper
