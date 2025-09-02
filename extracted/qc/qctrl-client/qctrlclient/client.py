# Copyright 2025 Q-CTRL. All rights reserved.
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

from typing import TYPE_CHECKING, Any, Callable

import gql
from gql.transport.exceptions import (
    TransportQueryError,
    TransportServerError,
)
from graphql import (
    DocumentNode,
    ExecutableDefinitionNode,
    FieldNode,
    print_schema,
)
from tenacity import (
    Retrying,
    retry_if_exception,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from .exceptions import (
    GraphQLQueryError,
)
from .transports import RequestsTransport

if TYPE_CHECKING:
    from collections.abc import Iterable

    from gql.transport import Transport
    from tenacity.retry import RetryBaseT
    from tenacity.wait import WaitBaseT

    from .auth.base import BaseAuth


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


class GraphQLClient:
    """Client implementation for making requests to the Q-CTRL GraphQL API."""

    DEFAULT_MAX_ATTEMPTS = 5
    DEFAULT_RETRY_DELAY_STRATEGY = wait_exponential(multiplier=0.3)

    def __init__(
        self,
        url: str,
        auth: BaseAuth | None = None,
        headers: dict[str, Any] | None = None,
        schema: str | None = None,
        fetch_schema_from_transport: bool = True,
        transport_cls: type[Transport] = RequestsTransport,
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
        transport_cls : type[Transport], optional
            The transport class to be used by the gql.Client instance.
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

        transport_options = transport_options or {}
        transport_kwargs = _prepare_kwargs(
            transport_options,
            url=url,
            headers=headers or {},
            auth=auth,
        )

        transport = transport_cls(**transport_kwargs)

        client_options = client_options or {}
        client_kwargs = _prepare_kwargs(
            client_options,
            schema=schema,
            transport=transport,
            fetch_schema_from_transport=fetch_schema_from_transport,
        )

        self._client = gql.Client(**client_kwargs)

    def get_access_token(self) -> str:
        """Returns an access token."""
        if self._auth is None:
            raise RuntimeError("Client is not authenticated.")

        return self._auth.access_token

    def execute(
        self,
        query: DocumentNode | str,
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
        self, query: DocumentNode | str, variable_values: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Executes a GraphQL query/mutation without retries."""
        if variable_values is None:
            variable_values = {}

        if isinstance(query, DocumentNode):
            document = query
        else:
            document = gql.gql(query)

        result = self._client.execute(document, variable_values=variable_values)
        self._check_errors(document, result)
        return result

    def _check_errors(
        self,
        document: DocumentNode,
        result: dict[str, Any],
    ) -> None:
        """Checks for any query-level errors returned from the query request.

        Parameters
        ----------
        document: DocumentNode
            The GraphQL document which was executed.
        result: dict
            The result of the query execution, as returned from
            gql.Client.execute
        """
        # search result for query errors
        for node in _get_query_field_nodes(document):
            if node.alias:
                query_key = node.alias.value
            else:
                query_key = node.name.value

            if result.get(query_key, {}).get("errors"):
                self._handle_query_error(query_key, result[query_key])

    def get_schema(self) -> str:
        """Get Schema from gql.Client."""
        with self._client as session:
            session.fetch_schema()

        if not self._client.schema:
            raise ValueError("Schema cannot be empty")

        return print_schema(self._client.schema)

    @classmethod
    def _get_retry(
        cls,
        max_attempts: int,
        retry_delay_strategy: WaitBaseT,
    ) -> Retrying:
        return Retrying(
            retry=cls._get_retry_condition(),
            wait=retry_delay_strategy,
            stop=stop_after_attempt(max_attempts),
            reraise=True,
        )

    @classmethod
    def _get_retry_condition(cls) -> RetryBaseT:
        return retry_if_exception_type(
            (TransportServerError, ConnectionError)
        ) | retry_if_exception(_is_graphql_internal_server_error)


def _get_query_field_nodes(
    document: DocumentNode,
) -> Iterable[FieldNode]:
    for definition_node in document.definitions:
        if isinstance(definition_node, ExecutableDefinitionNode):
            for selection_node in definition_node.selection_set.selections:
                if isinstance(selection_node, FieldNode):
                    yield selection_node
