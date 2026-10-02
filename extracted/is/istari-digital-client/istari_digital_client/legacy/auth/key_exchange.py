"""Identity Service PAT-to-key exchange.

Registers a client's ECDSA P-384 public key with the identity-service by
authenticating with a raw Zitadel Personal Access Token (PAT). This is the
bootstrap step that mints a client's first key: it runs before any
`IdentityServiceClient` exists, so it drives the shared request primitives in
`identity_service` directly with the PAT.
"""

from __future__ import annotations

import json
import logging
import pprint
from typing import Any, ClassVar, Dict, List, Optional, Set

from pydantic import (
    BaseModel,
    ConfigDict,
    StrictStr,
    ValidationError,
)
from typing_extensions import Self

from istari_digital_client.legacy.auth.identity_service import (
    PrincipalKind,
    RetryPolicy,
    _send_once,
    _send_with_retry,
    _TransientHttpError,
)
from istari_digital_client.legacy.auth.identity_service import (
    _validate_public_key_pem as _identity_service_validate_public_key_pem,
)
from istari_digital_client.legacy.auth.keys import (
    GeneratedClientCredentials,
    _CredentialsResult,
    generate_client_keypair,
)

logger = logging.getLogger("istari_digital_client.legacy.auth.key_exchange")

# `PrincipalKind` is imported from `identity_service` (its canonical home) and
# re-exported here for callers that import it from the PAT-exchange surface.

_ROUTES: Dict[str, str] = {
    PrincipalKind.AGENT.value: "/api/v1/agents/exchange-pat",
    PrincipalKind.USER.value: "/api/v1/users/exchange-pat",
}


class ExchangePatError(Exception):
    """Raised when the identity-service PAT-to-key exchange fails.

    Carries the structured `error` code and HTTP `status` from the
    identity-service's error response when available, so callers can branch on
    them (e.g. distinguish `invalid_pat` from `duplicate_key_id`). The raw
    response body and the PAT are never included in the message.
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


class ExchangePatDto(BaseModel):
    """Internal wire body for a PAT-to-key exchange: a `key_id` and its PEM public key.

    The public key must be ECDSA P-384 (ES384); the identity-service rejects anything else.
    `name` is an optional human-readable label for the key; it is omitted from the body
    when unset, and the identity-service defaults a blank/omitted name to the key id.
    """

    key_id: StrictStr
    public_key_pem: StrictStr
    name: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["key_id", "public_key_pem", "name"]

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
        """Create an instance of ExchangePatDto from a JSON string"""
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
        """Create an instance of ExchangePatDto from a dict"""
        if obj is None:
            return None
        if not isinstance(obj, dict):
            return cls.model_validate(obj)
        return cls.model_validate(
            {
                "key_id": obj.get("key_id"),
                "public_key_pem": obj.get("public_key_pem"),
                "name": obj.get("name"),
            }
        )


class ExchangePatResponseDto(BaseModel):
    """Response body for a successful PAT-to-key exchange.

    `client_id` is server-authoritative (derived from the Zitadel claims — `sub`
    for agents, `preferred_username` for users); any locally-chosen client id is
    ignored. Use this value as the `iss`/`sub` of subsequent `private_key_jwt`
    assertions.
    """

    client_id: StrictStr
    key_id: StrictStr
    tenant_id: StrictStr
    user_uuid: StrictStr
    name: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = [
        "client_id",
        "key_id",
        "tenant_id",
        "user_uuid",
        "name",
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
        """Create an instance of ExchangePatResponseDto from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias."""
        excluded_fields: Set[str] = set()
        return self.model_dump(by_alias=True, exclude=excluded_fields, exclude_none=True)

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ExchangePatResponseDto from a dict"""
        if obj is None:
            return None
        if not isinstance(obj, dict):
            return cls.model_validate(obj)
        return cls.model_validate(
            {
                "client_id": obj.get("client_id"),
                "key_id": obj.get("key_id"),
                "tenant_id": obj.get("tenant_id"),
                "user_uuid": obj.get("user_uuid"),
                "name": obj.get("name"),
            }
        )


class ExchangePatResult(_CredentialsResult):
    """Result of a PAT-to-key exchange."""

    client_id: str
    key_id: str
    tenant_id: str
    user_uuid: str
    name: Optional[str] = None

    @classmethod
    def _from_response(
        cls,
        response: ExchangePatResponseDto,
        credentials: GeneratedClientCredentials,
    ) -> Self:
        """Build a result from a wire response and the (rebound) credentials."""
        return cls(
            client_id=response.client_id,
            key_id=response.key_id,
            tenant_id=response.tenant_id,
            user_uuid=response.user_uuid,
            name=response.name,
            credentials=credentials,
        )


def _validate_public_key_pem(public_key_pem: str) -> None:
    """Validate that `public_key_pem` is an ECDSA P-384 public key.

    :raises ExchangePatError: if the PEM is unparseable or not ECDSA P-384.
    """
    _identity_service_validate_public_key_pem(public_key_pem, error_cls=ExchangePatError)


def _parse_exchange_response(data: Optional[bytes]) -> ExchangePatResponseDto:
    """Parse a 2xx body into `ExchangePatResponseDto`.

    Maps an empty or malformed body to a transient failure so it is retried like
    any other transient error inside `_send_with_retry`.
    """
    if not data:
        raise _TransientHttpError(
            "Identity-service returned an empty PAT exchange response"
        )
    try:
        parsed = ExchangePatResponseDto.from_json(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError, ValidationError) as e:
        raise _TransientHttpError(
            "Identity-service returned a malformed PAT exchange response"
        ) from e
    if parsed is None:
        raise _TransientHttpError(
            "Identity-service returned an empty PAT exchange response"
        )
    return parsed


def exchange_pat(
    identity_service_url: str,
    pat: str,
    credentials: GeneratedClientCredentials,
    *,
    kind: PrincipalKind = PrincipalKind.USER,
    retry_policy: Optional[RetryPolicy] = None,
    validate_public_key: bool = True,
    name: Optional[str] = None,
) -> ExchangePatResult:
    """Exchange a Zitadel PAT for identity-service client credentials.

    Registers the public key from `credentials` against the identity-service,
    authenticating with the raw Zitadel PAT. The returned result carries the
    server-authoritative `client_id` (the locally chosen one is discarded — the
    server derives it from the Zitadel claims) and the same keypair rebound to
    that `client_id`, so `result.write_credentials_json(path)` yields
    ready-to-use Identity Service credentials.

    :param identity_service_url: Base URL of the identity-service.
    :param pat: Zitadel Personal Access Token for the caller.
    :param credentials: The caller's keypair (e.g. from `generate_client_keypair()`
                        or `GeneratedClientCredentials.read_credentials_json()`).
                        Its public key is registered; its private key is retained
                        on the result. Must be ECDSA P-384.
    :param kind: Whether the PAT and key are for a human USER (default) or AGENT.
    :param retry_policy: Bounded retry/backoff for transient failures
                         (defaults to `RetryPolicy()`).
    :param validate_public_key: When True (default), check the public key is
                                ECDSA P-384 before exchanging.
    :param name: Optional human-readable label for the key. When omitted (or
                 blank) the identity-service defaults the name to the key id.
    :raises ExchangePatError: on invalid input, a 4xx client error (including a
                              401 — the PAT itself is the credential, so there is
                              nothing to refresh), or once the retry budget for
                              transient failures is exhausted.
    """
    route = _require_kind(kind)
    if validate_public_key:
        _validate_public_key_pem(credentials.public_key_pem)

    dto = ExchangePatDto(
        key_id=credentials.key_id,
        public_key_pem=credentials.public_key_pem,
        name=name,
    )
    policy = retry_policy or RetryPolicy()
    url = identity_service_url.rstrip("/") + route
    body = dto.to_json().encode("utf-8")
    # No on_unauthorized hook: a 401 means the PAT is bad, not stale, so it is
    # terminal rather than a trigger for a refresh-and-retry.
    response = _send_with_retry(
        lambda: _parse_exchange_response(_send_once("POST", url, pat, body=body)),
        policy,
        ExchangePatError,
        label="PAT exchange",
    )
    logger.info(
        "Exchanged PAT for identity-service credentials "
        "(kind=%s, client_id=%s, key_id=%s, tenant_id=%s)",
        kind,
        response.client_id,
        response.key_id,
        response.tenant_id,
    )
    # The server overrides the client id (and echoes the key id); rebind the
    # caller's keypair to the authoritative values before returning.
    rebound = credentials.model_copy(
        update={"client_id": response.client_id, "key_id": response.key_id}
    )
    return ExchangePatResult._from_response(response, credentials=rebound)


def generate_keypair_and_exchange(
    identity_service_url: str,
    pat: str,
    *,
    kind: PrincipalKind = PrincipalKind.USER,
    key_id: Optional[str] = None,
    retry_policy: Optional[RetryPolicy] = None,
    name: Optional[str] = None,
) -> ExchangePatResult:
    """Generate a P-384 keypair and exchange it for Identity Service credentials in one step.

    Convenience wrapper over `exchange_pat`: generates a fresh ECDSA P-384
    keypair via `generate_client_keypair`, exchanges it, and returns a result
    whose `credentials` are ready to persist via
    `result.write_credentials_json(path)` for use by `IdentityServiceClient`.

    :param identity_service_url: Base URL of the identity-service.
    :param pat: Zitadel Personal Access Token.
    :param kind: Whether the PAT and key are for a human USER (default) or AGENT.
    :param key_id: Key id to register; a random one is generated when omitted.
    :param retry_policy: Bounded retry/backoff for transient failures.
    :param name: Optional human-readable label for the key. When omitted (or
                 blank) the identity-service defaults the name to the key id.
    :raises ExchangePatError: on a 4xx client error or exhausted retry budget.
    """
    credentials = generate_client_keypair(key_id=key_id)
    return exchange_pat(
        identity_service_url,
        pat,
        credentials,
        kind=kind,
        retry_policy=retry_policy,
        # we generated the key, so we don't need to validate it.
        validate_public_key=False,
        name=name,
    )


def _require_kind(kind: PrincipalKind) -> str:
    """Return the route path for `kind`, or raise `ExchangePatError` if unknown."""
    try:
        return _ROUTES[kind]
    except KeyError:
        raise ExchangePatError(
            f"Unknown principal kind {kind!r}; expected one of {sorted(_ROUTES)}"
        ) from None
