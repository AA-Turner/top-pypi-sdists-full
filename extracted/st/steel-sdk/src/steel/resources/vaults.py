# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import (
    vault_list_params,
    vault_create_params,
    vault_delete_params,
    vault_update_params,
    vault_retrieve_params,
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
from ..types.vault import Vault
from .._base_client import make_request_options
from ..types.vault_list import VaultList

__all__ = ["VaultsResource", "AsyncVaultsResource"]


class VaultsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> VaultsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#accessing-raw-response-data-eg-headers
        """
        return VaultsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VaultsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#with_streaming_response
        """
        return VaultsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        description: Optional[str] | Omit = omit,
        project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Vault:
        """
        Create a Vault

        Args:
          name: 1–63 lowercase letters, digits, hyphens, underscores or dots; must start with a
              letter or digit.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/vaults",
            body=maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "project_id": project_id,
                },
                vault_create_params.VaultCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Vault,
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
    ) -> Vault:
        """
        Get a Vault

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/v1/vaults/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"project_id": project_id}, vault_retrieve_params.VaultRetrieveParams),
            ),
            cast_to=Vault,
        )

    def update(
        self,
        id: str,
        *,
        project_id: str | Omit = omit,
        description: Optional[str] | Omit = omit,
        name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Vault:
        """
        Update a Vault

        Args:
          name: 1–63 lowercase letters, digits, hyphens, underscores or dots; must start with a
              letter or digit.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._patch(
            path_template("/v1/vaults/{id}", id=id),
            body=maybe_transform(
                {
                    "description": description,
                    "name": name,
                },
                vault_update_params.VaultUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"project_id": project_id}, vault_update_params.VaultUpdateParams),
            ),
            cast_to=Vault,
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
    ) -> VaultList:
        """
        List Vaults

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/vaults",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"project_id": project_id}, vault_list_params.VaultListParams),
            ),
            cast_to=VaultList,
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
        """Soft-delete a Vault.

        Returns 409 while it contains any live Secrets or
        credentials; move or delete them first.

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
            path_template("/v1/vaults/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"project_id": project_id}, vault_delete_params.VaultDeleteParams),
            ),
            cast_to=NoneType,
        )


class AsyncVaultsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVaultsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#accessing-raw-response-data-eg-headers
        """
        return AsyncVaultsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVaultsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#with_streaming_response
        """
        return AsyncVaultsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        description: Optional[str] | Omit = omit,
        project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Vault:
        """
        Create a Vault

        Args:
          name: 1–63 lowercase letters, digits, hyphens, underscores or dots; must start with a
              letter or digit.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/vaults",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "project_id": project_id,
                },
                vault_create_params.VaultCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Vault,
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
    ) -> Vault:
        """
        Get a Vault

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/v1/vaults/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"project_id": project_id}, vault_retrieve_params.VaultRetrieveParams
                ),
            ),
            cast_to=Vault,
        )

    async def update(
        self,
        id: str,
        *,
        project_id: str | Omit = omit,
        description: Optional[str] | Omit = omit,
        name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Vault:
        """
        Update a Vault

        Args:
          name: 1–63 lowercase letters, digits, hyphens, underscores or dots; must start with a
              letter or digit.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._patch(
            path_template("/v1/vaults/{id}", id=id),
            body=await async_maybe_transform(
                {
                    "description": description,
                    "name": name,
                },
                vault_update_params.VaultUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"project_id": project_id}, vault_update_params.VaultUpdateParams),
            ),
            cast_to=Vault,
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
    ) -> VaultList:
        """
        List Vaults

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/vaults",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"project_id": project_id}, vault_list_params.VaultListParams),
            ),
            cast_to=VaultList,
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
        """Soft-delete a Vault.

        Returns 409 while it contains any live Secrets or
        credentials; move or delete them first.

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
            path_template("/v1/vaults/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"project_id": project_id}, vault_delete_params.VaultDeleteParams),
            ),
            cast_to=NoneType,
        )


class VaultsResourceWithRawResponse:
    def __init__(self, vaults: VaultsResource) -> None:
        self._vaults = vaults

        self.create = to_raw_response_wrapper(
            vaults.create,
        )
        self.retrieve = to_raw_response_wrapper(
            vaults.retrieve,
        )
        self.update = to_raw_response_wrapper(
            vaults.update,
        )
        self.list = to_raw_response_wrapper(
            vaults.list,
        )
        self.delete = to_raw_response_wrapper(
            vaults.delete,
        )


class AsyncVaultsResourceWithRawResponse:
    def __init__(self, vaults: AsyncVaultsResource) -> None:
        self._vaults = vaults

        self.create = async_to_raw_response_wrapper(
            vaults.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            vaults.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            vaults.update,
        )
        self.list = async_to_raw_response_wrapper(
            vaults.list,
        )
        self.delete = async_to_raw_response_wrapper(
            vaults.delete,
        )


class VaultsResourceWithStreamingResponse:
    def __init__(self, vaults: VaultsResource) -> None:
        self._vaults = vaults

        self.create = to_streamed_response_wrapper(
            vaults.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            vaults.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            vaults.update,
        )
        self.list = to_streamed_response_wrapper(
            vaults.list,
        )
        self.delete = to_streamed_response_wrapper(
            vaults.delete,
        )


class AsyncVaultsResourceWithStreamingResponse:
    def __init__(self, vaults: AsyncVaultsResource) -> None:
        self._vaults = vaults

        self.create = async_to_streamed_response_wrapper(
            vaults.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            vaults.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            vaults.update,
        )
        self.list = async_to_streamed_response_wrapper(
            vaults.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            vaults.delete,
        )
