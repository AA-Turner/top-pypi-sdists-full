"""Tracks IAM authentication middleware."""

from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from fluidattacks_tracks.auth.base import TracksAuthInterface

if TYPE_CHECKING:
    import aiohttp

try:
    import aiobotocore.session
    from botocore.auth import SigV4Auth
    from botocore.awsrequest import AWSRequest
except ImportError as exception:
    message = "To use TracksIAMAuth, please install fluidattacks-tracks[auth]"
    raise RuntimeError(message) from exception


class TracksIAMAuth(TracksAuthInterface):
    """Tracks IAM authentication."""

    def __init__(self) -> None:
        """Initialize the Tracks IAM authentication."""
        self.session = aiobotocore.session.get_session()

    async def sign_request(
        self, request: aiohttp.ClientRequest, handler: aiohttp.ClientHandlerType
    ) -> aiohttp.ClientResponse:
        """Authenticate the request."""
        parsed = urlparse(str(request.url))
        # yarl (aiohttp' underlying URL parser) doesn't encode : but AWS expects it.
        query = urlencode(parse_qsl(parsed.query), safe="")  # type: ignore[misc]
        url = urlunparse(parsed._replace(query=query))
        credentials = await self.session.get_credentials()
        if credentials:
            # Must be frozen to avoid SigV4Auth from triggering a blocking refresh call.
            frozen_credentials = await credentials.get_frozen_credentials()
            aws_request = AWSRequest(method=request.method, url=url)
            SigV4Auth(frozen_credentials, "execute-api", "us-east-1").add_auth(aws_request)
            headers = dict(aws_request.headers.items())
            request.headers.update(headers)
        return await handler(request)
