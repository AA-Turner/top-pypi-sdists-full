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
    BaseGraphQLSession,
    BaseIntegrationClient,
    BatchRequest,
    BatchRequests,
    RateLimitedClient,
    RateLimitedHTTPXAsyncTransport,
)
from connector.oai.capability import Request, get_token_auth
from connector.oai.errors import ConnectorError
from connector.utils.httpx_auth import BearerAuth
from connector.utils.rate_limit_context import (
    RATE_LIMIT_CONTEXT,
    RATE_LIMIT_RESULT_CONTEXT,
    RateLimitExecutionContext,
)
from connector.utils.rate_limit_utils import _resolve_rate_limiting_mode
from connector.utils.rate_limiting import RateLimitConfig, RateLimiter, RateLimitStrategy
from connector_sdk_types.generated import (
    ConnectorErrorCode,
    RateLimitMode,
    RateLimitStateSnapshot,
    StandardCapabilityName,
)
from connector_sdk_types.oai.modules.rate_limiting_types import RateLimitPolicySource


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
            config, delay = client.get_current_rate_limits()

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
                client._http_client,
                "get_current_rate_limits",
                return_value=(rate_limit_config, 5.0),
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


class TestRateLimitedHTTPXAsyncTransport:
    """Test cases for RateLimitedHTTPXAsyncTransport."""

    @pytest.fixture
    def mock_base_transport(self):
        """Create a mock HTTPXAsyncTransport for testing."""
        from types import SimpleNamespace

        transport = SimpleNamespace()
        transport.some_attr = "value"
        return transport

    async def test_rate_limited_graphql_execution(self, mock_base_transport, rate_limit_config):
        """Test that GraphQL requests are executed through rate limiter."""
        mock_result = {"data": {"test": "result"}}
        mock_base_transport.execute = AsyncMock(return_value=mock_result)

        transport = RateLimitedHTTPXAsyncTransport(mock_base_transport, rate_limit_config)

        async def mock_execute_requests(self, requests, handler):
            results = []
            for req in requests:
                result = await handler(req)
                results.append(result)
            return results

        with patch.object(RateLimiter, "execute_requests", mock_execute_requests):
            result = await transport.execute("query { test }", variable_values={})

        assert result == mock_result
        mock_base_transport.execute.assert_called_once()
        call_args = mock_base_transport.execute.call_args
        assert call_args.kwargs.get("document") == "query { test }"
        assert call_args.kwargs.get("variable_values") == {}

    async def test_connect_sets_client_reference(self, rate_limit_config):
        """Test that connect copies base_transport.client without wrapping it."""
        from connector.httpx_rewrite import AsyncClient

        class MockTransport:
            def __init__(self):
                self.client = None
                self.connect_called = False

            async def connect(self):
                self.connect_called = True

        real_client = AsyncClient(base_url="https://example.com")
        base_transport = MockTransport()
        base_transport.client = real_client

        transport = RateLimitedHTTPXAsyncTransport(base_transport, rate_limit_config)
        await transport.connect()

        assert base_transport.connect_called
        # Client must NOT be wrapped — rate limiting is enforced in execute(), not here
        assert base_transport.client is real_client
        assert not isinstance(base_transport.client, RateLimitedClient)
        assert transport.client is real_client

    async def test_connect_with_non_async_client(self, mock_base_transport, rate_limit_config):
        """Test that connect sets client reference for any client type."""
        mock_client = MagicMock()
        mock_base_transport.client = mock_client
        mock_base_transport.connect = AsyncMock()

        transport = RateLimitedHTTPXAsyncTransport(mock_base_transport, rate_limit_config)
        await transport.connect()

        mock_base_transport.connect.assert_called_once()
        assert transport.client is mock_client

    async def test_connect_without_client(self, mock_base_transport, rate_limit_config):
        """Test that connect handles case when base transport client is None."""
        mock_base_transport.connect = AsyncMock()
        mock_base_transport.client = None

        transport = RateLimitedHTTPXAsyncTransport(mock_base_transport, rate_limit_config)
        await transport.connect()

        mock_base_transport.connect.assert_called_once()
        assert transport.client is None

    async def test_connect_without_client_attribute(self, rate_limit_config):
        """Test that connect silently skips client copy when the attribute does not exist."""

        class MockTransportWithoutClient:
            def __init__(self):
                self.connect_called = False

            async def connect(self):
                self.connect_called = True

            def __getattribute__(self, name):
                if name == "client":
                    raise AttributeError(
                        f"'{type(self).__name__}' object has no attribute 'client'"
                    )
                return super().__getattribute__(name)

        mock_base_transport = MockTransportWithoutClient()
        transport = RateLimitedHTTPXAsyncTransport(mock_base_transport, rate_limit_config)

        assert not hasattr(transport.base_transport, "client")
        # hasattr protects us — connect should not raise
        await transport.connect()
        assert mock_base_transport.connect_called

    async def test_execute_with_all_parameters(self, mock_base_transport, rate_limit_config):
        """Test execute method with all GraphQL parameters."""
        mock_result = {"data": {"test": "result"}}
        mock_base_transport.execute = AsyncMock(return_value=mock_result)

        transport = RateLimitedHTTPXAsyncTransport(mock_base_transport, rate_limit_config)

        async def mock_execute_requests(self, requests, handler):
            results = []
            for req in requests:
                result = await handler(req)
                results.append(result)
            return results

        with patch.object(RateLimiter, "execute_requests", mock_execute_requests):
            result = await transport.execute(
                "query { test }", variable_values={"var": "value"}, operation_name="TestQuery"
            )

        assert result == mock_result
        mock_base_transport.execute.assert_called_once()
        call_args = mock_base_transport.execute.call_args
        assert call_args.kwargs.get("document") == "query { test }"
        assert call_args.kwargs.get("variable_values") == {"var": "value"}
        assert call_args.kwargs.get("operation_name") == "TestQuery"

    async def test_execute_calls_request_func_through_handler(
        self, mock_base_transport, rate_limit_config
    ):
        """Test that execute calls request_func() through the handler lambda (lines 209-214).

        This verifies that:
        1. A request_func closure is created (line 208-211) that calls base_transport.execute
        2. The request_func is passed to rate_limiter.execute_requests (line 214)
        3. The handler lambda (lambda x: x()) is used to call request_func (line 214)
        4. request_func() executes and calls base_transport.execute
        """
        mock_result = {"data": {"test": "result"}}
        mock_base_transport.execute = AsyncMock(return_value=mock_result)

        transport = RateLimitedHTTPXAsyncTransport(mock_base_transport, rate_limit_config)

        async def mock_execute_requests(self, requests, handler):
            results = []
            for req in requests:
                result = await handler(req)
                results.append(result)
            return results

        with patch.object(RateLimiter, "execute_requests", mock_execute_requests):
            result = await transport.execute("query { test }", variable_values={"var": "value"})

        assert result == mock_result
        mock_base_transport.execute.assert_called_once()

        call_args = mock_base_transport.execute.call_args
        assert call_args.kwargs.get("document") == "query { test }"
        assert call_args.kwargs.get("variable_values") == {"var": "value"}

    async def test_execute_raises_on_no_response(self, mock_base_transport, rate_limit_config):
        """Test that execute raises ConnectorError when rate limiter returns no response.

        This tests the negative branch of line 215 where responses is falsy (empty list).
        """
        transport = RateLimitedHTTPXAsyncTransport(mock_base_transport, rate_limit_config)

        async def empty_execute_requests(self, requests, handler):
            return []

        with patch.object(RateLimiter, "execute_requests", empty_execute_requests):
            with pytest.raises(ConnectorError) as exc_info:
                await transport.execute("query { test }")

            assert exc_info.value.message == "No response from GraphQL API"
            assert exc_info.value.error_code == ConnectorErrorCode.INVALID_RESPONSE

    async def test_execute_with_successful_response(self, mock_base_transport, rate_limit_config):
        """Test that execute returns response when rate limiter returns a response.

        This tests the positive branch of line 215 where responses is truthy (non-empty list).
        We patch at the class level to ensure the mock is actually used.
        """
        mock_result = {"data": {"test": "result"}}
        mock_base_transport.execute = AsyncMock(return_value=mock_result)

        transport = RateLimitedHTTPXAsyncTransport(mock_base_transport, rate_limit_config)

        async def mock_execute_requests(self, requests, handler):
            results = []
            for req in requests:
                result = await handler(req)
                results.append(result)
            return results

        with patch.object(RateLimiter, "execute_requests", mock_execute_requests):
            result = await transport.execute("query { test }")

        assert result == mock_result
        mock_base_transport.execute.assert_called_once()

    def test_delegation_and_state(self, mock_base_transport, rate_limit_config):
        """Test attribute delegation and state retrieval."""
        mock_base_transport.delegated_method = MagicMock(return_value="delegated_value")
        transport = RateLimitedHTTPXAsyncTransport(mock_base_transport, rate_limit_config)

        assert transport.some_attr == "value"
        assert transport.delegated_method() == "delegated_value"

        config, delay = transport.get_current_rate_limits()
        assert config is rate_limit_config  # RateLimitedHTTPXAsyncTransport stores config directly
        assert isinstance(delay, float)


class TestBaseGraphQLSession:
    """Test cases for BaseGraphQLSession."""

    class ConcreteTestGraphQLSession(BaseGraphQLSession):
        """Concrete implementation for testing."""

        @classmethod
        def prepare_client_args(cls, args: Request) -> dict[str, Any]:
            from connector.httpx_rewrite import HTTPXAsyncTransport

            return {
                "transport": HTTPXAsyncTransport(
                    url="https://example.com/graphql",
                    auth=BearerAuth(
                        token=get_token_auth(args).token,
                        token_prefix="",
                        auth_header="Authorization",
                    ),
                ),
            }

    def test_build_client_applies_rate_limiting(self, sample_request, rate_limit_config):
        """Test that build_client wraps transport with rate limiter when config provided."""
        client = self.ConcreteTestGraphQLSession.build_client(sample_request, rate_limit_config)

        assert client is not None
        assert isinstance(client.transport, RateLimitedHTTPXAsyncTransport)
        # mode is resolved (None → ENFORCE) via model_copy, so use field equality not identity
        assert client.transport.rate_limiter.config.app_id == rate_limit_config.app_id
        assert (
            client.transport.rate_limiter.config.requests_per_window
            == rate_limit_config.requests_per_window
        )

        client_no_rate_limit = self.ConcreteTestGraphQLSession.build_client(sample_request)
        assert client_no_rate_limit is not None
        assert not isinstance(client_no_rate_limit.transport, RateLimitedHTTPXAsyncTransport)

        class TestSessionWithClassConfig(self.ConcreteTestGraphQLSession):
            _rate_limit_config = RateLimitConfig(
                app_id="class-config",
                requests_per_window=5,
                window_seconds=30,
            )

        client_with_class_config = TestSessionWithClassConfig.build_client(sample_request)
        assert isinstance(client_with_class_config.transport, RateLimitedHTTPXAsyncTransport)

    def test_get_current_rate_limits(self, sample_request, rate_limit_config):
        """Test rate limit state retrieval."""
        client_with_rate_limit = self.ConcreteTestGraphQLSession.build_client(
            sample_request, rate_limit_config
        )
        session_with_rate_limit = self.ConcreteTestGraphQLSession(sample_request, rate_limit_config)
        session_with_rate_limit.client = client_with_rate_limit

        config, delay = session_with_rate_limit.get_current_rate_limits()
        # mode is resolved (None → ENFORCE) via model_copy, so use field equality not identity
        assert config is not None
        assert config.app_id == rate_limit_config.app_id
        assert config.requests_per_window == rate_limit_config.requests_per_window
        assert isinstance(delay, float)

        client_no_rate_limit = self.ConcreteTestGraphQLSession.build_client(sample_request)
        session_no_rate_limit = self.ConcreteTestGraphQLSession(sample_request)
        session_no_rate_limit.client = client_no_rate_limit

        config, delay = session_no_rate_limit.get_current_rate_limits()
        assert config is None
        assert delay == 0

    async def test_context_manager(self, sample_request):
        """Test async context manager functionality."""
        with patch("connector.oai.base_clients.Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock()
            mock_client_class.return_value = mock_client

            session = self.ConcreteTestGraphQLSession(sample_request)

            async with session as ctx:
                assert ctx is session

            mock_client.__aenter__.assert_called_once()
            mock_client.__aexit__.assert_called_once()

            test_exception = ValueError("Test error")
            with pytest.raises(ValueError, match="Test error"):
                async with session:
                    raise test_exception


# _resolve_rate_limiting_mode


def _make_config(mode: RateLimitMode | None = None) -> RateLimitConfig:
    return RateLimitConfig(
        app_id="test",
        requests_per_window=10,
        window_seconds=60,
        mode=mode,
    )


def _make_ctx(
    capability_level: str = "read",
    caller_override_mode: RateLimitMode | None = None,
    capability_override_mode: RateLimitMode | None = None,
) -> RateLimitExecutionContext:
    return RateLimitExecutionContext(
        capability_name=StandardCapabilityName.LIST_ACCOUNTS,
        capability_level=capability_level,  # type: ignore[arg-type]
        caller_override_mode=caller_override_mode,
        capability_override_mode=capability_override_mode,
    )


class TestResolveEffectiveMode:
    def test_capability_override_takes_highest_priority(self) -> None:
        ctx = _make_ctx(
            capability_override_mode=RateLimitMode.BYPASS,
            caller_override_mode=RateLimitMode.RETRY_ONLY,
        )
        config = _make_config(mode=RateLimitMode.ENFORCE)
        mode, source = _resolve_rate_limiting_mode(ctx, config)
        assert mode == RateLimitMode.BYPASS
        assert source == RateLimitPolicySource.CAPABILITY

    def test_connector_config_mode_second_priority(self) -> None:
        ctx = _make_ctx(caller_override_mode=RateLimitMode.RETRY_ONLY)
        config = _make_config(mode=RateLimitMode.BYPASS)
        mode, source = _resolve_rate_limiting_mode(ctx, config)
        assert mode == RateLimitMode.BYPASS
        assert source == RateLimitPolicySource.CONNECTOR

    def test_caller_override_third_priority(self) -> None:
        ctx = _make_ctx(caller_override_mode=RateLimitMode.BYPASS)
        config = _make_config(mode=None)  # no connector-level override
        mode, source = _resolve_rate_limiting_mode(ctx, config)
        assert mode == RateLimitMode.BYPASS
        assert source == RateLimitPolicySource.CALLER

    def test_sdk_default_read_capability_returns_enforce(self) -> None:
        ctx = _make_ctx(capability_level="read")
        config = _make_config(mode=None)
        mode, source = _resolve_rate_limiting_mode(ctx, config)
        assert mode == RateLimitMode.ENFORCE
        assert source == RateLimitPolicySource.SDK

    def test_sdk_default_write_capability_returns_retry_only(self) -> None:
        ctx = _make_ctx(capability_level="write")
        config = _make_config(mode=None)
        mode, source = _resolve_rate_limiting_mode(ctx, config)
        assert mode == RateLimitMode.RETRY_ONLY
        assert source == RateLimitPolicySource.SDK

    def test_no_context_defaults_to_enforce(self) -> None:
        config = _make_config(mode=None)
        mode, source = _resolve_rate_limiting_mode(None, config)
        assert mode == RateLimitMode.ENFORCE
        assert source == RateLimitPolicySource.SDK

    def test_all_overrides_none_read_ctx_returns_enforce(self) -> None:
        ctx = _make_ctx(
            capability_level="read", caller_override_mode=None, capability_override_mode=None
        )
        config = _make_config(mode=None)
        mode, source = _resolve_rate_limiting_mode(ctx, config)
        assert mode == RateLimitMode.ENFORCE

    def test_capability_override_wins_over_connector_mode(self) -> None:
        ctx = _make_ctx(capability_override_mode=RateLimitMode.RETRY_ONLY)
        config = _make_config(mode=RateLimitMode.ENFORCE)
        mode, source = _resolve_rate_limiting_mode(ctx, config)
        assert mode == RateLimitMode.RETRY_ONLY
        assert source == RateLimitPolicySource.CAPABILITY


# BaseIntegrationClient: BYPASS mode, state snapshot, seed from state


class TestBaseIntegrationClientRateLimitBehavior:
    """Tests for rate-limiting-related BaseIntegrationClient behaviour.

    The suppress_rate_limit_state_passthrough autouse fixture from the SDK plugin
    patches get_current_state → None. We override it here so state-snapshot tests
    can observe the real return value.
    """

    @pytest.fixture(autouse=True)
    def suppress_rate_limit_state_passthrough(self):
        """Override the plugin autouse fixture, these tests need the real get_current_state."""
        yield  # no patch

    class ConcreteClient(BaseIntegrationClient):
        @classmethod
        def prepare_client_args(cls, args: Request) -> dict[str, Any]:
            from connector.oai.capability import get_token_auth
            from connector.utils.httpx_auth import BearerAuth

            return {
                "auth": BearerAuth(
                    token=get_token_auth(args).token, token_prefix="", auth_header="X-Api-Key"
                ),
                "base_url": "https://example.com",
            }

    @pytest.fixture
    def sample_request(self):
        return ListAccountsRequest(
            auth=AuthCredential(token=TokenCredential(token="test-token")),
            request=ListAccounts(),
            settings={},
        )

    def test_bypass_mode_leaves_raw_client(self, sample_request) -> None:
        config = _make_config(mode=RateLimitMode.BYPASS)
        ctx = _make_ctx(capability_level="read")
        token = RATE_LIMIT_CONTEXT.set(ctx)
        try:
            with patch.object(self.ConcreteClient, "build_client") as mock_build:
                mock_client = AsyncMock(spec=httpx.AsyncClient)
                mock_build.return_value = mock_client
                client = self.ConcreteClient(sample_request, config)
                # BYPASS → no RateLimitedClient wrapper
                assert not isinstance(client._http_client, RateLimitedClient)
        finally:
            RATE_LIMIT_CONTEXT.reset(token)

    def test_non_bypass_mode_wraps_client(self, sample_request) -> None:
        config = _make_config(mode=None)
        ctx = _make_ctx(capability_level="read")
        token = RATE_LIMIT_CONTEXT.set(ctx)
        try:
            with patch.object(self.ConcreteClient, "build_client") as mock_build:
                mock_client = AsyncMock(spec=httpx.AsyncClient)
                mock_build.return_value = mock_client
                client = self.ConcreteClient(sample_request, config)
                assert isinstance(client._http_client, RateLimitedClient)
        finally:
            RATE_LIMIT_CONTEXT.reset(token)

    def test_seed_from_state_applied_on_init(self, sample_request) -> None:
        config = _make_config(mode=RateLimitMode.ENFORCE)
        state = RateLimitStateSnapshot(limit=99, window_seconds=30, current_delay=7)
        ctx = RateLimitExecutionContext(
            capability_name=StandardCapabilityName.LIST_ACCOUNTS,
            capability_level="read",
            caller_override_mode=None,
            last_known_state={config.effective_config_id: state},
        )
        token = RATE_LIMIT_CONTEXT.set(ctx)
        try:
            with patch.object(self.ConcreteClient, "build_client") as mock_build:
                mock_client = AsyncMock(spec=httpx.AsyncClient)
                mock_build.return_value = mock_client
                client = self.ConcreteClient(sample_request, config)
                assert isinstance(client._http_client, RateLimitedClient)
                assert client._http_client.rate_limiter.config.requests_per_window == 99
                assert client._http_client.rate_limiter.config.window_seconds == 30
                assert client._http_client.rate_limiter.current_delay == 7.0
        finally:
            RATE_LIMIT_CONTEXT.reset(token)

    async def test_aexit_writes_state_to_result_context(self, sample_request) -> None:
        config = _make_config(mode=RateLimitMode.ENFORCE)
        ctx = _make_ctx(capability_level="read")
        rate_limit_token = RATE_LIMIT_CONTEXT.set(ctx)
        result_token = RATE_LIMIT_RESULT_CONTEXT.set(None)
        try:
            with patch.object(self.ConcreteClient, "build_client") as mock_build:
                mock_client = AsyncMock(spec=httpx.AsyncClient)
                mock_build.return_value = mock_client
                client = self.ConcreteClient(sample_request, config)
                assert isinstance(client._http_client, RateLimitedClient)
                await client.__aexit__()
                state_map = RATE_LIMIT_RESULT_CONTEXT.get()
                assert state_map is not None
                assert config.effective_config_id in state_map
                assert state_map[config.effective_config_id].limit == config.requests_per_window
        finally:
            RATE_LIMIT_CONTEXT.reset(rate_limit_token)
            RATE_LIMIT_RESULT_CONTEXT.reset(result_token)

    async def test_aexit_does_not_write_state_when_not_rate_limited(self, sample_request) -> None:
        result_token = RATE_LIMIT_RESULT_CONTEXT.set(None)
        try:
            with patch.object(self.ConcreteClient, "build_client") as mock_build:
                mock_client = AsyncMock(spec=httpx.AsyncClient)
                mock_build.return_value = mock_client
                client = self.ConcreteClient(sample_request)  # no rate limit config
                await client.__aexit__()
                assert RATE_LIMIT_RESULT_CONTEXT.get() is None
        finally:
            RATE_LIMIT_RESULT_CONTEXT.reset(result_token)
