import functools
import os
import requests
from requests.utils import urlparse

from python_agent.common import constants
from python_agent.test_listener.state_tracker import StateTracker


class RequestsPatcher(object):
    def __init__(self, config_data):
        self.config_data = config_data

    def patch(self):
        requests.post = self.handle_requests(requests.post)
        requests.get = self.handle_requests(requests.get)
        requests.put = self.handle_requests(requests.put)
        requests.delete = self.handle_requests(requests.delete)
        requests.patch = self.handle_requests(requests.patch)

    def handle_requests(self, f):
        @functools.wraps(f)
        def inner_handle(*args, **kwargs):
            if StateTracker().current_test_identifier:
                headers = kwargs.get("headers", {})
                headers[constants.TEST_IDENTIFIER] = (
                    StateTracker().current_test_identifier
                )
                kwargs["headers"] = headers

            proxy = self.config_data.proxy
            if proxy:
                result = urlparse(proxy)
                if result.scheme == "https":
                    os.environ["https_proxy"] = proxy
                else:
                    os.environ["http_proxy"] = proxy
            return f(*args, **kwargs)

        return inner_handle
