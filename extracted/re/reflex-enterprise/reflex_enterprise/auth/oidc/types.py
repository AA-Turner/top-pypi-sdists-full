"""Type definitions for OIDC authentication in Reflex Enterprise."""

from types import TracebackType
from typing import Any, Callable, Mapping, Protocol, TypedDict


class OIDCUserInfo(TypedDict, total=False):
    """Type describing user info obtained from an OIDC provider.

    Attributes:
        sub: The unique identifier for the user.
    """

    sub: str


class AsyncHTTPResponse(Protocol):
    """Protocol for HTTP response used in OIDCAuthState."""

    status: int

    async def json(self) -> Any:
        """Parse and return the JSON content of the HTTP response."""
        ...

    async def text(self) -> str:
        """Return the text content of the HTTP response."""
        ...


def is_ok(response: AsyncHTTPResponse) -> bool:
    """Determine if the HTTP response was successful (status code 2xx)."""
    return 200 <= response.status < 300


class AsyncHTTPResponseContext(Protocol):
    """Protocol for HTTP response used in OIDCAuthState."""

    async def __aenter__(self) -> AsyncHTTPResponse:
        """Enter the asynchronous context manager."""
        ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Exit the asynchronous context manager."""
        ...


class AsyncHTTPClientProtocol(Protocol):
    """Protocol for HTTP client used in OIDCAuthState."""

    def get(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
    ) -> AsyncHTTPResponseContext:
        """Perform an asynchronous HTTP GET request.

        Args:
            url: The URL to send the GET request to.
            headers: Optional HTTP headers to include in the request.
            data: Optional data to include in the request body (for POST requests).

        Returns:
            An AsyncHTTPResponse object representing the HTTP response.
        """
        ...

    def post(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        data: Any = None,
    ) -> AsyncHTTPResponseContext:
        """Perform an asynchronous HTTP POST request.

        Args:
            url: The URL to send the POST request to.
            headers: Optional HTTP headers to include in the request.
            data: Optional data to include in the request body.

        Returns:
            An AsyncHTTPResponse object representing the HTTP response.
        """
        ...


AsyncHTTPClientGetter = Callable[[], AsyncHTTPClientProtocol]
