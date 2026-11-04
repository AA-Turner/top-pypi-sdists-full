# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.tool_router.session`` — the generated resource classes.

``SessionResource`` (sync) and ``AsyncSessionResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from collections.abc import Iterable
from functools import cached_property
from typing import TYPE_CHECKING, Literal, cast

import httpx
from typing_extensions import overload

from ...._base_client import BodyParam, QueryParam, RequestOptions
from ...._models import (
    SessionAttachBody,
    SessionCreateBody,
    SessionExecuteBody,
    SessionExecuteMetaBody,
    SessionLinkBody,
    SessionPatchBody,
    SessionProxyExecuteBody,
    SessionSearchBody,
)
from ...._operations import OPERATIONS_BY_CHAIN
from ...._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from ...._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, SequenceNotStr, omit
from ....types.tool_router import (
    session_attach_params,
    session_create_params,
    session_execute_meta_params,
    session_execute_params,
    session_link_params,
    session_patch_params,
    session_proxy_execute_params,
    session_search_params,
)
from ....types.tool_router.session_attach_response import SessionAttachResponse
from ....types.tool_router.session_config_history_response import SessionConfigHistoryResponse
from ....types.tool_router.session_create_response import SessionCreateResponse
from ....types.tool_router.session_delete_response import SessionDeleteResponse
from ....types.tool_router.session_execute_meta_response import SessionExecuteMetaResult
from ....types.tool_router.session_execute_response import SessionExecuteResult
from ....types.tool_router.session_link_response import SessionLinkResponse
from ....types.tool_router.session_patch_response import SessionPatchResponse
from ....types.tool_router.session_proxy_execute_response import SessionProxyExecuteResult
from ....types.tool_router.session_retrieve_response import SessionRetrieveResponse
from ....types.tool_router.session_search_response import SessionSearchResponse
from ....types.tool_router.session_toolkits_response import SessionToolkitsResponse
from ....types.tool_router.session_tools_response import SessionToolsResponse
from ..._base import (
    AsyncAPIResource,
    SyncAPIResource,
    build_path,
    compact,
    make_request_options,
    merge_body,
    merge_mapping,
    normalize_body_argument,
    require_fields,
    split_body_argument,
)
from .files import AsyncFilesResource, FilesResource

if TYPE_CHECKING:
    from ...._base_client import AsyncAPIClient, SyncAPIClient

_CREATE_OPERATION = OPERATIONS_BY_CHAIN[("tool_router", "session", "create")]
_RETRIEVE_OPERATION = OPERATIONS_BY_CHAIN[("tool_router", "session", "retrieve")]
_DELETE_OPERATION = OPERATIONS_BY_CHAIN[("tool_router", "session", "delete")]
_ATTACH_OPERATION = OPERATIONS_BY_CHAIN[("tool_router", "session", "attach")]
_CONFIG_HISTORY_OPERATION = OPERATIONS_BY_CHAIN[("tool_router", "session", "config_history")]
_EXECUTE_OPERATION = OPERATIONS_BY_CHAIN[("tool_router", "session", "execute")]
_EXECUTE_META_OPERATION = OPERATIONS_BY_CHAIN[("tool_router", "session", "execute_meta")]
_LINK_OPERATION = OPERATIONS_BY_CHAIN[("tool_router", "session", "link")]
_PATCH_OPERATION = OPERATIONS_BY_CHAIN[("tool_router", "session", "patch")]
_PROXY_EXECUTE_OPERATION = OPERATIONS_BY_CHAIN[("tool_router", "session", "proxy_execute")]
_SEARCH_OPERATION = OPERATIONS_BY_CHAIN[("tool_router", "session", "search")]
_TOOLKITS_OPERATION = OPERATIONS_BY_CHAIN[("tool_router", "session", "toolkits")]
_TOOLS_OPERATION = OPERATIONS_BY_CHAIN[("tool_router", "session", "tools")]


class SessionResource(SyncAPIResource):
    files: FilesResource

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.files = FilesResource(client)

    @cached_property
    def with_raw_response(self) -> SessionResourceWithRawResponse:
        return SessionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SessionResourceWithStreamingResponse:
        return SessionResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        user_id: str,
        toolkits: session_create_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        instant: Literal[False] | session_create_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_create_params.ManageConnections | Omit = omit,
        tools: dict[str, session_create_params.Tools] | Omit = omit,
        tags: session_create_params.Tags | Omit = omit,
        workbench: session_create_params.Workbench | Omit = omit,
        proxy_execute: session_create_params.CurrentProxyExecute | Omit = omit,
        multi_account: session_create_params.MultiAccount | Omit = omit,
        experimental: session_create_params.Experimental | Omit = omit,
        preload: session_create_params.Preload | Omit = omit,
        hooks: Iterable[session_create_params.CurrentHookVariant0 | session_create_params.CurrentHookVariant1]
        | Omit = omit,
        search: session_create_params.Search | Omit = omit,
        execute: session_create_params.Execute | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionCreateResponse: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        user_id: str | Omit = omit,
        toolkits: session_create_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        instant: Literal[False] | session_create_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_create_params.ManageConnections | Omit = omit,
        tools: dict[str, session_create_params.Tools] | Omit = omit,
        tags: session_create_params.Tags | Omit = omit,
        workbench: session_create_params.Workbench | Omit = omit,
        proxy_execute: session_create_params.CurrentProxyExecute | Omit = omit,
        multi_account: session_create_params.MultiAccount | Omit = omit,
        experimental: session_create_params.Experimental | Omit = omit,
        preload: session_create_params.Preload | Omit = omit,
        hooks: Iterable[session_create_params.CurrentHookVariant0 | session_create_params.CurrentHookVariant1]
        | Omit = omit,
        search: session_create_params.Search | Omit = omit,
        execute: session_create_params.Execute | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionCreateResponse: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        user_id: str | Omit = omit,
        toolkits: session_create_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        instant: Literal[False] | session_create_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_create_params.ManageConnections | Omit = omit,
        tools: dict[str, session_create_params.Tools] | Omit = omit,
        tags: session_create_params.Tags | Omit = omit,
        workbench: session_create_params.Workbench | Omit = omit,
        proxy_execute: session_create_params.CurrentProxyExecute | Omit = omit,
        multi_account: session_create_params.MultiAccount | Omit = omit,
        experimental: session_create_params.Experimental | Omit = omit,
        preload: session_create_params.Preload | Omit = omit,
        hooks: Iterable[session_create_params.CurrentHookVariant0 | session_create_params.CurrentHookVariant1]
        | Omit = omit,
        search: session_create_params.Search | Omit = omit,
        execute: session_create_params.Execute | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionCreateResponse:
        body_fields = compact(
            {
                "user_id": user_id,
                "toolkits": toolkits,
                "auth_configs": auth_configs,
                "connected_accounts": connected_accounts,
                "instant": instant,
                "manage_connections": manage_connections,
                "tools": tools,
                "tags": tags,
                "workbench": workbench,
                "proxy_execute": proxy_execute,
                "multi_account": multi_account,
                "experimental": experimental,
                "preload": preload,
                "hooks": hooks,
                "search": search,
                "execute": execute,
            }
        )
        require_fields(
            body,
            body_fields,
            ("user_id",),
            "body",
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
            "/api/v3.1/tool_router/session",
            cast_to=SessionCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=SessionCreateBody,
            options=options_data,
        )

    def retrieve(
        self,
        session_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionRetrieveResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "get",
            build_path(
                "/api/v3.1/tool_router/session/{session_id}",
                {"session_id": session_id},
            ),
            cast_to=SessionRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    def delete(
        self,
        session_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionDeleteResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "delete",
            build_path(
                "/api/v3.1/tool_router/session/{session_id}",
                {"session_id": session_id},
            ),
            cast_to=SessionDeleteResponse,
            operation=_DELETE_OPERATION,
            options=options_data,
        )

    def attach(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        experimental: session_attach_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionAttachResponse:
        body_fields = compact(
            {
                "experimental": experimental,
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/attach",
                {"session_id": session_id},
            ),
            cast_to=SessionAttachResponse,
            operation=_ATTACH_OPERATION,
            body=body_data,
            body_model=SessionAttachBody,
            options=options_data,
        )

    def config_history(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> SessionConfigHistoryResponse:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
            }
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/config_history",
                {"session_id": session_id},
            ),
            cast_to=SessionConfigHistoryResponse,
            operation=_CONFIG_HISTORY_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    def execute(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        tool_slug: str,
        arguments: dict[str, object | None] | Omit = omit,
        account: str | Omit = omit,
        enable_auto_workbench_offload: bool | Omit = omit,
        input_responses: dict[str, session_execute_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionExecuteResult: ...

    @overload
    def execute(
        self,
        session_id: str,
        body: BodyParam,
        *,
        tool_slug: str | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        account: str | Omit = omit,
        enable_auto_workbench_offload: bool | Omit = omit,
        input_responses: dict[str, session_execute_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionExecuteResult: ...

    def execute(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        tool_slug: str | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        account: str | Omit = omit,
        enable_auto_workbench_offload: bool | Omit = omit,
        input_responses: dict[str, session_execute_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionExecuteResult:
        body_fields = compact(
            {
                "tool_slug": tool_slug,
                "arguments": arguments,
                "account": account,
                "enable_auto_workbench_offload": enable_auto_workbench_offload,
                "input_responses": input_responses,
                "request_state": request_state,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("tool_slug",),
            "body",
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/execute",
                {"session_id": session_id},
            ),
            cast_to=cast("type[SessionExecuteResult]", SessionExecuteResult),
            operation=_EXECUTE_OPERATION,
            body=body_data,
            body_model=SessionExecuteBody,
            options=options_data,
        )

    @overload
    def execute_meta(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        slug: Literal[
            "COMPOSIO_SEARCH_TOOLS",
            "COMPOSIO_MULTI_EXECUTE_TOOL",
            "COMPOSIO_MANAGE_CONNECTIONS",
            "COMPOSIO_WAIT_FOR_CONNECTIONS",
            "COMPOSIO_REMOTE_WORKBENCH",
            "COMPOSIO_REMOTE_BASH_TOOL",
            "COMPOSIO_GET_TOOL_SCHEMAS",
            "COMPOSIO_SUBMIT_FEEDBACK",
            "COMPOSIO_PROXY_EXECUTE",
        ],
        arguments: dict[str, object | None] | Omit = omit,
        input_responses: dict[str, session_execute_meta_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_meta_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionExecuteMetaResult: ...

    @overload
    def execute_meta(
        self,
        session_id: str,
        body: BodyParam,
        *,
        slug: Literal[
            "COMPOSIO_SEARCH_TOOLS",
            "COMPOSIO_MULTI_EXECUTE_TOOL",
            "COMPOSIO_MANAGE_CONNECTIONS",
            "COMPOSIO_WAIT_FOR_CONNECTIONS",
            "COMPOSIO_REMOTE_WORKBENCH",
            "COMPOSIO_REMOTE_BASH_TOOL",
            "COMPOSIO_GET_TOOL_SCHEMAS",
            "COMPOSIO_SUBMIT_FEEDBACK",
            "COMPOSIO_PROXY_EXECUTE",
        ]
        | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        input_responses: dict[str, session_execute_meta_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_meta_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionExecuteMetaResult: ...

    def execute_meta(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        slug: Literal[
            "COMPOSIO_SEARCH_TOOLS",
            "COMPOSIO_MULTI_EXECUTE_TOOL",
            "COMPOSIO_MANAGE_CONNECTIONS",
            "COMPOSIO_WAIT_FOR_CONNECTIONS",
            "COMPOSIO_REMOTE_WORKBENCH",
            "COMPOSIO_REMOTE_BASH_TOOL",
            "COMPOSIO_GET_TOOL_SCHEMAS",
            "COMPOSIO_SUBMIT_FEEDBACK",
            "COMPOSIO_PROXY_EXECUTE",
        ]
        | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        input_responses: dict[str, session_execute_meta_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_meta_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionExecuteMetaResult:
        body_fields = compact(
            {
                "slug": slug,
                "arguments": arguments,
                "input_responses": input_responses,
                "request_state": request_state,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("slug",),
            "body",
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/execute_meta",
                {"session_id": session_id},
            ),
            cast_to=cast("type[SessionExecuteMetaResult]", SessionExecuteMetaResult),
            operation=_EXECUTE_META_OPERATION,
            body=body_data,
            body_model=SessionExecuteMetaBody,
            options=options_data,
        )

    @overload
    def link(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        toolkit: str,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        experimental: session_link_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionLinkResponse: ...

    @overload
    def link(
        self,
        session_id: str,
        body: BodyParam,
        *,
        toolkit: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        experimental: session_link_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionLinkResponse: ...

    def link(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        toolkit: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        experimental: session_link_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionLinkResponse:
        body_fields = compact(
            {
                "toolkit": toolkit,
                "alias": alias,
                "callback_url": callback_url,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit",),
            "body",
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/link",
                {"session_id": session_id},
            ),
            cast_to=SessionLinkResponse,
            operation=_LINK_OPERATION,
            body=body_data,
            body_model=SessionLinkBody,
            options=options_data,
        )

    def patch(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        toolkits: session_patch_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | None | Omit = omit,
        instant: Literal[False] | session_patch_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_patch_params.ManageConnections | None | Omit = omit,
        tools: dict[str, session_patch_params.Tools] | Omit = omit,
        tags: session_patch_params.Tags | Omit = omit,
        workbench: session_patch_params.Workbench | None | Omit = omit,
        multi_account: session_patch_params.MultiAccount | None | Omit = omit,
        proxy_execute: session_patch_params.CurrentProxyExecute | None | Omit = omit,
        preload: session_patch_params.Preload | Omit = omit,
        search: session_patch_params.Search | Omit = omit,
        execute: session_patch_params.Execute | Omit = omit,
        hooks: Iterable[session_patch_params.CurrentHookVariant0 | session_patch_params.CurrentHookVariant1]
        | None
        | Omit = omit,
        experimental: session_patch_params.Experimental | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionPatchResponse:
        body_fields = compact(
            {
                "toolkits": toolkits,
                "auth_configs": auth_configs,
                "connected_accounts": connected_accounts,
                "instant": instant,
                "manage_connections": manage_connections,
                "tools": tools,
                "tags": tags,
                "workbench": workbench,
                "multi_account": multi_account,
                "proxy_execute": proxy_execute,
                "preload": preload,
                "search": search,
                "execute": execute,
                "hooks": hooks,
                "experimental": experimental,
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
            "patch",
            build_path(
                "/api/v3.1/tool_router/session/{session_id}",
                {"session_id": session_id},
            ),
            cast_to=SessionPatchResponse,
            operation=_PATCH_OPERATION,
            body=body_data,
            body_model=SessionPatchBody,
            options=options_data,
        )

    @overload
    def proxy_execute(
        self,
        session_id: str,
        *,
        toolkit_slug: str,
        endpoint: str,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"],
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionProxyExecuteResult: ...

    @overload
    def proxy_execute(
        self,
        session_id: str,
        *,
        toolkit_slug: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionProxyExecuteResult: ...

    @overload
    def proxy_execute(
        self,
        session_id: str,
        legacy_body: BodyParam,
        /,
        *,
        toolkit_slug: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionProxyExecuteResult: ...

    def proxy_execute(
        self,
        session_id: str,
        *legacy_body: object,
        toolkit_slug: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionProxyExecuteResult:
        body = normalize_body_argument(body, legacy_body)
        body_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "endpoint": endpoint,
                "method": method,
                "binary_body": binary_body,
                "parameters": parameters,
                "custom_connection_data": custom_connection_data,
            }
        )
        aggregate_body, body_value = split_body_argument(
            body,
            body_fields,
            (
                "toolkit_slug",
                "endpoint",
                "method",
                "body",
                "binary_body",
                "parameters",
                "custom_connection_data",
            ),
        )
        body_fields.update(compact({"body": body_value}))
        require_fields(
            aggregate_body,
            body_fields,
            ("toolkit_slug", "endpoint", "method"),
            "body",
        )
        body_data = merge_body(aggregate_body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "post",
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/proxy_execute",
                {"session_id": session_id},
            ),
            cast_to=cast("type[SessionProxyExecuteResult]", SessionProxyExecuteResult),
            operation=_PROXY_EXECUTE_OPERATION,
            body=body_data,
            body_model=SessionProxyExecuteBody,
            options=options_data,
        )

    @overload
    def search(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        queries: Iterable[session_search_params.Query],
        model: str | Omit = omit,
        search_strategy: Literal["auto", "tool_search"] | Omit = omit,
        experimental: session_search_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionSearchResponse: ...

    @overload
    def search(
        self,
        session_id: str,
        body: BodyParam,
        *,
        queries: Iterable[session_search_params.Query] | Omit = omit,
        model: str | Omit = omit,
        search_strategy: Literal["auto", "tool_search"] | Omit = omit,
        experimental: session_search_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionSearchResponse: ...

    def search(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        queries: Iterable[session_search_params.Query] | Omit = omit,
        model: str | Omit = omit,
        search_strategy: Literal["auto", "tool_search"] | Omit = omit,
        experimental: session_search_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionSearchResponse:
        body_fields = compact(
            {
                "queries": queries,
                "model": model,
                "search_strategy": search_strategy,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("queries",),
            "body",
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/search",
                {"session_id": session_id},
            ),
            cast_to=SessionSearchResponse,
            operation=_SEARCH_OPERATION,
            body=body_data,
            body_model=SessionSearchBody,
            options=options_data,
        )

    def toolkits(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        toolkits: SequenceNotStr[str] | None | Omit = omit,
        is_connected: bool | None | Omit = omit,
        search: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> SessionToolkitsResponse:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
                "toolkits": toolkits,
                "is_connected": is_connected,
                "search": search,
            }
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/toolkits",
                {"session_id": session_id},
            ),
            cast_to=SessionToolkitsResponse,
            operation=_TOOLKITS_OPERATION,
            query=query_data,
            options=options_data,
        )

    def tools(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> SessionToolsResponse:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
            }
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/tools",
                {"session_id": session_id},
            ),
            cast_to=SessionToolsResponse,
            operation=_TOOLS_OPERATION,
            query=query_data,
            options=options_data,
        )


class AsyncSessionResource(AsyncAPIResource):
    files: AsyncFilesResource

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.files = AsyncFilesResource(client)

    @cached_property
    def with_raw_response(self) -> AsyncSessionResourceWithRawResponse:
        return AsyncSessionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSessionResourceWithStreamingResponse:
        return AsyncSessionResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        user_id: str,
        toolkits: session_create_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        instant: Literal[False] | session_create_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_create_params.ManageConnections | Omit = omit,
        tools: dict[str, session_create_params.Tools] | Omit = omit,
        tags: session_create_params.Tags | Omit = omit,
        workbench: session_create_params.Workbench | Omit = omit,
        proxy_execute: session_create_params.CurrentProxyExecute | Omit = omit,
        multi_account: session_create_params.MultiAccount | Omit = omit,
        experimental: session_create_params.Experimental | Omit = omit,
        preload: session_create_params.Preload | Omit = omit,
        hooks: Iterable[session_create_params.CurrentHookVariant0 | session_create_params.CurrentHookVariant1]
        | Omit = omit,
        search: session_create_params.Search | Omit = omit,
        execute: session_create_params.Execute | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionCreateResponse: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        user_id: str | Omit = omit,
        toolkits: session_create_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        instant: Literal[False] | session_create_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_create_params.ManageConnections | Omit = omit,
        tools: dict[str, session_create_params.Tools] | Omit = omit,
        tags: session_create_params.Tags | Omit = omit,
        workbench: session_create_params.Workbench | Omit = omit,
        proxy_execute: session_create_params.CurrentProxyExecute | Omit = omit,
        multi_account: session_create_params.MultiAccount | Omit = omit,
        experimental: session_create_params.Experimental | Omit = omit,
        preload: session_create_params.Preload | Omit = omit,
        hooks: Iterable[session_create_params.CurrentHookVariant0 | session_create_params.CurrentHookVariant1]
        | Omit = omit,
        search: session_create_params.Search | Omit = omit,
        execute: session_create_params.Execute | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionCreateResponse: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        user_id: str | Omit = omit,
        toolkits: session_create_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        instant: Literal[False] | session_create_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_create_params.ManageConnections | Omit = omit,
        tools: dict[str, session_create_params.Tools] | Omit = omit,
        tags: session_create_params.Tags | Omit = omit,
        workbench: session_create_params.Workbench | Omit = omit,
        proxy_execute: session_create_params.CurrentProxyExecute | Omit = omit,
        multi_account: session_create_params.MultiAccount | Omit = omit,
        experimental: session_create_params.Experimental | Omit = omit,
        preload: session_create_params.Preload | Omit = omit,
        hooks: Iterable[session_create_params.CurrentHookVariant0 | session_create_params.CurrentHookVariant1]
        | Omit = omit,
        search: session_create_params.Search | Omit = omit,
        execute: session_create_params.Execute | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionCreateResponse:
        body_fields = compact(
            {
                "user_id": user_id,
                "toolkits": toolkits,
                "auth_configs": auth_configs,
                "connected_accounts": connected_accounts,
                "instant": instant,
                "manage_connections": manage_connections,
                "tools": tools,
                "tags": tags,
                "workbench": workbench,
                "proxy_execute": proxy_execute,
                "multi_account": multi_account,
                "experimental": experimental,
                "preload": preload,
                "hooks": hooks,
                "search": search,
                "execute": execute,
            }
        )
        require_fields(
            body,
            body_fields,
            ("user_id",),
            "body",
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
            "/api/v3.1/tool_router/session",
            cast_to=SessionCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=SessionCreateBody,
            options=options_data,
        )

    async def retrieve(
        self,
        session_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionRetrieveResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "get",
            build_path(
                "/api/v3.1/tool_router/session/{session_id}",
                {"session_id": session_id},
            ),
            cast_to=SessionRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    async def delete(
        self,
        session_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionDeleteResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "delete",
            build_path(
                "/api/v3.1/tool_router/session/{session_id}",
                {"session_id": session_id},
            ),
            cast_to=SessionDeleteResponse,
            operation=_DELETE_OPERATION,
            options=options_data,
        )

    async def attach(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        experimental: session_attach_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionAttachResponse:
        body_fields = compact(
            {
                "experimental": experimental,
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/attach",
                {"session_id": session_id},
            ),
            cast_to=SessionAttachResponse,
            operation=_ATTACH_OPERATION,
            body=body_data,
            body_model=SessionAttachBody,
            options=options_data,
        )

    async def config_history(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> SessionConfigHistoryResponse:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
            }
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/config_history",
                {"session_id": session_id},
            ),
            cast_to=SessionConfigHistoryResponse,
            operation=_CONFIG_HISTORY_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    async def execute(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        tool_slug: str,
        arguments: dict[str, object | None] | Omit = omit,
        account: str | Omit = omit,
        enable_auto_workbench_offload: bool | Omit = omit,
        input_responses: dict[str, session_execute_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionExecuteResult: ...

    @overload
    async def execute(
        self,
        session_id: str,
        body: BodyParam,
        *,
        tool_slug: str | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        account: str | Omit = omit,
        enable_auto_workbench_offload: bool | Omit = omit,
        input_responses: dict[str, session_execute_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionExecuteResult: ...

    async def execute(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        tool_slug: str | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        account: str | Omit = omit,
        enable_auto_workbench_offload: bool | Omit = omit,
        input_responses: dict[str, session_execute_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionExecuteResult:
        body_fields = compact(
            {
                "tool_slug": tool_slug,
                "arguments": arguments,
                "account": account,
                "enable_auto_workbench_offload": enable_auto_workbench_offload,
                "input_responses": input_responses,
                "request_state": request_state,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("tool_slug",),
            "body",
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/execute",
                {"session_id": session_id},
            ),
            cast_to=cast("type[SessionExecuteResult]", SessionExecuteResult),
            operation=_EXECUTE_OPERATION,
            body=body_data,
            body_model=SessionExecuteBody,
            options=options_data,
        )

    @overload
    async def execute_meta(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        slug: Literal[
            "COMPOSIO_SEARCH_TOOLS",
            "COMPOSIO_MULTI_EXECUTE_TOOL",
            "COMPOSIO_MANAGE_CONNECTIONS",
            "COMPOSIO_WAIT_FOR_CONNECTIONS",
            "COMPOSIO_REMOTE_WORKBENCH",
            "COMPOSIO_REMOTE_BASH_TOOL",
            "COMPOSIO_GET_TOOL_SCHEMAS",
            "COMPOSIO_SUBMIT_FEEDBACK",
            "COMPOSIO_PROXY_EXECUTE",
        ],
        arguments: dict[str, object | None] | Omit = omit,
        input_responses: dict[str, session_execute_meta_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_meta_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionExecuteMetaResult: ...

    @overload
    async def execute_meta(
        self,
        session_id: str,
        body: BodyParam,
        *,
        slug: Literal[
            "COMPOSIO_SEARCH_TOOLS",
            "COMPOSIO_MULTI_EXECUTE_TOOL",
            "COMPOSIO_MANAGE_CONNECTIONS",
            "COMPOSIO_WAIT_FOR_CONNECTIONS",
            "COMPOSIO_REMOTE_WORKBENCH",
            "COMPOSIO_REMOTE_BASH_TOOL",
            "COMPOSIO_GET_TOOL_SCHEMAS",
            "COMPOSIO_SUBMIT_FEEDBACK",
            "COMPOSIO_PROXY_EXECUTE",
        ]
        | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        input_responses: dict[str, session_execute_meta_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_meta_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionExecuteMetaResult: ...

    async def execute_meta(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        slug: Literal[
            "COMPOSIO_SEARCH_TOOLS",
            "COMPOSIO_MULTI_EXECUTE_TOOL",
            "COMPOSIO_MANAGE_CONNECTIONS",
            "COMPOSIO_WAIT_FOR_CONNECTIONS",
            "COMPOSIO_REMOTE_WORKBENCH",
            "COMPOSIO_REMOTE_BASH_TOOL",
            "COMPOSIO_GET_TOOL_SCHEMAS",
            "COMPOSIO_SUBMIT_FEEDBACK",
            "COMPOSIO_PROXY_EXECUTE",
        ]
        | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        input_responses: dict[str, session_execute_meta_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_meta_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionExecuteMetaResult:
        body_fields = compact(
            {
                "slug": slug,
                "arguments": arguments,
                "input_responses": input_responses,
                "request_state": request_state,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("slug",),
            "body",
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/execute_meta",
                {"session_id": session_id},
            ),
            cast_to=cast("type[SessionExecuteMetaResult]", SessionExecuteMetaResult),
            operation=_EXECUTE_META_OPERATION,
            body=body_data,
            body_model=SessionExecuteMetaBody,
            options=options_data,
        )

    @overload
    async def link(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        toolkit: str,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        experimental: session_link_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionLinkResponse: ...

    @overload
    async def link(
        self,
        session_id: str,
        body: BodyParam,
        *,
        toolkit: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        experimental: session_link_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionLinkResponse: ...

    async def link(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        toolkit: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        experimental: session_link_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionLinkResponse:
        body_fields = compact(
            {
                "toolkit": toolkit,
                "alias": alias,
                "callback_url": callback_url,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit",),
            "body",
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/link",
                {"session_id": session_id},
            ),
            cast_to=SessionLinkResponse,
            operation=_LINK_OPERATION,
            body=body_data,
            body_model=SessionLinkBody,
            options=options_data,
        )

    async def patch(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        toolkits: session_patch_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | None | Omit = omit,
        instant: Literal[False] | session_patch_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_patch_params.ManageConnections | None | Omit = omit,
        tools: dict[str, session_patch_params.Tools] | Omit = omit,
        tags: session_patch_params.Tags | Omit = omit,
        workbench: session_patch_params.Workbench | None | Omit = omit,
        multi_account: session_patch_params.MultiAccount | None | Omit = omit,
        proxy_execute: session_patch_params.CurrentProxyExecute | None | Omit = omit,
        preload: session_patch_params.Preload | Omit = omit,
        search: session_patch_params.Search | Omit = omit,
        execute: session_patch_params.Execute | Omit = omit,
        hooks: Iterable[session_patch_params.CurrentHookVariant0 | session_patch_params.CurrentHookVariant1]
        | None
        | Omit = omit,
        experimental: session_patch_params.Experimental | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionPatchResponse:
        body_fields = compact(
            {
                "toolkits": toolkits,
                "auth_configs": auth_configs,
                "connected_accounts": connected_accounts,
                "instant": instant,
                "manage_connections": manage_connections,
                "tools": tools,
                "tags": tags,
                "workbench": workbench,
                "multi_account": multi_account,
                "proxy_execute": proxy_execute,
                "preload": preload,
                "search": search,
                "execute": execute,
                "hooks": hooks,
                "experimental": experimental,
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
            "patch",
            build_path(
                "/api/v3.1/tool_router/session/{session_id}",
                {"session_id": session_id},
            ),
            cast_to=SessionPatchResponse,
            operation=_PATCH_OPERATION,
            body=body_data,
            body_model=SessionPatchBody,
            options=options_data,
        )

    @overload
    async def proxy_execute(
        self,
        session_id: str,
        *,
        toolkit_slug: str,
        endpoint: str,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"],
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionProxyExecuteResult: ...

    @overload
    async def proxy_execute(
        self,
        session_id: str,
        *,
        toolkit_slug: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionProxyExecuteResult: ...

    @overload
    async def proxy_execute(
        self,
        session_id: str,
        legacy_body: BodyParam,
        /,
        *,
        toolkit_slug: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionProxyExecuteResult: ...

    async def proxy_execute(
        self,
        session_id: str,
        *legacy_body: object,
        toolkit_slug: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionProxyExecuteResult:
        body = normalize_body_argument(body, legacy_body)
        body_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "endpoint": endpoint,
                "method": method,
                "binary_body": binary_body,
                "parameters": parameters,
                "custom_connection_data": custom_connection_data,
            }
        )
        aggregate_body, body_value = split_body_argument(
            body,
            body_fields,
            (
                "toolkit_slug",
                "endpoint",
                "method",
                "body",
                "binary_body",
                "parameters",
                "custom_connection_data",
            ),
        )
        body_fields.update(compact({"body": body_value}))
        require_fields(
            aggregate_body,
            body_fields,
            ("toolkit_slug", "endpoint", "method"),
            "body",
        )
        body_data = merge_body(aggregate_body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "post",
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/proxy_execute",
                {"session_id": session_id},
            ),
            cast_to=cast("type[SessionProxyExecuteResult]", SessionProxyExecuteResult),
            operation=_PROXY_EXECUTE_OPERATION,
            body=body_data,
            body_model=SessionProxyExecuteBody,
            options=options_data,
        )

    @overload
    async def search(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        queries: Iterable[session_search_params.Query],
        model: str | Omit = omit,
        search_strategy: Literal["auto", "tool_search"] | Omit = omit,
        experimental: session_search_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionSearchResponse: ...

    @overload
    async def search(
        self,
        session_id: str,
        body: BodyParam,
        *,
        queries: Iterable[session_search_params.Query] | Omit = omit,
        model: str | Omit = omit,
        search_strategy: Literal["auto", "tool_search"] | Omit = omit,
        experimental: session_search_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionSearchResponse: ...

    async def search(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        queries: Iterable[session_search_params.Query] | Omit = omit,
        model: str | Omit = omit,
        search_strategy: Literal["auto", "tool_search"] | Omit = omit,
        experimental: session_search_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionSearchResponse:
        body_fields = compact(
            {
                "queries": queries,
                "model": model,
                "search_strategy": search_strategy,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("queries",),
            "body",
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/search",
                {"session_id": session_id},
            ),
            cast_to=SessionSearchResponse,
            operation=_SEARCH_OPERATION,
            body=body_data,
            body_model=SessionSearchBody,
            options=options_data,
        )

    async def toolkits(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        toolkits: SequenceNotStr[str] | None | Omit = omit,
        is_connected: bool | None | Omit = omit,
        search: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> SessionToolkitsResponse:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
                "toolkits": toolkits,
                "is_connected": is_connected,
                "search": search,
            }
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/toolkits",
                {"session_id": session_id},
            ),
            cast_to=SessionToolkitsResponse,
            operation=_TOOLKITS_OPERATION,
            query=query_data,
            options=options_data,
        )

    async def tools(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> SessionToolsResponse:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
            }
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/tools",
                {"session_id": session_id},
            ),
            cast_to=SessionToolsResponse,
            operation=_TOOLS_OPERATION,
            query=query_data,
            options=options_data,
        )


class SessionResourceWithRawResponse:
    def __init__(self, resource: SessionResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        user_id: str,
        toolkits: session_create_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        instant: Literal[False] | session_create_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_create_params.ManageConnections | Omit = omit,
        tools: dict[str, session_create_params.Tools] | Omit = omit,
        tags: session_create_params.Tags | Omit = omit,
        workbench: session_create_params.Workbench | Omit = omit,
        proxy_execute: session_create_params.CurrentProxyExecute | Omit = omit,
        multi_account: session_create_params.MultiAccount | Omit = omit,
        experimental: session_create_params.Experimental | Omit = omit,
        preload: session_create_params.Preload | Omit = omit,
        hooks: Iterable[session_create_params.CurrentHookVariant0 | session_create_params.CurrentHookVariant1]
        | Omit = omit,
        search: session_create_params.Search | Omit = omit,
        execute: session_create_params.Execute | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionCreateResponse]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        user_id: str | Omit = omit,
        toolkits: session_create_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        instant: Literal[False] | session_create_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_create_params.ManageConnections | Omit = omit,
        tools: dict[str, session_create_params.Tools] | Omit = omit,
        tags: session_create_params.Tags | Omit = omit,
        workbench: session_create_params.Workbench | Omit = omit,
        proxy_execute: session_create_params.CurrentProxyExecute | Omit = omit,
        multi_account: session_create_params.MultiAccount | Omit = omit,
        experimental: session_create_params.Experimental | Omit = omit,
        preload: session_create_params.Preload | Omit = omit,
        hooks: Iterable[session_create_params.CurrentHookVariant0 | session_create_params.CurrentHookVariant1]
        | Omit = omit,
        search: session_create_params.Search | Omit = omit,
        execute: session_create_params.Execute | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionCreateResponse]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        user_id: str | Omit = omit,
        toolkits: session_create_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        instant: Literal[False] | session_create_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_create_params.ManageConnections | Omit = omit,
        tools: dict[str, session_create_params.Tools] | Omit = omit,
        tags: session_create_params.Tags | Omit = omit,
        workbench: session_create_params.Workbench | Omit = omit,
        proxy_execute: session_create_params.CurrentProxyExecute | Omit = omit,
        multi_account: session_create_params.MultiAccount | Omit = omit,
        experimental: session_create_params.Experimental | Omit = omit,
        preload: session_create_params.Preload | Omit = omit,
        hooks: Iterable[session_create_params.CurrentHookVariant0 | session_create_params.CurrentHookVariant1]
        | Omit = omit,
        search: session_create_params.Search | Omit = omit,
        execute: session_create_params.Execute | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionCreateResponse]:
        body_fields = compact(
            {
                "user_id": user_id,
                "toolkits": toolkits,
                "auth_configs": auth_configs,
                "connected_accounts": connected_accounts,
                "instant": instant,
                "manage_connections": manage_connections,
                "tools": tools,
                "tags": tags,
                "workbench": workbench,
                "proxy_execute": proxy_execute,
                "multi_account": multi_account,
                "experimental": experimental,
                "preload": preload,
                "hooks": hooks,
                "search": search,
                "execute": execute,
            }
        )
        require_fields(
            body,
            body_fields,
            ("user_id",),
            "body",
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
            "/api/v3.1/tool_router/session",
            cast_to=SessionCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=SessionCreateBody,
            options=options_data,
        )

    def retrieve(
        self,
        session_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionRetrieveResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "get",
            build_path(
                "/api/v3.1/tool_router/session/{session_id}",
                {"session_id": session_id},
            ),
            cast_to=SessionRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    def delete(
        self,
        session_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionDeleteResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "delete",
            build_path(
                "/api/v3.1/tool_router/session/{session_id}",
                {"session_id": session_id},
            ),
            cast_to=SessionDeleteResponse,
            operation=_DELETE_OPERATION,
            options=options_data,
        )

    def attach(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        experimental: session_attach_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionAttachResponse]:
        body_fields = compact(
            {
                "experimental": experimental,
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/attach",
                {"session_id": session_id},
            ),
            cast_to=SessionAttachResponse,
            operation=_ATTACH_OPERATION,
            body=body_data,
            body_model=SessionAttachBody,
            options=options_data,
        )

    def config_history(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionConfigHistoryResponse]:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
            }
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/config_history",
                {"session_id": session_id},
            ),
            cast_to=SessionConfigHistoryResponse,
            operation=_CONFIG_HISTORY_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    def execute(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        tool_slug: str,
        arguments: dict[str, object | None] | Omit = omit,
        account: str | Omit = omit,
        enable_auto_workbench_offload: bool | Omit = omit,
        input_responses: dict[str, session_execute_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionExecuteResult]: ...

    @overload
    def execute(
        self,
        session_id: str,
        body: BodyParam,
        *,
        tool_slug: str | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        account: str | Omit = omit,
        enable_auto_workbench_offload: bool | Omit = omit,
        input_responses: dict[str, session_execute_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionExecuteResult]: ...

    def execute(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        tool_slug: str | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        account: str | Omit = omit,
        enable_auto_workbench_offload: bool | Omit = omit,
        input_responses: dict[str, session_execute_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionExecuteResult]:
        body_fields = compact(
            {
                "tool_slug": tool_slug,
                "arguments": arguments,
                "account": account,
                "enable_auto_workbench_offload": enable_auto_workbench_offload,
                "input_responses": input_responses,
                "request_state": request_state,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("tool_slug",),
            "body",
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/execute",
                {"session_id": session_id},
            ),
            cast_to=cast("type[SessionExecuteResult]", SessionExecuteResult),
            operation=_EXECUTE_OPERATION,
            body=body_data,
            body_model=SessionExecuteBody,
            options=options_data,
        )

    @overload
    def execute_meta(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        slug: Literal[
            "COMPOSIO_SEARCH_TOOLS",
            "COMPOSIO_MULTI_EXECUTE_TOOL",
            "COMPOSIO_MANAGE_CONNECTIONS",
            "COMPOSIO_WAIT_FOR_CONNECTIONS",
            "COMPOSIO_REMOTE_WORKBENCH",
            "COMPOSIO_REMOTE_BASH_TOOL",
            "COMPOSIO_GET_TOOL_SCHEMAS",
            "COMPOSIO_SUBMIT_FEEDBACK",
            "COMPOSIO_PROXY_EXECUTE",
        ],
        arguments: dict[str, object | None] | Omit = omit,
        input_responses: dict[str, session_execute_meta_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_meta_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionExecuteMetaResult]: ...

    @overload
    def execute_meta(
        self,
        session_id: str,
        body: BodyParam,
        *,
        slug: Literal[
            "COMPOSIO_SEARCH_TOOLS",
            "COMPOSIO_MULTI_EXECUTE_TOOL",
            "COMPOSIO_MANAGE_CONNECTIONS",
            "COMPOSIO_WAIT_FOR_CONNECTIONS",
            "COMPOSIO_REMOTE_WORKBENCH",
            "COMPOSIO_REMOTE_BASH_TOOL",
            "COMPOSIO_GET_TOOL_SCHEMAS",
            "COMPOSIO_SUBMIT_FEEDBACK",
            "COMPOSIO_PROXY_EXECUTE",
        ]
        | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        input_responses: dict[str, session_execute_meta_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_meta_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionExecuteMetaResult]: ...

    def execute_meta(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        slug: Literal[
            "COMPOSIO_SEARCH_TOOLS",
            "COMPOSIO_MULTI_EXECUTE_TOOL",
            "COMPOSIO_MANAGE_CONNECTIONS",
            "COMPOSIO_WAIT_FOR_CONNECTIONS",
            "COMPOSIO_REMOTE_WORKBENCH",
            "COMPOSIO_REMOTE_BASH_TOOL",
            "COMPOSIO_GET_TOOL_SCHEMAS",
            "COMPOSIO_SUBMIT_FEEDBACK",
            "COMPOSIO_PROXY_EXECUTE",
        ]
        | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        input_responses: dict[str, session_execute_meta_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_meta_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionExecuteMetaResult]:
        body_fields = compact(
            {
                "slug": slug,
                "arguments": arguments,
                "input_responses": input_responses,
                "request_state": request_state,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("slug",),
            "body",
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/execute_meta",
                {"session_id": session_id},
            ),
            cast_to=cast("type[SessionExecuteMetaResult]", SessionExecuteMetaResult),
            operation=_EXECUTE_META_OPERATION,
            body=body_data,
            body_model=SessionExecuteMetaBody,
            options=options_data,
        )

    @overload
    def link(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        toolkit: str,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        experimental: session_link_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionLinkResponse]: ...

    @overload
    def link(
        self,
        session_id: str,
        body: BodyParam,
        *,
        toolkit: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        experimental: session_link_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionLinkResponse]: ...

    def link(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        toolkit: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        experimental: session_link_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionLinkResponse]:
        body_fields = compact(
            {
                "toolkit": toolkit,
                "alias": alias,
                "callback_url": callback_url,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit",),
            "body",
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/link",
                {"session_id": session_id},
            ),
            cast_to=SessionLinkResponse,
            operation=_LINK_OPERATION,
            body=body_data,
            body_model=SessionLinkBody,
            options=options_data,
        )

    def patch(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        toolkits: session_patch_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | None | Omit = omit,
        instant: Literal[False] | session_patch_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_patch_params.ManageConnections | None | Omit = omit,
        tools: dict[str, session_patch_params.Tools] | Omit = omit,
        tags: session_patch_params.Tags | Omit = omit,
        workbench: session_patch_params.Workbench | None | Omit = omit,
        multi_account: session_patch_params.MultiAccount | None | Omit = omit,
        proxy_execute: session_patch_params.CurrentProxyExecute | None | Omit = omit,
        preload: session_patch_params.Preload | Omit = omit,
        search: session_patch_params.Search | Omit = omit,
        execute: session_patch_params.Execute | Omit = omit,
        hooks: Iterable[session_patch_params.CurrentHookVariant0 | session_patch_params.CurrentHookVariant1]
        | None
        | Omit = omit,
        experimental: session_patch_params.Experimental | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionPatchResponse]:
        body_fields = compact(
            {
                "toolkits": toolkits,
                "auth_configs": auth_configs,
                "connected_accounts": connected_accounts,
                "instant": instant,
                "manage_connections": manage_connections,
                "tools": tools,
                "tags": tags,
                "workbench": workbench,
                "multi_account": multi_account,
                "proxy_execute": proxy_execute,
                "preload": preload,
                "search": search,
                "execute": execute,
                "hooks": hooks,
                "experimental": experimental,
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
            "patch",
            build_path(
                "/api/v3.1/tool_router/session/{session_id}",
                {"session_id": session_id},
            ),
            cast_to=SessionPatchResponse,
            operation=_PATCH_OPERATION,
            body=body_data,
            body_model=SessionPatchBody,
            options=options_data,
        )

    @overload
    def proxy_execute(
        self,
        session_id: str,
        *,
        toolkit_slug: str,
        endpoint: str,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"],
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionProxyExecuteResult]: ...

    @overload
    def proxy_execute(
        self,
        session_id: str,
        *,
        toolkit_slug: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionProxyExecuteResult]: ...

    @overload
    def proxy_execute(
        self,
        session_id: str,
        legacy_body: BodyParam,
        /,
        *,
        toolkit_slug: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionProxyExecuteResult]: ...

    def proxy_execute(
        self,
        session_id: str,
        *legacy_body: object,
        toolkit_slug: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionProxyExecuteResult]:
        body = normalize_body_argument(body, legacy_body)
        body_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "endpoint": endpoint,
                "method": method,
                "binary_body": binary_body,
                "parameters": parameters,
                "custom_connection_data": custom_connection_data,
            }
        )
        aggregate_body, body_value = split_body_argument(
            body,
            body_fields,
            (
                "toolkit_slug",
                "endpoint",
                "method",
                "body",
                "binary_body",
                "parameters",
                "custom_connection_data",
            ),
        )
        body_fields.update(compact({"body": body_value}))
        require_fields(
            aggregate_body,
            body_fields,
            ("toolkit_slug", "endpoint", "method"),
            "body",
        )
        body_data = merge_body(aggregate_body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "post",
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/proxy_execute",
                {"session_id": session_id},
            ),
            cast_to=cast("type[SessionProxyExecuteResult]", SessionProxyExecuteResult),
            operation=_PROXY_EXECUTE_OPERATION,
            body=body_data,
            body_model=SessionProxyExecuteBody,
            options=options_data,
        )

    @overload
    def search(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        queries: Iterable[session_search_params.Query],
        model: str | Omit = omit,
        search_strategy: Literal["auto", "tool_search"] | Omit = omit,
        experimental: session_search_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionSearchResponse]: ...

    @overload
    def search(
        self,
        session_id: str,
        body: BodyParam,
        *,
        queries: Iterable[session_search_params.Query] | Omit = omit,
        model: str | Omit = omit,
        search_strategy: Literal["auto", "tool_search"] | Omit = omit,
        experimental: session_search_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionSearchResponse]: ...

    def search(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        queries: Iterable[session_search_params.Query] | Omit = omit,
        model: str | Omit = omit,
        search_strategy: Literal["auto", "tool_search"] | Omit = omit,
        experimental: session_search_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionSearchResponse]:
        body_fields = compact(
            {
                "queries": queries,
                "model": model,
                "search_strategy": search_strategy,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("queries",),
            "body",
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/search",
                {"session_id": session_id},
            ),
            cast_to=SessionSearchResponse,
            operation=_SEARCH_OPERATION,
            body=body_data,
            body_model=SessionSearchBody,
            options=options_data,
        )

    def toolkits(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        toolkits: SequenceNotStr[str] | None | Omit = omit,
        is_connected: bool | None | Omit = omit,
        search: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionToolkitsResponse]:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
                "toolkits": toolkits,
                "is_connected": is_connected,
                "search": search,
            }
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/toolkits",
                {"session_id": session_id},
            ),
            cast_to=SessionToolkitsResponse,
            operation=_TOOLKITS_OPERATION,
            query=query_data,
            options=options_data,
        )

    def tools(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionToolsResponse]:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
            }
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/tools",
                {"session_id": session_id},
            ),
            cast_to=SessionToolsResponse,
            operation=_TOOLS_OPERATION,
            query=query_data,
            options=options_data,
        )


class AsyncSessionResourceWithRawResponse:
    def __init__(self, resource: AsyncSessionResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        user_id: str,
        toolkits: session_create_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        instant: Literal[False] | session_create_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_create_params.ManageConnections | Omit = omit,
        tools: dict[str, session_create_params.Tools] | Omit = omit,
        tags: session_create_params.Tags | Omit = omit,
        workbench: session_create_params.Workbench | Omit = omit,
        proxy_execute: session_create_params.CurrentProxyExecute | Omit = omit,
        multi_account: session_create_params.MultiAccount | Omit = omit,
        experimental: session_create_params.Experimental | Omit = omit,
        preload: session_create_params.Preload | Omit = omit,
        hooks: Iterable[session_create_params.CurrentHookVariant0 | session_create_params.CurrentHookVariant1]
        | Omit = omit,
        search: session_create_params.Search | Omit = omit,
        execute: session_create_params.Execute | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionCreateResponse]: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        user_id: str | Omit = omit,
        toolkits: session_create_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        instant: Literal[False] | session_create_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_create_params.ManageConnections | Omit = omit,
        tools: dict[str, session_create_params.Tools] | Omit = omit,
        tags: session_create_params.Tags | Omit = omit,
        workbench: session_create_params.Workbench | Omit = omit,
        proxy_execute: session_create_params.CurrentProxyExecute | Omit = omit,
        multi_account: session_create_params.MultiAccount | Omit = omit,
        experimental: session_create_params.Experimental | Omit = omit,
        preload: session_create_params.Preload | Omit = omit,
        hooks: Iterable[session_create_params.CurrentHookVariant0 | session_create_params.CurrentHookVariant1]
        | Omit = omit,
        search: session_create_params.Search | Omit = omit,
        execute: session_create_params.Execute | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionCreateResponse]: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        user_id: str | Omit = omit,
        toolkits: session_create_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        instant: Literal[False] | session_create_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_create_params.ManageConnections | Omit = omit,
        tools: dict[str, session_create_params.Tools] | Omit = omit,
        tags: session_create_params.Tags | Omit = omit,
        workbench: session_create_params.Workbench | Omit = omit,
        proxy_execute: session_create_params.CurrentProxyExecute | Omit = omit,
        multi_account: session_create_params.MultiAccount | Omit = omit,
        experimental: session_create_params.Experimental | Omit = omit,
        preload: session_create_params.Preload | Omit = omit,
        hooks: Iterable[session_create_params.CurrentHookVariant0 | session_create_params.CurrentHookVariant1]
        | Omit = omit,
        search: session_create_params.Search | Omit = omit,
        execute: session_create_params.Execute | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionCreateResponse]:
        body_fields = compact(
            {
                "user_id": user_id,
                "toolkits": toolkits,
                "auth_configs": auth_configs,
                "connected_accounts": connected_accounts,
                "instant": instant,
                "manage_connections": manage_connections,
                "tools": tools,
                "tags": tags,
                "workbench": workbench,
                "proxy_execute": proxy_execute,
                "multi_account": multi_account,
                "experimental": experimental,
                "preload": preload,
                "hooks": hooks,
                "search": search,
                "execute": execute,
            }
        )
        require_fields(
            body,
            body_fields,
            ("user_id",),
            "body",
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
            "/api/v3.1/tool_router/session",
            cast_to=SessionCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=SessionCreateBody,
            options=options_data,
        )

    async def retrieve(
        self,
        session_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionRetrieveResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "get",
            build_path(
                "/api/v3.1/tool_router/session/{session_id}",
                {"session_id": session_id},
            ),
            cast_to=SessionRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    async def delete(
        self,
        session_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionDeleteResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "delete",
            build_path(
                "/api/v3.1/tool_router/session/{session_id}",
                {"session_id": session_id},
            ),
            cast_to=SessionDeleteResponse,
            operation=_DELETE_OPERATION,
            options=options_data,
        )

    async def attach(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        experimental: session_attach_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionAttachResponse]:
        body_fields = compact(
            {
                "experimental": experimental,
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/attach",
                {"session_id": session_id},
            ),
            cast_to=SessionAttachResponse,
            operation=_ATTACH_OPERATION,
            body=body_data,
            body_model=SessionAttachBody,
            options=options_data,
        )

    async def config_history(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionConfigHistoryResponse]:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
            }
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/config_history",
                {"session_id": session_id},
            ),
            cast_to=SessionConfigHistoryResponse,
            operation=_CONFIG_HISTORY_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    async def execute(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        tool_slug: str,
        arguments: dict[str, object | None] | Omit = omit,
        account: str | Omit = omit,
        enable_auto_workbench_offload: bool | Omit = omit,
        input_responses: dict[str, session_execute_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionExecuteResult]: ...

    @overload
    async def execute(
        self,
        session_id: str,
        body: BodyParam,
        *,
        tool_slug: str | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        account: str | Omit = omit,
        enable_auto_workbench_offload: bool | Omit = omit,
        input_responses: dict[str, session_execute_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionExecuteResult]: ...

    async def execute(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        tool_slug: str | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        account: str | Omit = omit,
        enable_auto_workbench_offload: bool | Omit = omit,
        input_responses: dict[str, session_execute_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionExecuteResult]:
        body_fields = compact(
            {
                "tool_slug": tool_slug,
                "arguments": arguments,
                "account": account,
                "enable_auto_workbench_offload": enable_auto_workbench_offload,
                "input_responses": input_responses,
                "request_state": request_state,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("tool_slug",),
            "body",
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/execute",
                {"session_id": session_id},
            ),
            cast_to=cast("type[SessionExecuteResult]", SessionExecuteResult),
            operation=_EXECUTE_OPERATION,
            body=body_data,
            body_model=SessionExecuteBody,
            options=options_data,
        )

    @overload
    async def execute_meta(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        slug: Literal[
            "COMPOSIO_SEARCH_TOOLS",
            "COMPOSIO_MULTI_EXECUTE_TOOL",
            "COMPOSIO_MANAGE_CONNECTIONS",
            "COMPOSIO_WAIT_FOR_CONNECTIONS",
            "COMPOSIO_REMOTE_WORKBENCH",
            "COMPOSIO_REMOTE_BASH_TOOL",
            "COMPOSIO_GET_TOOL_SCHEMAS",
            "COMPOSIO_SUBMIT_FEEDBACK",
            "COMPOSIO_PROXY_EXECUTE",
        ],
        arguments: dict[str, object | None] | Omit = omit,
        input_responses: dict[str, session_execute_meta_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_meta_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionExecuteMetaResult]: ...

    @overload
    async def execute_meta(
        self,
        session_id: str,
        body: BodyParam,
        *,
        slug: Literal[
            "COMPOSIO_SEARCH_TOOLS",
            "COMPOSIO_MULTI_EXECUTE_TOOL",
            "COMPOSIO_MANAGE_CONNECTIONS",
            "COMPOSIO_WAIT_FOR_CONNECTIONS",
            "COMPOSIO_REMOTE_WORKBENCH",
            "COMPOSIO_REMOTE_BASH_TOOL",
            "COMPOSIO_GET_TOOL_SCHEMAS",
            "COMPOSIO_SUBMIT_FEEDBACK",
            "COMPOSIO_PROXY_EXECUTE",
        ]
        | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        input_responses: dict[str, session_execute_meta_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_meta_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionExecuteMetaResult]: ...

    async def execute_meta(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        slug: Literal[
            "COMPOSIO_SEARCH_TOOLS",
            "COMPOSIO_MULTI_EXECUTE_TOOL",
            "COMPOSIO_MANAGE_CONNECTIONS",
            "COMPOSIO_WAIT_FOR_CONNECTIONS",
            "COMPOSIO_REMOTE_WORKBENCH",
            "COMPOSIO_REMOTE_BASH_TOOL",
            "COMPOSIO_GET_TOOL_SCHEMAS",
            "COMPOSIO_SUBMIT_FEEDBACK",
            "COMPOSIO_PROXY_EXECUTE",
        ]
        | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        input_responses: dict[str, session_execute_meta_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_meta_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionExecuteMetaResult]:
        body_fields = compact(
            {
                "slug": slug,
                "arguments": arguments,
                "input_responses": input_responses,
                "request_state": request_state,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("slug",),
            "body",
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/execute_meta",
                {"session_id": session_id},
            ),
            cast_to=cast("type[SessionExecuteMetaResult]", SessionExecuteMetaResult),
            operation=_EXECUTE_META_OPERATION,
            body=body_data,
            body_model=SessionExecuteMetaBody,
            options=options_data,
        )

    @overload
    async def link(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        toolkit: str,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        experimental: session_link_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionLinkResponse]: ...

    @overload
    async def link(
        self,
        session_id: str,
        body: BodyParam,
        *,
        toolkit: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        experimental: session_link_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionLinkResponse]: ...

    async def link(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        toolkit: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        experimental: session_link_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionLinkResponse]:
        body_fields = compact(
            {
                "toolkit": toolkit,
                "alias": alias,
                "callback_url": callback_url,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit",),
            "body",
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/link",
                {"session_id": session_id},
            ),
            cast_to=SessionLinkResponse,
            operation=_LINK_OPERATION,
            body=body_data,
            body_model=SessionLinkBody,
            options=options_data,
        )

    async def patch(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        toolkits: session_patch_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | None | Omit = omit,
        instant: Literal[False] | session_patch_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_patch_params.ManageConnections | None | Omit = omit,
        tools: dict[str, session_patch_params.Tools] | Omit = omit,
        tags: session_patch_params.Tags | Omit = omit,
        workbench: session_patch_params.Workbench | None | Omit = omit,
        multi_account: session_patch_params.MultiAccount | None | Omit = omit,
        proxy_execute: session_patch_params.CurrentProxyExecute | None | Omit = omit,
        preload: session_patch_params.Preload | Omit = omit,
        search: session_patch_params.Search | Omit = omit,
        execute: session_patch_params.Execute | Omit = omit,
        hooks: Iterable[session_patch_params.CurrentHookVariant0 | session_patch_params.CurrentHookVariant1]
        | None
        | Omit = omit,
        experimental: session_patch_params.Experimental | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionPatchResponse]:
        body_fields = compact(
            {
                "toolkits": toolkits,
                "auth_configs": auth_configs,
                "connected_accounts": connected_accounts,
                "instant": instant,
                "manage_connections": manage_connections,
                "tools": tools,
                "tags": tags,
                "workbench": workbench,
                "multi_account": multi_account,
                "proxy_execute": proxy_execute,
                "preload": preload,
                "search": search,
                "execute": execute,
                "hooks": hooks,
                "experimental": experimental,
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
            "patch",
            build_path(
                "/api/v3.1/tool_router/session/{session_id}",
                {"session_id": session_id},
            ),
            cast_to=SessionPatchResponse,
            operation=_PATCH_OPERATION,
            body=body_data,
            body_model=SessionPatchBody,
            options=options_data,
        )

    @overload
    async def proxy_execute(
        self,
        session_id: str,
        *,
        toolkit_slug: str,
        endpoint: str,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"],
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionProxyExecuteResult]: ...

    @overload
    async def proxy_execute(
        self,
        session_id: str,
        *,
        toolkit_slug: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionProxyExecuteResult]: ...

    @overload
    async def proxy_execute(
        self,
        session_id: str,
        legacy_body: BodyParam,
        /,
        *,
        toolkit_slug: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionProxyExecuteResult]: ...

    async def proxy_execute(
        self,
        session_id: str,
        *legacy_body: object,
        toolkit_slug: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionProxyExecuteResult]:
        body = normalize_body_argument(body, legacy_body)
        body_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "endpoint": endpoint,
                "method": method,
                "binary_body": binary_body,
                "parameters": parameters,
                "custom_connection_data": custom_connection_data,
            }
        )
        aggregate_body, body_value = split_body_argument(
            body,
            body_fields,
            (
                "toolkit_slug",
                "endpoint",
                "method",
                "body",
                "binary_body",
                "parameters",
                "custom_connection_data",
            ),
        )
        body_fields.update(compact({"body": body_value}))
        require_fields(
            aggregate_body,
            body_fields,
            ("toolkit_slug", "endpoint", "method"),
            "body",
        )
        body_data = merge_body(aggregate_body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "post",
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/proxy_execute",
                {"session_id": session_id},
            ),
            cast_to=cast("type[SessionProxyExecuteResult]", SessionProxyExecuteResult),
            operation=_PROXY_EXECUTE_OPERATION,
            body=body_data,
            body_model=SessionProxyExecuteBody,
            options=options_data,
        )

    @overload
    async def search(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        queries: Iterable[session_search_params.Query],
        model: str | Omit = omit,
        search_strategy: Literal["auto", "tool_search"] | Omit = omit,
        experimental: session_search_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionSearchResponse]: ...

    @overload
    async def search(
        self,
        session_id: str,
        body: BodyParam,
        *,
        queries: Iterable[session_search_params.Query] | Omit = omit,
        model: str | Omit = omit,
        search_strategy: Literal["auto", "tool_search"] | Omit = omit,
        experimental: session_search_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionSearchResponse]: ...

    async def search(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        queries: Iterable[session_search_params.Query] | Omit = omit,
        model: str | Omit = omit,
        search_strategy: Literal["auto", "tool_search"] | Omit = omit,
        experimental: session_search_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionSearchResponse]:
        body_fields = compact(
            {
                "queries": queries,
                "model": model,
                "search_strategy": search_strategy,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("queries",),
            "body",
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/search",
                {"session_id": session_id},
            ),
            cast_to=SessionSearchResponse,
            operation=_SEARCH_OPERATION,
            body=body_data,
            body_model=SessionSearchBody,
            options=options_data,
        )

    async def toolkits(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        toolkits: SequenceNotStr[str] | None | Omit = omit,
        is_connected: bool | None | Omit = omit,
        search: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionToolkitsResponse]:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
                "toolkits": toolkits,
                "is_connected": is_connected,
                "search": search,
            }
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/toolkits",
                {"session_id": session_id},
            ),
            cast_to=SessionToolkitsResponse,
            operation=_TOOLKITS_OPERATION,
            query=query_data,
            options=options_data,
        )

    async def tools(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionToolsResponse]:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
            }
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
            build_path(
                "/api/v3.1/tool_router/session/{session_id}/tools",
                {"session_id": session_id},
            ),
            cast_to=SessionToolsResponse,
            operation=_TOOLS_OPERATION,
            query=query_data,
            options=options_data,
        )


class SessionResourceWithStreamingResponse:
    def __init__(self, resource: SessionResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        user_id: str,
        toolkits: session_create_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        instant: Literal[False] | session_create_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_create_params.ManageConnections | Omit = omit,
        tools: dict[str, session_create_params.Tools] | Omit = omit,
        tags: session_create_params.Tags | Omit = omit,
        workbench: session_create_params.Workbench | Omit = omit,
        proxy_execute: session_create_params.CurrentProxyExecute | Omit = omit,
        multi_account: session_create_params.MultiAccount | Omit = omit,
        experimental: session_create_params.Experimental | Omit = omit,
        preload: session_create_params.Preload | Omit = omit,
        hooks: Iterable[session_create_params.CurrentHookVariant0 | session_create_params.CurrentHookVariant1]
        | Omit = omit,
        search: session_create_params.Search | Omit = omit,
        execute: session_create_params.Execute | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        user_id: str | Omit = omit,
        toolkits: session_create_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        instant: Literal[False] | session_create_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_create_params.ManageConnections | Omit = omit,
        tools: dict[str, session_create_params.Tools] | Omit = omit,
        tags: session_create_params.Tags | Omit = omit,
        workbench: session_create_params.Workbench | Omit = omit,
        proxy_execute: session_create_params.CurrentProxyExecute | Omit = omit,
        multi_account: session_create_params.MultiAccount | Omit = omit,
        experimental: session_create_params.Experimental | Omit = omit,
        preload: session_create_params.Preload | Omit = omit,
        hooks: Iterable[session_create_params.CurrentHookVariant0 | session_create_params.CurrentHookVariant1]
        | Omit = omit,
        search: session_create_params.Search | Omit = omit,
        execute: session_create_params.Execute | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        user_id: str | Omit = omit,
        toolkits: session_create_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        instant: Literal[False] | session_create_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_create_params.ManageConnections | Omit = omit,
        tools: dict[str, session_create_params.Tools] | Omit = omit,
        tags: session_create_params.Tags | Omit = omit,
        workbench: session_create_params.Workbench | Omit = omit,
        proxy_execute: session_create_params.CurrentProxyExecute | Omit = omit,
        multi_account: session_create_params.MultiAccount | Omit = omit,
        experimental: session_create_params.Experimental | Omit = omit,
        preload: session_create_params.Preload | Omit = omit,
        hooks: Iterable[session_create_params.CurrentHookVariant0 | session_create_params.CurrentHookVariant1]
        | Omit = omit,
        search: session_create_params.Search | Omit = omit,
        execute: session_create_params.Execute | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionCreateResponse]]:
        body_fields = compact(
            {
                "user_id": user_id,
                "toolkits": toolkits,
                "auth_configs": auth_configs,
                "connected_accounts": connected_accounts,
                "instant": instant,
                "manage_connections": manage_connections,
                "tools": tools,
                "tags": tags,
                "workbench": workbench,
                "proxy_execute": proxy_execute,
                "multi_account": multi_account,
                "experimental": experimental,
                "preload": preload,
                "hooks": hooks,
                "search": search,
                "execute": execute,
            }
        )
        require_fields(
            body,
            body_fields,
            ("user_id",),
            "body",
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
                "/api/v3.1/tool_router/session",
                cast_to=SessionCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=SessionCreateBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve(
        self,
        session_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionRetrieveResponse]]:
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}",
                    {"session_id": session_id},
                ),
                cast_to=SessionRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def delete(
        self,
        session_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionDeleteResponse]]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return ResponseContextManager(
            lambda: self._client._request_raw(
                "delete",
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}",
                    {"session_id": session_id},
                ),
                cast_to=SessionDeleteResponse,
                operation=_DELETE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def attach(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        experimental: session_attach_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionAttachResponse]]:
        body_fields = compact(
            {
                "experimental": experimental,
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}/attach",
                    {"session_id": session_id},
                ),
                cast_to=SessionAttachResponse,
                operation=_ATTACH_OPERATION,
                body=body_data,
                body_model=SessionAttachBody,
                options=options_data,
                stream=True,
            )
        )

    def config_history(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionConfigHistoryResponse]]:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
            }
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}/config_history",
                    {"session_id": session_id},
                ),
                cast_to=SessionConfigHistoryResponse,
                operation=_CONFIG_HISTORY_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def execute(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        tool_slug: str,
        arguments: dict[str, object | None] | Omit = omit,
        account: str | Omit = omit,
        enable_auto_workbench_offload: bool | Omit = omit,
        input_responses: dict[str, session_execute_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionExecuteResult]]: ...

    @overload
    def execute(
        self,
        session_id: str,
        body: BodyParam,
        *,
        tool_slug: str | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        account: str | Omit = omit,
        enable_auto_workbench_offload: bool | Omit = omit,
        input_responses: dict[str, session_execute_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionExecuteResult]]: ...

    def execute(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        tool_slug: str | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        account: str | Omit = omit,
        enable_auto_workbench_offload: bool | Omit = omit,
        input_responses: dict[str, session_execute_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionExecuteResult]]:
        body_fields = compact(
            {
                "tool_slug": tool_slug,
                "arguments": arguments,
                "account": account,
                "enable_auto_workbench_offload": enable_auto_workbench_offload,
                "input_responses": input_responses,
                "request_state": request_state,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("tool_slug",),
            "body",
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}/execute",
                    {"session_id": session_id},
                ),
                cast_to=cast("type[SessionExecuteResult]", SessionExecuteResult),
                operation=_EXECUTE_OPERATION,
                body=body_data,
                body_model=SessionExecuteBody,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def execute_meta(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        slug: Literal[
            "COMPOSIO_SEARCH_TOOLS",
            "COMPOSIO_MULTI_EXECUTE_TOOL",
            "COMPOSIO_MANAGE_CONNECTIONS",
            "COMPOSIO_WAIT_FOR_CONNECTIONS",
            "COMPOSIO_REMOTE_WORKBENCH",
            "COMPOSIO_REMOTE_BASH_TOOL",
            "COMPOSIO_GET_TOOL_SCHEMAS",
            "COMPOSIO_SUBMIT_FEEDBACK",
            "COMPOSIO_PROXY_EXECUTE",
        ],
        arguments: dict[str, object | None] | Omit = omit,
        input_responses: dict[str, session_execute_meta_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_meta_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionExecuteMetaResult]]: ...

    @overload
    def execute_meta(
        self,
        session_id: str,
        body: BodyParam,
        *,
        slug: Literal[
            "COMPOSIO_SEARCH_TOOLS",
            "COMPOSIO_MULTI_EXECUTE_TOOL",
            "COMPOSIO_MANAGE_CONNECTIONS",
            "COMPOSIO_WAIT_FOR_CONNECTIONS",
            "COMPOSIO_REMOTE_WORKBENCH",
            "COMPOSIO_REMOTE_BASH_TOOL",
            "COMPOSIO_GET_TOOL_SCHEMAS",
            "COMPOSIO_SUBMIT_FEEDBACK",
            "COMPOSIO_PROXY_EXECUTE",
        ]
        | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        input_responses: dict[str, session_execute_meta_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_meta_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionExecuteMetaResult]]: ...

    def execute_meta(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        slug: Literal[
            "COMPOSIO_SEARCH_TOOLS",
            "COMPOSIO_MULTI_EXECUTE_TOOL",
            "COMPOSIO_MANAGE_CONNECTIONS",
            "COMPOSIO_WAIT_FOR_CONNECTIONS",
            "COMPOSIO_REMOTE_WORKBENCH",
            "COMPOSIO_REMOTE_BASH_TOOL",
            "COMPOSIO_GET_TOOL_SCHEMAS",
            "COMPOSIO_SUBMIT_FEEDBACK",
            "COMPOSIO_PROXY_EXECUTE",
        ]
        | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        input_responses: dict[str, session_execute_meta_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_meta_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionExecuteMetaResult]]:
        body_fields = compact(
            {
                "slug": slug,
                "arguments": arguments,
                "input_responses": input_responses,
                "request_state": request_state,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("slug",),
            "body",
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}/execute_meta",
                    {"session_id": session_id},
                ),
                cast_to=cast("type[SessionExecuteMetaResult]", SessionExecuteMetaResult),
                operation=_EXECUTE_META_OPERATION,
                body=body_data,
                body_model=SessionExecuteMetaBody,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def link(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        toolkit: str,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        experimental: session_link_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionLinkResponse]]: ...

    @overload
    def link(
        self,
        session_id: str,
        body: BodyParam,
        *,
        toolkit: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        experimental: session_link_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionLinkResponse]]: ...

    def link(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        toolkit: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        experimental: session_link_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionLinkResponse]]:
        body_fields = compact(
            {
                "toolkit": toolkit,
                "alias": alias,
                "callback_url": callback_url,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit",),
            "body",
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}/link",
                    {"session_id": session_id},
                ),
                cast_to=SessionLinkResponse,
                operation=_LINK_OPERATION,
                body=body_data,
                body_model=SessionLinkBody,
                options=options_data,
                stream=True,
            )
        )

    def patch(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        toolkits: session_patch_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | None | Omit = omit,
        instant: Literal[False] | session_patch_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_patch_params.ManageConnections | None | Omit = omit,
        tools: dict[str, session_patch_params.Tools] | Omit = omit,
        tags: session_patch_params.Tags | Omit = omit,
        workbench: session_patch_params.Workbench | None | Omit = omit,
        multi_account: session_patch_params.MultiAccount | None | Omit = omit,
        proxy_execute: session_patch_params.CurrentProxyExecute | None | Omit = omit,
        preload: session_patch_params.Preload | Omit = omit,
        search: session_patch_params.Search | Omit = omit,
        execute: session_patch_params.Execute | Omit = omit,
        hooks: Iterable[session_patch_params.CurrentHookVariant0 | session_patch_params.CurrentHookVariant1]
        | None
        | Omit = omit,
        experimental: session_patch_params.Experimental | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionPatchResponse]]:
        body_fields = compact(
            {
                "toolkits": toolkits,
                "auth_configs": auth_configs,
                "connected_accounts": connected_accounts,
                "instant": instant,
                "manage_connections": manage_connections,
                "tools": tools,
                "tags": tags,
                "workbench": workbench,
                "multi_account": multi_account,
                "proxy_execute": proxy_execute,
                "preload": preload,
                "search": search,
                "execute": execute,
                "hooks": hooks,
                "experimental": experimental,
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
                "patch",
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}",
                    {"session_id": session_id},
                ),
                cast_to=SessionPatchResponse,
                operation=_PATCH_OPERATION,
                body=body_data,
                body_model=SessionPatchBody,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def proxy_execute(
        self,
        session_id: str,
        *,
        toolkit_slug: str,
        endpoint: str,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"],
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionProxyExecuteResult]]: ...

    @overload
    def proxy_execute(
        self,
        session_id: str,
        *,
        toolkit_slug: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionProxyExecuteResult]]: ...

    @overload
    def proxy_execute(
        self,
        session_id: str,
        legacy_body: BodyParam,
        /,
        *,
        toolkit_slug: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionProxyExecuteResult]]: ...

    def proxy_execute(
        self,
        session_id: str,
        *legacy_body: object,
        toolkit_slug: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionProxyExecuteResult]]:
        body = normalize_body_argument(body, legacy_body)
        body_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "endpoint": endpoint,
                "method": method,
                "binary_body": binary_body,
                "parameters": parameters,
                "custom_connection_data": custom_connection_data,
            }
        )
        aggregate_body, body_value = split_body_argument(
            body,
            body_fields,
            (
                "toolkit_slug",
                "endpoint",
                "method",
                "body",
                "binary_body",
                "parameters",
                "custom_connection_data",
            ),
        )
        body_fields.update(compact({"body": body_value}))
        require_fields(
            aggregate_body,
            body_fields,
            ("toolkit_slug", "endpoint", "method"),
            "body",
        )
        body_data = merge_body(aggregate_body, body_fields)
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}/proxy_execute",
                    {"session_id": session_id},
                ),
                cast_to=cast("type[SessionProxyExecuteResult]", SessionProxyExecuteResult),
                operation=_PROXY_EXECUTE_OPERATION,
                body=body_data,
                body_model=SessionProxyExecuteBody,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def search(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        queries: Iterable[session_search_params.Query],
        model: str | Omit = omit,
        search_strategy: Literal["auto", "tool_search"] | Omit = omit,
        experimental: session_search_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionSearchResponse]]: ...

    @overload
    def search(
        self,
        session_id: str,
        body: BodyParam,
        *,
        queries: Iterable[session_search_params.Query] | Omit = omit,
        model: str | Omit = omit,
        search_strategy: Literal["auto", "tool_search"] | Omit = omit,
        experimental: session_search_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionSearchResponse]]: ...

    def search(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        queries: Iterable[session_search_params.Query] | Omit = omit,
        model: str | Omit = omit,
        search_strategy: Literal["auto", "tool_search"] | Omit = omit,
        experimental: session_search_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionSearchResponse]]:
        body_fields = compact(
            {
                "queries": queries,
                "model": model,
                "search_strategy": search_strategy,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("queries",),
            "body",
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}/search",
                    {"session_id": session_id},
                ),
                cast_to=SessionSearchResponse,
                operation=_SEARCH_OPERATION,
                body=body_data,
                body_model=SessionSearchBody,
                options=options_data,
                stream=True,
            )
        )

    def toolkits(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        toolkits: SequenceNotStr[str] | None | Omit = omit,
        is_connected: bool | None | Omit = omit,
        search: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionToolkitsResponse]]:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
                "toolkits": toolkits,
                "is_connected": is_connected,
                "search": search,
            }
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}/toolkits",
                    {"session_id": session_id},
                ),
                cast_to=SessionToolkitsResponse,
                operation=_TOOLKITS_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def tools(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionToolsResponse]]:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
            }
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}/tools",
                    {"session_id": session_id},
                ),
                cast_to=SessionToolsResponse,
                operation=_TOOLS_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )


class AsyncSessionResourceWithStreamingResponse:
    def __init__(self, resource: AsyncSessionResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        user_id: str,
        toolkits: session_create_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        instant: Literal[False] | session_create_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_create_params.ManageConnections | Omit = omit,
        tools: dict[str, session_create_params.Tools] | Omit = omit,
        tags: session_create_params.Tags | Omit = omit,
        workbench: session_create_params.Workbench | Omit = omit,
        proxy_execute: session_create_params.CurrentProxyExecute | Omit = omit,
        multi_account: session_create_params.MultiAccount | Omit = omit,
        experimental: session_create_params.Experimental | Omit = omit,
        preload: session_create_params.Preload | Omit = omit,
        hooks: Iterable[session_create_params.CurrentHookVariant0 | session_create_params.CurrentHookVariant1]
        | Omit = omit,
        search: session_create_params.Search | Omit = omit,
        execute: session_create_params.Execute | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        user_id: str | Omit = omit,
        toolkits: session_create_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        instant: Literal[False] | session_create_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_create_params.ManageConnections | Omit = omit,
        tools: dict[str, session_create_params.Tools] | Omit = omit,
        tags: session_create_params.Tags | Omit = omit,
        workbench: session_create_params.Workbench | Omit = omit,
        proxy_execute: session_create_params.CurrentProxyExecute | Omit = omit,
        multi_account: session_create_params.MultiAccount | Omit = omit,
        experimental: session_create_params.Experimental | Omit = omit,
        preload: session_create_params.Preload | Omit = omit,
        hooks: Iterable[session_create_params.CurrentHookVariant0 | session_create_params.CurrentHookVariant1]
        | Omit = omit,
        search: session_create_params.Search | Omit = omit,
        execute: session_create_params.Execute | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        user_id: str | Omit = omit,
        toolkits: session_create_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        instant: Literal[False] | session_create_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_create_params.ManageConnections | Omit = omit,
        tools: dict[str, session_create_params.Tools] | Omit = omit,
        tags: session_create_params.Tags | Omit = omit,
        workbench: session_create_params.Workbench | Omit = omit,
        proxy_execute: session_create_params.CurrentProxyExecute | Omit = omit,
        multi_account: session_create_params.MultiAccount | Omit = omit,
        experimental: session_create_params.Experimental | Omit = omit,
        preload: session_create_params.Preload | Omit = omit,
        hooks: Iterable[session_create_params.CurrentHookVariant0 | session_create_params.CurrentHookVariant1]
        | Omit = omit,
        search: session_create_params.Search | Omit = omit,
        execute: session_create_params.Execute | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionCreateResponse]]:
        body_fields = compact(
            {
                "user_id": user_id,
                "toolkits": toolkits,
                "auth_configs": auth_configs,
                "connected_accounts": connected_accounts,
                "instant": instant,
                "manage_connections": manage_connections,
                "tools": tools,
                "tags": tags,
                "workbench": workbench,
                "proxy_execute": proxy_execute,
                "multi_account": multi_account,
                "experimental": experimental,
                "preload": preload,
                "hooks": hooks,
                "search": search,
                "execute": execute,
            }
        )
        require_fields(
            body,
            body_fields,
            ("user_id",),
            "body",
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
                "/api/v3.1/tool_router/session",
                cast_to=SessionCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=SessionCreateBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve(
        self,
        session_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionRetrieveResponse]]:
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}",
                    {"session_id": session_id},
                ),
                cast_to=SessionRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def delete(
        self,
        session_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionDeleteResponse]]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return AsyncResponseContextManager(
            self._client._request_raw(
                "delete",
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}",
                    {"session_id": session_id},
                ),
                cast_to=SessionDeleteResponse,
                operation=_DELETE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def attach(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        experimental: session_attach_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionAttachResponse]]:
        body_fields = compact(
            {
                "experimental": experimental,
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}/attach",
                    {"session_id": session_id},
                ),
                cast_to=SessionAttachResponse,
                operation=_ATTACH_OPERATION,
                body=body_data,
                body_model=SessionAttachBody,
                options=options_data,
                stream=True,
            )
        )

    def config_history(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionConfigHistoryResponse]]:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
            }
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}/config_history",
                    {"session_id": session_id},
                ),
                cast_to=SessionConfigHistoryResponse,
                operation=_CONFIG_HISTORY_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def execute(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        tool_slug: str,
        arguments: dict[str, object | None] | Omit = omit,
        account: str | Omit = omit,
        enable_auto_workbench_offload: bool | Omit = omit,
        input_responses: dict[str, session_execute_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionExecuteResult]]: ...

    @overload
    def execute(
        self,
        session_id: str,
        body: BodyParam,
        *,
        tool_slug: str | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        account: str | Omit = omit,
        enable_auto_workbench_offload: bool | Omit = omit,
        input_responses: dict[str, session_execute_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionExecuteResult]]: ...

    def execute(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        tool_slug: str | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        account: str | Omit = omit,
        enable_auto_workbench_offload: bool | Omit = omit,
        input_responses: dict[str, session_execute_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionExecuteResult]]:
        body_fields = compact(
            {
                "tool_slug": tool_slug,
                "arguments": arguments,
                "account": account,
                "enable_auto_workbench_offload": enable_auto_workbench_offload,
                "input_responses": input_responses,
                "request_state": request_state,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("tool_slug",),
            "body",
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}/execute",
                    {"session_id": session_id},
                ),
                cast_to=cast("type[SessionExecuteResult]", SessionExecuteResult),
                operation=_EXECUTE_OPERATION,
                body=body_data,
                body_model=SessionExecuteBody,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def execute_meta(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        slug: Literal[
            "COMPOSIO_SEARCH_TOOLS",
            "COMPOSIO_MULTI_EXECUTE_TOOL",
            "COMPOSIO_MANAGE_CONNECTIONS",
            "COMPOSIO_WAIT_FOR_CONNECTIONS",
            "COMPOSIO_REMOTE_WORKBENCH",
            "COMPOSIO_REMOTE_BASH_TOOL",
            "COMPOSIO_GET_TOOL_SCHEMAS",
            "COMPOSIO_SUBMIT_FEEDBACK",
            "COMPOSIO_PROXY_EXECUTE",
        ],
        arguments: dict[str, object | None] | Omit = omit,
        input_responses: dict[str, session_execute_meta_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_meta_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionExecuteMetaResult]]: ...

    @overload
    def execute_meta(
        self,
        session_id: str,
        body: BodyParam,
        *,
        slug: Literal[
            "COMPOSIO_SEARCH_TOOLS",
            "COMPOSIO_MULTI_EXECUTE_TOOL",
            "COMPOSIO_MANAGE_CONNECTIONS",
            "COMPOSIO_WAIT_FOR_CONNECTIONS",
            "COMPOSIO_REMOTE_WORKBENCH",
            "COMPOSIO_REMOTE_BASH_TOOL",
            "COMPOSIO_GET_TOOL_SCHEMAS",
            "COMPOSIO_SUBMIT_FEEDBACK",
            "COMPOSIO_PROXY_EXECUTE",
        ]
        | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        input_responses: dict[str, session_execute_meta_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_meta_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionExecuteMetaResult]]: ...

    def execute_meta(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        slug: Literal[
            "COMPOSIO_SEARCH_TOOLS",
            "COMPOSIO_MULTI_EXECUTE_TOOL",
            "COMPOSIO_MANAGE_CONNECTIONS",
            "COMPOSIO_WAIT_FOR_CONNECTIONS",
            "COMPOSIO_REMOTE_WORKBENCH",
            "COMPOSIO_REMOTE_BASH_TOOL",
            "COMPOSIO_GET_TOOL_SCHEMAS",
            "COMPOSIO_SUBMIT_FEEDBACK",
            "COMPOSIO_PROXY_EXECUTE",
        ]
        | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        input_responses: dict[str, session_execute_meta_params.CurrentInputResponsesValue] | Omit = omit,
        request_state: str | Omit = omit,
        experimental: session_execute_meta_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionExecuteMetaResult]]:
        body_fields = compact(
            {
                "slug": slug,
                "arguments": arguments,
                "input_responses": input_responses,
                "request_state": request_state,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("slug",),
            "body",
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}/execute_meta",
                    {"session_id": session_id},
                ),
                cast_to=cast("type[SessionExecuteMetaResult]", SessionExecuteMetaResult),
                operation=_EXECUTE_META_OPERATION,
                body=body_data,
                body_model=SessionExecuteMetaBody,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def link(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        toolkit: str,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        experimental: session_link_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionLinkResponse]]: ...

    @overload
    def link(
        self,
        session_id: str,
        body: BodyParam,
        *,
        toolkit: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        experimental: session_link_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionLinkResponse]]: ...

    def link(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        toolkit: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        experimental: session_link_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionLinkResponse]]:
        body_fields = compact(
            {
                "toolkit": toolkit,
                "alias": alias,
                "callback_url": callback_url,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit",),
            "body",
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}/link",
                    {"session_id": session_id},
                ),
                cast_to=SessionLinkResponse,
                operation=_LINK_OPERATION,
                body=body_data,
                body_model=SessionLinkBody,
                options=options_data,
                stream=True,
            )
        )

    def patch(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        toolkits: session_patch_params.Toolkits | Omit = omit,
        auth_configs: dict[str, str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | None | Omit = omit,
        instant: Literal[False] | session_patch_params.CurrentInstantVariant1 | Omit = omit,
        manage_connections: session_patch_params.ManageConnections | None | Omit = omit,
        tools: dict[str, session_patch_params.Tools] | Omit = omit,
        tags: session_patch_params.Tags | Omit = omit,
        workbench: session_patch_params.Workbench | None | Omit = omit,
        multi_account: session_patch_params.MultiAccount | None | Omit = omit,
        proxy_execute: session_patch_params.CurrentProxyExecute | None | Omit = omit,
        preload: session_patch_params.Preload | Omit = omit,
        search: session_patch_params.Search | Omit = omit,
        execute: session_patch_params.Execute | Omit = omit,
        hooks: Iterable[session_patch_params.CurrentHookVariant0 | session_patch_params.CurrentHookVariant1]
        | None
        | Omit = omit,
        experimental: session_patch_params.Experimental | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionPatchResponse]]:
        body_fields = compact(
            {
                "toolkits": toolkits,
                "auth_configs": auth_configs,
                "connected_accounts": connected_accounts,
                "instant": instant,
                "manage_connections": manage_connections,
                "tools": tools,
                "tags": tags,
                "workbench": workbench,
                "multi_account": multi_account,
                "proxy_execute": proxy_execute,
                "preload": preload,
                "search": search,
                "execute": execute,
                "hooks": hooks,
                "experimental": experimental,
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
                "patch",
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}",
                    {"session_id": session_id},
                ),
                cast_to=SessionPatchResponse,
                operation=_PATCH_OPERATION,
                body=body_data,
                body_model=SessionPatchBody,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def proxy_execute(
        self,
        session_id: str,
        *,
        toolkit_slug: str,
        endpoint: str,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"],
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionProxyExecuteResult]]: ...

    @overload
    def proxy_execute(
        self,
        session_id: str,
        *,
        toolkit_slug: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionProxyExecuteResult]]: ...

    @overload
    def proxy_execute(
        self,
        session_id: str,
        legacy_body: BodyParam,
        /,
        *,
        toolkit_slug: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionProxyExecuteResult]]: ...

    def proxy_execute(
        self,
        session_id: str,
        *legacy_body: object,
        toolkit_slug: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: session_proxy_execute_params.BinaryBody | Omit = omit,
        parameters: Iterable[session_proxy_execute_params.Parameter] | Omit = omit,
        custom_connection_data: session_proxy_execute_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionProxyExecuteResult]]:
        body = normalize_body_argument(body, legacy_body)
        body_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "endpoint": endpoint,
                "method": method,
                "binary_body": binary_body,
                "parameters": parameters,
                "custom_connection_data": custom_connection_data,
            }
        )
        aggregate_body, body_value = split_body_argument(
            body,
            body_fields,
            (
                "toolkit_slug",
                "endpoint",
                "method",
                "body",
                "binary_body",
                "parameters",
                "custom_connection_data",
            ),
        )
        body_fields.update(compact({"body": body_value}))
        require_fields(
            aggregate_body,
            body_fields,
            ("toolkit_slug", "endpoint", "method"),
            "body",
        )
        body_data = merge_body(aggregate_body, body_fields)
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}/proxy_execute",
                    {"session_id": session_id},
                ),
                cast_to=cast("type[SessionProxyExecuteResult]", SessionProxyExecuteResult),
                operation=_PROXY_EXECUTE_OPERATION,
                body=body_data,
                body_model=SessionProxyExecuteBody,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def search(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        queries: Iterable[session_search_params.Query],
        model: str | Omit = omit,
        search_strategy: Literal["auto", "tool_search"] | Omit = omit,
        experimental: session_search_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionSearchResponse]]: ...

    @overload
    def search(
        self,
        session_id: str,
        body: BodyParam,
        *,
        queries: Iterable[session_search_params.Query] | Omit = omit,
        model: str | Omit = omit,
        search_strategy: Literal["auto", "tool_search"] | Omit = omit,
        experimental: session_search_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionSearchResponse]]: ...

    def search(
        self,
        session_id: str,
        body: BodyParam | None = None,
        *,
        queries: Iterable[session_search_params.Query] | Omit = omit,
        model: str | Omit = omit,
        search_strategy: Literal["auto", "tool_search"] | Omit = omit,
        experimental: session_search_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionSearchResponse]]:
        body_fields = compact(
            {
                "queries": queries,
                "model": model,
                "search_strategy": search_strategy,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("queries",),
            "body",
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}/search",
                    {"session_id": session_id},
                ),
                cast_to=SessionSearchResponse,
                operation=_SEARCH_OPERATION,
                body=body_data,
                body_model=SessionSearchBody,
                options=options_data,
                stream=True,
            )
        )

    def toolkits(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        toolkits: SequenceNotStr[str] | None | Omit = omit,
        is_connected: bool | None | Omit = omit,
        search: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionToolkitsResponse]]:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
                "toolkits": toolkits,
                "is_connected": is_connected,
                "search": search,
            }
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}/toolkits",
                    {"session_id": session_id},
                ),
                cast_to=SessionToolkitsResponse,
                operation=_TOOLKITS_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def tools(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionToolsResponse]]:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
            }
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
                build_path(
                    "/api/v3.1/tool_router/session/{session_id}/tools",
                    {"session_id": session_id},
                ),
                cast_to=SessionToolsResponse,
                operation=_TOOLS_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )
