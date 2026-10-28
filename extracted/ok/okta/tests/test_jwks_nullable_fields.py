"""
Tests for JWKS models with nullable discriminator fields.

This test suite verifies that JWKS models correctly handle nullable fields
including the 'use' discriminator field that can be null in actual Okta API responses.
"""

import pytest
from okta.models.get_jwk200_response import GetJwk200Response
from okta.models.list_jwk200_response_inner import ListJwk200ResponseInner
from okta.models.o_auth2_client_json_signing_key_response import (
    OAuth2ClientJsonSigningKeyResponse,
)
from okta.models.o_auth2_client_json_web_key_rsa_response import (
    OAuth2ClientJsonWebKeyRsaResponse,
)
from okta.models.o_auth2_client_json_web_key_ec_response import (
    OAuth2ClientJsonWebKeyECResponse,
)
from okta.models.o_auth2_client_json_encryption_key_response import (
    OAuth2ClientJsonEncryptionKeyResponse,
)


class TestJWKSWithNullUseField:
    """Test JWKS deserialization with null 'use' field"""

    def test_get_jwk_response_with_null_use(self):
        """Test GetJwk200Response deserializes correctly when 'use' is null"""
        jwks_data = {
            "id": "pks123456",
            "kid": None,
            "use": None,
            "kty": "RSA",
            "alg": "RS256",
            "status": "ACTIVE",
        }

        response = GetJwk200Response.from_dict(jwks_data)

        assert response.actual_instance is not None
        assert isinstance(
            response.actual_instance,
            (OAuth2ClientJsonSigningKeyResponse, OAuth2ClientJsonEncryptionKeyResponse)
        )

    def test_list_jwk_response_inner_with_null_use(self):
        """Test ListJwk200ResponseInner deserializes correctly when 'use' is null"""
        jwks_data = {
            "id": "pks789012",
            "kid": None,
            "use": None,
            "kty": "RSA",
            "alg": "RS256",
            "status": "ACTIVE",
        }

        response = ListJwk200ResponseInner.from_dict(jwks_data)

        assert response.actual_instance is not None
        assert isinstance(
            response.actual_instance,
            (OAuth2ClientJsonSigningKeyResponse, OAuth2ClientJsonEncryptionKeyResponse)
        )

    def test_signing_key_response_with_null_use(self):
        """Test OAuth2ClientJsonSigningKeyResponse handles null 'use' field"""
        jwks_data = {
            "id": "pks345678",
            "kid": "key-123",
            "use": None,
            "kty": "RSA",
            "alg": "RS256",
            "status": "ACTIVE",
        }

        response = OAuth2ClientJsonSigningKeyResponse.from_dict(jwks_data)

        assert response is not None
        assert response.id == "pks345678"
        assert response.use is None

    def test_rsa_response_with_null_use(self):
        """Test OAuth2ClientJsonWebKeyRsaResponse handles null 'use' field"""
        jwks_data = {
            "id": "pks901234",
            "kid": None,
            "use": None,
            "kty": "RSA",
            "alg": "RS256",
            "status": "ACTIVE",
            "e": "AQAB",
            "n": "xGOr-H7A...",
        }

        response = OAuth2ClientJsonWebKeyRsaResponse.from_dict(jwks_data)

        assert response is not None
        assert response.id == "pks901234"
        assert response.use is None
        assert response.kty == "RSA"


class TestJWKSWithNullKidField:
    """Test JWKS deserialization with null 'kid' field"""

    def test_get_jwk_response_with_null_kid(self):
        """Test GetJwk200Response deserializes correctly when 'kid' is null"""
        jwks_data = {
            "id": "pks111222",
            "kid": None,
            "use": "sig",
            "kty": "RSA",
            "alg": "RS256",
            "status": "ACTIVE",
        }

        response = GetJwk200Response.from_dict(jwks_data)

        assert response.actual_instance is not None
        assert isinstance(response.actual_instance, OAuth2ClientJsonSigningKeyResponse)

    def test_signing_key_with_null_kid_and_null_use(self):
        """Test JWKS with both kid and use as null"""
        jwks_data = {
            "id": "pks333444",
            "kid": None,
            "use": None,
            "kty": "RSA",
            "alg": "RS256",
            "status": "ACTIVE",
        }

        response = OAuth2ClientJsonSigningKeyResponse.from_dict(jwks_data)

        assert response is not None
        assert response.kid is None
        assert response.use is None


class TestJWKSWithNullKtyField:
    """Test JWKS deserialization with null 'kty' discriminator field"""

    def test_signing_key_with_null_kty(self):
        """Test OAuth2ClientJsonSigningKeyResponse handles null 'kty' field"""
        jwks_data = {
            "id": "pks555666",
            "kid": "key-456",
            "use": "sig",
            "kty": None,
            "alg": "RS256",
            "status": "ACTIVE",
        }

        # Should not raise an error, should return base class instance
        response = OAuth2ClientJsonSigningKeyResponse.from_dict(jwks_data)

        assert response is not None
        assert response.id == "pks555666"
        assert response.kty is None


class TestJWKSDiscriminatorRouting:
    """Test discriminator-based routing for oneOf schemas"""

    def test_use_sig_routes_to_signing_key(self):
        """Test that 'use: sig' routes to OAuth2ClientJsonSigningKeyResponse"""
        jwks_data = {
            "id": "pks777888",
            "kid": "key-sig",
            "use": "sig",
            "kty": "RSA",
            "alg": "RS256",
            "status": "ACTIVE",
        }

        response = GetJwk200Response.from_dict(jwks_data)

        assert response.actual_instance is not None
        assert isinstance(response.actual_instance, OAuth2ClientJsonSigningKeyResponse)

    def test_use_enc_routes_to_encryption_key(self):
        """Test that 'use: enc' routes to OAuth2ClientJsonEncryptionKeyResponse"""
        jwks_data = {
            "id": "pks999000",
            "kid": "key-enc",
            "use": "enc",
            "kty": "RSA",
            "alg": "RSA-OAEP",
            "status": "ACTIVE",
        }

        response = GetJwk200Response.from_dict(jwks_data)

        assert response.actual_instance is not None
        assert isinstance(response.actual_instance, OAuth2ClientJsonEncryptionKeyResponse)

    def test_kty_rsa_routes_correctly(self):
        """Test that 'kty: RSA' is handled correctly"""
        jwks_data = {
            "id": "pks111000",
            "kid": "key-rsa",
            "use": "sig",
            "kty": "RSA",
            "alg": "RS256",
            "status": "ACTIVE",
        }

        response = OAuth2ClientJsonSigningKeyResponse.from_dict(jwks_data)

        assert response is not None
        assert response.kty == "RSA"


class TestJWKSRoundTripSerialization:
    """Test round-trip serialization of JWKS with nullable fields"""

    def test_round_trip_with_null_use(self):
        """Test that null 'use' field is preserved through serialization"""
        original_data = {
            "id": "pks333000",
            "kid": None,
            "use": None,
            "kty": "RSA",
            "alg": "RS256",
            "status": "ACTIVE",
        }

        # Deserialize
        response = OAuth2ClientJsonSigningKeyResponse.from_dict(original_data)

        # Serialize back
        serialized = response.to_dict()

        # Verify nullable fields are preserved
        assert serialized.get("use") is None
        assert serialized.get("kid") is None

    def test_round_trip_with_null_kty(self):
        """Test that null 'kty' field is preserved through serialization"""
        original_data = {
            "id": "pks444000",
            "kid": "key-789",
            "use": "sig",
            "kty": None,
            "alg": "RS256",
            "status": "ACTIVE",
        }

        # Deserialize
        response = OAuth2ClientJsonSigningKeyResponse.from_dict(original_data)

        # Serialize back
        serialized = response.to_dict()

        # Verify kty is None
        assert serialized.get("kty") is None

    def test_round_trip_preserves_non_null_values(self):
        """Test that non-null values are correctly preserved"""
        original_data = {
            "id": "pks555000",
            "kid": "key-active",
            "use": "sig",
            "kty": "RSA",
            "alg": "RS256",
            "status": "ACTIVE",
        }

        # Deserialize
        response = OAuth2ClientJsonSigningKeyResponse.from_dict(original_data)

        # Serialize back
        serialized = response.to_dict()

        # Verify all non-null values are preserved
        assert serialized["kid"] == "key-active"
        assert serialized["use"] == "sig"
        assert serialized["kty"] == "RSA"
        assert serialized["alg"] == "RS256"
        assert serialized["status"] == "ACTIVE"


class TestJWKSReadOnlyFieldsExclusion:
    """Test that read-only fields behavior in serialization"""

    def test_rsa_response_serialization(self):
        """Test that RSA response to_dict() works correctly"""
        jwks_data = {
            "id": "pks666000",
            "created": "2023-01-01T00:00:00.000Z",
            "lastUpdated": "2023-01-02T00:00:00.000Z",
            "kid": "key-123",
            "use": "sig",
            "kty": "RSA",
            "alg": "RS256",
            "status": "ACTIVE",
            "e": "AQAB",
            "n": "xGOr...",
        }

        response = OAuth2ClientJsonWebKeyRsaResponse.from_dict(jwks_data)
        serialized = response.to_dict()

        # Key fields should be present
        assert "kid" in serialized
        assert "use" in serialized
        assert "e" in serialized
        assert "n" in serialized

    def test_ec_response_serialization(self):
        """Test that EC response to_dict() works correctly"""
        jwks_data = {
            "id": "pks777000",
            "created": "2023-01-01T00:00:00.000Z",
            "lastUpdated": "2023-01-02T00:00:00.000Z",
            "kid": "key-456",
            "use": "sig",
            "kty": "EC",
            "alg": "ES256",
            "status": "ACTIVE",
            "x": "WKn-ZIGevcwGIyyrzFoZNBdaq9_TsqzGl96oc0CWuis",
            "y": "y77t-RvAHRKTsSGdIYUfweuOvwrvDD-Q3Hv5J0fSKbE",
            "crv": "P-256",
        }

        response = OAuth2ClientJsonWebKeyECResponse.from_dict(jwks_data)
        serialized = response.to_dict()

        # Key fields should be present
        assert "kid" in serialized
        assert "x" in serialized
        assert "y" in serialized
        assert "crv" in serialized


class TestJWKSValidation:
    """Test validation of JWKS models"""

    def test_invalid_status_enum_raises_error(self):
        """Test that invalid status value raises ValidationError"""
        jwks_data = {
            "id": "pks888000",
            "kid": "key-789",
            "use": "sig",
            "kty": "RSA",
            "alg": "RS256",
            "status": "INVALID_STATUS",
        }

        with pytest.raises(Exception):  # Pydantic ValidationError
            OAuth2ClientJsonSigningKeyResponse.from_dict(jwks_data)

    def test_invalid_kty_enum_raises_error(self):
        """Test that invalid kty value raises ValidationError"""
        jwks_data = {
            "id": "pks999000",
            "kid": "key-012",
            "use": "sig",
            "kty": "INVALID_KTY",
            "alg": "RS256",
            "status": "ACTIVE",
        }

        with pytest.raises(Exception):  # Pydantic ValidationError
            OAuth2ClientJsonSigningKeyResponse.from_dict(jwks_data)

    def test_invalid_use_enum_raises_error(self):
        """Test that invalid use value raises ValidationError"""
        jwks_data = {
            "id": "pks000111",
            "kid": "key-345",
            "use": "INVALID_USE",
            "kty": "RSA",
            "alg": "RS256",
            "status": "ACTIVE",
        }

        with pytest.raises(Exception):  # Pydantic ValidationError
            OAuth2ClientJsonSigningKeyResponse.from_dict(jwks_data)






