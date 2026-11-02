"""How to reach a Lakekeeper warehouse, and how to prove who you are.

Credentials are a sum type rather than a bag of nullable fields: the prior art
carried six optional attributes and validated their combinations in
``__post_init__``, which made several invalid states representable. Here an
``OAuthClientCredentials`` or a ``StaticToken`` (or any ``TokenProvider``) is
supplied, and there is nothing left to validate.

``LakehouseSettings`` is frozen so it can safely key a cache. Namespace is the
one field that varies per call site, so it is changed with ``with_namespace``
rather than by mutation.
"""

from __future__ import annotations

import os
import threading
import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

import requests

from databaas_utils.errors import AuthenticationError, ConfigurationError

DEFAULT_REGION = "nl-ams"
DEFAULT_WAREHOUSE = "databaas-lakehouse"
# Lakekeeper's in-cluster Service, as seen from a JupyterHub singleuser pod.
DEFAULT_JUPYTERHUB_CATALOG = "http://lakekeeper:8181"
TOKEN_TIMEOUT = 30
# Refresh this many seconds before actual expiry, so a token cannot lapse
# between the check and the request it authorises.
_EXPIRY_MARGIN = 60


@runtime_checkable
class TokenProvider(Protocol):
    """Anything that can produce an ``Authorization`` header value.

    This is the seam that lets a notebook pass the logged-in user's bearer
    instead of a service account, without this package learning what
    JupyterHub is.
    """

    def auth_header(self) -> str:
        """The full ``Authorization`` header value, e.g. ``"Bearer eyJ..."``.

        Called on every request, so implementations should cache and refresh.
        """
        ...


@dataclass(frozen=True)
class StaticToken:
    """A bearer token supplied verbatim. Never refreshed.

    Args:
        token: The raw access token (a JWT that Lakekeeper can validate).

    Example:
        >>> settings = LakehouseSettings(
        ...     base_url="https://lakekeeper.example.com",
        ...     warehouse="databaas-lakehouse",
        ...     credentials=StaticToken("eyJ..."),
        ... )
    """

    token: str = field(repr=False)

    def auth_header(self) -> str:
        """``Bearer <token>``."""
        return f"Bearer {self.token}"


@dataclass(frozen=True)
class OAuthClientCredentials:
    """OAuth2 client-credentials, cached and refreshed on demand.

    ``project_id`` is Zitadel shorthand: it expands to the audience scope that
    Lakekeeper expects. Supply ``scope`` directly to override.

    Args:
        client_id: The machine user's OAuth client id.
        client_secret: The matching client secret.
        token_url: The Zitadel token endpoint, e.g.
            ``https://auth.example.com/oauth/v2/token``.
        scope: Full OAuth scope string. Overrides ``project_id``.
        project_id: Zitadel project id; expands to the audience scope.

    Raises:
        ConfigurationError: If neither ``scope`` nor ``project_id`` is given.

    Example:
        >>> creds = OAuthClientCredentials(
        ...     client_id="databaas-pipeline",
        ...     client_secret=os.environ["CLIENT_SECRET"],
        ...     token_url="https://auth.example.com/oauth/v2/token",
        ...     project_id="123456789",
        ... )
    """

    client_id: str
    client_secret: str = field(repr=False)
    token_url: str
    scope: str | None = None
    project_id: str | None = None
    _cache: dict[str, Any] = field(
        default_factory=dict, repr=False, compare=False, hash=False
    )
    _lock: threading.Lock = field(
        default_factory=threading.Lock, repr=False, compare=False, hash=False
    )

    def __post_init__(self) -> None:
        if not (self.scope or self.project_id):
            raise ConfigurationError(
                "OAuthClientCredentials needs either scope or project_id "
                "(Lakekeeper rejects a token without the project audience)"
            )

    @property
    def effective_scope(self) -> str:
        """``scope`` if set, else the Zitadel project-audience scope."""
        if self.scope:
            return self.scope
        return f"openid urn:zitadel:iam:org:project:id:{self.project_id}"

    def auth_header(self) -> str:
        """``Bearer <token>``, fetching or refreshing the token if it is stale.

        Raises:
            AuthenticationError: If the token endpoint is unreachable or
                rejects the credentials.
        """
        return f"Bearer {self._token()}"

    def _token(self) -> str:
        now = time.monotonic()
        token = self._cache.get("token")
        if token and now < self._cache.get("expires_at", 0.0):
            return str(token)
        # Double-checked: the fetch is slow, and concurrent obstore sign
        # callbacks would otherwise each trigger their own.
        with self._lock:
            token = self._cache.get("token")
            if token and time.monotonic() < self._cache.get("expires_at", 0.0):
                return str(token)
            fetched, expires_in = self._fetch()
            self._cache["token"] = fetched
            self._cache["expires_at"] = time.monotonic() + max(
                expires_in - _EXPIRY_MARGIN, 0
            )
            return fetched

    def _fetch(self) -> tuple[str, float]:
        try:
            response = requests.post(
                self.token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "scope": self.effective_scope,
                },
                timeout=TOKEN_TIMEOUT,
            )
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException as exc:
            raise AuthenticationError(
                f"token request to {self.token_url} failed: {exc}"
            ) from exc
        token = payload.get("access_token")
        if not token:
            raise AuthenticationError(
                f"token response from {self.token_url} carried no access_token"
            )
        return str(token), float(payload.get("expires_in", 3600))


@dataclass(frozen=True)
class ServiceAccountKey:
    """A Zitadel service-account JSON key: Private Key JWT (RFC 7523) auth.

    Some Zitadel consoles only offer a downloadable JSON key for a machine
    user, not a plain client secret — the key's fields are exactly
    ``type``/``keyId``/``key``/``userId``, matching :meth:`from_json`. This
    signs a JWT assertion with the private key and exchanges it for a real
    access token via the ``urn:ietf:params:oauth:grant-type:jwt-bearer``
    grant. The resulting token is a normal Zitadel-issued JWT — structurally
    identical to what ``client_credentials`` with a secret produces, so
    anything that accepts one accepts the other. Only how the *client* proves
    itself to Zitadel differs; a Lakekeeper (or anything else) validating the
    access token cannot tell the two apart.

    A raw Zitadel Personal Access Token is not usable here or anywhere else
    against Lakekeeper: it is an opaque credential meant for calling
    Zitadel's own APIs, not a JWT a resource server's OIDC validator can
    parse. Signing an assertion and exchanging it for a real access token —
    what this class does — is the fix.

    Needs the ``jwt`` extra: ``pip install "databaas-utils[jwt]"``.

    Args:
        key_id: The key's ``keyId``.
        private_key: The PEM private key (the JSON key's ``key`` field).
        user_id: The machine user's id (the JSON key's ``userId`` field).
        token_url: The Zitadel token endpoint.
        scope: Full OAuth scope string. Overrides ``project_id``.
        project_id: Zitadel project id; expands to the audience scope.
        audience: The assertion's ``aud``. Defaults to ``token_url`` without
            the ``/oauth/v2/token`` suffix.

    Raises:
        ConfigurationError: If neither ``scope`` nor ``project_id`` is given.

    Example:
        >>> creds = ServiceAccountKey.from_json(
        ...     "/secrets/zitadel-key.json",
        ...     token_url="https://auth.example.com/oauth/v2/token",
        ...     project_id="123456789",
        ... )
    """

    key_id: str
    private_key: str = field(repr=False)
    user_id: str
    token_url: str
    scope: str | None = None
    project_id: str | None = None
    # The JWT assertion's `aud`. Zitadel checks this against its own issuer
    # exactly, so get it right rather than derive it wrong silently: defaults
    # to token_url with the well-known `/oauth/v2/token` suffix stripped.
    audience: str | None = None
    _cache: dict[str, Any] = field(
        default_factory=dict, repr=False, compare=False, hash=False
    )
    _lock: threading.Lock = field(
        default_factory=threading.Lock, repr=False, compare=False, hash=False
    )

    def __post_init__(self) -> None:
        if not (self.scope or self.project_id):
            raise ConfigurationError(
                "ServiceAccountKey needs either scope or project_id "
                "(Lakekeeper rejects a token without the project audience)"
            )

    @property
    def effective_scope(self) -> str:
        """``scope`` if set, else the Zitadel project-audience scope."""
        if self.scope:
            return self.scope
        return f"openid urn:zitadel:iam:org:project:id:{self.project_id}"

    @property
    def effective_audience(self) -> str:
        """The assertion's ``aud``: ``audience``, else the issuer from ``token_url``."""
        if self.audience:
            return self.audience
        return self.token_url.removesuffix("/oauth/v2/token")

    @classmethod
    def from_json(
        cls, source: Mapping[str, Any] | str | os.PathLike[str], **overrides: Any
    ) -> ServiceAccountKey:
        """Build from a Zitadel service-account JSON key file's own fields.

        ``source`` is the file's parsed contents, its raw JSON text, or a path
        to the file — accepting all three covers "I already loaded it" and "I
        have the path" without asking the caller to pick one.

        Args:
            source: Parsed key, raw JSON text, or path to the JSON file.
            **overrides: The remaining constructor fields (``token_url``,
                ``project_id``, ``scope``, ``audience``).

        Raises:
            ConfigurationError: If the key lacks ``keyId``/``key``/``userId``.
        """
        import json
        from pathlib import Path

        data: Any = source
        if isinstance(data, os.PathLike):
            data = Path(data).read_text()
        if isinstance(data, str):
            text = data
            if not text.lstrip().startswith("{"):
                text = Path(text).read_text()
            data = json.loads(text)
        try:
            key_id = data["keyId"]
            private_key = data["key"]
            user_id = data["userId"]
        except KeyError as exc:
            raise ConfigurationError(
                f"service-account JSON key is missing {exc.args[0]!r} — expected "
                "the keyId/key/userId fields Zitadel's console downloads"
            ) from exc
        return cls(key_id=key_id, private_key=private_key, user_id=user_id, **overrides)

    def auth_header(self) -> str:
        """``Bearer <token>``, signing a new assertion if the token is stale.

        Raises:
            AuthenticationError: If the token exchange fails.
            ConfigurationError: If the private key cannot sign.
        """
        return f"Bearer {self._token()}"

    def _token(self) -> str:
        now = time.monotonic()
        token = self._cache.get("token")
        if token and now < self._cache.get("expires_at", 0.0):
            return str(token)
        # Double-checked, same reason as OAuthClientCredentials: concurrent
        # callers must not each sign and exchange their own assertion.
        with self._lock:
            token = self._cache.get("token")
            if token and time.monotonic() < self._cache.get("expires_at", 0.0):
                return str(token)
            fetched, expires_in = self._fetch()
            self._cache["token"] = fetched
            self._cache["expires_at"] = time.monotonic() + max(
                expires_in - _EXPIRY_MARGIN, 0
            )
            return fetched

    def _assertion(self) -> str:
        import jwt

        now = int(time.time())
        claims = {
            "iss": self.user_id,
            "sub": self.user_id,
            "aud": self.effective_audience,
            "iat": now,
            # Short-lived on purpose: this assertion is used once, immediately,
            # to fetch a real access token — it is not the credential that
            # actually authorises anything afterward.
            "exp": now + 60,
        }
        try:
            return jwt.encode(
                claims,
                self.private_key,
                algorithm="RS256",
                headers={"kid": self.key_id},
            )
        except (ValueError, jwt.InvalidKeyError) as exc:
            raise ConfigurationError(
                f"could not sign a JWT assertion with this service-account "
                f"key (key id {self.key_id!r}): {exc}"
            ) from exc

    def _fetch(self) -> tuple[str, float]:
        try:
            response = requests.post(
                self.token_url,
                data={
                    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                    "assertion": self._assertion(),
                    "scope": self.effective_scope,
                },
                timeout=TOKEN_TIMEOUT,
            )
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException as exc:
            raise AuthenticationError(
                f"JWT-bearer token request to {self.token_url} failed: {exc}"
            ) from exc
        token = payload.get("access_token")
        if not token:
            raise AuthenticationError(
                f"token response from {self.token_url} carried no access_token"
            )
        return str(token), float(payload.get("expires_in", 3600))


Credentials = TokenProvider


@dataclass(frozen=True)
class LakehouseSettings:
    """Everything needed to reach one warehouse as one identity.

    Frozen, so it is safe as a cache key. Most code never builds one directly:
    use :meth:`from_env`, :meth:`from_profile`, :meth:`from_jupyterhub`, or (in
    a DAG) ``databaas_utils.airflow.get_settings``.

    Args:
        base_url: The Lakekeeper server root, e.g.
            ``https://lakekeeper.example.com``. Not the ``/catalog`` endpoint.
            A missing scheme is taken to be ``https://``.
        warehouse: Warehouse name.
        credentials: Any :class:`TokenProvider`.
        namespace: Default namespace for tables and generic tables.
        region: Storage region, used until Lakekeeper's table config overrides it.
        endpoint: S3 endpoint override, for MinIO and similar.
        verify: TLS verification: ``True``, ``False`` or a CA bundle path.

    Raises:
        ConfigurationError: If ``base_url`` or ``warehouse`` is empty, or
            ``base_url`` ends in ``/catalog``.

    Example:
        >>> settings = LakehouseSettings(
        ...     base_url="https://lakekeeper.example.com",
        ...     warehouse="databaas-lakehouse",
        ...     credentials=StaticToken("eyJ..."),
        ...     namespace="open_meteo",
        ... )
    """

    base_url: str
    warehouse: str
    credentials: Credentials
    namespace: str = "default"
    region: str = DEFAULT_REGION
    endpoint: str | None = None
    verify: bool | str = True

    def __post_init__(self) -> None:
        url = self.base_url.rstrip("/")
        if not url:
            raise ConfigurationError("base_url is required")
        if url.endswith("/catalog"):
            raise ConfigurationError(
                "base_url must be the Lakekeeper server root, not the catalog "
                f"endpoint — drop the trailing '/catalog' from {self.base_url!r}. "
                "The catalog path is appended where it is needed."
            )
        if "://" not in url:
            url = f"https://{url}"
        object.__setattr__(self, "base_url", url)
        if not self.warehouse:
            raise ConfigurationError("warehouse is required")

    @property
    def catalog_url(self) -> str:
        """The Iceberg REST endpoint: ``base_url`` plus ``/catalog``."""
        return f"{self.base_url}/catalog"

    def auth_header(self) -> str:
        """The current ``Authorization`` header value, from ``credentials``."""
        return self.credentials.auth_header()

    def with_namespace(self, namespace: str) -> LakehouseSettings:
        """A copy pointing at ``namespace``; ``self`` if it already does."""
        if namespace == self.namespace:
            return self
        return LakehouseSettings(
            base_url=self.base_url,
            warehouse=self.warehouse,
            credentials=self.credentials,
            namespace=namespace,
            region=self.region,
            endpoint=self.endpoint,
            verify=self.verify,
        )

    @classmethod
    def from_mapping(
        cls, values: Mapping[str, Any], *, namespace: str | None = None
    ) -> LakehouseSettings:
        """Build from a flat mapping. Shared by the env and Airflow adapters.

        Credentials are chosen by which keys are present, in this order:
        ``service_account_key``, then ``client_id`` (+ ``client_secret``), then
        ``token``.

        Args:
            values: Keys ``base_url`` (or ``uri``), one credential set, and
                optionally ``warehouse`` (``databaas-lakehouse`` by default),
                ``token_url``, ``project_id``, ``scope``, ``region``,
                ``endpoint``, ``verify``, ``namespace``.
            namespace: Overrides ``values["namespace"]``.

        Raises:
            ConfigurationError: If the mapping has no credentials, or a
                credential set without its token endpoint.
        """
        token = values.get("token")
        client_id = values.get("client_id")
        service_account_key = values.get("service_account_key")
        credentials: Credentials
        if service_account_key:
            sak_token_url = values.get("token_url") or values.get("oauth2_server_uri")
            if not sak_token_url:
                raise ConfigurationError(
                    "service_account_key was supplied without token_url — "
                    "the JWT-bearer grant needs the OAuth token endpoint"
                )
            credentials = ServiceAccountKey.from_json(
                service_account_key,
                token_url=str(sak_token_url),
                scope=values.get("scope") or values.get("oauth2_scope"),
                project_id=values.get("project_id"),
                audience=values.get("audience"),
            )
        elif client_id:
            token_url = values.get("token_url") or values.get("oauth2_server_uri")
            if not token_url:
                raise ConfigurationError(
                    "client_id was supplied without token_url — "
                    "client-credentials auth needs the OAuth token endpoint"
                )
            credentials = OAuthClientCredentials(
                client_id=str(client_id),
                client_secret=str(values.get("client_secret") or ""),
                token_url=str(token_url),
                scope=values.get("scope") or values.get("oauth2_scope"),
                project_id=values.get("project_id"),
            )
        elif token:
            credentials = StaticToken(str(token))
        else:
            raise ConfigurationError(
                "no credentials: supply client_id (+ client_secret, token_url) "
                "or a static token"
            )
        return cls(
            base_url=str(values.get("base_url") or values.get("uri") or ""),
            warehouse=str(values.get("warehouse") or DEFAULT_WAREHOUSE),
            credentials=credentials,
            namespace=str(namespace or values.get("namespace") or "default"),
            region=str(values.get("region") or DEFAULT_REGION),
            endpoint=values.get("endpoint"),
            verify=values.get("verify", True),
        )

    @classmethod
    def from_env(
        cls,
        prefix: str = "LAKEKEEPER_",
        *,
        env: Mapping[str, str] | None = None,
        namespace: str | None = None,
    ) -> LakehouseSettings:
        """Build from the environment a container or notebook already carries.

        Reads ``{prefix}URI``, ``WAREHOUSE``, ``CLIENT_ID``, ``CLIENT_SECRET``,
        ``OAUTH2_SERVER_URI``, ``PROJECT_ID``, ``OAUTH2_SCOPE``, ``TOKEN``,
        ``REGION`` and ``ENDPOINT``.

        Args:
            prefix: Variable-name prefix.
            env: Mapping to read instead of ``os.environ``.
            namespace: Default namespace.

        Raises:
            ConfigurationError: If the variables do not form a complete config.
        """
        source = env if env is not None else os.environ

        def get(name: str) -> str | None:
            return source.get(f"{prefix}{name}")

        return cls.from_mapping(
            {
                "base_url": get("URI"),
                "warehouse": get("WAREHOUSE"),
                "client_id": get("CLIENT_ID"),
                "client_secret": get("CLIENT_SECRET"),
                "token_url": get("OAUTH2_SERVER_URI"),
                "project_id": get("PROJECT_ID"),
                "scope": get("OAUTH2_SCOPE"),
                "token": get("TOKEN"),
                "region": get("REGION"),
                "endpoint": get("ENDPOINT"),
            },
            namespace=namespace,
        )

    @classmethod
    def from_profile(
        cls,
        name: str | None = None,
        *,
        namespace: str | None = None,
        interactive: bool = True,
        store: Any = None,
    ) -> LakehouseSettings:
        """Build from a saved local profile, authenticating as the logged-in user.

        This is the entry point for local, interactive use — log in first with
        ``databaas login`` (see ``databaas_utils.cli``). Machine contexts
        (Airflow, CI) should keep using ``from_env``/``from_mapping`` with a
        service credential; a browser login is not something a scheduled task
        can complete.

        Args:
            name: Profile name; the default profile if omitted.
            namespace: Default namespace.
            interactive: Whether to open a browser/device login when no valid
                session is cached. Set ``False`` for unattended code, which
                then raises instead of prompting.
            store: A ``TokenStore`` to keep the session in; the OS keychain
                (or a private file) by default.

        Raises:
            ConfigurationError: If no such profile exists.

        Example:
            >>> settings = LakehouseSettings.from_profile()
            >>> catalog = rest_catalog(settings)
        """
        from databaas_utils.profiles import load_profile
        from databaas_utils.userauth import UserLogin

        profile = load_profile(name)
        kwargs: dict[str, Any] = {"interactive": interactive}
        if store is not None:
            kwargs["store"] = store
        credentials = UserLogin.from_profile(profile, **kwargs)
        return cls(
            base_url=profile.catalog_url,
            warehouse=profile.warehouse,
            credentials=credentials,
            namespace=namespace or "default",
            region=profile.region,
        )

    @classmethod
    def from_jupyterhub(
        cls,
        *,
        namespace: str | None = None,
        warehouse: str | None = None,
        env: Mapping[str, str] | None = None,
    ) -> LakehouseSettings:
        """Build inside a JupyterHub singleuser pod, as the logged-in user.

        The token comes from the hub (see ``databaas_utils.jupyterhub``). The
        pod's environment names the catalog: ``CATALOG_URI`` (the Lakekeeper
        server root) and ``LAKEKEEPER_WAREHOUSE``. The storage region and
        endpoint are not read here — Lakekeeper supplies both in each table's
        config, which takes precedence over the client's.

        Args:
            namespace: Default namespace.
            warehouse: Warehouse name; ``LAKEKEEPER_WAREHOUSE`` or
                ``databaas-lakehouse`` if omitted.
            env: Mapping to read instead of ``os.environ``.

        Raises:
            ConfigurationError: If this is not a JupyterHub singleuser server.
        """
        from databaas_utils.jupyterhub import JupyterHubToken

        source = env if env is not None else os.environ
        return cls(
            base_url=source.get("CATALOG_URI") or DEFAULT_JUPYTERHUB_CATALOG,
            warehouse=warehouse
            or source.get("LAKEKEEPER_WAREHOUSE")
            or DEFAULT_WAREHOUSE,
            credentials=JupyterHubToken.from_env(source),
            namespace=namespace or "default",
        )
