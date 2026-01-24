from contextlib import contextmanager
from ssl import SSLContext
from threading import local
from typing import Any, Dict, Iterator, Optional, Union
from urllib.parse import urljoin

from httpx import AsyncClient, Client, HTTPError, Response, Timeout
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, SecretStr

from galileo_core.constants.http_headers import HttpHeaders
from galileo_core.constants.request_method import RequestMethod
from galileo_core.exceptions.http import GalileoHTTPException
from galileo_core.helpers.execution import async_run
from galileo_core.helpers.logger import logger

DEFAULT_TIMEOUT_SECONDS = 60.0


class ApiClient(BaseModel):
    host: HttpUrl
    jwt_token: SecretStr
    # Used by the openapi generated resources
    raise_on_unexpected_status: bool = False
    ssl_context: Union[SSLContext, bool] = True
    # Thread-local storage for AsyncClient instances
    thread_local: local = Field(default_factory=local, exclude=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def async_client(self) -> AsyncClient:
        """Get or create an AsyncClient for the current thread."""
        if not hasattr(self.thread_local, "client"):
            self.thread_local.client = AsyncClient(
                base_url=self.host.unicode_string(),
                verify=self.ssl_context,
                timeout=Timeout(DEFAULT_TIMEOUT_SECONDS, connect=5.0),
            )
        return self.thread_local.client

    @property
    def sync_client(self) -> Client:
        """Get or create a synchronous Client for the current thread."""
        if not hasattr(self.thread_local, "sync_client"):
            self.thread_local.sync_client = Client(
                base_url=self.host.unicode_string(),
                verify=self.ssl_context,
                timeout=Timeout(DEFAULT_TIMEOUT_SECONDS, connect=5.0),
            )
        return self.thread_local.sync_client

    @property
    def auth_header(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.jwt_token.get_secret_value()}"}

    @staticmethod
    def validate_response(response: Response, raise_on_error: bool = True) -> None:
        for header, value in response.headers.items():
            # Log all Galileo headers. These are headers that start with `Galileo-Request-`.
            # These can be in any case, so we lower-case them for comparison.
            if header.lower().startswith("galileo-request-"):
                logger.debug(f"{header.title()}: {value}.")
        if raise_on_error:
            try:
                response.raise_for_status()
            except HTTPError:
                raise GalileoHTTPException(
                    f"Galileo API returned HTTP status code {response.status_code}. Error was: {response.text}",
                    response.status_code,
                    response.text,
                )

    @staticmethod
    async def make_request(
        request_method: RequestMethod,
        base_url: str,
        endpoint: str,
        ssl_context: Union[SSLContext, bool] = True,
        read_timeout: float = DEFAULT_TIMEOUT_SECONDS,
        return_raw_response: bool = False,
        async_client: Optional[AsyncClient] = None,
        **kwargs: Any,
    ) -> Any:
        url = urljoin(base_url, endpoint)
        logger.debug(f"Making request to {url}.")
        local_client = False
        if async_client is None:
            # Create a new AsyncClient instance.
            logger.debug("Creating new AsyncClient instance for this request.")
            async_client = AsyncClient(
                base_url=base_url, timeout=Timeout(read_timeout, connect=5.0), verify=ssl_context
            )
            local_client = True

        response = await async_client.request(
            method=request_method.value,
            url=url,
            timeout=Timeout(read_timeout, connect=5.0),
            **kwargs,
        )
        # Skip validation when return_raw_response=True, as the caller will handle the response
        ApiClient.validate_response(response, raise_on_error=not return_raw_response)
        logger.debug(f"Response was received from {url}.")

        if local_client:
            await async_client.aclose()
            logger.debug("Closed AsyncClient instance.")

        # If the caller asked for the raw Response object, just return it.
        if return_raw_response:
            return response

        # Some successful responses (e.g. HTTP 204 No Content) legitimately have no body.
        # Attempting to call `response.json()` in these cases raises a JSONDecodeError.
        # We treat 204 responses or any response with an empty body as having no payload
        # and return `None` to the caller.
        if response.status_code == 204 or not response.content:
            return None

        # Otherwise attempt to parse the response as JSON. If this fails, fall back to
        # returning the raw text content so the caller still receives the payload.
        try:
            return response.json()
        except ValueError:
            return response.text

    @contextmanager
    def stream_request(
        self,
        method: RequestMethod,
        path: str,
        content_headers: Dict[str, str] = HttpHeaders.json(),
        read_timeout: float = DEFAULT_TIMEOUT_SECONDS,
        **kwargs: Any,
    ) -> Iterator[Response]:
        kwargs.pop("return_raw_response", None)
        headers = {**content_headers, **self.auth_header}
        url = urljoin(self.host.unicode_string(), path)
        logger.debug(f"Streaming request to {url}.")

        with self.sync_client.stream(
            method=method.value,
            url=url,
            headers=headers,
            timeout=Timeout(read_timeout, connect=5.0),
            **kwargs,
        ) as response:
            ApiClient.validate_response(response)
            yield response

    def request(
        self,
        method: RequestMethod,
        path: str,
        content_headers: Dict[str, str] = HttpHeaders.json(),
        **kwargs: Any,
    ) -> Any:
        return async_run(self.arequest(method=method, path=path, content_headers=content_headers, **kwargs))

    async def arequest(
        self,
        method: RequestMethod,
        path: str,
        content_headers: Dict[str, str] = HttpHeaders.json(),
        **kwargs: Any,
    ) -> Any:
        return await ApiClient.make_request(
            request_method=method,
            base_url=self.host.unicode_string(),
            endpoint=path,
            headers={**content_headers, **self.auth_header},
            ssl_context=self.ssl_context,
            async_client=self.async_client,
            **kwargs,
        )
