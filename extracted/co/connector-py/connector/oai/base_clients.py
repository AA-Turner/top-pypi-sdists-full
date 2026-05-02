import json
import logging
import typing as t
from abc import abstractmethod
from collections.abc import Callable
from pathlib import Path
from typing import Any

from gql import Client
from gql.client import AsyncClientSession
from gql.dsl import DSLSchema
from gql.transport.httpx import HTTPXAsyncTransport as GqlHTTPXAsyncTransport
from graphql import DocumentNode, GraphQLSchema, build_client_schema, build_schema
from httpx import Response
from typing_extensions import Self

from connector.httpx_rewrite import AsyncClient, HTTPXAsyncTransport
from connector.oai.capability import Request
from connector.oai.errors import InvalidResponseError
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
            response = await func(*args, **kwargs)
            # This raises for the RateLimiter to handle
            if (
                hasattr(response, "raise_for_status")
                and hasattr(response, "_request")
                and response._request is not None
            ):
                try:
                    response.raise_for_status()
                except Exception as e:
                    error_check = (
                        self.rate_limiter.config.rate_limit_error_check
                        or RateLimiter.is_rate_limit_error
                    )
                    if error_check(e):
                        raise e
                    else:
                        return response
            return response

        # We're only sending one request, but using the batch API
        responses = await self.rate_limiter.execute_requests([request_func], lambda x: x())
        if responses:
            return responses[0]

        raise InvalidResponseError(
            message="No response from the API",
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
                    response = await func(*request_args, **merged_kwargs)
                    # This raises for the RateLimiter to handle
                    if (
                        hasattr(response, "raise_for_status")
                        and hasattr(response, "_request")
                        and response._request is not None
                    ):
                        try:
                            response.raise_for_status()
                        except Exception as e:
                            error_check = (
                                self.rate_limiter.config.rate_limit_error_check
                                or RateLimiter.is_rate_limit_error
                            )
                            if error_check(e):
                                raise e
                            else:
                                return response
                    return response

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


class RateLimitedHTTPXAsyncTransport(HTTPXAsyncTransport):
    """A wrapper around HTTPXAsyncTransport that applies rate limiting to GraphQL requests."""

    def __init__(self, base_transport: GqlHTTPXAsyncTransport, rate_limit_config: RateLimitConfig):
        # Copy all attributes from base transport, but exclude 'execute' to avoid shadowing our method
        base_dict = {k: v for k, v in base_transport.__dict__.items() if k != "execute"}
        self.__dict__.update(base_dict)
        self.base_transport = base_transport
        self.rate_limiter = RateLimiter[Callable[[], Any], Any](rate_limit_config)

    async def connect(self):
        """Connect the underlying transport and replace its client with a rate-limited one."""
        await self.base_transport.connect()

        # Replace the base transport's client with a rate-limited version
        if hasattr(self.base_transport, "client") and self.base_transport.client:
            # The transport's client should be our AsyncClient type, but we need to handle the type
            if isinstance(self.base_transport.client, AsyncClient):
                self.base_transport.client = RateLimitedClient(
                    self.base_transport.client, self.rate_limiter.config
                )

        # Copy the client reference
        self.client = self.base_transport.client

    async def execute(
        self,
        document: DocumentNode,
        variable_values: dict[str, Any] | None = None,
        operation_name: str | None = None,
        extra_args: dict[str, Any] | None = None,
        upload_files: bool = False,
    ):
        """Execute a GraphQL request with rate limiting."""

        async def request_func():
            result = await self.base_transport.execute(
                document=document,
                variable_values=variable_values,
                operation_name=operation_name,
                extra_args=extra_args,
                upload_files=upload_files,
            )
            return result

        # Use the rate limiter to execute the request
        responses = await self.rate_limiter.execute_requests([request_func], lambda x: x())
        if responses:
            return responses[0]

        raise InvalidResponseError(
            message="No response from GraphQL API",
        )

    def get_state(self) -> tuple[RateLimitConfig, float]:
        """Get the current rate limit state."""
        return self.rate_limiter.config, self.rate_limiter.current_delay

    async def close(self):
        """Close the underlying transport."""
        if hasattr(self.base_transport, "close"):
            await self.base_transport.close()

    def __getattr__(self, name):
        """Delegate attribute access to the underlying base_transport."""
        return getattr(self.base_transport, name)


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
                # We are not raising here because we want to return the responses to the caller
                # And we are not rate-limiting these, hence the raise should be on the caller
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
    _rate_limit_config: RateLimitConfig | None = None

    def __init__(self, args: Request, rate_limit_config: RateLimitConfig | None = None):
        client = self.build_client(args, rate_limit_config)
        super().__init__(client=client)

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
    def build_client(
        cls, args: Request, rate_limit_config: RateLimitConfig | None = None
    ) -> Client:
        client_args = cls.prepare_client_args(args)

        # Apply rate limiting if configured
        rate_limiting = rate_limit_config or cls._rate_limit_config
        if rate_limiting is not None and "transport" in client_args:
            transport = client_args["transport"]
            # wrap any gql HTTPX transport (tests use the GqlHTTPXAsyncTransport, client uses the SDK's HTTPXAsyncTransport)
            if isinstance(transport, GqlHTTPXAsyncTransport):
                client_args["transport"] = RateLimitedHTTPXAsyncTransport(transport, rate_limiting)

        return Client(**client_args)

    def get_current_rate_limits(self) -> tuple[RateLimitConfig | None, float]:
        """
        Get the current rate limit state.

        Returns a tuple of the rate limit config and the current delay. (or None if the client is not rate limited)
        """
        if hasattr(self.client, "transport") and isinstance(
            self.client.transport, RateLimitedHTTPXAsyncTransport
        ):
            return self.client.transport.get_state()
        return None, 0

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
            raise InvalidResponseError(
                message="Failed to fetch schema",
            )

        return DSLSchema(self.client.schema)
