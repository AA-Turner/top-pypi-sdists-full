# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

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
from ..._base_client import make_request_options
from ...types.sessions import credential_attach_params, credential_replace_params, credential_detach_binding_params
from ...types.session_credentials import SessionCredentials

__all__ = ["CredentialsResource", "AsyncCredentialsResource"]


class CredentialsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CredentialsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#accessing-raw-response-data-eg-headers
        """
        return CredentialsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CredentialsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#with_streaming_response
        """
        return CredentialsResourceWithStreamingResponse(self)

    def list(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionCredentials:
        """The session's credential lookup and the live credentials bound to it (no
        values).

        Subject to session organization and project access.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/v1/sessions/{id}/credentials", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionCredentials,
        )

    def attach(
        self,
        id: str,
        *,
        bindings: SequenceNotStr[credential_attach_params.Binding] | Omit = omit,
        credential_ids: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionCredentials:
        """Attach credentialIds and/or Vault or item references in bindings.

        Each array
        accepts at most 100 entries; at most 100 distinct direct items and whole Vaults
        may be bound. Only credentials can be autofilled. Lookup becomes explicit and
        remains so. Errors: 400 `invalid_reference`, `reference_not_found`,
        `reference_ambiguous`, `reference_not_supported`, `credential_not_bindable`, or
        `too_many_credentials`; 409 `credentials_not_enabled` or `session_not_running`;
        503 `credential_bindings_busy` (retryable).

        Args:
          bindings: At most 100 bindings; KV bindings may specify allowedOrigins.

          credential_ids: Ids of credentials (Secrets of kind `credential`) in the session's project.
              Binding makes the session's lookup `explicit` for good.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/v1/sessions/{id}/credentials", id=id),
            body=maybe_transform(
                {
                    "bindings": bindings,
                    "credential_ids": credential_ids,
                },
                credential_attach_params.CredentialAttachParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionCredentials,
        )

    def detach(
        self,
        credential_id: str,
        *,
        id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionCredentials:
        """Unbind a credential from a running session.

        The lookup stays `explicit`: with
        nothing bound, the session fills nothing. Errors: 404 `credential_not_attached`,
        409 `session_not_running`, 503 `credential_bindings_busy` (retryable).

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return self._delete(
            path_template("/v1/sessions/{id}/credentials/{credential_id}", id=id, credential_id=credential_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionCredentials,
        )

    def detach_binding(
        self,
        id: str,
        *,
        reference: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionCredentials:
        """
        Pass reference as a query parameter to detach one Vault or item binding,
        including steel://connections/<connection>/vaults/<vault>[/<item>]. Does not
        detach items covered by a whole Vault binding. Errors: 400 `invalid_reference`
        or `reference_ambiguous`; 404 `credential_not_attached`; 409
        `session_not_running`; 503 `credential_bindings_busy` (retryable).

        Args:
          reference: Vault or item reference to detach

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._delete(
            path_template("/v1/sessions/{id}/credentials/bindings", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"reference": reference}, credential_detach_binding_params.CredentialDetachBindingParams
                ),
            ),
            cast_to=SessionCredentials,
        )

    def replace(
        self,
        id: str,
        *,
        bindings: SequenceNotStr[credential_replace_params.Binding] | Omit = omit,
        credential_ids: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionCredentials:
        """
        Replace all direct item and Vault bindings, including provider references
        steel://connections/<connection>/vaults/<vault>[/<item>]. Supply credentialIds
        and/or bindings; empty arrays detach all. At most 100 distinct bindings may be
        stored. Only credentials can be autofilled. Lookup becomes explicit and remains
        so.

        Args:
          bindings: At most 100 bindings; KV bindings may specify allowedOrigins.

          credential_ids: Ids of credentials (Secrets of kind `credential`) in the session's project.
              Binding makes the session's lookup `explicit` for good.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._put(
            path_template("/v1/sessions/{id}/credentials", id=id),
            body=maybe_transform(
                {
                    "bindings": bindings,
                    "credential_ids": credential_ids,
                },
                credential_replace_params.CredentialReplaceParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionCredentials,
        )


class AsyncCredentialsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCredentialsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#accessing-raw-response-data-eg-headers
        """
        return AsyncCredentialsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCredentialsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#with_streaming_response
        """
        return AsyncCredentialsResourceWithStreamingResponse(self)

    async def list(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionCredentials:
        """The session's credential lookup and the live credentials bound to it (no
        values).

        Subject to session organization and project access.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/v1/sessions/{id}/credentials", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionCredentials,
        )

    async def attach(
        self,
        id: str,
        *,
        bindings: SequenceNotStr[credential_attach_params.Binding] | Omit = omit,
        credential_ids: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionCredentials:
        """Attach credentialIds and/or Vault or item references in bindings.

        Each array
        accepts at most 100 entries; at most 100 distinct direct items and whole Vaults
        may be bound. Only credentials can be autofilled. Lookup becomes explicit and
        remains so. Errors: 400 `invalid_reference`, `reference_not_found`,
        `reference_ambiguous`, `reference_not_supported`, `credential_not_bindable`, or
        `too_many_credentials`; 409 `credentials_not_enabled` or `session_not_running`;
        503 `credential_bindings_busy` (retryable).

        Args:
          bindings: At most 100 bindings; KV bindings may specify allowedOrigins.

          credential_ids: Ids of credentials (Secrets of kind `credential`) in the session's project.
              Binding makes the session's lookup `explicit` for good.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/v1/sessions/{id}/credentials", id=id),
            body=await async_maybe_transform(
                {
                    "bindings": bindings,
                    "credential_ids": credential_ids,
                },
                credential_attach_params.CredentialAttachParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionCredentials,
        )

    async def detach(
        self,
        credential_id: str,
        *,
        id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionCredentials:
        """Unbind a credential from a running session.

        The lookup stays `explicit`: with
        nothing bound, the session fills nothing. Errors: 404 `credential_not_attached`,
        409 `session_not_running`, 503 `credential_bindings_busy` (retryable).

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return await self._delete(
            path_template("/v1/sessions/{id}/credentials/{credential_id}", id=id, credential_id=credential_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionCredentials,
        )

    async def detach_binding(
        self,
        id: str,
        *,
        reference: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionCredentials:
        """
        Pass reference as a query parameter to detach one Vault or item binding,
        including steel://connections/<connection>/vaults/<vault>[/<item>]. Does not
        detach items covered by a whole Vault binding. Errors: 400 `invalid_reference`
        or `reference_ambiguous`; 404 `credential_not_attached`; 409
        `session_not_running`; 503 `credential_bindings_busy` (retryable).

        Args:
          reference: Vault or item reference to detach

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._delete(
            path_template("/v1/sessions/{id}/credentials/bindings", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"reference": reference}, credential_detach_binding_params.CredentialDetachBindingParams
                ),
            ),
            cast_to=SessionCredentials,
        )

    async def replace(
        self,
        id: str,
        *,
        bindings: SequenceNotStr[credential_replace_params.Binding] | Omit = omit,
        credential_ids: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionCredentials:
        """
        Replace all direct item and Vault bindings, including provider references
        steel://connections/<connection>/vaults/<vault>[/<item>]. Supply credentialIds
        and/or bindings; empty arrays detach all. At most 100 distinct bindings may be
        stored. Only credentials can be autofilled. Lookup becomes explicit and remains
        so.

        Args:
          bindings: At most 100 bindings; KV bindings may specify allowedOrigins.

          credential_ids: Ids of credentials (Secrets of kind `credential`) in the session's project.
              Binding makes the session's lookup `explicit` for good.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._put(
            path_template("/v1/sessions/{id}/credentials", id=id),
            body=await async_maybe_transform(
                {
                    "bindings": bindings,
                    "credential_ids": credential_ids,
                },
                credential_replace_params.CredentialReplaceParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionCredentials,
        )


class CredentialsResourceWithRawResponse:
    def __init__(self, credentials: CredentialsResource) -> None:
        self._credentials = credentials

        self.list = to_raw_response_wrapper(
            credentials.list,
        )
        self.attach = to_raw_response_wrapper(
            credentials.attach,
        )
        self.detach = to_raw_response_wrapper(
            credentials.detach,
        )
        self.detach_binding = to_raw_response_wrapper(
            credentials.detach_binding,
        )
        self.replace = to_raw_response_wrapper(
            credentials.replace,
        )


class AsyncCredentialsResourceWithRawResponse:
    def __init__(self, credentials: AsyncCredentialsResource) -> None:
        self._credentials = credentials

        self.list = async_to_raw_response_wrapper(
            credentials.list,
        )
        self.attach = async_to_raw_response_wrapper(
            credentials.attach,
        )
        self.detach = async_to_raw_response_wrapper(
            credentials.detach,
        )
        self.detach_binding = async_to_raw_response_wrapper(
            credentials.detach_binding,
        )
        self.replace = async_to_raw_response_wrapper(
            credentials.replace,
        )


class CredentialsResourceWithStreamingResponse:
    def __init__(self, credentials: CredentialsResource) -> None:
        self._credentials = credentials

        self.list = to_streamed_response_wrapper(
            credentials.list,
        )
        self.attach = to_streamed_response_wrapper(
            credentials.attach,
        )
        self.detach = to_streamed_response_wrapper(
            credentials.detach,
        )
        self.detach_binding = to_streamed_response_wrapper(
            credentials.detach_binding,
        )
        self.replace = to_streamed_response_wrapper(
            credentials.replace,
        )


class AsyncCredentialsResourceWithStreamingResponse:
    def __init__(self, credentials: AsyncCredentialsResource) -> None:
        self._credentials = credentials

        self.list = async_to_streamed_response_wrapper(
            credentials.list,
        )
        self.attach = async_to_streamed_response_wrapper(
            credentials.attach,
        )
        self.detach = async_to_streamed_response_wrapper(
            credentials.detach,
        )
        self.detach_binding = async_to_streamed_response_wrapper(
            credentials.detach_binding,
        )
        self.replace = async_to_streamed_response_wrapper(
            credentials.replace,
        )
