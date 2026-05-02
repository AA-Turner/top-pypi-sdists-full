# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Headers,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import is_given, get_async_library
from ._version import __version__
from .resources import (
    apps,
    whoami,
    prompts,
    projects,
    evaluators,
    evaluations,
    experiments,
    trace_insight,
    evaluator_criteria,
)
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)
from .resources.otel import otel

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "PatronusAPI",
    "AsyncPatronusAPI",
    "Client",
    "AsyncClient",
]


class PatronusAPI(SyncAPIClient):
    evaluator_criteria: evaluator_criteria.EvaluatorCriteriaResource
    experiments: experiments.ExperimentsResource
    projects: projects.ProjectsResource
    evaluations: evaluations.EvaluationsResource
    otel: otel.OtelResource
    trace_insight: trace_insight.TraceInsightResource
    evaluators: evaluators.EvaluatorsResource
    whoami: whoami.WhoamiResource
    apps: apps.AppsResource
    prompts: prompts.PromptsResource
    with_raw_response: PatronusAPIWithRawResponse
    with_streaming_response: PatronusAPIWithStreamedResponse

    # client options
    api_key: str | None
    access_token: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        access_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
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
        """Construct a new synchronous PatronusAPI client instance.

        This automatically infers the `api_key` argument from the `PATRONUS_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("PATRONUS_API_KEY")
        self.api_key = api_key

        self.access_token = access_token

        if base_url is None:
            base_url = os.environ.get("PATRONUS_API_BASE_URL")
        if base_url is None:
            base_url = f"https://api.patronus.ai"

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

        self.evaluator_criteria = evaluator_criteria.EvaluatorCriteriaResource(self)
        self.experiments = experiments.ExperimentsResource(self)
        self.projects = projects.ProjectsResource(self)
        self.evaluations = evaluations.EvaluationsResource(self)
        self.otel = otel.OtelResource(self)
        self.trace_insight = trace_insight.TraceInsightResource(self)
        self.evaluators = evaluators.EvaluatorsResource(self)
        self.whoami = whoami.WhoamiResource(self)
        self.apps = apps.AppsResource(self)
        self.prompts = prompts.PromptsResource(self)
        self.with_raw_response = PatronusAPIWithRawResponse(self)
        self.with_streaming_response = PatronusAPIWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {**self._api_key, **self._bearer_auth}

    @property
    def _api_key(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"X-API-KEY": api_key}

    @property
    def _bearer_auth(self) -> dict[str, str]:
        access_token = self.access_token
        if access_token is None:
            return {}
        return {"Authorization": f"Bearer {access_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.api_key and headers.get("X-API-KEY"):
            return
        if isinstance(custom_headers.get("X-API-KEY"), Omit):
            return

        if self.access_token and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected either api_key or access_token to be set. Or for one of the `X-API-KEY` or `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        api_key: str | None = None,
        access_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
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
            access_token=access_token or self.access_token,
            base_url=base_url or self.base_url,
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


class AsyncPatronusAPI(AsyncAPIClient):
    evaluator_criteria: evaluator_criteria.AsyncEvaluatorCriteriaResource
    experiments: experiments.AsyncExperimentsResource
    projects: projects.AsyncProjectsResource
    evaluations: evaluations.AsyncEvaluationsResource
    otel: otel.AsyncOtelResource
    trace_insight: trace_insight.AsyncTraceInsightResource
    evaluators: evaluators.AsyncEvaluatorsResource
    whoami: whoami.AsyncWhoamiResource
    apps: apps.AsyncAppsResource
    prompts: prompts.AsyncPromptsResource
    with_raw_response: AsyncPatronusAPIWithRawResponse
    with_streaming_response: AsyncPatronusAPIWithStreamedResponse

    # client options
    api_key: str | None
    access_token: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        access_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
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
        """Construct a new async AsyncPatronusAPI client instance.

        This automatically infers the `api_key` argument from the `PATRONUS_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("PATRONUS_API_KEY")
        self.api_key = api_key

        self.access_token = access_token

        if base_url is None:
            base_url = os.environ.get("PATRONUS_API_BASE_URL")
        if base_url is None:
            base_url = f"https://api.patronus.ai"

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

        self.evaluator_criteria = evaluator_criteria.AsyncEvaluatorCriteriaResource(self)
        self.experiments = experiments.AsyncExperimentsResource(self)
        self.projects = projects.AsyncProjectsResource(self)
        self.evaluations = evaluations.AsyncEvaluationsResource(self)
        self.otel = otel.AsyncOtelResource(self)
        self.trace_insight = trace_insight.AsyncTraceInsightResource(self)
        self.evaluators = evaluators.AsyncEvaluatorsResource(self)
        self.whoami = whoami.AsyncWhoamiResource(self)
        self.apps = apps.AsyncAppsResource(self)
        self.prompts = prompts.AsyncPromptsResource(self)
        self.with_raw_response = AsyncPatronusAPIWithRawResponse(self)
        self.with_streaming_response = AsyncPatronusAPIWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {**self._api_key, **self._bearer_auth}

    @property
    def _api_key(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"X-API-KEY": api_key}

    @property
    def _bearer_auth(self) -> dict[str, str]:
        access_token = self.access_token
        if access_token is None:
            return {}
        return {"Authorization": f"Bearer {access_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.api_key and headers.get("X-API-KEY"):
            return
        if isinstance(custom_headers.get("X-API-KEY"), Omit):
            return

        if self.access_token and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected either api_key or access_token to be set. Or for one of the `X-API-KEY` or `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        api_key: str | None = None,
        access_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
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
            access_token=access_token or self.access_token,
            base_url=base_url or self.base_url,
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


class PatronusAPIWithRawResponse:
    def __init__(self, client: PatronusAPI) -> None:
        self.evaluator_criteria = evaluator_criteria.EvaluatorCriteriaResourceWithRawResponse(client.evaluator_criteria)
        self.experiments = experiments.ExperimentsResourceWithRawResponse(client.experiments)
        self.projects = projects.ProjectsResourceWithRawResponse(client.projects)
        self.evaluations = evaluations.EvaluationsResourceWithRawResponse(client.evaluations)
        self.otel = otel.OtelResourceWithRawResponse(client.otel)
        self.trace_insight = trace_insight.TraceInsightResourceWithRawResponse(client.trace_insight)
        self.evaluators = evaluators.EvaluatorsResourceWithRawResponse(client.evaluators)
        self.whoami = whoami.WhoamiResourceWithRawResponse(client.whoami)
        self.apps = apps.AppsResourceWithRawResponse(client.apps)
        self.prompts = prompts.PromptsResourceWithRawResponse(client.prompts)


class AsyncPatronusAPIWithRawResponse:
    def __init__(self, client: AsyncPatronusAPI) -> None:
        self.evaluator_criteria = evaluator_criteria.AsyncEvaluatorCriteriaResourceWithRawResponse(
            client.evaluator_criteria
        )
        self.experiments = experiments.AsyncExperimentsResourceWithRawResponse(client.experiments)
        self.projects = projects.AsyncProjectsResourceWithRawResponse(client.projects)
        self.evaluations = evaluations.AsyncEvaluationsResourceWithRawResponse(client.evaluations)
        self.otel = otel.AsyncOtelResourceWithRawResponse(client.otel)
        self.trace_insight = trace_insight.AsyncTraceInsightResourceWithRawResponse(client.trace_insight)
        self.evaluators = evaluators.AsyncEvaluatorsResourceWithRawResponse(client.evaluators)
        self.whoami = whoami.AsyncWhoamiResourceWithRawResponse(client.whoami)
        self.apps = apps.AsyncAppsResourceWithRawResponse(client.apps)
        self.prompts = prompts.AsyncPromptsResourceWithRawResponse(client.prompts)


class PatronusAPIWithStreamedResponse:
    def __init__(self, client: PatronusAPI) -> None:
        self.evaluator_criteria = evaluator_criteria.EvaluatorCriteriaResourceWithStreamingResponse(
            client.evaluator_criteria
        )
        self.experiments = experiments.ExperimentsResourceWithStreamingResponse(client.experiments)
        self.projects = projects.ProjectsResourceWithStreamingResponse(client.projects)
        self.evaluations = evaluations.EvaluationsResourceWithStreamingResponse(client.evaluations)
        self.otel = otel.OtelResourceWithStreamingResponse(client.otel)
        self.trace_insight = trace_insight.TraceInsightResourceWithStreamingResponse(client.trace_insight)
        self.evaluators = evaluators.EvaluatorsResourceWithStreamingResponse(client.evaluators)
        self.whoami = whoami.WhoamiResourceWithStreamingResponse(client.whoami)
        self.apps = apps.AppsResourceWithStreamingResponse(client.apps)
        self.prompts = prompts.PromptsResourceWithStreamingResponse(client.prompts)


class AsyncPatronusAPIWithStreamedResponse:
    def __init__(self, client: AsyncPatronusAPI) -> None:
        self.evaluator_criteria = evaluator_criteria.AsyncEvaluatorCriteriaResourceWithStreamingResponse(
            client.evaluator_criteria
        )
        self.experiments = experiments.AsyncExperimentsResourceWithStreamingResponse(client.experiments)
        self.projects = projects.AsyncProjectsResourceWithStreamingResponse(client.projects)
        self.evaluations = evaluations.AsyncEvaluationsResourceWithStreamingResponse(client.evaluations)
        self.otel = otel.AsyncOtelResourceWithStreamingResponse(client.otel)
        self.trace_insight = trace_insight.AsyncTraceInsightResourceWithStreamingResponse(client.trace_insight)
        self.evaluators = evaluators.AsyncEvaluatorsResourceWithStreamingResponse(client.evaluators)
        self.whoami = whoami.AsyncWhoamiResourceWithStreamingResponse(client.whoami)
        self.apps = apps.AsyncAppsResourceWithStreamingResponse(client.apps)
        self.prompts = prompts.AsyncPromptsResourceWithStreamingResponse(client.prompts)


Client = PatronusAPI

AsyncClient = AsyncPatronusAPI
