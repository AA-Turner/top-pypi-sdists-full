"""Tests for get_context_artifacts."""

from agentic_devtools.cli.setup.registry import (
    ArtifactEntry,
    ContextEntry,
    RegistryData,
    get_context_artifacts,
)


class TestGetContextArtifacts:
    """Tests for get_context_artifacts."""

    def test_returns_referenced_artifacts_sorted_by_hash(self) -> None:
        """Returns the artifacts a context references, sorted by content hash."""
        data = RegistryData(
            contexts={"ctxA": ContextEntry(path="/a", last_setup_utc="t", artifacts=["hashB", "hashA"])},
            artifacts={
                "hashA": ArtifactEntry(type="npmrc", path="/n", content_hash="hashA", referenced_by=["ctxA"]),
                "hashB": ArtifactEntry(type="cert_bundle", path="/c", content_hash="hashB", referenced_by=["ctxA"]),
            },
        )
        result = get_context_artifacts(data, "ctxA")
        assert [entry.content_hash for entry in result] == ["hashA", "hashB"]

    def test_returns_empty_list_for_unknown_context(self) -> None:
        """An unknown context id yields an empty list."""
        assert get_context_artifacts(RegistryData(), "nope") == []

    def test_skips_references_missing_from_artifacts(self) -> None:
        """A dangling artifact reference is skipped rather than raising."""
        data = RegistryData(
            contexts={"ctxA": ContextEntry(path="/a", last_setup_utc="t", artifacts=["present", "dangling"])},
            artifacts={
                "present": ArtifactEntry(type="npmrc", path="/n", content_hash="present", referenced_by=["ctxA"]),
            },
        )
        result = get_context_artifacts(data, "ctxA")
        assert [entry.content_hash for entry in result] == ["present"]
