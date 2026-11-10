# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import api_key_create_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.api_key import APIKey

__all__ = ["APIKeysResource", "AsyncAPIKeysResource"]


class APIKeysResource(SyncAPIResource):
    """Create project-scoped API keys using an organization-scoped API key."""

    @cached_property
    def with_raw_response(self) -> APIKeysResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#accessing-raw-response-data-eg-headers
        """
        return APIKeysResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> APIKeysResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#with_streaming_response
        """
        return APIKeysResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str | Omit = omit,
        project_id: str | Omit = omit,
        scope_type: Literal["project", "global"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> APIKey:
        """
        Create a project-scoped API key using a global (organization-scoped) API key.
        Supply projectId for an active project in the authenticated organization;
        scopeType must be project or omitted. Project-scoped API keys cannot create
        keys, and global keys cannot create other global keys. Dashboard users may also
        create project keys, or global keys with organization admin access. Returns the
        full secret once with Cache-Control: no-store; save it securely. The new key is
        independent: revoking the creating global key does not revoke keys it created.
        Missing projectId returns 400; insufficient scope returns 403; an unavailable or
        foreign project returns 404.

        Args:
          name: A human-readable label for the new key. Defaults to Default.

          project_id: The active project to bind the new key to, belonging to the authenticated
              organization. Required when authenticating with a global API key. Dashboard
              users may omit it to use their default project.

          scope_type: Defaults to `project`. Global API keys may only create project-scoped keys. Only
              organization admins using dashboard authentication may create a `global` key;
              projectId is ignored for those keys.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/api-keys",
            body=maybe_transform(
                {
                    "name": name,
                    "project_id": project_id,
                    "scope_type": scope_type,
                },
                api_key_create_params.APIKeyCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIKey,
        )


class AsyncAPIKeysResource(AsyncAPIResource):
    """Create project-scoped API keys using an organization-scoped API key."""

    @cached_property
    def with_raw_response(self) -> AsyncAPIKeysResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#accessing-raw-response-data-eg-headers
        """
        return AsyncAPIKeysResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAPIKeysResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#with_streaming_response
        """
        return AsyncAPIKeysResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str | Omit = omit,
        project_id: str | Omit = omit,
        scope_type: Literal["project", "global"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> APIKey:
        """
        Create a project-scoped API key using a global (organization-scoped) API key.
        Supply projectId for an active project in the authenticated organization;
        scopeType must be project or omitted. Project-scoped API keys cannot create
        keys, and global keys cannot create other global keys. Dashboard users may also
        create project keys, or global keys with organization admin access. Returns the
        full secret once with Cache-Control: no-store; save it securely. The new key is
        independent: revoking the creating global key does not revoke keys it created.
        Missing projectId returns 400; insufficient scope returns 403; an unavailable or
        foreign project returns 404.

        Args:
          name: A human-readable label for the new key. Defaults to Default.

          project_id: The active project to bind the new key to, belonging to the authenticated
              organization. Required when authenticating with a global API key. Dashboard
              users may omit it to use their default project.

          scope_type: Defaults to `project`. Global API keys may only create project-scoped keys. Only
              organization admins using dashboard authentication may create a `global` key;
              projectId is ignored for those keys.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/api-keys",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "project_id": project_id,
                    "scope_type": scope_type,
                },
                api_key_create_params.APIKeyCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIKey,
        )


class APIKeysResourceWithRawResponse:
    def __init__(self, api_keys: APIKeysResource) -> None:
        self._api_keys = api_keys

        self.create = to_raw_response_wrapper(
            api_keys.create,
        )


class AsyncAPIKeysResourceWithRawResponse:
    def __init__(self, api_keys: AsyncAPIKeysResource) -> None:
        self._api_keys = api_keys

        self.create = async_to_raw_response_wrapper(
            api_keys.create,
        )


class APIKeysResourceWithStreamingResponse:
    def __init__(self, api_keys: APIKeysResource) -> None:
        self._api_keys = api_keys

        self.create = to_streamed_response_wrapper(
            api_keys.create,
        )


class AsyncAPIKeysResourceWithStreamingResponse:
    def __init__(self, api_keys: AsyncAPIKeysResource) -> None:
        self._api_keys = api_keys

        self.create = async_to_streamed_response_wrapper(
            api_keys.create,
        )
