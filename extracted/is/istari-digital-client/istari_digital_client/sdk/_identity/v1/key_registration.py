"""Identity Service key management (register / list / get / revoke).

Manages a principal's ECDSA P-384 public keys against the identity-service's
key-management endpoints, authenticating with an identity-service-issued JWT
(obtained via `IdentityServiceClient`, RFC 7523 `private_key_jwt`). This is the
sibling surface to `key_exchange`: where `exchange_pat` registers a first key
using a raw Zitadel PAT, these wrappers manage keys for an already-authenticated
principal (and, for an admin browser session, for other principals in tenant).

Like `key_exchange`, hand-written because the Identity Service publishes no OpenAPI spec to
generate from.

Every function here takes an `api_version` keyword, an `IdentityApiVersion` or its
string. ``"auto"``, the default, uses identity-service's v2 key routes
(``/api/v2/principals/{id}/keys``) when the identity-service client was built for v2
and v2 can address the call, resolving a v1 id to its principal UUID over v2.
Otherwise it uses the deprecated v1 routes with a token from the v1 token endpoint,
minted from the same credentials, so a v2 token never reaches a v1 route. A call that
reaches a v1 route warns once per process. Return types are the same either way.
"""

from __future__ import annotations

import json
import logging
import pprint
import re
from typing import Any, Callable, ClassVar, Dict, List, Optional, Set, TypeVar
from urllib.parse import quote

from pydantic import (
    BaseModel,
    ConfigDict,
    StrictBool,
    StrictStr,
    ValidationError,
)
from typing_extensions import Self

from istari_digital_client.sdk._identity.auth.identity_service import (
    IdentityApiVersion,
    IdentityApiVersionLike,
    IdentityServiceClient,
    PrincipalKind,
    RetryPolicy,
    _TransientHttpError,
    _validate_public_key_pem,
)
from istari_digital_client.sdk._identity.auth.keys import (
    GeneratedClientCredentials,
    _CredentialsResult,
    generate_client_keypair,
)
from istari_digital_client.sdk._identity.v1._deprecation import (
    _configuration_error,
    configured_api_version,
    no_v2_form_message,
    normalize_api_version,
    warn_v1,
)

logger = logging.getLogger("istari_digital_client.sdk._identity.v1.key_registration")

# Route prefixes per principal kind; the collection path is
# "<prefix>/<principal_id>/keys" and a single key adds "/<key_id>".
_KEYS_ROUTE_PREFIXES: Dict[str, str] = {
    PrincipalKind.AGENT.value: "/api/v1/agents",
    PrincipalKind.USER.value: "/api/v1/users",
}

# Path value resolving to the authenticated caller's own principal. Valid on
# user routes only; cannot be used to derive a client id locally.
_ME_PARAM = "me"

_V2_KEYS_ROUTE_PREFIX = "/api/v2/principals"
# The canonical form; identity-service also parses others, which v1 ids could collide with.
_UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)

_T = TypeVar("_T")


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


def _require_kind(kind: PrincipalKind) -> None:
    """Raise `KeyRegistrationError` unless `kind` is a known principal kind."""
    if kind not in _KEYS_ROUTE_PREFIXES:
        raise KeyRegistrationError(
            f"Unknown principal kind {kind!r}; expected one of "
            f"{sorted(_KEYS_ROUTE_PREFIXES)}"
        )


def _route_prefix(kind: PrincipalKind) -> str:
    """Return the route prefix for `kind`, or raise `KeyRegistrationError`."""
    _require_kind(kind)
    return _KEYS_ROUTE_PREFIXES[kind]


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


def _parse_principal_keys_v2(data: Optional[bytes]) -> PrincipalKeys:
    """Parse a 2xx v2 list body into the v1 `PrincipalKeys` shape."""
    if not data:
        raise _TransientHttpError(
            "Identity-router returned an empty key list response"
        )
    try:
        body = json.loads(data.decode("utf-8"))
        if not isinstance(body, dict):
            raise _TransientHttpError(
                "Identity-router returned a malformed key list response"
            )
        parsed = PrincipalKeys.from_dict(
            {
                "client_id": body.get("client_id"),
                "user_uuid": body.get("principal_id"),
                "tenant_id": body.get("tenant_id"),
                "enabled": body.get("active"),
                "keys": body.get("keys"),
            }
        )
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


def _parse_principal_ids(data: Optional[bytes]) -> list[str]:
    """Parse a 2xx v2 principal listing into the principal ids it holds."""
    try:
        body = json.loads((data or b"").decode("utf-8"))
        if not isinstance(body, dict):
            raise TypeError("listing is not an object")
        items = body.get("items") or []  # an empty page's items arrive as null
        if not isinstance(items, list):
            raise TypeError("items is not a list")
        return [str(item["principal_id"]) for item in items]
    except (ValueError, KeyError, TypeError, UnicodeDecodeError) as e:
        raise _TransientHttpError(
            "Identity-service returned a malformed principal listing"
        ) from e


def _v2_collection_path(principal_id: str) -> str:
    """Build the v2 keys-collection path for a principal UUID or ``"me"``."""
    return f"{_V2_KEYS_ROUTE_PREFIX}/{quote(principal_id, safe='')}/keys"


def _v2_key_path(principal_id: str, key_id: str) -> str:
    """Build the v2 single-key path for a principal UUID or ``"me"``."""
    return f"{_v2_collection_path(principal_id)}/{quote(key_id, safe='')}"


def _for_version(
    client: IdentityServiceClient, api_version: IdentityApiVersion
) -> IdentityServiceClient:
    """`client`, or its sibling on the same credentials whose token suits `api_version`'s routes."""
    if client is None or not hasattr(client, "for_api_version"):
        return client
    return client.for_api_version(api_version)


def _route(
    operation: str,
    version: IdentityApiVersion,
    client: IdentityServiceClient,
    principal_id: str,
    kind: PrincipalKind,
    *,
    seed_argument: Optional[str] = None,
) -> IdentityApiVersion:
    """Return ``V1`` or ``V2``, the route `operation` tries first. Sends nothing.

    :raises ConfigurationError: for ``V2`` on a call v2 cannot express.
    """
    if version is IdentityApiVersion.V1 or (
        version is IdentityApiVersion.AUTO and configured_api_version(client) is IdentityApiVersion.V1
    ):
        return IdentityApiVersion.V1
    argument = reason = None
    if seed_argument is not None:
        argument = seed_argument
        reason = (
            "cannot use identity-service v2 with username or display_name, "
            "which only seed a new agent on the v1 route"
        )
    elif principal_id == _ME_PARAM and kind == PrincipalKind.AGENT:
        argument = "principal_id='me' with kind=AGENT"
        reason = "cannot use identity-service v2 for 'me' on agent routes"
    if reason is None:
        return IdentityApiVersion.V2
    if version is IdentityApiVersion.V2:
        raise _configuration_error()(no_v2_form_message(operation, reason))
    logger.warning(
        "%s: %s has no identity-service v2 equivalent, so this call used "
        "identity-service's deprecated v1 API",
        operation,
        argument,
    )
    return IdentityApiVersion.V1


def _not_visible(label: str, field: str, principal_id: str) -> KeyRegistrationError:
    """The ``principal_not_found`` error for an id no visible principal answers to."""
    return KeyRegistrationError(
        f"No {label} principal with {field} {principal_id!r} is visible on "
        "identity-service v2; it may not exist, or the caller may lack permission "
        "to see it. Pass its principal UUID instead",
        code="principal_not_found",
        status=404,
    )


def _lookup_labels(kind: PrincipalKind) -> tuple[str, str, str, str]:
    """Label, field name, v2 collection and filter for looking up a `kind` by its v1 id."""
    if kind == PrincipalKind.AGENT:
        return "agent", "client id", "agents", "client_id"
    return "user", "upstream user id", "humans", "upstream_user_id"


def _v2_principal_id(
    client: IdentityServiceClient,
    principal_id: str,
    kind: PrincipalKind,
    retry_policy: Optional[RetryPolicy],
    explicit: bool,
) -> tuple[Optional[str], bool]:
    """The v2 target for `principal_id`, and whether its holder must still be checked.

    A caller's id is tried as a v1 id first: agents by client id, users by upstream user
    id, a UUID-shaped one included. A UUID that matches nothing is taken as a principal
    UUID. A None target sends the call to v1 instead.

    :raises KeyRegistrationError: when `explicit` and the id resolves to no principal
                                  (``principal_not_found``) or several
                                  (``principal_ambiguous``), or when the lookup fails
                                  other than with a 403 under ``"auto"``.
    """
    if principal_id == _ME_PARAM:
        return principal_id, False
    label, field, collection, query = _lookup_labels(kind)
    path = f"{_V2_KEYS_ROUTE_PREFIX}/{collection}?{query}={quote(principal_id, safe='')}&limit=2"
    try:
        matches = _for_version(client, IdentityApiVersion.V2).request(
            "GET",
            path,
            _parse_principal_ids,
            error_cls=KeyRegistrationError,
            retry_policy=retry_policy,
        )
    except KeyRegistrationError as e:
        # A caller refused the listing may still hold the id on v1, where it is native.
        if explicit or e.status != 403:
            raise
        return None, False
    if len(matches) == 1:
        # An upstream user id need not be the person's v1 id; the key list confirms it.
        return matches[0], kind != PrincipalKind.AGENT
    if not matches and _UUID_RE.match(principal_id):
        return principal_id, False
    if not explicit:
        return None, False
    if not matches:
        raise _not_visible(label, field, principal_id)
    raise KeyRegistrationError(
        f"More than one {label} principal has {field} {principal_id!r} on "
        "identity-service v2; pass its principal UUID instead",
        code="principal_ambiguous",
    )


def _holder_is(
    listing: PrincipalKeys, principal_id: str, kind: PrincipalKind, explicit: bool
) -> bool:
    """Whether the v2 key holder in `listing` is `principal_id`; ``"v2"`` raises if not."""
    if listing.client_id == principal_id:
        return True
    if explicit:
        _, field, _, _ = _lookup_labels(kind)
        raise _not_visible("user", field, principal_id)
    return False


def _dispatch(
    operation: str,
    replacement: str,
    route: IdentityApiVersion,
    version: IdentityApiVersion,
    client: IdentityServiceClient,
    principal_id: str,
    kind: PrincipalKind,
    retry_policy: Optional[RetryPolicy],
    v2: Callable[[IdentityServiceClient, str], _T],
    v1: Callable[[IdentityServiceClient], _T],
    *,
    v2_lists_keys: bool = False,
) -> _T:
    """Run `v2` with the v2 principal id, or `v1`, each with a client whose token suits the route.

    Under ``"auto"`` an id the v2 lookup cannot pin to one principal, or one whose
    resolved holder is someone else, runs on v1, where it is a native id. A holder is
    checked before any v2 call, except when `v2` itself returns the key list.
    """
    if route is IdentityApiVersion.V2:
        explicit = version is IdentityApiVersion.V2
        target, check_holder = _v2_principal_id(
            client, principal_id, kind, retry_policy, explicit
        )
        v2_client = _for_version(client, IdentityApiVersion.V2)
        if target is not None and check_holder and not v2_lists_keys:
            listing = _list_v2(v2_client, target, retry_policy)
            if not _holder_is(listing, principal_id, kind, explicit):
                target = None
        if target is not None:
            result = v2(v2_client, target)
            if not (check_holder and v2_lists_keys):
                return result
            assert isinstance(result, PrincipalKeys)
            if _holder_is(result, principal_id, kind, explicit):
                return result
    warn_v1(operation, replacement)
    return v1(_for_version(client, IdentityApiVersion.V1))


def _list_v2(
    client: IdentityServiceClient, target: str, retry_policy: Optional[RetryPolicy]
) -> PrincipalKeys:
    """GET the v2 key list for a principal UUID or ``"me"``."""
    return client.request(
        "GET",
        _v2_collection_path(target),
        _parse_principal_keys_v2,
        error_cls=KeyRegistrationError,
        retry_policy=retry_policy,
    )


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
    api_version: Optional[IdentityApiVersionLike] = IdentityApiVersion.AUTO,
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
                     for a not-yet-existing agent (seeds the new agent). Sends the
                     call to v1.
    :param display_name: Optional; seeds a new agent's display name (see `username`).
    :param expires_at: Optional RFC 3339 timestamp for key expiration. Must be in
                       the future and at most one year out. Omit to use the
                       server default (one year).
    :param api_version: An `IdentityApiVersion` or its string. ``"auto"`` (default;
                        ``None`` means the same) uses the v2 route
                        when the client was built for v2 and v2 can address the call
                        (``"me"``, an id the lookup resolves to one principal, or a UUID that matches nothing),
                        and the v1 route with a v1 token otherwise. ``"v1"`` and
                        ``"v2"`` force a route.
    :raises ConfigurationError: for an invalid `api_version`, or ``"v2"`` on a call
                                with no v2 form.
    :raises KeyRegistrationError: on invalid input, a 4xx client error (e.g.
                                  `duplicate_key_id`), an unresolvable id under
                                  ``"v2"``, or once the retry budget for transient
                                  failures is exhausted.
    """
    version = normalize_api_version(api_version)
    _require_kind(kind)
    route = _route(
        "register_key",
        version,
        ir_client,
        principal_id,
        kind,
        seed_argument="username"
        if username is not None
        else ("display_name" if display_name is not None else None),
    )
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
    body = dto.to_json().encode("utf-8")

    def send(client: IdentityServiceClient, path: str) -> KeyMetadata:
        return client.request(
            "POST",
            path,
            _parse_key_metadata,
            body=body,
            error_cls=KeyRegistrationError,
            retry_policy=retry_policy,
        )

    metadata = _dispatch(
        "register_key",
        "admin.identity.keys.register",
        route,
        version,
        ir_client,
        principal_id,
        kind,
        retry_policy,
        lambda client, target: send(client, _v2_collection_path(target)),
        lambda client: send(client, _collection_path(kind, principal_id)),
    )
    logger.info(
        "Registered key with identity-service (kind=%s, principal_id=%s, key_id=%s)",
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
    api_version: Optional[IdentityApiVersionLike] = IdentityApiVersion.AUTO,
) -> PrincipalKeys:
    """List a principal's registered keys (metadata only, no key material).

    The result has the same shape whichever API version served it: a v2 response's
    ``principal_id`` and ``active`` arrive as `user_uuid` and `enabled`.

    :param ir_client: Authenticated identity-service client; supplies the target
                      base URL and the bearer token.
    :param principal_id: Target principal id; ``"me"`` resolves to the caller (user routes).
    :param kind: Whether the principal is a human USER (default) or AGENT.
    :param retry_policy: Bounded retry/backoff for transient failures.
    :param api_version: Routes the call as `register_key` does.
    :raises ConfigurationError: for an invalid `api_version`, or ``"v2"`` on a call
                                with no v2 form.
    :raises KeyRegistrationError: on an unknown `kind`, a 4xx client error, an
                                  unresolvable id under ``"v2"``, or an exhausted retry budget.
    """
    version = normalize_api_version(api_version)
    _require_kind(kind)
    route = _route("list_keys", version, ir_client, principal_id, kind)
    return _dispatch(
        "list_keys",
        "admin.identity.keys.list",
        route,
        version,
        ir_client,
        principal_id,
        kind,
        retry_policy,
        lambda client, target: _list_v2(client, target, retry_policy),
        lambda client: client.request(
            "GET",
            _collection_path(kind, principal_id),
            _parse_principal_keys,
            error_cls=KeyRegistrationError,
            retry_policy=retry_policy,
        ),
        v2_lists_keys=True,
    )


def get_key(
    ir_client: IdentityServiceClient,
    principal_id: str,
    key_id: str,
    *,
    kind: PrincipalKind = PrincipalKind.USER,
    retry_policy: Optional[RetryPolicy] = None,
    api_version: Optional[IdentityApiVersionLike] = IdentityApiVersion.AUTO,
) -> KeyMetadata:
    """Fetch the metadata for a single registered key.

    :param ir_client: Authenticated identity-service client; supplies the target
                      base URL and the bearer token.
    :param principal_id: Target principal id; ``"me"`` resolves to the caller (user routes).
    :param key_id: The key id to fetch.
    :param kind: Whether the principal is a human USER (default) or AGENT.
    :param retry_policy: Bounded retry/backoff for transient failures.
    :param api_version: Routes the call as `register_key` does.
    :raises ConfigurationError: for an invalid `api_version`, or ``"v2"`` on a call
                                with no v2 form.
    :raises KeyRegistrationError: on an unknown `kind`, if the key is not found
                                  (HTTP 404), on any other 4xx client error, an
                                  unresolvable id under ``"v2"``, or once the retry
                                  budget is exhausted.
    """
    version = normalize_api_version(api_version)
    _require_kind(kind)
    route = _route("get_key", version, ir_client, principal_id, kind)

    def send(client: IdentityServiceClient, path: str) -> KeyMetadata:
        return client.request(
            "GET",
            path,
            _parse_key_metadata,
            error_cls=KeyRegistrationError,
            retry_policy=retry_policy,
        )

    return _dispatch(
        "get_key",
        "admin.identity.keys.get",
        route,
        version,
        ir_client,
        principal_id,
        kind,
        retry_policy,
        lambda client, target: send(client, _v2_key_path(target, key_id)),
        lambda client: send(client, _key_path(kind, principal_id, key_id)),
    )


def revoke_key(
    ir_client: IdentityServiceClient,
    principal_id: str,
    key_id: str,
    *,
    kind: PrincipalKind = PrincipalKind.USER,
    retry_policy: Optional[RetryPolicy] = None,
    api_version: Optional[IdentityApiVersionLike] = IdentityApiVersion.AUTO,
) -> None:
    """Revoke (hard-delete) a single registered key.

    :param ir_client: Authenticated identity-service client; supplies the target
                      base URL and the bearer token.
    :param principal_id: Target principal id; ``"me"`` resolves to the caller (user routes).
    :param key_id: The key id to revoke.
    :param kind: Whether the principal is a human USER (default) or AGENT.
    :param retry_policy: Bounded retry/backoff for transient failures.
    :param api_version: Routes the call as `register_key` does.
    :raises ConfigurationError: for an invalid `api_version`, or ``"v2"`` on a call
                                with no v2 form.
    :raises KeyRegistrationError: on an unknown `kind`, if the key is not found
                                  (HTTP 404), on any other 4xx client error, an
                                  unresolvable id under ``"v2"``, or once the retry
                                  budget is exhausted.
    """
    version = normalize_api_version(api_version)
    _require_kind(kind)
    route = _route("revoke_key", version, ir_client, principal_id, kind)

    def send(client: IdentityServiceClient, path: str) -> None:
        client.request(
            "DELETE",
            path,
            _parse_none,
            error_cls=KeyRegistrationError,
            retry_policy=retry_policy,
        )

    _dispatch(
        "revoke_key",
        "admin.identity.keys.revoke",
        route,
        version,
        ir_client,
        principal_id,
        kind,
        retry_policy,
        lambda client, target: send(client, _v2_key_path(target, key_id)),
        lambda client: send(client, _key_path(kind, principal_id, key_id)),
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
    api_version: Optional[IdentityApiVersionLike] = IdentityApiVersion.AUTO,
) -> RegisterKeyResult:
    """Generate a P-384 keypair and register it for a principal in one step.

    Convenience wrapper over `register_key`: generates a fresh ECDSA P-384 keypair
    via `generate_client_keypair`, registers its public key for `principal_id`, and
    returns a result whose `credentials` are bound to the key holder's client id and
    the registered key id — ready to persist via `result.write_credentials_json(path)`
    for use by `IdentityServiceClient`.

    On v1 the client id is `principal_id`. On v2 it is the holder's row id, which a
    v2 key listing reads before registering. `principal_id` must be an explicit id
    (not ``"me"``).

    :param ir_client: Authenticated identity-service client; supplies the target
                      base URL and the bearer token.
    :param principal_id: Target principal id the key is registered for and bound to.
    :param kind: Whether the principal is a human USER (default) or AGENT.
    :param key_id: Key id to register; a random one is generated when omitted.
    :param retry_policy: Bounded retry/backoff for transient failures.
    :param expires_at: Optional RFC 3339 timestamp for key expiration. Must be in
                       the future and at most one year out. Omit to use the
                       server default (one year).
    :param api_version: Routes the registration as `register_key` does.
    :raises ConfigurationError: for an invalid `api_version`.
    :raises KeyRegistrationError: if `principal_id` is ``"me"``, on an unknown `kind`,
                                  on a 4xx client error, an unresolvable id under
                                  ``"v2"``, or once the retry budget is exhausted.
    """
    version = normalize_api_version(api_version)
    _require_kind(kind)
    if principal_id == _ME_PARAM:
        raise KeyRegistrationError(
            "generate_keypair_and_register requires an explicit principal_id; "
            '"me" cannot be bound to the returned credentials'
        )

    operation = "generate_keypair_and_register"
    route = _route(operation, version, ir_client, principal_id, kind)
    target, check_holder = None, False
    if route is IdentityApiVersion.V2:
        target, check_holder = _v2_principal_id(
            ir_client,
            principal_id,
            kind,
            retry_policy,
            version is IdentityApiVersion.V2,
        )
    client_id = principal_id
    v2_client = _for_version(ir_client, IdentityApiVersion.V2)
    if target is not None:
        # A v2 key authenticates as its holder's row id, which only the v2 listing reports.
        listing = _list_v2(v2_client, target, retry_policy)
        if check_holder and not _holder_is(
            listing, principal_id, kind, version is IdentityApiVersion.V2
        ):
            target = None
        else:
            client_id = listing.client_id

    credentials = generate_client_keypair(client_id=client_id, key_id=key_id)
    if target is not None:
        dto = RegisterKeyDto(
            key_id=credentials.key_id,
            public_key_pem=credentials.public_key_pem,
            expires_at=expires_at,
        )
        metadata = v2_client.request(
            "POST",
            _v2_collection_path(target),
            _parse_key_metadata,
            body=dto.to_json().encode("utf-8"),
            error_cls=KeyRegistrationError,
            retry_policy=retry_policy,
        )
    else:
        warn_v1(operation, "admin.identity.keys.generate_and_register")
        metadata = register_key(
            ir_client,
            principal_id,
            credentials,
            kind=kind,
            retry_policy=retry_policy,
            validate_public_key=False,
            expires_at=expires_at,
            api_version=IdentityApiVersion.V1,
        )
    # Bind the keypair to the authoritative key id echoed by the server.
    rebound = credentials.model_copy(update={"key_id": metadata.key_id})
    return RegisterKeyResult(metadata=metadata, credentials=rebound)
