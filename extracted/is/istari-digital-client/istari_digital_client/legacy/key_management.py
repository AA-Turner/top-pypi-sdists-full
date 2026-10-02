"""High-level key-management wrappers for the top-level Istari clients.

The hand-written helpers in `auth` are free functions that make the caller
assemble low-level plumbing — an identity-service base URL for the PAT-to-key
exchange, or a fully-constructed `IdentityServiceClient` for key CRUD. A configured
`Client` / `V3Client` already holds all of that on its `Configuration`, so this
module exposes the helpers as a `client.keys` accessor that supplies the plumbing
automatically.

Two families with different prerequisites:

* **Exchange** (`exchange_pat`, `generate_keypair_and_exchange`) — needs only
  `Configuration.digital_api_url` (the Identity Service base URL is derived from it as
  `<digital_api_url>/identity`); Identity Service mode need not be enabled.
* **CRUD** (`register`, `list`, `get`, `revoke`,
  `generate_keypair_and_register`) — needs Identity Service mode enabled, i.e. a
  live `Configuration._identity_service_client`. `kind=AGENT` requires an explicit
  agent `principal_id`: `"me"` is invalid on agent routes and an agent cannot
  manage its own keys; whether a (potential admin) caller may manage that agent
  is left to the server.

A prerequisite that is not satisfied raises `ConfigurationError`.
"""

from __future__ import annotations

from typing import Optional

from istari_digital_client.legacy.auth import (
    ExchangePatResult,
    GeneratedClientCredentials,
    IdentityServiceClient,
    KeyMetadata,
    PrincipalKeys,
    PrincipalKind,
    RegisterKeyResult,
    RetryPolicy,
    exchange_pat,
    generate_keypair_and_exchange,
    generate_keypair_and_register,
    get_key,
    list_keys,
    register_key,
    revoke_key,
)
from istari_digital_client.legacy.configuration import Configuration
from istari_digital_client.legacy.configuration import ConfigurationError

#: The Identity Service "me" route, which resolves server-side to the authenticated
#: caller on user routes. Used as the default `principal_id` for CRUD operations.
_ME = "me"


class KeyManagement:
    """Identity-service key operations bound to a client's `Configuration`.

    Reached via `client.keys`; not constructed directly. Each method resolves the
    operation's prerequisite from the configuration (the Identity Service URL for exchange, the
    live Identity Service client for CRUD), defaults the retry policy from the SDK's `retry_*`
    knobs, and delegates to the matching `auth` helper.
    """

    def __init__(self, config: Configuration) -> None:
        """Bind the accessor to `config`.

        :param config: The owning client's configuration.
        """
        self._config = config

    # -- prerequisite resolvers ------------------------------------------------

    def _require_ir_url(self) -> str:
        """Return the derived Identity Service base URL, or raise if it cannot be derived.

        The Identity Service base URL is derived from ``digital_api_url`` (the gateway serves the
        Identity Service under ``<digital_api_url>/identity``).

        :raises ConfigurationError: when `digital_api_url` is not configured.
        """
        url = self._config._identity_service_base_url()
        if not url:
            raise ConfigurationError(
                "Identity Service URL could not be derived; key exchange requires it. "
                "Set the digital API URL via the ISTARI_DIGITAL_API_URL env variable "
                "or the digital_api_url attribute on the Configuration."
            )
        return url

    def _require_ir_client(self) -> IdentityServiceClient:
        """Return the live Identity Service client, or raise if Identity Service mode is not enabled.

        :raises ConfigurationError: when Identity Service mode is not enabled.
        """
        identity_service_client = self._config._identity_service_client
        if identity_service_client is None:
            raise ConfigurationError(
                "Identity Service mode is not enabled; key management requires it. "
                "Enable it via the ISTARI_CLIENT_IDENTITY_SERVICE_ENABLED env "
                "variable (with the Identity Service credentials configured) or the "
                "identity_service_enabled attribute on the Configuration."
            )
        return identity_service_client

    def _require_pat(self, pat: Optional[str]) -> str:
        """Return `pat`, or the configured `registry_auth_token` when `pat` is None.

        :raises ConfigurationError: when no PAT is given and no `registry_auth_token`
                                    is configured.
        """
        resolved = pat or self._config.registry_auth_token
        if not resolved:
            raise ConfigurationError(
                "No PAT provided and no registry auth token is configured; the PAT "
                "exchange requires a Zitadel Personal Access Token. Pass pat=... or "
                "set the ISTARI_REGISTRY_AUTH_TOKEN env variable or the "
                "registry_auth_token attribute on the Configuration."
            )
        return resolved

    def _policy(self, retry_policy: Optional[RetryPolicy]) -> RetryPolicy:
        """Return `retry_policy` or the policy built from the SDK retry knobs."""
        return retry_policy or self._config._retry_policy()

    @staticmethod
    def _reject_agent_self_route(
        principal_id: Optional[str], kind: PrincipalKind
    ) -> None:
        """Reject the implicit "self" target on agent key routes.

        `"me"` (the default) resolves to the caller only on user routes and
        agents can never manage their own keys by Identity Service policy, so
        `kind=AGENT` with no explicit `principal_id` can never work. Agent-route
        CRUD is an admin operation against a *named* agent only.

        :raises ValueError: when `kind` is `AGENT` and `principal_id` is unset
                            or `"me"`.
        """
        if kind == PrincipalKind.AGENT and (not principal_id or principal_id == _ME):
            raise ValueError(
                '"me" is not valid on agent key routes, and an agent cannot '
                "manage its own keys; pass an explicit agent principal_id "
                "(agent key management is an admin operation against a named "
                "agent)."
            )

    # -- exchange family (needs the Identity Service URL only) -------------------------------

    def exchange_pat(
        self,
        credentials: GeneratedClientCredentials,
        *,
        pat: Optional[str] = None,
        kind: PrincipalKind = PrincipalKind.USER,
        validate_public_key: bool = True,
        name: Optional[str] = None,
        retry_policy: Optional[RetryPolicy] = None,
    ) -> ExchangePatResult:
        """Exchange a Zitadel PAT for identity-service credentials using your own key.

        Wraps `exchange_pat`, supplying the derived Identity Service URL. Does not require
        Identity Service mode to be enabled.

        :param credentials: The caller's ECDSA P-384 keypair whose public key is
                            registered; the private key is retained on the result.
        :param pat: Zitadel Personal Access Token for the caller; defaults to the
                    configured `registry_auth_token` when omitted.
        :param kind: Whether the PAT and key are for a human USER (default) or AGENT.
        :param validate_public_key: When True (default), check the public key is
                                    ECDSA P-384 before exchanging.
        :param name: Optional human-readable label for the key. When omitted (or
                     blank) the identity-service defaults the name to the key id.
        :param retry_policy: Bounded retry/backoff; defaults to the SDK retry knobs.
        :raises ConfigurationError: when `digital_api_url` (from which the Identity Service base
                                    URL is derived) is not configured, or when no PAT
                                    is given and no `registry_auth_token` is configured.
        """
        return exchange_pat(
            self._require_ir_url(),
            self._require_pat(pat),
            credentials,
            kind=kind,
            retry_policy=self._policy(retry_policy),
            validate_public_key=validate_public_key,
            name=name,
        )

    def generate_keypair_and_exchange(
        self,
        *,
        pat: Optional[str] = None,
        kind: PrincipalKind = PrincipalKind.USER,
        key_id: Optional[str] = None,
        name: Optional[str] = None,
        retry_policy: Optional[RetryPolicy] = None,
    ) -> ExchangePatResult:
        """Generate a P-384 keypair and exchange it for Identity Service credentials in one step.

        Wraps `generate_keypair_and_exchange`, supplying the derived Identity Service URL.
        Does not require Identity Service mode to be enabled.

        :param pat: Zitadel Personal Access Token for the caller; defaults to the
                    configured `registry_auth_token` when omitted.
        :param kind: Whether the PAT and key are for a human USER (default) or AGENT.
        :param key_id: Key id to register; a random one is generated when omitted.
        :param name: Optional human-readable label for the key. When omitted (or
                     blank) the identity-service defaults the name to the key id.
        :param retry_policy: Bounded retry/backoff; defaults to the SDK retry knobs.
        :raises ConfigurationError: when `digital_api_url` (from which the Identity Service base
                                    URL is derived) is not configured, or when no PAT
                                    is given and no `registry_auth_token` is configured.
        """
        return generate_keypair_and_exchange(
            self._require_ir_url(),
            self._require_pat(pat),
            kind=kind,
            key_id=key_id,
            retry_policy=self._policy(retry_policy),
            name=name,
        )

    # -- CRUD family (needs Identity Service mode enabled) ----------------------

    @property
    def client_id(self) -> str:
        """The client ID this client authenticates as against the Identity Service.

        This is the JWT `sub`/`iss` — the principal ID the configured Identity Service
        credentials belong to. Useful when you need the caller's own identity
        without issuing a network request (e.g. to pass as `principal_id` to
        another operation).

        :raises ConfigurationError: when Identity Service mode is not enabled.
        """
        return self._require_ir_client().client_id

    def register(
        self,
        credentials: GeneratedClientCredentials,
        *,
        principal_id: str = _ME,
        kind: PrincipalKind = PrincipalKind.USER,
        validate_public_key: bool = True,
        name: Optional[str] = None,
        username: Optional[str] = None,
        display_name: Optional[str] = None,
        retry_policy: Optional[RetryPolicy] = None,
    ) -> KeyMetadata:
        """Register a principal's ECDSA P-384 public key with the identity-service.

        Wraps `register_key`, supplying the live Identity Service client. Requires
        Identity Service mode to be enabled.

        :param credentials: The keypair to register; only its public key and key id
                            are sent. Must be ECDSA P-384.
        :param principal_id: Target principal id; defaults to `"me"` (the caller,
                            on user routes). On agent routes you must pass an
                            explicit agent id — `"me"` is not valid there.
        :param kind: Whether the principal is a human USER (default) or AGENT.
        :param validate_public_key: When True (default), check the public key is
                                    ECDSA P-384 before registering.
        :param name: Optional human-readable label for the key. When omitted (or
                     blank) the identity-service defaults the name to the key id.
        :param username: Optional; honored only when an admin registers the first
                        key for a not-yet-existing agent.
        :param display_name: Optional; seeds a new agent's display name.
        :param retry_policy: Bounded retry/backoff; defaults to the SDK retry knobs.
        :raises ConfigurationError: when Identity Service mode is not enabled.
        :raises ValueError: when `kind` is `AGENT` with no explicit `principal_id`
                            (`"me"` is not valid on agent routes).
        """
        self._reject_agent_self_route(principal_id, kind)
        return register_key(
            self._require_ir_client(),
            principal_id,
            credentials,
            kind=kind,
            retry_policy=self._policy(retry_policy),
            validate_public_key=validate_public_key,
            name=name,
            username=username,
            display_name=display_name,
        )

    def list(
        self,
        *,
        principal_id: str = _ME,
        kind: PrincipalKind = PrincipalKind.USER,
        retry_policy: Optional[RetryPolicy] = None,
    ) -> PrincipalKeys:
        """List a principal's registered keys (metadata only, no key material).

        Wraps `list_keys`, supplying the live Identity Service client. Requires Identity Service
        mode to be enabled.

        :param principal_id: Target principal id; defaults to `"me"` (the caller,
                            on user routes). On agent routes you must pass an
                            explicit agent id — `"me"` is not valid there.
        :param kind: Whether the principal is a human USER (default) or AGENT.
        :param retry_policy: Bounded retry/backoff; defaults to the SDK retry knobs.
        :raises ConfigurationError: when Identity Service mode is not enabled.
        :raises ValueError: when `kind` is `AGENT` with no explicit `principal_id`
                            (`"me"` is not valid on agent routes).
        """
        self._reject_agent_self_route(principal_id, kind)
        return list_keys(
            self._require_ir_client(),
            principal_id,
            kind=kind,
            retry_policy=self._policy(retry_policy),
        )

    def get(
        self,
        key_id: str,
        *,
        principal_id: str = _ME,
        kind: PrincipalKind = PrincipalKind.USER,
        retry_policy: Optional[RetryPolicy] = None,
    ) -> KeyMetadata:
        """Fetch the metadata for a single registered key.

        Wraps `get_key`, supplying the live Identity Service client. Requires Identity Service
        mode to be enabled.

        :param key_id: The key id to fetch.
        :param principal_id: Target principal id; defaults to `"me"` (the caller,
                            on user routes). On agent routes you must pass an
                            explicit agent id — `"me"` is not valid there.
        :param kind: Whether the principal is a human USER (default) or AGENT.
        :param retry_policy: Bounded retry/backoff; defaults to the SDK retry knobs.
        :raises ConfigurationError: when Identity Service mode is not enabled.
        :raises ValueError: when `kind` is `AGENT` with no explicit `principal_id`
                            (`"me"` is not valid on agent routes).
        """
        self._reject_agent_self_route(principal_id, kind)
        return get_key(
            self._require_ir_client(),
            principal_id,
            key_id,
            kind=kind,
            retry_policy=self._policy(retry_policy),
        )

    def revoke(
        self,
        key_id: str,
        *,
        principal_id: str = _ME,
        kind: PrincipalKind = PrincipalKind.USER,
        retry_policy: Optional[RetryPolicy] = None,
    ) -> None:
        """Revoke (hard-delete) a single registered key.

        Wraps `revoke_key`, supplying the live Identity Service client. Requires Identity Service
        mode to be enabled.

        :param key_id: The key id to revoke.
        :param principal_id: Target principal id; defaults to `"me"` (the caller,
                            on user routes). On agent routes you must pass an
                            explicit agent id — `"me"` is not valid there.
        :param kind: Whether the principal is a human USER (default) or AGENT.
        :param retry_policy: Bounded retry/backoff; defaults to the SDK retry knobs.
        :raises ConfigurationError: when Identity Service mode is not enabled.
        :raises ValueError: when `kind` is `AGENT` with no explicit `principal_id`
                            (`"me"` is not valid on agent routes).
        """
        self._reject_agent_self_route(principal_id, kind)
        revoke_key(
            self._require_ir_client(),
            principal_id,
            key_id,
            kind=kind,
            retry_policy=self._policy(retry_policy),
        )

    def generate_keypair_and_register(
        self,
        *,
        principal_id: Optional[str] = None,
        kind: PrincipalKind = PrincipalKind.USER,
        key_id: Optional[str] = None,
        name: Optional[str] = None,
        retry_policy: Optional[RetryPolicy] = None,
    ) -> RegisterKeyResult:
        """Generate a P-384 keypair and register it for a principal in one step.

        Wraps `generate_keypair_and_register`, supplying the live Identity Service client.
        Requires Identity Service mode to be enabled.

        Unlike the other CRUD operations the underlying helper needs a concrete
        principal id (not `"me"`) to bind the returned credentials to. When
        `principal_id` is omitted (or `"me"`) it defaults to the principal this
        client authenticates as — `IdentityServiceClient.client_id`, which is exactly
        what `"me"` resolves to for a human caller — so self-registration needs no
        argument. Pass an explicit id (admin only) to register for another principal.

        On agent routes the self default does not apply: an agent cannot register
        its own keys, so `kind=AGENT` requires an explicit agent `principal_id`.

        :param principal_id: Target principal id the key is registered for and bound
                            to; defaults to the caller's own principal id. Required
                            (no self default) on agent routes.
        :param kind: Whether the principal is a human USER (default) or AGENT.
        :param key_id: Key id to register; a random one is generated when omitted.
        :param name: Optional human-readable label for the key. When omitted (or
                     blank) the identity-service defaults the name to the key id.
        :param retry_policy: Bounded retry/backoff; defaults to the SDK retry knobs.
        :raises ConfigurationError: when Identity Service mode is not enabled.
        :raises ValueError: when `kind` is `AGENT` with no explicit `principal_id`
                            (an agent cannot register its own keys).
        """
        self._reject_agent_self_route(principal_id, kind)
        identity_service_client = self._require_ir_client()
        if not principal_id or principal_id == _ME:
            principal_id = identity_service_client.client_id
        return generate_keypair_and_register(
            identity_service_client,
            principal_id,
            kind=kind,
            key_id=key_id,
            retry_policy=self._policy(retry_policy),
            name=name,
        )


class KeyManagementMixin:
    """Mixin that exposes a `keys` accessor on the top-level clients.

    Concrete clients implement `_identity_service_config` to point at their configuration
    (the V2 `Client` and `V3Client` store it under different attribute names).
    """

    @property
    def _identity_service_config(self) -> Configuration:
        """Return the configuration backing the `keys` accessor.

        :raises NotImplementedError: unless overridden by the concrete client.
        """
        raise NotImplementedError

    @property
    def keys(self) -> KeyManagement:
        """Identity-service key exchange and CRUD operations for this client."""
        return KeyManagement(self._identity_service_config)
