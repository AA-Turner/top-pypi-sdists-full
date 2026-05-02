# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import studio_project_list_params, studio_project_create_params, studio_project_update_params
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
from ..types.studio_project import StudioProject
from ..types.shared.generic_delete_response import GenericDeleteResponse

__all__ = ["StudioProjectsResource", "AsyncStudioProjectsResource"]


class StudioProjectsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> StudioProjectsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return StudioProjectsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> StudioProjectsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return StudioProjectsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        description: str,
        name: str,
        studio_api_key: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StudioProject:
        """
        ### Description

        Creates a studio project

        ### Details

        This API can be used to create a studio project. To use this API, review the
        request schema and pass in all fields that are required to create a studio
        project.

        Args:
          account_id: The ID of the account that owns the given entity.

          description: The description of the Studio Project

          name: The name of the Studio Project

          studio_api_key: Your API key for Studio, can be updated with the PATCH endpoint

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v4/studio-projects",
            body=maybe_transform(
                {
                    "account_id": account_id,
                    "description": description,
                    "name": name,
                    "studio_api_key": studio_api_key,
                },
                studio_project_create_params.StudioProjectCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StudioProject,
        )

    def retrieve(
        self,
        studio_project_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StudioProject:
        """
        ### Description

        Gets the details of a studio project

        ### Details

        This API can be used to get information about a single studio project by ID. To
        use this API, pass in the `id` that was returned from your Create Studio Project
        API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not studio_project_id:
            raise ValueError(f"Expected a non-empty value for `studio_project_id` but received {studio_project_id!r}")
        return self._get(
            f"/v4/studio-projects/{studio_project_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StudioProject,
        )

    def update(
        self,
        studio_project_id: str,
        *,
        description: str | Omit = omit,
        name: str | Omit = omit,
        studio_api_key: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StudioProject:
        """
        ### Description

        Updates a studio project

        ### Details

        This API can be used to update the studio project that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Studio Project API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          description: The description of the Studio Project

          name: The name of the Studio Project

          studio_api_key: Your API key for Studio, can be updated with the PATCH endpoint

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not studio_project_id:
            raise ValueError(f"Expected a non-empty value for `studio_project_id` but received {studio_project_id!r}")
        return self._patch(
            f"/v4/studio-projects/{studio_project_id}",
            body=maybe_transform(
                {
                    "description": description,
                    "name": name,
                    "studio_api_key": studio_api_key,
                },
                studio_project_update_params.StudioProjectUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StudioProject,
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageResponse[StudioProject]:
        """
        ### Description

        Lists all studio projects accessible to the user.

        ### Details

        This API can be used to list studio projects. If a user has access to multiple
        accounts, all studio projects from all accounts the user is associated with will
        be returned.

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
            "/v4/studio-projects",
            page=SyncPageResponse[StudioProject],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "limit": limit,
                        "page": page,
                    },
                    studio_project_list_params.StudioProjectListParams,
                ),
            ),
            model=StudioProject,
        )

    def delete(
        self,
        studio_project_id: str,
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

        Deletes a studio project

        ### Details

        This API can be used to delete a studio project by ID. To use this API, pass in
        the `id` that was returned from your Create Studio Project API call as a path
        parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not studio_project_id:
            raise ValueError(f"Expected a non-empty value for `studio_project_id` but received {studio_project_id!r}")
        return self._delete(
            f"/v4/studio-projects/{studio_project_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )


class AsyncStudioProjectsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncStudioProjectsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncStudioProjectsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncStudioProjectsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncStudioProjectsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        description: str,
        name: str,
        studio_api_key: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StudioProject:
        """
        ### Description

        Creates a studio project

        ### Details

        This API can be used to create a studio project. To use this API, review the
        request schema and pass in all fields that are required to create a studio
        project.

        Args:
          account_id: The ID of the account that owns the given entity.

          description: The description of the Studio Project

          name: The name of the Studio Project

          studio_api_key: Your API key for Studio, can be updated with the PATCH endpoint

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v4/studio-projects",
            body=await async_maybe_transform(
                {
                    "account_id": account_id,
                    "description": description,
                    "name": name,
                    "studio_api_key": studio_api_key,
                },
                studio_project_create_params.StudioProjectCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StudioProject,
        )

    async def retrieve(
        self,
        studio_project_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StudioProject:
        """
        ### Description

        Gets the details of a studio project

        ### Details

        This API can be used to get information about a single studio project by ID. To
        use this API, pass in the `id` that was returned from your Create Studio Project
        API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not studio_project_id:
            raise ValueError(f"Expected a non-empty value for `studio_project_id` but received {studio_project_id!r}")
        return await self._get(
            f"/v4/studio-projects/{studio_project_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StudioProject,
        )

    async def update(
        self,
        studio_project_id: str,
        *,
        description: str | Omit = omit,
        name: str | Omit = omit,
        studio_api_key: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StudioProject:
        """
        ### Description

        Updates a studio project

        ### Details

        This API can be used to update the studio project that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Studio Project API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          description: The description of the Studio Project

          name: The name of the Studio Project

          studio_api_key: Your API key for Studio, can be updated with the PATCH endpoint

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not studio_project_id:
            raise ValueError(f"Expected a non-empty value for `studio_project_id` but received {studio_project_id!r}")
        return await self._patch(
            f"/v4/studio-projects/{studio_project_id}",
            body=await async_maybe_transform(
                {
                    "description": description,
                    "name": name,
                    "studio_api_key": studio_api_key,
                },
                studio_project_update_params.StudioProjectUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StudioProject,
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[StudioProject, AsyncPageResponse[StudioProject]]:
        """
        ### Description

        Lists all studio projects accessible to the user.

        ### Details

        This API can be used to list studio projects. If a user has access to multiple
        accounts, all studio projects from all accounts the user is associated with will
        be returned.

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
            "/v4/studio-projects",
            page=AsyncPageResponse[StudioProject],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "limit": limit,
                        "page": page,
                    },
                    studio_project_list_params.StudioProjectListParams,
                ),
            ),
            model=StudioProject,
        )

    async def delete(
        self,
        studio_project_id: str,
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

        Deletes a studio project

        ### Details

        This API can be used to delete a studio project by ID. To use this API, pass in
        the `id` that was returned from your Create Studio Project API call as a path
        parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not studio_project_id:
            raise ValueError(f"Expected a non-empty value for `studio_project_id` but received {studio_project_id!r}")
        return await self._delete(
            f"/v4/studio-projects/{studio_project_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )


class StudioProjectsResourceWithRawResponse:
    def __init__(self, studio_projects: StudioProjectsResource) -> None:
        self._studio_projects = studio_projects

        self.create = to_raw_response_wrapper(
            studio_projects.create,
        )
        self.retrieve = to_raw_response_wrapper(
            studio_projects.retrieve,
        )
        self.update = to_raw_response_wrapper(
            studio_projects.update,
        )
        self.list = to_raw_response_wrapper(
            studio_projects.list,
        )
        self.delete = to_raw_response_wrapper(
            studio_projects.delete,
        )


class AsyncStudioProjectsResourceWithRawResponse:
    def __init__(self, studio_projects: AsyncStudioProjectsResource) -> None:
        self._studio_projects = studio_projects

        self.create = async_to_raw_response_wrapper(
            studio_projects.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            studio_projects.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            studio_projects.update,
        )
        self.list = async_to_raw_response_wrapper(
            studio_projects.list,
        )
        self.delete = async_to_raw_response_wrapper(
            studio_projects.delete,
        )


class StudioProjectsResourceWithStreamingResponse:
    def __init__(self, studio_projects: StudioProjectsResource) -> None:
        self._studio_projects = studio_projects

        self.create = to_streamed_response_wrapper(
            studio_projects.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            studio_projects.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            studio_projects.update,
        )
        self.list = to_streamed_response_wrapper(
            studio_projects.list,
        )
        self.delete = to_streamed_response_wrapper(
            studio_projects.delete,
        )


class AsyncStudioProjectsResourceWithStreamingResponse:
    def __init__(self, studio_projects: AsyncStudioProjectsResource) -> None:
        self._studio_projects = studio_projects

        self.create = async_to_streamed_response_wrapper(
            studio_projects.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            studio_projects.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            studio_projects.update,
        )
        self.list = async_to_streamed_response_wrapper(
            studio_projects.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            studio_projects.delete,
        )
