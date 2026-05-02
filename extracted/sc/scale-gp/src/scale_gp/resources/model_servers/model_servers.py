# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...types import model_server_create_params, model_server_execute_params, model_server_update_backend_params
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from .deployment import (
    DeploymentResource,
    AsyncDeploymentResource,
    DeploymentResourceWithRawResponse,
    AsyncDeploymentResourceWithRawResponse,
    DeploymentResourceWithStreamingResponse,
    AsyncDeploymentResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncTopLevelArray, AsyncTopLevelArray
from ..._base_client import AsyncPaginator, make_request_options
from ...types.generic_model_response import GenericModelResponse
from ...types.shared.model_server_info import ModelServerInfo
from ...types.model_server_rollback_response import ModelServerRollbackResponse
from ...types.model_server_update_backend_response import ModelServerUpdateBackendResponse

__all__ = ["ModelServersResource", "AsyncModelServersResource"]


class ModelServersResource(SyncAPIResource):
    @cached_property
    def deployment(self) -> DeploymentResource:
        return DeploymentResource(self._client)

    @cached_property
    def with_raw_response(self) -> ModelServersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return ModelServersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ModelServersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return ModelServersResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        model_deployment_id: str,
        name: str,
        alias: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelServerInfo:
        """
        Create a new Model Server

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v4/serving",
            body=maybe_transform(
                {
                    "model_deployment_id": model_deployment_id,
                    "name": name,
                    "alias": alias,
                },
                model_server_create_params.ModelServerCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelServerInfo,
        )

    def retrieve(
        self,
        model_server_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelServerInfo:
        """
        Fixed Server interface for Model execution by named alias

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_server_id:
            raise ValueError(f"Expected a non-empty value for `model_server_id` but received {model_server_id!r}")
        return self._get(
            f"/v4/serving/{model_server_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelServerInfo,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncTopLevelArray[ModelServerInfo]:
        """Fixed Server interface for Model execution by named alias"""
        return self._get_api_list(
            "/v4/serving",
            page=SyncTopLevelArray[ModelServerInfo],
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            model=ModelServerInfo,
        )

    def execute(
        self,
        model_server_id: str,
        *,
        stream: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GenericModelResponse:
        """
        Fixed Server interface for Model execution

        Args:
          stream: Flag indicating whether to stream the completion response

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_server_id:
            raise ValueError(f"Expected a non-empty value for `model_server_id` but received {model_server_id!r}")
        return self._post(
            f"/v4/serving/{model_server_id}/execute",
            body=maybe_transform({"stream": stream}, model_server_execute_params.ModelServerExecuteParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericModelResponse,
        )

    def rollback(
        self,
        model_server_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelServerRollbackResponse:
        """
        Rollback backend of the Model Server

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_server_id:
            raise ValueError(f"Expected a non-empty value for `model_server_id` but received {model_server_id!r}")
        return self._post(
            f"/v4/serving/{model_server_id}/rollback",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelServerRollbackResponse,
        )

    def update_backend(
        self,
        model_server_id: str,
        *,
        new_model_deployment_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelServerUpdateBackendResponse:
        """
        Change backend of the Model Server

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_server_id:
            raise ValueError(f"Expected a non-empty value for `model_server_id` but received {model_server_id!r}")
        return self._put(
            f"/v4/serving/{model_server_id}/backend",
            body=maybe_transform(
                {"new_model_deployment_id": new_model_deployment_id},
                model_server_update_backend_params.ModelServerUpdateBackendParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelServerUpdateBackendResponse,
        )


class AsyncModelServersResource(AsyncAPIResource):
    @cached_property
    def deployment(self) -> AsyncDeploymentResource:
        return AsyncDeploymentResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncModelServersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncModelServersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncModelServersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncModelServersResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        model_deployment_id: str,
        name: str,
        alias: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelServerInfo:
        """
        Create a new Model Server

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v4/serving",
            body=await async_maybe_transform(
                {
                    "model_deployment_id": model_deployment_id,
                    "name": name,
                    "alias": alias,
                },
                model_server_create_params.ModelServerCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelServerInfo,
        )

    async def retrieve(
        self,
        model_server_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelServerInfo:
        """
        Fixed Server interface for Model execution by named alias

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_server_id:
            raise ValueError(f"Expected a non-empty value for `model_server_id` but received {model_server_id!r}")
        return await self._get(
            f"/v4/serving/{model_server_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelServerInfo,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[ModelServerInfo, AsyncTopLevelArray[ModelServerInfo]]:
        """Fixed Server interface for Model execution by named alias"""
        return self._get_api_list(
            "/v4/serving",
            page=AsyncTopLevelArray[ModelServerInfo],
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            model=ModelServerInfo,
        )

    async def execute(
        self,
        model_server_id: str,
        *,
        stream: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GenericModelResponse:
        """
        Fixed Server interface for Model execution

        Args:
          stream: Flag indicating whether to stream the completion response

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_server_id:
            raise ValueError(f"Expected a non-empty value for `model_server_id` but received {model_server_id!r}")
        return await self._post(
            f"/v4/serving/{model_server_id}/execute",
            body=await async_maybe_transform({"stream": stream}, model_server_execute_params.ModelServerExecuteParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericModelResponse,
        )

    async def rollback(
        self,
        model_server_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelServerRollbackResponse:
        """
        Rollback backend of the Model Server

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_server_id:
            raise ValueError(f"Expected a non-empty value for `model_server_id` but received {model_server_id!r}")
        return await self._post(
            f"/v4/serving/{model_server_id}/rollback",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelServerRollbackResponse,
        )

    async def update_backend(
        self,
        model_server_id: str,
        *,
        new_model_deployment_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelServerUpdateBackendResponse:
        """
        Change backend of the Model Server

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_server_id:
            raise ValueError(f"Expected a non-empty value for `model_server_id` but received {model_server_id!r}")
        return await self._put(
            f"/v4/serving/{model_server_id}/backend",
            body=await async_maybe_transform(
                {"new_model_deployment_id": new_model_deployment_id},
                model_server_update_backend_params.ModelServerUpdateBackendParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelServerUpdateBackendResponse,
        )


class ModelServersResourceWithRawResponse:
    def __init__(self, model_servers: ModelServersResource) -> None:
        self._model_servers = model_servers

        self.create = to_raw_response_wrapper(
            model_servers.create,
        )
        self.retrieve = to_raw_response_wrapper(
            model_servers.retrieve,
        )
        self.list = to_raw_response_wrapper(
            model_servers.list,
        )
        self.execute = to_raw_response_wrapper(
            model_servers.execute,
        )
        self.rollback = to_raw_response_wrapper(
            model_servers.rollback,
        )
        self.update_backend = to_raw_response_wrapper(
            model_servers.update_backend,
        )

    @cached_property
    def deployment(self) -> DeploymentResourceWithRawResponse:
        return DeploymentResourceWithRawResponse(self._model_servers.deployment)


class AsyncModelServersResourceWithRawResponse:
    def __init__(self, model_servers: AsyncModelServersResource) -> None:
        self._model_servers = model_servers

        self.create = async_to_raw_response_wrapper(
            model_servers.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            model_servers.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            model_servers.list,
        )
        self.execute = async_to_raw_response_wrapper(
            model_servers.execute,
        )
        self.rollback = async_to_raw_response_wrapper(
            model_servers.rollback,
        )
        self.update_backend = async_to_raw_response_wrapper(
            model_servers.update_backend,
        )

    @cached_property
    def deployment(self) -> AsyncDeploymentResourceWithRawResponse:
        return AsyncDeploymentResourceWithRawResponse(self._model_servers.deployment)


class ModelServersResourceWithStreamingResponse:
    def __init__(self, model_servers: ModelServersResource) -> None:
        self._model_servers = model_servers

        self.create = to_streamed_response_wrapper(
            model_servers.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            model_servers.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            model_servers.list,
        )
        self.execute = to_streamed_response_wrapper(
            model_servers.execute,
        )
        self.rollback = to_streamed_response_wrapper(
            model_servers.rollback,
        )
        self.update_backend = to_streamed_response_wrapper(
            model_servers.update_backend,
        )

    @cached_property
    def deployment(self) -> DeploymentResourceWithStreamingResponse:
        return DeploymentResourceWithStreamingResponse(self._model_servers.deployment)


class AsyncModelServersResourceWithStreamingResponse:
    def __init__(self, model_servers: AsyncModelServersResource) -> None:
        self._model_servers = model_servers

        self.create = async_to_streamed_response_wrapper(
            model_servers.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            model_servers.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            model_servers.list,
        )
        self.execute = async_to_streamed_response_wrapper(
            model_servers.execute,
        )
        self.rollback = async_to_streamed_response_wrapper(
            model_servers.rollback,
        )
        self.update_backend = async_to_streamed_response_wrapper(
            model_servers.update_backend,
        )

    @cached_property
    def deployment(self) -> AsyncDeploymentResourceWithStreamingResponse:
        return AsyncDeploymentResourceWithStreamingResponse(self._model_servers.deployment)
