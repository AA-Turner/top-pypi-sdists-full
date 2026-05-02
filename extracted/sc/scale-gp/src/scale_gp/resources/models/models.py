# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union
from typing_extensions import Literal

import httpx

from ...types import model_list_params, model_create_params, model_update_params, model_retrieve_params
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from .embeddings import (
    EmbeddingsResource,
    AsyncEmbeddingsResource,
    EmbeddingsResourceWithRawResponse,
    AsyncEmbeddingsResourceWithRawResponse,
    EmbeddingsResourceWithStreamingResponse,
    AsyncEmbeddingsResourceWithStreamingResponse,
)
from .rerankings import (
    RerankingsResource,
    AsyncRerankingsResource,
    RerankingsResourceWithRawResponse,
    AsyncRerankingsResourceWithRawResponse,
    RerankingsResourceWithStreamingResponse,
    AsyncRerankingsResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .completions import (
    CompletionsResource,
    AsyncCompletionsResource,
    CompletionsResourceWithRawResponse,
    AsyncCompletionsResourceWithRawResponse,
    CompletionsResourceWithStreamingResponse,
    AsyncCompletionsResourceWithStreamingResponse,
)
from ...pagination import SyncPageResponse, AsyncPageResponse
from ..._base_client import AsyncPaginator, make_request_options
from .chat_completions import (
    ChatCompletionsResource,
    AsyncChatCompletionsResource,
    ChatCompletionsResourceWithRawResponse,
    AsyncChatCompletionsResourceWithRawResponse,
    ChatCompletionsResourceWithStreamingResponse,
    AsyncChatCompletionsResourceWithStreamingResponse,
)
from .usage_statistics import (
    UsageStatisticsResource,
    AsyncUsageStatisticsResource,
    UsageStatisticsResourceWithRawResponse,
    AsyncUsageStatisticsResourceWithRawResponse,
    UsageStatisticsResourceWithStreamingResponse,
    AsyncUsageStatisticsResourceWithStreamingResponse,
)
from ...types.model_instance import ModelInstance
from .deployments.deployments import (
    DeploymentsResource,
    AsyncDeploymentsResource,
    DeploymentsResourceWithRawResponse,
    AsyncDeploymentsResourceWithRawResponse,
    DeploymentsResourceWithStreamingResponse,
    AsyncDeploymentsResourceWithStreamingResponse,
)
from ...types.model_instance_with_views import ModelInstanceWithViews
from ...types.shared.generic_delete_response import GenericDeleteResponse

__all__ = ["ModelsResource", "AsyncModelsResource"]


class ModelsResource(SyncAPIResource):
    @cached_property
    def deployments(self) -> DeploymentsResource:
        return DeploymentsResource(self._client)

    @cached_property
    def embeddings(self) -> EmbeddingsResource:
        return EmbeddingsResource(self._client)

    @cached_property
    def rerankings(self) -> RerankingsResource:
        return RerankingsResource(self._client)

    @cached_property
    def completions(self) -> CompletionsResource:
        return CompletionsResource(self._client)

    @cached_property
    def chat_completions(self) -> ChatCompletionsResource:
        return ChatCompletionsResource(self._client)

    @cached_property
    def usage_statistics(self) -> UsageStatisticsResource:
        return UsageStatisticsResource(self._client)

    @cached_property
    def with_raw_response(self) -> ModelsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return ModelsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ModelsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return ModelsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        model_type: Literal["COMPLETION", "CHAT_COMPLETION", "AGENT", "EMBEDDING", "RERANKING", "GENERIC", "BUNDLE"],
        name: str,
        base_model_id: str | Omit = omit,
        base_model_metadata: model_create_params.BaseModelMetadata | Omit = omit,
        description: str | Omit = omit,
        display_name: str | Omit = omit,
        model_card: str | Omit = omit,
        model_creation_parameters: Dict[str, object] | Omit = omit,
        model_group_id: str | Omit = omit,
        model_template_id: str | Omit = omit,
        model_vendor: Literal[
            "OPENAI",
            "COHERE",
            "GOOGLE",
            "VERTEX_AI",
            "ANTHROPIC",
            "LAUNCH",
            "LLMENGINE",
            "BEDROCK",
            "FIREWORKS_AI",
            "OTHER",
        ]
        | Omit = omit,
        training_data_card: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelInstance:
        """
        ### Description

        Creates and hosts a model based on a model template.

        Base embedding models, chunk ranking functions, and LLMs are often not
        sufficient for customer use cases. We have shown in various blogs that
        fine-tuning these models on customer data can lead to significant improvements
        in performance.

        1. [We Fine-Tuned GPT-4 to Beat the Industry Standard for Text2SQL](https://scale.com/blog/text2sql-fine-tuning)
        2. [OpenAI Names Scale as Preferred Partner to Fine-Tune GPT-3.5](https://scale.com/blog/open-ai-scale-partnership-gpt-3-5-fine-tuning)
        3. [How to Fine-Tune GPT-3.5 Turbo With OpenAI API](https://scale.com/blog/fine-tune-gpt-3.5)

        ### Details

        Before creating a model, you must first create a model template. A model
        template serves 2 purposes. First, it provides common scaffolding that is static
        across multiple models. Second, it exposes several variables that can be
        injected at model creation time to customize the model.

        For example, a model template can define a docker image that contains code to
        run a HuggingFace or SentenceTransformers model. This docker image code also
        accepts environment variables that can be set to swap out the model weights or
        model name. Refer to the Create Model Template API for more details.

        To create a new model, users must refer to an existing model template and
        provide the necessary parameters the the model template requires in its
        `model_creation_parameters_schema` field. The combination of the model template
        and the model creation parameters will be used to create and deploy a new model.

        Once a model has been created, it can be executed by calling the Execute Model
        API.

        ### Coming Soon

        Some of our EGP APIs depend on models, for example Knowledge Base APIs depend on
        embedding models, Chunk Ranking APIs depend on ranking models, and Completion
        APIs depend on LLMs.

        In the near future, if a model is created from a model template that is
        compatible with one of these APIs (based on the model template's
        `model_type field`), the model will automatically be registered with the API.
        This will allow users to immediately start using the model with those API
        without any additional setup.

        Args:
          account_id: The ID of the account that owns the given entity.

          model_type: An enum representing the different types of models supported.

              Attributes: COMPLETION: Denotes that the model type is completion.
              CHAT_COMPLETION: Denotes that the model type is chat completion. AGENT: Denotes
              that the model type is agent. EMBEDDING: Denotes that the model type is
              embedding. RERANKING: Denotes that the model type is reranking. GENERIC: Denotes
              that the model type is generic. BUNDLE: "Not to be used directly - type to
              surface a model bundle in the UI - TODO: Explicitly type a bundle

          model_vendor: An enum representing the different types of model vendors supported.

              Attributes: OPENAI: Denotes that the model vendor is OpenAI. COHERE: Denotes
              that the model vendor is Cohere. GOOGLE: Denotes that the model vendor is
              Google. ANTHROPIC: Denotes that the model vendor is Anthropic. LLMENGINE:
              Denotes that the model vendor is LLM Engine. OTHER: Denotes that the model
              vendor is Other.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v4/models",
            body=maybe_transform(
                {
                    "account_id": account_id,
                    "model_type": model_type,
                    "name": name,
                    "base_model_id": base_model_id,
                    "base_model_metadata": base_model_metadata,
                    "description": description,
                    "display_name": display_name,
                    "model_card": model_card,
                    "model_creation_parameters": model_creation_parameters,
                    "model_group_id": model_group_id,
                    "model_template_id": model_template_id,
                    "model_vendor": model_vendor,
                    "training_data_card": training_data_card,
                },
                model_create_params.ModelCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelInstance,
        )

    def retrieve(
        self,
        model_id: str,
        *,
        view: List[Literal["Deployments", "ModelGroup"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelInstanceWithViews:
        """
        ### Description

        Gets the details of a model

        ### Details

        This API can be used to get information about a single model by ID. To use this
        API, pass in the `id` that was returned from your Create Model API call as a
        path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return self._get(
            f"/v4/models/{model_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"view": view}, model_retrieve_params.ModelRetrieveParams),
            ),
            cast_to=ModelInstanceWithViews,
        )

    def update(
        self,
        model_id: str,
        *,
        base_model_id: str | Omit = omit,
        base_model_metadata: model_update_params.BaseModelMetadata | Omit = omit,
        description: str | Omit = omit,
        display_name: str | Omit = omit,
        model_card: str | Omit = omit,
        model_creation_parameters: Dict[str, object] | Omit = omit,
        model_group_id: str | Omit = omit,
        model_template_id: str | Omit = omit,
        model_type: Literal["COMPLETION", "CHAT_COMPLETION", "AGENT", "EMBEDDING", "RERANKING", "GENERIC", "BUNDLE"]
        | Omit = omit,
        model_vendor: Literal[
            "OPENAI",
            "COHERE",
            "GOOGLE",
            "VERTEX_AI",
            "ANTHROPIC",
            "LAUNCH",
            "LLMENGINE",
            "BEDROCK",
            "FIREWORKS_AI",
            "OTHER",
        ]
        | Omit = omit,
        name: str | Omit = omit,
        training_data_card: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelInstance:
        """
        ### Description

        Updates a model

        ### Details

        This API can be used to update the model that matches the ID that was passed in
        as a path parameter. To use this API, pass in the `id` that was returned from
        your Create Model API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          model_type: An enum representing the different types of models supported.

              Attributes: COMPLETION: Denotes that the model type is completion.
              CHAT_COMPLETION: Denotes that the model type is chat completion. AGENT: Denotes
              that the model type is agent. EMBEDDING: Denotes that the model type is
              embedding. RERANKING: Denotes that the model type is reranking. GENERIC: Denotes
              that the model type is generic. BUNDLE: "Not to be used directly - type to
              surface a model bundle in the UI - TODO: Explicitly type a bundle

          model_vendor: An enum representing the different types of model vendors supported.

              Attributes: OPENAI: Denotes that the model vendor is OpenAI. COHERE: Denotes
              that the model vendor is Cohere. GOOGLE: Denotes that the model vendor is
              Google. ANTHROPIC: Denotes that the model vendor is Anthropic. LLMENGINE:
              Denotes that the model vendor is LLM Engine. OTHER: Denotes that the model
              vendor is Other.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return self._patch(
            f"/v4/models/{model_id}",
            body=maybe_transform(
                {
                    "base_model_id": base_model_id,
                    "base_model_metadata": base_model_metadata,
                    "description": description,
                    "display_name": display_name,
                    "model_card": model_card,
                    "model_creation_parameters": model_creation_parameters,
                    "model_group_id": model_group_id,
                    "model_template_id": model_template_id,
                    "model_type": model_type,
                    "model_vendor": model_vendor,
                    "name": name,
                    "training_data_card": training_data_card,
                },
                model_update_params.ModelUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelInstance,
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        limit: int | Omit = omit,
        model_group_id: Union[int, str] | Omit = omit,
        model_type: Union[int, str] | Omit = omit,
        page: int | Omit = omit,
        sort_by: List[
            Literal[
                "display_name:asc",
                "display_name:desc",
                "model_vendor:asc",
                "model_vendor:desc",
                "base_model_id:asc",
                "base_model_id:desc",
                "base_model_metadata:asc",
                "base_model_metadata:desc",
                "model_creation_parameters:asc",
                "model_creation_parameters:desc",
                "model_card:asc",
                "model_card:desc",
                "training_data_card:asc",
                "training_data_card:desc",
                "description:asc",
                "description:desc",
                "model_template_id:asc",
                "model_template_id:desc",
                "model_group_id:asc",
                "model_group_id:desc",
                "model_group:asc",
                "model_group:desc",
                "request_schema:asc",
                "request_schema:desc",
                "response_schema:asc",
                "response_schema:desc",
                "deployment_count:asc",
                "deployment_count:desc",
                "supports_multi_turn:asc",
                "supports_multi_turn:desc",
                "deployments:asc",
                "deployments:desc",
                "id:asc",
                "id:desc",
                "created_at:asc",
                "created_at:desc",
                "account_id:asc",
                "account_id:desc",
                "created_by_user_id:asc",
                "created_by_user_id:desc",
                "created_by_identity_type:asc",
                "created_by_identity_type:desc",
                "name:asc",
                "name:desc",
                "model_type:asc",
                "model_type:desc",
            ]
        ]
        | Omit = omit,
        view: List[Literal["Deployments", "ModelGroup"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageResponse[ModelInstanceWithViews]:
        """
        ### Description

        Lists all models accessible to the user.

        ### Details

        This API can be used to list models. If a user has access to multiple accounts,
        all models from all accounts the user is associated with will be returned.

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
            "/v4/models",
            page=SyncPageResponse[ModelInstanceWithViews],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "limit": limit,
                        "model_group_id": model_group_id,
                        "model_type": model_type,
                        "page": page,
                        "sort_by": sort_by,
                        "view": view,
                    },
                    model_list_params.ModelListParams,
                ),
            ),
            model=ModelInstanceWithViews,
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
    ) -> GenericDeleteResponse:
        """
        ### Description

        Deletes a model

        ### Details

        This API can be used to delete a model by ID. To use this API, pass in the `id`
        that was returned from your Create Model API call as a path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return self._delete(
            f"/v4/models/{model_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )


class AsyncModelsResource(AsyncAPIResource):
    @cached_property
    def deployments(self) -> AsyncDeploymentsResource:
        return AsyncDeploymentsResource(self._client)

    @cached_property
    def embeddings(self) -> AsyncEmbeddingsResource:
        return AsyncEmbeddingsResource(self._client)

    @cached_property
    def rerankings(self) -> AsyncRerankingsResource:
        return AsyncRerankingsResource(self._client)

    @cached_property
    def completions(self) -> AsyncCompletionsResource:
        return AsyncCompletionsResource(self._client)

    @cached_property
    def chat_completions(self) -> AsyncChatCompletionsResource:
        return AsyncChatCompletionsResource(self._client)

    @cached_property
    def usage_statistics(self) -> AsyncUsageStatisticsResource:
        return AsyncUsageStatisticsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncModelsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncModelsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncModelsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncModelsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        model_type: Literal["COMPLETION", "CHAT_COMPLETION", "AGENT", "EMBEDDING", "RERANKING", "GENERIC", "BUNDLE"],
        name: str,
        base_model_id: str | Omit = omit,
        base_model_metadata: model_create_params.BaseModelMetadata | Omit = omit,
        description: str | Omit = omit,
        display_name: str | Omit = omit,
        model_card: str | Omit = omit,
        model_creation_parameters: Dict[str, object] | Omit = omit,
        model_group_id: str | Omit = omit,
        model_template_id: str | Omit = omit,
        model_vendor: Literal[
            "OPENAI",
            "COHERE",
            "GOOGLE",
            "VERTEX_AI",
            "ANTHROPIC",
            "LAUNCH",
            "LLMENGINE",
            "BEDROCK",
            "FIREWORKS_AI",
            "OTHER",
        ]
        | Omit = omit,
        training_data_card: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelInstance:
        """
        ### Description

        Creates and hosts a model based on a model template.

        Base embedding models, chunk ranking functions, and LLMs are often not
        sufficient for customer use cases. We have shown in various blogs that
        fine-tuning these models on customer data can lead to significant improvements
        in performance.

        1. [We Fine-Tuned GPT-4 to Beat the Industry Standard for Text2SQL](https://scale.com/blog/text2sql-fine-tuning)
        2. [OpenAI Names Scale as Preferred Partner to Fine-Tune GPT-3.5](https://scale.com/blog/open-ai-scale-partnership-gpt-3-5-fine-tuning)
        3. [How to Fine-Tune GPT-3.5 Turbo With OpenAI API](https://scale.com/blog/fine-tune-gpt-3.5)

        ### Details

        Before creating a model, you must first create a model template. A model
        template serves 2 purposes. First, it provides common scaffolding that is static
        across multiple models. Second, it exposes several variables that can be
        injected at model creation time to customize the model.

        For example, a model template can define a docker image that contains code to
        run a HuggingFace or SentenceTransformers model. This docker image code also
        accepts environment variables that can be set to swap out the model weights or
        model name. Refer to the Create Model Template API for more details.

        To create a new model, users must refer to an existing model template and
        provide the necessary parameters the the model template requires in its
        `model_creation_parameters_schema` field. The combination of the model template
        and the model creation parameters will be used to create and deploy a new model.

        Once a model has been created, it can be executed by calling the Execute Model
        API.

        ### Coming Soon

        Some of our EGP APIs depend on models, for example Knowledge Base APIs depend on
        embedding models, Chunk Ranking APIs depend on ranking models, and Completion
        APIs depend on LLMs.

        In the near future, if a model is created from a model template that is
        compatible with one of these APIs (based on the model template's
        `model_type field`), the model will automatically be registered with the API.
        This will allow users to immediately start using the model with those API
        without any additional setup.

        Args:
          account_id: The ID of the account that owns the given entity.

          model_type: An enum representing the different types of models supported.

              Attributes: COMPLETION: Denotes that the model type is completion.
              CHAT_COMPLETION: Denotes that the model type is chat completion. AGENT: Denotes
              that the model type is agent. EMBEDDING: Denotes that the model type is
              embedding. RERANKING: Denotes that the model type is reranking. GENERIC: Denotes
              that the model type is generic. BUNDLE: "Not to be used directly - type to
              surface a model bundle in the UI - TODO: Explicitly type a bundle

          model_vendor: An enum representing the different types of model vendors supported.

              Attributes: OPENAI: Denotes that the model vendor is OpenAI. COHERE: Denotes
              that the model vendor is Cohere. GOOGLE: Denotes that the model vendor is
              Google. ANTHROPIC: Denotes that the model vendor is Anthropic. LLMENGINE:
              Denotes that the model vendor is LLM Engine. OTHER: Denotes that the model
              vendor is Other.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v4/models",
            body=await async_maybe_transform(
                {
                    "account_id": account_id,
                    "model_type": model_type,
                    "name": name,
                    "base_model_id": base_model_id,
                    "base_model_metadata": base_model_metadata,
                    "description": description,
                    "display_name": display_name,
                    "model_card": model_card,
                    "model_creation_parameters": model_creation_parameters,
                    "model_group_id": model_group_id,
                    "model_template_id": model_template_id,
                    "model_vendor": model_vendor,
                    "training_data_card": training_data_card,
                },
                model_create_params.ModelCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelInstance,
        )

    async def retrieve(
        self,
        model_id: str,
        *,
        view: List[Literal["Deployments", "ModelGroup"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelInstanceWithViews:
        """
        ### Description

        Gets the details of a model

        ### Details

        This API can be used to get information about a single model by ID. To use this
        API, pass in the `id` that was returned from your Create Model API call as a
        path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return await self._get(
            f"/v4/models/{model_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"view": view}, model_retrieve_params.ModelRetrieveParams),
            ),
            cast_to=ModelInstanceWithViews,
        )

    async def update(
        self,
        model_id: str,
        *,
        base_model_id: str | Omit = omit,
        base_model_metadata: model_update_params.BaseModelMetadata | Omit = omit,
        description: str | Omit = omit,
        display_name: str | Omit = omit,
        model_card: str | Omit = omit,
        model_creation_parameters: Dict[str, object] | Omit = omit,
        model_group_id: str | Omit = omit,
        model_template_id: str | Omit = omit,
        model_type: Literal["COMPLETION", "CHAT_COMPLETION", "AGENT", "EMBEDDING", "RERANKING", "GENERIC", "BUNDLE"]
        | Omit = omit,
        model_vendor: Literal[
            "OPENAI",
            "COHERE",
            "GOOGLE",
            "VERTEX_AI",
            "ANTHROPIC",
            "LAUNCH",
            "LLMENGINE",
            "BEDROCK",
            "FIREWORKS_AI",
            "OTHER",
        ]
        | Omit = omit,
        name: str | Omit = omit,
        training_data_card: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelInstance:
        """
        ### Description

        Updates a model

        ### Details

        This API can be used to update the model that matches the ID that was passed in
        as a path parameter. To use this API, pass in the `id` that was returned from
        your Create Model API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          model_type: An enum representing the different types of models supported.

              Attributes: COMPLETION: Denotes that the model type is completion.
              CHAT_COMPLETION: Denotes that the model type is chat completion. AGENT: Denotes
              that the model type is agent. EMBEDDING: Denotes that the model type is
              embedding. RERANKING: Denotes that the model type is reranking. GENERIC: Denotes
              that the model type is generic. BUNDLE: "Not to be used directly - type to
              surface a model bundle in the UI - TODO: Explicitly type a bundle

          model_vendor: An enum representing the different types of model vendors supported.

              Attributes: OPENAI: Denotes that the model vendor is OpenAI. COHERE: Denotes
              that the model vendor is Cohere. GOOGLE: Denotes that the model vendor is
              Google. ANTHROPIC: Denotes that the model vendor is Anthropic. LLMENGINE:
              Denotes that the model vendor is LLM Engine. OTHER: Denotes that the model
              vendor is Other.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return await self._patch(
            f"/v4/models/{model_id}",
            body=await async_maybe_transform(
                {
                    "base_model_id": base_model_id,
                    "base_model_metadata": base_model_metadata,
                    "description": description,
                    "display_name": display_name,
                    "model_card": model_card,
                    "model_creation_parameters": model_creation_parameters,
                    "model_group_id": model_group_id,
                    "model_template_id": model_template_id,
                    "model_type": model_type,
                    "model_vendor": model_vendor,
                    "name": name,
                    "training_data_card": training_data_card,
                },
                model_update_params.ModelUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelInstance,
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        limit: int | Omit = omit,
        model_group_id: Union[int, str] | Omit = omit,
        model_type: Union[int, str] | Omit = omit,
        page: int | Omit = omit,
        sort_by: List[
            Literal[
                "display_name:asc",
                "display_name:desc",
                "model_vendor:asc",
                "model_vendor:desc",
                "base_model_id:asc",
                "base_model_id:desc",
                "base_model_metadata:asc",
                "base_model_metadata:desc",
                "model_creation_parameters:asc",
                "model_creation_parameters:desc",
                "model_card:asc",
                "model_card:desc",
                "training_data_card:asc",
                "training_data_card:desc",
                "description:asc",
                "description:desc",
                "model_template_id:asc",
                "model_template_id:desc",
                "model_group_id:asc",
                "model_group_id:desc",
                "model_group:asc",
                "model_group:desc",
                "request_schema:asc",
                "request_schema:desc",
                "response_schema:asc",
                "response_schema:desc",
                "deployment_count:asc",
                "deployment_count:desc",
                "supports_multi_turn:asc",
                "supports_multi_turn:desc",
                "deployments:asc",
                "deployments:desc",
                "id:asc",
                "id:desc",
                "created_at:asc",
                "created_at:desc",
                "account_id:asc",
                "account_id:desc",
                "created_by_user_id:asc",
                "created_by_user_id:desc",
                "created_by_identity_type:asc",
                "created_by_identity_type:desc",
                "name:asc",
                "name:desc",
                "model_type:asc",
                "model_type:desc",
            ]
        ]
        | Omit = omit,
        view: List[Literal["Deployments", "ModelGroup"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[ModelInstanceWithViews, AsyncPageResponse[ModelInstanceWithViews]]:
        """
        ### Description

        Lists all models accessible to the user.

        ### Details

        This API can be used to list models. If a user has access to multiple accounts,
        all models from all accounts the user is associated with will be returned.

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
            "/v4/models",
            page=AsyncPageResponse[ModelInstanceWithViews],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "limit": limit,
                        "model_group_id": model_group_id,
                        "model_type": model_type,
                        "page": page,
                        "sort_by": sort_by,
                        "view": view,
                    },
                    model_list_params.ModelListParams,
                ),
            ),
            model=ModelInstanceWithViews,
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
    ) -> GenericDeleteResponse:
        """
        ### Description

        Deletes a model

        ### Details

        This API can be used to delete a model by ID. To use this API, pass in the `id`
        that was returned from your Create Model API call as a path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return await self._delete(
            f"/v4/models/{model_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
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

    @cached_property
    def deployments(self) -> DeploymentsResourceWithRawResponse:
        return DeploymentsResourceWithRawResponse(self._models.deployments)

    @cached_property
    def embeddings(self) -> EmbeddingsResourceWithRawResponse:
        return EmbeddingsResourceWithRawResponse(self._models.embeddings)

    @cached_property
    def rerankings(self) -> RerankingsResourceWithRawResponse:
        return RerankingsResourceWithRawResponse(self._models.rerankings)

    @cached_property
    def completions(self) -> CompletionsResourceWithRawResponse:
        return CompletionsResourceWithRawResponse(self._models.completions)

    @cached_property
    def chat_completions(self) -> ChatCompletionsResourceWithRawResponse:
        return ChatCompletionsResourceWithRawResponse(self._models.chat_completions)

    @cached_property
    def usage_statistics(self) -> UsageStatisticsResourceWithRawResponse:
        return UsageStatisticsResourceWithRawResponse(self._models.usage_statistics)


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

    @cached_property
    def deployments(self) -> AsyncDeploymentsResourceWithRawResponse:
        return AsyncDeploymentsResourceWithRawResponse(self._models.deployments)

    @cached_property
    def embeddings(self) -> AsyncEmbeddingsResourceWithRawResponse:
        return AsyncEmbeddingsResourceWithRawResponse(self._models.embeddings)

    @cached_property
    def rerankings(self) -> AsyncRerankingsResourceWithRawResponse:
        return AsyncRerankingsResourceWithRawResponse(self._models.rerankings)

    @cached_property
    def completions(self) -> AsyncCompletionsResourceWithRawResponse:
        return AsyncCompletionsResourceWithRawResponse(self._models.completions)

    @cached_property
    def chat_completions(self) -> AsyncChatCompletionsResourceWithRawResponse:
        return AsyncChatCompletionsResourceWithRawResponse(self._models.chat_completions)

    @cached_property
    def usage_statistics(self) -> AsyncUsageStatisticsResourceWithRawResponse:
        return AsyncUsageStatisticsResourceWithRawResponse(self._models.usage_statistics)


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

    @cached_property
    def deployments(self) -> DeploymentsResourceWithStreamingResponse:
        return DeploymentsResourceWithStreamingResponse(self._models.deployments)

    @cached_property
    def embeddings(self) -> EmbeddingsResourceWithStreamingResponse:
        return EmbeddingsResourceWithStreamingResponse(self._models.embeddings)

    @cached_property
    def rerankings(self) -> RerankingsResourceWithStreamingResponse:
        return RerankingsResourceWithStreamingResponse(self._models.rerankings)

    @cached_property
    def completions(self) -> CompletionsResourceWithStreamingResponse:
        return CompletionsResourceWithStreamingResponse(self._models.completions)

    @cached_property
    def chat_completions(self) -> ChatCompletionsResourceWithStreamingResponse:
        return ChatCompletionsResourceWithStreamingResponse(self._models.chat_completions)

    @cached_property
    def usage_statistics(self) -> UsageStatisticsResourceWithStreamingResponse:
        return UsageStatisticsResourceWithStreamingResponse(self._models.usage_statistics)


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

    @cached_property
    def deployments(self) -> AsyncDeploymentsResourceWithStreamingResponse:
        return AsyncDeploymentsResourceWithStreamingResponse(self._models.deployments)

    @cached_property
    def embeddings(self) -> AsyncEmbeddingsResourceWithStreamingResponse:
        return AsyncEmbeddingsResourceWithStreamingResponse(self._models.embeddings)

    @cached_property
    def rerankings(self) -> AsyncRerankingsResourceWithStreamingResponse:
        return AsyncRerankingsResourceWithStreamingResponse(self._models.rerankings)

    @cached_property
    def completions(self) -> AsyncCompletionsResourceWithStreamingResponse:
        return AsyncCompletionsResourceWithStreamingResponse(self._models.completions)

    @cached_property
    def chat_completions(self) -> AsyncChatCompletionsResourceWithStreamingResponse:
        return AsyncChatCompletionsResourceWithStreamingResponse(self._models.chat_completions)

    @cached_property
    def usage_statistics(self) -> AsyncUsageStatisticsResourceWithStreamingResponse:
        return AsyncUsageStatisticsResourceWithStreamingResponse(self._models.usage_statistics)
