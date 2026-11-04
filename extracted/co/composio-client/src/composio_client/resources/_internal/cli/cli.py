# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client._internal.cli`` — the generated resource classes.

``CliResource`` (sync) and ``AsyncCliResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Literal

import httpx
from typing_extensions import overload

from ...._base_client import BodyParam, HeaderParam, QueryParam, RequestOptions
from ...._models import CliCreateCodactFailureBody, CliCreateSessionBody
from ...._operations import OPERATIONS_BY_CHAIN
from ...._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from ...._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, omit
from ....types import cli_create_codact_failure_params
from ....types.cli_create_codact_failure_response import CliCreateCodactFailureResponse
from ....types.cli_create_session_response import CliCreateSessionResponse
from ....types.cli_get_session_response import CliGetSessionResponse
from ..._base import (
    AsyncAPIResource,
    SyncAPIResource,
    compact,
    make_request_options,
    merge_body,
    merge_mapping,
    require_fields,
)
from .realtime import AsyncRealtimeResource, RealtimeResource

if TYPE_CHECKING:
    from ...._base_client import AsyncAPIClient, SyncAPIClient

_CREATE_CODACT_FAILURE_OPERATION = OPERATIONS_BY_CHAIN[("_internal", "cli", "create_codact_failure")]
_CREATE_SESSION_OPERATION = OPERATIONS_BY_CHAIN[("_internal", "cli", "create_session")]
_GET_SESSION_OPERATION = OPERATIONS_BY_CHAIN[("_internal", "cli", "get_session")]


class CliResource(SyncAPIResource):
    realtime: RealtimeResource

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.realtime = RealtimeResource(client)

    @cached_property
    def with_raw_response(self) -> CliResourceWithRawResponse:
        return CliResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CliResourceWithStreamingResponse:
        return CliResourceWithStreamingResponse(self)

    # Declared header parameter(s): x-user-api-key (required).
    @overload
    def create_codact_failure(
        self,
        body: BodyParam | None = None,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"],
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None],
        session: dict[str, object | None],
        request_id: str | Omit = omit,
        x_user_api_key: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> CliCreateCodactFailureResponse: ...

    @overload
    def create_codact_failure(
        self,
        body: BodyParam,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"] | Omit = omit,
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None] | Omit = omit,
        session: dict[str, object | None] | Omit = omit,
        request_id: str | Omit = omit,
        x_user_api_key: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> CliCreateCodactFailureResponse: ...

    @overload
    def create_codact_failure(
        self,
        body: BodyParam | None = None,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"],
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None],
        session: dict[str, object | None],
        request_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> CliCreateCodactFailureResponse: ...

    @overload
    def create_codact_failure(
        self,
        body: BodyParam,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"] | Omit = omit,
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None] | Omit = omit,
        session: dict[str, object | None] | Omit = omit,
        request_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> CliCreateCodactFailureResponse: ...

    def create_codact_failure(
        self,
        body: BodyParam | None = None,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"] | Omit = omit,
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None] | Omit = omit,
        session: dict[str, object | None] | Omit = omit,
        request_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> CliCreateCodactFailureResponse:
        body_fields = compact(
            {
                "failure_type": failure_type,
                "tool_info": tool_info,
                "ctx": ctx,
                "session": session,
                "request_id": request_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("failure_type", "ctx", "session"),
            "body",
        )
        body_data = merge_body(body, body_fields)
        header_fields = compact(
            {
                "x-user-api-key": x_user_api_key,
            }
        )
        require_fields(
            headers,
            header_fields,
            ("x-user-api-key",),
            "header",
        )
        headers_data = merge_mapping(headers, header_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "post",
            "/api/v3.1/cli/codact_failures",
            cast_to=CliCreateCodactFailureResponse,
            operation=_CREATE_CODACT_FAILURE_OPERATION,
            body=body_data,
            body_model=CliCreateCodactFailureBody,
            operation_headers=headers_data,
            options=options_data,
        )

    def create_session(
        self,
        body: BodyParam | None = None,
        *,
        scope: Literal["project", "user"] | Omit = omit,
        source: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CliCreateSessionResponse:
        body_fields = compact(
            {
                "scope": scope,
                "source": source,
            }
        )
        body_data = merge_body(body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "post",
            "/api/v3.1/cli/create-session",
            cast_to=CliCreateSessionResponse,
            operation=_CREATE_SESSION_OPERATION,
            body=body_data,
            body_model=CliCreateSessionBody,
            options=options_data,
        )

    @overload
    def get_session(
        self,
        *,
        id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> CliGetSessionResponse: ...

    @overload
    def get_session(
        self,
        *,
        id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam,
        request_options: RequestOptions | None = None,
    ) -> CliGetSessionResponse: ...

    def get_session(
        self,
        *,
        id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> CliGetSessionResponse:
        query_fields = compact(
            {
                "id": id,
            }
        )
        require_fields(
            query,
            query_fields,
            ("id",),
            "query",
        )
        query_data = merge_mapping(query, query_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "get",
            "/api/v3.1/cli/get-session",
            cast_to=CliGetSessionResponse,
            operation=_GET_SESSION_OPERATION,
            query=query_data,
            options=options_data,
        )


class AsyncCliResource(AsyncAPIResource):
    realtime: AsyncRealtimeResource

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.realtime = AsyncRealtimeResource(client)

    @cached_property
    def with_raw_response(self) -> AsyncCliResourceWithRawResponse:
        return AsyncCliResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCliResourceWithStreamingResponse:
        return AsyncCliResourceWithStreamingResponse(self)

    # Declared header parameter(s): x-user-api-key (required).
    @overload
    async def create_codact_failure(
        self,
        body: BodyParam | None = None,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"],
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None],
        session: dict[str, object | None],
        request_id: str | Omit = omit,
        x_user_api_key: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> CliCreateCodactFailureResponse: ...

    @overload
    async def create_codact_failure(
        self,
        body: BodyParam,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"] | Omit = omit,
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None] | Omit = omit,
        session: dict[str, object | None] | Omit = omit,
        request_id: str | Omit = omit,
        x_user_api_key: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> CliCreateCodactFailureResponse: ...

    @overload
    async def create_codact_failure(
        self,
        body: BodyParam | None = None,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"],
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None],
        session: dict[str, object | None],
        request_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> CliCreateCodactFailureResponse: ...

    @overload
    async def create_codact_failure(
        self,
        body: BodyParam,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"] | Omit = omit,
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None] | Omit = omit,
        session: dict[str, object | None] | Omit = omit,
        request_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> CliCreateCodactFailureResponse: ...

    async def create_codact_failure(
        self,
        body: BodyParam | None = None,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"] | Omit = omit,
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None] | Omit = omit,
        session: dict[str, object | None] | Omit = omit,
        request_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> CliCreateCodactFailureResponse:
        body_fields = compact(
            {
                "failure_type": failure_type,
                "tool_info": tool_info,
                "ctx": ctx,
                "session": session,
                "request_id": request_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("failure_type", "ctx", "session"),
            "body",
        )
        body_data = merge_body(body, body_fields)
        header_fields = compact(
            {
                "x-user-api-key": x_user_api_key,
            }
        )
        require_fields(
            headers,
            header_fields,
            ("x-user-api-key",),
            "header",
        )
        headers_data = merge_mapping(headers, header_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "post",
            "/api/v3.1/cli/codact_failures",
            cast_to=CliCreateCodactFailureResponse,
            operation=_CREATE_CODACT_FAILURE_OPERATION,
            body=body_data,
            body_model=CliCreateCodactFailureBody,
            operation_headers=headers_data,
            options=options_data,
        )

    async def create_session(
        self,
        body: BodyParam | None = None,
        *,
        scope: Literal["project", "user"] | Omit = omit,
        source: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CliCreateSessionResponse:
        body_fields = compact(
            {
                "scope": scope,
                "source": source,
            }
        )
        body_data = merge_body(body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "post",
            "/api/v3.1/cli/create-session",
            cast_to=CliCreateSessionResponse,
            operation=_CREATE_SESSION_OPERATION,
            body=body_data,
            body_model=CliCreateSessionBody,
            options=options_data,
        )

    @overload
    async def get_session(
        self,
        *,
        id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> CliGetSessionResponse: ...

    @overload
    async def get_session(
        self,
        *,
        id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam,
        request_options: RequestOptions | None = None,
    ) -> CliGetSessionResponse: ...

    async def get_session(
        self,
        *,
        id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> CliGetSessionResponse:
        query_fields = compact(
            {
                "id": id,
            }
        )
        require_fields(
            query,
            query_fields,
            ("id",),
            "query",
        )
        query_data = merge_mapping(query, query_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "get",
            "/api/v3.1/cli/get-session",
            cast_to=CliGetSessionResponse,
            operation=_GET_SESSION_OPERATION,
            query=query_data,
            options=options_data,
        )


class CliResourceWithRawResponse:
    def __init__(self, resource: CliResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Declared header parameter(s): x-user-api-key (required).
    @overload
    def create_codact_failure(
        self,
        body: BodyParam | None = None,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"],
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None],
        session: dict[str, object | None],
        request_id: str | Omit = omit,
        x_user_api_key: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CliCreateCodactFailureResponse]: ...

    @overload
    def create_codact_failure(
        self,
        body: BodyParam,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"] | Omit = omit,
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None] | Omit = omit,
        session: dict[str, object | None] | Omit = omit,
        request_id: str | Omit = omit,
        x_user_api_key: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CliCreateCodactFailureResponse]: ...

    @overload
    def create_codact_failure(
        self,
        body: BodyParam | None = None,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"],
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None],
        session: dict[str, object | None],
        request_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CliCreateCodactFailureResponse]: ...

    @overload
    def create_codact_failure(
        self,
        body: BodyParam,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"] | Omit = omit,
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None] | Omit = omit,
        session: dict[str, object | None] | Omit = omit,
        request_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CliCreateCodactFailureResponse]: ...

    def create_codact_failure(
        self,
        body: BodyParam | None = None,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"] | Omit = omit,
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None] | Omit = omit,
        session: dict[str, object | None] | Omit = omit,
        request_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CliCreateCodactFailureResponse]:
        body_fields = compact(
            {
                "failure_type": failure_type,
                "tool_info": tool_info,
                "ctx": ctx,
                "session": session,
                "request_id": request_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("failure_type", "ctx", "session"),
            "body",
        )
        body_data = merge_body(body, body_fields)
        header_fields = compact(
            {
                "x-user-api-key": x_user_api_key,
            }
        )
        require_fields(
            headers,
            header_fields,
            ("x-user-api-key",),
            "header",
        )
        headers_data = merge_mapping(headers, header_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "post",
            "/api/v3.1/cli/codact_failures",
            cast_to=CliCreateCodactFailureResponse,
            operation=_CREATE_CODACT_FAILURE_OPERATION,
            body=body_data,
            body_model=CliCreateCodactFailureBody,
            operation_headers=headers_data,
            options=options_data,
        )

    def create_session(
        self,
        body: BodyParam | None = None,
        *,
        scope: Literal["project", "user"] | Omit = omit,
        source: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CliCreateSessionResponse]:
        body_fields = compact(
            {
                "scope": scope,
                "source": source,
            }
        )
        body_data = merge_body(body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "post",
            "/api/v3.1/cli/create-session",
            cast_to=CliCreateSessionResponse,
            operation=_CREATE_SESSION_OPERATION,
            body=body_data,
            body_model=CliCreateSessionBody,
            options=options_data,
        )

    @overload
    def get_session(
        self,
        *,
        id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CliGetSessionResponse]: ...

    @overload
    def get_session(
        self,
        *,
        id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CliGetSessionResponse]: ...

    def get_session(
        self,
        *,
        id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CliGetSessionResponse]:
        query_fields = compact(
            {
                "id": id,
            }
        )
        require_fields(
            query,
            query_fields,
            ("id",),
            "query",
        )
        query_data = merge_mapping(query, query_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "get",
            "/api/v3.1/cli/get-session",
            cast_to=CliGetSessionResponse,
            operation=_GET_SESSION_OPERATION,
            query=query_data,
            options=options_data,
        )


class AsyncCliResourceWithRawResponse:
    def __init__(self, resource: AsyncCliResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Declared header parameter(s): x-user-api-key (required).
    @overload
    async def create_codact_failure(
        self,
        body: BodyParam | None = None,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"],
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None],
        session: dict[str, object | None],
        request_id: str | Omit = omit,
        x_user_api_key: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CliCreateCodactFailureResponse]: ...

    @overload
    async def create_codact_failure(
        self,
        body: BodyParam,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"] | Omit = omit,
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None] | Omit = omit,
        session: dict[str, object | None] | Omit = omit,
        request_id: str | Omit = omit,
        x_user_api_key: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CliCreateCodactFailureResponse]: ...

    @overload
    async def create_codact_failure(
        self,
        body: BodyParam | None = None,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"],
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None],
        session: dict[str, object | None],
        request_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CliCreateCodactFailureResponse]: ...

    @overload
    async def create_codact_failure(
        self,
        body: BodyParam,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"] | Omit = omit,
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None] | Omit = omit,
        session: dict[str, object | None] | Omit = omit,
        request_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CliCreateCodactFailureResponse]: ...

    async def create_codact_failure(
        self,
        body: BodyParam | None = None,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"] | Omit = omit,
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None] | Omit = omit,
        session: dict[str, object | None] | Omit = omit,
        request_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CliCreateCodactFailureResponse]:
        body_fields = compact(
            {
                "failure_type": failure_type,
                "tool_info": tool_info,
                "ctx": ctx,
                "session": session,
                "request_id": request_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("failure_type", "ctx", "session"),
            "body",
        )
        body_data = merge_body(body, body_fields)
        header_fields = compact(
            {
                "x-user-api-key": x_user_api_key,
            }
        )
        require_fields(
            headers,
            header_fields,
            ("x-user-api-key",),
            "header",
        )
        headers_data = merge_mapping(headers, header_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "post",
            "/api/v3.1/cli/codact_failures",
            cast_to=CliCreateCodactFailureResponse,
            operation=_CREATE_CODACT_FAILURE_OPERATION,
            body=body_data,
            body_model=CliCreateCodactFailureBody,
            operation_headers=headers_data,
            options=options_data,
        )

    async def create_session(
        self,
        body: BodyParam | None = None,
        *,
        scope: Literal["project", "user"] | Omit = omit,
        source: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CliCreateSessionResponse]:
        body_fields = compact(
            {
                "scope": scope,
                "source": source,
            }
        )
        body_data = merge_body(body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "post",
            "/api/v3.1/cli/create-session",
            cast_to=CliCreateSessionResponse,
            operation=_CREATE_SESSION_OPERATION,
            body=body_data,
            body_model=CliCreateSessionBody,
            options=options_data,
        )

    @overload
    async def get_session(
        self,
        *,
        id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CliGetSessionResponse]: ...

    @overload
    async def get_session(
        self,
        *,
        id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CliGetSessionResponse]: ...

    async def get_session(
        self,
        *,
        id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CliGetSessionResponse]:
        query_fields = compact(
            {
                "id": id,
            }
        )
        require_fields(
            query,
            query_fields,
            ("id",),
            "query",
        )
        query_data = merge_mapping(query, query_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "get",
            "/api/v3.1/cli/get-session",
            cast_to=CliGetSessionResponse,
            operation=_GET_SESSION_OPERATION,
            query=query_data,
            options=options_data,
        )


class CliResourceWithStreamingResponse:
    def __init__(self, resource: CliResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Declared header parameter(s): x-user-api-key (required).
    @overload
    def create_codact_failure(
        self,
        body: BodyParam | None = None,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"],
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None],
        session: dict[str, object | None],
        request_id: str | Omit = omit,
        x_user_api_key: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CliCreateCodactFailureResponse]]: ...

    @overload
    def create_codact_failure(
        self,
        body: BodyParam,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"] | Omit = omit,
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None] | Omit = omit,
        session: dict[str, object | None] | Omit = omit,
        request_id: str | Omit = omit,
        x_user_api_key: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CliCreateCodactFailureResponse]]: ...

    @overload
    def create_codact_failure(
        self,
        body: BodyParam | None = None,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"],
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None],
        session: dict[str, object | None],
        request_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CliCreateCodactFailureResponse]]: ...

    @overload
    def create_codact_failure(
        self,
        body: BodyParam,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"] | Omit = omit,
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None] | Omit = omit,
        session: dict[str, object | None] | Omit = omit,
        request_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CliCreateCodactFailureResponse]]: ...

    def create_codact_failure(
        self,
        body: BodyParam | None = None,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"] | Omit = omit,
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None] | Omit = omit,
        session: dict[str, object | None] | Omit = omit,
        request_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CliCreateCodactFailureResponse]]:
        body_fields = compact(
            {
                "failure_type": failure_type,
                "tool_info": tool_info,
                "ctx": ctx,
                "session": session,
                "request_id": request_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("failure_type", "ctx", "session"),
            "body",
        )
        body_data = merge_body(body, body_fields)
        header_fields = compact(
            {
                "x-user-api-key": x_user_api_key,
            }
        )
        require_fields(
            headers,
            header_fields,
            ("x-user-api-key",),
            "header",
        )
        headers_data = merge_mapping(headers, header_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return ResponseContextManager(
            lambda: self._client._request_raw(
                "post",
                "/api/v3.1/cli/codact_failures",
                cast_to=CliCreateCodactFailureResponse,
                operation=_CREATE_CODACT_FAILURE_OPERATION,
                body=body_data,
                body_model=CliCreateCodactFailureBody,
                operation_headers=headers_data,
                options=options_data,
                stream=True,
            )
        )

    def create_session(
        self,
        body: BodyParam | None = None,
        *,
        scope: Literal["project", "user"] | Omit = omit,
        source: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CliCreateSessionResponse]]:
        body_fields = compact(
            {
                "scope": scope,
                "source": source,
            }
        )
        body_data = merge_body(body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return ResponseContextManager(
            lambda: self._client._request_raw(
                "post",
                "/api/v3.1/cli/create-session",
                cast_to=CliCreateSessionResponse,
                operation=_CREATE_SESSION_OPERATION,
                body=body_data,
                body_model=CliCreateSessionBody,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def get_session(
        self,
        *,
        id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CliGetSessionResponse]]: ...

    @overload
    def get_session(
        self,
        *,
        id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CliGetSessionResponse]]: ...

    def get_session(
        self,
        *,
        id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CliGetSessionResponse]]:
        query_fields = compact(
            {
                "id": id,
            }
        )
        require_fields(
            query,
            query_fields,
            ("id",),
            "query",
        )
        query_data = merge_mapping(query, query_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return ResponseContextManager(
            lambda: self._client._request_raw(
                "get",
                "/api/v3.1/cli/get-session",
                cast_to=CliGetSessionResponse,
                operation=_GET_SESSION_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )


class AsyncCliResourceWithStreamingResponse:
    def __init__(self, resource: AsyncCliResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Declared header parameter(s): x-user-api-key (required).
    @overload
    def create_codact_failure(
        self,
        body: BodyParam | None = None,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"],
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None],
        session: dict[str, object | None],
        request_id: str | Omit = omit,
        x_user_api_key: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CliCreateCodactFailureResponse]]: ...

    @overload
    def create_codact_failure(
        self,
        body: BodyParam,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"] | Omit = omit,
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None] | Omit = omit,
        session: dict[str, object | None] | Omit = omit,
        request_id: str | Omit = omit,
        x_user_api_key: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CliCreateCodactFailureResponse]]: ...

    @overload
    def create_codact_failure(
        self,
        body: BodyParam | None = None,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"],
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None],
        session: dict[str, object | None],
        request_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CliCreateCodactFailureResponse]]: ...

    @overload
    def create_codact_failure(
        self,
        body: BodyParam,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"] | Omit = omit,
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None] | Omit = omit,
        session: dict[str, object | None] | Omit = omit,
        request_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CliCreateCodactFailureResponse]]: ...

    def create_codact_failure(
        self,
        body: BodyParam | None = None,
        *,
        failure_type: Literal["wrong_tool_slug", "wrong_tool_input_param"] | Omit = omit,
        tool_info: cli_create_codact_failure_params.ToolInfo | Omit = omit,
        ctx: dict[str, object | None] | Omit = omit,
        session: dict[str, object | None] | Omit = omit,
        request_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CliCreateCodactFailureResponse]]:
        body_fields = compact(
            {
                "failure_type": failure_type,
                "tool_info": tool_info,
                "ctx": ctx,
                "session": session,
                "request_id": request_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("failure_type", "ctx", "session"),
            "body",
        )
        body_data = merge_body(body, body_fields)
        header_fields = compact(
            {
                "x-user-api-key": x_user_api_key,
            }
        )
        require_fields(
            headers,
            header_fields,
            ("x-user-api-key",),
            "header",
        )
        headers_data = merge_mapping(headers, header_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return AsyncResponseContextManager(
            self._client._request_raw(
                "post",
                "/api/v3.1/cli/codact_failures",
                cast_to=CliCreateCodactFailureResponse,
                operation=_CREATE_CODACT_FAILURE_OPERATION,
                body=body_data,
                body_model=CliCreateCodactFailureBody,
                operation_headers=headers_data,
                options=options_data,
                stream=True,
            )
        )

    def create_session(
        self,
        body: BodyParam | None = None,
        *,
        scope: Literal["project", "user"] | Omit = omit,
        source: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CliCreateSessionResponse]]:
        body_fields = compact(
            {
                "scope": scope,
                "source": source,
            }
        )
        body_data = merge_body(body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return AsyncResponseContextManager(
            self._client._request_raw(
                "post",
                "/api/v3.1/cli/create-session",
                cast_to=CliCreateSessionResponse,
                operation=_CREATE_SESSION_OPERATION,
                body=body_data,
                body_model=CliCreateSessionBody,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def get_session(
        self,
        *,
        id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CliGetSessionResponse]]: ...

    @overload
    def get_session(
        self,
        *,
        id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CliGetSessionResponse]]: ...

    def get_session(
        self,
        *,
        id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CliGetSessionResponse]]:
        query_fields = compact(
            {
                "id": id,
            }
        )
        require_fields(
            query,
            query_fields,
            ("id",),
            "query",
        )
        query_data = merge_mapping(query, query_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return AsyncResponseContextManager(
            self._client._request_raw(
                "get",
                "/api/v3.1/cli/get-session",
                cast_to=CliGetSessionResponse,
                operation=_GET_SESSION_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )
