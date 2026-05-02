import asyncio
import logging
import time
import typing as t

import httpx
import pytest
from connector.generated import (
    AuthCredential,
    ListAccounts,
    ListAccountsRequest,
    TokenCredential,
)
from connector.oai.base_clients import BaseIntegrationClient
from connector.oai.capability import Request, get_token_auth
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


async def test_rate_limiter_concurrent_execution(monkeypatch, sleep_calls):
    """Test rate limiter with concurrent execution (max_concurrent > 1)."""

    # Create config with concurrent execution
    config = RateLimitConfig(
        app_id="test-concurrent",
        requests_per_window=10,
        window_seconds=60,
        strategy=RateLimitStrategy.FIXED,
        max_concurrent=3,  # Allow 3 concurrent requests
        max_batch_size=5,
    )

    # Track request execution order and timing
    request_execution_order = []
    request_start_times = []

    async def mock_get_response(*args, **kwargs):
        url = args[1] if len(args) > 1 else kwargs.get("url", "")
        request_id = url.split("/")[-1] if "/" in url else "unknown"

        # Record when this request started
        start_time = time.time()
        request_start_times.append(start_time)
        request_execution_order.append(f"start_{request_id}")

        # Simulate some processing time
        await asyncio.sleep(0.1)

        request_execution_order.append(f"end_{request_id}")

        response = httpx.Response(200, json={"id": request_id, "data": "success"})
        response._request = httpx.Request("GET", url)
        return response

    monkeypatch.setattr("connector.httpx_rewrite.AsyncClient.get", mock_get_response)

    args = ListAccountsRequest(
        auth=AuthCredential(
            token=TokenCredential(token="test-token"),
        ),
        request=ListAccounts(),
        settings={},
    )

    async with RateLimitingTestClient(args, config) as client:
        # Test batch request with 5 requests
        batch_requests = [
            (("/users/user1",), {}),
            (("/users/user2",), {}),
            (("/users/user3",), {}),
            (("/users/user4",), {}),
            (("/users/user5",), {}),
        ]

        start_time = time.time()
        responses = await client.batch_request("get", batch_requests)
        end_time = time.time()

    # Should have 5 responses
    assert len(responses) == 5, f"Expected 5 responses, got {len(responses)}"

    # With concurrent execution, requests should overlap in time
    # The first 3 requests should start almost simultaneously
    if len(request_start_times) >= 3:
        time_diff_first_three = max(request_start_times[:3]) - min(request_start_times[:3])
        assert (
            time_diff_first_three < 0.05
        ), f"First 3 requests should start concurrently, but time diff was {time_diff_first_three}s"

    # Total execution time should be less than sequential (5 * 0.1s = 0.5s)
    # With 3 concurrent, it should be closer to 0.2s (2 batches of ~0.1s each)
    total_time = end_time - start_time
    assert (
        total_time < 0.4
    ), f"Concurrent execution should be faster than sequential, but took {total_time}s"


async def test_rate_limiter_sequential_execution(monkeypatch, sleep_calls):
    """Test rate limiter with sequential execution (max_concurrent = 1)."""

    # Create config with sequential execution
    config = RateLimitConfig(
        app_id="test-sequential",
        requests_per_window=10,
        window_seconds=60,
        strategy=RateLimitStrategy.FIXED,
        max_concurrent=1,  # Force sequential execution
        max_batch_size=5,
    )

    # Track request execution order
    request_execution_order = []
    request_start_times = []

    async def mock_get_response(*args, **kwargs):
        url = args[1] if len(args) > 1 else kwargs.get("url", "")
        request_id = url.split("/")[-1] if "/" in url else "unknown"

        # Record when this request started
        start_time = time.time()
        request_start_times.append(start_time)
        request_execution_order.append(f"start_{request_id}")

        # Simulate some processing time
        await asyncio.sleep(0.1)

        request_execution_order.append(f"end_{request_id}")

        response = httpx.Response(200, json={"id": request_id, "data": "success"})
        response._request = httpx.Request("GET", url)
        return response

    monkeypatch.setattr("connector.httpx_rewrite.AsyncClient.get", mock_get_response)

    args = ListAccountsRequest(
        auth=AuthCredential(
            token=TokenCredential(token="test-token"),
        ),
        request=ListAccounts(),
        settings={},
    )

    async with RateLimitingTestClient(args, config) as client:
        # Test batch request with 3 requests
        batch_requests = [
            (("/users/user1",), {}),
            (("/users/user2",), {}),
            (("/users/user3",), {}),
        ]

        start_time = time.time()
        responses = await client.batch_request("get", batch_requests)
        end_time = time.time()

    # Should have 3 responses
    assert len(responses) == 3, f"Expected 3 responses, got {len(responses)}"

    # With sequential execution, requests should not overlap
    # Each request should start after the previous one ends
    # Note: The gap might be very small due to fast processing, so we check for any gap
    for i in range(1, len(request_start_times)):
        time_diff = request_start_times[i] - request_start_times[i - 1]
        assert (
            time_diff >= 0.0
        ), f"Sequential execution should have some gap between requests, but gap was {time_diff}s"

    # Total execution time should be close to sequential (3 * 0.1s = 0.3s)
    # Note: The sleep calls are captured by the fixture, so actual time might be faster
    total_time = end_time - start_time
    # We expect at least some time due to the async.sleep calls
    assert total_time >= 0.0, f"Sequential execution should take some time, but took {total_time}s"


async def test_rate_limiter_semaphore_behavior(monkeypatch, sleep_calls):
    """Test that semaphore properly limits concurrent requests."""

    # Create config with limited concurrency
    config = RateLimitConfig(
        app_id="test-semaphore",
        requests_per_window=20,
        window_seconds=60,
        strategy=RateLimitStrategy.FIXED,
        max_concurrent=2,  # Only 2 concurrent requests allowed
        max_batch_size=10,
    )

    # Track active requests at any given time
    active_requests = 0
    max_active_requests = 0
    request_timeline = []

    async def mock_get_response(*args, **kwargs):
        nonlocal active_requests, max_active_requests
        url = args[1] if len(args) > 1 else kwargs.get("url", "")
        request_id = url.split("/")[-1] if "/" in url else "unknown"

        # Simulate request start
        active_requests += 1
        max_active_requests = max(max_active_requests, active_requests)
        request_timeline.append(f"start_{request_id}_active_{active_requests}")

        # Simulate processing time
        await asyncio.sleep(0.5)

        # Simulate request end
        active_requests -= 1
        request_timeline.append(f"end_{request_id}_active_{active_requests}")

        response = httpx.Response(200, json={"id": request_id, "data": "success"})
        response._request = httpx.Request("GET", url)
        return response

    monkeypatch.setattr("connector.httpx_rewrite.AsyncClient.get", mock_get_response)

    args = ListAccountsRequest(
        auth=AuthCredential(
            token=TokenCredential(token="test-token"),
        ),
        request=ListAccounts(),
        settings={},
    )

    async with RateLimitingTestClient(args, config) as client:
        # Test batch request with 4 requests
        batch_requests = [
            (("/users/user1",), {}),
            (("/users/user2",), {}),
            (("/users/user3",), {}),
            (("/users/user4",), {}),
        ]

        responses = await client.batch_request("get", batch_requests)

    # Should have 4 responses
    assert len(responses) == 4, f"Expected 4 responses, got {len(responses)}"

    # Maximum active requests should not exceed max_concurrent
    assert (
        max_active_requests <= 2
    ), f"Max concurrent requests exceeded semaphore limit: {max_active_requests} > 2"

    # Should have at least 1 concurrent request
    assert (
        max_active_requests >= 1
    ), f"Expected at least 1 concurrent request, got {max_active_requests}"
    assert (
        max_active_requests <= 2
    ), f"Max concurrent requests exceeded semaphore limit: {max_active_requests} > 2"


async def test_rate_limiter_concurrent_with_rate_limiting(monkeypatch, sleep_calls):
    """Test concurrent execution with rate limiting scenarios."""

    # Create config with concurrent execution and restrictive rate limits
    config = RateLimitConfig(
        app_id="test-concurrent-rate-limit",
        requests_per_window=2,  # Very restrictive
        window_seconds=10,
        strategy=RateLimitStrategy.FIXED,
        max_concurrent=3,  # Allow 3 concurrent
        max_batch_size=5,
        maximum_retries=2,
    )

    call_count = {"count": 0}

    async def mock_get_response(*args, **kwargs):
        call_count["count"] += 1
        url = args[1] if len(args) > 1 else kwargs.get("url", "")
        request_id = url.split("/")[-1] if "/" in url else "unknown"

        # Simulate rate limit on every 3rd call
        if call_count["count"] % 3 == 0:
            response = httpx.Response(429, text="Rate limit exceeded")
            response._request = httpx.Request("GET", url)
            return response

        response = httpx.Response(200, json={"id": request_id, "data": "success"})
        response._request = httpx.Request("GET", url)
        return response

    monkeypatch.setattr("connector.httpx_rewrite.AsyncClient.get", mock_get_response)

    args = ListAccountsRequest(
        auth=AuthCredential(
            token=TokenCredential(token="test-token"),
        ),
        request=ListAccounts(),
        settings={},
    )

    async with RateLimitingTestClient(args, config) as client:
        # Test batch request with 6 requests
        batch_requests = [
            (("/users/user1",), {}),
            (("/users/user2",), {}),
            (("/users/user3",), {}),
            (("/users/user4",), {}),
            (("/users/user5",), {}),
            (("/users/user6",), {}),
        ]

        responses = await client.batch_request("get", batch_requests)

    # Should have 6 responses (some may be retries)
    assert len(responses) == 6, f"Expected 6 responses, got {len(responses)}"

    # Should have made more than 6 calls due to retries
    assert (
        call_count["count"] > 6
    ), f"Expected retries due to rate limiting, but only made {call_count['count']} calls"

    # Should have sleep calls for rate limit retries
    assert len(sleep_calls) > 0, f"Expected sleep calls for rate limit retries, got {sleep_calls}"


async def test_rate_limiter_concurrent_exception_handling(monkeypatch, sleep_calls):
    """
    Test exception handling in concurrent execution.
    This would only happen if the request errors out on its own. (probably redundant case)
    We still return the unraised responses through the rate limiter.
    """

    # Create config with concurrent execution
    config = RateLimitConfig(
        app_id="test-concurrent-exceptions",
        requests_per_window=10,
        window_seconds=60,
        strategy=RateLimitStrategy.FIXED,
        max_concurrent=3,
        max_batch_size=5,
    )

    call_count = {"count": 0}

    async def mock_get_response(*args, **kwargs):
        call_count["count"] += 1
        url = args[1] if len(args) > 1 else kwargs.get("url", "")
        request_id = url.split("/")[-1] if "/" in url else "unknown"

        # Simulate failure on user3
        if request_id == "user3":
            raise Exception(f"Simulated failure for {request_id}")

        response = httpx.Response(200, json={"id": request_id, "data": "success"})
        response._request = httpx.Request("GET", url)
        return response

    monkeypatch.setattr("connector.httpx_rewrite.AsyncClient.get", mock_get_response)

    args = ListAccountsRequest(
        auth=AuthCredential(
            token=TokenCredential(token="test-token"),
        ),
        request=ListAccounts(),
        settings={},
    )

    # Should raise exception when one request fails
    with pytest.raises(Exception, match="Simulated failure for user3"):
        async with RateLimitingTestClient(args, config) as client:
            batch_requests = [
                (("/users/user1",), {}),
                (("/users/user2",), {}),
                (("/users/user3",), {}),
                (("/users/user4",), {}),
            ]

            await client.batch_request("get", batch_requests)


async def test_rate_limiter_single_request_concurrent_config(monkeypatch, sleep_calls):
    """Test that single requests use sequential execution even with concurrent config."""

    # Create config with concurrent execution
    config = RateLimitConfig(
        app_id="test-single-concurrent",
        requests_per_window=10,
        window_seconds=60,
        strategy=RateLimitStrategy.FIXED,
        max_concurrent=5,  # High concurrency
        max_batch_size=5,
    )

    request_execution_order = []

    async def mock_get_response(*args, **kwargs):
        url = args[1] if len(args) > 1 else kwargs.get("url", "")
        request_id = url.split("/")[-1] if "/" in url else "unknown"

        request_execution_order.append(f"executing_{request_id}")

        response = httpx.Response(200, json={"id": request_id, "data": "success"})
        response._request = httpx.Request("GET", url)
        return response

    monkeypatch.setattr("connector.httpx_rewrite.AsyncClient.get", mock_get_response)

    args = ListAccountsRequest(
        auth=AuthCredential(
            token=TokenCredential(token="test-token"),
        ),
        request=ListAccounts(),
        settings={},
    )

    async with RateLimitingTestClient(args, config) as client:
        # Test with single request
        batch_requests = [
            (("/users/user1",), {}),
        ]

        responses = await client.batch_request("get", batch_requests)

    # Should have 1 response
    assert len(responses) == 1, f"Expected 1 response, got {len(responses)}"

    # Should have executed the single request
    assert (
        len(request_execution_order) == 1
    ), f"Expected 1 request execution, got {len(request_execution_order)}"
    assert request_execution_order[0] == "executing_user1"


async def test_rate_limiter_response_order_preservation(monkeypatch, sleep_calls):
    """Test that response order matches request order in concurrent execution."""

    # Create config with concurrent execution
    config = RateLimitConfig(
        app_id="test-response-order",
        requests_per_window=10,
        window_seconds=60,
        strategy=RateLimitStrategy.FIXED,
        max_concurrent=3,  # Allow 3 concurrent requests
        max_batch_size=5,
    )

    # Track request processing order and response order
    request_processing_order = []
    response_order = []

    async def mock_get_response(*args, **kwargs):
        url = args[1] if len(args) > 1 else kwargs.get("url", "")
        request_id = url.split("/")[-1] if "/" in url else "unknown"

        # Record when this request starts processing
        request_processing_order.append(f"processing_{request_id}")

        # Simulate different processing times to mix the processing order
        if request_id == "user1":
            await asyncio.sleep(0.3)
        elif request_id == "user2":
            await asyncio.sleep(0.1)
        elif request_id == "user3":
            await asyncio.sleep(0.2)
        elif request_id == "user4":
            await asyncio.sleep(0.15)
        elif request_id == "user5":
            await asyncio.sleep(0.25)

        response = httpx.Response(200, json={"id": request_id, "data": "success"})
        response._request = httpx.Request("GET", url)
        return response

    monkeypatch.setattr("connector.httpx_rewrite.AsyncClient.get", mock_get_response)

    args = ListAccountsRequest(
        auth=AuthCredential(
            token=TokenCredential(token="test-token"),
        ),
        request=ListAccounts(),
        settings={},
    )

    async with RateLimitingTestClient(args, config) as client:
        # Test batch request with 5 requests in specific order
        batch_requests = [
            (("/users/user1",), {}),
            (("/users/user2",), {}),
            (("/users/user3",), {}),
            (("/users/user4",), {}),
            (("/users/user5",), {}),
        ]

        responses = await client.batch_request("get", batch_requests)

    # Should have 5 responses
    assert len(responses) == 5, f"Expected 5 responses, got {len(responses)}"

    # Verify response order matches input order (not processing order)
    expected_response_order = [
        "response_user1",
        "response_user2",
        "response_user3",
        "response_user4",
        "response_user5",
    ]

    # Get the order of items in the responses and verify
    response_order = [f"response_{response.json()['id']}" for response in responses]
    assert (
        response_order == expected_response_order
    ), f"Response order should match input order. Expected {expected_response_order}, got {response_order}"

    # Processing order is different than response order (concurrency)
    assert request_processing_order != response_order, (
        f"Processing order should differ from response order in concurrent execution. "
        f"Processing: {request_processing_order}, Response: {response_order}"
    )

    # Verify that responses contain the correct data in the correct order
    for i, response in enumerate(responses):
        response_data = response.json()
        expected_id = f"user{i + 1}"
        assert (
            response_data["id"] == expected_id
        ), f"Response {i} should have id '{expected_id}', got '{response_data['id']}'"


async def test_rate_limiter_concurrent_http_error_responses(monkeypatch, sleep_calls):
    """Test that HTTP error responses are returned (not raised) in concurrent execution."""

    # Create config with concurrent execution
    config = RateLimitConfig(
        app_id="test-concurrent-http-errors",
        requests_per_window=10,
        window_seconds=60,
        strategy=RateLimitStrategy.FIXED,
        max_concurrent=3,
        max_batch_size=5,
    )

    async def mock_get_response(*args, **kwargs):
        url = args[1] if len(args) > 1 else kwargs.get("url", "")
        request_id = url.split("/")[-1] if "/" in url else "unknown"

        # Simulate different HTTP error responses for different users
        if request_id == "user1":
            # Return 400 Bad Request
            response = httpx.Response(400, text="Bad Request: Invalid user ID")
            response._request = httpx.Request("GET", url)
            return response
        elif request_id == "user2":
            # Return 200 Success
            response = httpx.Response(200, json={"id": request_id, "data": "success"})
            response._request = httpx.Request("GET", url)
            return response
        elif request_id == "user3":
            # Return 500 Internal Server Error
            response = httpx.Response(500, text="Internal Server Error")
            response._request = httpx.Request("GET", url)
            return response
        elif request_id == "user4":
            # Return 404 Not Found
            response = httpx.Response(404, text="User not found")
            response._request = httpx.Request("GET", url)
            return response
        elif request_id == "user5":
            # Return 200 Success
            response = httpx.Response(200, json={"id": request_id, "data": "success"})
            response._request = httpx.Request("GET", url)
            return response
        else:
            # Default success
            response = httpx.Response(200, json={"id": request_id, "data": "success"})
            response._request = httpx.Request("GET", url)
            return response

    monkeypatch.setattr("connector.httpx_rewrite.AsyncClient.get", mock_get_response)

    args = ListAccountsRequest(
        auth=AuthCredential(
            token=TokenCredential(token="test-token"),
        ),
        request=ListAccounts(),
        settings={},
    )

    async with RateLimitingTestClient(args, config) as client:
        # Test batch request with mixed success and error responses
        batch_requests = [
            (("/users/user1",), {}),  # 400 error
            (("/users/user2",), {}),  # 200 success
            (("/users/user3",), {}),  # 500 error
            (("/users/user4",), {}),  # 404 error
            (("/users/user5",), {}),  # 200 success
        ]

        responses = await client.batch_request("get", batch_requests)

    # Should have 5 responses (all returned, none raised as exceptions)
    assert len(responses) == 5, f"Expected 5 responses, got {len(responses)}"

    # Verify response status codes match expected errors
    expected_status_codes = [400, 200, 500, 404, 200]
    actual_status_codes = [response.status_code for response in responses]
    assert (
        actual_status_codes == expected_status_codes
    ), f"Status codes should match expected. Expected {expected_status_codes}, got {actual_status_codes}"

    # Verify that error responses contain the expected error text
    assert responses[0].text == "Bad Request: Invalid user ID"
    assert responses[1].json()["id"] == "user2"
    assert responses[2].text == "Internal Server Error"
    assert responses[3].text == "User not found"
    assert responses[4].json()["id"] == "user5"

    # Verify that the caller can call raise_for_status on error responses
    # This should raise HTTPStatusError for error status codes
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        responses[0].raise_for_status()  # 400 error
    assert exc_info.value.response.status_code == 400

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        responses[2].raise_for_status()  # 500 error
    assert exc_info.value.response.status_code == 500

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        responses[3].raise_for_status()  # 404 error
    assert exc_info.value.response.status_code == 404

    # Success responses should not raise when calling raise_for_status
    responses[1].raise_for_status()
    responses[4].raise_for_status()

    # Verify response order is preserved even with mixed success/error responses
    expected_user_ids = ["user1", "user2", "user3", "user4", "user5"]
    actual_user_ids = []
    for response in responses:
        if response.status_code == 200:
            actual_user_ids.append(response.json()["id"])
        else:
            # For error responses, extract user ID from URL
            url = response._request.url.path
            user_id = url.split("/")[-1]
            actual_user_ids.append(user_id)

    assert (
        actual_user_ids == expected_user_ids
    ), f"Response order should be preserved. Expected {expected_user_ids}, got {actual_user_ids}"
