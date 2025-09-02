"""Tracks IAM authentication middleware."""

from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

if TYPE_CHECKING:
    import aiohttp
    from aiobotocore.credentials import AioCredentials


class TracksIAMAuth:
    """Tracks IAM authentication."""

    def __init__(self, credentials: AioCredentials | None) -> None:
        """Initialize the Tracks IAM authentication."""
        self.credentials = credentials

    async def sign_request(
        self, request: aiohttp.ClientRequest, handler: aiohttp.ClientHandlerType
    ) -> aiohttp.ClientResponse:
        """Authenticate the request."""
        try:
            from botocore.auth import SigV4Auth  # noqa: PLC0415
            from botocore.awsrequest import AWSRequest  # noqa: PLC0415
        except ImportError as exception:
            message = "botocore not found, please install fluidattacks-tracks[auth]"
            raise RuntimeError(message) from exception

        parsed = urlparse(str(request.url))
        # yarl (aiohttp' underlying URL parser) doesn't encode : but AWS expects it.
        query = urlencode(parse_qsl(parsed.query), safe="")  # type: ignore[misc]
        url = urlunparse(parsed._replace(query=query))
        if self.credentials:
            # Must be frozen to avoid SigV4Auth from triggering a blocking refresh call.
            frozen_credentials = await self.credentials.get_frozen_credentials()
            aws_request = AWSRequest(method=request.method, url=url)
            SigV4Auth(frozen_credentials, "execute-api", "us-east-1").add_auth(aws_request)
            headers = dict(aws_request.headers.items())
            request.headers.update(headers)
        return await handler(request)
