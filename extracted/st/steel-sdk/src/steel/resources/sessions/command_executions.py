# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._utils import path_template
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.sessions.command_execution_cancel_response import CommandExecutionCancelResponse
from ...types.sessions.command_execution_retrieve_response import CommandExecutionRetrieveResponse

__all__ = ["CommandExecutionsResource", "AsyncCommandExecutionsResource"]


class CommandExecutionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CommandExecutionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#accessing-raw-response-data-eg-headers
        """
        return CommandExecutionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CommandExecutionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#with_streaming_response
        """
        return CommandExecutionsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        execution_id: str,
        *,
        session_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CommandExecutionRetrieveResponse:
        """Waits up to 20 seconds for an execution to finish and returns it.

        Use it when a
        run answered with state running.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not execution_id:
            raise ValueError(f"Expected a non-empty value for `execution_id` but received {execution_id!r}")
        return self._get(
            path_template(
                "/v1/sessions/{session_id}/commands/executions/{execution_id}",
                session_id=session_id,
                execution_id=execution_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CommandExecutionRetrieveResponse,
        )

    def cancel(
        self,
        execution_id: str,
        *,
        session_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CommandExecutionCancelResponse:
        """Stops an execution.

        The running command stops before its next input, and
        commands that already ran are not undone.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not execution_id:
            raise ValueError(f"Expected a non-empty value for `execution_id` but received {execution_id!r}")
        return self._post(
            path_template(
                "/v1/sessions/{session_id}/commands/executions/{execution_id}/cancel",
                session_id=session_id,
                execution_id=execution_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CommandExecutionCancelResponse,
        )


class AsyncCommandExecutionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCommandExecutionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#accessing-raw-response-data-eg-headers
        """
        return AsyncCommandExecutionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCommandExecutionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#with_streaming_response
        """
        return AsyncCommandExecutionsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        execution_id: str,
        *,
        session_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CommandExecutionRetrieveResponse:
        """Waits up to 20 seconds for an execution to finish and returns it.

        Use it when a
        run answered with state running.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not execution_id:
            raise ValueError(f"Expected a non-empty value for `execution_id` but received {execution_id!r}")
        return await self._get(
            path_template(
                "/v1/sessions/{session_id}/commands/executions/{execution_id}",
                session_id=session_id,
                execution_id=execution_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CommandExecutionRetrieveResponse,
        )

    async def cancel(
        self,
        execution_id: str,
        *,
        session_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CommandExecutionCancelResponse:
        """Stops an execution.

        The running command stops before its next input, and
        commands that already ran are not undone.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not execution_id:
            raise ValueError(f"Expected a non-empty value for `execution_id` but received {execution_id!r}")
        return await self._post(
            path_template(
                "/v1/sessions/{session_id}/commands/executions/{execution_id}/cancel",
                session_id=session_id,
                execution_id=execution_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CommandExecutionCancelResponse,
        )


class CommandExecutionsResourceWithRawResponse:
    def __init__(self, command_executions: CommandExecutionsResource) -> None:
        self._command_executions = command_executions

        self.retrieve = to_raw_response_wrapper(
            command_executions.retrieve,
        )
        self.cancel = to_raw_response_wrapper(
            command_executions.cancel,
        )


class AsyncCommandExecutionsResourceWithRawResponse:
    def __init__(self, command_executions: AsyncCommandExecutionsResource) -> None:
        self._command_executions = command_executions

        self.retrieve = async_to_raw_response_wrapper(
            command_executions.retrieve,
        )
        self.cancel = async_to_raw_response_wrapper(
            command_executions.cancel,
        )


class CommandExecutionsResourceWithStreamingResponse:
    def __init__(self, command_executions: CommandExecutionsResource) -> None:
        self._command_executions = command_executions

        self.retrieve = to_streamed_response_wrapper(
            command_executions.retrieve,
        )
        self.cancel = to_streamed_response_wrapper(
            command_executions.cancel,
        )


class AsyncCommandExecutionsResourceWithStreamingResponse:
    def __init__(self, command_executions: AsyncCommandExecutionsResource) -> None:
        self._command_executions = command_executions

        self.retrieve = async_to_streamed_response_wrapper(
            command_executions.retrieve,
        )
        self.cancel = async_to_streamed_response_wrapper(
            command_executions.cancel,
        )
