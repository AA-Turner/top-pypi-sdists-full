# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Type, Iterable, Optional, cast

import httpx

from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._wrappers import ResultWrapper
from ..._base_client import make_request_options
from ...types.field_extractors import field_extractor_update_params
from ...types.field_extractors.field_extractor_get_response import FieldExtractorGetResponse
from ...types.field_extractors.field_extractor_update_response import FieldExtractorUpdateResponse

__all__ = ["FieldExtractorsResource", "AsyncFieldExtractorsResource"]


class FieldExtractorsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FieldExtractorsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return FieldExtractorsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FieldExtractorsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return FieldExtractorsResourceWithStreamingResponse(self)

    def update(
        self,
        extractor: str,
        *,
        account_id: str,
        rules: Iterable[field_extractor_update_params.Rule],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FieldExtractorUpdateResponse:
        """Replaces all custom extraction rules for an extractor type.

        Omitted rules are
        deleted.

        Args:
          account_id: Cloudflare account ID.

          extractor: Extractor type.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not extractor:
            raise ValueError(f"Expected a non-empty value for `extractor` but received {extractor!r}")
        return self._put(
            path_template(
                "/accounts/{account_id}/field_extractors/{extractor}", account_id=account_id, extractor=extractor
            ),
            body=maybe_transform({"rules": rules}, field_extractor_update_params.FieldExtractorUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[FieldExtractorUpdateResponse]._unwrapper,
            ),
            cast_to=cast(Type[FieldExtractorUpdateResponse], ResultWrapper[FieldExtractorUpdateResponse]),
        )

    def delete(
        self,
        extractor: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Deletes all custom extraction rules for an extractor type.

        Args:
          account_id: Cloudflare account ID.

          extractor: Extractor type.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not extractor:
            raise ValueError(f"Expected a non-empty value for `extractor` but received {extractor!r}")
        return self._delete(
            path_template(
                "/accounts/{account_id}/field_extractors/{extractor}", account_id=account_id, extractor=extractor
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[Optional[object]]._unwrapper,
            ),
            cast_to=cast(Type[object], ResultWrapper[object]),
        )

    def get(
        self,
        extractor: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FieldExtractorGetResponse:
        """
        Retrieves the custom extraction rules configured for a given extractor type.

        Args:
          account_id: Cloudflare account ID.

          extractor: Extractor type.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not extractor:
            raise ValueError(f"Expected a non-empty value for `extractor` but received {extractor!r}")
        return self._get(
            path_template(
                "/accounts/{account_id}/field_extractors/{extractor}", account_id=account_id, extractor=extractor
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[FieldExtractorGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[FieldExtractorGetResponse], ResultWrapper[FieldExtractorGetResponse]),
        )


class AsyncFieldExtractorsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFieldExtractorsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncFieldExtractorsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFieldExtractorsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncFieldExtractorsResourceWithStreamingResponse(self)

    async def update(
        self,
        extractor: str,
        *,
        account_id: str,
        rules: Iterable[field_extractor_update_params.Rule],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FieldExtractorUpdateResponse:
        """Replaces all custom extraction rules for an extractor type.

        Omitted rules are
        deleted.

        Args:
          account_id: Cloudflare account ID.

          extractor: Extractor type.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not extractor:
            raise ValueError(f"Expected a non-empty value for `extractor` but received {extractor!r}")
        return await self._put(
            path_template(
                "/accounts/{account_id}/field_extractors/{extractor}", account_id=account_id, extractor=extractor
            ),
            body=await async_maybe_transform(
                {"rules": rules}, field_extractor_update_params.FieldExtractorUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[FieldExtractorUpdateResponse]._unwrapper,
            ),
            cast_to=cast(Type[FieldExtractorUpdateResponse], ResultWrapper[FieldExtractorUpdateResponse]),
        )

    async def delete(
        self,
        extractor: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Deletes all custom extraction rules for an extractor type.

        Args:
          account_id: Cloudflare account ID.

          extractor: Extractor type.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not extractor:
            raise ValueError(f"Expected a non-empty value for `extractor` but received {extractor!r}")
        return await self._delete(
            path_template(
                "/accounts/{account_id}/field_extractors/{extractor}", account_id=account_id, extractor=extractor
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[Optional[object]]._unwrapper,
            ),
            cast_to=cast(Type[object], ResultWrapper[object]),
        )

    async def get(
        self,
        extractor: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FieldExtractorGetResponse:
        """
        Retrieves the custom extraction rules configured for a given extractor type.

        Args:
          account_id: Cloudflare account ID.

          extractor: Extractor type.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not extractor:
            raise ValueError(f"Expected a non-empty value for `extractor` but received {extractor!r}")
        return await self._get(
            path_template(
                "/accounts/{account_id}/field_extractors/{extractor}", account_id=account_id, extractor=extractor
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[FieldExtractorGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[FieldExtractorGetResponse], ResultWrapper[FieldExtractorGetResponse]),
        )


class FieldExtractorsResourceWithRawResponse:
    def __init__(self, field_extractors: FieldExtractorsResource) -> None:
        self._field_extractors = field_extractors

        self.update = to_raw_response_wrapper(
            field_extractors.update,
        )
        self.delete = to_raw_response_wrapper(
            field_extractors.delete,
        )
        self.get = to_raw_response_wrapper(
            field_extractors.get,
        )


class AsyncFieldExtractorsResourceWithRawResponse:
    def __init__(self, field_extractors: AsyncFieldExtractorsResource) -> None:
        self._field_extractors = field_extractors

        self.update = async_to_raw_response_wrapper(
            field_extractors.update,
        )
        self.delete = async_to_raw_response_wrapper(
            field_extractors.delete,
        )
        self.get = async_to_raw_response_wrapper(
            field_extractors.get,
        )


class FieldExtractorsResourceWithStreamingResponse:
    def __init__(self, field_extractors: FieldExtractorsResource) -> None:
        self._field_extractors = field_extractors

        self.update = to_streamed_response_wrapper(
            field_extractors.update,
        )
        self.delete = to_streamed_response_wrapper(
            field_extractors.delete,
        )
        self.get = to_streamed_response_wrapper(
            field_extractors.get,
        )


class AsyncFieldExtractorsResourceWithStreamingResponse:
    def __init__(self, field_extractors: AsyncFieldExtractorsResource) -> None:
        self._field_extractors = field_extractors

        self.update = async_to_streamed_response_wrapper(
            field_extractors.update,
        )
        self.delete = async_to_streamed_response_wrapper(
            field_extractors.delete,
        )
        self.get = async_to_streamed_response_wrapper(
            field_extractors.get,
        )
