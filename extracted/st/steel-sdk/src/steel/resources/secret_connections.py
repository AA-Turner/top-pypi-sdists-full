# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal

import httpx

from ..types import (
    secret_connection_list_params,
    secret_connection_test_params,
    secret_connection_create_params,
    secret_connection_delete_params,
    secret_connection_update_params,
    secret_connection_retrieve_params,
)
from .._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.secret_connection_list_response import SecretConnectionListResponse
from ..types.secret_connection_create_response import SecretConnectionCreateResponse
from ..types.secret_connection_update_response import SecretConnectionUpdateResponse
from ..types.secret_connection_retrieve_response import SecretConnectionRetrieveResponse

__all__ = ["SecretConnectionsResource", "AsyncSecretConnectionsResource"]


class SecretConnectionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SecretConnectionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#accessing-raw-response-data-eg-headers
        """
        return SecretConnectionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SecretConnectionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#with_streaming_response
        """
        return SecretConnectionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        auth: secret_connection_create_params.Auth,
        name: str,
        provider: Literal["1password", "hashicorp_vault"],
        config: secret_connection_create_params.Config | Omit = omit,
        project_id: str | Omit = omit,
        token_budget: Optional[secret_connection_create_params.TokenBudget] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SecretConnectionCreateResponse:
        """Create a secret connection

        Args:
          auth: Write-only provider authentication.

        Supply a service account token for
              1Password, a token for HashiCorp token auth, or a role ID and secret ID for
              HashiCorp AppRole.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/secret-connections",
            body=maybe_transform(
                {
                    "auth": auth,
                    "name": name,
                    "provider": provider,
                    "config": config,
                    "project_id": project_id,
                    "token_budget": token_budget,
                },
                secret_connection_create_params.SecretConnectionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SecretConnectionCreateResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SecretConnectionRetrieveResponse:
        """
        Get a secret connection

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/v1/secret-connections/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"project_id": project_id}, secret_connection_retrieve_params.SecretConnectionRetrieveParams
                ),
            ),
            cast_to=SecretConnectionRetrieveResponse,
        )

    def update(
        self,
        id: str,
        *,
        project_id: str | Omit = omit,
        auth: secret_connection_update_params.Auth | Omit = omit,
        config: secret_connection_update_params.Config | Omit = omit,
        enabled: bool | Omit = omit,
        name: str | Omit = omit,
        token_budget: Optional[secret_connection_update_params.TokenBudget] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SecretConnectionUpdateResponse:
        """Update a secret connection

        Args:
          auth: Write-only provider authentication.

        Supply a service account token for
              1Password, a token for HashiCorp token auth, or a role ID and secret ID for
              HashiCorp AppRole.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._patch(
            path_template("/v1/secret-connections/{id}", id=id),
            body=maybe_transform(
                {
                    "auth": auth,
                    "config": config,
                    "enabled": enabled,
                    "name": name,
                    "token_budget": token_budget,
                },
                secret_connection_update_params.SecretConnectionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"project_id": project_id}, secret_connection_update_params.SecretConnectionUpdateParams
                ),
            ),
            cast_to=SecretConnectionUpdateResponse,
        )

    def list(
        self,
        *,
        project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SecretConnectionListResponse:
        """
        List secret connections

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/secret-connections",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"project_id": project_id}, secret_connection_list_params.SecretConnectionListParams
                ),
            ),
            cast_to=SecretConnectionListResponse,
        )

    def delete(
        self,
        id: str,
        *,
        project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Delete a secret connection

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            path_template("/v1/secret-connections/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"project_id": project_id}, secret_connection_delete_params.SecretConnectionDeleteParams
                ),
            ),
            cast_to=NoneType,
        )

    def test(
        self,
        id: str,
        *,
        project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Test a secret connection

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            path_template("/v1/secret-connections/{id}/test", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"project_id": project_id}, secret_connection_test_params.SecretConnectionTestParams
                ),
            ),
            cast_to=NoneType,
        )


class AsyncSecretConnectionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSecretConnectionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#accessing-raw-response-data-eg-headers
        """
        return AsyncSecretConnectionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSecretConnectionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#with_streaming_response
        """
        return AsyncSecretConnectionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        auth: secret_connection_create_params.Auth,
        name: str,
        provider: Literal["1password", "hashicorp_vault"],
        config: secret_connection_create_params.Config | Omit = omit,
        project_id: str | Omit = omit,
        token_budget: Optional[secret_connection_create_params.TokenBudget] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SecretConnectionCreateResponse:
        """Create a secret connection

        Args:
          auth: Write-only provider authentication.

        Supply a service account token for
              1Password, a token for HashiCorp token auth, or a role ID and secret ID for
              HashiCorp AppRole.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/secret-connections",
            body=await async_maybe_transform(
                {
                    "auth": auth,
                    "name": name,
                    "provider": provider,
                    "config": config,
                    "project_id": project_id,
                    "token_budget": token_budget,
                },
                secret_connection_create_params.SecretConnectionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SecretConnectionCreateResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SecretConnectionRetrieveResponse:
        """
        Get a secret connection

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/v1/secret-connections/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"project_id": project_id}, secret_connection_retrieve_params.SecretConnectionRetrieveParams
                ),
            ),
            cast_to=SecretConnectionRetrieveResponse,
        )

    async def update(
        self,
        id: str,
        *,
        project_id: str | Omit = omit,
        auth: secret_connection_update_params.Auth | Omit = omit,
        config: secret_connection_update_params.Config | Omit = omit,
        enabled: bool | Omit = omit,
        name: str | Omit = omit,
        token_budget: Optional[secret_connection_update_params.TokenBudget] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SecretConnectionUpdateResponse:
        """Update a secret connection

        Args:
          auth: Write-only provider authentication.

        Supply a service account token for
              1Password, a token for HashiCorp token auth, or a role ID and secret ID for
              HashiCorp AppRole.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._patch(
            path_template("/v1/secret-connections/{id}", id=id),
            body=await async_maybe_transform(
                {
                    "auth": auth,
                    "config": config,
                    "enabled": enabled,
                    "name": name,
                    "token_budget": token_budget,
                },
                secret_connection_update_params.SecretConnectionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"project_id": project_id}, secret_connection_update_params.SecretConnectionUpdateParams
                ),
            ),
            cast_to=SecretConnectionUpdateResponse,
        )

    async def list(
        self,
        *,
        project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SecretConnectionListResponse:
        """
        List secret connections

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/secret-connections",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"project_id": project_id}, secret_connection_list_params.SecretConnectionListParams
                ),
            ),
            cast_to=SecretConnectionListResponse,
        )

    async def delete(
        self,
        id: str,
        *,
        project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Delete a secret connection

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            path_template("/v1/secret-connections/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"project_id": project_id}, secret_connection_delete_params.SecretConnectionDeleteParams
                ),
            ),
            cast_to=NoneType,
        )

    async def test(
        self,
        id: str,
        *,
        project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Test a secret connection

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            path_template("/v1/secret-connections/{id}/test", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"project_id": project_id}, secret_connection_test_params.SecretConnectionTestParams
                ),
            ),
            cast_to=NoneType,
        )


class SecretConnectionsResourceWithRawResponse:
    def __init__(self, secret_connections: SecretConnectionsResource) -> None:
        self._secret_connections = secret_connections

        self.create = to_raw_response_wrapper(
            secret_connections.create,
        )
        self.retrieve = to_raw_response_wrapper(
            secret_connections.retrieve,
        )
        self.update = to_raw_response_wrapper(
            secret_connections.update,
        )
        self.list = to_raw_response_wrapper(
            secret_connections.list,
        )
        self.delete = to_raw_response_wrapper(
            secret_connections.delete,
        )
        self.test = to_raw_response_wrapper(
            secret_connections.test,
        )


class AsyncSecretConnectionsResourceWithRawResponse:
    def __init__(self, secret_connections: AsyncSecretConnectionsResource) -> None:
        self._secret_connections = secret_connections

        self.create = async_to_raw_response_wrapper(
            secret_connections.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            secret_connections.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            secret_connections.update,
        )
        self.list = async_to_raw_response_wrapper(
            secret_connections.list,
        )
        self.delete = async_to_raw_response_wrapper(
            secret_connections.delete,
        )
        self.test = async_to_raw_response_wrapper(
            secret_connections.test,
        )


class SecretConnectionsResourceWithStreamingResponse:
    def __init__(self, secret_connections: SecretConnectionsResource) -> None:
        self._secret_connections = secret_connections

        self.create = to_streamed_response_wrapper(
            secret_connections.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            secret_connections.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            secret_connections.update,
        )
        self.list = to_streamed_response_wrapper(
            secret_connections.list,
        )
        self.delete = to_streamed_response_wrapper(
            secret_connections.delete,
        )
        self.test = to_streamed_response_wrapper(
            secret_connections.test,
        )


class AsyncSecretConnectionsResourceWithStreamingResponse:
    def __init__(self, secret_connections: AsyncSecretConnectionsResource) -> None:
        self._secret_connections = secret_connections

        self.create = async_to_streamed_response_wrapper(
            secret_connections.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            secret_connections.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            secret_connections.update,
        )
        self.list = async_to_streamed_response_wrapper(
            secret_connections.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            secret_connections.delete,
        )
        self.test = async_to_streamed_response_wrapper(
            secret_connections.test,
        )
