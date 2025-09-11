import typing as t
from collections.abc import Callable
from enum import Enum
from urllib.parse import urlencode

import httpx
import pydantic

DTO = t.TypeVar("DTO", bound=pydantic.BaseModel)


def create_client_response(
    response: httpx.Response,
    dto: type[DTO],
) -> DTO:
    response.raise_for_status()
    return dto.model_validate(response.json())


class EndpointsBase(str, Enum):
    """Base class for API endpoint enumerations.

    This class combines string and enum functionality to create endpoint definitions
    that can be easily converted to full URLs with query parameters.

    Inherits from both :class:`str` and :class:`Enum` to provide string-like behavior
    while maintaining enumeration semantics for API endpoints.
    """

    ...

    def to_str(
        self,
        params: dict[str, t.Any],
        base_url: str = "",
        normalize: Callable[[t.Any], str] = lambda x: x,
    ) -> str:
        """Convert endpoint to a full URL with query parameters.

        Args:
            params: Dictionary of query parameters to append to the URL.
            base_url: Base URL to prepend to the endpoint path.
            normalize: Function to normalize parameter values before URL encoding.
                      Allows custom formatting of complex objects like datetime.

        Returns:
            Complete URL string with encoded query parameters.

        Example:
            >>> class MyEndpoints(EndpointsBase):
            ...     USERS = "/api/users"
            ...     POSTS = "/api/posts"
            >>> endpoint = MyEndpoints.USERS
            >>> url = endpoint.to_str({"page": 1}, base_url="https://api.example.com")
            >>> print(url)  # https://api.example.com/api/users?page=1
            >>>
            >>> # Using normalize function to format datetime objects
            >>> from datetime import datetime
            >>> url_with_normalize = endpoint.to_str(
            ...     {"created_at": datetime(2023, 1, 1)},
            ...     base_url="https://api.example.com",
            ...     normalize=lambda x: x.isoformat() if hasattr(x, 'isoformat') else str(x)
            ... )
            >>> print(url_with_normalize)  # https://api.example.com/api/users?created_at=2023-01-01T00%3A00%3A00
        """
        return f"{base_url}{self}?{urlencode({key: normalize(value) for key, value in params.items()})}"
