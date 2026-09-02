"""Tests for ArtifactEntry."""

import pytest

from agentic_devtools.cli.setup.registry import ArtifactEntry, RegistryError


class TestArtifactEntryToDict:
    """Tests for ArtifactEntry.to_dict."""

    def test_serializes_all_fields_with_sorted_references(self) -> None:
        """to_dict returns all fields with a sorted referenced_by list."""
        entry = ArtifactEntry(
            type="cert_bundle",
            path="/home/user/.agdt/certs/unified.pem",
            content_hash="abc123",
            referenced_by=["ctxB", "ctxA"],
        )
        assert entry.to_dict() == {
            "type": "cert_bundle",
            "path": "/home/user/.agdt/certs/unified.pem",
            "content_hash": "abc123",
            "referenced_by": ["ctxA", "ctxB"],
        }

    def test_defaults_to_empty_reference_list(self) -> None:
        """referenced_by defaults to an empty list."""
        entry = ArtifactEntry(type="npmrc", path="/x", content_hash="h")
        assert entry.to_dict()["referenced_by"] == []


class TestArtifactEntryFromDict:
    """Tests for ArtifactEntry.from_dict."""

    def test_round_trips_from_serialized_form(self) -> None:
        """from_dict reconstructs an equivalent entry from to_dict output."""
        original = ArtifactEntry(type="npmrc", path="/x/npmrc", content_hash="h1", referenced_by=["c1"])
        assert ArtifactEntry.from_dict(original.to_dict()) == original

    def test_rejects_missing_required_keys(self) -> None:
        """Missing required scalar fields raise RegistryError instead of defaulting to empty strings."""
        with pytest.raises(RegistryError, match="'type' must be a string, got NoneType"):
            ArtifactEntry.from_dict({})

    def test_rejects_empty_string_required_field(self) -> None:
        """An explicit empty string in a required field raises RegistryError."""
        with pytest.raises(RegistryError, match="'path' must not be empty"):
            ArtifactEntry.from_dict({"type": "cert_bundle", "content_hash": "h", "path": ""})

    def test_rejects_non_str_reference_items(self) -> None:
        """Non-string referenced_by items raise RegistryError instead of coercing."""
        with pytest.raises(RegistryError, match="'referenced_by item' must be a string"):
            ArtifactEntry.from_dict({"type": "cert_bundle", "path": "/x", "content_hash": "h", "referenced_by": [1, 2]})

    def test_rejects_non_str_scalar_field(self) -> None:
        """A non-string scalar field (e.g. null path) raises RegistryError."""
        with pytest.raises(RegistryError, match="'path' must be a string"):
            ArtifactEntry.from_dict({"type": "cert_bundle", "content_hash": "h", "path": None})

    def test_rejects_non_dict_input(self) -> None:
        """A non-dict raw value raises RegistryError."""
        with pytest.raises(RegistryError, match="Expected artifact entry to be a dict"):
            ArtifactEntry.from_dict(["not", "a", "dict"])  # type: ignore[arg-type]

    def test_rejects_non_list_referenced_by(self) -> None:
        """A non-list referenced_by raises RegistryError."""
        with pytest.raises(RegistryError, match="'referenced_by' must be a list"):
            ArtifactEntry.from_dict({"type": "cert_bundle", "path": "/x", "content_hash": "h", "referenced_by": "ctxA"})
