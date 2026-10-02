"""Identity Service key management (register / list / get / revoke).

Manages a principal's ECDSA P-384 public keys against the identity-service's
key-management endpoints, authenticating with an identity-service-issued JWT
(obtained via `IdentityServiceClient`, RFC 7523 `private_key_jwt`). This is the
sibling surface to `key_exchange`: where `exchange_pat` registers a first key
using a raw Zitadel PAT, these wrappers manage keys for an already-authenticated
principal (and, for an admin browser session, for other principals in tenant).

Like `key_exchange`, hand-written because the Identity Service publishes no OpenAPI spec to
generate from.
"""

from __future__ import annotations

import json
import logging
import pprint
from typing import Any, ClassVar, Dict, List, Optional, Set
from urllib.parse import quote

from pydantic import (
    BaseModel,
    ConfigDict,
    StrictBool,
    StrictStr,
    ValidationError,
)
from typing_extensions import Self

from istari_digital_client.sdk._auth.identity_service import (
    IdentityServiceClient,
    PrincipalKind,
    RetryPolicy,
    _TransientHttpError,
    _validate_public_key_pem,
)
from istari_digital_client.sdk._auth.keys import (
    GeneratedClientCredentials,
    _CredentialsResult,
    generate_client_keypair,
)

logger = logging.getLogger("istari_digital_client._auth.key_registration")

# Route prefixes per principal kind; the collection path is
# "<prefix>/<principal_id>/keys" and a single key adds "/<key_id>".
_KEYS_ROUTE_PREFIXES: Dict[str, str] = {
    PrincipalKind.AGENT.value: "/api/v1/agents",
    PrincipalKind.USER.value: "/api/v1/users",
}

# Path value resolving to the authenticated caller's own principal. Valid on
# user routes only; cannot be used to derive a client id locally.
_ME_PARAM = "me"


class KeyRegistrationError(Exception):
    """Raised when an identity-service key-management operation fails.

    Carries the structured `error` code and HTTP `status` from the
    identity-service's error response when available, so callers can branch on
    them (e.g. distinguish `duplicate_key_id` from `not_found`). The raw
    response body is never included in the message.
    """

    def __init__(
        self,
        message: str,
        *,
        code: Optional[str] = None,
        status: Optional[int] = None,
    ) -> None:
        """Initialize the error with an optional server `code` and HTTP `status`."""
        super().__init__(message)
        self.code = code
        self.status = status


class RegisterKeyDto(BaseModel):
    """Internal wire body for a key registration.

    Carries the `key_id` and its PEM public key (ECDSA P-384; the
    identity-service rejects anything else). `username`/`display_name` are honored
    by the server only when an admin registers the first key for a not-yet-existing
    agent; they are omitted from the body when unset. `expires_at`, when set, is an
    RFC 3339 timestamp specifying when the key stops authenticating (must be in the
    future and at most one year out); when omitted the server defaults to one year.
    """

    key_id: StrictStr
    public_key_pem: StrictStr
    username: Optional[StrictStr] = None
    display_name: Optional[StrictStr] = None
    expires_at: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = [
        "key_id",
        "public_key_pem",
        "username",
        "display_name",
        "expires_at",
    ]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of RegisterKeyDto from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias."""
        excluded_fields: Set[str] = set()
        return self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RegisterKeyDto from a dict"""
        if obj is None:
            return None
        if not isinstance(obj, dict):
            return cls.model_validate(obj)
        return cls.model_validate(
            {
                "key_id": obj.get("key_id"),
                "public_key_pem": obj.get("public_key_pem"),
                "username": obj.get("username"),
                "display_name": obj.get("display_name"),
                "expires_at": obj.get("expires_at"),
            }
        )


class KeyMetadata(BaseModel):
    """Metadata for one registered key.

    Deliberately carries no key material — only the `key_id`, `algorithm`
    (always `ES384` for ECDSA P-384), the RFC3339 `created_at` timestamp, and
    the optional RFC3339 `expires_at` timestamp indicating when the key stops
    authenticating.
    """

    key_id: StrictStr
    name: Optional[StrictStr] = None
    algorithm: StrictStr
    created_at: StrictStr
    expires_at: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["key_id", "name", "algorithm", "created_at", "expires_at"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of KeyMetadata from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias."""
        excluded_fields: Set[str] = set()
        return self.model_dump(by_alias=True, exclude=excluded_fields, exclude_none=True)

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of KeyMetadata from a dict"""
        if obj is None:
            return None
        if not isinstance(obj, dict):
            return cls.model_validate(obj)
        return cls.model_validate(
            {
                "key_id": obj.get("key_id"),
                "name": obj.get("name"),
                "algorithm": obj.get("algorithm"),
                "created_at": obj.get("created_at"),
                "expires_at": obj.get("expires_at"),
            }
        )


class PrincipalKeys(BaseModel):
    """List payload: a principal's stable identifiers plus its registered keys.

    `client_id` is the principal's route id (the human/agent id). No key material
    is ever exposed — `keys` carries only `KeyMetadata`.
    """

    client_id: StrictStr
    user_uuid: StrictStr
    tenant_id: StrictStr
    enabled: StrictBool
    keys: List[KeyMetadata]
    __properties: ClassVar[List[str]] = [
        "client_id",
        "user_uuid",
        "tenant_id",
        "enabled",
        "keys",
    ]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of PrincipalKeys from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias."""
        excluded_fields: Set[str] = set()
        return self.model_dump(by_alias=True, exclude=excluded_fields, exclude_none=True)

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PrincipalKeys from a dict"""
        if obj is None:
            return None
        if not isinstance(obj, dict):
            return cls.model_validate(obj)
        raw_keys = obj.get("keys") or []
        return cls.model_validate(
            {
                "client_id": obj.get("client_id"),
                "user_uuid": obj.get("user_uuid"),
                "tenant_id": obj.get("tenant_id"),
                "enabled": obj.get("enabled"),
                "keys": [KeyMetadata.from_dict(k) for k in raw_keys],
            }
        )


class RegisterKeyResult(_CredentialsResult):
    """Result of `generate_keypair_and_register`."""

    metadata: KeyMetadata


def _route_prefix(kind: PrincipalKind) -> str:
    """Return the route prefix for `kind`, or raise `KeyRegistrationError`."""
    try:
        return _KEYS_ROUTE_PREFIXES[kind]
    except KeyError:
        raise KeyRegistrationError(
            f"Unknown principal kind {kind!r}; expected one of "
            f"{sorted(_KEYS_ROUTE_PREFIXES)}"
        ) from None


def _collection_path(kind: PrincipalKind, principal_id: str) -> str:
    """Build the keys-collection path (relative to the Identity Service base) for a principal."""
    prefix = _route_prefix(kind)
    return f"{prefix}/{quote(principal_id, safe='')}/keys"


def _key_path(kind: PrincipalKind, principal_id: str, key_id: str) -> str:
    """Build the single-key path (relative to the Identity Service base) for a principal's key."""
    return f"{_collection_path(kind, principal_id)}/{quote(key_id, safe='')}"


def _parse_key_metadata(data: Optional[bytes]) -> KeyMetadata:
    """Parse a 2xx body into `KeyMetadata`, mapping failures to retryable errors."""
    if not data:
        raise _TransientHttpError(
            "Identity-router returned an empty key metadata response"
        )
    try:
        parsed = KeyMetadata.from_json(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError, ValidationError) as e:
        raise _TransientHttpError(
            "Identity-router returned a malformed key metadata response"
        ) from e
    if parsed is None:
        raise _TransientHttpError(
            "Identity-router returned an empty key metadata response"
        )
    return parsed


def _parse_principal_keys(data: Optional[bytes]) -> PrincipalKeys:
    """Parse a 2xx body into `PrincipalKeys`, mapping failures to retryable errors."""
    if not data:
        raise _TransientHttpError(
            "Identity-router returned an empty key list response"
        )
    try:
        parsed = PrincipalKeys.from_json(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError, ValidationError) as e:
        raise _TransientHttpError(
            "Identity-router returned a malformed key list response"
        ) from e
    if parsed is None:
        raise _TransientHttpError(
            "Identity-router returned an empty key list response"
        )
    return parsed


def _parse_none(_data: Optional[bytes]) -> None:
    """Discard the body of a no-content (204) response."""
    return None


def register_key(
    ir_client: IdentityServiceClient,
    principal_id: str,
    credentials: GeneratedClientCredentials,
    *,
    kind: PrincipalKind = PrincipalKind.USER,
    retry_policy: Optional[RetryPolicy] = None,
    validate_public_key: bool = True,
    username: Optional[str] = None,
    display_name: Optional[str] = None,
    expires_at: Optional[str] = None,
) -> KeyMetadata:
    """Register a principal's ECDSA P-384 public key with the identity-service.

    Registers `credentials.public_key_pem` under `credentials.key_id` for
    `principal_id`, authenticating with an identity-service JWT minted by
    `ir_client`. To manage your own keys, pass your principal id (or ``"me"`` on
    user routes); to manage another principal's keys you must be an admin and
    the target must be in your tenant.

    :param ir_client: Authenticated identity-service client; supplies both the
                      target base URL and the bearer token (its private_key_jwt is
                      exchanged for an Identity Service JWT).
    :param principal_id: Target principal id; ``"me"`` resolves server-side to the
                         caller (user routes only).
    :param credentials: The keypair to register. Only its public key and key id
                        are sent; the private key is never transmitted. Must be
                        ECDSA P-384.
    :param kind: Whether the principal is a human USER (default) or AGENT.
    :param retry_policy: Bounded retry/backoff for transient failures (defaults
                         to the identity-service client's configured policy).
    :param validate_public_key: When True (default), check the public key is
                                ECDSA P-384 before registering.
    :param username: Optional; honored only when an admin registers the first key
                     for a not-yet-existing agent (seeds the new agent).
    :param display_name: Optional; seeds a new agent's display name (see `username`).
    :param expires_at: Optional RFC 3339 timestamp for key expiration. Must be in
                       the future and at most one year out. Omit to use the
                       server default (one year).
    :raises KeyRegistrationError: on invalid input, a 4xx client error (e.g.
                                  `duplicate_key_id`), or once the retry budget for
                                  transient failures is exhausted.
    """
    if validate_public_key:
        _validate_public_key_pem(
            credentials.public_key_pem, error_cls=KeyRegistrationError
        )

    dto = RegisterKeyDto(
        key_id=credentials.key_id,
        public_key_pem=credentials.public_key_pem,
        username=username,
        display_name=display_name,
        expires_at=expires_at,
    )
    path = _collection_path(kind, principal_id)
    metadata = ir_client.request(
        "POST",
        path,
        _parse_key_metadata,
        body=dto.to_json().encode("utf-8"),
        error_cls=KeyRegistrationError,
        retry_policy=retry_policy,
    )
    logger.info(
        "Registered key with identity-service "
        "(kind=%s, principal_id=%s, key_id=%s)",
        kind,
        principal_id,
        metadata.key_id,
    )
    return metadata


def list_keys(
    ir_client: IdentityServiceClient,
    principal_id: str,
    *,
    kind: PrincipalKind = PrincipalKind.USER,
    retry_policy: Optional[RetryPolicy] = None,
) -> PrincipalKeys:
    """List a principal's registered keys (metadata only, no key material).

    :param ir_client: Authenticated identity-service client; supplies the target
                      base URL and the bearer token.
    :param principal_id: Target principal id; ``"me"`` resolves to the caller (user routes).
    :param kind: Whether the principal is a human USER (default) or AGENT.
    :param retry_policy: Bounded retry/backoff for transient failures.
    :raises KeyRegistrationError: on a 4xx client error or exhausted retry budget.
    """
    path = _collection_path(kind, principal_id)
    return ir_client.request(
        "GET",
        path,
        _parse_principal_keys,
        error_cls=KeyRegistrationError,
        retry_policy=retry_policy,
    )


def get_key(
    ir_client: IdentityServiceClient,
    principal_id: str,
    key_id: str,
    *,
    kind: PrincipalKind = PrincipalKind.USER,
    retry_policy: Optional[RetryPolicy] = None,
) -> KeyMetadata:
    """Fetch the metadata for a single registered key.

    :param ir_client: Authenticated identity-service client; supplies the target
                      base URL and the bearer token.
    :param principal_id: Target principal id; ``"me"`` resolves to the caller (user routes).
    :param key_id: The key id to fetch.
    :param kind: Whether the principal is a human USER (default) or AGENT.
    :param retry_policy: Bounded retry/backoff for transient failures.
    :raises KeyRegistrationError: if the key is not found (HTTP 404), on any other
                                  4xx client error, or once the retry budget is exhausted.
    """
    path = _key_path(kind, principal_id, key_id)
    return ir_client.request(
        "GET",
        path,
        _parse_key_metadata,
        error_cls=KeyRegistrationError,
        retry_policy=retry_policy,
    )


def revoke_key(
    ir_client: IdentityServiceClient,
    principal_id: str,
    key_id: str,
    *,
    kind: PrincipalKind = PrincipalKind.USER,
    retry_policy: Optional[RetryPolicy] = None,
) -> None:
    """Revoke (hard-delete) a single registered key.

    :param ir_client: Authenticated identity-service client; supplies the target
                      base URL and the bearer token.
    :param principal_id: Target principal id; ``"me"`` resolves to the caller (user routes).
    :param key_id: The key id to revoke.
    :param kind: Whether the principal is a human USER (default) or AGENT.
    :param retry_policy: Bounded retry/backoff for transient failures.
    :raises KeyRegistrationError: if the key is not found (HTTP 404), on any other
                                  4xx client error, or once the retry budget is exhausted.
    """
    path = _key_path(kind, principal_id, key_id)
    ir_client.request(
        "DELETE",
        path,
        _parse_none,
        error_cls=KeyRegistrationError,
        retry_policy=retry_policy,
    )
    logger.info(
        "Revoked key with identity-service (kind=%s, principal_id=%s, key_id=%s)",
        kind,
        principal_id,
        key_id,
    )


def generate_keypair_and_register(
    ir_client: IdentityServiceClient,
    principal_id: str,
    *,
    kind: PrincipalKind = PrincipalKind.USER,
    key_id: Optional[str] = None,
    retry_policy: Optional[RetryPolicy] = None,
    expires_at: Optional[str] = None,
) -> RegisterKeyResult:
    """Generate a P-384 keypair and register it for a principal in one step.

    Convenience wrapper over `register_key`: generates a fresh ECDSA P-384 keypair
    via `generate_client_keypair`, registers its public key for `principal_id`, and
    returns a result whose `credentials` are bound to `principal_id` and the
    registered key id — ready to persist via `result.write_credentials_json(path)`
    for use by `IdentityServiceClient`.

    Because the register response carries no client id, `principal_id` must be an
    explicit id (not ``"me"``) so the returned credentials can be formed.

    :param ir_client: Authenticated identity-service client; supplies the target
                      base URL and the bearer token.
    :param principal_id: Target principal id the key is registered for and bound to.
    :param kind: Whether the principal is a human USER (default) or AGENT.
    :param key_id: Key id to register; a random one is generated when omitted.
    :param retry_policy: Bounded retry/backoff for transient failures.
    :param expires_at: Optional RFC 3339 timestamp for key expiration. Must be in
                       the future and at most one year out. Omit to use the
                       server default (one year).
    :raises KeyRegistrationError: if `principal_id` is ``"me"``, on a 4xx client
                                  error, or once the retry budget is exhausted.
    """
    if principal_id == _ME_PARAM:
        raise KeyRegistrationError(
            'generate_keypair_and_register requires an explicit principal_id; '
            '"me" cannot be bound to the returned credentials'
        )

    credentials = generate_client_keypair(client_id=principal_id, key_id=key_id)
    metadata = register_key(
        ir_client,
        principal_id,
        credentials,
        kind=kind,
        retry_policy=retry_policy,
        validate_public_key=False,
        expires_at=expires_at,
    )
    # Bind the keypair to the authoritative key id echoed by the server.
    rebound = credentials.model_copy(update={"key_id": metadata.key_id})
    return RegisterKeyResult(metadata=metadata, credentials=rebound)
