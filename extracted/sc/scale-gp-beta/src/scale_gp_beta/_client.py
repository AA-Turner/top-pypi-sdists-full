# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Dict, Mapping, cast
from typing_extensions import Self, Literal, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    not_given,
)
from ._utils import is_given, get_async_library
from ._compat import cached_property
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError, SGPClientError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

if TYPE_CHECKING:
    from .resources import (
        chat,
        build,
        files,
        spans,
        deploy,
        models,
        rubrics,
        secrets,
        datasets,
        inference,
        questions,
        responses,
        completions,
        credentials,
        evaluations,
        dataset_items,
        vector_stores,
        evaluation_items,
        span_assessments,
        evaluation_groups,
        evaluation_dashboards,
    )
    from .resources.build import BuildResource, AsyncBuildResource
    from .resources.spans import SpansResource, AsyncSpansResource
    from .resources.deploy import DeployResource, AsyncDeployResource
    from .resources.models import ModelsResource, AsyncModelsResource
    from .resources.secrets import SecretsResource, AsyncSecretsResource
    from .resources.datasets import DatasetsResource, AsyncDatasetsResource
    from .resources.chat.chat import ChatResource, AsyncChatResource
    from .resources.inference import InferenceResource, AsyncInferenceResource
    from .resources.questions import QuestionsResource, AsyncQuestionsResource
    from .resources.responses import ResponsesResource, AsyncResponsesResource
    from .resources.completions import CompletionsResource, AsyncCompletionsResource
    from .resources.credentials import CredentialsResource, AsyncCredentialsResource
    from .resources.evaluations import EvaluationsResource, AsyncEvaluationsResource
    from .resources.files.files import FilesResource, AsyncFilesResource
    from .resources.dataset_items import DatasetItemsResource, AsyncDatasetItemsResource
    from .resources.rubrics.rubrics import RubricsResource, AsyncRubricsResource
    from .resources.evaluation_items import EvaluationItemsResource, AsyncEvaluationItemsResource
    from .resources.span_assessments import SpanAssessmentsResource, AsyncSpanAssessmentsResource
    from .resources.evaluation_groups import EvaluationGroupsResource, AsyncEvaluationGroupsResource
    from .resources.vector_stores.vector_stores import VectorStoresResource, AsyncVectorStoresResource
    from .resources.evaluation_dashboards.evaluation_dashboards import (
        EvaluationDashboardsResource,
        AsyncEvaluationDashboardsResource,
    )

__all__ = [
    "ENVIRONMENTS",
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "SGPClient",
    "AsyncSGPClient",
    "Client",
    "AsyncClient",
]

ENVIRONMENTS: Dict[str, str] = {
    "production": "https://api.egp.scale.com",
    "production-multitenant": "https://api.sgp.scale.com",
    "staging": "https://api.staging-sgp.scale.com",
    "development": "https://api.dev-sgp.scale.com",
    "local": "http://127.0.0.1:5003/public",
}


class SGPClient(SyncAPIClient):
    # client options
    api_key: str
    account_id: str

    _environment: Literal["production", "production-multitenant", "staging", "development", "local"] | NotGiven

    def __init__(
        self,
        *,
        api_key: str | None = None,
        account_id: str | None = None,
        environment: Literal["production", "production-multitenant", "staging", "development", "local"]
        | NotGiven = not_given,
        base_url: str | httpx.URL | None | NotGiven = not_given,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous SGPClient client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `SGP_API_KEY`
        - `account_id` from `SGP_ACCOUNT_ID`
        """
        if api_key is None:
            api_key = os.environ.get("SGP_API_KEY")
        if api_key is None:
            raise SGPClientError(
                "The api_key client option must be set either by passing api_key to the client or by setting the SGP_API_KEY environment variable"
            )
        self.api_key = api_key

        if account_id is None:
            account_id = os.environ.get("SGP_ACCOUNT_ID")
        if account_id is None:
            raise SGPClientError(
                "The account_id client option must be set either by passing account_id to the client or by setting the SGP_ACCOUNT_ID environment variable"
            )
        self.account_id = account_id

        self._environment = environment

        base_url_env = os.environ.get("SGP_CLIENT_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `SGP_CLIENT_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "production"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self._default_stream_cls = Stream

    @cached_property
    def responses(self) -> ResponsesResource:
        from .resources.responses import ResponsesResource

        return ResponsesResource(self)

    @cached_property
    def completions(self) -> CompletionsResource:
        from .resources.completions import CompletionsResource

        return CompletionsResource(self)

    @cached_property
    def chat(self) -> ChatResource:
        from .resources.chat import ChatResource

        return ChatResource(self)

    @cached_property
    def inference(self) -> InferenceResource:
        from .resources.inference import InferenceResource

        return InferenceResource(self)

    @cached_property
    def questions(self) -> QuestionsResource:
        from .resources.questions import QuestionsResource

        return QuestionsResource(self)

    @cached_property
    def files(self) -> FilesResource:
        from .resources.files import FilesResource

        return FilesResource(self)

    @cached_property
    def models(self) -> ModelsResource:
        from .resources.models import ModelsResource

        return ModelsResource(self)

    @cached_property
    def datasets(self) -> DatasetsResource:
        from .resources.datasets import DatasetsResource

        return DatasetsResource(self)

    @cached_property
    def dataset_items(self) -> DatasetItemsResource:
        from .resources.dataset_items import DatasetItemsResource

        return DatasetItemsResource(self)

    @cached_property
    def evaluations(self) -> EvaluationsResource:
        from .resources.evaluations import EvaluationsResource

        return EvaluationsResource(self)

    @cached_property
    def evaluation_items(self) -> EvaluationItemsResource:
        from .resources.evaluation_items import EvaluationItemsResource

        return EvaluationItemsResource(self)

    @cached_property
    def rubrics(self) -> RubricsResource:
        from .resources.rubrics import RubricsResource

        return RubricsResource(self)

    @cached_property
    def evaluation_groups(self) -> EvaluationGroupsResource:
        from .resources.evaluation_groups import EvaluationGroupsResource

        return EvaluationGroupsResource(self)

    @cached_property
    def evaluation_dashboards(self) -> EvaluationDashboardsResource:
        from .resources.evaluation_dashboards import EvaluationDashboardsResource

        return EvaluationDashboardsResource(self)

    @cached_property
    def spans(self) -> SpansResource:
        from .resources.spans import SpansResource

        return SpansResource(self)

    @cached_property
    def span_assessments(self) -> SpanAssessmentsResource:
        from .resources.span_assessments import SpanAssessmentsResource

        return SpanAssessmentsResource(self)

    @cached_property
    def credentials(self) -> CredentialsResource:
        from .resources.credentials import CredentialsResource

        return CredentialsResource(self)

    @cached_property
    def build(self) -> BuildResource:
        from .resources.build import BuildResource

        return BuildResource(self)

    @cached_property
    def deploy(self) -> DeployResource:
        from .resources.deploy import DeployResource

        return DeployResource(self)

    @cached_property
    def secrets(self) -> SecretsResource:
        from .resources.secrets import SecretsResource

        return SecretsResource(self)

    @cached_property
    def vector_stores(self) -> VectorStoresResource:
        from .resources.vector_stores import VectorStoresResource

        return VectorStoresResource(self)

    @cached_property
    def with_raw_response(self) -> SGPClientWithRawResponse:
        return SGPClientWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SGPClientWithStreamedResponse:
        return SGPClientWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"x-api-key": api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            "x-selected-account-id": self.account_id,
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        account_id: str | None = None,
        environment: Literal["production", "production-multitenant", "staging", "development", "local"] | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            account_id=account_id or self.account_id,
            base_url=base_url or self.base_url,
            environment=environment or self._environment,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncSGPClient(AsyncAPIClient):
    # client options
    api_key: str
    account_id: str

    _environment: Literal["production", "production-multitenant", "staging", "development", "local"] | NotGiven

    def __init__(
        self,
        *,
        api_key: str | None = None,
        account_id: str | None = None,
        environment: Literal["production", "production-multitenant", "staging", "development", "local"]
        | NotGiven = not_given,
        base_url: str | httpx.URL | None | NotGiven = not_given,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncSGPClient client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `SGP_API_KEY`
        - `account_id` from `SGP_ACCOUNT_ID`
        """
        if api_key is None:
            api_key = os.environ.get("SGP_API_KEY")
        if api_key is None:
            raise SGPClientError(
                "The api_key client option must be set either by passing api_key to the client or by setting the SGP_API_KEY environment variable"
            )
        self.api_key = api_key

        if account_id is None:
            account_id = os.environ.get("SGP_ACCOUNT_ID")
        if account_id is None:
            raise SGPClientError(
                "The account_id client option must be set either by passing account_id to the client or by setting the SGP_ACCOUNT_ID environment variable"
            )
        self.account_id = account_id

        self._environment = environment

        base_url_env = os.environ.get("SGP_CLIENT_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `SGP_CLIENT_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "production"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self._default_stream_cls = AsyncStream

    @cached_property
    def responses(self) -> AsyncResponsesResource:
        from .resources.responses import AsyncResponsesResource

        return AsyncResponsesResource(self)

    @cached_property
    def completions(self) -> AsyncCompletionsResource:
        from .resources.completions import AsyncCompletionsResource

        return AsyncCompletionsResource(self)

    @cached_property
    def chat(self) -> AsyncChatResource:
        from .resources.chat import AsyncChatResource

        return AsyncChatResource(self)

    @cached_property
    def inference(self) -> AsyncInferenceResource:
        from .resources.inference import AsyncInferenceResource

        return AsyncInferenceResource(self)

    @cached_property
    def questions(self) -> AsyncQuestionsResource:
        from .resources.questions import AsyncQuestionsResource

        return AsyncQuestionsResource(self)

    @cached_property
    def files(self) -> AsyncFilesResource:
        from .resources.files import AsyncFilesResource

        return AsyncFilesResource(self)

    @cached_property
    def models(self) -> AsyncModelsResource:
        from .resources.models import AsyncModelsResource

        return AsyncModelsResource(self)

    @cached_property
    def datasets(self) -> AsyncDatasetsResource:
        from .resources.datasets import AsyncDatasetsResource

        return AsyncDatasetsResource(self)

    @cached_property
    def dataset_items(self) -> AsyncDatasetItemsResource:
        from .resources.dataset_items import AsyncDatasetItemsResource

        return AsyncDatasetItemsResource(self)

    @cached_property
    def evaluations(self) -> AsyncEvaluationsResource:
        from .resources.evaluations import AsyncEvaluationsResource

        return AsyncEvaluationsResource(self)

    @cached_property
    def evaluation_items(self) -> AsyncEvaluationItemsResource:
        from .resources.evaluation_items import AsyncEvaluationItemsResource

        return AsyncEvaluationItemsResource(self)

    @cached_property
    def rubrics(self) -> AsyncRubricsResource:
        from .resources.rubrics import AsyncRubricsResource

        return AsyncRubricsResource(self)

    @cached_property
    def evaluation_groups(self) -> AsyncEvaluationGroupsResource:
        from .resources.evaluation_groups import AsyncEvaluationGroupsResource

        return AsyncEvaluationGroupsResource(self)

    @cached_property
    def evaluation_dashboards(self) -> AsyncEvaluationDashboardsResource:
        from .resources.evaluation_dashboards import AsyncEvaluationDashboardsResource

        return AsyncEvaluationDashboardsResource(self)

    @cached_property
    def spans(self) -> AsyncSpansResource:
        from .resources.spans import AsyncSpansResource

        return AsyncSpansResource(self)

    @cached_property
    def span_assessments(self) -> AsyncSpanAssessmentsResource:
        from .resources.span_assessments import AsyncSpanAssessmentsResource

        return AsyncSpanAssessmentsResource(self)

    @cached_property
    def credentials(self) -> AsyncCredentialsResource:
        from .resources.credentials import AsyncCredentialsResource

        return AsyncCredentialsResource(self)

    @cached_property
    def build(self) -> AsyncBuildResource:
        from .resources.build import AsyncBuildResource

        return AsyncBuildResource(self)

    @cached_property
    def deploy(self) -> AsyncDeployResource:
        from .resources.deploy import AsyncDeployResource

        return AsyncDeployResource(self)

    @cached_property
    def secrets(self) -> AsyncSecretsResource:
        from .resources.secrets import AsyncSecretsResource

        return AsyncSecretsResource(self)

    @cached_property
    def vector_stores(self) -> AsyncVectorStoresResource:
        from .resources.vector_stores import AsyncVectorStoresResource

        return AsyncVectorStoresResource(self)

    @cached_property
    def with_raw_response(self) -> AsyncSGPClientWithRawResponse:
        return AsyncSGPClientWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSGPClientWithStreamedResponse:
        return AsyncSGPClientWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"x-api-key": api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            "x-selected-account-id": self.account_id,
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        account_id: str | None = None,
        environment: Literal["production", "production-multitenant", "staging", "development", "local"] | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            account_id=account_id or self.account_id,
            base_url=base_url or self.base_url,
            environment=environment or self._environment,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class SGPClientWithRawResponse:
    _client: SGPClient

    def __init__(self, client: SGPClient) -> None:
        self._client = client

    @cached_property
    def responses(self) -> responses.ResponsesResourceWithRawResponse:
        from .resources.responses import ResponsesResourceWithRawResponse

        return ResponsesResourceWithRawResponse(self._client.responses)

    @cached_property
    def completions(self) -> completions.CompletionsResourceWithRawResponse:
        from .resources.completions import CompletionsResourceWithRawResponse

        return CompletionsResourceWithRawResponse(self._client.completions)

    @cached_property
    def chat(self) -> chat.ChatResourceWithRawResponse:
        from .resources.chat import ChatResourceWithRawResponse

        return ChatResourceWithRawResponse(self._client.chat)

    @cached_property
    def inference(self) -> inference.InferenceResourceWithRawResponse:
        from .resources.inference import InferenceResourceWithRawResponse

        return InferenceResourceWithRawResponse(self._client.inference)

    @cached_property
    def questions(self) -> questions.QuestionsResourceWithRawResponse:
        from .resources.questions import QuestionsResourceWithRawResponse

        return QuestionsResourceWithRawResponse(self._client.questions)

    @cached_property
    def files(self) -> files.FilesResourceWithRawResponse:
        from .resources.files import FilesResourceWithRawResponse

        return FilesResourceWithRawResponse(self._client.files)

    @cached_property
    def models(self) -> models.ModelsResourceWithRawResponse:
        from .resources.models import ModelsResourceWithRawResponse

        return ModelsResourceWithRawResponse(self._client.models)

    @cached_property
    def datasets(self) -> datasets.DatasetsResourceWithRawResponse:
        from .resources.datasets import DatasetsResourceWithRawResponse

        return DatasetsResourceWithRawResponse(self._client.datasets)

    @cached_property
    def dataset_items(self) -> dataset_items.DatasetItemsResourceWithRawResponse:
        from .resources.dataset_items import DatasetItemsResourceWithRawResponse

        return DatasetItemsResourceWithRawResponse(self._client.dataset_items)

    @cached_property
    def evaluations(self) -> evaluations.EvaluationsResourceWithRawResponse:
        from .resources.evaluations import EvaluationsResourceWithRawResponse

        return EvaluationsResourceWithRawResponse(self._client.evaluations)

    @cached_property
    def evaluation_items(self) -> evaluation_items.EvaluationItemsResourceWithRawResponse:
        from .resources.evaluation_items import EvaluationItemsResourceWithRawResponse

        return EvaluationItemsResourceWithRawResponse(self._client.evaluation_items)

    @cached_property
    def rubrics(self) -> rubrics.RubricsResourceWithRawResponse:
        from .resources.rubrics import RubricsResourceWithRawResponse

        return RubricsResourceWithRawResponse(self._client.rubrics)

    @cached_property
    def evaluation_groups(self) -> evaluation_groups.EvaluationGroupsResourceWithRawResponse:
        from .resources.evaluation_groups import EvaluationGroupsResourceWithRawResponse

        return EvaluationGroupsResourceWithRawResponse(self._client.evaluation_groups)

    @cached_property
    def evaluation_dashboards(self) -> evaluation_dashboards.EvaluationDashboardsResourceWithRawResponse:
        from .resources.evaluation_dashboards import EvaluationDashboardsResourceWithRawResponse

        return EvaluationDashboardsResourceWithRawResponse(self._client.evaluation_dashboards)

    @cached_property
    def spans(self) -> spans.SpansResourceWithRawResponse:
        from .resources.spans import SpansResourceWithRawResponse

        return SpansResourceWithRawResponse(self._client.spans)

    @cached_property
    def span_assessments(self) -> span_assessments.SpanAssessmentsResourceWithRawResponse:
        from .resources.span_assessments import SpanAssessmentsResourceWithRawResponse

        return SpanAssessmentsResourceWithRawResponse(self._client.span_assessments)

    @cached_property
    def credentials(self) -> credentials.CredentialsResourceWithRawResponse:
        from .resources.credentials import CredentialsResourceWithRawResponse

        return CredentialsResourceWithRawResponse(self._client.credentials)

    @cached_property
    def build(self) -> build.BuildResourceWithRawResponse:
        from .resources.build import BuildResourceWithRawResponse

        return BuildResourceWithRawResponse(self._client.build)

    @cached_property
    def deploy(self) -> deploy.DeployResourceWithRawResponse:
        from .resources.deploy import DeployResourceWithRawResponse

        return DeployResourceWithRawResponse(self._client.deploy)

    @cached_property
    def secrets(self) -> secrets.SecretsResourceWithRawResponse:
        from .resources.secrets import SecretsResourceWithRawResponse

        return SecretsResourceWithRawResponse(self._client.secrets)

    @cached_property
    def vector_stores(self) -> vector_stores.VectorStoresResourceWithRawResponse:
        from .resources.vector_stores import VectorStoresResourceWithRawResponse

        return VectorStoresResourceWithRawResponse(self._client.vector_stores)


class AsyncSGPClientWithRawResponse:
    _client: AsyncSGPClient

    def __init__(self, client: AsyncSGPClient) -> None:
        self._client = client

    @cached_property
    def responses(self) -> responses.AsyncResponsesResourceWithRawResponse:
        from .resources.responses import AsyncResponsesResourceWithRawResponse

        return AsyncResponsesResourceWithRawResponse(self._client.responses)

    @cached_property
    def completions(self) -> completions.AsyncCompletionsResourceWithRawResponse:
        from .resources.completions import AsyncCompletionsResourceWithRawResponse

        return AsyncCompletionsResourceWithRawResponse(self._client.completions)

    @cached_property
    def chat(self) -> chat.AsyncChatResourceWithRawResponse:
        from .resources.chat import AsyncChatResourceWithRawResponse

        return AsyncChatResourceWithRawResponse(self._client.chat)

    @cached_property
    def inference(self) -> inference.AsyncInferenceResourceWithRawResponse:
        from .resources.inference import AsyncInferenceResourceWithRawResponse

        return AsyncInferenceResourceWithRawResponse(self._client.inference)

    @cached_property
    def questions(self) -> questions.AsyncQuestionsResourceWithRawResponse:
        from .resources.questions import AsyncQuestionsResourceWithRawResponse

        return AsyncQuestionsResourceWithRawResponse(self._client.questions)

    @cached_property
    def files(self) -> files.AsyncFilesResourceWithRawResponse:
        from .resources.files import AsyncFilesResourceWithRawResponse

        return AsyncFilesResourceWithRawResponse(self._client.files)

    @cached_property
    def models(self) -> models.AsyncModelsResourceWithRawResponse:
        from .resources.models import AsyncModelsResourceWithRawResponse

        return AsyncModelsResourceWithRawResponse(self._client.models)

    @cached_property
    def datasets(self) -> datasets.AsyncDatasetsResourceWithRawResponse:
        from .resources.datasets import AsyncDatasetsResourceWithRawResponse

        return AsyncDatasetsResourceWithRawResponse(self._client.datasets)

    @cached_property
    def dataset_items(self) -> dataset_items.AsyncDatasetItemsResourceWithRawResponse:
        from .resources.dataset_items import AsyncDatasetItemsResourceWithRawResponse

        return AsyncDatasetItemsResourceWithRawResponse(self._client.dataset_items)

    @cached_property
    def evaluations(self) -> evaluations.AsyncEvaluationsResourceWithRawResponse:
        from .resources.evaluations import AsyncEvaluationsResourceWithRawResponse

        return AsyncEvaluationsResourceWithRawResponse(self._client.evaluations)

    @cached_property
    def evaluation_items(self) -> evaluation_items.AsyncEvaluationItemsResourceWithRawResponse:
        from .resources.evaluation_items import AsyncEvaluationItemsResourceWithRawResponse

        return AsyncEvaluationItemsResourceWithRawResponse(self._client.evaluation_items)

    @cached_property
    def rubrics(self) -> rubrics.AsyncRubricsResourceWithRawResponse:
        from .resources.rubrics import AsyncRubricsResourceWithRawResponse

        return AsyncRubricsResourceWithRawResponse(self._client.rubrics)

    @cached_property
    def evaluation_groups(self) -> evaluation_groups.AsyncEvaluationGroupsResourceWithRawResponse:
        from .resources.evaluation_groups import AsyncEvaluationGroupsResourceWithRawResponse

        return AsyncEvaluationGroupsResourceWithRawResponse(self._client.evaluation_groups)

    @cached_property
    def evaluation_dashboards(self) -> evaluation_dashboards.AsyncEvaluationDashboardsResourceWithRawResponse:
        from .resources.evaluation_dashboards import AsyncEvaluationDashboardsResourceWithRawResponse

        return AsyncEvaluationDashboardsResourceWithRawResponse(self._client.evaluation_dashboards)

    @cached_property
    def spans(self) -> spans.AsyncSpansResourceWithRawResponse:
        from .resources.spans import AsyncSpansResourceWithRawResponse

        return AsyncSpansResourceWithRawResponse(self._client.spans)

    @cached_property
    def span_assessments(self) -> span_assessments.AsyncSpanAssessmentsResourceWithRawResponse:
        from .resources.span_assessments import AsyncSpanAssessmentsResourceWithRawResponse

        return AsyncSpanAssessmentsResourceWithRawResponse(self._client.span_assessments)

    @cached_property
    def credentials(self) -> credentials.AsyncCredentialsResourceWithRawResponse:
        from .resources.credentials import AsyncCredentialsResourceWithRawResponse

        return AsyncCredentialsResourceWithRawResponse(self._client.credentials)

    @cached_property
    def build(self) -> build.AsyncBuildResourceWithRawResponse:
        from .resources.build import AsyncBuildResourceWithRawResponse

        return AsyncBuildResourceWithRawResponse(self._client.build)

    @cached_property
    def deploy(self) -> deploy.AsyncDeployResourceWithRawResponse:
        from .resources.deploy import AsyncDeployResourceWithRawResponse

        return AsyncDeployResourceWithRawResponse(self._client.deploy)

    @cached_property
    def secrets(self) -> secrets.AsyncSecretsResourceWithRawResponse:
        from .resources.secrets import AsyncSecretsResourceWithRawResponse

        return AsyncSecretsResourceWithRawResponse(self._client.secrets)

    @cached_property
    def vector_stores(self) -> vector_stores.AsyncVectorStoresResourceWithRawResponse:
        from .resources.vector_stores import AsyncVectorStoresResourceWithRawResponse

        return AsyncVectorStoresResourceWithRawResponse(self._client.vector_stores)


class SGPClientWithStreamedResponse:
    _client: SGPClient

    def __init__(self, client: SGPClient) -> None:
        self._client = client

    @cached_property
    def responses(self) -> responses.ResponsesResourceWithStreamingResponse:
        from .resources.responses import ResponsesResourceWithStreamingResponse

        return ResponsesResourceWithStreamingResponse(self._client.responses)

    @cached_property
    def completions(self) -> completions.CompletionsResourceWithStreamingResponse:
        from .resources.completions import CompletionsResourceWithStreamingResponse

        return CompletionsResourceWithStreamingResponse(self._client.completions)

    @cached_property
    def chat(self) -> chat.ChatResourceWithStreamingResponse:
        from .resources.chat import ChatResourceWithStreamingResponse

        return ChatResourceWithStreamingResponse(self._client.chat)

    @cached_property
    def inference(self) -> inference.InferenceResourceWithStreamingResponse:
        from .resources.inference import InferenceResourceWithStreamingResponse

        return InferenceResourceWithStreamingResponse(self._client.inference)

    @cached_property
    def questions(self) -> questions.QuestionsResourceWithStreamingResponse:
        from .resources.questions import QuestionsResourceWithStreamingResponse

        return QuestionsResourceWithStreamingResponse(self._client.questions)

    @cached_property
    def files(self) -> files.FilesResourceWithStreamingResponse:
        from .resources.files import FilesResourceWithStreamingResponse

        return FilesResourceWithStreamingResponse(self._client.files)

    @cached_property
    def models(self) -> models.ModelsResourceWithStreamingResponse:
        from .resources.models import ModelsResourceWithStreamingResponse

        return ModelsResourceWithStreamingResponse(self._client.models)

    @cached_property
    def datasets(self) -> datasets.DatasetsResourceWithStreamingResponse:
        from .resources.datasets import DatasetsResourceWithStreamingResponse

        return DatasetsResourceWithStreamingResponse(self._client.datasets)

    @cached_property
    def dataset_items(self) -> dataset_items.DatasetItemsResourceWithStreamingResponse:
        from .resources.dataset_items import DatasetItemsResourceWithStreamingResponse

        return DatasetItemsResourceWithStreamingResponse(self._client.dataset_items)

    @cached_property
    def evaluations(self) -> evaluations.EvaluationsResourceWithStreamingResponse:
        from .resources.evaluations import EvaluationsResourceWithStreamingResponse

        return EvaluationsResourceWithStreamingResponse(self._client.evaluations)

    @cached_property
    def evaluation_items(self) -> evaluation_items.EvaluationItemsResourceWithStreamingResponse:
        from .resources.evaluation_items import EvaluationItemsResourceWithStreamingResponse

        return EvaluationItemsResourceWithStreamingResponse(self._client.evaluation_items)

    @cached_property
    def rubrics(self) -> rubrics.RubricsResourceWithStreamingResponse:
        from .resources.rubrics import RubricsResourceWithStreamingResponse

        return RubricsResourceWithStreamingResponse(self._client.rubrics)

    @cached_property
    def evaluation_groups(self) -> evaluation_groups.EvaluationGroupsResourceWithStreamingResponse:
        from .resources.evaluation_groups import EvaluationGroupsResourceWithStreamingResponse

        return EvaluationGroupsResourceWithStreamingResponse(self._client.evaluation_groups)

    @cached_property
    def evaluation_dashboards(self) -> evaluation_dashboards.EvaluationDashboardsResourceWithStreamingResponse:
        from .resources.evaluation_dashboards import EvaluationDashboardsResourceWithStreamingResponse

        return EvaluationDashboardsResourceWithStreamingResponse(self._client.evaluation_dashboards)

    @cached_property
    def spans(self) -> spans.SpansResourceWithStreamingResponse:
        from .resources.spans import SpansResourceWithStreamingResponse

        return SpansResourceWithStreamingResponse(self._client.spans)

    @cached_property
    def span_assessments(self) -> span_assessments.SpanAssessmentsResourceWithStreamingResponse:
        from .resources.span_assessments import SpanAssessmentsResourceWithStreamingResponse

        return SpanAssessmentsResourceWithStreamingResponse(self._client.span_assessments)

    @cached_property
    def credentials(self) -> credentials.CredentialsResourceWithStreamingResponse:
        from .resources.credentials import CredentialsResourceWithStreamingResponse

        return CredentialsResourceWithStreamingResponse(self._client.credentials)

    @cached_property
    def build(self) -> build.BuildResourceWithStreamingResponse:
        from .resources.build import BuildResourceWithStreamingResponse

        return BuildResourceWithStreamingResponse(self._client.build)

    @cached_property
    def deploy(self) -> deploy.DeployResourceWithStreamingResponse:
        from .resources.deploy import DeployResourceWithStreamingResponse

        return DeployResourceWithStreamingResponse(self._client.deploy)

    @cached_property
    def secrets(self) -> secrets.SecretsResourceWithStreamingResponse:
        from .resources.secrets import SecretsResourceWithStreamingResponse

        return SecretsResourceWithStreamingResponse(self._client.secrets)

    @cached_property
    def vector_stores(self) -> vector_stores.VectorStoresResourceWithStreamingResponse:
        from .resources.vector_stores import VectorStoresResourceWithStreamingResponse

        return VectorStoresResourceWithStreamingResponse(self._client.vector_stores)


class AsyncSGPClientWithStreamedResponse:
    _client: AsyncSGPClient

    def __init__(self, client: AsyncSGPClient) -> None:
        self._client = client

    @cached_property
    def responses(self) -> responses.AsyncResponsesResourceWithStreamingResponse:
        from .resources.responses import AsyncResponsesResourceWithStreamingResponse

        return AsyncResponsesResourceWithStreamingResponse(self._client.responses)

    @cached_property
    def completions(self) -> completions.AsyncCompletionsResourceWithStreamingResponse:
        from .resources.completions import AsyncCompletionsResourceWithStreamingResponse

        return AsyncCompletionsResourceWithStreamingResponse(self._client.completions)

    @cached_property
    def chat(self) -> chat.AsyncChatResourceWithStreamingResponse:
        from .resources.chat import AsyncChatResourceWithStreamingResponse

        return AsyncChatResourceWithStreamingResponse(self._client.chat)

    @cached_property
    def inference(self) -> inference.AsyncInferenceResourceWithStreamingResponse:
        from .resources.inference import AsyncInferenceResourceWithStreamingResponse

        return AsyncInferenceResourceWithStreamingResponse(self._client.inference)

    @cached_property
    def questions(self) -> questions.AsyncQuestionsResourceWithStreamingResponse:
        from .resources.questions import AsyncQuestionsResourceWithStreamingResponse

        return AsyncQuestionsResourceWithStreamingResponse(self._client.questions)

    @cached_property
    def files(self) -> files.AsyncFilesResourceWithStreamingResponse:
        from .resources.files import AsyncFilesResourceWithStreamingResponse

        return AsyncFilesResourceWithStreamingResponse(self._client.files)

    @cached_property
    def models(self) -> models.AsyncModelsResourceWithStreamingResponse:
        from .resources.models import AsyncModelsResourceWithStreamingResponse

        return AsyncModelsResourceWithStreamingResponse(self._client.models)

    @cached_property
    def datasets(self) -> datasets.AsyncDatasetsResourceWithStreamingResponse:
        from .resources.datasets import AsyncDatasetsResourceWithStreamingResponse

        return AsyncDatasetsResourceWithStreamingResponse(self._client.datasets)

    @cached_property
    def dataset_items(self) -> dataset_items.AsyncDatasetItemsResourceWithStreamingResponse:
        from .resources.dataset_items import AsyncDatasetItemsResourceWithStreamingResponse

        return AsyncDatasetItemsResourceWithStreamingResponse(self._client.dataset_items)

    @cached_property
    def evaluations(self) -> evaluations.AsyncEvaluationsResourceWithStreamingResponse:
        from .resources.evaluations import AsyncEvaluationsResourceWithStreamingResponse

        return AsyncEvaluationsResourceWithStreamingResponse(self._client.evaluations)

    @cached_property
    def evaluation_items(self) -> evaluation_items.AsyncEvaluationItemsResourceWithStreamingResponse:
        from .resources.evaluation_items import AsyncEvaluationItemsResourceWithStreamingResponse

        return AsyncEvaluationItemsResourceWithStreamingResponse(self._client.evaluation_items)

    @cached_property
    def rubrics(self) -> rubrics.AsyncRubricsResourceWithStreamingResponse:
        from .resources.rubrics import AsyncRubricsResourceWithStreamingResponse

        return AsyncRubricsResourceWithStreamingResponse(self._client.rubrics)

    @cached_property
    def evaluation_groups(self) -> evaluation_groups.AsyncEvaluationGroupsResourceWithStreamingResponse:
        from .resources.evaluation_groups import AsyncEvaluationGroupsResourceWithStreamingResponse

        return AsyncEvaluationGroupsResourceWithStreamingResponse(self._client.evaluation_groups)

    @cached_property
    def evaluation_dashboards(self) -> evaluation_dashboards.AsyncEvaluationDashboardsResourceWithStreamingResponse:
        from .resources.evaluation_dashboards import AsyncEvaluationDashboardsResourceWithStreamingResponse

        return AsyncEvaluationDashboardsResourceWithStreamingResponse(self._client.evaluation_dashboards)

    @cached_property
    def spans(self) -> spans.AsyncSpansResourceWithStreamingResponse:
        from .resources.spans import AsyncSpansResourceWithStreamingResponse

        return AsyncSpansResourceWithStreamingResponse(self._client.spans)

    @cached_property
    def span_assessments(self) -> span_assessments.AsyncSpanAssessmentsResourceWithStreamingResponse:
        from .resources.span_assessments import AsyncSpanAssessmentsResourceWithStreamingResponse

        return AsyncSpanAssessmentsResourceWithStreamingResponse(self._client.span_assessments)

    @cached_property
    def credentials(self) -> credentials.AsyncCredentialsResourceWithStreamingResponse:
        from .resources.credentials import AsyncCredentialsResourceWithStreamingResponse

        return AsyncCredentialsResourceWithStreamingResponse(self._client.credentials)

    @cached_property
    def build(self) -> build.AsyncBuildResourceWithStreamingResponse:
        from .resources.build import AsyncBuildResourceWithStreamingResponse

        return AsyncBuildResourceWithStreamingResponse(self._client.build)

    @cached_property
    def deploy(self) -> deploy.AsyncDeployResourceWithStreamingResponse:
        from .resources.deploy import AsyncDeployResourceWithStreamingResponse

        return AsyncDeployResourceWithStreamingResponse(self._client.deploy)

    @cached_property
    def secrets(self) -> secrets.AsyncSecretsResourceWithStreamingResponse:
        from .resources.secrets import AsyncSecretsResourceWithStreamingResponse

        return AsyncSecretsResourceWithStreamingResponse(self._client.secrets)

    @cached_property
    def vector_stores(self) -> vector_stores.AsyncVectorStoresResourceWithStreamingResponse:
        from .resources.vector_stores import AsyncVectorStoresResourceWithStreamingResponse

        return AsyncVectorStoresResourceWithStreamingResponse(self._client.vector_stores)


Client = SGPClient

AsyncClient = AsyncSGPClient
