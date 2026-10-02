# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncCursorPage, AsyncCursorPage
from ...types.admin import api_key_list_params, api_key_create_params
from ..._base_client import AsyncPaginator, make_request_options
from ...types.admin.api_key_list_response import APIKeyListResponse
from ...types.admin.api_key_create_response import APIKeyCreateResponse
from ...types.admin.api_key_revoke_response import APIKeyRevokeResponse

__all__ = ["APIKeysResource", "AsyncAPIKeysResource"]


class APIKeysResource(SyncAPIResource):
    """API keys authenticate requests to the Boltz API.

    There are two key types: admin keys have full access to all management and compute operations across the organization, while workspace keys are scoped to a single workspace and can only perform compute operations (predictions, protein design, small molecule design) within that workspace. Keys can be created in live or test mode. Test keys (prefixed `sk_bc_*_test_`) create test-mode resources with synthetic data and no GPU cost. Every resource includes a `livemode` field indicating its mode.
    """

    @cached_property
    def with_raw_response(self) -> APIKeysResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return APIKeysResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> APIKeysResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return APIKeysResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        allowed_ips: SequenceNotStr[str] | Omit = omit,
        expires_in_days: int | Omit = omit,
        mode: Literal["live", "test"] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> APIKeyCreateResponse:
        """
        Create a workspace API key

        Args:
          name: API key name

          allowed_ips: IP addresses allowed to use this key (IPv4 or IPv6). An empty array (the
              default) means all IPs are allowed.

          expires_in_days: Days until the key expires. Omit for a key that does not expire.

          mode: Key mode. Test keys create test-mode resources with synthetic data.

          workspace_id: Workspace ID to scope this key to. Omit for default workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/compute/v1/admin/api-keys",
            body=maybe_transform(
                {
                    "name": name,
                    "allowed_ips": allowed_ips,
                    "expires_in_days": expires_in_days,
                    "mode": mode,
                    "workspace_id": workspace_id,
                },
                api_key_create_params.APIKeyCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIKeyCreateResponse,
        )

    def list(
        self,
        *,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        limit: int | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPage[APIKeyListResponse]:
        """
        List API keys

        Args:
          after_id: Return results after this ID

          before_id: Return results before this ID

          limit: Max items to return

          workspace_id: Filter by workspace ID. If not provided, returns keys across all workspaces.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/compute/v1/admin/api-keys",
            page=SyncCursorPage[APIKeyListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "limit": limit,
                        "workspace_id": workspace_id,
                    },
                    api_key_list_params.APIKeyListParams,
                ),
            ),
            model=APIKeyListResponse,
        )

    def revoke(
        self,
        api_key_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> APIKeyRevokeResponse:
        """
        Revoke an API key

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not api_key_id:
            raise ValueError(f"Expected a non-empty value for `api_key_id` but received {api_key_id!r}")
        return self._post(
            path_template("/compute/v1/admin/api-keys/{api_key_id}/revoke", api_key_id=api_key_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIKeyRevokeResponse,
        )


class AsyncAPIKeysResource(AsyncAPIResource):
    """API keys authenticate requests to the Boltz API.

    There are two key types: admin keys have full access to all management and compute operations across the organization, while workspace keys are scoped to a single workspace and can only perform compute operations (predictions, protein design, small molecule design) within that workspace. Keys can be created in live or test mode. Test keys (prefixed `sk_bc_*_test_`) create test-mode resources with synthetic data and no GPU cost. Every resource includes a `livemode` field indicating its mode.
    """

    @cached_property
    def with_raw_response(self) -> AsyncAPIKeysResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAPIKeysResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAPIKeysResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return AsyncAPIKeysResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        allowed_ips: SequenceNotStr[str] | Omit = omit,
        expires_in_days: int | Omit = omit,
        mode: Literal["live", "test"] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> APIKeyCreateResponse:
        """
        Create a workspace API key

        Args:
          name: API key name

          allowed_ips: IP addresses allowed to use this key (IPv4 or IPv6). An empty array (the
              default) means all IPs are allowed.

          expires_in_days: Days until the key expires. Omit for a key that does not expire.

          mode: Key mode. Test keys create test-mode resources with synthetic data.

          workspace_id: Workspace ID to scope this key to. Omit for default workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/compute/v1/admin/api-keys",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "allowed_ips": allowed_ips,
                    "expires_in_days": expires_in_days,
                    "mode": mode,
                    "workspace_id": workspace_id,
                },
                api_key_create_params.APIKeyCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIKeyCreateResponse,
        )

    def list(
        self,
        *,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        limit: int | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[APIKeyListResponse, AsyncCursorPage[APIKeyListResponse]]:
        """
        List API keys

        Args:
          after_id: Return results after this ID

          before_id: Return results before this ID

          limit: Max items to return

          workspace_id: Filter by workspace ID. If not provided, returns keys across all workspaces.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/compute/v1/admin/api-keys",
            page=AsyncCursorPage[APIKeyListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "limit": limit,
                        "workspace_id": workspace_id,
                    },
                    api_key_list_params.APIKeyListParams,
                ),
            ),
            model=APIKeyListResponse,
        )

    async def revoke(
        self,
        api_key_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> APIKeyRevokeResponse:
        """
        Revoke an API key

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not api_key_id:
            raise ValueError(f"Expected a non-empty value for `api_key_id` but received {api_key_id!r}")
        return await self._post(
            path_template("/compute/v1/admin/api-keys/{api_key_id}/revoke", api_key_id=api_key_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIKeyRevokeResponse,
        )


class APIKeysResourceWithRawResponse:
    def __init__(self, api_keys: APIKeysResource) -> None:
        self._api_keys = api_keys

        self.create = to_raw_response_wrapper(
            api_keys.create,
        )
        self.list = to_raw_response_wrapper(
            api_keys.list,
        )
        self.revoke = to_raw_response_wrapper(
            api_keys.revoke,
        )


class AsyncAPIKeysResourceWithRawResponse:
    def __init__(self, api_keys: AsyncAPIKeysResource) -> None:
        self._api_keys = api_keys

        self.create = async_to_raw_response_wrapper(
            api_keys.create,
        )
        self.list = async_to_raw_response_wrapper(
            api_keys.list,
        )
        self.revoke = async_to_raw_response_wrapper(
            api_keys.revoke,
        )


class APIKeysResourceWithStreamingResponse:
    def __init__(self, api_keys: APIKeysResource) -> None:
        self._api_keys = api_keys

        self.create = to_streamed_response_wrapper(
            api_keys.create,
        )
        self.list = to_streamed_response_wrapper(
            api_keys.list,
        )
        self.revoke = to_streamed_response_wrapper(
            api_keys.revoke,
        )


class AsyncAPIKeysResourceWithStreamingResponse:
    def __init__(self, api_keys: AsyncAPIKeysResource) -> None:
        self._api_keys = api_keys

        self.create = async_to_streamed_response_wrapper(
            api_keys.create,
        )
        self.list = async_to_streamed_response_wrapper(
            api_keys.list,
        )
        self.revoke = async_to_streamed_response_wrapper(
            api_keys.revoke,
        )
