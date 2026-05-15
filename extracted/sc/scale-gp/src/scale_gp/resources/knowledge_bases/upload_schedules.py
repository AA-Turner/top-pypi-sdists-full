# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import Literal

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
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
from ...types.knowledge_bases import (
    upload_schedule_list_params,
    upload_schedule_create_params,
    upload_schedule_update_params,
    upload_schedule_retrieve_params,
)
from ...types.shared.generic_delete_response import GenericDeleteResponse
from ...types.knowledge_bases.upload_schedule import UploadSchedule
from ...types.knowledge_bases.upload_schedule_with_views import UploadScheduleWithViews

__all__ = ["UploadSchedulesResource", "AsyncUploadSchedulesResource"]


class UploadSchedulesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UploadSchedulesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return UploadSchedulesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UploadSchedulesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return UploadSchedulesResourceWithStreamingResponse(self)

    def create(
        self,
        knowledge_base_id: str,
        *,
        chunking_strategy_config: upload_schedule_create_params.ChunkingStrategyConfig,
        interval: float,
        knowledge_base_data_source_id: str,
        account_id: str | Omit = omit,
        next_run_at: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> UploadSchedule:
        """
        ### Description

        Creates a upload schedule

        ### Details

        This API can be used to create a upload schedule. To use this API, review the
        request schema and pass in all fields that are required to create a upload
        schedule.

        Args:
          chunking_strategy_config: Only compliant with the .chunks file type

          account_id: The ID of the account that owns the given entity.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        return self._post(
            path_template(
                "/v4/knowledge-bases/{knowledge_base_id}/upload-schedules", knowledge_base_id=knowledge_base_id
            ),
            body=maybe_transform(
                {
                    "chunking_strategy_config": chunking_strategy_config,
                    "interval": interval,
                    "knowledge_base_data_source_id": knowledge_base_data_source_id,
                    "account_id": account_id,
                    "next_run_at": next_run_at,
                },
                upload_schedule_create_params.UploadScheduleCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UploadSchedule,
        )

    def retrieve(
        self,
        upload_schedule_id: str,
        *,
        knowledge_base_id: str,
        view: List[Literal["DataSource"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> UploadScheduleWithViews:
        """
        ### Description

        Gets the details of a upload schedule

        ### Details

        This API can be used to get information about a single upload schedule by ID. To
        use this API, pass in the `id` that was returned from your Create Upload
        Schedule API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not upload_schedule_id:
            raise ValueError(f"Expected a non-empty value for `upload_schedule_id` but received {upload_schedule_id!r}")
        return self._get(
            path_template(
                "/v4/knowledge-bases/{knowledge_base_id}/upload-schedules/{upload_schedule_id}",
                knowledge_base_id=knowledge_base_id,
                upload_schedule_id=upload_schedule_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"view": view}, upload_schedule_retrieve_params.UploadScheduleRetrieveParams),
            ),
            cast_to=UploadScheduleWithViews,
        )

    def update(
        self,
        upload_schedule_id: str,
        *,
        knowledge_base_id: str,
        chunking_strategy_config: upload_schedule_update_params.ChunkingStrategyConfig | Omit = omit,
        interval: float | Omit = omit,
        next_run_at: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> UploadSchedule:
        """
        ### Description

        Updates a upload schedule

        ### Details

        This API can be used to update the upload schedule that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Upload Schedule API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          chunking_strategy_config: Only compliant with the .chunks file type

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not upload_schedule_id:
            raise ValueError(f"Expected a non-empty value for `upload_schedule_id` but received {upload_schedule_id!r}")
        return self._patch(
            path_template(
                "/v4/knowledge-bases/{knowledge_base_id}/upload-schedules/{upload_schedule_id}",
                knowledge_base_id=knowledge_base_id,
                upload_schedule_id=upload_schedule_id,
            ),
            body=maybe_transform(
                {
                    "chunking_strategy_config": chunking_strategy_config,
                    "interval": interval,
                    "next_run_at": next_run_at,
                },
                upload_schedule_update_params.UploadScheduleUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UploadSchedule,
        )

    def list(
        self,
        knowledge_base_id: str,
        *,
        account_id: str | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        view: List[Literal["DataSource"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageResponse[UploadScheduleWithViews]:
        """
        ### Description

        Lists all upload schedules accessible to the user.

        ### Details

        This API can be used to list upload schedules. If a user has access to multiple
        accounts, all upload schedules from all accounts the user is associated with
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
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        return self._get_api_list(
            path_template(
                "/v4/knowledge-bases/{knowledge_base_id}/upload-schedules", knowledge_base_id=knowledge_base_id
            ),
            page=SyncPageResponse[UploadScheduleWithViews],
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
                        "view": view,
                    },
                    upload_schedule_list_params.UploadScheduleListParams,
                ),
            ),
            model=UploadScheduleWithViews,
        )

    def delete(
        self,
        upload_schedule_id: str,
        *,
        knowledge_base_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GenericDeleteResponse:
        """
        ### Description

        Deletes a upload schedule

        ### Details

        This API can be used to delete a upload schedule by ID. To use this API, pass in
        the `id` that was returned from your Create Upload Schedule API call as a path
        parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not upload_schedule_id:
            raise ValueError(f"Expected a non-empty value for `upload_schedule_id` but received {upload_schedule_id!r}")
        return self._delete(
            path_template(
                "/v4/knowledge-bases/{knowledge_base_id}/upload-schedules/{upload_schedule_id}",
                knowledge_base_id=knowledge_base_id,
                upload_schedule_id=upload_schedule_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )


class AsyncUploadSchedulesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUploadSchedulesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncUploadSchedulesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUploadSchedulesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncUploadSchedulesResourceWithStreamingResponse(self)

    async def create(
        self,
        knowledge_base_id: str,
        *,
        chunking_strategy_config: upload_schedule_create_params.ChunkingStrategyConfig,
        interval: float,
        knowledge_base_data_source_id: str,
        account_id: str | Omit = omit,
        next_run_at: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> UploadSchedule:
        """
        ### Description

        Creates a upload schedule

        ### Details

        This API can be used to create a upload schedule. To use this API, review the
        request schema and pass in all fields that are required to create a upload
        schedule.

        Args:
          chunking_strategy_config: Only compliant with the .chunks file type

          account_id: The ID of the account that owns the given entity.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        return await self._post(
            path_template(
                "/v4/knowledge-bases/{knowledge_base_id}/upload-schedules", knowledge_base_id=knowledge_base_id
            ),
            body=await async_maybe_transform(
                {
                    "chunking_strategy_config": chunking_strategy_config,
                    "interval": interval,
                    "knowledge_base_data_source_id": knowledge_base_data_source_id,
                    "account_id": account_id,
                    "next_run_at": next_run_at,
                },
                upload_schedule_create_params.UploadScheduleCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UploadSchedule,
        )

    async def retrieve(
        self,
        upload_schedule_id: str,
        *,
        knowledge_base_id: str,
        view: List[Literal["DataSource"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> UploadScheduleWithViews:
        """
        ### Description

        Gets the details of a upload schedule

        ### Details

        This API can be used to get information about a single upload schedule by ID. To
        use this API, pass in the `id` that was returned from your Create Upload
        Schedule API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not upload_schedule_id:
            raise ValueError(f"Expected a non-empty value for `upload_schedule_id` but received {upload_schedule_id!r}")
        return await self._get(
            path_template(
                "/v4/knowledge-bases/{knowledge_base_id}/upload-schedules/{upload_schedule_id}",
                knowledge_base_id=knowledge_base_id,
                upload_schedule_id=upload_schedule_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"view": view}, upload_schedule_retrieve_params.UploadScheduleRetrieveParams
                ),
            ),
            cast_to=UploadScheduleWithViews,
        )

    async def update(
        self,
        upload_schedule_id: str,
        *,
        knowledge_base_id: str,
        chunking_strategy_config: upload_schedule_update_params.ChunkingStrategyConfig | Omit = omit,
        interval: float | Omit = omit,
        next_run_at: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> UploadSchedule:
        """
        ### Description

        Updates a upload schedule

        ### Details

        This API can be used to update the upload schedule that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Upload Schedule API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          chunking_strategy_config: Only compliant with the .chunks file type

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not upload_schedule_id:
            raise ValueError(f"Expected a non-empty value for `upload_schedule_id` but received {upload_schedule_id!r}")
        return await self._patch(
            path_template(
                "/v4/knowledge-bases/{knowledge_base_id}/upload-schedules/{upload_schedule_id}",
                knowledge_base_id=knowledge_base_id,
                upload_schedule_id=upload_schedule_id,
            ),
            body=await async_maybe_transform(
                {
                    "chunking_strategy_config": chunking_strategy_config,
                    "interval": interval,
                    "next_run_at": next_run_at,
                },
                upload_schedule_update_params.UploadScheduleUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UploadSchedule,
        )

    def list(
        self,
        knowledge_base_id: str,
        *,
        account_id: str | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        view: List[Literal["DataSource"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[UploadScheduleWithViews, AsyncPageResponse[UploadScheduleWithViews]]:
        """
        ### Description

        Lists all upload schedules accessible to the user.

        ### Details

        This API can be used to list upload schedules. If a user has access to multiple
        accounts, all upload schedules from all accounts the user is associated with
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
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        return self._get_api_list(
            path_template(
                "/v4/knowledge-bases/{knowledge_base_id}/upload-schedules", knowledge_base_id=knowledge_base_id
            ),
            page=AsyncPageResponse[UploadScheduleWithViews],
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
                        "view": view,
                    },
                    upload_schedule_list_params.UploadScheduleListParams,
                ),
            ),
            model=UploadScheduleWithViews,
        )

    async def delete(
        self,
        upload_schedule_id: str,
        *,
        knowledge_base_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GenericDeleteResponse:
        """
        ### Description

        Deletes a upload schedule

        ### Details

        This API can be used to delete a upload schedule by ID. To use this API, pass in
        the `id` that was returned from your Create Upload Schedule API call as a path
        parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not upload_schedule_id:
            raise ValueError(f"Expected a non-empty value for `upload_schedule_id` but received {upload_schedule_id!r}")
        return await self._delete(
            path_template(
                "/v4/knowledge-bases/{knowledge_base_id}/upload-schedules/{upload_schedule_id}",
                knowledge_base_id=knowledge_base_id,
                upload_schedule_id=upload_schedule_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )


class UploadSchedulesResourceWithRawResponse:
    def __init__(self, upload_schedules: UploadSchedulesResource) -> None:
        self._upload_schedules = upload_schedules

        self.create = to_raw_response_wrapper(
            upload_schedules.create,
        )
        self.retrieve = to_raw_response_wrapper(
            upload_schedules.retrieve,
        )
        self.update = to_raw_response_wrapper(
            upload_schedules.update,
        )
        self.list = to_raw_response_wrapper(
            upload_schedules.list,
        )
        self.delete = to_raw_response_wrapper(
            upload_schedules.delete,
        )


class AsyncUploadSchedulesResourceWithRawResponse:
    def __init__(self, upload_schedules: AsyncUploadSchedulesResource) -> None:
        self._upload_schedules = upload_schedules

        self.create = async_to_raw_response_wrapper(
            upload_schedules.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            upload_schedules.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            upload_schedules.update,
        )
        self.list = async_to_raw_response_wrapper(
            upload_schedules.list,
        )
        self.delete = async_to_raw_response_wrapper(
            upload_schedules.delete,
        )


class UploadSchedulesResourceWithStreamingResponse:
    def __init__(self, upload_schedules: UploadSchedulesResource) -> None:
        self._upload_schedules = upload_schedules

        self.create = to_streamed_response_wrapper(
            upload_schedules.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            upload_schedules.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            upload_schedules.update,
        )
        self.list = to_streamed_response_wrapper(
            upload_schedules.list,
        )
        self.delete = to_streamed_response_wrapper(
            upload_schedules.delete,
        )


class AsyncUploadSchedulesResourceWithStreamingResponse:
    def __init__(self, upload_schedules: AsyncUploadSchedulesResource) -> None:
        self._upload_schedules = upload_schedules

        self.create = async_to_streamed_response_wrapper(
            upload_schedules.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            upload_schedules.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            upload_schedules.update,
        )
        self.list = async_to_streamed_response_wrapper(
            upload_schedules.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            upload_schedules.delete,
        )
