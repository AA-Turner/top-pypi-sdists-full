from typing import Any

from connector_sdk_types import (
    ActivateAccount,
    CreateAccount,
    FoundAccountData,
    ListAccounts,
    request_fingerprint,
)
from connector_sdk_types.serializers import AnnotatedField
from pydantic import BaseModel


class SimpleModel(BaseModel):
    name: str
    value: int


class ModelWithOptional(BaseModel):
    required: str
    optional: str | None = None


class NestedModel(BaseModel):
    inner: SimpleModel
    label: str


# --- DTOs using AnnotatedField for x-unique testing ---


class AccountRequestWithUniqueField(BaseModel):
    """DTO with x-unique field - only account_id should be hashed."""

    account_id: str = AnnotatedField(description="The account ID", unique=True)
    optional_note: str | None = None


class AccountRequestMultipleUniqueFields(BaseModel):
    """DTO with multiple x-unique fields."""

    account_id: str = AnnotatedField(unique=True)
    tenant_id: str = AnnotatedField(unique=True)
    description: str | None = None


class RequestWithoutUniqueFields(BaseModel):
    """DTO without any x-unique fields - all fields should be hashed."""

    query: str
    limit: int = 10


class TestRequestFingerprint:
    def test_same_input_produces_same_hash(self) -> None:
        """Same input should always produce the same fingerprint."""
        model1 = SimpleModel(name="test", value=42)
        model2 = SimpleModel(name="test", value=42)

        assert request_fingerprint(model1) == request_fingerprint(model2)

    def test_same_input_different_order_produces_same_hash(self) -> None:
        """Same input should always produce the same fingerprint."""
        model1 = SimpleModel(name="test", value=42)
        model2 = SimpleModel(value=42, name="test")

        assert request_fingerprint(model1) == request_fingerprint(model2)

    def test_different_input_produces_different_hash(self) -> None:
        """Different inputs should produce different fingerprints."""
        model1 = SimpleModel(name="test", value=42)
        model2 = SimpleModel(name="test", value=43)

        assert request_fingerprint(model1) != request_fingerprint(model2)

    def test_returns_sha256_hex_digest(self) -> None:
        """Fingerprint should be a 64-character hex string (SHA256)."""
        model = SimpleModel(name="test", value=42)
        fingerprint = request_fingerprint(model)

        assert len(fingerprint) == 64
        assert all(c in "0123456789abcdef" for c in fingerprint)

    def test_dict_input(self) -> None:
        """Function should work with dict input."""
        data: dict[str, Any] = {"name": "test", "value": 42}
        fingerprint = request_fingerprint(data)

        assert len(fingerprint) == 64

    def test_dict_and_model_produce_same_hash(self) -> None:
        """Dict and equivalent model should produce the same fingerprint."""
        model = SimpleModel(name="test", value=42)
        data: dict[str, Any] = {"name": "test", "value": 42}

        assert request_fingerprint(model) == request_fingerprint(data)

    def test_key_order_does_not_matter_for_dict(self) -> None:
        """Key order in dict should not affect fingerprint (canonical JSON sorts keys)."""
        data1: dict[str, Any] = {"name": "test", "value": 42}
        data2: dict[str, Any] = {"value": 42, "name": "test"}

        assert request_fingerprint(data1) == request_fingerprint(data2)

    def test_none_values_excluded(self) -> None:
        """None values should be excluded for consistency."""
        model_with_none = ModelWithOptional(required="test", optional=None)
        model_without_optional = ModelWithOptional(required="test")

        # Both should produce the same hash since optional=None is excluded
        assert request_fingerprint(model_with_none) == request_fingerprint(model_without_optional)

    def test_nested_model(self) -> None:
        """Nested models should be handled correctly."""
        inner = SimpleModel(name="inner", value=1)
        nested1 = NestedModel(inner=inner, label="outer")
        nested2 = NestedModel(inner=SimpleModel(name="inner", value=1), label="outer")

        assert request_fingerprint(nested1) == request_fingerprint(nested2)

    def test_empty_dict(self) -> None:
        """Empty dict should produce a valid fingerprint."""
        fingerprint = request_fingerprint({})

        assert len(fingerprint) == 64

    def test_special_characters(self) -> None:
        """
        Non-ASCII characters are safely handled because json.dumps(ensure_ascii=True)
        escapes them to \\uXXXX sequences before UTF-8 encoding.
        """
        test_names = [
            "José García",  # Spanish accents
            "François Müller",  # French/German
            "北京用户",  # Chinese
            "Александр",  # Cyrillic
            "🎉👨‍💻",  # Emojis with ZWJ
        ]

        for name in test_names:
            model = SimpleModel(name=name, value=1)
            # Should not raise and should be deterministic
            assert request_fingerprint(model) == request_fingerprint(model)

    def test_deterministic_across_calls(self) -> None:
        """Multiple calls should produce the same result."""
        model = SimpleModel(name="test", value=42)

        fingerprints = [request_fingerprint(model) for _ in range(10)]

        assert len(set(fingerprints)) == 1  # All should be identical

    def test_different_optional_values_produce_different_hash(self) -> None:
        """Different optional field values should produce different fingerprints."""
        model1 = ModelWithOptional(required="test", optional="foo")
        model2 = ModelWithOptional(required="test", optional="bar")

        # All fields are hashed, so different optional values = different hash
        assert request_fingerprint(model1) != request_fingerprint(model2)


class TestRequestFingerprintWithGeneratedTypes:
    """Test fingerprint with actual generated SDK types."""

    def test_list_accounts_request(self) -> None:
        """Test with ListAccounts model from generated types."""

        req1 = ListAccounts(custom_attributes=["email", "department"])
        req2 = ListAccounts(custom_attributes=["email", "department"])

        assert request_fingerprint(req1) == request_fingerprint(req2)

    def test_list_accounts_different_attrs(self) -> None:
        """Different custom_attributes should produce different fingerprints."""

        req1 = ListAccounts(custom_attributes=["email"])
        req2 = ListAccounts(custom_attributes=["department"])

        assert request_fingerprint(req1) != request_fingerprint(req2)

    def test_found_account_data(self) -> None:
        """Test with FoundAccountData model."""

        account1 = FoundAccountData(
            integration_specific_id="user-123",
            email="user@example.com",
        )
        account2 = FoundAccountData(
            integration_specific_id="user-123",
            email="user@example.com",
        )

        assert request_fingerprint(account1) == request_fingerprint(account2)


class TestCapabilityModelFingerprintMethod:
    """Test the fingerprint() method on capability request models."""

    def test_list_accounts_has_fingerprint_method(self) -> None:
        """ListAccounts (capability model) should have a fingerprint() method."""

        req = ListAccounts(custom_attributes=["email"])
        assert hasattr(req, "fingerprint")
        assert callable(req.fingerprint)

    def test_fingerprint_method_returns_hash(self) -> None:
        """fingerprint() method should return SHA256 hex digest."""

        req = ListAccounts(custom_attributes=["email"])
        fingerprint = req.fingerprint()

        assert len(fingerprint) == 64
        assert all(c in "0123456789abcdef" for c in fingerprint)

    def test_fingerprint_method_matches_utility_function(self) -> None:
        """fingerprint() method should produce same result as utility function."""

        req = ListAccounts(custom_attributes=["email"])

        # Method and utility should produce same result
        assert req.fingerprint() == request_fingerprint(req)

    def test_create_account_has_fingerprint_method(self) -> None:
        """CreateAccount (capability model) should have a fingerprint() method."""

        req = CreateAccount(entitlements=[])
        assert hasattr(req, "fingerprint")
        assert callable(req.fingerprint)

    def test_activate_account_has_fingerprint_method(self) -> None:
        """ActivateAccount (capability model) should have a fingerprint() method."""

        req = ActivateAccount(account_id="test-123")
        assert hasattr(req, "fingerprint")
        assert callable(req.fingerprint)


class TestUniqueFieldFingerprint:
    """
    Integration tests showing the full flow:
    AnnotatedField(unique=True) → DTO → json_schema_extra → fingerprint behavior
    """

    def test_unique_field_determines_fingerprint(self) -> None:
        """When x-unique fields exist, only those determine the fingerprint."""
        req1 = AccountRequestWithUniqueField(account_id="user-123", optional_note="first request")
        req2 = AccountRequestWithUniqueField(account_id="user-123", optional_note="different note")

        # Same account_id = same fingerprint (optional_note is ignored)
        assert request_fingerprint(req1) == request_fingerprint(req2)

    def test_different_unique_field_different_fingerprint(self) -> None:
        """Different x-unique field values produce different fingerprints."""
        req1 = AccountRequestWithUniqueField(account_id="user-123")
        req2 = AccountRequestWithUniqueField(account_id="user-456")

        assert request_fingerprint(req1) != request_fingerprint(req2)

    def test_multiple_unique_fields_all_included(self) -> None:
        """When multiple fields have x-unique, all are included in fingerprint."""
        req1 = AccountRequestMultipleUniqueFields(
            account_id="user-123", tenant_id="tenant-A", description="desc1"
        )
        req2 = AccountRequestMultipleUniqueFields(
            account_id="user-123", tenant_id="tenant-A", description="desc2"
        )

        # Same unique fields = same fingerprint (description is ignored)
        assert request_fingerprint(req1) == request_fingerprint(req2)

    def test_multiple_unique_fields_any_difference_changes_fingerprint(self) -> None:
        """If any x-unique field differs, fingerprint changes."""
        req1 = AccountRequestMultipleUniqueFields(
            account_id="user-123", tenant_id="tenant-A", description="same"
        )
        req2 = AccountRequestMultipleUniqueFields(
            account_id="user-123", tenant_id="tenant-B", description="same"
        )

        # Different tenant_id = different fingerprint
        assert request_fingerprint(req1) != request_fingerprint(req2)

    def test_no_unique_fields_hashes_everything(self) -> None:
        """Without x-unique fields, all fields are included in fingerprint."""
        req1 = RequestWithoutUniqueFields(query="test", limit=10)
        req2 = RequestWithoutUniqueFields(query="test", limit=20)

        # Different limit = different fingerprint (all fields matter)
        assert request_fingerprint(req1) != request_fingerprint(req2)

    def test_no_unique_fields_same_values_same_hash(self) -> None:
        """Without x-unique fields, same values = same fingerprint."""
        req1 = RequestWithoutUniqueFields(query="test", limit=10)
        req2 = RequestWithoutUniqueFields(query="test", limit=10)

        assert request_fingerprint(req1) == request_fingerprint(req2)
