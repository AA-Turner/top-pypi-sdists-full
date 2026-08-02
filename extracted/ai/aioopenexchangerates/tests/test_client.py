"""Test the client."""

from collections.abc import Callable
from unittest.mock import patch

from aiohttp import ClientConnectionError, ClientPayloadError, ClientSession
from aioresponses import aioresponses
import pytest

from aioopenexchangerates.client import Client
from aioopenexchangerates.exceptions import (
    OpenExchangeRatesAuthError,
    OpenExchangeRatesClientError,
    OpenExchangeRatesRateLimitError,
)


@pytest.mark.parametrize(
    ("status", "error", "message"),
    [
        (401, OpenExchangeRatesAuthError, "Unauthorized"),
        (403, OpenExchangeRatesAuthError, "Forbidden"),
        (429, OpenExchangeRatesRateLimitError, "Too Many Requests"),
        (400, OpenExchangeRatesClientError, "Bad Request"),
        (500, OpenExchangeRatesClientError, "Internal Server Error"),
    ],
)
async def test_response_error(
    client: Client,
    mock_response: aioresponses,
    generate_url: Callable[..., str],
    status: int,
    error: type[Exception],
    message: str,
) -> None:
    """Test get_latest."""
    mock_response.get(
        generate_url("latest.json", app_id=client.api_key, base="USD"),
        status=status,
    )

    with pytest.raises(error) as err:
        await client.get_latest()

    assert str(err.value) == message


@pytest.mark.parametrize(
    ("aiohttp_error", "error", "message"),
    [
        (
            ClientConnectionError("Boom"),
            OpenExchangeRatesClientError,
            "Unknown error: Boom",
        ),
        (
            ClientPayloadError("Bad payload"),
            OpenExchangeRatesClientError,
            "Unknown error: Bad payload",
        ),
    ],
)
async def test_client_error(
    session: ClientSession,
    client: Client,
    aiohttp_error: Exception,
    error: type[Exception],
    message: str,
) -> None:
    """Test get_latest."""
    with (
        patch.object(session, "get", side_effect=aiohttp_error),
        pytest.raises(
            error,
        ) as err,
    ):
        await client.get_latest()

    assert str(err.value) == message
