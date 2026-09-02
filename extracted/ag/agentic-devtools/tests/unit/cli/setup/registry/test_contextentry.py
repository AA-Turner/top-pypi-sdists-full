"""Tests for ContextEntry."""

import pytest

from agentic_devtools.cli.setup.registry import ContextEntry, RegistryError


class TestContextEntryToDict:
    """Tests for ContextEntry.to_dict."""

    def test_serializes_all_fields_with_sorted_artifacts(self) -> None:
        """to_dict returns all fields with a sorted artifacts list."""
        entry = ContextEntry(
            path="/home/user/repo",
            last_setup_utc="2024-01-01T00:00:00Z",
            artifacts=["hashB", "hashA"],
        )
        assert entry.to_dict() == {
            "path": "/home/user/repo",
            "last_setup_utc": "2024-01-01T00:00:00Z",
            "artifacts": ["hashA", "hashB"],
        }

    def test_defaults_to_empty_artifact_list(self) -> None:
        """artifacts defaults to an empty list."""
        entry = ContextEntry(path="/x", last_setup_utc="t")
        assert entry.to_dict()["artifacts"] == []


class TestContextEntryFromDict:
    """Tests for ContextEntry.from_dict."""

    def test_round_trips_from_serialized_form(self) -> None:
        """from_dict reconstructs an equivalent entry from to_dict output."""
        original = ContextEntry(path="/x/repo", last_setup_utc="t1", artifacts=["h1"])
        assert ContextEntry.from_dict(original.to_dict()) == original

    def test_rejects_missing_required_keys(self) -> None:
        """Missing required scalar fields raise RegistryError instead of defaulting to empty strings."""
        with pytest.raises(RegistryError, match="'path' must be a string, got NoneType"):
            ContextEntry.from_dict({})

    def test_rejects_empty_string_required_field(self) -> None:
        """An explicit empty string in a required field raises RegistryError."""
        with pytest.raises(RegistryError, match="'last_setup_utc' must not be empty"):
            ContextEntry.from_dict({"path": "/repo", "last_setup_utc": ""})

    def test_rejects_non_str_artifact_items(self) -> None:
        """Non-string artifacts items raise RegistryError instead of coercing."""
        with pytest.raises(RegistryError, match="'artifacts item' must be a string"):
            ContextEntry.from_dict({"path": "/repo", "last_setup_utc": "t", "artifacts": [1, 2]})

    def test_rejects_non_str_scalar_field(self) -> None:
        """A non-string scalar field (e.g. null last_setup_utc) raises RegistryError."""
        with pytest.raises(RegistryError, match="'last_setup_utc' must be a string"):
            ContextEntry.from_dict({"path": "/repo", "last_setup_utc": None})

    def test_rejects_non_dict_input(self) -> None:
        """A non-dict raw value raises RegistryError."""
        with pytest.raises(RegistryError, match="Expected context entry to be a dict"):
            ContextEntry.from_dict("nope")  # type: ignore[arg-type]

    def test_rejects_non_list_artifacts(self) -> None:
        """A non-list artifacts value raises RegistryError."""
        with pytest.raises(RegistryError, match="'artifacts' must be a list"):
            ContextEntry.from_dict({"path": "/repo", "last_setup_utc": "t", "artifacts": "hashA"})
