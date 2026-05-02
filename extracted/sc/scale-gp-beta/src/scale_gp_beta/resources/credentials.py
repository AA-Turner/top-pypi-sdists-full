# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict

import httpx

from ..types import credential_list_params, credential_create_params, credential_update_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncCursorPage, AsyncCursorPage
from ..types.chat import SortOrder
from .._base_client import AsyncPaginator, make_request_options
from ..types.credential import Credential
from ..types.chat.sort_order import SortOrder
from ..types.credential_secret import CredentialSecret
from ..types.credential_delete_response import CredentialDeleteResponse

__all__ = ["CredentialsResource", "AsyncCredentialsResource"]


class CredentialsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CredentialsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return CredentialsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CredentialsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return CredentialsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        payload: str,
        type: str,
        credential_metadata: Dict[str, object] | Omit = omit,
        description: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Credential:
        """
        Create a new credential for storing sensitive data like API keys, tokens, or
        other secrets.

        Args:
          name: User-friendly name for the credential

          payload: The credential payload to be encrypted

          type: Type of credential: key or json

          credential_metadata: Optional unencrypted credential_metadata

          description: Optional description

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v5/credentials",
            body=maybe_transform(
                {
                    "name": name,
                    "payload": payload,
                    "type": type,
                    "credential_metadata": credential_metadata,
                    "description": description,
                },
                credential_create_params.CredentialCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Credential,
        )

    def retrieve(
        self,
        credential_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Credential:
        """
        Retrieve a specific credential by its unique identifier.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return self._get(
            path_template("/v5/credentials/{credential_id}", credential_id=credential_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Credential,
        )

    def update(
        self,
        credential_id: str,
        *,
        credential_metadata: Dict[str, object] | Omit = omit,
        description: str | Omit = omit,
        name: str | Omit = omit,
        payload: str | Omit = omit,
        type: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Credential:
        """
        Update an existing credential's properties including name, description, type,
        payload, and metadata.

        Args:
          credential_metadata: Optional unencrypted credential_metadata

          description: Optional description

          name: User-friendly name for the credential

          payload: The credential payload to be encrypted

          type: Type of credential: key or json

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return self._patch(
            path_template("/v5/credentials/{credential_id}", credential_id=credential_id),
            body=maybe_transform(
                {
                    "credential_metadata": credential_metadata,
                    "description": description,
                    "name": name,
                    "payload": payload,
                    "type": type,
                },
                credential_update_params.CredentialUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Credential,
        )

    def list(
        self,
        *,
        ending_before: str | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPage[Credential]:
        """
        Retrieve a paginated list of all credentials for the current account with
        optional name filtering.

        Args:
          name: Filter credentials by name

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/credentials",
            page=SyncCursorPage[Credential],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "limit": limit,
                        "name": name,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    credential_list_params.CredentialListParams,
                ),
            ),
            model=Credential,
        )

    def delete(
        self,
        credential_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CredentialDeleteResponse:
        """
        Permanently delete a credential and all its associated data.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return self._delete(
            path_template("/v5/credentials/{credential_id}", credential_id=credential_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CredentialDeleteResponse,
        )

    def decrypt(
        self,
        credential_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CredentialSecret:
        """
        Retrieve the plaintext payload of a credential by its ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return self._post(
            path_template("/v5/credentials/{credential_id}/secret", credential_id=credential_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CredentialSecret,
        )

    def decrypt_by_name(
        self,
        credential_name: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CredentialSecret:
        """
        Retrieve the plaintext payload of a credential by its name.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not credential_name:
            raise ValueError(f"Expected a non-empty value for `credential_name` but received {credential_name!r}")
        return self._post(
            path_template("/v5/credentials/name/{credential_name}/secret", credential_name=credential_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CredentialSecret,
        )

    def retrieve_by_name(
        self,
        credential_name: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Credential:
        """
        Retrieve a specific credential by its name.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not credential_name:
            raise ValueError(f"Expected a non-empty value for `credential_name` but received {credential_name!r}")
        return self._get(
            path_template("/v5/credentials/name/{credential_name}", credential_name=credential_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Credential,
        )


class AsyncCredentialsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCredentialsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncCredentialsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCredentialsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncCredentialsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        payload: str,
        type: str,
        credential_metadata: Dict[str, object] | Omit = omit,
        description: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Credential:
        """
        Create a new credential for storing sensitive data like API keys, tokens, or
        other secrets.

        Args:
          name: User-friendly name for the credential

          payload: The credential payload to be encrypted

          type: Type of credential: key or json

          credential_metadata: Optional unencrypted credential_metadata

          description: Optional description

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v5/credentials",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "payload": payload,
                    "type": type,
                    "credential_metadata": credential_metadata,
                    "description": description,
                },
                credential_create_params.CredentialCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Credential,
        )

    async def retrieve(
        self,
        credential_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Credential:
        """
        Retrieve a specific credential by its unique identifier.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return await self._get(
            path_template("/v5/credentials/{credential_id}", credential_id=credential_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Credential,
        )

    async def update(
        self,
        credential_id: str,
        *,
        credential_metadata: Dict[str, object] | Omit = omit,
        description: str | Omit = omit,
        name: str | Omit = omit,
        payload: str | Omit = omit,
        type: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Credential:
        """
        Update an existing credential's properties including name, description, type,
        payload, and metadata.

        Args:
          credential_metadata: Optional unencrypted credential_metadata

          description: Optional description

          name: User-friendly name for the credential

          payload: The credential payload to be encrypted

          type: Type of credential: key or json

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return await self._patch(
            path_template("/v5/credentials/{credential_id}", credential_id=credential_id),
            body=await async_maybe_transform(
                {
                    "credential_metadata": credential_metadata,
                    "description": description,
                    "name": name,
                    "payload": payload,
                    "type": type,
                },
                credential_update_params.CredentialUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Credential,
        )

    def list(
        self,
        *,
        ending_before: str | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Credential, AsyncCursorPage[Credential]]:
        """
        Retrieve a paginated list of all credentials for the current account with
        optional name filtering.

        Args:
          name: Filter credentials by name

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/credentials",
            page=AsyncCursorPage[Credential],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "limit": limit,
                        "name": name,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    credential_list_params.CredentialListParams,
                ),
            ),
            model=Credential,
        )

    async def delete(
        self,
        credential_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CredentialDeleteResponse:
        """
        Permanently delete a credential and all its associated data.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return await self._delete(
            path_template("/v5/credentials/{credential_id}", credential_id=credential_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CredentialDeleteResponse,
        )

    async def decrypt(
        self,
        credential_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CredentialSecret:
        """
        Retrieve the plaintext payload of a credential by its ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return await self._post(
            path_template("/v5/credentials/{credential_id}/secret", credential_id=credential_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CredentialSecret,
        )

    async def decrypt_by_name(
        self,
        credential_name: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CredentialSecret:
        """
        Retrieve the plaintext payload of a credential by its name.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not credential_name:
            raise ValueError(f"Expected a non-empty value for `credential_name` but received {credential_name!r}")
        return await self._post(
            path_template("/v5/credentials/name/{credential_name}/secret", credential_name=credential_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CredentialSecret,
        )

    async def retrieve_by_name(
        self,
        credential_name: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Credential:
        """
        Retrieve a specific credential by its name.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not credential_name:
            raise ValueError(f"Expected a non-empty value for `credential_name` but received {credential_name!r}")
        return await self._get(
            path_template("/v5/credentials/name/{credential_name}", credential_name=credential_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Credential,
        )


class CredentialsResourceWithRawResponse:
    def __init__(self, credentials: CredentialsResource) -> None:
        self._credentials = credentials

        self.create = to_raw_response_wrapper(
            credentials.create,
        )
        self.retrieve = to_raw_response_wrapper(
            credentials.retrieve,
        )
        self.update = to_raw_response_wrapper(
            credentials.update,
        )
        self.list = to_raw_response_wrapper(
            credentials.list,
        )
        self.delete = to_raw_response_wrapper(
            credentials.delete,
        )
        self.decrypt = to_raw_response_wrapper(
            credentials.decrypt,
        )
        self.decrypt_by_name = to_raw_response_wrapper(
            credentials.decrypt_by_name,
        )
        self.retrieve_by_name = to_raw_response_wrapper(
            credentials.retrieve_by_name,
        )


class AsyncCredentialsResourceWithRawResponse:
    def __init__(self, credentials: AsyncCredentialsResource) -> None:
        self._credentials = credentials

        self.create = async_to_raw_response_wrapper(
            credentials.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            credentials.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            credentials.update,
        )
        self.list = async_to_raw_response_wrapper(
            credentials.list,
        )
        self.delete = async_to_raw_response_wrapper(
            credentials.delete,
        )
        self.decrypt = async_to_raw_response_wrapper(
            credentials.decrypt,
        )
        self.decrypt_by_name = async_to_raw_response_wrapper(
            credentials.decrypt_by_name,
        )
        self.retrieve_by_name = async_to_raw_response_wrapper(
            credentials.retrieve_by_name,
        )


class CredentialsResourceWithStreamingResponse:
    def __init__(self, credentials: CredentialsResource) -> None:
        self._credentials = credentials

        self.create = to_streamed_response_wrapper(
            credentials.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            credentials.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            credentials.update,
        )
        self.list = to_streamed_response_wrapper(
            credentials.list,
        )
        self.delete = to_streamed_response_wrapper(
            credentials.delete,
        )
        self.decrypt = to_streamed_response_wrapper(
            credentials.decrypt,
        )
        self.decrypt_by_name = to_streamed_response_wrapper(
            credentials.decrypt_by_name,
        )
        self.retrieve_by_name = to_streamed_response_wrapper(
            credentials.retrieve_by_name,
        )


class AsyncCredentialsResourceWithStreamingResponse:
    def __init__(self, credentials: AsyncCredentialsResource) -> None:
        self._credentials = credentials

        self.create = async_to_streamed_response_wrapper(
            credentials.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            credentials.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            credentials.update,
        )
        self.list = async_to_streamed_response_wrapper(
            credentials.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            credentials.delete,
        )
        self.decrypt = async_to_streamed_response_wrapper(
            credentials.decrypt,
        )
        self.decrypt_by_name = async_to_streamed_response_wrapper(
            credentials.decrypt_by_name,
        )
        self.retrieve_by_name = async_to_streamed_response_wrapper(
            credentials.retrieve_by_name,
        )
