# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import model_list_params, model_create_params, model_update_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncCursorPage, AsyncCursorPage
from ..types.chat import SortOrder, InferenceModelVendor
from .._base_client import AsyncPaginator, make_request_options
from ..types.chat.sort_order import SortOrder
from ..types.inference_model import InferenceModel
from ..types.model_delete_response import ModelDeleteResponse
from ..types.chat.inference_model_vendor import InferenceModelVendor

__all__ = ["ModelsResource", "AsyncModelsResource"]


class ModelsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ModelsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return ModelsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ModelsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return ModelsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        model: model_create_params.Model,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InferenceModel:
        """
        Create a custom model record in your account and begin deploying it through a
        supported serving vendor.

        A model here is a record for a model you deploy and serve through Scale's own
        inference vendors: only the `launch` and `llmengine` vendors are accepted and
        any other vendor is rejected. This is distinct from
        `GET /v5/chat/completions/models`, which lists the models already available to
        call for chat completions rather than creating or managing these records. The
        call is asynchronous — the record is created in a deploying status, a deployment
        job is recorded, and a Temporal workflow is started to perform the deployment,
        so the model is not ready for inference when this returns. A model name must be
        unique per vendor within your account; if a model with the same name and vendor
        already exists the request fails unless `on_conflict` is set to `update`, in
        which case the existing model is updated instead.

        Args:
          model: Register a model already served by an external / proxy-served vendor (e.g. an
              OpenAI-compatible self-hosted model behind the inference proxy).

              Unlike launch/llmengine, no Scale-side deployment is performed: the record is
              created READY and is immediately callable via /v5/chat/completions. Accepted
              only when NATIVE_OPENAI_INFERENCE_GATEWAY is enabled. The discriminator
              (model_vendor) covers every vendor except launch/llmengine, and no
              vendor_configuration applies.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v5/models",
            body=maybe_transform(model, model_create_params.ModelCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InferenceModel,
        )

    def retrieve(
        self,
        model_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InferenceModel:
        """
        Retrieve a single custom model record by its ID.

        Returns the model record — including its vendor, configuration, and current
        deployment status — for a model managed through this API and owned by the
        caller's account. This is distinct from `GET /v5/chat/completions/models`, which
        lists the models available to call for chat completions rather than returning a
        single managed record.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return self._get(
            path_template("/v5/models/{model_id}", model_id=model_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InferenceModel,
        )

    def update(
        self,
        model_id: str,
        *,
        model: model_update_params.Model,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InferenceModel:
        """
        Update a custom model record; vendor-configuration changes are applied
        asynchronously by redeploying the model.

        This supports three kinds of update: changing model metadata only, renaming the
        model, and changing the vendor configuration. A vendor-configuration change is
        asynchronous — it puts the model back into a deploying status, records an update
        job, and starts a Temporal workflow to redeploy, so the new configuration is not
        live when this returns; metadata-only and rename changes take effect
        immediately. The vendor configuration supplied must match the model's own vendor
        (`launch` or `llmengine`), and only those two vendors are supported. A model
        that is currently deploying cannot be modified and the request fails until
        deployment finishes. When renaming with `on_conflict` set to `swap`, the name is
        exchanged with an existing model of the same name and vendor instead of failing
        on the uniqueness constraint.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return self._patch(
            path_template("/v5/models/{model_id}", model_id=model_id),
            body=maybe_transform(model, model_update_params.ModelUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InferenceModel,
        )

    def list(
        self,
        *,
        ending_before: str | Omit = omit,
        limit: int | Omit = omit,
        model_vendor: InferenceModelVendor | Omit = omit,
        name: str | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPage[InferenceModel]:
        """
        List the custom model records registered in your account.

        Returns a paginated list of the model records managed through this API — models
        your account deploys through the `launch` or `llmengine` serving vendors —
        optionally filtered by name and by model vendor, and scoped to the caller's
        account. This is different from `GET /v5/chat/completions/models`, which lists
        the models available to invoke for chat completions; this endpoint returns the
        managed records along with their deployment status, not the catalog of callable
        completion models.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/models",
            page=SyncCursorPage[InferenceModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "limit": limit,
                        "model_vendor": model_vendor,
                        "name": name,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    model_list_params.ModelListParams,
                ),
            ),
            model=InferenceModel,
        )

    def delete(
        self,
        model_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelDeleteResponse:
        """
        Permanently delete a custom model record and tear down its deployment at the
        serving vendor.

        This is a hard delete: the model row is removed from your account entirely and
        cannot be restored afterward. Before the record is removed, if the model has an
        associated vendor deployment that deployment is torn down at its serving vendor.
        A model that is currently deploying cannot be deleted and the request fails
        until deployment finishes. This operates on the model records managed by this
        API, distinct from the `GET /v5/chat/completions/models` catalog of models
        callable for chat completions.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return self._delete(
            path_template("/v5/models/{model_id}", model_id=model_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelDeleteResponse,
        )


class AsyncModelsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncModelsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncModelsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncModelsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncModelsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        model: model_create_params.Model,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InferenceModel:
        """
        Create a custom model record in your account and begin deploying it through a
        supported serving vendor.

        A model here is a record for a model you deploy and serve through Scale's own
        inference vendors: only the `launch` and `llmengine` vendors are accepted and
        any other vendor is rejected. This is distinct from
        `GET /v5/chat/completions/models`, which lists the models already available to
        call for chat completions rather than creating or managing these records. The
        call is asynchronous — the record is created in a deploying status, a deployment
        job is recorded, and a Temporal workflow is started to perform the deployment,
        so the model is not ready for inference when this returns. A model name must be
        unique per vendor within your account; if a model with the same name and vendor
        already exists the request fails unless `on_conflict` is set to `update`, in
        which case the existing model is updated instead.

        Args:
          model: Register a model already served by an external / proxy-served vendor (e.g. an
              OpenAI-compatible self-hosted model behind the inference proxy).

              Unlike launch/llmengine, no Scale-side deployment is performed: the record is
              created READY and is immediately callable via /v5/chat/completions. Accepted
              only when NATIVE_OPENAI_INFERENCE_GATEWAY is enabled. The discriminator
              (model_vendor) covers every vendor except launch/llmengine, and no
              vendor_configuration applies.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v5/models",
            body=await async_maybe_transform(model, model_create_params.ModelCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InferenceModel,
        )

    async def retrieve(
        self,
        model_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InferenceModel:
        """
        Retrieve a single custom model record by its ID.

        Returns the model record — including its vendor, configuration, and current
        deployment status — for a model managed through this API and owned by the
        caller's account. This is distinct from `GET /v5/chat/completions/models`, which
        lists the models available to call for chat completions rather than returning a
        single managed record.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return await self._get(
            path_template("/v5/models/{model_id}", model_id=model_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InferenceModel,
        )

    async def update(
        self,
        model_id: str,
        *,
        model: model_update_params.Model,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InferenceModel:
        """
        Update a custom model record; vendor-configuration changes are applied
        asynchronously by redeploying the model.

        This supports three kinds of update: changing model metadata only, renaming the
        model, and changing the vendor configuration. A vendor-configuration change is
        asynchronous — it puts the model back into a deploying status, records an update
        job, and starts a Temporal workflow to redeploy, so the new configuration is not
        live when this returns; metadata-only and rename changes take effect
        immediately. The vendor configuration supplied must match the model's own vendor
        (`launch` or `llmengine`), and only those two vendors are supported. A model
        that is currently deploying cannot be modified and the request fails until
        deployment finishes. When renaming with `on_conflict` set to `swap`, the name is
        exchanged with an existing model of the same name and vendor instead of failing
        on the uniqueness constraint.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return await self._patch(
            path_template("/v5/models/{model_id}", model_id=model_id),
            body=await async_maybe_transform(model, model_update_params.ModelUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InferenceModel,
        )

    def list(
        self,
        *,
        ending_before: str | Omit = omit,
        limit: int | Omit = omit,
        model_vendor: InferenceModelVendor | Omit = omit,
        name: str | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[InferenceModel, AsyncCursorPage[InferenceModel]]:
        """
        List the custom model records registered in your account.

        Returns a paginated list of the model records managed through this API — models
        your account deploys through the `launch` or `llmengine` serving vendors —
        optionally filtered by name and by model vendor, and scoped to the caller's
        account. This is different from `GET /v5/chat/completions/models`, which lists
        the models available to invoke for chat completions; this endpoint returns the
        managed records along with their deployment status, not the catalog of callable
        completion models.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/models",
            page=AsyncCursorPage[InferenceModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "limit": limit,
                        "model_vendor": model_vendor,
                        "name": name,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    model_list_params.ModelListParams,
                ),
            ),
            model=InferenceModel,
        )

    async def delete(
        self,
        model_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelDeleteResponse:
        """
        Permanently delete a custom model record and tear down its deployment at the
        serving vendor.

        This is a hard delete: the model row is removed from your account entirely and
        cannot be restored afterward. Before the record is removed, if the model has an
        associated vendor deployment that deployment is torn down at its serving vendor.
        A model that is currently deploying cannot be deleted and the request fails
        until deployment finishes. This operates on the model records managed by this
        API, distinct from the `GET /v5/chat/completions/models` catalog of models
        callable for chat completions.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return await self._delete(
            path_template("/v5/models/{model_id}", model_id=model_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelDeleteResponse,
        )


class ModelsResourceWithRawResponse:
    def __init__(self, models: ModelsResource) -> None:
        self._models = models

        self.create = to_raw_response_wrapper(
            models.create,
        )
        self.retrieve = to_raw_response_wrapper(
            models.retrieve,
        )
        self.update = to_raw_response_wrapper(
            models.update,
        )
        self.list = to_raw_response_wrapper(
            models.list,
        )
        self.delete = to_raw_response_wrapper(
            models.delete,
        )


class AsyncModelsResourceWithRawResponse:
    def __init__(self, models: AsyncModelsResource) -> None:
        self._models = models

        self.create = async_to_raw_response_wrapper(
            models.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            models.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            models.update,
        )
        self.list = async_to_raw_response_wrapper(
            models.list,
        )
        self.delete = async_to_raw_response_wrapper(
            models.delete,
        )


class ModelsResourceWithStreamingResponse:
    def __init__(self, models: ModelsResource) -> None:
        self._models = models

        self.create = to_streamed_response_wrapper(
            models.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            models.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            models.update,
        )
        self.list = to_streamed_response_wrapper(
            models.list,
        )
        self.delete = to_streamed_response_wrapper(
            models.delete,
        )


class AsyncModelsResourceWithStreamingResponse:
    def __init__(self, models: AsyncModelsResource) -> None:
        self._models = models

        self.create = async_to_streamed_response_wrapper(
            models.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            models.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            models.update,
        )
        self.list = async_to_streamed_response_wrapper(
            models.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            models.delete,
        )
