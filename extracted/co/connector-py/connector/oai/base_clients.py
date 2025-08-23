import json
import logging
import typing as t
from abc import abstractmethod
from collections.abc import Callable
from pathlib import Path
from typing import Any

from connector_sdk_types.generated import ErrorCode
from gql import Client
from gql.client import AsyncClientSession
from gql.dsl import DSLSchema
from graphql import GraphQLSchema, build_client_schema, build_schema
from httpx import Response
from typing_extensions import Self

from connector.httpx_rewrite import AsyncClient
from connector.oai.capability import Request
from connector.oai.errors import ConnectorError
from connector.utils.rate_limiting import RateLimitConfig, RateLimiter

logger = logging.getLogger(__name__)

# Type alias for batch requests
BatchRequest = tuple[tuple[Any, ...], dict[str, Any]]
BatchRequests = list[BatchRequest]


class RateLimitedClient(AsyncClient):
    """A wrapper around httpx.AsyncClient that applies rate limiting."""

    def __init__(self, base_client: AsyncClient, rate_limit_config: RateLimitConfig):
        self.base_client = base_client
        self.rate_limiter = RateLimiter[Callable[[], Any], Any](rate_limit_config)

    def __getattr__(self, name):
        """Delegate attribute access to the underlying base_client."""
        return getattr(self.base_client, name)

    async def _execute_request(self, method, *args, **kwargs) -> Response:
        """Execute a request with rate limiting."""

        async def request_func():
            func = getattr(self.base_client, method)
            return await func(*args, **kwargs)

        # We're only sending one request, but using the batch API
        responses = await self.rate_limiter.execute_requests([request_func], lambda x: x())
        if responses:
            return responses[0]

        raise ConnectorError(
            message="No response from the API",
            error_code=ErrorCode.API_ERROR,
        )

    async def batch_request(
        self, method: str, requests: BatchRequests, **default_kwargs
    ) -> list[Response]:
        """
        Execute multiple requests of the same HTTP method in a batch with rate limiting.

        Args:
            method: The HTTP method to use (e.g., 'get', 'post', 'patch', 'put', 'delete')
            requests: List of tuples containing (args, kwargs) for each request
            **default_kwargs: Default keyword arguments to apply to all requests

        Returns:
            List of Response objects in the same order as the input requests

        Example:
            # Prepare batch requests
            batch_requests: BatchRequests = [
                ((f"{Endpoint.USERS}/{user_id}",), {}) for user_id in user_ids
            ]

            # Execute batch request
            responses = await self.batch_request("get", batch_requests)

            # Convert responses to User objects
            users = []
            for response in responses:
                user = create_client_response(response, User)
                users.append(user)

            return users
        """
        if not requests:
            return []

        # Create request functions for each request
        request_functions = []
        for args, kwargs in requests:
            # Create a closure to capture the current args and kwargs
            def make_request_func(request_args=args, request_kwargs=kwargs):
                async def execute_single_request():
                    # Merge default kwargs with request-specific kwargs
                    merged_kwargs = {**default_kwargs, **request_kwargs}
                    func = getattr(self.base_client, method)
                    return await func(*request_args, **merged_kwargs)

                return execute_single_request

            request_functions.append(make_request_func())

        # Execute all requests with rate limiting
        responses = await self.rate_limiter.execute_requests(request_functions, lambda x: x())

        return responses

    def get_state(self) -> tuple[RateLimitConfig, float]:
        """
        Get the current rate limit state.

        Returns a tuple of the rate limit config and the current delay.
        """
        return self.rate_limiter.config, self.rate_limiter.current_delay

    async def get(self, *args, **kwargs):
        return await self._execute_request("get", *args, **kwargs)

    async def post(self, *args, **kwargs):
        return await self._execute_request("post", *args, **kwargs)

    async def patch(self, *args, **kwargs):
        return await self._execute_request("patch", *args, **kwargs)

    async def put(self, *args, **kwargs):
        return await self._execute_request("put", *args, **kwargs)

    async def delete(self, *args, **kwargs):
        return await self._execute_request("delete", *args, **kwargs)

    # Add async context manager methods
    async def __aenter__(self):
        if hasattr(self.base_client, "__aenter__"):
            await self.base_client.__aenter__()
        return self

    async def __aexit__(self, exc_type=None, exc_val=None, exc_tb=None):
        if hasattr(self.base_client, "__aexit__"):
            await self.base_client.__aexit__(exc_type, exc_val, exc_tb)


class BaseIntegrationClient:
    _http_client: AsyncClient | RateLimitedClient
    _rate_limit_config: RateLimitConfig | None = None

    @classmethod
    @abstractmethod
    def prepare_client_args(cls, args: Request) -> dict[str, t.Any]:
        pass

    @classmethod
    def build_client(cls, args: Request) -> AsyncClient:
        return AsyncClient(**cls.prepare_client_args(args))

    def get_current_rate_limits(self) -> tuple[RateLimitConfig | None, float]:
        """
        Get the current rate limit state.

        Returns a tuple of the rate limit config and the current delay. (or None if the client is not rate limited)
        """
        if isinstance(self._http_client, RateLimitedClient):
            return self._http_client.get_state()
        return None, 0

    async def batch_request(
        self, method: str, requests: BatchRequests, **default_kwargs
    ) -> list[Response]:
        """
        Execute multiple requests of the same HTTP method in a batch with/without rate limiting.

        Args:
            method: The HTTP method to use (e.g., 'get', 'post', 'patch', 'put', 'delete')
            requests: List of tuples containing (args, kwargs) for each request
            **default_kwargs: Default keyword arguments to apply to all requests

        Returns:
            List of Response objects in the same order as the input requests
        """
        if isinstance(self._http_client, RateLimitedClient):
            return await self._http_client.batch_request(method, requests, **default_kwargs)
        else:
            # Fallback for non-rate-limited clients
            responses = []
            for args, kwargs in requests:
                merged_kwargs = {**default_kwargs, **kwargs}
                func = getattr(self._http_client, method)
                response = await func(*args, **merged_kwargs)
                responses.append(response)
            return responses

    def __init__(self, args: Request, rate_limit_config: RateLimitConfig | None = None) -> None:
        base_client = self.build_client(args)
        self._http_client = base_client

        rate_limiting = rate_limit_config or self._rate_limit_config
        if rate_limiting is not None:
            self._http_client = RateLimitedClient(base_client, rate_limiting)

    async def __aenter__(self):
        await self._http_client.__aenter__()
        return self

    async def __aexit__(self, exc_type=None, exc_val=None, exc_tb=None):
        await self._http_client.__aexit__(exc_type, exc_val, exc_tb)
        if exc_val is not None:
            raise exc_val


class BaseGraphQLSession(AsyncClientSession):
    def __init__(self, args: Request):
        super().__init__(client=self.build_client(args))

    async def __aenter__(self) -> Self:
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.__aexit__(exc_type=exc_type, exc=exc, tb=tb)

        if exc_type is not None:
            raise exc

    @classmethod
    @abstractmethod
    def prepare_client_args(cls, args: Request) -> dict[str, t.Any]:
        pass

    @classmethod
    def build_client(cls, args: Request) -> Client:
        return Client(**cls.prepare_client_args(args))

    @classmethod
    def load_schema(cls, schema_file_path: str | Path) -> GraphQLSchema:
        """Load the GraphQL schema from a .gql file."""
        with open(schema_file_path) as f:
            return build_schema(f.read())

    @classmethod
    def load_client_schema(cls, schema_file_path: str | Path) -> GraphQLSchema:
        """Load the GraphQL schema from a .json file."""
        with open(schema_file_path) as f:
            introspection = json.load(f)
            return build_client_schema(introspection.get("data", introspection))

    @property
    def schema(self) -> DSLSchema:
        if self.client.schema is None:
            raise ConnectorError(
                message="Failed to fetch schema",
                error_code=ErrorCode.API_ERROR,
            )

        return DSLSchema(self.client.schema)
