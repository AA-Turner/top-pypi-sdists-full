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
from ._models import SecurityOptions
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

if TYPE_CHECKING:
    from .resources import cli, auth, admin, protein, predictions, share_links, small_molecule
    from .resources.cli import CliResource, AsyncCliResource
    from .resources.auth import AuthResource, AsyncAuthResource
    from .resources.admin.admin import AdminResource, AsyncAdminResource
    from .resources.share_links import ShareLinksResource, AsyncShareLinksResource
    from .resources.protein.protein import ProteinResource, AsyncProteinResource
    from .resources.predictions.predictions import PredictionsResource, AsyncPredictionsResource
    from .resources.small_molecule.small_molecule import SmallMoleculeResource, AsyncSmallMoleculeResource

__all__ = ["Timeout", "Transport", "ProxiesTypes", "RequestOptions", "Boltz", "AsyncBoltz", "Client", "AsyncClient"]

# <boltz-api-custom-code>
if TYPE_CHECKING:
    from .experiments import ExperimentsNamespace
# </boltz-api-custom-code>


class Boltz(SyncAPIClient):
    # client options
    api_key: str | None

    def __init__(
        self,
        *,
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
        """Construct a new synchronous Boltz client instance.

        This automatically infers the `api_key` argument from the `BOLTZ_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("BOLTZ_API_KEY")
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("BOLTZ_BASE_URL")
        if base_url is None:
            base_url = f"https://api.boltz.bio"

        custom_headers_env = os.environ.get("BOLTZ_CUSTOM_HEADERS")
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
    def predictions(self) -> PredictionsResource:
        """Run prediction models on molecular inputs.

        Each application is available as its own endpoint with application-specific inputs and outputs.
        """
        from .resources.predictions import PredictionsResource

        return PredictionsResource(self)

    @cached_property
    def small_molecule(self) -> SmallMoleculeResource:
        """
        Small Molecule Pipeline: design novel small molecules and screen compound libraries against protein targets. Includes de novo generation and virtual screening.
        """
        from .resources.small_molecule import SmallMoleculeResource

        return SmallMoleculeResource(self)

    @cached_property
    def protein(self) -> ProteinResource:
        """
        Design novel protein binders, redesign selected residues in fixed structures, and screen protein libraries against targets.
        """
        from .resources.protein import ProteinResource

        return ProteinResource(self)

    @cached_property
    def share_links(self) -> ShareLinksResource:
        """
        Share read-only access to predictions and pipeline runs by issuing time-limited links that visitors can open without an API key or, for email-restricted links, after signing in with an allowed email. A share link is scoped to a single workspace and bundles one or more predictions and pipeline runs. The link ID is itself the bearer credential; treat it as a secret. Create, retrieve, and archive require an API key or supported OAuth bearer token with read permission on every referenced resource. Retrieving metadata remains available after expiry or archive. Viewing content and listing shared pipeline results are gated by the link ID and the link's access mode. Archiving a link revokes public access immediately; subsequent content reads return 404. The underlying predictions and pipelines are unaffected and remain accessible through their own authenticated endpoints.
        """
        from .resources.share_links import ShareLinksResource

        return ShareLinksResource(self)

    @cached_property
    def admin(self) -> AdminResource:
        """Manage workspaces and API keys.

        Requires an admin API key. Admin keys have full access to all management and compute operations across all workspaces in the organization.
        """
        from .resources.admin import AdminResource

        return AdminResource(self)

    @cached_property
    def cli(self) -> CliResource:
        """
        Check the installed boltz-api CLI version against the currently published CLI release and the minimum version supported by the Boltz API.
        """
        from .resources.cli import CliResource

        return CliResource(self)

    @cached_property
    def auth(self) -> AuthResource:
        """
        Inspect the authentication context for the current credential, including the organization or workspace scope for API keys and the available organization memberships for OAuth bearer tokens. OAuth callers can use this information to choose which organization to send with future requests.
        """
        from .resources.auth import AuthResource

        return AuthResource(self)

    @cached_property
    def with_raw_response(self) -> BoltzWithRawResponse:
        return BoltzWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BoltzWithStreamedResponse:
        return BoltzWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="repeat")

    @override
    def _auth_headers(self, security: SecurityOptions) -> dict[str, str]:
        headers: dict[str, str] = {}
        if security.get("api_key_auth", False):
            for key, value in self._api_key_auth.items():
                headers.setdefault(key, value)
        return headers

    @property
    def _api_key_auth(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"x-api-key": api_key}

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
        if headers.get("x-api-key") or isinstance(custom_headers.get("x-api-key"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected the api_key to be set. Or for the `x-api-key` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
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

    # <boltz-api-custom-code>
    @cached_property
    def experiments(self) -> ExperimentsNamespace:
        """Scientist-facing notebook and script workflows.

        This namespace is intentionally synchronous in v1. Async parity will be
        added separately rather than exposing a partial async surface.
        """
        from .experiments import ExperimentsNamespace

        return ExperimentsNamespace(self)

    # </boltz-api-custom-code>

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


class AsyncBoltz(AsyncAPIClient):
    # client options
    api_key: str | None

    def __init__(
        self,
        *,
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
        """Construct a new async AsyncBoltz client instance.

        This automatically infers the `api_key` argument from the `BOLTZ_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("BOLTZ_API_KEY")
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("BOLTZ_BASE_URL")
        if base_url is None:
            base_url = f"https://api.boltz.bio"

        custom_headers_env = os.environ.get("BOLTZ_CUSTOM_HEADERS")
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
    def predictions(self) -> AsyncPredictionsResource:
        """Run prediction models on molecular inputs.

        Each application is available as its own endpoint with application-specific inputs and outputs.
        """
        from .resources.predictions import AsyncPredictionsResource

        return AsyncPredictionsResource(self)

    @cached_property
    def small_molecule(self) -> AsyncSmallMoleculeResource:
        """
        Small Molecule Pipeline: design novel small molecules and screen compound libraries against protein targets. Includes de novo generation and virtual screening.
        """
        from .resources.small_molecule import AsyncSmallMoleculeResource

        return AsyncSmallMoleculeResource(self)

    @cached_property
    def protein(self) -> AsyncProteinResource:
        """
        Design novel protein binders, redesign selected residues in fixed structures, and screen protein libraries against targets.
        """
        from .resources.protein import AsyncProteinResource

        return AsyncProteinResource(self)

    @cached_property
    def share_links(self) -> AsyncShareLinksResource:
        """
        Share read-only access to predictions and pipeline runs by issuing time-limited links that visitors can open without an API key or, for email-restricted links, after signing in with an allowed email. A share link is scoped to a single workspace and bundles one or more predictions and pipeline runs. The link ID is itself the bearer credential; treat it as a secret. Create, retrieve, and archive require an API key or supported OAuth bearer token with read permission on every referenced resource. Retrieving metadata remains available after expiry or archive. Viewing content and listing shared pipeline results are gated by the link ID and the link's access mode. Archiving a link revokes public access immediately; subsequent content reads return 404. The underlying predictions and pipelines are unaffected and remain accessible through their own authenticated endpoints.
        """
        from .resources.share_links import AsyncShareLinksResource

        return AsyncShareLinksResource(self)

    @cached_property
    def admin(self) -> AsyncAdminResource:
        """Manage workspaces and API keys.

        Requires an admin API key. Admin keys have full access to all management and compute operations across all workspaces in the organization.
        """
        from .resources.admin import AsyncAdminResource

        return AsyncAdminResource(self)

    @cached_property
    def cli(self) -> AsyncCliResource:
        """
        Check the installed boltz-api CLI version against the currently published CLI release and the minimum version supported by the Boltz API.
        """
        from .resources.cli import AsyncCliResource

        return AsyncCliResource(self)

    @cached_property
    def auth(self) -> AsyncAuthResource:
        """
        Inspect the authentication context for the current credential, including the organization or workspace scope for API keys and the available organization memberships for OAuth bearer tokens. OAuth callers can use this information to choose which organization to send with future requests.
        """
        from .resources.auth import AsyncAuthResource

        return AsyncAuthResource(self)

    @cached_property
    def with_raw_response(self) -> AsyncBoltzWithRawResponse:
        return AsyncBoltzWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBoltzWithStreamedResponse:
        return AsyncBoltzWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="repeat")

    @override
    def _auth_headers(self, security: SecurityOptions) -> dict[str, str]:
        headers: dict[str, str] = {}
        if security.get("api_key_auth", False):
            for key, value in self._api_key_auth.items():
                headers.setdefault(key, value)
        return headers

    @property
    def _api_key_auth(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"x-api-key": api_key}

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
        if headers.get("x-api-key") or isinstance(custom_headers.get("x-api-key"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected the api_key to be set. Or for the `x-api-key` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
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


class BoltzWithRawResponse:
    _client: Boltz

    def __init__(self, client: Boltz) -> None:
        self._client = client

    @cached_property
    def predictions(self) -> predictions.PredictionsResourceWithRawResponse:
        """Run prediction models on molecular inputs.

        Each application is available as its own endpoint with application-specific inputs and outputs.
        """
        from .resources.predictions import PredictionsResourceWithRawResponse

        return PredictionsResourceWithRawResponse(self._client.predictions)

    @cached_property
    def small_molecule(self) -> small_molecule.SmallMoleculeResourceWithRawResponse:
        """
        Small Molecule Pipeline: design novel small molecules and screen compound libraries against protein targets. Includes de novo generation and virtual screening.
        """
        from .resources.small_molecule import SmallMoleculeResourceWithRawResponse

        return SmallMoleculeResourceWithRawResponse(self._client.small_molecule)

    @cached_property
    def protein(self) -> protein.ProteinResourceWithRawResponse:
        """
        Design novel protein binders, redesign selected residues in fixed structures, and screen protein libraries against targets.
        """
        from .resources.protein import ProteinResourceWithRawResponse

        return ProteinResourceWithRawResponse(self._client.protein)

    @cached_property
    def share_links(self) -> share_links.ShareLinksResourceWithRawResponse:
        """
        Share read-only access to predictions and pipeline runs by issuing time-limited links that visitors can open without an API key or, for email-restricted links, after signing in with an allowed email. A share link is scoped to a single workspace and bundles one or more predictions and pipeline runs. The link ID is itself the bearer credential; treat it as a secret. Create, retrieve, and archive require an API key or supported OAuth bearer token with read permission on every referenced resource. Retrieving metadata remains available after expiry or archive. Viewing content and listing shared pipeline results are gated by the link ID and the link's access mode. Archiving a link revokes public access immediately; subsequent content reads return 404. The underlying predictions and pipelines are unaffected and remain accessible through their own authenticated endpoints.
        """
        from .resources.share_links import ShareLinksResourceWithRawResponse

        return ShareLinksResourceWithRawResponse(self._client.share_links)

    @cached_property
    def admin(self) -> admin.AdminResourceWithRawResponse:
        """Manage workspaces and API keys.

        Requires an admin API key. Admin keys have full access to all management and compute operations across all workspaces in the organization.
        """
        from .resources.admin import AdminResourceWithRawResponse

        return AdminResourceWithRawResponse(self._client.admin)

    @cached_property
    def cli(self) -> cli.CliResourceWithRawResponse:
        """
        Check the installed boltz-api CLI version against the currently published CLI release and the minimum version supported by the Boltz API.
        """
        from .resources.cli import CliResourceWithRawResponse

        return CliResourceWithRawResponse(self._client.cli)

    @cached_property
    def auth(self) -> auth.AuthResourceWithRawResponse:
        """
        Inspect the authentication context for the current credential, including the organization or workspace scope for API keys and the available organization memberships for OAuth bearer tokens. OAuth callers can use this information to choose which organization to send with future requests.
        """
        from .resources.auth import AuthResourceWithRawResponse

        return AuthResourceWithRawResponse(self._client.auth)


class AsyncBoltzWithRawResponse:
    _client: AsyncBoltz

    def __init__(self, client: AsyncBoltz) -> None:
        self._client = client

    @cached_property
    def predictions(self) -> predictions.AsyncPredictionsResourceWithRawResponse:
        """Run prediction models on molecular inputs.

        Each application is available as its own endpoint with application-specific inputs and outputs.
        """
        from .resources.predictions import AsyncPredictionsResourceWithRawResponse

        return AsyncPredictionsResourceWithRawResponse(self._client.predictions)

    @cached_property
    def small_molecule(self) -> small_molecule.AsyncSmallMoleculeResourceWithRawResponse:
        """
        Small Molecule Pipeline: design novel small molecules and screen compound libraries against protein targets. Includes de novo generation and virtual screening.
        """
        from .resources.small_molecule import AsyncSmallMoleculeResourceWithRawResponse

        return AsyncSmallMoleculeResourceWithRawResponse(self._client.small_molecule)

    @cached_property
    def protein(self) -> protein.AsyncProteinResourceWithRawResponse:
        """
        Design novel protein binders, redesign selected residues in fixed structures, and screen protein libraries against targets.
        """
        from .resources.protein import AsyncProteinResourceWithRawResponse

        return AsyncProteinResourceWithRawResponse(self._client.protein)

    @cached_property
    def share_links(self) -> share_links.AsyncShareLinksResourceWithRawResponse:
        """
        Share read-only access to predictions and pipeline runs by issuing time-limited links that visitors can open without an API key or, for email-restricted links, after signing in with an allowed email. A share link is scoped to a single workspace and bundles one or more predictions and pipeline runs. The link ID is itself the bearer credential; treat it as a secret. Create, retrieve, and archive require an API key or supported OAuth bearer token with read permission on every referenced resource. Retrieving metadata remains available after expiry or archive. Viewing content and listing shared pipeline results are gated by the link ID and the link's access mode. Archiving a link revokes public access immediately; subsequent content reads return 404. The underlying predictions and pipelines are unaffected and remain accessible through their own authenticated endpoints.
        """
        from .resources.share_links import AsyncShareLinksResourceWithRawResponse

        return AsyncShareLinksResourceWithRawResponse(self._client.share_links)

    @cached_property
    def admin(self) -> admin.AsyncAdminResourceWithRawResponse:
        """Manage workspaces and API keys.

        Requires an admin API key. Admin keys have full access to all management and compute operations across all workspaces in the organization.
        """
        from .resources.admin import AsyncAdminResourceWithRawResponse

        return AsyncAdminResourceWithRawResponse(self._client.admin)

    @cached_property
    def cli(self) -> cli.AsyncCliResourceWithRawResponse:
        """
        Check the installed boltz-api CLI version against the currently published CLI release and the minimum version supported by the Boltz API.
        """
        from .resources.cli import AsyncCliResourceWithRawResponse

        return AsyncCliResourceWithRawResponse(self._client.cli)

    @cached_property
    def auth(self) -> auth.AsyncAuthResourceWithRawResponse:
        """
        Inspect the authentication context for the current credential, including the organization or workspace scope for API keys and the available organization memberships for OAuth bearer tokens. OAuth callers can use this information to choose which organization to send with future requests.
        """
        from .resources.auth import AsyncAuthResourceWithRawResponse

        return AsyncAuthResourceWithRawResponse(self._client.auth)


class BoltzWithStreamedResponse:
    _client: Boltz

    def __init__(self, client: Boltz) -> None:
        self._client = client

    @cached_property
    def predictions(self) -> predictions.PredictionsResourceWithStreamingResponse:
        """Run prediction models on molecular inputs.

        Each application is available as its own endpoint with application-specific inputs and outputs.
        """
        from .resources.predictions import PredictionsResourceWithStreamingResponse

        return PredictionsResourceWithStreamingResponse(self._client.predictions)

    @cached_property
    def small_molecule(self) -> small_molecule.SmallMoleculeResourceWithStreamingResponse:
        """
        Small Molecule Pipeline: design novel small molecules and screen compound libraries against protein targets. Includes de novo generation and virtual screening.
        """
        from .resources.small_molecule import SmallMoleculeResourceWithStreamingResponse

        return SmallMoleculeResourceWithStreamingResponse(self._client.small_molecule)

    @cached_property
    def protein(self) -> protein.ProteinResourceWithStreamingResponse:
        """
        Design novel protein binders, redesign selected residues in fixed structures, and screen protein libraries against targets.
        """
        from .resources.protein import ProteinResourceWithStreamingResponse

        return ProteinResourceWithStreamingResponse(self._client.protein)

    @cached_property
    def share_links(self) -> share_links.ShareLinksResourceWithStreamingResponse:
        """
        Share read-only access to predictions and pipeline runs by issuing time-limited links that visitors can open without an API key or, for email-restricted links, after signing in with an allowed email. A share link is scoped to a single workspace and bundles one or more predictions and pipeline runs. The link ID is itself the bearer credential; treat it as a secret. Create, retrieve, and archive require an API key or supported OAuth bearer token with read permission on every referenced resource. Retrieving metadata remains available after expiry or archive. Viewing content and listing shared pipeline results are gated by the link ID and the link's access mode. Archiving a link revokes public access immediately; subsequent content reads return 404. The underlying predictions and pipelines are unaffected and remain accessible through their own authenticated endpoints.
        """
        from .resources.share_links import ShareLinksResourceWithStreamingResponse

        return ShareLinksResourceWithStreamingResponse(self._client.share_links)

    @cached_property
    def admin(self) -> admin.AdminResourceWithStreamingResponse:
        """Manage workspaces and API keys.

        Requires an admin API key. Admin keys have full access to all management and compute operations across all workspaces in the organization.
        """
        from .resources.admin import AdminResourceWithStreamingResponse

        return AdminResourceWithStreamingResponse(self._client.admin)

    @cached_property
    def cli(self) -> cli.CliResourceWithStreamingResponse:
        """
        Check the installed boltz-api CLI version against the currently published CLI release and the minimum version supported by the Boltz API.
        """
        from .resources.cli import CliResourceWithStreamingResponse

        return CliResourceWithStreamingResponse(self._client.cli)

    @cached_property
    def auth(self) -> auth.AuthResourceWithStreamingResponse:
        """
        Inspect the authentication context for the current credential, including the organization or workspace scope for API keys and the available organization memberships for OAuth bearer tokens. OAuth callers can use this information to choose which organization to send with future requests.
        """
        from .resources.auth import AuthResourceWithStreamingResponse

        return AuthResourceWithStreamingResponse(self._client.auth)


class AsyncBoltzWithStreamedResponse:
    _client: AsyncBoltz

    def __init__(self, client: AsyncBoltz) -> None:
        self._client = client

    @cached_property
    def predictions(self) -> predictions.AsyncPredictionsResourceWithStreamingResponse:
        """Run prediction models on molecular inputs.

        Each application is available as its own endpoint with application-specific inputs and outputs.
        """
        from .resources.predictions import AsyncPredictionsResourceWithStreamingResponse

        return AsyncPredictionsResourceWithStreamingResponse(self._client.predictions)

    @cached_property
    def small_molecule(self) -> small_molecule.AsyncSmallMoleculeResourceWithStreamingResponse:
        """
        Small Molecule Pipeline: design novel small molecules and screen compound libraries against protein targets. Includes de novo generation and virtual screening.
        """
        from .resources.small_molecule import AsyncSmallMoleculeResourceWithStreamingResponse

        return AsyncSmallMoleculeResourceWithStreamingResponse(self._client.small_molecule)

    @cached_property
    def protein(self) -> protein.AsyncProteinResourceWithStreamingResponse:
        """
        Design novel protein binders, redesign selected residues in fixed structures, and screen protein libraries against targets.
        """
        from .resources.protein import AsyncProteinResourceWithStreamingResponse

        return AsyncProteinResourceWithStreamingResponse(self._client.protein)

    @cached_property
    def share_links(self) -> share_links.AsyncShareLinksResourceWithStreamingResponse:
        """
        Share read-only access to predictions and pipeline runs by issuing time-limited links that visitors can open without an API key or, for email-restricted links, after signing in with an allowed email. A share link is scoped to a single workspace and bundles one or more predictions and pipeline runs. The link ID is itself the bearer credential; treat it as a secret. Create, retrieve, and archive require an API key or supported OAuth bearer token with read permission on every referenced resource. Retrieving metadata remains available after expiry or archive. Viewing content and listing shared pipeline results are gated by the link ID and the link's access mode. Archiving a link revokes public access immediately; subsequent content reads return 404. The underlying predictions and pipelines are unaffected and remain accessible through their own authenticated endpoints.
        """
        from .resources.share_links import AsyncShareLinksResourceWithStreamingResponse

        return AsyncShareLinksResourceWithStreamingResponse(self._client.share_links)

    @cached_property
    def admin(self) -> admin.AsyncAdminResourceWithStreamingResponse:
        """Manage workspaces and API keys.

        Requires an admin API key. Admin keys have full access to all management and compute operations across all workspaces in the organization.
        """
        from .resources.admin import AsyncAdminResourceWithStreamingResponse

        return AsyncAdminResourceWithStreamingResponse(self._client.admin)

    @cached_property
    def cli(self) -> cli.AsyncCliResourceWithStreamingResponse:
        """
        Check the installed boltz-api CLI version against the currently published CLI release and the minimum version supported by the Boltz API.
        """
        from .resources.cli import AsyncCliResourceWithStreamingResponse

        return AsyncCliResourceWithStreamingResponse(self._client.cli)

    @cached_property
    def auth(self) -> auth.AsyncAuthResourceWithStreamingResponse:
        """
        Inspect the authentication context for the current credential, including the organization or workspace scope for API keys and the available organization memberships for OAuth bearer tokens. OAuth callers can use this information to choose which organization to send with future requests.
        """
        from .resources.auth import AsyncAuthResourceWithStreamingResponse

        return AsyncAuthResourceWithStreamingResponse(self._client.auth)


Client = Boltz

AsyncClient = AsyncBoltz
