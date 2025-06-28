import logging
import typing as t

import httpx
import pytest
from connector.generated import (
    AuthCredential,
    ListAccounts,
    ListAccountsRequest,
    ListAccountsResponse,
    StandardCapabilityName,
    TokenCredential,
)
from connector.oai.base_clients import BaseIntegrationClient
from connector.oai.capability import Request, get_token_auth
from connector.oai.integration import DescriptionData, Integration
from connector.utils.httpx_auth import BearerAuth
from connector.utils.rate_limiting import (
    RateLimitConfig,
    RateLimitStrategy,
)


@pytest.fixture(autouse=True)
def configure_logging():
    logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def sleep_calls(monkeypatch):
    calls = []

    async def fake_asyncio_sleep(seconds):
        calls.append(seconds)

    monkeypatch.setattr("asyncio.sleep", fake_asyncio_sleep)
    return calls


RATE_LIMIT_CONFIG = RateLimitConfig(
    app_id="test-app",
    requests_per_window=1,
    window_seconds=10,
    strategy=RateLimitStrategy.FIXED,
    max_delay=10 * 1.2,
    maximum_retries=3,
)

integration_mock = Integration(
    app_id="test-app",
    version="1.0.0",
    exception_handlers=[],
    auth=TokenCredential,
    settings_model=None,
    description_data=DescriptionData(
        user_friendly_name="Test App",
        categories=[],
        app_vendor_domain="example.com",
        logo_url="https://example.com/logo.png",
        description="This is a test app for rate limiting.",
    ),
)


class RateLimitingTestClient(BaseIntegrationClient):
    @classmethod
    def prepare_client_args(cls, args: Request) -> dict[str, t.Any]:
        return {
            "auth": BearerAuth(
                token=get_token_auth(args).token,
                token_prefix="",
                auth_header="X-Api-Key",
            ),
            "base_url": "https://example.com",
        }

    async def get_users(self):
        """Simulate a request to get users."""
        response = await self._http_client.get("/users")
        return response


@integration_mock.register_capability(StandardCapabilityName.LIST_ACCOUNTS)
async def list_accounts_test_capability(args: ListAccountsRequest) -> ListAccountsResponse:
    """Testing capabilty"""
    async with RateLimitingTestClient(args, RATE_LIMIT_CONFIG) as client:
        # Simulate a request
        await client.get_users()

        return ListAccountsResponse(
            response=[],
            page=None,
        )


async def test_rate_limiting_waits_and_succeeds(monkeypatch, sleep_calls):
    """
    Test that rate limiter waits for max_delay and then succeeds after rate limit related error.

    This also simulates a scenario where the request is not the first one from the requester.
    """

    # Patch the client's get_users to raise on first call, succeed on second
    call_count = {"count": 0}

    async def counted_response(_, __):
        if call_count["count"] == 0:
            call_count["count"] += 1
            raise Exception("Rate limit exceeded")
        return []

    monkeypatch.setattr("connector.httpx_rewrite.AsyncClient.get", counted_response)

    args = ListAccountsRequest(
        auth=AuthCredential(
            token=TokenCredential(token="test-token"),
        ),
        request=ListAccounts(),
        settings={},
    ).model_dump_json()

    # Should not raise, should wait for max_delay and then succeed
    await integration_mock.dispatch(StandardCapabilityName.LIST_ACCOUNTS, args)

    # Assert we waited for max_delay (10 * 1.2)
    assert any(
        abs(s - 12.0) < 0.01 for s in sleep_calls
    ), f"Expected sleep for 12.0s, got {sleep_calls}"
    # Assert get_users was called twice (once failed, once succeeded)
    assert call_count["count"] == 1


async def test_rate_limiting_waits_and_succeeds_httpx_error(monkeypatch, sleep_calls):
    """
    Test that rate limiter waits for max_delay and then succeeds after httpx 429 error.

    This also simulates a scenario where the request is not the first one from the requester.
    """

    # Patch the client's get_users to raise on first call, succeed on second
    call_count = {"count": 0}

    async def counted_response_httpx(_, __):
        if call_count["count"] == 0:
            call_count["count"] += 1
            raise httpx.HTTPStatusError(
                "Rate limit exceeded",
                request=httpx.Request("GET", "https://example.com/users"),
                response=httpx.Response(429),
            )
        return []

    monkeypatch.setattr("connector.httpx_rewrite.AsyncClient.get", counted_response_httpx)

    args = ListAccountsRequest(
        auth=AuthCredential(
            token=TokenCredential(token="test-token"),
        ),
        request=ListAccounts(),
        settings={},
    ).model_dump_json()

    # Should not raise, should wait for max_delay and then succeed
    await integration_mock.dispatch(StandardCapabilityName.LIST_ACCOUNTS, args)

    # Assert we waited for max_delay (10 * 1.2)
    assert any(
        abs(s - 12.0) < 0.01 for s in sleep_calls
    ), f"Expected sleep for 12.0s, got {sleep_calls}"
    # Assert get_users was called twice (once failed, once succeeded)
    assert call_count["count"] == 1


async def test_rate_limiting_multiple_requests(monkeypatch, sleep_calls):
    """Test that rate limiter waits between multiple requests as per config."""

    # Patch the client's get_users to always succeed and return a dummy user
    async def actual_response(_, __):
        return [{"integration_specific_id": "user", "email": "test@user.com"}]

    monkeypatch.setattr("connector.httpx_rewrite.AsyncClient.get", actual_response)

    args = ListAccountsRequest(
        auth=AuthCredential(
            token=TokenCredential(token="test-token"),
        ),
        request=ListAccounts(),
        settings={},
    )

    # Call the capability multiple times to simulate multiple requests
    async with RateLimitingTestClient(args, RATE_LIMIT_CONFIG) as client:
        for _ in range(3):
            await client.get_users()

    # Since requests_per_window=1 and window_seconds=10, we expect a wait between each request
    # The first call should not wait, but the next two should each wait for window_seconds (10s)
    # So, sleep_calls should have two entries of 10.0 (+/- some small tolerance for sleep())
    waits = [s for s in sleep_calls if abs(s - 10.0) < 0.01]
    assert len(waits) == 2, f"Expected two sleeps of 10s, got {sleep_calls}"


async def test_rate_limiter_maximum_retries(monkeypatch, sleep_calls):
    """Test that the rate limiter raises after exceeding maximum retries."""

    # Patch the client's get_users to always raise a rate limit error
    async def always_rate_limited(_, __):
        raise Exception("Rate limit exceeded")

    monkeypatch.setattr("connector.httpx_rewrite.AsyncClient.get", always_rate_limited)

    args = ListAccountsRequest(
        auth=AuthCredential(
            token=TokenCredential(token="test-token"),
        ),
        request=ListAccounts(),
        settings={},
    )

    # Should raise after maximum retries (3 retries + 1 initial attempt = 4 total attempts)
    with pytest.raises(Exception, match="Maximum retries \\(3\\) reached"):
        async with RateLimitingTestClient(args, RATE_LIMIT_CONFIG) as client:
            await client.get_users()

    # Should have sleep and retry 3 times
    expected_sleeps = [12.0, 12.0, 12.0]
    assert len(sleep_calls) == 3, f"Expected 3 sleep calls, got {len(sleep_calls)}"

    for i, expected_sleep in enumerate(expected_sleeps):
        assert (
            abs(sleep_calls[i] - expected_sleep) < 0.01
        ), f"Expected sleep {i + 1} to be {expected_sleep}s, got {sleep_calls[i]}s"


async def test_batch_request_rate_limiting(monkeypatch, sleep_calls):
    """Test that batch_request method works correctly with rate limiting."""

    # Track request calls to verify order and count
    request_calls = []

    async def mock_get_response(*args, **kwargs):
        # Extract user ID from URL for verification
        url = args[1] if len(args) > 1 else kwargs.get("url", "")
        user_id = url.split("/")[-1]
        request_calls.append(user_id)

        # Simulate different response times and potential rate limiting
        if user_id == "user2":
            # Simulate rate limit error for user2, then succeed on retry
            if len([c for c in request_calls if c == "user2"]) == 1:
                raise Exception("Rate limit exceeded")

        # Create a mock Response object
        response_data = {"id": user_id, "name": f"User {user_id}"}
        mock_response = httpx.Response(200, json=response_data)
        return mock_response

    monkeypatch.setattr("connector.httpx_rewrite.AsyncClient.get", mock_get_response)

    args = ListAccountsRequest(
        auth=AuthCredential(
            token=TokenCredential(token="test-token"),
        ),
        request=ListAccounts(),
        settings={},
    )

    # Create a rate limit config that allows batching
    batch_rate_config = RateLimitConfig(
        app_id="test-batch-app",
        requests_per_window=3,  # Allow 3 requests per window
        window_seconds=5,  # 5 second window
        strategy=RateLimitStrategy.FIXED,
        max_batch_size=2,  # Process 2 requests at a time
        maximum_retries=3,
    )

    async with RateLimitingTestClient(args, batch_rate_config) as client:
        # Test batch request with 4 users
        batch_requests = [
            (("/users/user1",), {}),
            (("/users/user2",), {}),
            (("/users/user3",), {"params": {"include": "profile"}}),
            (("/users/user4",), {}),
        ]

        # Use the new batch_request method directly on the client
        responses = await client.batch_request("get", batch_requests)

    # Verify we got 4 responses
    assert len(responses) == 4, f"Expected 4 responses, got {len(responses)}"

    # Verify request calls (user2 should appear twice due to retry)
    expected_calls = ["user1", "user2", "user2", "user3", "user4"]
    assert request_calls == expected_calls, f"Expected calls {expected_calls}, got {request_calls}"

    # Verify responses are in correct order
    for i, response in enumerate(responses):
        response_data = response.json()
        assert response_data["id"] == f"user{i + 1}", f"Response {i} should be for user{i + 1}"

    # Verify rate limiting was applied (should have waits between batches)
    # With max_batch_size=2, we should have 2 batches, so 1 wait between them
    batch_waits = [s for s in sleep_calls if s > 0]
    assert len(batch_waits) >= 1, f"Expected at least 1 batch wait, got {batch_waits}"

    # Verify rate limit retry for user2
    rate_limit_waits = [s for s in sleep_calls if abs(s - 5.0) < 0.01]  # window_seconds
    assert len(rate_limit_waits) >= 1, f"Expected rate limit retry wait, got {sleep_calls}"


async def test_batch_request_with_default_kwargs(monkeypatch, sleep_calls):
    """Test that batch_request properly merges default kwargs with request-specific kwargs."""

    captured_kwargs = []

    async def mock_post_response(*args, **kwargs):
        captured_kwargs.append(kwargs.copy())
        # Create a mock Response object
        # The first arg is the client instance, the second is the URL
        url = args[1] if len(args) > 1 else kwargs.get("url", "")
        response_data = {"id": url.split("/")[-1], "status": "created"}
        mock_response = httpx.Response(201, json=response_data)
        return mock_response

    monkeypatch.setattr("connector.httpx_rewrite.AsyncClient.post", mock_post_response)

    args = ListAccountsRequest(
        auth=AuthCredential(
            token=TokenCredential(token="test-token"),
        ),
        request=ListAccounts(),
        settings={},
    )

    batch_rate_config = RateLimitConfig(
        app_id="test-batch-kwargs",
        requests_per_window=5,
        window_seconds=1,
        strategy=RateLimitStrategy.FIXED,
        max_batch_size=3,
    )

    async with RateLimitingTestClient(args, batch_rate_config) as client:
        # Test batch request with default headers and request-specific data
        batch_requests = [
            (("/users",), {"json": {"name": "John"}}),
            (("/users",), {"json": {"name": "Jane"}, "timeout": 30}),
            (("/users",), {"json": {"name": "Bob"}}),
        ]
        responses = await client.batch_request(
            "post",
            batch_requests,
            headers={"Content-Type": "application/json", "Authorization": "Bearer test"},
            timeout=10,
        )

    # Verify we got 3 responses
    assert len(responses) == 3, f"Expected 3 responses, got {len(responses)}"

    # Verify kwargs were properly merged
    expected_kwargs = [
        {
            "json": {"name": "John"},
            "headers": {"Content-Type": "application/json", "Authorization": "Bearer test"},
            "timeout": 10,
        },
        {
            "json": {"name": "Jane"},
            "headers": {"Content-Type": "application/json", "Authorization": "Bearer test"},
            "timeout": 30,  # Request-specific timeout should override default
        },
        {
            "json": {"name": "Bob"},
            "headers": {"Content-Type": "application/json", "Authorization": "Bearer test"},
            "timeout": 10,
        },
    ]

    assert (
        captured_kwargs == expected_kwargs
    ), f"Expected kwargs {expected_kwargs}, got {captured_kwargs}"


async def test_batch_request_empty_list(monkeypatch, sleep_calls):
    """Test that batch_request handles empty request list correctly."""

    args = ListAccountsRequest(
        auth=AuthCredential(
            token=TokenCredential(token="test-token"),
        ),
        request=ListAccounts(),
        settings={},
    )

    batch_rate_config = RateLimitConfig(
        app_id="test-batch-empty",
        requests_per_window=5,
        window_seconds=1,
        strategy=RateLimitStrategy.FIXED,
        max_batch_size=3,
    )

    async with RateLimitingTestClient(args, batch_rate_config) as client:
        # Test with empty request list
        responses = await client.batch_request("get", [])

    # Should return empty list
    assert responses == [], f"Expected empty list, got {responses}"

    # Should not have any sleep calls
    assert len(sleep_calls) == 0, f"Expected no sleep calls, got {sleep_calls}"
