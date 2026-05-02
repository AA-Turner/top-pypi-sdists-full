# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, overload

import httpx

from ..types import application_spec_list_params, application_spec_create_params, application_spec_update_params
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
from .._base_client import AsyncPaginator, make_request_options
from ..types.paginated_application_specs import Item
from ..types.shared.generic_delete_response import GenericDeleteResponse
from ..types.application_spec_create_response import ApplicationSpecCreateResponse
from ..types.application_spec_update_response import ApplicationSpecUpdateResponse
from ..types.application_spec_retrieve_response import ApplicationSpecRetrieveResponse

__all__ = ["ApplicationSpecsResource", "AsyncApplicationSpecsResource"]


class ApplicationSpecsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ApplicationSpecsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return ApplicationSpecsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ApplicationSpecsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return ApplicationSpecsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        description: str,
        name: str,
        run_online_evaluation: bool | Omit = omit,
        theme_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationSpecCreateResponse:
        """
        ### Description

        Creates a application spec

        ### Details

        This API can be used to create a application spec. To use this API, review the
        request schema and pass in all fields that are required to create a application
        spec.

        Args:
          account_id: The ID of the account that owns the given entity.

          description: The description of the Application Spec

          name: The name of the Application Spec

          run_online_evaluation: Whether the application spec should run online evaluation, default is `false`

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v4/application-specs",
            body=maybe_transform(
                {
                    "account_id": account_id,
                    "description": description,
                    "name": name,
                    "run_online_evaluation": run_online_evaluation,
                    "theme_id": theme_id,
                },
                application_spec_create_params.ApplicationSpecCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationSpecCreateResponse,
        )

    def retrieve(
        self,
        application_spec_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationSpecRetrieveResponse:
        """
        ### Description

        Gets the details of a application spec

        ### Details

        This API can be used to get information about a single application spec by ID.
        To use this API, pass in the `id` that was returned from your Create Application
        Spec API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_spec_id:
            raise ValueError(
                f"Expected a non-empty value for `application_spec_id` but received {application_spec_id!r}"
            )
        return self._get(
            f"/v4/application-specs/{application_spec_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationSpecRetrieveResponse,
        )

    @overload
    def update(
        self,
        application_spec_id: str,
        *,
        description: str | Omit = omit,
        name: str | Omit = omit,
        restore: Literal[False] | Omit = omit,
        run_online_evaluation: bool | Omit = omit,
        theme_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationSpecUpdateResponse:
        """
        ### Description

        Updates a application spec

        ### Details

        This API can be used to update the application spec that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Application Spec API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          description: The description of the Application Spec

          name: The name of the Application Spec

          restore: Set to true to restore the entity from the database.

          run_online_evaluation: Whether the application spec should run online evaluation, default is `false`

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def update(
        self,
        application_spec_id: str,
        *,
        restore: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationSpecUpdateResponse:
        """
        ### Description

        Updates a application spec

        ### Details

        This API can be used to update the application spec that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Application Spec API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          restore: Set to true to restore the entity from the database.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    def update(
        self,
        application_spec_id: str,
        *,
        description: str | Omit = omit,
        name: str | Omit = omit,
        restore: Literal[False] | Literal[True] | Omit = omit,
        run_online_evaluation: bool | Omit = omit,
        theme_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationSpecUpdateResponse:
        if not application_spec_id:
            raise ValueError(
                f"Expected a non-empty value for `application_spec_id` but received {application_spec_id!r}"
            )
        return self._patch(
            f"/v4/application-specs/{application_spec_id}",
            body=maybe_transform(
                {
                    "description": description,
                    "name": name,
                    "restore": restore,
                    "run_online_evaluation": run_online_evaluation,
                    "theme_id": theme_id,
                },
                application_spec_update_params.ApplicationSpecUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationSpecUpdateResponse,
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
    ) -> SyncPageResponse[Item]:
        """
        ### Description

        Lists all application specs accessible to the user.

        ### Details

        This API can be used to list application specs. If a user has access to multiple
        accounts, all application specs from all accounts the user is associated with
        will be returned.

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
            "/v4/application-specs",
            page=SyncPageResponse[Item],
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
                    application_spec_list_params.ApplicationSpecListParams,
                ),
            ),
            model=Item,
        )

    def delete(
        self,
        application_spec_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GenericDeleteResponse:
        """
        ### Description

        Deletes a application spec

        ### Details

        This API can be used to delete a application spec by ID. To use this API, pass
        in the `id` that was returned from your Create Application Spec API call as a
        path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_spec_id:
            raise ValueError(
                f"Expected a non-empty value for `application_spec_id` but received {application_spec_id!r}"
            )
        return self._delete(
            f"/v4/application-specs/{application_spec_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )


class AsyncApplicationSpecsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncApplicationSpecsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncApplicationSpecsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncApplicationSpecsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncApplicationSpecsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        description: str,
        name: str,
        run_online_evaluation: bool | Omit = omit,
        theme_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationSpecCreateResponse:
        """
        ### Description

        Creates a application spec

        ### Details

        This API can be used to create a application spec. To use this API, review the
        request schema and pass in all fields that are required to create a application
        spec.

        Args:
          account_id: The ID of the account that owns the given entity.

          description: The description of the Application Spec

          name: The name of the Application Spec

          run_online_evaluation: Whether the application spec should run online evaluation, default is `false`

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v4/application-specs",
            body=await async_maybe_transform(
                {
                    "account_id": account_id,
                    "description": description,
                    "name": name,
                    "run_online_evaluation": run_online_evaluation,
                    "theme_id": theme_id,
                },
                application_spec_create_params.ApplicationSpecCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationSpecCreateResponse,
        )

    async def retrieve(
        self,
        application_spec_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationSpecRetrieveResponse:
        """
        ### Description

        Gets the details of a application spec

        ### Details

        This API can be used to get information about a single application spec by ID.
        To use this API, pass in the `id` that was returned from your Create Application
        Spec API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_spec_id:
            raise ValueError(
                f"Expected a non-empty value for `application_spec_id` but received {application_spec_id!r}"
            )
        return await self._get(
            f"/v4/application-specs/{application_spec_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationSpecRetrieveResponse,
        )

    @overload
    async def update(
        self,
        application_spec_id: str,
        *,
        description: str | Omit = omit,
        name: str | Omit = omit,
        restore: Literal[False] | Omit = omit,
        run_online_evaluation: bool | Omit = omit,
        theme_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationSpecUpdateResponse:
        """
        ### Description

        Updates a application spec

        ### Details

        This API can be used to update the application spec that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Application Spec API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          description: The description of the Application Spec

          name: The name of the Application Spec

          restore: Set to true to restore the entity from the database.

          run_online_evaluation: Whether the application spec should run online evaluation, default is `false`

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def update(
        self,
        application_spec_id: str,
        *,
        restore: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationSpecUpdateResponse:
        """
        ### Description

        Updates a application spec

        ### Details

        This API can be used to update the application spec that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Application Spec API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          restore: Set to true to restore the entity from the database.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    async def update(
        self,
        application_spec_id: str,
        *,
        description: str | Omit = omit,
        name: str | Omit = omit,
        restore: Literal[False] | Literal[True] | Omit = omit,
        run_online_evaluation: bool | Omit = omit,
        theme_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationSpecUpdateResponse:
        if not application_spec_id:
            raise ValueError(
                f"Expected a non-empty value for `application_spec_id` but received {application_spec_id!r}"
            )
        return await self._patch(
            f"/v4/application-specs/{application_spec_id}",
            body=await async_maybe_transform(
                {
                    "description": description,
                    "name": name,
                    "restore": restore,
                    "run_online_evaluation": run_online_evaluation,
                    "theme_id": theme_id,
                },
                application_spec_update_params.ApplicationSpecUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationSpecUpdateResponse,
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
    ) -> AsyncPaginator[Item, AsyncPageResponse[Item]]:
        """
        ### Description

        Lists all application specs accessible to the user.

        ### Details

        This API can be used to list application specs. If a user has access to multiple
        accounts, all application specs from all accounts the user is associated with
        will be returned.

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
            "/v4/application-specs",
            page=AsyncPageResponse[Item],
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
                    application_spec_list_params.ApplicationSpecListParams,
                ),
            ),
            model=Item,
        )

    async def delete(
        self,
        application_spec_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GenericDeleteResponse:
        """
        ### Description

        Deletes a application spec

        ### Details

        This API can be used to delete a application spec by ID. To use this API, pass
        in the `id` that was returned from your Create Application Spec API call as a
        path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_spec_id:
            raise ValueError(
                f"Expected a non-empty value for `application_spec_id` but received {application_spec_id!r}"
            )
        return await self._delete(
            f"/v4/application-specs/{application_spec_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )


class ApplicationSpecsResourceWithRawResponse:
    def __init__(self, application_specs: ApplicationSpecsResource) -> None:
        self._application_specs = application_specs

        self.create = to_raw_response_wrapper(
            application_specs.create,
        )
        self.retrieve = to_raw_response_wrapper(
            application_specs.retrieve,
        )
        self.update = to_raw_response_wrapper(
            application_specs.update,
        )
        self.list = to_raw_response_wrapper(
            application_specs.list,
        )
        self.delete = to_raw_response_wrapper(
            application_specs.delete,
        )


class AsyncApplicationSpecsResourceWithRawResponse:
    def __init__(self, application_specs: AsyncApplicationSpecsResource) -> None:
        self._application_specs = application_specs

        self.create = async_to_raw_response_wrapper(
            application_specs.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            application_specs.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            application_specs.update,
        )
        self.list = async_to_raw_response_wrapper(
            application_specs.list,
        )
        self.delete = async_to_raw_response_wrapper(
            application_specs.delete,
        )


class ApplicationSpecsResourceWithStreamingResponse:
    def __init__(self, application_specs: ApplicationSpecsResource) -> None:
        self._application_specs = application_specs

        self.create = to_streamed_response_wrapper(
            application_specs.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            application_specs.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            application_specs.update,
        )
        self.list = to_streamed_response_wrapper(
            application_specs.list,
        )
        self.delete = to_streamed_response_wrapper(
            application_specs.delete,
        )


class AsyncApplicationSpecsResourceWithStreamingResponse:
    def __init__(self, application_specs: AsyncApplicationSpecsResource) -> None:
        self._application_specs = application_specs

        self.create = async_to_streamed_response_wrapper(
            application_specs.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            application_specs.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            application_specs.update,
        )
        self.list = async_to_streamed_response_wrapper(
            application_specs.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            application_specs.delete,
        )
