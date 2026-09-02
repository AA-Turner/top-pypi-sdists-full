"""Tests for register_artifact."""

from agentic_devtools.cli.setup.registry import RegistryData, register_artifact


class TestRegisterArtifact:
    """Tests for register_artifact."""

    def test_creates_new_entry_referenced_by_context(self) -> None:
        """A previously unseen content hash creates a new artifact entry."""
        data = RegistryData()
        entry = register_artifact(data, "ctxA", "cert_bundle", "/certs/a.pem", "hashA")
        assert data.artifacts == {"hashA": entry}
        assert entry.referenced_by == ["ctxA"]
        assert entry.type == "cert_bundle"
        assert entry.path == "/certs/a.pem"

    def test_appends_new_context_to_existing_artifact(self) -> None:
        """An existing content hash gains the new context in referenced_by."""
        data = RegistryData()
        register_artifact(data, "ctxA", "npmrc", "/n", "shared")
        entry = register_artifact(data, "ctxB", "npmrc", "/n", "shared")
        assert len(data.artifacts) == 1
        assert sorted(entry.referenced_by) == ["ctxA", "ctxB"]

    def test_does_not_duplicate_existing_context_reference(self) -> None:
        """Re-registering the same content for the same context is idempotent."""
        data = RegistryData()
        register_artifact(data, "ctxA", "npmrc", "/n", "shared")
        entry = register_artifact(data, "ctxA", "npmrc", "/n", "shared")
        assert entry.referenced_by == ["ctxA"]

    def test_preserves_original_path_for_deduplicated_content(self) -> None:
        """Content-addressed dedup keeps the first-registered path/type."""
        data = RegistryData()
        register_artifact(data, "ctxA", "cert_bundle", "/first.pem", "shared")
        entry = register_artifact(data, "ctxB", "cert_bundle", "/second.pem", "shared")
        assert entry.path == "/first.pem"
