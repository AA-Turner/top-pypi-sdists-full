"""Tests for ``get_credential``."""

from types import SimpleNamespace
from typing import Any, cast

import pytest
from connector.oai.capability import Request, get_credential
from connector.oai.errors import InternalError, InvalidConfigurationError, MissingParameterError
from connector_sdk_types.generated import (
    AuthCredential,
    BasicCredential,
    JWTCredential,
    KeyPairCredential,
    OAuth1Credential,
    OAuthClientCredential,
    OAuthCredential,
    ServiceAccountCredential,
    TokenCredential,
    ValidateCredentialConfig,
    ValidateCredentialConfigRequest,
)
from connector_sdk_types.generated.models.jwt_claims import JWTClaims
from connector_sdk_types.generated.models.jwt_headers import JWTHeaders
from connector_sdk_types.generated.models.service_account_type import ServiceAccountType

CREDENTIAL_ID = "my_credential"

OAUTH_CREDENTIAL = AuthCredential(
    id=CREDENTIAL_ID,
    oauth=OAuthCredential(access_token="access-tok"),
)

OAUTH_CLIENT_CREDENTIAL = AuthCredential(
    id=CREDENTIAL_ID,
    oauth_client_credentials=OAuthClientCredential(
        access_token="access-tok",
        client_id="cid",
        client_secret="csecret",
        scopes=["read"],
    ),
)

OAUTH1_CREDENTIAL = AuthCredential(
    id=CREDENTIAL_ID,
    oauth1=OAuth1Credential(
        consumer_key="consumer-key",
        consumer_secret="consumer-secret",
        token_id="token-id",
        token_secret="token-secret",
    ),
)

BASIC_CREDENTIAL = AuthCredential(
    id=CREDENTIAL_ID,
    basic=BasicCredential(username="user", password="pass"),
)

TOKEN_CREDENTIAL = AuthCredential(
    id=CREDENTIAL_ID,
    token=TokenCredential(token="test-token"),
)

JWT_CREDENTIAL = AuthCredential(
    id=CREDENTIAL_ID,
    jwt=JWTCredential(
        headers=JWTHeaders(
            alg="RS256",
            jku="",
            jwk="",
            typ="JWT",
            kid="k1",
            x5u="",
            x5c="",
            x5t="",
            **{"x5t#S256": ""},
            cty="",
            crit=[],
        ),
        claims=JWTClaims(
            iss="issuer",
            sub="subject",
            aud="audience",
            exp=9999999999,
            nbf=0,
            iat=0,
            jti="jti",
            act="",
            scope=[],
            client_id="cid",
            may_act="",
        ),
        secret="secret",
    ),
)

SERVICE_ACCOUNT_CREDENTIAL = AuthCredential(
    id=CREDENTIAL_ID,
    service_account=ServiceAccountCredential(
        service_type=ServiceAccountType.AWS,
        key={"access_key_id": "key", "secret_access_key": "secret"},
        impersonation_email="sa@example.com",
        tenant_id="tenant",
        scopes=["admin"],
    ),
)

KEY_PAIR_CREDENTIAL = AuthCredential(
    id=CREDENTIAL_ID,
    key_pair=KeyPairCredential(
        key_identifier="kid-1",
        private_key="-----BEGIN MOCK RSA PRIVATE KEY-----",
    ),
)

ALL_CREDENTIAL_TYPES = [
    (OAUTH_CREDENTIAL, OAuthCredential),
    (OAUTH_CLIENT_CREDENTIAL, OAuthClientCredential),
    (OAUTH1_CREDENTIAL, OAuth1Credential),
    (BASIC_CREDENTIAL, BasicCredential),
    (TOKEN_CREDENTIAL, TokenCredential),
    (JWT_CREDENTIAL, JWTCredential),
    (SERVICE_ACCOUNT_CREDENTIAL, ServiceAccountCredential),
    (KEY_PAIR_CREDENTIAL, KeyPairCredential),
]


def _make_request(credentials: Any = None) -> Request:
    return cast(
        Request,
        SimpleNamespace(
            auth=None,
            credentials=credentials,
            request=None,
            page=None,
            include_raw_data=None,
            settings={},
        ),
    )


def _make_validate_config_request(credential: AuthCredential) -> ValidateCredentialConfigRequest:
    return ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(credential=credential),
    )


@pytest.mark.parametrize(
    ("auth_credential", "credential_type"),
    ALL_CREDENTIAL_TYPES,
    ids=[t.__name__ for _, t in ALL_CREDENTIAL_TYPES],
)
def test_returns_credential(auth_credential, credential_type) -> None:
    request = _make_request(credentials=[auth_credential])
    result = get_credential(request, CREDENTIAL_ID, credential_type)
    assert isinstance(result, credential_type)


def test_raises_when_credentials_none() -> None:
    request = _make_request(credentials=None)
    with pytest.raises(InvalidConfigurationError):
        get_credential(request, CREDENTIAL_ID, TokenCredential)


def test_returns_none_when_credentials_none() -> None:
    request = _make_request(credentials=None)
    assert get_credential(request, CREDENTIAL_ID, TokenCredential, strict=False) is None


def test_raises_when_credentials_empty() -> None:
    request = _make_request(credentials=[])
    with pytest.raises(InvalidConfigurationError):
        get_credential(request, CREDENTIAL_ID, TokenCredential)


def test_returns_none_when_credentials_empty() -> None:
    request = _make_request(credentials=[])
    assert get_credential(request, CREDENTIAL_ID, TokenCredential, strict=False) is None


def test_raises_when_id_not_found() -> None:
    other = AuthCredential(id="other", token=TokenCredential(token="t"))
    request = _make_request(credentials=[other])
    with pytest.raises(MissingParameterError):
        get_credential(request, CREDENTIAL_ID, TokenCredential)


def test_returns_none_when_id_not_found() -> None:
    other = AuthCredential(id="other", token=TokenCredential(token="t"))
    request = _make_request(credentials=[other])
    assert get_credential(request, CREDENTIAL_ID, TokenCredential, strict=False) is None


def test_raises_when_wrong_type() -> None:
    request = _make_request(credentials=[TOKEN_CREDENTIAL])
    with pytest.raises(InvalidConfigurationError):
        get_credential(request, CREDENTIAL_ID, BasicCredential)


def test_returns_none_when_wrong_type() -> None:
    request = _make_request(credentials=[TOKEN_CREDENTIAL])
    assert get_credential(request, CREDENTIAL_ID, BasicCredential, strict=False) is None


@pytest.mark.parametrize(
    ("auth_credential", "credential_type"),
    ALL_CREDENTIAL_TYPES,
    ids=[f"validate_config_{t.__name__}" for _, t in ALL_CREDENTIAL_TYPES],
)
def test_validate_config_returns_credential(auth_credential, credential_type) -> None:
    request = _make_validate_config_request(auth_credential)
    result = get_credential(request, CREDENTIAL_ID, credential_type)
    assert isinstance(result, credential_type)


def test_validate_config_raises_internal_error_when_credential_id_missing() -> None:
    request = _make_validate_config_request(
        AuthCredential(id=None, token=TokenCredential(token="token"))
    )
    with pytest.raises(InternalError, match="without ID"):
        get_credential(request, CREDENTIAL_ID, TokenCredential)


def test_validate_config_non_strict_raises_internal_error_when_credential_id_missing() -> None:
    request = _make_validate_config_request(
        AuthCredential(id=None, token=TokenCredential(token="token"))
    )
    with pytest.raises(InternalError, match="without ID"):
        get_credential(request, CREDENTIAL_ID, TokenCredential, strict=False)


def test_validate_config_raises_internal_error_when_credential_id_mismatch() -> None:
    request = _make_validate_config_request(
        AuthCredential(id="unexpected_id", token=TokenCredential(token="token"))
    )
    with pytest.raises(InternalError, match="expected 'my_credential'"):
        get_credential(request, CREDENTIAL_ID, TokenCredential)


def test_validate_config_non_strict_raises_internal_error_when_credential_id_mismatch() -> None:
    request = _make_validate_config_request(
        AuthCredential(id="unexpected_id", token=TokenCredential(token="token"))
    )
    with pytest.raises(InternalError, match="expected 'my_credential'"):
        get_credential(request, CREDENTIAL_ID, TokenCredential, strict=False)


def test_validate_config_raises_internal_error_when_typed_payload_missing() -> None:
    request = _make_validate_config_request(AuthCredential(id=CREDENTIAL_ID))
    with pytest.raises(InternalError, match="expected payload type 'TokenCredential'"):
        get_credential(request, CREDENTIAL_ID, TokenCredential)


def test_validate_config_raises_internal_error_when_typed_payload_wrong() -> None:
    request = _make_validate_config_request(
        AuthCredential(id=CREDENTIAL_ID, basic=BasicCredential(username="u", password="p"))
    )
    with pytest.raises(InternalError, match="expected payload type 'TokenCredential'"):
        get_credential(request, CREDENTIAL_ID, TokenCredential)


def test_validate_config_returns_none_when_wrong_type_non_strict() -> None:
    request = _make_validate_config_request(
        AuthCredential(id=CREDENTIAL_ID, basic=BasicCredential(username="u", password="p"))
    )
    assert get_credential(request, CREDENTIAL_ID, TokenCredential, strict=False) is None
