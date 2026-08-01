import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Dict, Optional

import requests
import requests.adapters
import urllib3

from abstra_internals.environment import MAX_HTTP_CLIENT_THREADS, REQUEST_TIMEOUT
from abstra_internals.logger import AbstraLogger

AbstraHTTPResponse = requests.Response


class HTTPClient:
    def __init__(
        self,
        base_url: str,
        base_headers: Optional[Dict[str, str]] = None,
        base_headers_resolver: Optional[Callable[[], Dict[str, str]]] = None,
        on_unauthorized: Optional[Callable[[Optional[str]], bool]] = None,
    ) -> None:
        if base_headers and base_headers_resolver:
            raise ValueError(
                "You cannot provide both base_headers and base_headers_resolver."
            )

        self.base_url = base_url
        self._base_headers = base_headers
        self._base_headers_resolver = base_headers_resolver
        self._on_unauthorized = on_unauthorized
        self.retry_strategy = urllib3.Retry(
            total=5,
            backoff_factor=2,
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        )
        self.timeout = REQUEST_TIMEOUT
        self.pool = ThreadPoolExecutor(
            max_workers=MAX_HTTP_CLIENT_THREADS,
            thread_name_prefix="HTTPClient",
        )
        self._local = threading.local()

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        if hasattr(self, "pool"):
            self.pool.shutdown(wait=False)
        if hasattr(self, "_local") and hasattr(self._local, "session"):
            self._local.session.close()

    @property
    def base_headers(self) -> Dict[str, str]:
        if callable(self._base_headers_resolver):
            return self._base_headers_resolver()
        return self._base_headers or {}

    @property
    def session(self) -> requests.Session:
        if not hasattr(self._local, "session"):
            self._local.session = requests.Session()
            adapter = requests.adapters.HTTPAdapter(max_retries=self.retry_strategy)
            self._local.session.mount("http://", adapter)
            self._local.session.mount("https://", adapter)
        return self._local.session

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Internal request handler.

        Args:
            method (str): HTTP method (e.g., 'GET', 'POST').
            endpoint (str): The URL endpoint to append to the base URL.
            **kwargs: Additional arguments passed to the requests method.

        Returns:
            requests.Response: The response object.
        """
        kwargs.setdefault("timeout", self.timeout)
        kwargs["headers"] = {**self.base_headers, **kwargs.get("headers", {})}

        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        # What this request actually authenticated with. The hook needs it to tell
        # a credential that is still current from one that was already replaced
        # while this request was in flight — in the second case there is nothing
        # to repair and the request just has to be replayed.
        sent_credential = kwargs["headers"].get("Api-Authorization")

        response = self.session.request(method, url, **kwargs)

        # Every caller of this client authenticates with the same credentials, so
        # a 401 anywhere is a signal about them and not about the endpoint. The
        # hook decides whether they are actually dead and, when it can, replaces
        # them; it returns whether that happened, and only then is the request
        # worth repeating. A 401 means cloud-api rejected the caller before doing
        # any work, so replaying is safe for any method.
        if response.status_code == 401 and self._on_unauthorized is not None:
            try:
                recovered = self._on_unauthorized(sent_credential)
            except Exception as e:
                AbstraLogger.capture_exception(e)
                recovered = False

            if recovered:
                # Callers that resolved the credential themselves passed the dead
                # one in their own headers, and those win the merge above — so the
                # retry has to overwrite it rather than just re-merge, or it would
                # present the same rejected token again.
                kwargs["headers"] = {**kwargs["headers"], **self.base_headers}
                response = self.session.request(method, url, **kwargs)

        return response

    def async_post(self, endpoint: str, **kwargs) -> None:
        """
        Sends a request in the background using a thread pool.

        Args:
            endpoint (str): The URL endpoint to append to the base URL.
            **kwargs: Additional arguments passed to the requests method.
        """

        def post(**i_kwargs):
            try:
                res = self.post(endpoint, **i_kwargs)
                res.raise_for_status()
            except Exception as e:
                AbstraLogger.error(f"Error in async_post: {str(e)}")

        self.pool.submit(post, **kwargs)

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """Sends a GET request."""
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """Sends a POST request."""
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """Sends a PUT request."""
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Sends a DELETE request."""
        return self.request("DELETE", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        """Sends a PATCH request."""
        return self.request("PATCH", endpoint, **kwargs)
