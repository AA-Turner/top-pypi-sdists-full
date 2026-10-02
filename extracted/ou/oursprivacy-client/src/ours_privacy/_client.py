# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Mapping
from typing_extensions import Self, override

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
    from .resources import batch, track, visitor, experiments
    from .resources.batch import BatchResource, AsyncBatchResource
    from .resources.track import TrackResource, AsyncTrackResource
    from .resources.visitor import VisitorResource, AsyncVisitorResource
    from .resources.experiments import ExperimentsResource, AsyncExperimentsResource

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "OursPrivacy",
    "AsyncOursPrivacy",
    "Client",
    "AsyncClient",
]


class OursPrivacy(SyncAPIClient):
    # client options

    def __init__(
        self,
        *,
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
        """Construct a new synchronous OursPrivacy client instance."""
        if base_url is None:
            base_url = os.environ.get("OURS_PRIVACY_BASE_URL")
        self._base_url_overridden = base_url is not None
        if base_url is None:
            base_url = f"https://api.oursprivacy.com/api/v1"

        custom_headers_env = os.environ.get("OURS_PRIVACY_CUSTOM_HEADERS")
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

    @cached_property
    def batch(self) -> BatchResource:
        from .resources.batch import BatchResource

        return BatchResource(self)

    @cached_property
    def track(self) -> TrackResource:
        from .resources.track import TrackResource

        return TrackResource(self)

    @cached_property
    def visitor(self) -> VisitorResource:
        from .resources.visitor import VisitorResource

        return VisitorResource(self)

    @cached_property
    def experiments(self) -> ExperimentsResource:
        from .resources.experiments import ExperimentsResource

        return ExperimentsResource(self)

    @cached_property
    def with_raw_response(self) -> OursPrivacyWithRawResponse:
        return OursPrivacyWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OursPrivacyWithStreamedResponse:
        return OursPrivacyWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
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
        client = self.__class__(
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )
        client._base_url_overridden = self._base_url_overridden or base_url is not None
        return client

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


class AsyncOursPrivacy(AsyncAPIClient):
    # client options

    def __init__(
        self,
        *,
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
        """Construct a new async AsyncOursPrivacy client instance."""
        if base_url is None:
            base_url = os.environ.get("OURS_PRIVACY_BASE_URL")
        self._base_url_overridden = base_url is not None
        if base_url is None:
            base_url = f"https://api.oursprivacy.com/api/v1"

        custom_headers_env = os.environ.get("OURS_PRIVACY_CUSTOM_HEADERS")
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

    @cached_property
    def batch(self) -> AsyncBatchResource:
        from .resources.batch import AsyncBatchResource

        return AsyncBatchResource(self)

    @cached_property
    def track(self) -> AsyncTrackResource:
        from .resources.track import AsyncTrackResource

        return AsyncTrackResource(self)

    @cached_property
    def visitor(self) -> AsyncVisitorResource:
        from .resources.visitor import AsyncVisitorResource

        return AsyncVisitorResource(self)

    @cached_property
    def experiments(self) -> AsyncExperimentsResource:
        from .resources.experiments import AsyncExperimentsResource

        return AsyncExperimentsResource(self)

    @cached_property
    def with_raw_response(self) -> AsyncOursPrivacyWithRawResponse:
        return AsyncOursPrivacyWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOursPrivacyWithStreamedResponse:
        return AsyncOursPrivacyWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
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
        client = self.__class__(
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )
        client._base_url_overridden = self._base_url_overridden or base_url is not None
        return client

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


class OursPrivacyWithRawResponse:
    _client: OursPrivacy

    def __init__(self, client: OursPrivacy) -> None:
        self._client = client

    @cached_property
    def batch(self) -> batch.BatchResourceWithRawResponse:
        from .resources.batch import BatchResourceWithRawResponse

        return BatchResourceWithRawResponse(self._client.batch)

    @cached_property
    def track(self) -> track.TrackResourceWithRawResponse:
        from .resources.track import TrackResourceWithRawResponse

        return TrackResourceWithRawResponse(self._client.track)

    @cached_property
    def visitor(self) -> visitor.VisitorResourceWithRawResponse:
        from .resources.visitor import VisitorResourceWithRawResponse

        return VisitorResourceWithRawResponse(self._client.visitor)

    @cached_property
    def experiments(self) -> experiments.ExperimentsResourceWithRawResponse:
        from .resources.experiments import ExperimentsResourceWithRawResponse

        return ExperimentsResourceWithRawResponse(self._client.experiments)


class AsyncOursPrivacyWithRawResponse:
    _client: AsyncOursPrivacy

    def __init__(self, client: AsyncOursPrivacy) -> None:
        self._client = client

    @cached_property
    def batch(self) -> batch.AsyncBatchResourceWithRawResponse:
        from .resources.batch import AsyncBatchResourceWithRawResponse

        return AsyncBatchResourceWithRawResponse(self._client.batch)

    @cached_property
    def track(self) -> track.AsyncTrackResourceWithRawResponse:
        from .resources.track import AsyncTrackResourceWithRawResponse

        return AsyncTrackResourceWithRawResponse(self._client.track)

    @cached_property
    def visitor(self) -> visitor.AsyncVisitorResourceWithRawResponse:
        from .resources.visitor import AsyncVisitorResourceWithRawResponse

        return AsyncVisitorResourceWithRawResponse(self._client.visitor)

    @cached_property
    def experiments(self) -> experiments.AsyncExperimentsResourceWithRawResponse:
        from .resources.experiments import AsyncExperimentsResourceWithRawResponse

        return AsyncExperimentsResourceWithRawResponse(self._client.experiments)


class OursPrivacyWithStreamedResponse:
    _client: OursPrivacy

    def __init__(self, client: OursPrivacy) -> None:
        self._client = client

    @cached_property
    def batch(self) -> batch.BatchResourceWithStreamingResponse:
        from .resources.batch import BatchResourceWithStreamingResponse

        return BatchResourceWithStreamingResponse(self._client.batch)

    @cached_property
    def track(self) -> track.TrackResourceWithStreamingResponse:
        from .resources.track import TrackResourceWithStreamingResponse

        return TrackResourceWithStreamingResponse(self._client.track)

    @cached_property
    def visitor(self) -> visitor.VisitorResourceWithStreamingResponse:
        from .resources.visitor import VisitorResourceWithStreamingResponse

        return VisitorResourceWithStreamingResponse(self._client.visitor)

    @cached_property
    def experiments(self) -> experiments.ExperimentsResourceWithStreamingResponse:
        from .resources.experiments import ExperimentsResourceWithStreamingResponse

        return ExperimentsResourceWithStreamingResponse(self._client.experiments)


class AsyncOursPrivacyWithStreamedResponse:
    _client: AsyncOursPrivacy

    def __init__(self, client: AsyncOursPrivacy) -> None:
        self._client = client

    @cached_property
    def batch(self) -> batch.AsyncBatchResourceWithStreamingResponse:
        from .resources.batch import AsyncBatchResourceWithStreamingResponse

        return AsyncBatchResourceWithStreamingResponse(self._client.batch)

    @cached_property
    def track(self) -> track.AsyncTrackResourceWithStreamingResponse:
        from .resources.track import AsyncTrackResourceWithStreamingResponse

        return AsyncTrackResourceWithStreamingResponse(self._client.track)

    @cached_property
    def visitor(self) -> visitor.AsyncVisitorResourceWithStreamingResponse:
        from .resources.visitor import AsyncVisitorResourceWithStreamingResponse

        return AsyncVisitorResourceWithStreamingResponse(self._client.visitor)

    @cached_property
    def experiments(self) -> experiments.AsyncExperimentsResourceWithStreamingResponse:
        from .resources.experiments import AsyncExperimentsResourceWithStreamingResponse

        return AsyncExperimentsResourceWithStreamingResponse(self._client.experiments)


Client = OursPrivacy

AsyncClient = AsyncOursPrivacy
