"""Interface for Tracks authentication classes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import aiohttp


class TracksAuthInterface(ABC):
    """Interface for Tracks authentication classes."""

    @abstractmethod
    async def sign_request(
        self, request: aiohttp.ClientRequest, handler: aiohttp.ClientHandlerType
    ) -> aiohttp.ClientResponse:
        """Authenticate the request."""
        ...
