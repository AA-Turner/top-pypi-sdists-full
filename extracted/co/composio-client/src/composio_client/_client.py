"""``Composio`` and ``AsyncComposio`` — the entry points.

``Composio(auth=ProjectAuth(key)).tool_router.session.*``. ``auth`` is required
and says how the client authenticates (:mod:`._auth`); ``scope`` optionally
routes every request to an organization and project. The constructor reads
nothing from the process: :meth:`Composio.from_env` is the one reader of the
``COMPOSIO_*`` variables, and it takes the mapping as an argument.

Base-URL resolution: an explicit ``base_url`` wins over ``environment``, and
omitting both means production.

Everything here is hand-written except *which* resources hang off a client:
that inventory is generated into ``resources/_wiring.py`` from the same
operation plan the resource classes come from, and mixed in below, so widening
the surface never edits this module.
"""

from __future__ import annotations

import inspect
from collections.abc import Mapping
from types import TracebackType
from typing import Any, Literal

import httpx
from typing_extensions import Self

from ._auth import Auth, Scope, auth_from_credentials
from ._base_client import AsyncAPIClient, SyncAPIClient
from ._identity import ClientIdentity
from ._types import DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT, NOT_GIVEN, NotGiven
from ._version import __version__
from .resources._wiring import AsyncClientResources, ClientResources

ENVIRONMENTS: dict[str, str] = {
    "production": "https://backend.composio.dev",
    "staging": "https://staging-backend.composio.dev",
    "local": "http://localhost:9900",
}


def _parse_custom_headers(raw: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in raw.split("\n"):
        colon = line.find(":")
        if colon >= 0:
            parsed[line[:colon].strip()] = line[colon + 1 :].strip()
    return parsed


Environment = Literal["production", "staging", "local"]
EnvironmentMap = Mapping[str, str]
Timeout = float | httpx.Timeout | None


# ``inspect.signature`` is the slowest call on the ``with_options()`` path by an order
# of magnitude, and ``with_options`` is the documented in-loop idiom, so the
# answer is memoized per class. Bounded the same way the warn-once records
# are: test doubles create classes freely, and a cheap recompute on overflow
# beats unbounded retention.
_KEYWORD_CACHE: dict[tuple[type[Any], str], bool] = {}
_KEYWORD_CACHE_LIMIT = 256


def _accepts_keyword(client_type: type[Any], name: str) -> bool:
    """Whether a client subclass constructor accepts an owned-only option."""
    key = (client_type, name)
    cached = _KEYWORD_CACHE.get(key)
    if cached is not None:
        return cached
    parameters = inspect.signature(client_type.__init__).parameters.values()
    accepts = any(
        parameter.name == name or parameter.kind is inspect.Parameter.VAR_KEYWORD for parameter in parameters
    )
    if len(_KEYWORD_CACHE) >= _KEYWORD_CACHE_LIMIT:
        _KEYWORD_CACHE.clear()
    _KEYWORD_CACHE[key] = accepts
    return accepts


def _read_env(environment: EnvironmentMap, name: str) -> str | None:
    value = environment.get(name)
    if value is None:
        return None
    return value.strip() or None


def _resolve_base_url(base_url: str | httpx.URL | None, environment: Environment | None) -> str:
    if base_url is not None:
        return str(base_url)
    if environment is not None:
        try:
            return ENVIRONMENTS[environment]
        except KeyError as exc:
            raise ValueError(f"Unknown environment: {environment}") from exc
    return ENVIRONMENTS["production"]


def _resolve_kwargs(
    *,
    platform: str,
    auth: Auth,
    scope: Scope | None,
    environment: Environment | NotGiven,
    base_url: str | httpx.URL | None | NotGiven,
    timeout: Timeout | NotGiven,
    max_retries: int,
    default_headers: Mapping[str, str | None] | None,
) -> dict[str, Any]:
    return {
        "base_url": _resolve_base_url(
            None if isinstance(base_url, NotGiven) else base_url,
            None if isinstance(environment, NotGiven) else environment,
        ),
        "auth": auth,
        "scope": scope,
        "max_retries": max_retries,
        "timeout": DEFAULT_TIMEOUT if isinstance(timeout, NotGiven) else timeout,
        "user_agent": f"Composio/{platform} {__version__}",
        "default_headers": dict(default_headers) if default_headers else None,
    }


def _from_env_kwargs(
    environment_variables: EnvironmentMap,
    *,
    auth: Auth | NotGiven,
    scope: Scope | None | NotGiven,
    environment: Environment | NotGiven,
    base_url: str | httpx.URL | None | NotGiven,
    timeout: Timeout | NotGiven,
    max_retries: int | NotGiven,
    default_headers: Mapping[str, str | None] | None | NotGiven,
) -> dict[str, Any]:
    """The constructor's keywords for a mapping; each override replaces the field it names."""
    if not isinstance(base_url, NotGiven) and base_url is not None and not isinstance(environment, NotGiven):
        raise ValueError("The `base_url` and `environment` options cannot be used together")

    if isinstance(auth, NotGiven):
        auth = auth_from_credentials(
            project=_read_env(environment_variables, "COMPOSIO_API_KEY"),
            user=_read_env(environment_variables, "COMPOSIO_USER_API_KEY"),
            organization=_read_env(environment_variables, "COMPOSIO_ORG_API_KEY"),
        )
    if isinstance(default_headers, NotGiven):
        custom = _read_env(environment_variables, "COMPOSIO_CUSTOM_HEADERS")
        default_headers = _parse_custom_headers(custom) if custom else None
    if isinstance(base_url, NotGiven) and isinstance(environment, NotGiven):
        base_url = _read_env(environment_variables, "COMPOSIO_BASE_URL")

    return {
        "auth": auth,
        "scope": None if isinstance(scope, NotGiven) else scope,
        "environment": environment,
        "base_url": base_url,
        "timeout": timeout,
        "max_retries": DEFAULT_MAX_RETRIES if isinstance(max_retries, NotGiven) else max_retries,
        "default_headers": default_headers,
    }


def _derived_base_url(
    client: Composio | AsyncComposio, environment: Environment | None, base_url: str | httpx.URL | None
) -> str | httpx.URL | None:
    if environment is not None:
        return None
    if base_url is None:
        return client.base_url
    return base_url


def _copy_kwargs(
    client: Composio | AsyncComposio,
    *,
    auth: Auth | NotGiven,
    scope: Scope | None | NotGiven,
    environment: Environment | None,
    base_url: str | httpx.URL | None,
    timeout: Timeout | NotGiven,
    http_client: httpx.Client | httpx.AsyncClient | None,
    max_retries: int | NotGiven,
    default_headers: Mapping[str, str | None] | None,
    set_default_headers: Mapping[str, str | None] | None,
    identity: ClientIdentity | None,
    extra_kwargs: Mapping[str, Any],
) -> dict[str, Any]:
    """The parent's keywords with the given ones laid over them; construction re-validates."""
    headers = (
        dict(set_default_headers)
        if set_default_headers is not None
        else {**dict(client._default_headers or {}), **dict(default_headers or {})}
    )
    kwargs: dict[str, Any] = {
        "auth": client._auth if isinstance(auth, NotGiven) else auth,
        "environment": environment if environment is not None else NOT_GIVEN,
        "base_url": _derived_base_url(client, environment, base_url),
        "timeout": client.timeout if isinstance(timeout, NotGiven) else timeout,
        "max_retries": client.max_retries if isinstance(max_retries, NotGiven) else max_retries,
        "default_headers": headers or None,
        "http_client": client._client if http_client is None else http_client,
        "_strict_response_validation": client._strict_response_validation,
    }
    resolved_scope = client._scope if isinstance(scope, NotGiven) else scope
    resolved_identity = client._identity if identity is None else identity
    # A subclass constructor without `scope` or `identity` keeps deriving unless asked to carry one.
    for name, value in (("scope", resolved_scope), ("identity", resolved_identity)):
        if value is not None or _accepts_keyword(type(client), name):
            kwargs[name] = value
    kwargs.update(extra_kwargs)
    return kwargs


class Composio(SyncAPIClient, ClientResources):
    def __init__(
        self,
        *,
        auth: Auth,
        scope: Scope | None = None,
        environment: Environment | NotGiven = NOT_GIVEN,
        base_url: str | httpx.URL | None | NotGiven = NOT_GIVEN,
        timeout: Timeout | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str | None] | None = None,
        identity: ClientIdentity | None = None,
        http_client: httpx.Client | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        super().__init__(
            http_client=http_client,
            **_resolve_kwargs(
                platform="Python",
                auth=auth,
                scope=scope,
                environment=environment,
                base_url=base_url,
                timeout=timeout,
                max_retries=max_retries,
                default_headers=default_headers,
            ),
            identity=identity,
            _strict_response_validation=_strict_response_validation,
        )
        self._install_resources(self)

    @classmethod
    def from_env(
        cls,
        environment_variables: EnvironmentMap,
        *,
        auth: Auth | NotGiven = NOT_GIVEN,
        scope: Scope | None | NotGiven = NOT_GIVEN,
        environment: Environment | NotGiven = NOT_GIVEN,
        base_url: str | httpx.URL | None | NotGiven = NOT_GIVEN,
        timeout: Timeout | NotGiven = NOT_GIVEN,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str | None] | None | NotGiven = NOT_GIVEN,
        identity: ClientIdentity | None = None,
        http_client: httpx.Client | None = None,
        _strict_response_validation: bool = False,
    ) -> Self:
        """Construct from a mapping such as ``os.environ``; each keyword replaces the field it names."""
        return cls(
            **_from_env_kwargs(
                environment_variables,
                auth=auth,
                scope=scope,
                environment=environment,
                base_url=base_url,
                timeout=timeout,
                max_retries=max_retries,
                default_headers=default_headers,
            ),
            identity=identity,
            http_client=http_client,
            _strict_response_validation=_strict_response_validation,
        )

    def __enter__(self) -> Composio:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    def with_options(
        self,
        *,
        auth: Auth | NotGiven = NOT_GIVEN,
        scope: Scope | None | NotGiven = NOT_GIVEN,
        environment: Environment | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Timeout | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str | None] | None = None,
        set_default_headers: Mapping[str, str | None] | None = None,
        identity: ClientIdentity | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """A new client with the given options laid over this one's; ``scope=None`` clears the scope."""
        return type(self)(
            **_copy_kwargs(
                self,
                auth=auth,
                scope=scope,
                environment=environment,
                base_url=base_url,
                timeout=timeout,
                http_client=http_client,
                max_retries=max_retries,
                default_headers=default_headers,
                set_default_headers=set_default_headers,
                identity=identity,
                extra_kwargs=_extra_kwargs,
            )
        )


class AsyncComposio(AsyncAPIClient, AsyncClientResources):
    def __init__(
        self,
        *,
        auth: Auth,
        scope: Scope | None = None,
        environment: Environment | NotGiven = NOT_GIVEN,
        base_url: str | httpx.URL | None | NotGiven = NOT_GIVEN,
        timeout: Timeout | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str | None] | None = None,
        identity: ClientIdentity | None = None,
        http_client: httpx.AsyncClient | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        super().__init__(
            http_client=http_client,
            **_resolve_kwargs(
                platform="Python",
                auth=auth,
                scope=scope,
                environment=environment,
                base_url=base_url,
                timeout=timeout,
                max_retries=max_retries,
                default_headers=default_headers,
            ),
            identity=identity,
            _strict_response_validation=_strict_response_validation,
        )
        self._install_resources(self)

    @classmethod
    def from_env(
        cls,
        environment_variables: EnvironmentMap,
        *,
        auth: Auth | NotGiven = NOT_GIVEN,
        scope: Scope | None | NotGiven = NOT_GIVEN,
        environment: Environment | NotGiven = NOT_GIVEN,
        base_url: str | httpx.URL | None | NotGiven = NOT_GIVEN,
        timeout: Timeout | NotGiven = NOT_GIVEN,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str | None] | None | NotGiven = NOT_GIVEN,
        identity: ClientIdentity | None = None,
        http_client: httpx.AsyncClient | None = None,
        _strict_response_validation: bool = False,
    ) -> Self:
        """See :meth:`Composio.from_env`."""
        return cls(
            **_from_env_kwargs(
                environment_variables,
                auth=auth,
                scope=scope,
                environment=environment,
                base_url=base_url,
                timeout=timeout,
                max_retries=max_retries,
                default_headers=default_headers,
            ),
            identity=identity,
            http_client=http_client,
            _strict_response_validation=_strict_response_validation,
        )

    async def __aenter__(self) -> AsyncComposio:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    def with_options(
        self,
        *,
        auth: Auth | NotGiven = NOT_GIVEN,
        scope: Scope | None | NotGiven = NOT_GIVEN,
        environment: Environment | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Timeout | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str | None] | None = None,
        set_default_headers: Mapping[str, str | None] | None = None,
        identity: ClientIdentity | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """See :meth:`Composio.with_options`."""
        return type(self)(
            **_copy_kwargs(
                self,
                auth=auth,
                scope=scope,
                environment=environment,
                base_url=base_url,
                timeout=timeout,
                http_client=http_client,
                max_retries=max_retries,
                default_headers=default_headers,
                set_default_headers=set_default_headers,
                identity=identity,
                extra_kwargs=_extra_kwargs,
            )
        )
