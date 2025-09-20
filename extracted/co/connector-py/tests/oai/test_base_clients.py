import logging
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from connector.generated import (
    AuthCredential,
    ListAccounts,
    ListAccountsRequest,
    TokenCredential,
)
from connector.oai.base_clients import (
    BaseIntegrationClient,
    BatchRequest,
    BatchRequests,
    RateLimitedClient,
)
from connector.oai.capability import Request, get_token_auth
from connector.oai.errors import ConnectorError
from connector.utils.httpx_auth import BearerAuth
from connector.utils.rate_limiting import RateLimitConfig, RateLimitStrategy


@pytest.fixture(autouse=True)
def configure_logging():
    logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def mock_async_client():
    """Create a mock AsyncClient for testing."""
    client = AsyncMock(spec=httpx.AsyncClient)
    return client


@pytest.fixture
def rate_limit_config():
    """Create a test rate limit configuration."""
    return RateLimitConfig(
        app_id="test-app",
        requests_per_window=10,
        window_seconds=60,
        strategy=RateLimitStrategy.FIXED,
        max_batch_size=5,
        maximum_retries=3,
    )


@pytest.fixture
def sample_request():
    """Create a sample request for testing."""
    return ListAccountsRequest(
        auth=AuthCredential(
            token=TokenCredential(token="test-token"),
        ),
        request=ListAccounts(),
        settings={},
    )


class TestRateLimitedClient:
    """Test cases for RateLimitedClient."""

    def test_init(self, mock_async_client, rate_limit_config):
        """Test RateLimitedClient initialization."""
        client = RateLimitedClient(mock_async_client, rate_limit_config)

        assert client.base_client is mock_async_client
        assert client.rate_limiter is not None
        assert client.rate_limiter.config is rate_limit_config

    def test_getattr_delegation(self, mock_async_client, rate_limit_config):
        """Test that attribute access is delegated to base_client."""
        client = RateLimitedClient(mock_async_client, rate_limit_config)

        # Mock a method on the base client
        mock_async_client.some_method = MagicMock(return_value="delegated")

        # Access the method through the rate limited client
        result = client.some_method()

        assert result == "delegated"
        mock_async_client.some_method.assert_called_once()

    async def test_execute_request_success(self, mock_async_client, rate_limit_config):
        """Test successful request execution."""
        # Mock successful response
        mock_response = httpx.Response(200, json={"data": "success"})
        mock_response._request = httpx.Request("GET", "https://example.com")
        mock_async_client.get.return_value = mock_response

        client = RateLimitedClient(mock_async_client, rate_limit_config)

        # Mock the rate limiter instance
        with patch.object(client, "rate_limiter") as mock_limiter:
            mock_limiter.execute_requests = AsyncMock(return_value=[mock_response])

            response = await client._execute_request("get", "/test")

            assert response is mock_response
            mock_limiter.execute_requests.assert_called_once()

    async def test_execute_request_no_response(self, mock_async_client, rate_limit_config):
        """Test execute_request when no response is returned."""
        client = RateLimitedClient(mock_async_client, rate_limit_config)

        with patch.object(client, "rate_limiter") as mock_limiter:
            mock_limiter.execute_requests = AsyncMock(return_value=[])

            with pytest.raises(ConnectorError) as exc_info:
                await client._execute_request("get", "/test")
            # Check that the error has the expected message
            assert exc_info.value.message == "No response from the API"

    async def test_execute_request_with_raise_for_status(
        self, mock_async_client, rate_limit_config
    ):
        """Test execute_request with raise_for_status behavior."""
        # Mock response that will raise HTTPStatusError
        mock_response = httpx.Response(400, text="Bad request")
        mock_response._request = httpx.Request("GET", "https://example.com")
        mock_async_client.get.return_value = mock_response

        client = RateLimitedClient(mock_async_client, rate_limit_config)

        with patch.object(client, "rate_limiter") as mock_limiter:
            # Simulate the rate limiter handling the error
            mock_limiter.execute_requests = AsyncMock(
                side_effect=httpx.HTTPStatusError(
                    "Bad request", request=mock_response._request, response=mock_response
                )
            )

            with pytest.raises(httpx.HTTPStatusError):
                await client._execute_request("get", "/test")

    async def test_batch_request_success(self, mock_async_client, rate_limit_config):
        """Test successful batch request execution."""
        # Mock responses
        responses = [
            httpx.Response(200, json={"id": "user1"}),
            httpx.Response(200, json={"id": "user2"}),
        ]
        for response in responses:
            response._request = httpx.Request("GET", "https://example.com")

        client = RateLimitedClient(mock_async_client, rate_limit_config)

        with patch.object(client, "rate_limiter") as mock_limiter:
            mock_limiter.execute_requests = AsyncMock(return_value=responses)

            batch_requests = [
                (("/users/user1",), {}),
                (("/users/user2",), {}),
            ]

            result = await client.batch_request("get", batch_requests)

            assert len(result) == 2
            assert result == responses
            mock_limiter.execute_requests.assert_called_once()

    async def test_batch_request_empty_list(self, mock_async_client, rate_limit_config):
        """Test batch request with empty list."""
        client = RateLimitedClient(mock_async_client, rate_limit_config)

        with patch.object(client, "rate_limiter") as mock_limiter:
            mock_limiter.execute_requests = AsyncMock(return_value=[])

            result = await client.batch_request("get", [])

            assert result == []
            # When request list is empty, execute_requests is never called
            mock_limiter.execute_requests.assert_not_called()

    async def test_batch_request_with_default_kwargs(self, mock_async_client, rate_limit_config):
        """Test batch request with default kwargs merging."""
        # Mock responses
        responses = [httpx.Response(200, json={"id": "user1"})]
        responses[0]._request = httpx.Request("GET", "https://example.com")

        client = RateLimitedClient(mock_async_client, rate_limit_config)

        with patch.object(client, "rate_limiter") as mock_limiter:
            mock_limiter.execute_requests = AsyncMock(return_value=responses)

            batch_requests = [(("/users/user1",), {"timeout": 30})]

            await client.batch_request(
                "get", batch_requests, headers={"Authorization": "Bearer token"}, timeout=10
            )

            # Verify the request function was created with merged kwargs
            call_args = mock_limiter.execute_requests.call_args
            request_functions = call_args[0][0]

            # The first request function should have merged kwargs
            assert len(request_functions) == 1

    def test_get_state(self, mock_async_client, rate_limit_config):
        """Test get_state method."""
        client = RateLimitedClient(mock_async_client, rate_limit_config)

        with (
            patch.object(client.rate_limiter, "config", rate_limit_config),
            patch.object(client.rate_limiter, "current_delay", 5.0),
        ):
            config, delay = client.get_state()

            assert config is rate_limit_config
            assert delay == 5.0

    async def test_http_methods(self, mock_async_client, rate_limit_config):
        """Test that HTTP methods are properly delegated."""
        mock_response = httpx.Response(200, json={"data": "success"})
        mock_response._request = httpx.Request("GET", "https://example.com")

        with patch.object(
            RateLimitedClient, "_execute_request", return_value=mock_response
        ) as mock_execute:
            client = RateLimitedClient(mock_async_client, rate_limit_config)

            # Test all HTTP methods
            await client.get("/test")
            await client.post("/test", json={"data": "test"})
            await client.put("/test", json={"data": "test"})
            await client.patch("/test", json={"data": "test"})
            await client.delete("/test")

            assert mock_execute.call_count == 5
            assert mock_execute.call_args_list[0][0] == ("get", "/test")
            assert mock_execute.call_args_list[1][0] == ("post", "/test")
            assert mock_execute.call_args_list[2][0] == ("put", "/test")
            assert mock_execute.call_args_list[3][0] == ("patch", "/test")
            assert mock_execute.call_args_list[4][0] == ("delete", "/test")

    async def test_context_manager(self, mock_async_client, rate_limit_config):
        """Test async context manager functionality."""
        client = RateLimitedClient(mock_async_client, rate_limit_config)

        async with client as ctx:
            assert ctx is client
            mock_async_client.__aenter__.assert_called_once()

        mock_async_client.__aexit__.assert_called_once_with(None, None, None)


class TestBaseIntegrationClient:
    """Test cases for BaseIntegrationClient."""

    class ConcreteTestClient(BaseIntegrationClient):
        """Concrete implementation for testing."""

        @classmethod
        def prepare_client_args(cls, args: Request) -> dict[str, Any]:
            return {
                "auth": BearerAuth(
                    token=get_token_auth(args).token,
                    token_prefix="",
                    auth_header="X-Api-Key",
                ),
                "base_url": "https://example.com",
            }

    def test_init_without_rate_limiting(self, sample_request):
        """Test initialization without rate limiting."""
        with patch.object(self.ConcreteTestClient, "build_client") as mock_build:
            mock_client = AsyncMock(spec=httpx.AsyncClient)
            mock_build.return_value = mock_client

            client = self.ConcreteTestClient(sample_request)

            assert client._http_client is mock_client
            assert client._rate_limit_config is None

    def test_init_with_rate_limiting(self, sample_request, rate_limit_config):
        """Test initialization with rate limiting."""
        with patch.object(self.ConcreteTestClient, "build_client") as mock_build:
            mock_client = AsyncMock(spec=httpx.AsyncClient)
            mock_build.return_value = mock_client

            client = self.ConcreteTestClient(sample_request, rate_limit_config)

            assert isinstance(client._http_client, RateLimitedClient)
            assert client._http_client.base_client is mock_client
            # The rate_limit_config is not stored as an instance variable in BaseIntegrationClient

    def test_init_with_class_rate_limit_config(self, sample_request):
        """Test initialization with class-level rate limit config."""

        class TestClientWithConfig(self.ConcreteTestClient):
            _rate_limit_config = RateLimitConfig(
                app_id="class-config",
                requests_per_window=5,
                window_seconds=30,
            )

        with patch.object(TestClientWithConfig, "build_client") as mock_build:
            mock_client = AsyncMock(spec=httpx.AsyncClient)
            mock_build.return_value = mock_client

            client = TestClientWithConfig(sample_request)

            assert isinstance(client._http_client, RateLimitedClient)
            assert client._rate_limit_config.app_id == "class-config"

    def test_get_current_rate_limits_with_rate_limiting(self, sample_request, rate_limit_config):
        """Test get_current_rate_limits with rate limited client."""
        with patch.object(self.ConcreteTestClient, "build_client") as mock_build:
            mock_client = AsyncMock(spec=httpx.AsyncClient)
            mock_build.return_value = mock_client

            client = self.ConcreteTestClient(sample_request, rate_limit_config)

            with patch.object(
                client._http_client, "get_state", return_value=(rate_limit_config, 5.0)
            ):
                config, delay = client.get_current_rate_limits()

                assert config is rate_limit_config
                assert delay == 5.0

    def test_get_current_rate_limits_without_rate_limiting(self, sample_request):
        """Test get_current_rate_limits without rate limited client."""
        with patch.object(self.ConcreteTestClient, "build_client") as mock_build:
            mock_client = AsyncMock(spec=httpx.AsyncClient)
            mock_build.return_value = mock_client

            client = self.ConcreteTestClient(sample_request)

            config, delay = client.get_current_rate_limits()

            assert config is None
            assert delay == 0

    async def test_batch_request_with_rate_limiting(self, sample_request, rate_limit_config):
        """Test batch_request with rate limited client."""
        with patch.object(self.ConcreteTestClient, "build_client") as mock_build:
            mock_client = AsyncMock(spec=httpx.AsyncClient)
            mock_build.return_value = mock_client

            client = self.ConcreteTestClient(sample_request, rate_limit_config)

            mock_responses = [httpx.Response(200, json={"data": "test"})]
            with patch.object(
                client._http_client, "batch_request", return_value=mock_responses
            ) as mock_batch:
                batch_requests = [(("/test",), {})]
                result = await client.batch_request("get", batch_requests)

                assert result == mock_responses
                mock_batch.assert_called_once_with("get", batch_requests)

    async def test_batch_request_without_rate_limiting(self, sample_request):
        """Test batch_request without rate limited client."""
        with patch.object(self.ConcreteTestClient, "build_client") as mock_build:
            mock_client = AsyncMock(spec=httpx.AsyncClient)
            mock_build.return_value = mock_client

            client = self.ConcreteTestClient(sample_request)

            # Mock individual request responses
            mock_response1 = httpx.Response(200, json={"id": "user1"})
            mock_response2 = httpx.Response(200, json={"id": "user2"})
            mock_client.get.side_effect = [mock_response1, mock_response2]

            batch_requests = [
                (("/users/user1",), {}),
                (("/users/user2",), {}),
            ]

            result = await client.batch_request("get", batch_requests)

            assert len(result) == 2
            assert result == [mock_response1, mock_response2]
            assert mock_client.get.call_count == 2

    async def test_batch_request_with_default_kwargs(self, sample_request):
        """Test batch_request with default kwargs merging."""
        with patch.object(self.ConcreteTestClient, "build_client") as mock_build:
            mock_client = AsyncMock(spec=httpx.AsyncClient)
            mock_build.return_value = mock_client

            client = self.ConcreteTestClient(sample_request)

            # Mock individual request responses
            mock_response = httpx.Response(200, json={"id": "user1"})
            mock_client.get.return_value = mock_response

            batch_requests = [(("/users/user1",), {"timeout": 30})]

            await client.batch_request(
                "get", batch_requests, headers={"Authorization": "Bearer token"}, timeout=10
            )

            # Verify the call was made with merged kwargs
            mock_client.get.assert_called_once_with(
                "/users/user1",
                timeout=30,  # Request-specific timeout should override default
                headers={"Authorization": "Bearer token"},
            )

    async def test_context_manager(self, sample_request):
        """Test async context manager functionality."""
        with patch.object(self.ConcreteTestClient, "build_client") as mock_build:
            mock_client = AsyncMock(spec=httpx.AsyncClient)
            mock_build.return_value = mock_client

            client = self.ConcreteTestClient(sample_request)

            async with client as ctx:
                assert ctx is client
                mock_client.__aenter__.assert_called_once()

            mock_client.__aexit__.assert_called_once_with(None, None, None)

    async def test_context_manager_with_exception(self, sample_request):
        """Test context manager with exception handling."""
        with patch.object(self.ConcreteTestClient, "build_client") as mock_build:
            mock_client = AsyncMock(spec=httpx.AsyncClient)
            mock_build.return_value = mock_client

            client = self.ConcreteTestClient(sample_request)

            test_exception = Exception("Test error")

            with pytest.raises(Exception, match="Test error"):
                async with client:
                    raise test_exception

            # Check that __aexit__ was called with the exception
            mock_client.__aexit__.assert_called_once()
            call_args = mock_client.__aexit__.call_args[0]
            assert call_args[0] is Exception
            assert call_args[1] is test_exception
            # Don't check traceback object identity as it may differ


class TestBatchRequestTypes:
    """Test cases for batch request type definitions."""

    def test_batch_request_type_alias(self):
        """Test that BatchRequest type alias is properly defined."""
        # Test that we can create a BatchRequest
        batch_request: BatchRequest = (("/test",), {"timeout": 10})
        assert isinstance(batch_request, tuple)
        assert len(batch_request) == 2
        assert batch_request[0] == ("/test",)
        assert batch_request[1] == {"timeout": 10}

    def test_batch_requests_type_alias(self):
        """Test that BatchRequests type alias is properly defined."""
        # Test that we can create a BatchRequests list
        batch_requests: BatchRequests = [
            (("/test1",), {}),
            (("/test2",), {"timeout": 10}),
        ]
        assert isinstance(batch_requests, list)
        assert len(batch_requests) == 2
        assert all(isinstance(req, tuple) for req in batch_requests)


class TestErrorHandling:
    """Test cases for error handling scenarios."""

    async def test_rate_limited_client_handles_non_httpx_errors(
        self, mock_async_client, rate_limit_config
    ):
        """Test that RateLimitedClient handles non-httpx errors properly."""
        # Mock a response without proper request context
        mock_response = httpx.Response(200, json={"data": "success"})
        # Don't set _request to simulate a response without proper context
        mock_async_client.get.return_value = mock_response

        client = RateLimitedClient(mock_async_client, rate_limit_config)

        with patch.object(client, "rate_limiter") as mock_limiter:
            mock_limiter.execute_requests = AsyncMock(return_value=[mock_response])
            response = await client._execute_request("get", "/test")

            # Should return the response without calling raise_for_status
            assert response is mock_response

    async def test_rate_limited_client_handles_raise_for_status_errors(
        self, mock_async_client, rate_limit_config
    ):
        """Test that RateLimitedClient handles raise_for_status errors properly."""
        # Mock a response that will raise HTTPStatusError
        mock_response = httpx.Response(400, text="Bad request")
        mock_response._request = httpx.Request("GET", "https://example.com")
        mock_async_client.get.return_value = mock_response

        client = RateLimitedClient(mock_async_client, rate_limit_config)

        with patch.object(client, "rate_limiter") as mock_limiter:
            # Simulate rate limiter handling the error
            mock_limiter.execute_requests = AsyncMock(
                side_effect=httpx.HTTPStatusError(
                    "Bad request", request=mock_response._request, response=mock_response
                )
            )

            with pytest.raises(httpx.HTTPStatusError):
                await client._execute_request("get", "/test")

    async def test_base_integration_client_handles_build_client_errors(self, sample_request):
        """Test that BaseIntegrationClient handles build_client errors."""

        class ErrorTestClient(BaseIntegrationClient):
            @classmethod
            def prepare_client_args(cls, args: Request) -> dict[str, Any]:
                return {"base_url": "https://example.com"}

        with patch.object(ErrorTestClient, "build_client", side_effect=Exception("Build error")):
            with pytest.raises(Exception, match="Build error"):
                ErrorTestClient(sample_request)


class TestIntegrationScenarios:
    """Test cases for integration scenarios."""

    async def test_full_workflow_with_rate_limiting(self, sample_request, rate_limit_config):
        """Test a full workflow with rate limiting enabled."""

        class IntegrationTestClient(BaseIntegrationClient):
            @classmethod
            def prepare_client_args(cls, args: Request) -> dict[str, Any]:
                return {
                    "auth": BearerAuth(
                        token=get_token_auth(args).token,
                        token_prefix="",
                        auth_header="X-Api-Key",
                    ),
                    "base_url": "https://example.com",
                }

        with patch.object(IntegrationTestClient, "build_client") as mock_build:
            mock_client = AsyncMock(spec=httpx.AsyncClient)
            mock_build.return_value = mock_client

            client = IntegrationTestClient(sample_request, rate_limit_config)

            # Mock successful responses
            mock_response = httpx.Response(200, json={"data": "success"})
            mock_response._request = httpx.Request("GET", "https://example.com")

            with patch.object(client._http_client, "get", return_value=mock_response):
                async with client:
                    response = await client._http_client.get("/test")
                    assert response.status_code == 200

    async def test_batch_workflow_with_mixed_success_failure(self, sample_request):
        """Test batch workflow with mixed success and failure scenarios."""

        class BatchTestClient(BaseIntegrationClient):
            @classmethod
            def prepare_client_args(cls, args: Request) -> dict[str, Any]:
                return {"base_url": "https://example.com"}

        with patch.object(BatchTestClient, "build_client") as mock_build:
            mock_client = AsyncMock(spec=httpx.AsyncClient)
            mock_build.return_value = mock_client

            client = BatchTestClient(sample_request)

            # Mock mixed responses
            success_response = httpx.Response(200, json={"id": "user1"})
            error_response = httpx.Response(404, text="Not found")
            mock_client.get.side_effect = [success_response, error_response]

            batch_requests = [
                (("/users/user1",), {}),
                (("/users/user2",), {}),
            ]

            responses = await client.batch_request("get", batch_requests)

            assert len(responses) == 2
            assert responses[0].status_code == 200
            assert responses[1].status_code == 404
