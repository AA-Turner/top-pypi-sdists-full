# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
import base64
from typing import TYPE_CHECKING, Any, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    Omit,
    Headers,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    not_given,
)
from ._utils import (
    is_given,
    is_mapping_t,
    get_async_library,
)
from ._compat import cached_property
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

if TYPE_CHECKING:
    from .resources import (
        cases,
        scores,
        scorers,
        service,
        datasets,
        comparisons,
        eval_tables,
        evaluations,
        verification,
    )
    from .resources.cases import CasesResource, AsyncCasesResource
    from .resources.scores import ScoresResource, AsyncScoresResource
    from .resources.service import ServiceResource, AsyncServiceResource
    from .resources.comparisons import ComparisonsResource, AsyncComparisonsResource
    from .resources.verification import VerificationResource, AsyncVerificationResource
    from .resources.scorers.scorers import ScorersResource, AsyncScorersResource
    from .resources.datasets.datasets import DatasetsResource, AsyncDatasetsResource
    from .resources.eval_tables.eval_tables import EvalTablesResource, AsyncEvalTablesResource
    from .resources.evaluations.evaluations import EvaluationsResource, AsyncEvaluationsResource

__all__ = ["Timeout", "Transport", "ProxiesTypes", "RequestOptions", "Client", "AsyncClient"]


class Client(SyncAPIClient):
    # client options
    namespace: str | None
    scope_id: str | None
    bearer_token: str | None
    username: str | None
    api_key: str | None

    def __init__(
        self,
        *,
        namespace: str | None = "wandb",
        scope_id: str | None = None,
        bearer_token: str | None = None,
        username: str | None = "api",
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
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
        """Construct a new synchronous Client client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `bearer_token` from `WANDB_ACCESS_TOKEN`
        - `api_key` from `WANDB_API_KEY`
        """
        if namespace is None:
            namespace = "wandb"
        self.namespace = namespace

        self.scope_id = scope_id

        if bearer_token is None:
            bearer_token = os.environ.get("WANDB_ACCESS_TOKEN")
        self.bearer_token = bearer_token

        if username is None:
            username = "api"
        self.username = username

        if api_key is None:
            api_key = os.environ.get("WANDB_API_KEY")
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("CES_BASE_URL")
        if base_url is None:
            base_url = f"http://localhost:9300"

        custom_headers_env = os.environ.get("CES_CUSTOM_HEADERS")
        if custom_headers_env is not None:
            parsed: dict[str, str] = {}
            for line in custom_headers_env.split("\n"):
                colon = line.find(":")
                if colon >= 0:
                    parsed[line[:colon].strip()] = line[colon + 1 :].strip()
            default_headers = {**parsed, **(default_headers if is_mapping_t(default_headers) else {})}

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

        self._idempotency_header = "Idempotency-Key"

    @cached_property
    def service(self) -> ServiceResource:
        from .resources.service import ServiceResource

        return ServiceResource(self)

    @cached_property
    def verification(self) -> VerificationResource:
        from .resources.verification import VerificationResource

        return VerificationResource(self)

    @cached_property
    def datasets(self) -> DatasetsResource:
        from .resources.datasets import DatasetsResource

        return DatasetsResource(self)

    @cached_property
    def cases(self) -> CasesResource:
        from .resources.cases import CasesResource

        return CasesResource(self)

    @cached_property
    def comparisons(self) -> ComparisonsResource:
        from .resources.comparisons import ComparisonsResource

        return ComparisonsResource(self)

    @cached_property
    def scorers(self) -> ScorersResource:
        from .resources.scorers import ScorersResource

        return ScorersResource(self)

    @cached_property
    def scores(self) -> ScoresResource:
        from .resources.scores import ScoresResource

        return ScoresResource(self)

    @cached_property
    def evaluations(self) -> EvaluationsResource:
        from .resources.evaluations import EvaluationsResource

        return EvaluationsResource(self)

    @cached_property
    def eval_tables(self) -> EvalTablesResource:
        from .resources.eval_tables import EvalTablesResource

        return EvalTablesResource(self)

    @cached_property
    def with_raw_response(self) -> ClientWithRawResponse:
        return ClientWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ClientWithStreamedResponse:
        return ClientWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {**self._wandb_basic_auth, **self._wandb_bearer_auth}

    @property
    def _wandb_basic_auth(self) -> dict[str, str]:
        if self.username is None:
            return {}
        if self.api_key is None:
            return {}
        credentials = f"{self.username}:{self.api_key}".encode("ascii")
        header = f"Basic {base64.b64encode(credentials).decode('ascii')}"
        return {"Authorization": header}

    @property
    def _wandb_bearer_auth(self) -> dict[str, str]:
        bearer_token = self.bearer_token
        if bearer_token is None:
            return {}
        return {"Authorization": f"Bearer {bearer_token}"}

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
        if headers.get("Authorization") or isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected either username, api_key or bearer_token to be set. Or for one of the `Authorization` or `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        bearer_token: str | None = None,
        username: str | None = None,
        api_key: str | None = None,
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
            namespace=namespace or self.namespace,
            scope_id=scope_id or self.scope_id,
            bearer_token=bearer_token or self.bearer_token,
            username=username or self.username,
            api_key=api_key or self.api_key,
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

    def _get_namespace_path_param(self) -> str:
        from_client = self.namespace
        if from_client is not None:
            return from_client

        raise ValueError(
            "Missing namespace argument; Please provide it at the client level, e.g. Client(namespace='abcd') or per method."
        )

    def _get_scope_id_path_param(self) -> str:
        from_client = self.scope_id
        if from_client is not None:
            return from_client

        raise ValueError(
            "Missing scope_id argument; Please provide it at the client level, e.g. Client(scope_id='abcd') or per method."
        )

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


class AsyncClient(AsyncAPIClient):
    # client options
    namespace: str | None
    scope_id: str | None
    bearer_token: str | None
    username: str | None
    api_key: str | None

    def __init__(
        self,
        *,
        namespace: str | None = "wandb",
        scope_id: str | None = None,
        bearer_token: str | None = None,
        username: str | None = "api",
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
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
        """Construct a new async AsyncClient client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `bearer_token` from `WANDB_ACCESS_TOKEN`
        - `api_key` from `WANDB_API_KEY`
        """
        if namespace is None:
            namespace = "wandb"
        self.namespace = namespace

        self.scope_id = scope_id

        if bearer_token is None:
            bearer_token = os.environ.get("WANDB_ACCESS_TOKEN")
        self.bearer_token = bearer_token

        if username is None:
            username = "api"
        self.username = username

        if api_key is None:
            api_key = os.environ.get("WANDB_API_KEY")
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("CES_BASE_URL")
        if base_url is None:
            base_url = f"http://localhost:9300"

        custom_headers_env = os.environ.get("CES_CUSTOM_HEADERS")
        if custom_headers_env is not None:
            parsed: dict[str, str] = {}
            for line in custom_headers_env.split("\n"):
                colon = line.find(":")
                if colon >= 0:
                    parsed[line[:colon].strip()] = line[colon + 1 :].strip()
            default_headers = {**parsed, **(default_headers if is_mapping_t(default_headers) else {})}

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

        self._idempotency_header = "Idempotency-Key"

    @cached_property
    def service(self) -> AsyncServiceResource:
        from .resources.service import AsyncServiceResource

        return AsyncServiceResource(self)

    @cached_property
    def verification(self) -> AsyncVerificationResource:
        from .resources.verification import AsyncVerificationResource

        return AsyncVerificationResource(self)

    @cached_property
    def datasets(self) -> AsyncDatasetsResource:
        from .resources.datasets import AsyncDatasetsResource

        return AsyncDatasetsResource(self)

    @cached_property
    def cases(self) -> AsyncCasesResource:
        from .resources.cases import AsyncCasesResource

        return AsyncCasesResource(self)

    @cached_property
    def comparisons(self) -> AsyncComparisonsResource:
        from .resources.comparisons import AsyncComparisonsResource

        return AsyncComparisonsResource(self)

    @cached_property
    def scorers(self) -> AsyncScorersResource:
        from .resources.scorers import AsyncScorersResource

        return AsyncScorersResource(self)

    @cached_property
    def scores(self) -> AsyncScoresResource:
        from .resources.scores import AsyncScoresResource

        return AsyncScoresResource(self)

    @cached_property
    def evaluations(self) -> AsyncEvaluationsResource:
        from .resources.evaluations import AsyncEvaluationsResource

        return AsyncEvaluationsResource(self)

    @cached_property
    def eval_tables(self) -> AsyncEvalTablesResource:
        from .resources.eval_tables import AsyncEvalTablesResource

        return AsyncEvalTablesResource(self)

    @cached_property
    def with_raw_response(self) -> AsyncClientWithRawResponse:
        return AsyncClientWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncClientWithStreamedResponse:
        return AsyncClientWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {**self._wandb_basic_auth, **self._wandb_bearer_auth}

    @property
    def _wandb_basic_auth(self) -> dict[str, str]:
        if self.username is None:
            return {}
        if self.api_key is None:
            return {}
        credentials = f"{self.username}:{self.api_key}".encode("ascii")
        header = f"Basic {base64.b64encode(credentials).decode('ascii')}"
        return {"Authorization": header}

    @property
    def _wandb_bearer_auth(self) -> dict[str, str]:
        bearer_token = self.bearer_token
        if bearer_token is None:
            return {}
        return {"Authorization": f"Bearer {bearer_token}"}

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
        if headers.get("Authorization") or isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected either username, api_key or bearer_token to be set. Or for one of the `Authorization` or `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        bearer_token: str | None = None,
        username: str | None = None,
        api_key: str | None = None,
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
            namespace=namespace or self.namespace,
            scope_id=scope_id or self.scope_id,
            bearer_token=bearer_token or self.bearer_token,
            username=username or self.username,
            api_key=api_key or self.api_key,
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

    def _get_namespace_path_param(self) -> str:
        from_client = self.namespace
        if from_client is not None:
            return from_client

        raise ValueError(
            "Missing namespace argument; Please provide it at the client level, e.g. AsyncClient(namespace='abcd') or per method."
        )

    def _get_scope_id_path_param(self) -> str:
        from_client = self.scope_id
        if from_client is not None:
            return from_client

        raise ValueError(
            "Missing scope_id argument; Please provide it at the client level, e.g. AsyncClient(scope_id='abcd') or per method."
        )

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


class ClientWithRawResponse:
    _client: Client

    def __init__(self, client: Client) -> None:
        self._client = client

    @cached_property
    def service(self) -> service.ServiceResourceWithRawResponse:
        from .resources.service import ServiceResourceWithRawResponse

        return ServiceResourceWithRawResponse(self._client.service)

    @cached_property
    def verification(self) -> verification.VerificationResourceWithRawResponse:
        from .resources.verification import VerificationResourceWithRawResponse

        return VerificationResourceWithRawResponse(self._client.verification)

    @cached_property
    def datasets(self) -> datasets.DatasetsResourceWithRawResponse:
        from .resources.datasets import DatasetsResourceWithRawResponse

        return DatasetsResourceWithRawResponse(self._client.datasets)

    @cached_property
    def cases(self) -> cases.CasesResourceWithRawResponse:
        from .resources.cases import CasesResourceWithRawResponse

        return CasesResourceWithRawResponse(self._client.cases)

    @cached_property
    def comparisons(self) -> comparisons.ComparisonsResourceWithRawResponse:
        from .resources.comparisons import ComparisonsResourceWithRawResponse

        return ComparisonsResourceWithRawResponse(self._client.comparisons)

    @cached_property
    def scorers(self) -> scorers.ScorersResourceWithRawResponse:
        from .resources.scorers import ScorersResourceWithRawResponse

        return ScorersResourceWithRawResponse(self._client.scorers)

    @cached_property
    def scores(self) -> scores.ScoresResourceWithRawResponse:
        from .resources.scores import ScoresResourceWithRawResponse

        return ScoresResourceWithRawResponse(self._client.scores)

    @cached_property
    def evaluations(self) -> evaluations.EvaluationsResourceWithRawResponse:
        from .resources.evaluations import EvaluationsResourceWithRawResponse

        return EvaluationsResourceWithRawResponse(self._client.evaluations)

    @cached_property
    def eval_tables(self) -> eval_tables.EvalTablesResourceWithRawResponse:
        from .resources.eval_tables import EvalTablesResourceWithRawResponse

        return EvalTablesResourceWithRawResponse(self._client.eval_tables)


class AsyncClientWithRawResponse:
    _client: AsyncClient

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    @cached_property
    def service(self) -> service.AsyncServiceResourceWithRawResponse:
        from .resources.service import AsyncServiceResourceWithRawResponse

        return AsyncServiceResourceWithRawResponse(self._client.service)

    @cached_property
    def verification(self) -> verification.AsyncVerificationResourceWithRawResponse:
        from .resources.verification import AsyncVerificationResourceWithRawResponse

        return AsyncVerificationResourceWithRawResponse(self._client.verification)

    @cached_property
    def datasets(self) -> datasets.AsyncDatasetsResourceWithRawResponse:
        from .resources.datasets import AsyncDatasetsResourceWithRawResponse

        return AsyncDatasetsResourceWithRawResponse(self._client.datasets)

    @cached_property
    def cases(self) -> cases.AsyncCasesResourceWithRawResponse:
        from .resources.cases import AsyncCasesResourceWithRawResponse

        return AsyncCasesResourceWithRawResponse(self._client.cases)

    @cached_property
    def comparisons(self) -> comparisons.AsyncComparisonsResourceWithRawResponse:
        from .resources.comparisons import AsyncComparisonsResourceWithRawResponse

        return AsyncComparisonsResourceWithRawResponse(self._client.comparisons)

    @cached_property
    def scorers(self) -> scorers.AsyncScorersResourceWithRawResponse:
        from .resources.scorers import AsyncScorersResourceWithRawResponse

        return AsyncScorersResourceWithRawResponse(self._client.scorers)

    @cached_property
    def scores(self) -> scores.AsyncScoresResourceWithRawResponse:
        from .resources.scores import AsyncScoresResourceWithRawResponse

        return AsyncScoresResourceWithRawResponse(self._client.scores)

    @cached_property
    def evaluations(self) -> evaluations.AsyncEvaluationsResourceWithRawResponse:
        from .resources.evaluations import AsyncEvaluationsResourceWithRawResponse

        return AsyncEvaluationsResourceWithRawResponse(self._client.evaluations)

    @cached_property
    def eval_tables(self) -> eval_tables.AsyncEvalTablesResourceWithRawResponse:
        from .resources.eval_tables import AsyncEvalTablesResourceWithRawResponse

        return AsyncEvalTablesResourceWithRawResponse(self._client.eval_tables)


class ClientWithStreamedResponse:
    _client: Client

    def __init__(self, client: Client) -> None:
        self._client = client

    @cached_property
    def service(self) -> service.ServiceResourceWithStreamingResponse:
        from .resources.service import ServiceResourceWithStreamingResponse

        return ServiceResourceWithStreamingResponse(self._client.service)

    @cached_property
    def verification(self) -> verification.VerificationResourceWithStreamingResponse:
        from .resources.verification import VerificationResourceWithStreamingResponse

        return VerificationResourceWithStreamingResponse(self._client.verification)

    @cached_property
    def datasets(self) -> datasets.DatasetsResourceWithStreamingResponse:
        from .resources.datasets import DatasetsResourceWithStreamingResponse

        return DatasetsResourceWithStreamingResponse(self._client.datasets)

    @cached_property
    def cases(self) -> cases.CasesResourceWithStreamingResponse:
        from .resources.cases import CasesResourceWithStreamingResponse

        return CasesResourceWithStreamingResponse(self._client.cases)

    @cached_property
    def comparisons(self) -> comparisons.ComparisonsResourceWithStreamingResponse:
        from .resources.comparisons import ComparisonsResourceWithStreamingResponse

        return ComparisonsResourceWithStreamingResponse(self._client.comparisons)

    @cached_property
    def scorers(self) -> scorers.ScorersResourceWithStreamingResponse:
        from .resources.scorers import ScorersResourceWithStreamingResponse

        return ScorersResourceWithStreamingResponse(self._client.scorers)

    @cached_property
    def scores(self) -> scores.ScoresResourceWithStreamingResponse:
        from .resources.scores import ScoresResourceWithStreamingResponse

        return ScoresResourceWithStreamingResponse(self._client.scores)

    @cached_property
    def evaluations(self) -> evaluations.EvaluationsResourceWithStreamingResponse:
        from .resources.evaluations import EvaluationsResourceWithStreamingResponse

        return EvaluationsResourceWithStreamingResponse(self._client.evaluations)

    @cached_property
    def eval_tables(self) -> eval_tables.EvalTablesResourceWithStreamingResponse:
        from .resources.eval_tables import EvalTablesResourceWithStreamingResponse

        return EvalTablesResourceWithStreamingResponse(self._client.eval_tables)


class AsyncClientWithStreamedResponse:
    _client: AsyncClient

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    @cached_property
    def service(self) -> service.AsyncServiceResourceWithStreamingResponse:
        from .resources.service import AsyncServiceResourceWithStreamingResponse

        return AsyncServiceResourceWithStreamingResponse(self._client.service)

    @cached_property
    def verification(self) -> verification.AsyncVerificationResourceWithStreamingResponse:
        from .resources.verification import AsyncVerificationResourceWithStreamingResponse

        return AsyncVerificationResourceWithStreamingResponse(self._client.verification)

    @cached_property
    def datasets(self) -> datasets.AsyncDatasetsResourceWithStreamingResponse:
        from .resources.datasets import AsyncDatasetsResourceWithStreamingResponse

        return AsyncDatasetsResourceWithStreamingResponse(self._client.datasets)

    @cached_property
    def cases(self) -> cases.AsyncCasesResourceWithStreamingResponse:
        from .resources.cases import AsyncCasesResourceWithStreamingResponse

        return AsyncCasesResourceWithStreamingResponse(self._client.cases)

    @cached_property
    def comparisons(self) -> comparisons.AsyncComparisonsResourceWithStreamingResponse:
        from .resources.comparisons import AsyncComparisonsResourceWithStreamingResponse

        return AsyncComparisonsResourceWithStreamingResponse(self._client.comparisons)

    @cached_property
    def scorers(self) -> scorers.AsyncScorersResourceWithStreamingResponse:
        from .resources.scorers import AsyncScorersResourceWithStreamingResponse

        return AsyncScorersResourceWithStreamingResponse(self._client.scorers)

    @cached_property
    def scores(self) -> scores.AsyncScoresResourceWithStreamingResponse:
        from .resources.scores import AsyncScoresResourceWithStreamingResponse

        return AsyncScoresResourceWithStreamingResponse(self._client.scores)

    @cached_property
    def evaluations(self) -> evaluations.AsyncEvaluationsResourceWithStreamingResponse:
        from .resources.evaluations import AsyncEvaluationsResourceWithStreamingResponse

        return AsyncEvaluationsResourceWithStreamingResponse(self._client.evaluations)

    @cached_property
    def eval_tables(self) -> eval_tables.AsyncEvalTablesResourceWithStreamingResponse:
        from .resources.eval_tables import AsyncEvalTablesResourceWithStreamingResponse

        return AsyncEvalTablesResourceWithStreamingResponse(self._client.eval_tables)


Client = Client

AsyncClient = AsyncClient
