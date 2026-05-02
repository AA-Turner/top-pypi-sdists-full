# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import application_schema_retrieve_params
from .._types import Body, Query, Headers, NotGiven, not_given
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
from ..types.application_schema_retrieve_response import ApplicationSchemaRetrieveResponse

__all__ = ["ApplicationSchemasResource", "AsyncApplicationSchemasResource"]


class ApplicationSchemasResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ApplicationSchemasResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return ApplicationSchemasResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ApplicationSchemasResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return ApplicationSchemasResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        version: Literal["OFFLINE", "V0", "AGENTS_SERVICE"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationSchemaRetrieveResponse:
        """
        Get Application Schemas

        Args:
          version: An enum representing the version states of an application and its nodes'
              schemas. Attributes: V0: The initial version of an application schema.
              AGENTS_SERVICE: Application schema references egp_services definition. OFFLINE:
              Application schema for applications that do not run on SGP directly.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v4/application-schemas",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"version": version}, application_schema_retrieve_params.ApplicationSchemaRetrieveParams
                ),
            ),
            cast_to=ApplicationSchemaRetrieveResponse,
        )


class AsyncApplicationSchemasResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncApplicationSchemasResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncApplicationSchemasResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncApplicationSchemasResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncApplicationSchemasResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        version: Literal["OFFLINE", "V0", "AGENTS_SERVICE"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationSchemaRetrieveResponse:
        """
        Get Application Schemas

        Args:
          version: An enum representing the version states of an application and its nodes'
              schemas. Attributes: V0: The initial version of an application schema.
              AGENTS_SERVICE: Application schema references egp_services definition. OFFLINE:
              Application schema for applications that do not run on SGP directly.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v4/application-schemas",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"version": version}, application_schema_retrieve_params.ApplicationSchemaRetrieveParams
                ),
            ),
            cast_to=ApplicationSchemaRetrieveResponse,
        )


class ApplicationSchemasResourceWithRawResponse:
    def __init__(self, application_schemas: ApplicationSchemasResource) -> None:
        self._application_schemas = application_schemas

        self.retrieve = to_raw_response_wrapper(
            application_schemas.retrieve,
        )


class AsyncApplicationSchemasResourceWithRawResponse:
    def __init__(self, application_schemas: AsyncApplicationSchemasResource) -> None:
        self._application_schemas = application_schemas

        self.retrieve = async_to_raw_response_wrapper(
            application_schemas.retrieve,
        )


class ApplicationSchemasResourceWithStreamingResponse:
    def __init__(self, application_schemas: ApplicationSchemasResource) -> None:
        self._application_schemas = application_schemas

        self.retrieve = to_streamed_response_wrapper(
            application_schemas.retrieve,
        )


class AsyncApplicationSchemasResourceWithStreamingResponse:
    def __init__(self, application_schemas: AsyncApplicationSchemasResource) -> None:
        self._application_schemas = application_schemas

        self.retrieve = async_to_streamed_response_wrapper(
            application_schemas.retrieve,
        )
