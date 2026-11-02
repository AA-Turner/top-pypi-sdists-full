"""Tests for RegistryData."""

import pytest

from agentic_devtools.cli.setup.registry import (
    SCHEMA_VERSION,
    ArtifactEntry,
    ContextEntry,
    RegistryData,
    RegistryError,
)


class TestRegistryDataToDict:
    """Tests for RegistryData.to_dict."""

    def test_serializes_nested_entries_with_sorted_keys(self) -> None:
        """to_dict serializes nested contexts/artifacts under sorted keys."""
        data = RegistryData(
            contexts={
                "ctxB": ContextEntry(path="/b", last_setup_utc="t", artifacts=["h1"]),
                "ctxA": ContextEntry(path="/a", last_setup_utc="t", artifacts=["h1"]),
            },
            artifacts={"h1": ArtifactEntry(type="npmrc", path="/n", content_hash="h1", referenced_by=["ctxA"])},
        )
        result = data.to_dict()
        assert result["schema_version"] == SCHEMA_VERSION
        assert list(result["contexts"].keys()) == ["ctxA", "ctxB"]
        assert result["artifacts"]["h1"]["content_hash"] == "h1"

    def test_empty_registry_serializes_to_empty_maps(self) -> None:
        """An empty registry serializes to empty context/artifact maps."""
        assert RegistryData().to_dict() == {
            "schema_version": SCHEMA_VERSION,
            "contexts": {},
            "artifacts": {},
        }


class TestRegistryDataFromDict:
    """Tests for RegistryData.from_dict."""

    def test_round_trips_from_serialized_form(self) -> None:
        """from_dict reconstructs an equivalent registry from to_dict output."""
        original = RegistryData(
            schema_version=1,
            contexts={"ctxA": ContextEntry(path="/a", last_setup_utc="t", artifacts=["h1"])},
            artifacts={"h1": ArtifactEntry(type="npmrc", path="/n", content_hash="h1", referenced_by=["ctxA"])},
        )
        assert RegistryData.from_dict(original.to_dict()) == original

    def test_applies_defaults_for_missing_keys(self) -> None:
        """Missing keys fall back to the default schema version and empty maps."""
        data = RegistryData.from_dict({})
        assert data == RegistryData(schema_version=SCHEMA_VERSION, contexts={}, artifacts={})

    def test_coerces_context_keys_to_str(self) -> None:
        """Context/artifact map keys are coerced to strings."""
        data = RegistryData.from_dict({"contexts": {}, "artifacts": {}})
        assert data.contexts == {}

    def test_rejects_non_dict_root(self) -> None:
        """A non-dict root raises RegistryError."""
        with pytest.raises(RegistryError, match="Expected registry root to be a dict"):
            RegistryData.from_dict([1, 2, 3])  # type: ignore[arg-type]

    def test_rejects_non_dict_contexts(self) -> None:
        """A non-dict contexts value raises RegistryError."""
        with pytest.raises(RegistryError, match="'contexts' must be a dict"):
            RegistryData.from_dict({"contexts": []})

    def test_rejects_non_dict_artifacts(self) -> None:
        """A non-dict artifacts value raises RegistryError."""
        with pytest.raises(RegistryError, match="'artifacts' must be a dict"):
            RegistryData.from_dict({"artifacts": []})

    def test_rejects_non_int_schema_version(self) -> None:
        """A non-int schema_version raises RegistryError."""
        with pytest.raises(RegistryError, match="'schema_version' must be an integer"):
            RegistryData.from_dict({"schema_version": "1"})

    def test_rejects_bool_schema_version(self) -> None:
        """A bool schema_version raises RegistryError (bool is not accepted as int)."""
        with pytest.raises(RegistryError, match="'schema_version' must be an integer"):
            RegistryData.from_dict({"schema_version": True})

    def test_rejects_unsupported_schema_version(self) -> None:
        """A future/unsupported schema_version raises RegistryError."""
        with pytest.raises(RegistryError, match="Unsupported registry schema_version"):
            RegistryData.from_dict({"schema_version": SCHEMA_VERSION + 1})

    def test_rejects_zero_schema_version(self) -> None:
        """A schema_version below 1 raises RegistryError."""
        with pytest.raises(RegistryError, match="Unsupported registry schema_version"):
            RegistryData.from_dict({"schema_version": 0})
