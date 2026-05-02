# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .models import (
    ModelsResource,
    AsyncModelsResource,
    ModelsResourceWithRawResponse,
    AsyncModelsResourceWithRawResponse,
    ModelsResourceWithStreamingResponse,
    AsyncModelsResourceWithStreamingResponse,
)
from ...types import model_group_list_params, model_group_create_params, model_group_update_params
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncPageResponse, AsyncPageResponse
from ..._base_client import AsyncPaginator, make_request_options
from .usage_statistics import (
    UsageStatisticsResource,
    AsyncUsageStatisticsResource,
    UsageStatisticsResourceWithRawResponse,
    AsyncUsageStatisticsResourceWithRawResponse,
    UsageStatisticsResourceWithStreamingResponse,
    AsyncUsageStatisticsResourceWithStreamingResponse,
)
from ...types.model_group import ModelGroup
from ...types.shared.generic_delete_response import GenericDeleteResponse

__all__ = ["ModelGroupsResource", "AsyncModelGroupsResource"]


class ModelGroupsResource(SyncAPIResource):
    @cached_property
    def models(self) -> ModelsResource:
        return ModelsResource(self._client)

    @cached_property
    def usage_statistics(self) -> UsageStatisticsResource:
        return UsageStatisticsResource(self._client)

    @cached_property
    def with_raw_response(self) -> ModelGroupsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return ModelGroupsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ModelGroupsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return ModelGroupsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        name: str,
        description: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelGroup:
        """### Description

        Model groups are grouping models together.

        You can add models with the same
        base_model_id.

        Args:
          account_id: The ID of the account that owns the given entity.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v4/model-groups",
            body=maybe_transform(
                {
                    "account_id": account_id,
                    "name": name,
                    "description": description,
                },
                model_group_create_params.ModelGroupCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelGroup,
        )

    def retrieve(
        self,
        model_group_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelGroup:
        """
        ### Description

        Gets the details of a model group

        ### Details

        This API can be used to get information about a single model group by ID. To use
        this API, pass in the `id` that was returned from your Create Model Group API
        call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_group_id:
            raise ValueError(f"Expected a non-empty value for `model_group_id` but received {model_group_id!r}")
        return self._get(
            f"/v4/model-groups/{model_group_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelGroup,
        )

    def update(
        self,
        model_group_id: str,
        *,
        description: str | Omit = omit,
        name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelGroup:
        """
        ### Description

        Updates a model group

        ### Details

        This API can be used to update the model group that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Model Group API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_group_id:
            raise ValueError(f"Expected a non-empty value for `model_group_id` but received {model_group_id!r}")
        return self._patch(
            f"/v4/model-groups/{model_group_id}",
            body=maybe_transform(
                {
                    "description": description,
                    "name": name,
                },
                model_group_update_params.ModelGroupUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelGroup,
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
    ) -> SyncPageResponse[ModelGroup]:
        """
        ### Description

        Lists all model groups accessible to the user.

        ### Details

        This API can be used to list model groups. If a user has access to multiple
        accounts, all model groups from all accounts the user is associated with will be
        returned.

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
            "/v4/model-groups",
            page=SyncPageResponse[ModelGroup],
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
                    model_group_list_params.ModelGroupListParams,
                ),
            ),
            model=ModelGroup,
        )

    def delete(
        self,
        model_group_id: str,
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

        Deletes a model group

        ### Details

        This API can be used to delete a model group by ID. To use this API, pass in the
        `id` that was returned from your Create Model Group API call as a path
        parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_group_id:
            raise ValueError(f"Expected a non-empty value for `model_group_id` but received {model_group_id!r}")
        return self._delete(
            f"/v4/model-groups/{model_group_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )


class AsyncModelGroupsResource(AsyncAPIResource):
    @cached_property
    def models(self) -> AsyncModelsResource:
        return AsyncModelsResource(self._client)

    @cached_property
    def usage_statistics(self) -> AsyncUsageStatisticsResource:
        return AsyncUsageStatisticsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncModelGroupsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncModelGroupsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncModelGroupsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncModelGroupsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        name: str,
        description: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelGroup:
        """### Description

        Model groups are grouping models together.

        You can add models with the same
        base_model_id.

        Args:
          account_id: The ID of the account that owns the given entity.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v4/model-groups",
            body=await async_maybe_transform(
                {
                    "account_id": account_id,
                    "name": name,
                    "description": description,
                },
                model_group_create_params.ModelGroupCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelGroup,
        )

    async def retrieve(
        self,
        model_group_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelGroup:
        """
        ### Description

        Gets the details of a model group

        ### Details

        This API can be used to get information about a single model group by ID. To use
        this API, pass in the `id` that was returned from your Create Model Group API
        call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_group_id:
            raise ValueError(f"Expected a non-empty value for `model_group_id` but received {model_group_id!r}")
        return await self._get(
            f"/v4/model-groups/{model_group_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelGroup,
        )

    async def update(
        self,
        model_group_id: str,
        *,
        description: str | Omit = omit,
        name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelGroup:
        """
        ### Description

        Updates a model group

        ### Details

        This API can be used to update the model group that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Model Group API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_group_id:
            raise ValueError(f"Expected a non-empty value for `model_group_id` but received {model_group_id!r}")
        return await self._patch(
            f"/v4/model-groups/{model_group_id}",
            body=await async_maybe_transform(
                {
                    "description": description,
                    "name": name,
                },
                model_group_update_params.ModelGroupUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelGroup,
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
    ) -> AsyncPaginator[ModelGroup, AsyncPageResponse[ModelGroup]]:
        """
        ### Description

        Lists all model groups accessible to the user.

        ### Details

        This API can be used to list model groups. If a user has access to multiple
        accounts, all model groups from all accounts the user is associated with will be
        returned.

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
            "/v4/model-groups",
            page=AsyncPageResponse[ModelGroup],
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
                    model_group_list_params.ModelGroupListParams,
                ),
            ),
            model=ModelGroup,
        )

    async def delete(
        self,
        model_group_id: str,
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

        Deletes a model group

        ### Details

        This API can be used to delete a model group by ID. To use this API, pass in the
        `id` that was returned from your Create Model Group API call as a path
        parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_group_id:
            raise ValueError(f"Expected a non-empty value for `model_group_id` but received {model_group_id!r}")
        return await self._delete(
            f"/v4/model-groups/{model_group_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )


class ModelGroupsResourceWithRawResponse:
    def __init__(self, model_groups: ModelGroupsResource) -> None:
        self._model_groups = model_groups

        self.create = to_raw_response_wrapper(
            model_groups.create,
        )
        self.retrieve = to_raw_response_wrapper(
            model_groups.retrieve,
        )
        self.update = to_raw_response_wrapper(
            model_groups.update,
        )
        self.list = to_raw_response_wrapper(
            model_groups.list,
        )
        self.delete = to_raw_response_wrapper(
            model_groups.delete,
        )

    @cached_property
    def models(self) -> ModelsResourceWithRawResponse:
        return ModelsResourceWithRawResponse(self._model_groups.models)

    @cached_property
    def usage_statistics(self) -> UsageStatisticsResourceWithRawResponse:
        return UsageStatisticsResourceWithRawResponse(self._model_groups.usage_statistics)


class AsyncModelGroupsResourceWithRawResponse:
    def __init__(self, model_groups: AsyncModelGroupsResource) -> None:
        self._model_groups = model_groups

        self.create = async_to_raw_response_wrapper(
            model_groups.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            model_groups.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            model_groups.update,
        )
        self.list = async_to_raw_response_wrapper(
            model_groups.list,
        )
        self.delete = async_to_raw_response_wrapper(
            model_groups.delete,
        )

    @cached_property
    def models(self) -> AsyncModelsResourceWithRawResponse:
        return AsyncModelsResourceWithRawResponse(self._model_groups.models)

    @cached_property
    def usage_statistics(self) -> AsyncUsageStatisticsResourceWithRawResponse:
        return AsyncUsageStatisticsResourceWithRawResponse(self._model_groups.usage_statistics)


class ModelGroupsResourceWithStreamingResponse:
    def __init__(self, model_groups: ModelGroupsResource) -> None:
        self._model_groups = model_groups

        self.create = to_streamed_response_wrapper(
            model_groups.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            model_groups.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            model_groups.update,
        )
        self.list = to_streamed_response_wrapper(
            model_groups.list,
        )
        self.delete = to_streamed_response_wrapper(
            model_groups.delete,
        )

    @cached_property
    def models(self) -> ModelsResourceWithStreamingResponse:
        return ModelsResourceWithStreamingResponse(self._model_groups.models)

    @cached_property
    def usage_statistics(self) -> UsageStatisticsResourceWithStreamingResponse:
        return UsageStatisticsResourceWithStreamingResponse(self._model_groups.usage_statistics)


class AsyncModelGroupsResourceWithStreamingResponse:
    def __init__(self, model_groups: AsyncModelGroupsResource) -> None:
        self._model_groups = model_groups

        self.create = async_to_streamed_response_wrapper(
            model_groups.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            model_groups.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            model_groups.update,
        )
        self.list = async_to_streamed_response_wrapper(
            model_groups.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            model_groups.delete,
        )

    @cached_property
    def models(self) -> AsyncModelsResourceWithStreamingResponse:
        return AsyncModelsResourceWithStreamingResponse(self._model_groups.models)

    @cached_property
    def usage_statistics(self) -> AsyncUsageStatisticsResourceWithStreamingResponse:
        return AsyncUsageStatisticsResourceWithStreamingResponse(self._model_groups.usage_statistics)
