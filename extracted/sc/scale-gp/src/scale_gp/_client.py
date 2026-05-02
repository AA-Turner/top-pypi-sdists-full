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
        beta,
        alias,
        users,
        agents,
        chunks,
        models,
        themes,
        accounts,
        questions,
        completions,
        evaluations,
        applications,
        chat_threads,
        interactions,
        model_groups,
        model_servers,
        question_sets,
        knowledge_bases,
        model_templates,
        studio_projects,
        chat_completions,
        fine_tuning_jobs,
        application_specs,
        training_datasets,
        evaluation_configs,
        application_schemas,
        application_threads,
        deployment_packages,
        evaluation_datasets,
        application_variants,
        application_deployments,
        application_variant_reports,
        knowledge_base_data_sources,
        application_test_case_outputs,
    )
    from .resources.alias import AliasResource, AsyncAliasResource
    from .resources.users import UsersResource, AsyncUsersResource
    from .resources.agents import AgentsResource, AsyncAgentsResource
    from .resources.chunks import ChunksResource, AsyncChunksResource
    from .resources.themes import ThemesResource, AsyncThemesResource
    from .resources.accounts import AccountsResource, AsyncAccountsResource
    from .resources.beta.beta import BetaResource, AsyncBetaResource
    from .resources.questions import QuestionsResource, AsyncQuestionsResource
    from .resources.completions import CompletionsResource, AsyncCompletionsResource
    from .resources.interactions import InteractionsResource, AsyncInteractionsResource
    from .resources.models.models import ModelsResource, AsyncModelsResource
    from .resources.question_sets import QuestionSetsResource, AsyncQuestionSetsResource
    from .resources.model_templates import ModelTemplatesResource, AsyncModelTemplatesResource
    from .resources.studio_projects import StudioProjectsResource, AsyncStudioProjectsResource
    from .resources.chat_completions import ChatCompletionsResource, AsyncChatCompletionsResource
    from .resources.application_specs import ApplicationSpecsResource, AsyncApplicationSpecsResource
    from .resources.evaluation_configs import EvaluationConfigsResource, AsyncEvaluationConfigsResource
    from .resources.application_schemas import ApplicationSchemasResource, AsyncApplicationSchemasResource
    from .resources.application_threads import ApplicationThreadsResource, AsyncApplicationThreadsResource
    from .resources.deployment_packages import DeploymentPackagesResource, AsyncDeploymentPackagesResource
    from .resources.application_variants import ApplicationVariantsResource, AsyncApplicationVariantsResource
    from .resources.application_deployments import ApplicationDeploymentsResource, AsyncApplicationDeploymentsResource
    from .resources.evaluations.evaluations import EvaluationsResource, AsyncEvaluationsResource
    from .resources.applications.applications import ApplicationsResource, AsyncApplicationsResource
    from .resources.chat_threads.chat_threads import ChatThreadsResource, AsyncChatThreadsResource
    from .resources.model_groups.model_groups import ModelGroupsResource, AsyncModelGroupsResource
    from .resources.application_variant_reports import (
        ApplicationVariantReportsResource,
        AsyncApplicationVariantReportsResource,
    )
    from .resources.knowledge_base_data_sources import (
        KnowledgeBaseDataSourcesResource,
        AsyncKnowledgeBaseDataSourcesResource,
    )
    from .resources.model_servers.model_servers import ModelServersResource, AsyncModelServersResource
    from .resources.application_test_case_outputs import (
        ApplicationTestCaseOutputsResource,
        AsyncApplicationTestCaseOutputsResource,
    )
    from .resources.knowledge_bases.knowledge_bases import KnowledgeBasesResource, AsyncKnowledgeBasesResource
    from .resources.fine_tuning_jobs.fine_tuning_jobs import FineTuningJobsResource, AsyncFineTuningJobsResource
    from .resources.training_datasets.training_datasets import TrainingDatasetsResource, AsyncTrainingDatasetsResource
    from .resources.evaluation_datasets.evaluation_datasets import (
        EvaluationDatasetsResource,
        AsyncEvaluationDatasetsResource,
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
    "development": "http://127.0.0.1:5003/public",
}


class SGPClient(SyncAPIClient):
    # client options
    api_key: str
    account_id: str | None

    _environment: Literal["production", "development"] | NotGiven

    def __init__(
        self,
        *,
        api_key: str | None = None,
        account_id: str | None = None,
        environment: Literal["production", "development"] | NotGiven = not_given,
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
    def knowledge_bases(self) -> KnowledgeBasesResource:
        from .resources.knowledge_bases import KnowledgeBasesResource

        return KnowledgeBasesResource(self)

    @cached_property
    def knowledge_base_data_sources(self) -> KnowledgeBaseDataSourcesResource:
        from .resources.knowledge_base_data_sources import KnowledgeBaseDataSourcesResource

        return KnowledgeBaseDataSourcesResource(self)

    @cached_property
    def chunks(self) -> ChunksResource:
        from .resources.chunks import ChunksResource

        return ChunksResource(self)

    @cached_property
    def agents(self) -> AgentsResource:
        from .resources.agents import AgentsResource

        return AgentsResource(self)

    @cached_property
    def completions(self) -> CompletionsResource:
        from .resources.completions import CompletionsResource

        return CompletionsResource(self)

    @cached_property
    def chat_completions(self) -> ChatCompletionsResource:
        from .resources.chat_completions import ChatCompletionsResource

        return ChatCompletionsResource(self)

    @cached_property
    def models(self) -> ModelsResource:
        from .resources.models import ModelsResource

        return ModelsResource(self)

    @cached_property
    def model_groups(self) -> ModelGroupsResource:
        from .resources.model_groups import ModelGroupsResource

        return ModelGroupsResource(self)

    @cached_property
    def users(self) -> UsersResource:
        from .resources.users import UsersResource

        return UsersResource(self)

    @cached_property
    def accounts(self) -> AccountsResource:
        from .resources.accounts import AccountsResource

        return AccountsResource(self)

    @cached_property
    def question_sets(self) -> QuestionSetsResource:
        from .resources.question_sets import QuestionSetsResource

        return QuestionSetsResource(self)

    @cached_property
    def evaluations(self) -> EvaluationsResource:
        from .resources.evaluations import EvaluationsResource

        return EvaluationsResource(self)

    @cached_property
    def evaluation_configs(self) -> EvaluationConfigsResource:
        from .resources.evaluation_configs import EvaluationConfigsResource

        return EvaluationConfigsResource(self)

    @cached_property
    def evaluation_datasets(self) -> EvaluationDatasetsResource:
        from .resources.evaluation_datasets import EvaluationDatasetsResource

        return EvaluationDatasetsResource(self)

    @cached_property
    def studio_projects(self) -> StudioProjectsResource:
        from .resources.studio_projects import StudioProjectsResource

        return StudioProjectsResource(self)

    @cached_property
    def application_specs(self) -> ApplicationSpecsResource:
        from .resources.application_specs import ApplicationSpecsResource

        return ApplicationSpecsResource(self)

    @cached_property
    def questions(self) -> QuestionsResource:
        from .resources.questions import QuestionsResource

        return QuestionsResource(self)

    @cached_property
    def model_templates(self) -> ModelTemplatesResource:
        from .resources.model_templates import ModelTemplatesResource

        return ModelTemplatesResource(self)

    @cached_property
    def fine_tuning_jobs(self) -> FineTuningJobsResource:
        from .resources.fine_tuning_jobs import FineTuningJobsResource

        return FineTuningJobsResource(self)

    @cached_property
    def training_datasets(self) -> TrainingDatasetsResource:
        from .resources.training_datasets import TrainingDatasetsResource

        return TrainingDatasetsResource(self)

    @cached_property
    def deployment_packages(self) -> DeploymentPackagesResource:
        from .resources.deployment_packages import DeploymentPackagesResource

        return DeploymentPackagesResource(self)

    @cached_property
    def application_variants(self) -> ApplicationVariantsResource:
        from .resources.application_variants import ApplicationVariantsResource

        return ApplicationVariantsResource(self)

    @cached_property
    def application_deployments(self) -> ApplicationDeploymentsResource:
        from .resources.application_deployments import ApplicationDeploymentsResource

        return ApplicationDeploymentsResource(self)

    @cached_property
    def application_variant_reports(self) -> ApplicationVariantReportsResource:
        from .resources.application_variant_reports import ApplicationVariantReportsResource

        return ApplicationVariantReportsResource(self)

    @cached_property
    def application_test_case_outputs(self) -> ApplicationTestCaseOutputsResource:
        from .resources.application_test_case_outputs import ApplicationTestCaseOutputsResource

        return ApplicationTestCaseOutputsResource(self)

    @cached_property
    def application_schemas(self) -> ApplicationSchemasResource:
        from .resources.application_schemas import ApplicationSchemasResource

        return ApplicationSchemasResource(self)

    @cached_property
    def interactions(self) -> InteractionsResource:
        from .resources.interactions import InteractionsResource

        return InteractionsResource(self)

    @cached_property
    def applications(self) -> ApplicationsResource:
        from .resources.applications import ApplicationsResource

        return ApplicationsResource(self)

    @cached_property
    def application_threads(self) -> ApplicationThreadsResource:
        from .resources.application_threads import ApplicationThreadsResource

        return ApplicationThreadsResource(self)

    @cached_property
    def chat_threads(self) -> ChatThreadsResource:
        from .resources.chat_threads import ChatThreadsResource

        return ChatThreadsResource(self)

    @cached_property
    def themes(self) -> ThemesResource:
        from .resources.themes import ThemesResource

        return ThemesResource(self)

    @cached_property
    def beta(self) -> BetaResource:
        from .resources.beta import BetaResource

        return BetaResource(self)

    @cached_property
    def model_servers(self) -> ModelServersResource:
        from .resources.model_servers import ModelServersResource

        return ModelServersResource(self)

    @cached_property
    def alias(self) -> AliasResource:
        from .resources.alias import AliasResource

        return AliasResource(self)

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
            "x-selected-account-id": self.account_id if self.account_id is not None else Omit(),
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        account_id: str | None = None,
        environment: Literal["production", "development"] | None = None,
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
    account_id: str | None

    _environment: Literal["production", "development"] | NotGiven

    def __init__(
        self,
        *,
        api_key: str | None = None,
        account_id: str | None = None,
        environment: Literal["production", "development"] | NotGiven = not_given,
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
    def knowledge_bases(self) -> AsyncKnowledgeBasesResource:
        from .resources.knowledge_bases import AsyncKnowledgeBasesResource

        return AsyncKnowledgeBasesResource(self)

    @cached_property
    def knowledge_base_data_sources(self) -> AsyncKnowledgeBaseDataSourcesResource:
        from .resources.knowledge_base_data_sources import AsyncKnowledgeBaseDataSourcesResource

        return AsyncKnowledgeBaseDataSourcesResource(self)

    @cached_property
    def chunks(self) -> AsyncChunksResource:
        from .resources.chunks import AsyncChunksResource

        return AsyncChunksResource(self)

    @cached_property
    def agents(self) -> AsyncAgentsResource:
        from .resources.agents import AsyncAgentsResource

        return AsyncAgentsResource(self)

    @cached_property
    def completions(self) -> AsyncCompletionsResource:
        from .resources.completions import AsyncCompletionsResource

        return AsyncCompletionsResource(self)

    @cached_property
    def chat_completions(self) -> AsyncChatCompletionsResource:
        from .resources.chat_completions import AsyncChatCompletionsResource

        return AsyncChatCompletionsResource(self)

    @cached_property
    def models(self) -> AsyncModelsResource:
        from .resources.models import AsyncModelsResource

        return AsyncModelsResource(self)

    @cached_property
    def model_groups(self) -> AsyncModelGroupsResource:
        from .resources.model_groups import AsyncModelGroupsResource

        return AsyncModelGroupsResource(self)

    @cached_property
    def users(self) -> AsyncUsersResource:
        from .resources.users import AsyncUsersResource

        return AsyncUsersResource(self)

    @cached_property
    def accounts(self) -> AsyncAccountsResource:
        from .resources.accounts import AsyncAccountsResource

        return AsyncAccountsResource(self)

    @cached_property
    def question_sets(self) -> AsyncQuestionSetsResource:
        from .resources.question_sets import AsyncQuestionSetsResource

        return AsyncQuestionSetsResource(self)

    @cached_property
    def evaluations(self) -> AsyncEvaluationsResource:
        from .resources.evaluations import AsyncEvaluationsResource

        return AsyncEvaluationsResource(self)

    @cached_property
    def evaluation_configs(self) -> AsyncEvaluationConfigsResource:
        from .resources.evaluation_configs import AsyncEvaluationConfigsResource

        return AsyncEvaluationConfigsResource(self)

    @cached_property
    def evaluation_datasets(self) -> AsyncEvaluationDatasetsResource:
        from .resources.evaluation_datasets import AsyncEvaluationDatasetsResource

        return AsyncEvaluationDatasetsResource(self)

    @cached_property
    def studio_projects(self) -> AsyncStudioProjectsResource:
        from .resources.studio_projects import AsyncStudioProjectsResource

        return AsyncStudioProjectsResource(self)

    @cached_property
    def application_specs(self) -> AsyncApplicationSpecsResource:
        from .resources.application_specs import AsyncApplicationSpecsResource

        return AsyncApplicationSpecsResource(self)

    @cached_property
    def questions(self) -> AsyncQuestionsResource:
        from .resources.questions import AsyncQuestionsResource

        return AsyncQuestionsResource(self)

    @cached_property
    def model_templates(self) -> AsyncModelTemplatesResource:
        from .resources.model_templates import AsyncModelTemplatesResource

        return AsyncModelTemplatesResource(self)

    @cached_property
    def fine_tuning_jobs(self) -> AsyncFineTuningJobsResource:
        from .resources.fine_tuning_jobs import AsyncFineTuningJobsResource

        return AsyncFineTuningJobsResource(self)

    @cached_property
    def training_datasets(self) -> AsyncTrainingDatasetsResource:
        from .resources.training_datasets import AsyncTrainingDatasetsResource

        return AsyncTrainingDatasetsResource(self)

    @cached_property
    def deployment_packages(self) -> AsyncDeploymentPackagesResource:
        from .resources.deployment_packages import AsyncDeploymentPackagesResource

        return AsyncDeploymentPackagesResource(self)

    @cached_property
    def application_variants(self) -> AsyncApplicationVariantsResource:
        from .resources.application_variants import AsyncApplicationVariantsResource

        return AsyncApplicationVariantsResource(self)

    @cached_property
    def application_deployments(self) -> AsyncApplicationDeploymentsResource:
        from .resources.application_deployments import AsyncApplicationDeploymentsResource

        return AsyncApplicationDeploymentsResource(self)

    @cached_property
    def application_variant_reports(self) -> AsyncApplicationVariantReportsResource:
        from .resources.application_variant_reports import AsyncApplicationVariantReportsResource

        return AsyncApplicationVariantReportsResource(self)

    @cached_property
    def application_test_case_outputs(self) -> AsyncApplicationTestCaseOutputsResource:
        from .resources.application_test_case_outputs import AsyncApplicationTestCaseOutputsResource

        return AsyncApplicationTestCaseOutputsResource(self)

    @cached_property
    def application_schemas(self) -> AsyncApplicationSchemasResource:
        from .resources.application_schemas import AsyncApplicationSchemasResource

        return AsyncApplicationSchemasResource(self)

    @cached_property
    def interactions(self) -> AsyncInteractionsResource:
        from .resources.interactions import AsyncInteractionsResource

        return AsyncInteractionsResource(self)

    @cached_property
    def applications(self) -> AsyncApplicationsResource:
        from .resources.applications import AsyncApplicationsResource

        return AsyncApplicationsResource(self)

    @cached_property
    def application_threads(self) -> AsyncApplicationThreadsResource:
        from .resources.application_threads import AsyncApplicationThreadsResource

        return AsyncApplicationThreadsResource(self)

    @cached_property
    def chat_threads(self) -> AsyncChatThreadsResource:
        from .resources.chat_threads import AsyncChatThreadsResource

        return AsyncChatThreadsResource(self)

    @cached_property
    def themes(self) -> AsyncThemesResource:
        from .resources.themes import AsyncThemesResource

        return AsyncThemesResource(self)

    @cached_property
    def beta(self) -> AsyncBetaResource:
        from .resources.beta import AsyncBetaResource

        return AsyncBetaResource(self)

    @cached_property
    def model_servers(self) -> AsyncModelServersResource:
        from .resources.model_servers import AsyncModelServersResource

        return AsyncModelServersResource(self)

    @cached_property
    def alias(self) -> AsyncAliasResource:
        from .resources.alias import AsyncAliasResource

        return AsyncAliasResource(self)

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
            "x-selected-account-id": self.account_id if self.account_id is not None else Omit(),
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        account_id: str | None = None,
        environment: Literal["production", "development"] | None = None,
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
    def knowledge_bases(self) -> knowledge_bases.KnowledgeBasesResourceWithRawResponse:
        from .resources.knowledge_bases import KnowledgeBasesResourceWithRawResponse

        return KnowledgeBasesResourceWithRawResponse(self._client.knowledge_bases)

    @cached_property
    def knowledge_base_data_sources(
        self,
    ) -> knowledge_base_data_sources.KnowledgeBaseDataSourcesResourceWithRawResponse:
        from .resources.knowledge_base_data_sources import KnowledgeBaseDataSourcesResourceWithRawResponse

        return KnowledgeBaseDataSourcesResourceWithRawResponse(self._client.knowledge_base_data_sources)

    @cached_property
    def chunks(self) -> chunks.ChunksResourceWithRawResponse:
        from .resources.chunks import ChunksResourceWithRawResponse

        return ChunksResourceWithRawResponse(self._client.chunks)

    @cached_property
    def agents(self) -> agents.AgentsResourceWithRawResponse:
        from .resources.agents import AgentsResourceWithRawResponse

        return AgentsResourceWithRawResponse(self._client.agents)

    @cached_property
    def completions(self) -> completions.CompletionsResourceWithRawResponse:
        from .resources.completions import CompletionsResourceWithRawResponse

        return CompletionsResourceWithRawResponse(self._client.completions)

    @cached_property
    def chat_completions(self) -> chat_completions.ChatCompletionsResourceWithRawResponse:
        from .resources.chat_completions import ChatCompletionsResourceWithRawResponse

        return ChatCompletionsResourceWithRawResponse(self._client.chat_completions)

    @cached_property
    def models(self) -> models.ModelsResourceWithRawResponse:
        from .resources.models import ModelsResourceWithRawResponse

        return ModelsResourceWithRawResponse(self._client.models)

    @cached_property
    def model_groups(self) -> model_groups.ModelGroupsResourceWithRawResponse:
        from .resources.model_groups import ModelGroupsResourceWithRawResponse

        return ModelGroupsResourceWithRawResponse(self._client.model_groups)

    @cached_property
    def users(self) -> users.UsersResourceWithRawResponse:
        from .resources.users import UsersResourceWithRawResponse

        return UsersResourceWithRawResponse(self._client.users)

    @cached_property
    def accounts(self) -> accounts.AccountsResourceWithRawResponse:
        from .resources.accounts import AccountsResourceWithRawResponse

        return AccountsResourceWithRawResponse(self._client.accounts)

    @cached_property
    def question_sets(self) -> question_sets.QuestionSetsResourceWithRawResponse:
        from .resources.question_sets import QuestionSetsResourceWithRawResponse

        return QuestionSetsResourceWithRawResponse(self._client.question_sets)

    @cached_property
    def evaluations(self) -> evaluations.EvaluationsResourceWithRawResponse:
        from .resources.evaluations import EvaluationsResourceWithRawResponse

        return EvaluationsResourceWithRawResponse(self._client.evaluations)

    @cached_property
    def evaluation_configs(self) -> evaluation_configs.EvaluationConfigsResourceWithRawResponse:
        from .resources.evaluation_configs import EvaluationConfigsResourceWithRawResponse

        return EvaluationConfigsResourceWithRawResponse(self._client.evaluation_configs)

    @cached_property
    def evaluation_datasets(self) -> evaluation_datasets.EvaluationDatasetsResourceWithRawResponse:
        from .resources.evaluation_datasets import EvaluationDatasetsResourceWithRawResponse

        return EvaluationDatasetsResourceWithRawResponse(self._client.evaluation_datasets)

    @cached_property
    def studio_projects(self) -> studio_projects.StudioProjectsResourceWithRawResponse:
        from .resources.studio_projects import StudioProjectsResourceWithRawResponse

        return StudioProjectsResourceWithRawResponse(self._client.studio_projects)

    @cached_property
    def application_specs(self) -> application_specs.ApplicationSpecsResourceWithRawResponse:
        from .resources.application_specs import ApplicationSpecsResourceWithRawResponse

        return ApplicationSpecsResourceWithRawResponse(self._client.application_specs)

    @cached_property
    def questions(self) -> questions.QuestionsResourceWithRawResponse:
        from .resources.questions import QuestionsResourceWithRawResponse

        return QuestionsResourceWithRawResponse(self._client.questions)

    @cached_property
    def model_templates(self) -> model_templates.ModelTemplatesResourceWithRawResponse:
        from .resources.model_templates import ModelTemplatesResourceWithRawResponse

        return ModelTemplatesResourceWithRawResponse(self._client.model_templates)

    @cached_property
    def fine_tuning_jobs(self) -> fine_tuning_jobs.FineTuningJobsResourceWithRawResponse:
        from .resources.fine_tuning_jobs import FineTuningJobsResourceWithRawResponse

        return FineTuningJobsResourceWithRawResponse(self._client.fine_tuning_jobs)

    @cached_property
    def training_datasets(self) -> training_datasets.TrainingDatasetsResourceWithRawResponse:
        from .resources.training_datasets import TrainingDatasetsResourceWithRawResponse

        return TrainingDatasetsResourceWithRawResponse(self._client.training_datasets)

    @cached_property
    def deployment_packages(self) -> deployment_packages.DeploymentPackagesResourceWithRawResponse:
        from .resources.deployment_packages import DeploymentPackagesResourceWithRawResponse

        return DeploymentPackagesResourceWithRawResponse(self._client.deployment_packages)

    @cached_property
    def application_variants(self) -> application_variants.ApplicationVariantsResourceWithRawResponse:
        from .resources.application_variants import ApplicationVariantsResourceWithRawResponse

        return ApplicationVariantsResourceWithRawResponse(self._client.application_variants)

    @cached_property
    def application_deployments(self) -> application_deployments.ApplicationDeploymentsResourceWithRawResponse:
        from .resources.application_deployments import ApplicationDeploymentsResourceWithRawResponse

        return ApplicationDeploymentsResourceWithRawResponse(self._client.application_deployments)

    @cached_property
    def application_variant_reports(
        self,
    ) -> application_variant_reports.ApplicationVariantReportsResourceWithRawResponse:
        from .resources.application_variant_reports import ApplicationVariantReportsResourceWithRawResponse

        return ApplicationVariantReportsResourceWithRawResponse(self._client.application_variant_reports)

    @cached_property
    def application_test_case_outputs(
        self,
    ) -> application_test_case_outputs.ApplicationTestCaseOutputsResourceWithRawResponse:
        from .resources.application_test_case_outputs import ApplicationTestCaseOutputsResourceWithRawResponse

        return ApplicationTestCaseOutputsResourceWithRawResponse(self._client.application_test_case_outputs)

    @cached_property
    def application_schemas(self) -> application_schemas.ApplicationSchemasResourceWithRawResponse:
        from .resources.application_schemas import ApplicationSchemasResourceWithRawResponse

        return ApplicationSchemasResourceWithRawResponse(self._client.application_schemas)

    @cached_property
    def interactions(self) -> interactions.InteractionsResourceWithRawResponse:
        from .resources.interactions import InteractionsResourceWithRawResponse

        return InteractionsResourceWithRawResponse(self._client.interactions)

    @cached_property
    def applications(self) -> applications.ApplicationsResourceWithRawResponse:
        from .resources.applications import ApplicationsResourceWithRawResponse

        return ApplicationsResourceWithRawResponse(self._client.applications)

    @cached_property
    def application_threads(self) -> application_threads.ApplicationThreadsResourceWithRawResponse:
        from .resources.application_threads import ApplicationThreadsResourceWithRawResponse

        return ApplicationThreadsResourceWithRawResponse(self._client.application_threads)

    @cached_property
    def chat_threads(self) -> chat_threads.ChatThreadsResourceWithRawResponse:
        from .resources.chat_threads import ChatThreadsResourceWithRawResponse

        return ChatThreadsResourceWithRawResponse(self._client.chat_threads)

    @cached_property
    def themes(self) -> themes.ThemesResourceWithRawResponse:
        from .resources.themes import ThemesResourceWithRawResponse

        return ThemesResourceWithRawResponse(self._client.themes)

    @cached_property
    def beta(self) -> beta.BetaResourceWithRawResponse:
        from .resources.beta import BetaResourceWithRawResponse

        return BetaResourceWithRawResponse(self._client.beta)

    @cached_property
    def model_servers(self) -> model_servers.ModelServersResourceWithRawResponse:
        from .resources.model_servers import ModelServersResourceWithRawResponse

        return ModelServersResourceWithRawResponse(self._client.model_servers)

    @cached_property
    def alias(self) -> alias.AliasResourceWithRawResponse:
        from .resources.alias import AliasResourceWithRawResponse

        return AliasResourceWithRawResponse(self._client.alias)


class AsyncSGPClientWithRawResponse:
    _client: AsyncSGPClient

    def __init__(self, client: AsyncSGPClient) -> None:
        self._client = client

    @cached_property
    def knowledge_bases(self) -> knowledge_bases.AsyncKnowledgeBasesResourceWithRawResponse:
        from .resources.knowledge_bases import AsyncKnowledgeBasesResourceWithRawResponse

        return AsyncKnowledgeBasesResourceWithRawResponse(self._client.knowledge_bases)

    @cached_property
    def knowledge_base_data_sources(
        self,
    ) -> knowledge_base_data_sources.AsyncKnowledgeBaseDataSourcesResourceWithRawResponse:
        from .resources.knowledge_base_data_sources import AsyncKnowledgeBaseDataSourcesResourceWithRawResponse

        return AsyncKnowledgeBaseDataSourcesResourceWithRawResponse(self._client.knowledge_base_data_sources)

    @cached_property
    def chunks(self) -> chunks.AsyncChunksResourceWithRawResponse:
        from .resources.chunks import AsyncChunksResourceWithRawResponse

        return AsyncChunksResourceWithRawResponse(self._client.chunks)

    @cached_property
    def agents(self) -> agents.AsyncAgentsResourceWithRawResponse:
        from .resources.agents import AsyncAgentsResourceWithRawResponse

        return AsyncAgentsResourceWithRawResponse(self._client.agents)

    @cached_property
    def completions(self) -> completions.AsyncCompletionsResourceWithRawResponse:
        from .resources.completions import AsyncCompletionsResourceWithRawResponse

        return AsyncCompletionsResourceWithRawResponse(self._client.completions)

    @cached_property
    def chat_completions(self) -> chat_completions.AsyncChatCompletionsResourceWithRawResponse:
        from .resources.chat_completions import AsyncChatCompletionsResourceWithRawResponse

        return AsyncChatCompletionsResourceWithRawResponse(self._client.chat_completions)

    @cached_property
    def models(self) -> models.AsyncModelsResourceWithRawResponse:
        from .resources.models import AsyncModelsResourceWithRawResponse

        return AsyncModelsResourceWithRawResponse(self._client.models)

    @cached_property
    def model_groups(self) -> model_groups.AsyncModelGroupsResourceWithRawResponse:
        from .resources.model_groups import AsyncModelGroupsResourceWithRawResponse

        return AsyncModelGroupsResourceWithRawResponse(self._client.model_groups)

    @cached_property
    def users(self) -> users.AsyncUsersResourceWithRawResponse:
        from .resources.users import AsyncUsersResourceWithRawResponse

        return AsyncUsersResourceWithRawResponse(self._client.users)

    @cached_property
    def accounts(self) -> accounts.AsyncAccountsResourceWithRawResponse:
        from .resources.accounts import AsyncAccountsResourceWithRawResponse

        return AsyncAccountsResourceWithRawResponse(self._client.accounts)

    @cached_property
    def question_sets(self) -> question_sets.AsyncQuestionSetsResourceWithRawResponse:
        from .resources.question_sets import AsyncQuestionSetsResourceWithRawResponse

        return AsyncQuestionSetsResourceWithRawResponse(self._client.question_sets)

    @cached_property
    def evaluations(self) -> evaluations.AsyncEvaluationsResourceWithRawResponse:
        from .resources.evaluations import AsyncEvaluationsResourceWithRawResponse

        return AsyncEvaluationsResourceWithRawResponse(self._client.evaluations)

    @cached_property
    def evaluation_configs(self) -> evaluation_configs.AsyncEvaluationConfigsResourceWithRawResponse:
        from .resources.evaluation_configs import AsyncEvaluationConfigsResourceWithRawResponse

        return AsyncEvaluationConfigsResourceWithRawResponse(self._client.evaluation_configs)

    @cached_property
    def evaluation_datasets(self) -> evaluation_datasets.AsyncEvaluationDatasetsResourceWithRawResponse:
        from .resources.evaluation_datasets import AsyncEvaluationDatasetsResourceWithRawResponse

        return AsyncEvaluationDatasetsResourceWithRawResponse(self._client.evaluation_datasets)

    @cached_property
    def studio_projects(self) -> studio_projects.AsyncStudioProjectsResourceWithRawResponse:
        from .resources.studio_projects import AsyncStudioProjectsResourceWithRawResponse

        return AsyncStudioProjectsResourceWithRawResponse(self._client.studio_projects)

    @cached_property
    def application_specs(self) -> application_specs.AsyncApplicationSpecsResourceWithRawResponse:
        from .resources.application_specs import AsyncApplicationSpecsResourceWithRawResponse

        return AsyncApplicationSpecsResourceWithRawResponse(self._client.application_specs)

    @cached_property
    def questions(self) -> questions.AsyncQuestionsResourceWithRawResponse:
        from .resources.questions import AsyncQuestionsResourceWithRawResponse

        return AsyncQuestionsResourceWithRawResponse(self._client.questions)

    @cached_property
    def model_templates(self) -> model_templates.AsyncModelTemplatesResourceWithRawResponse:
        from .resources.model_templates import AsyncModelTemplatesResourceWithRawResponse

        return AsyncModelTemplatesResourceWithRawResponse(self._client.model_templates)

    @cached_property
    def fine_tuning_jobs(self) -> fine_tuning_jobs.AsyncFineTuningJobsResourceWithRawResponse:
        from .resources.fine_tuning_jobs import AsyncFineTuningJobsResourceWithRawResponse

        return AsyncFineTuningJobsResourceWithRawResponse(self._client.fine_tuning_jobs)

    @cached_property
    def training_datasets(self) -> training_datasets.AsyncTrainingDatasetsResourceWithRawResponse:
        from .resources.training_datasets import AsyncTrainingDatasetsResourceWithRawResponse

        return AsyncTrainingDatasetsResourceWithRawResponse(self._client.training_datasets)

    @cached_property
    def deployment_packages(self) -> deployment_packages.AsyncDeploymentPackagesResourceWithRawResponse:
        from .resources.deployment_packages import AsyncDeploymentPackagesResourceWithRawResponse

        return AsyncDeploymentPackagesResourceWithRawResponse(self._client.deployment_packages)

    @cached_property
    def application_variants(self) -> application_variants.AsyncApplicationVariantsResourceWithRawResponse:
        from .resources.application_variants import AsyncApplicationVariantsResourceWithRawResponse

        return AsyncApplicationVariantsResourceWithRawResponse(self._client.application_variants)

    @cached_property
    def application_deployments(self) -> application_deployments.AsyncApplicationDeploymentsResourceWithRawResponse:
        from .resources.application_deployments import AsyncApplicationDeploymentsResourceWithRawResponse

        return AsyncApplicationDeploymentsResourceWithRawResponse(self._client.application_deployments)

    @cached_property
    def application_variant_reports(
        self,
    ) -> application_variant_reports.AsyncApplicationVariantReportsResourceWithRawResponse:
        from .resources.application_variant_reports import AsyncApplicationVariantReportsResourceWithRawResponse

        return AsyncApplicationVariantReportsResourceWithRawResponse(self._client.application_variant_reports)

    @cached_property
    def application_test_case_outputs(
        self,
    ) -> application_test_case_outputs.AsyncApplicationTestCaseOutputsResourceWithRawResponse:
        from .resources.application_test_case_outputs import AsyncApplicationTestCaseOutputsResourceWithRawResponse

        return AsyncApplicationTestCaseOutputsResourceWithRawResponse(self._client.application_test_case_outputs)

    @cached_property
    def application_schemas(self) -> application_schemas.AsyncApplicationSchemasResourceWithRawResponse:
        from .resources.application_schemas import AsyncApplicationSchemasResourceWithRawResponse

        return AsyncApplicationSchemasResourceWithRawResponse(self._client.application_schemas)

    @cached_property
    def interactions(self) -> interactions.AsyncInteractionsResourceWithRawResponse:
        from .resources.interactions import AsyncInteractionsResourceWithRawResponse

        return AsyncInteractionsResourceWithRawResponse(self._client.interactions)

    @cached_property
    def applications(self) -> applications.AsyncApplicationsResourceWithRawResponse:
        from .resources.applications import AsyncApplicationsResourceWithRawResponse

        return AsyncApplicationsResourceWithRawResponse(self._client.applications)

    @cached_property
    def application_threads(self) -> application_threads.AsyncApplicationThreadsResourceWithRawResponse:
        from .resources.application_threads import AsyncApplicationThreadsResourceWithRawResponse

        return AsyncApplicationThreadsResourceWithRawResponse(self._client.application_threads)

    @cached_property
    def chat_threads(self) -> chat_threads.AsyncChatThreadsResourceWithRawResponse:
        from .resources.chat_threads import AsyncChatThreadsResourceWithRawResponse

        return AsyncChatThreadsResourceWithRawResponse(self._client.chat_threads)

    @cached_property
    def themes(self) -> themes.AsyncThemesResourceWithRawResponse:
        from .resources.themes import AsyncThemesResourceWithRawResponse

        return AsyncThemesResourceWithRawResponse(self._client.themes)

    @cached_property
    def beta(self) -> beta.AsyncBetaResourceWithRawResponse:
        from .resources.beta import AsyncBetaResourceWithRawResponse

        return AsyncBetaResourceWithRawResponse(self._client.beta)

    @cached_property
    def model_servers(self) -> model_servers.AsyncModelServersResourceWithRawResponse:
        from .resources.model_servers import AsyncModelServersResourceWithRawResponse

        return AsyncModelServersResourceWithRawResponse(self._client.model_servers)

    @cached_property
    def alias(self) -> alias.AsyncAliasResourceWithRawResponse:
        from .resources.alias import AsyncAliasResourceWithRawResponse

        return AsyncAliasResourceWithRawResponse(self._client.alias)


class SGPClientWithStreamedResponse:
    _client: SGPClient

    def __init__(self, client: SGPClient) -> None:
        self._client = client

    @cached_property
    def knowledge_bases(self) -> knowledge_bases.KnowledgeBasesResourceWithStreamingResponse:
        from .resources.knowledge_bases import KnowledgeBasesResourceWithStreamingResponse

        return KnowledgeBasesResourceWithStreamingResponse(self._client.knowledge_bases)

    @cached_property
    def knowledge_base_data_sources(
        self,
    ) -> knowledge_base_data_sources.KnowledgeBaseDataSourcesResourceWithStreamingResponse:
        from .resources.knowledge_base_data_sources import KnowledgeBaseDataSourcesResourceWithStreamingResponse

        return KnowledgeBaseDataSourcesResourceWithStreamingResponse(self._client.knowledge_base_data_sources)

    @cached_property
    def chunks(self) -> chunks.ChunksResourceWithStreamingResponse:
        from .resources.chunks import ChunksResourceWithStreamingResponse

        return ChunksResourceWithStreamingResponse(self._client.chunks)

    @cached_property
    def agents(self) -> agents.AgentsResourceWithStreamingResponse:
        from .resources.agents import AgentsResourceWithStreamingResponse

        return AgentsResourceWithStreamingResponse(self._client.agents)

    @cached_property
    def completions(self) -> completions.CompletionsResourceWithStreamingResponse:
        from .resources.completions import CompletionsResourceWithStreamingResponse

        return CompletionsResourceWithStreamingResponse(self._client.completions)

    @cached_property
    def chat_completions(self) -> chat_completions.ChatCompletionsResourceWithStreamingResponse:
        from .resources.chat_completions import ChatCompletionsResourceWithStreamingResponse

        return ChatCompletionsResourceWithStreamingResponse(self._client.chat_completions)

    @cached_property
    def models(self) -> models.ModelsResourceWithStreamingResponse:
        from .resources.models import ModelsResourceWithStreamingResponse

        return ModelsResourceWithStreamingResponse(self._client.models)

    @cached_property
    def model_groups(self) -> model_groups.ModelGroupsResourceWithStreamingResponse:
        from .resources.model_groups import ModelGroupsResourceWithStreamingResponse

        return ModelGroupsResourceWithStreamingResponse(self._client.model_groups)

    @cached_property
    def users(self) -> users.UsersResourceWithStreamingResponse:
        from .resources.users import UsersResourceWithStreamingResponse

        return UsersResourceWithStreamingResponse(self._client.users)

    @cached_property
    def accounts(self) -> accounts.AccountsResourceWithStreamingResponse:
        from .resources.accounts import AccountsResourceWithStreamingResponse

        return AccountsResourceWithStreamingResponse(self._client.accounts)

    @cached_property
    def question_sets(self) -> question_sets.QuestionSetsResourceWithStreamingResponse:
        from .resources.question_sets import QuestionSetsResourceWithStreamingResponse

        return QuestionSetsResourceWithStreamingResponse(self._client.question_sets)

    @cached_property
    def evaluations(self) -> evaluations.EvaluationsResourceWithStreamingResponse:
        from .resources.evaluations import EvaluationsResourceWithStreamingResponse

        return EvaluationsResourceWithStreamingResponse(self._client.evaluations)

    @cached_property
    def evaluation_configs(self) -> evaluation_configs.EvaluationConfigsResourceWithStreamingResponse:
        from .resources.evaluation_configs import EvaluationConfigsResourceWithStreamingResponse

        return EvaluationConfigsResourceWithStreamingResponse(self._client.evaluation_configs)

    @cached_property
    def evaluation_datasets(self) -> evaluation_datasets.EvaluationDatasetsResourceWithStreamingResponse:
        from .resources.evaluation_datasets import EvaluationDatasetsResourceWithStreamingResponse

        return EvaluationDatasetsResourceWithStreamingResponse(self._client.evaluation_datasets)

    @cached_property
    def studio_projects(self) -> studio_projects.StudioProjectsResourceWithStreamingResponse:
        from .resources.studio_projects import StudioProjectsResourceWithStreamingResponse

        return StudioProjectsResourceWithStreamingResponse(self._client.studio_projects)

    @cached_property
    def application_specs(self) -> application_specs.ApplicationSpecsResourceWithStreamingResponse:
        from .resources.application_specs import ApplicationSpecsResourceWithStreamingResponse

        return ApplicationSpecsResourceWithStreamingResponse(self._client.application_specs)

    @cached_property
    def questions(self) -> questions.QuestionsResourceWithStreamingResponse:
        from .resources.questions import QuestionsResourceWithStreamingResponse

        return QuestionsResourceWithStreamingResponse(self._client.questions)

    @cached_property
    def model_templates(self) -> model_templates.ModelTemplatesResourceWithStreamingResponse:
        from .resources.model_templates import ModelTemplatesResourceWithStreamingResponse

        return ModelTemplatesResourceWithStreamingResponse(self._client.model_templates)

    @cached_property
    def fine_tuning_jobs(self) -> fine_tuning_jobs.FineTuningJobsResourceWithStreamingResponse:
        from .resources.fine_tuning_jobs import FineTuningJobsResourceWithStreamingResponse

        return FineTuningJobsResourceWithStreamingResponse(self._client.fine_tuning_jobs)

    @cached_property
    def training_datasets(self) -> training_datasets.TrainingDatasetsResourceWithStreamingResponse:
        from .resources.training_datasets import TrainingDatasetsResourceWithStreamingResponse

        return TrainingDatasetsResourceWithStreamingResponse(self._client.training_datasets)

    @cached_property
    def deployment_packages(self) -> deployment_packages.DeploymentPackagesResourceWithStreamingResponse:
        from .resources.deployment_packages import DeploymentPackagesResourceWithStreamingResponse

        return DeploymentPackagesResourceWithStreamingResponse(self._client.deployment_packages)

    @cached_property
    def application_variants(self) -> application_variants.ApplicationVariantsResourceWithStreamingResponse:
        from .resources.application_variants import ApplicationVariantsResourceWithStreamingResponse

        return ApplicationVariantsResourceWithStreamingResponse(self._client.application_variants)

    @cached_property
    def application_deployments(self) -> application_deployments.ApplicationDeploymentsResourceWithStreamingResponse:
        from .resources.application_deployments import ApplicationDeploymentsResourceWithStreamingResponse

        return ApplicationDeploymentsResourceWithStreamingResponse(self._client.application_deployments)

    @cached_property
    def application_variant_reports(
        self,
    ) -> application_variant_reports.ApplicationVariantReportsResourceWithStreamingResponse:
        from .resources.application_variant_reports import ApplicationVariantReportsResourceWithStreamingResponse

        return ApplicationVariantReportsResourceWithStreamingResponse(self._client.application_variant_reports)

    @cached_property
    def application_test_case_outputs(
        self,
    ) -> application_test_case_outputs.ApplicationTestCaseOutputsResourceWithStreamingResponse:
        from .resources.application_test_case_outputs import ApplicationTestCaseOutputsResourceWithStreamingResponse

        return ApplicationTestCaseOutputsResourceWithStreamingResponse(self._client.application_test_case_outputs)

    @cached_property
    def application_schemas(self) -> application_schemas.ApplicationSchemasResourceWithStreamingResponse:
        from .resources.application_schemas import ApplicationSchemasResourceWithStreamingResponse

        return ApplicationSchemasResourceWithStreamingResponse(self._client.application_schemas)

    @cached_property
    def interactions(self) -> interactions.InteractionsResourceWithStreamingResponse:
        from .resources.interactions import InteractionsResourceWithStreamingResponse

        return InteractionsResourceWithStreamingResponse(self._client.interactions)

    @cached_property
    def applications(self) -> applications.ApplicationsResourceWithStreamingResponse:
        from .resources.applications import ApplicationsResourceWithStreamingResponse

        return ApplicationsResourceWithStreamingResponse(self._client.applications)

    @cached_property
    def application_threads(self) -> application_threads.ApplicationThreadsResourceWithStreamingResponse:
        from .resources.application_threads import ApplicationThreadsResourceWithStreamingResponse

        return ApplicationThreadsResourceWithStreamingResponse(self._client.application_threads)

    @cached_property
    def chat_threads(self) -> chat_threads.ChatThreadsResourceWithStreamingResponse:
        from .resources.chat_threads import ChatThreadsResourceWithStreamingResponse

        return ChatThreadsResourceWithStreamingResponse(self._client.chat_threads)

    @cached_property
    def themes(self) -> themes.ThemesResourceWithStreamingResponse:
        from .resources.themes import ThemesResourceWithStreamingResponse

        return ThemesResourceWithStreamingResponse(self._client.themes)

    @cached_property
    def beta(self) -> beta.BetaResourceWithStreamingResponse:
        from .resources.beta import BetaResourceWithStreamingResponse

        return BetaResourceWithStreamingResponse(self._client.beta)

    @cached_property
    def model_servers(self) -> model_servers.ModelServersResourceWithStreamingResponse:
        from .resources.model_servers import ModelServersResourceWithStreamingResponse

        return ModelServersResourceWithStreamingResponse(self._client.model_servers)

    @cached_property
    def alias(self) -> alias.AliasResourceWithStreamingResponse:
        from .resources.alias import AliasResourceWithStreamingResponse

        return AliasResourceWithStreamingResponse(self._client.alias)


class AsyncSGPClientWithStreamedResponse:
    _client: AsyncSGPClient

    def __init__(self, client: AsyncSGPClient) -> None:
        self._client = client

    @cached_property
    def knowledge_bases(self) -> knowledge_bases.AsyncKnowledgeBasesResourceWithStreamingResponse:
        from .resources.knowledge_bases import AsyncKnowledgeBasesResourceWithStreamingResponse

        return AsyncKnowledgeBasesResourceWithStreamingResponse(self._client.knowledge_bases)

    @cached_property
    def knowledge_base_data_sources(
        self,
    ) -> knowledge_base_data_sources.AsyncKnowledgeBaseDataSourcesResourceWithStreamingResponse:
        from .resources.knowledge_base_data_sources import AsyncKnowledgeBaseDataSourcesResourceWithStreamingResponse

        return AsyncKnowledgeBaseDataSourcesResourceWithStreamingResponse(self._client.knowledge_base_data_sources)

    @cached_property
    def chunks(self) -> chunks.AsyncChunksResourceWithStreamingResponse:
        from .resources.chunks import AsyncChunksResourceWithStreamingResponse

        return AsyncChunksResourceWithStreamingResponse(self._client.chunks)

    @cached_property
    def agents(self) -> agents.AsyncAgentsResourceWithStreamingResponse:
        from .resources.agents import AsyncAgentsResourceWithStreamingResponse

        return AsyncAgentsResourceWithStreamingResponse(self._client.agents)

    @cached_property
    def completions(self) -> completions.AsyncCompletionsResourceWithStreamingResponse:
        from .resources.completions import AsyncCompletionsResourceWithStreamingResponse

        return AsyncCompletionsResourceWithStreamingResponse(self._client.completions)

    @cached_property
    def chat_completions(self) -> chat_completions.AsyncChatCompletionsResourceWithStreamingResponse:
        from .resources.chat_completions import AsyncChatCompletionsResourceWithStreamingResponse

        return AsyncChatCompletionsResourceWithStreamingResponse(self._client.chat_completions)

    @cached_property
    def models(self) -> models.AsyncModelsResourceWithStreamingResponse:
        from .resources.models import AsyncModelsResourceWithStreamingResponse

        return AsyncModelsResourceWithStreamingResponse(self._client.models)

    @cached_property
    def model_groups(self) -> model_groups.AsyncModelGroupsResourceWithStreamingResponse:
        from .resources.model_groups import AsyncModelGroupsResourceWithStreamingResponse

        return AsyncModelGroupsResourceWithStreamingResponse(self._client.model_groups)

    @cached_property
    def users(self) -> users.AsyncUsersResourceWithStreamingResponse:
        from .resources.users import AsyncUsersResourceWithStreamingResponse

        return AsyncUsersResourceWithStreamingResponse(self._client.users)

    @cached_property
    def accounts(self) -> accounts.AsyncAccountsResourceWithStreamingResponse:
        from .resources.accounts import AsyncAccountsResourceWithStreamingResponse

        return AsyncAccountsResourceWithStreamingResponse(self._client.accounts)

    @cached_property
    def question_sets(self) -> question_sets.AsyncQuestionSetsResourceWithStreamingResponse:
        from .resources.question_sets import AsyncQuestionSetsResourceWithStreamingResponse

        return AsyncQuestionSetsResourceWithStreamingResponse(self._client.question_sets)

    @cached_property
    def evaluations(self) -> evaluations.AsyncEvaluationsResourceWithStreamingResponse:
        from .resources.evaluations import AsyncEvaluationsResourceWithStreamingResponse

        return AsyncEvaluationsResourceWithStreamingResponse(self._client.evaluations)

    @cached_property
    def evaluation_configs(self) -> evaluation_configs.AsyncEvaluationConfigsResourceWithStreamingResponse:
        from .resources.evaluation_configs import AsyncEvaluationConfigsResourceWithStreamingResponse

        return AsyncEvaluationConfigsResourceWithStreamingResponse(self._client.evaluation_configs)

    @cached_property
    def evaluation_datasets(self) -> evaluation_datasets.AsyncEvaluationDatasetsResourceWithStreamingResponse:
        from .resources.evaluation_datasets import AsyncEvaluationDatasetsResourceWithStreamingResponse

        return AsyncEvaluationDatasetsResourceWithStreamingResponse(self._client.evaluation_datasets)

    @cached_property
    def studio_projects(self) -> studio_projects.AsyncStudioProjectsResourceWithStreamingResponse:
        from .resources.studio_projects import AsyncStudioProjectsResourceWithStreamingResponse

        return AsyncStudioProjectsResourceWithStreamingResponse(self._client.studio_projects)

    @cached_property
    def application_specs(self) -> application_specs.AsyncApplicationSpecsResourceWithStreamingResponse:
        from .resources.application_specs import AsyncApplicationSpecsResourceWithStreamingResponse

        return AsyncApplicationSpecsResourceWithStreamingResponse(self._client.application_specs)

    @cached_property
    def questions(self) -> questions.AsyncQuestionsResourceWithStreamingResponse:
        from .resources.questions import AsyncQuestionsResourceWithStreamingResponse

        return AsyncQuestionsResourceWithStreamingResponse(self._client.questions)

    @cached_property
    def model_templates(self) -> model_templates.AsyncModelTemplatesResourceWithStreamingResponse:
        from .resources.model_templates import AsyncModelTemplatesResourceWithStreamingResponse

        return AsyncModelTemplatesResourceWithStreamingResponse(self._client.model_templates)

    @cached_property
    def fine_tuning_jobs(self) -> fine_tuning_jobs.AsyncFineTuningJobsResourceWithStreamingResponse:
        from .resources.fine_tuning_jobs import AsyncFineTuningJobsResourceWithStreamingResponse

        return AsyncFineTuningJobsResourceWithStreamingResponse(self._client.fine_tuning_jobs)

    @cached_property
    def training_datasets(self) -> training_datasets.AsyncTrainingDatasetsResourceWithStreamingResponse:
        from .resources.training_datasets import AsyncTrainingDatasetsResourceWithStreamingResponse

        return AsyncTrainingDatasetsResourceWithStreamingResponse(self._client.training_datasets)

    @cached_property
    def deployment_packages(self) -> deployment_packages.AsyncDeploymentPackagesResourceWithStreamingResponse:
        from .resources.deployment_packages import AsyncDeploymentPackagesResourceWithStreamingResponse

        return AsyncDeploymentPackagesResourceWithStreamingResponse(self._client.deployment_packages)

    @cached_property
    def application_variants(self) -> application_variants.AsyncApplicationVariantsResourceWithStreamingResponse:
        from .resources.application_variants import AsyncApplicationVariantsResourceWithStreamingResponse

        return AsyncApplicationVariantsResourceWithStreamingResponse(self._client.application_variants)

    @cached_property
    def application_deployments(
        self,
    ) -> application_deployments.AsyncApplicationDeploymentsResourceWithStreamingResponse:
        from .resources.application_deployments import AsyncApplicationDeploymentsResourceWithStreamingResponse

        return AsyncApplicationDeploymentsResourceWithStreamingResponse(self._client.application_deployments)

    @cached_property
    def application_variant_reports(
        self,
    ) -> application_variant_reports.AsyncApplicationVariantReportsResourceWithStreamingResponse:
        from .resources.application_variant_reports import AsyncApplicationVariantReportsResourceWithStreamingResponse

        return AsyncApplicationVariantReportsResourceWithStreamingResponse(self._client.application_variant_reports)

    @cached_property
    def application_test_case_outputs(
        self,
    ) -> application_test_case_outputs.AsyncApplicationTestCaseOutputsResourceWithStreamingResponse:
        from .resources.application_test_case_outputs import (
            AsyncApplicationTestCaseOutputsResourceWithStreamingResponse,
        )

        return AsyncApplicationTestCaseOutputsResourceWithStreamingResponse(self._client.application_test_case_outputs)

    @cached_property
    def application_schemas(self) -> application_schemas.AsyncApplicationSchemasResourceWithStreamingResponse:
        from .resources.application_schemas import AsyncApplicationSchemasResourceWithStreamingResponse

        return AsyncApplicationSchemasResourceWithStreamingResponse(self._client.application_schemas)

    @cached_property
    def interactions(self) -> interactions.AsyncInteractionsResourceWithStreamingResponse:
        from .resources.interactions import AsyncInteractionsResourceWithStreamingResponse

        return AsyncInteractionsResourceWithStreamingResponse(self._client.interactions)

    @cached_property
    def applications(self) -> applications.AsyncApplicationsResourceWithStreamingResponse:
        from .resources.applications import AsyncApplicationsResourceWithStreamingResponse

        return AsyncApplicationsResourceWithStreamingResponse(self._client.applications)

    @cached_property
    def application_threads(self) -> application_threads.AsyncApplicationThreadsResourceWithStreamingResponse:
        from .resources.application_threads import AsyncApplicationThreadsResourceWithStreamingResponse

        return AsyncApplicationThreadsResourceWithStreamingResponse(self._client.application_threads)

    @cached_property
    def chat_threads(self) -> chat_threads.AsyncChatThreadsResourceWithStreamingResponse:
        from .resources.chat_threads import AsyncChatThreadsResourceWithStreamingResponse

        return AsyncChatThreadsResourceWithStreamingResponse(self._client.chat_threads)

    @cached_property
    def themes(self) -> themes.AsyncThemesResourceWithStreamingResponse:
        from .resources.themes import AsyncThemesResourceWithStreamingResponse

        return AsyncThemesResourceWithStreamingResponse(self._client.themes)

    @cached_property
    def beta(self) -> beta.AsyncBetaResourceWithStreamingResponse:
        from .resources.beta import AsyncBetaResourceWithStreamingResponse

        return AsyncBetaResourceWithStreamingResponse(self._client.beta)

    @cached_property
    def model_servers(self) -> model_servers.AsyncModelServersResourceWithStreamingResponse:
        from .resources.model_servers import AsyncModelServersResourceWithStreamingResponse

        return AsyncModelServersResourceWithStreamingResponse(self._client.model_servers)

    @cached_property
    def alias(self) -> alias.AsyncAliasResourceWithStreamingResponse:
        from .resources.alias import AsyncAliasResourceWithStreamingResponse

        return AsyncAliasResourceWithStreamingResponse(self._client.alias)


Client = SGPClient

AsyncClient = AsyncSGPClient
