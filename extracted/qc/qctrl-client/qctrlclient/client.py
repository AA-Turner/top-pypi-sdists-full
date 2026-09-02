# Copyright 2026 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any, ClassVar, NamedTuple, TypedDict

import gql
from gql import Client
from gql.graphql_request import GraphQLRequest
from gql.transport.exceptions import TransportQueryError, TransportServerError
from gql.transport.httpx import HTTPXAsyncTransport, HTTPXTransport
from graphql import ExecutableDefinitionNode, FieldNode, print_schema
from httpx import Timeout
from tenacity import (
    AsyncRetrying,
    Retrying,
    retry_if_exception,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from .consistency_headers import HttpxConsistencyHandler, SimpleTokenCache, TokenCache
from .exceptions import GraphQLQueryError

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from tenacity.retry import RetryBaseT
    from tenacity.wait import WaitBaseT

    from .auth.base import BaseAuth


DEFAULT_MAX_ATTEMPTS = 5
DEFAULT_RETRY_DELAY_STRATEGY = wait_exponential(multiplier=0.3)
DEFAULT_REQUEST_TIMEOUT = Timeout(60.0)


class _GQLExecuteArguments(NamedTuple):
    # NOTE: `request` needs to be provided as a positional arg to gql execute to work with Sentry patching
    request: GraphQLRequest
    kwargs: _GQLExecuteKeywordArguments


class _GQLExecuteKeywordArguments(TypedDict):
    """Keyword arguments for the `execute` method of the GraphQL client."""

    extra_args: dict[str, Any]


def _default_handle_query_error(key: str, data: dict[str, Any]) -> None:  # noqa: ARG001
    """
    Handles query level errors.

    Parameters
    ----------
    key : str
        The query name or alias key.
    data : dict
        The query result returned from gql.Client.

    Raises
    ------
    GraphQLQueryError
        If there are any errors.
    """
    raise GraphQLQueryError(data["errors"])


def _prepare_kwargs(
    user_options: dict[str, Any], **mandatory_kwargs: Any
) -> dict[str, Any]:
    """
    Combines mandatory keyword arguments with options
    provided by the user.

    Parameters
    ----------
    user_options : Dict[str,Any]
        Keyword arguments requested by the user.
    mandatory_kwargs : Any
        Keyword arguments that must be included in the
        result.

    Returns
    -------
    Dict[str,Any]

    Raises
    ------
    RuntimeError
        If any keyword arguments requested by the user
        conflict with any mandatory keyword arguments.
    """
    kwargs = mandatory_kwargs.copy()

    for name, value in user_options.items():
        if name in kwargs:
            raise RuntimeError(f"Unable to specify keyword argument: {name}")

        kwargs[name] = value

    return kwargs


def _is_graphql_internal_server_error(exception: BaseException) -> bool:
    """
    Checks if the exception is a GraphQL internal server
    error which should trigger a retry.

    Parameters
    ----------
    exception : BaseException
        The exception raised by the client.

    Returns
    -------
    bool
    """
    if isinstance(exception, TransportQueryError):
        return "INTERNAL_SERVER_ERROR" in str(exception)

    return False


class _BaseGraphQLClient(abc.ABC):
    """Base GraphQL client definition."""

    transport_cls: ClassVar[type[HTTPXTransport | HTTPXAsyncTransport]]

    def __init__(
        self,
        url: str,
        auth: BaseAuth | None = None,
        consistency_token_cache: TokenCache | None = None,
        headers: dict[str, Any] | None = None,
        schema: str | None = None,
        fetch_schema_from_transport: bool = True,
        timeout: Timeout = DEFAULT_REQUEST_TIMEOUT,
        transport_options: dict[str, Any] | None = None,
        client_options: dict[str, Any] | None = None,
        handle_query_error: Callable[
            [str, dict[str, Any]], None
        ] = _default_handle_query_error,
    ):
        """
        Parameters
        ----------
        url : str
            The endpoint for the graphql request.
        headers : dict
            The dictionary of http headers.
        auth : BaseAuthHandler, optional
            An instance of an authentication object. (Default value = None)
        schema : list of str, Optional
            The string version of the GQL schema. (Default value = None)
        fetch_schema_from_transport : bool
            Whether the schema should be fetched from the transport using an introspection query. (Default value = True)
        timeout : Timeout
            A `httpx.Timeout` object specifying timeout parameters for graphql requests. (Default value = Timeout(60.0))
        transport_options : dict
            Custom arguments to the used transport instance. (Default value = None)
        client_options : dict
            Custom arguments to the created gql.Client instance. (Default value = None)
        handle_query_error : Callable
            Hook function called if any query level errors are found. The callable
            should accept two arguments - the query key and the query result. Default
            behaviour is to raise a GraphQLQueryError.
        """
        self._auth = auth
        self._handle_query_error = handle_query_error

        self._consistency_handler = HttpxConsistencyHandler(
            consistency_token_cache
            if consistency_token_cache is not None
            else SimpleTokenCache()
        )
        self._transport_args = _prepare_transport_args(
            url,
            headers,
            timeout,
            self._consistency_handler,
            transport_options,
            async_hooks=issubclass(self.transport_cls, HTTPXAsyncTransport),
        )
        self._timeout = timeout
        self._client_options = client_options
        self._schema = schema
        self._fetch_schema_from_transport = fetch_schema_from_transport

    @property
    def _transport(self) -> HTTPXTransport | HTTPXAsyncTransport:
        """Returns a new gql.Transport instance."""
        return self.transport_cls(**self._transport_args)

    @property
    def _client(self) -> Client:
        """Returns a new gql.Client instance."""
        return _prepare_gql_client(
            client_options=self._client_options,
            schema=self._schema,
            transport=self._transport,
            fetch_schema_from_transport=self._fetch_schema_from_transport,
            execute_timeout=self._timeout.read,
        )


class GraphQLClient(_BaseGraphQLClient):
    """Client implementation for making requests to the Q-CTRL GraphQL API."""

    transport_cls = HTTPXTransport

    def execute(
        self,
        query: GraphQLRequest | str,
        variable_values: dict[str, Any] | None = None,
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
        retry_delay_strategy: WaitBaseT = DEFAULT_RETRY_DELAY_STRATEGY,
    ) -> dict[str, Any]:
        """Executes a GraphQL query/mutation with retries."""
        wrapped_func = self._get_retry(
            max_attempts=max_attempts,
            retry_delay_strategy=retry_delay_strategy,
        ).wraps(self.execute_once)
        return wrapped_func(query, variable_values)

    def execute_once(
        self, query: GraphQLRequest | str, variable_values: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Executes a GraphQL query/mutation without retries."""
        request, kwargs = _prepare_execute_args(
            query=query, variable_values=variable_values, auth=self._auth
        )

        # NOTE: `request` needs to be provided as a positional arg to work with Sentry patching
        result = self._client.execute(request, **kwargs)

        _check_errors(request, result, self._handle_query_error)
        return result

    def get_schema(self) -> str:
        """Get Schema from gql.Client."""
        client = self._client  # Retain the client instance for schema fetching
        with client as session:
            session.fetch_schema()

        if not client.schema:
            raise ValueError("Schema cannot be empty")

        return print_schema(client.schema)

    @classmethod
    def _get_retry(
        cls,
        max_attempts: int,
        retry_delay_strategy: WaitBaseT,
    ) -> Retrying:
        args = _get_tenacity_retry_args(
            max_attempts=max_attempts,
            retry_delay_strategy=retry_delay_strategy,
        )
        return Retrying(**args)


class GraphQLAsyncClient(_BaseGraphQLClient):
    """Async client implementation for making requests to the Q-CTRL GraphQL API."""

    transport_cls = HTTPXAsyncTransport

    async def execute(
        self,
        query: GraphQLRequest | str,
        variable_values: dict[str, Any] | None = None,
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
        retry_delay_strategy: WaitBaseT = DEFAULT_RETRY_DELAY_STRATEGY,
    ) -> dict[str, Any]:
        """Executes a GraphQL query/mutation with retries."""
        wrapped_func = self._get_retry(
            max_attempts=max_attempts,
            retry_delay_strategy=retry_delay_strategy,
        ).wraps(self.execute_once)
        return await wrapped_func(query, variable_values)

    async def execute_once(
        self, query: GraphQLRequest | str, variable_values: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Executes a GraphQL query/mutation without retries."""
        request, kwargs = _prepare_execute_args(
            query=query, variable_values=variable_values, auth=self._auth
        )

        # NOTE: `request` needs to be provided as a positional arg to work with Sentry patching
        result = await self._client.execute_async(request, **kwargs)

        _check_errors(request, result, self._handle_query_error)
        return result

    async def get_schema(self) -> str:
        """Get Schema from gql.Client."""
        client = self._client  # Retain the client instance for schema fetching
        async with client as session:
            await session.fetch_schema()

        if not client.schema:
            raise ValueError("Schema cannot be empty")

        return print_schema(client.schema)

    @classmethod
    def _get_retry(
        cls,
        max_attempts: int,
        retry_delay_strategy: WaitBaseT,
    ) -> AsyncRetrying:
        args = _get_tenacity_retry_args(
            max_attempts=max_attempts,
            retry_delay_strategy=retry_delay_strategy,
        )
        return AsyncRetrying(**args)


def _prepare_gql_client(
    client_options: dict[str, Any] | None,
    schema: str | None,
    transport: HTTPXTransport | HTTPXAsyncTransport,
    fetch_schema_from_transport: bool,
    execute_timeout: float | None,
) -> gql.Client:
    client_options = client_options or {}
    client_kwargs = _prepare_kwargs(
        client_options,
        schema=schema,
        transport=transport,
        fetch_schema_from_transport=fetch_schema_from_transport,
        execute_timeout=execute_timeout,
    )
    return gql.Client(**client_kwargs)


def _prepare_transport_args(
    url: str,
    headers: dict[str, Any] | None,
    timeout: Timeout,
    consistency_token_handler: HttpxConsistencyHandler,
    transport_options: dict[str, Any] | None,
    *,
    async_hooks: bool = False,
) -> dict[str, Any]:
    transport_options = transport_options or {}
    event_hooks = (
        consistency_token_handler.as_async_event_hooks()
        if async_hooks
        else consistency_token_handler.as_event_hooks()
    )
    return _prepare_kwargs(
        transport_options,
        url=url,
        headers=headers or {},
        timeout=timeout,
        event_hooks=event_hooks,
    )


def _prepare_execute_args(
    query: GraphQLRequest | str,
    variable_values: dict[str, Any] | None,
    auth: BaseAuth | None,
) -> _GQLExecuteArguments:
    if isinstance(query, GraphQLRequest):
        request = query
    else:
        request = gql.gql(query)

    if variable_values is not None:
        request.variable_values = variable_values

    # TODO (https://qctrl.atlassian.net/browse/PA-4749): Support async auth implementation
    authorization_headers = (
        {"Authorization": auth.get_authorization_header()} if auth else {}
    )

    return _GQLExecuteArguments(
        request=request,
        kwargs={
            "extra_args": {"headers": {**authorization_headers}},
        },
    )


def _check_errors(
    request: GraphQLRequest,
    result: dict[str, Any],
    handle_query_error: Callable[[str, dict[str, Any]], None],
) -> None:
    """Checks for any query-level errors returned from the query request.

    Parameters
    ----------
    request: GraphQLRequest
        The GraphQL request which was executed.
    result: dict
        The result of the query execution, as returned from
        gql.Client.execute
    """
    # search result for query errors
    for node in _get_query_field_nodes(request):
        if node.alias:
            query_key = node.alias.value
        else:
            query_key = node.name.value

        if result.get(query_key, {}).get("errors"):
            handle_query_error(query_key, result[query_key])


def _get_tenacity_retry_args(
    max_attempts: int,
    retry_delay_strategy: WaitBaseT,
) -> dict[str, Any]:
    return {
        "retry": _get_retry_condition(),
        "wait": retry_delay_strategy,
        "stop": stop_after_attempt(max_attempts),
        "reraise": True,
    }


def _get_retry_condition() -> RetryBaseT:
    return retry_if_exception_type(
        (TransportServerError, ConnectionError)
    ) | retry_if_exception(_is_graphql_internal_server_error)


def _get_query_field_nodes(
    request: GraphQLRequest,
) -> Iterable[FieldNode]:
    for definition_node in request.document.definitions:
        if isinstance(definition_node, ExecutableDefinitionNode):
            for selection_node in definition_node.selection_set.selections:
                if isinstance(selection_node, FieldNode):
                    yield selection_node
