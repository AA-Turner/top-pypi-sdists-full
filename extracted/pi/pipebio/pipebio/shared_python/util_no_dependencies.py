import copy
import logging
import os
import socket
import time
from typing import Callable, Dict

import requests
from requests import HTTPError, Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

DEFAULT_TIMEOUT = 60 * 10  # seconds


class MaxRetriesExceededError(Exception):
    """Raised when the maximum number of retries is exceeded."""
    pass


class CustomResponse(requests.Response):
    attempt: int

    def __init__(self, original_response: requests.Response, attempt: int = None):
        super().__init__()
        self.__dict__.update(original_response.__dict__)
        self.attempt = attempt if attempt else 0


class CustomSession(Session):
    max_retries: int

    def __init__(self,
                 base_session: Session = None,
                 header_function: Callable[[], Dict] = None,
                 max_retries=None,
                 backoff_factor=0.5,
                 retry_on=(500, 502, 503, 504),
                 timeout_minutes: int = 10,
                 **kwargs):
        """
        # NOTE: header_function has not been validated in a multithreading / multiprocessing environment.
        """
        super().__init__(**kwargs)
        if base_session:
            # NOTE: Here we do not copy, instead we create a reference to the base session.
            # That enables us to login to base_session AFTER creating CustomSession and have the same
            # cookies propagate out.
            # NOTE: The edge case would be if we started threads ahead of that because then the cookies
            # would not be copied over.
            # Likewise - there is a risk for header_function in the same way and I don't think that's yet supported.
            self.headers = base_session.headers
            self.cookies = base_session.cookies
            self.auth = base_session.auth
            self.params = getattr(base_session, 'params', {})
            self.hooks = base_session.hooks
            self.proxies = base_session.proxies
            self.verify = base_session.verify
            self.cert = base_session.cert
            self.adapters = base_session.adapters
        # NOTE: header_function has not been validated in a multithreading / multiprocessing environment.
        self.header_function = header_function
        self.max_retries = max_retries if max_retries is not None else 3
        self.backoff_factor = backoff_factor
        self.retry_on = retry_on
        self.timeout_seconds = round(timeout_minutes * 60)

    def get(self, url, **kwargs) -> CustomResponse:
        return self._request_with_retry('GET', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs) -> CustomResponse:
        return self._request_with_retry('POST', url, data=data, json=json, **kwargs)

    def patch(self, url, data=None, **kwargs) -> CustomResponse:
        return self._request_with_retry('PATCH', url, data=data, **kwargs)

    def delete(self, url, **kwargs) -> CustomResponse:
        return self._request_with_retry('DELETE', url, **kwargs)

    def _request_with_retry(self, method, url, **kwargs) -> CustomResponse:
        prefix = f'[{method}, {url}]'
        for attempt in range(1, self.max_retries + 1):
            try:
                headers_to_use = dict(self.headers).copy()

                if self.header_function:
                    headers = self.header_function()
                    headers_to_use.update(headers)

                if "timeout" in kwargs:
                    self.timeout = kwargs["timeout"]
                    del kwargs["timeout"]

                if "method" in kwargs:
                    method = kwargs["method"]
                    del kwargs["method"]

                if "url" in kwargs:
                    method = kwargs["url"]
                    del kwargs["url"]

                response = self.request(method, url, headers=headers_to_use, timeout=self.timeout_seconds, **kwargs)
                response = CustomResponse(response, attempt=attempt)
                if response.status_code not in self.retry_on:
                    return response
                print(f"{prefix} Retryable status {response.status_code} on attempt {attempt}")
            except requests.RequestException as e:
                print(f"{prefix} Request error on attempt {attempt}: {e}")

            sleep_time = self.backoff_factor * (2 ** (attempt - 1))
            print(f"{prefix} Retrying in {sleep_time:.1f}s... {method}, {url}")
            time.sleep(sleep_time)

        print(f"{prefix} Max retries exceeded.")
        raise MaxRetriesExceededError(f"{prefix} Max retries exceeded.")

    # Required when being used in a multi-threading / mult-processing environment.
    def __getstate__(self):
        state = self.__dict__.copy()

        # Remove objects that can't be pickled
        state['max_retries'] = self.max_retries

        return state

    # Required when being used in a multi-threading / mult-processing environment.
    def __setstate__(self, state):
        self.__dict__.update(state)

        self.max_retries = state['max_retries']


# https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/
class TimeoutHTTPAdapter(HTTPAdapter):

    def __init__(self,
                 post_retry_config: Retry,
                 other_retry_config: Retry,
                 header_function=None,
                 *args,
                 **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]

        self.post_retry_config = post_retry_config
        self.other_retry_config = other_retry_config
        self.header_function = header_function

        self.pool_kwargs = {
            # SO_KEEPALIVE: Sends keepalive packets to detect dead connections
            'socket_options': [(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)],
        }

        super().__init__(*args, **kwargs)

    # This method removes the `poolmanager` and `proxy_manager` from the HTTP adapter as they cannot be pickled.
    # Pickling can happen when passing objects into subprocesses (multiprocessing). We've had issues in workflow job
    # itests in the past where pickling didn't work correctly and important information was lost as a consequence.
    def __getstate__(self):
        state = self.__dict__.copy()

        # Remove objects that can't be pickled
        state.pop("poolmanager", None)
        state.pop("proxy_manager", None)

        return state

    # When restoring the HTTP adapter from a pickled object, we need to create new a new `poolmanager` and
    # `proxy_manager` since those were removed when pickling the adapter.
    def __setstate__(self, state):
        self.__dict__.update(state)

        # Re-initialize poolmanager when needed
        if not hasattr(self, 'poolmanager'):
            self.init_poolmanager(self._pool_connections, self._pool_maxsize, **self.pool_kwargs)
        if hasattr(self, 'proxy_manager') and self.proxy_manager is None:
            self.proxy_manager = {}

    def send(self, request, **kwargs):
        # Choose the retry configuration based on the HTTP method.
        if request.method.upper() == "POST":
            self.max_retries = self.post_retry_config
        else:
            self.max_retries = self.other_retry_config

        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout

        return super().send(request, **kwargs)


class UtilNoDependencies:

    # Copied from the google library.
    @staticmethod
    def raise_detailed_error(request_object):
        try:
            request_object.raise_for_status()
        except HTTPError as e:
            raise HTTPError(e, request_object.text)

    @staticmethod
    def mount_session_that_recalculates_headers_on_retry(session: requests.Session,
                                                         header_function: Callable[[], Dict] = None,
                                                         max_retries: int = 3,
                                                         timeout_minutes: int = 10) -> CustomSession:
        return CustomSession(
            session,
            max_retries=max_retries,
            backoff_factor=1,
            header_function=header_function,
            timeout_minutes=timeout_minutes
        )

    @staticmethod
    def mount_session_with_retries(
            session: requests.Session,
            retry_post: bool = False,
            backoff_factor: int = 5,
            total_retries: int = 5,
            timeout_minutes: int = 10,
    ) -> requests.Session:
        """
        Configures a requests.Session with retry logic for common HTTP methods.

        Parameters:
            session (requests.Session): The session instance to configure.
            retry_post (bool): If True, include POST in the standard retry methods.
            backoff_factor (float): Factor for calculating the delay between retries.
            total_retries (int): The total number of retry attempts for failed requests.
            timeout_minutes: How long to wait before timing out for a given http connection.

        Returns:
            requests.Session: The session with mounted retry adapters.
        """
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.DEBUG)
        logging.getLogger("requests").setLevel(logging.DEBUG)

        # Define the HTTP methods for standard retries.
        methods = ['HEAD', 'GET', 'OPTIONS', 'TRACE', 'PUT', 'PATCH', 'DELETE']

        # Define status codes for which retries should occur.
        server_errors = list(range(500, 600))
        force_list = [100, 101, 102, 103, 104, 404, 408, 429] + server_errors

        # Create the retry configuration for POST requests.
        error_codes_to_retry_for_post_requests = force_list if retry_post else [104, 502, 503, 504]
        post_retry_config = Retry(
            total=total_retries,
            backoff_factor=backoff_factor,
            status_forcelist=error_codes_to_retry_for_post_requests,
            raise_on_status=True,
            connect=total_retries,
            read=total_retries,
            allowed_methods=['POST']
        )

        # Create the retry configuration for other requests.
        other_retry_config = Retry(
            total=total_retries,
            backoff_factor=backoff_factor,
            status_forcelist=force_list,
            raise_on_status=True,
            connect=total_retries,
            read=total_retries,
            allowed_methods=methods
        )

        retry_adapter = TimeoutHTTPAdapter(
            post_retry_config=post_retry_config,
            other_retry_config=other_retry_config,
            # Timeout is in seconds.
            timeout=timeout_minutes * 60
        )

        for prefix in ('http://', 'https://'):
            session.mount(prefix, retry_adapter)

        return session

    @staticmethod
    def no_retries(session: requests.Session) -> requests.Session:
        """
        Returns a copy of the given session that will not retry.
        The original session will not be modified.
        """
        # @see https://stackoverflow.com/questions/4794244/how-can-i-create-a-copy-of-an-object-in-python
        copied = copy.deepcopy(session)
        logging.basicConfig(level=logging.DEBUG)
        # NOTE: We often use POST for "READ" operations. Can we retry on those specifically?
        methods = ['HEAD', 'GET', 'OPTIONS', 'TRACE', 'PUT', 'PATCH', 'DELETE']
        no_retries = Retry(
            total=1,
            backoff_factor=0,
            status_forcelist=[],
            connect=1,
            read=1,
            allowed_methods=methods,
        )

        no_retry_adapter = TimeoutHTTPAdapter(post_retry_config=no_retries, other_retry_config=no_retries)

        for prefix in ('http://', 'https://'):
            copied.mount(prefix, no_retry_adapter)

        return copied


def is_aws():
    return os.environ.get('CLOUD_VENDOR') is not None and os.environ.get('CLOUD_VENDOR').upper() == 'AWS'


def format_number(n):
    """Format number as 123, 1.35k, 5.23M, 10.5B, etc."""
    if n < 1000:
        return str(n)
    elif n < 1_000_000:
        return f'{n/1000:.2f}k'.rstrip('0').rstrip('.')
    elif n < 1_000_000_000:
        return f'{n/1_000_000:.2f}M'.rstrip('0').rstrip('.')
    else:
        return f'{n/1_000_000_000:.2f}B'.rstrip('0').rstrip('.')