# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import theme_list_params, theme_create_params
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
from ..pagination import SyncPageResponse, AsyncPageResponse
from ..types.theme import Theme
from .._base_client import AsyncPaginator, make_request_options

__all__ = ["ThemesResource", "AsyncThemesResource"]


class ThemesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ThemesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return ThemesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ThemesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return ThemesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        logo_blob: str,
        theme_vars: theme_create_params.ThemeVars,
        title: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Theme:
        """
        ### Description

        Custom chat themes

        Args:
          account_id: The ID of the account that owns the given entity.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v4/themes",
            body=maybe_transform(
                {
                    "account_id": account_id,
                    "logo_blob": logo_blob,
                    "theme_vars": theme_vars,
                    "title": title,
                },
                theme_create_params.ThemeCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Theme,
        )

    def retrieve(
        self,
        theme_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Theme:
        """
        ### Description

        Gets the details of a theme

        ### Details

        This API can be used to get information about a single theme by ID. To use this
        API, pass in the `id` that was returned from your Create Theme API call as a
        path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not theme_id:
            raise ValueError(f"Expected a non-empty value for `theme_id` but received {theme_id!r}")
        return self._get(
            f"/v4/themes/{theme_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Theme,
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageResponse[Theme]:
        """
        ### Description

        Lists all themes accessible to the user.

        ### Details

        This API can be used to list themes. If a user has access to multiple accounts,
        all themes from all accounts the user is associated with will be returned.

        Args:
          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v4/themes",
            page=SyncPageResponse[Theme],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "include_archived": include_archived,
                        "limit": limit,
                        "page": page,
                    },
                    theme_list_params.ThemeListParams,
                ),
            ),
            model=Theme,
        )


class AsyncThemesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncThemesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncThemesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncThemesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncThemesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        logo_blob: str,
        theme_vars: theme_create_params.ThemeVars,
        title: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Theme:
        """
        ### Description

        Custom chat themes

        Args:
          account_id: The ID of the account that owns the given entity.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v4/themes",
            body=await async_maybe_transform(
                {
                    "account_id": account_id,
                    "logo_blob": logo_blob,
                    "theme_vars": theme_vars,
                    "title": title,
                },
                theme_create_params.ThemeCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Theme,
        )

    async def retrieve(
        self,
        theme_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Theme:
        """
        ### Description

        Gets the details of a theme

        ### Details

        This API can be used to get information about a single theme by ID. To use this
        API, pass in the `id` that was returned from your Create Theme API call as a
        path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not theme_id:
            raise ValueError(f"Expected a non-empty value for `theme_id` but received {theme_id!r}")
        return await self._get(
            f"/v4/themes/{theme_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Theme,
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Theme, AsyncPageResponse[Theme]]:
        """
        ### Description

        Lists all themes accessible to the user.

        ### Details

        This API can be used to list themes. If a user has access to multiple accounts,
        all themes from all accounts the user is associated with will be returned.

        Args:
          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v4/themes",
            page=AsyncPageResponse[Theme],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "include_archived": include_archived,
                        "limit": limit,
                        "page": page,
                    },
                    theme_list_params.ThemeListParams,
                ),
            ),
            model=Theme,
        )


class ThemesResourceWithRawResponse:
    def __init__(self, themes: ThemesResource) -> None:
        self._themes = themes

        self.create = to_raw_response_wrapper(
            themes.create,
        )
        self.retrieve = to_raw_response_wrapper(
            themes.retrieve,
        )
        self.list = to_raw_response_wrapper(
            themes.list,
        )


class AsyncThemesResourceWithRawResponse:
    def __init__(self, themes: AsyncThemesResource) -> None:
        self._themes = themes

        self.create = async_to_raw_response_wrapper(
            themes.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            themes.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            themes.list,
        )


class ThemesResourceWithStreamingResponse:
    def __init__(self, themes: ThemesResource) -> None:
        self._themes = themes

        self.create = to_streamed_response_wrapper(
            themes.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            themes.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            themes.list,
        )


class AsyncThemesResourceWithStreamingResponse:
    def __init__(self, themes: AsyncThemesResource) -> None:
        self._themes = themes

        self.create = async_to_streamed_response_wrapper(
            themes.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            themes.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            themes.list,
        )
