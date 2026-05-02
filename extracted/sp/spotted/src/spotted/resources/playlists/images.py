# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os

import httpx

from ..._files import read_file_content, async_read_file_content
from ..._types import (
    Body,
    Query,
    Headers,
    NotGiven,
    BinaryTypes,
    FileContent,
    AsyncBinaryTypes,
    not_given,
)
from ..._utils import path_template
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    to_custom_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.playlists.image_list_response import ImageListResponse

__all__ = ["ImagesResource", "AsyncImagesResource"]


class ImagesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ImagesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return ImagesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ImagesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return ImagesResourceWithStreamingResponse(self)

    def update(
        self,
        playlist_id: str,
        body: FileContent | BinaryTypes,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BinaryAPIResponse:
        """
        Replace the image used to represent a specific playlist.

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

          body: Base64 encoded JPEG image data, maximum payload size is 256 KB.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        extra_headers = {"Accept": "application/binary", **(extra_headers or {})}
        extra_headers = {"Content-Type": "image/jpeg", **(extra_headers or {})}
        return self._put(
            path_template("/playlists/{playlist_id}/images", playlist_id=playlist_id),
            content=read_file_content(body) if isinstance(body, os.PathLike) else body,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def list(
        self,
        playlist_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ImageListResponse:
        """
        Get the current image associated with a specific playlist.

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        return self._get(
            path_template("/playlists/{playlist_id}/images", playlist_id=playlist_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ImageListResponse,
        )


class AsyncImagesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncImagesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncImagesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncImagesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncImagesResourceWithStreamingResponse(self)

    async def update(
        self,
        playlist_id: str,
        body: FileContent | AsyncBinaryTypes,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncBinaryAPIResponse:
        """
        Replace the image used to represent a specific playlist.

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

          body: Base64 encoded JPEG image data, maximum payload size is 256 KB.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        extra_headers = {"Accept": "application/binary", **(extra_headers or {})}
        extra_headers = {"Content-Type": "image/jpeg", **(extra_headers or {})}
        return await self._put(
            path_template("/playlists/{playlist_id}/images", playlist_id=playlist_id),
            content=await async_read_file_content(body) if isinstance(body, os.PathLike) else body,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def list(
        self,
        playlist_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ImageListResponse:
        """
        Get the current image associated with a specific playlist.

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        return await self._get(
            path_template("/playlists/{playlist_id}/images", playlist_id=playlist_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ImageListResponse,
        )


class ImagesResourceWithRawResponse:
    def __init__(self, images: ImagesResource) -> None:
        self._images = images

        self.update = to_custom_raw_response_wrapper(
            images.update,
            BinaryAPIResponse,
        )
        self.list = to_raw_response_wrapper(
            images.list,
        )


class AsyncImagesResourceWithRawResponse:
    def __init__(self, images: AsyncImagesResource) -> None:
        self._images = images

        self.update = async_to_custom_raw_response_wrapper(
            images.update,
            AsyncBinaryAPIResponse,
        )
        self.list = async_to_raw_response_wrapper(
            images.list,
        )


class ImagesResourceWithStreamingResponse:
    def __init__(self, images: ImagesResource) -> None:
        self._images = images

        self.update = to_custom_streamed_response_wrapper(
            images.update,
            StreamedBinaryAPIResponse,
        )
        self.list = to_streamed_response_wrapper(
            images.list,
        )


class AsyncImagesResourceWithStreamingResponse:
    def __init__(self, images: AsyncImagesResource) -> None:
        self._images = images

        self.update = async_to_custom_streamed_response_wrapper(
            images.update,
            AsyncStreamedBinaryAPIResponse,
        )
        self.list = async_to_streamed_response_wrapper(
            images.list,
        )
