"""Tests for deregister_context."""

from pathlib import Path

from agentic_devtools.cli.setup import registry
from agentic_devtools.cli.setup.registry import (
    ArtifactEntry,
    ContextEntry,
    RegistryData,
    deregister_context,
    load_registry,
    save_registry,
)


def _seed(path: Path) -> None:
    data = RegistryData(
        contexts={
            "ctxA": ContextEntry(path="/a", last_setup_utc="t", artifacts=["shared", "onlyA"]),
            "ctxB": ContextEntry(path="/b", last_setup_utc="t", artifacts=["shared"]),
        },
        artifacts={
            "shared": ArtifactEntry(type="npmrc", path="/n", content_hash="shared", referenced_by=["ctxA", "ctxB"]),
            "onlyA": ArtifactEntry(type="cert_bundle", path="/a.pem", content_hash="onlyA", referenced_by=["ctxA"]),
        },
    )
    save_registry(data, path)


class TestDeregisterContext:
    """Tests for deregister_context."""

    def test_removes_context_and_its_references_only(self, tmp_path: Path) -> None:
        """Deregistering ctxA drops its references but preserves ctxB's."""
        reg = tmp_path / "registry.json"
        _seed(reg)
        removed = deregister_context("ctxA", registry_path=reg)
        data = load_registry(reg)
        assert removed is True
        assert set(data.contexts) == {"ctxB"}
        # Shared artifact still referenced by ctxB (not clobbered).
        assert data.artifacts["shared"].referenced_by == ["ctxB"]
        # Artifact only referenced by ctxA remains (append-only), now unreferenced.
        assert data.artifacts["onlyA"].referenced_by == []

    def test_returns_false_for_unknown_context(self, tmp_path: Path) -> None:
        """Deregistering a missing context returns False and does not rewrite the registry."""
        reg = tmp_path / "registry.json"
        _seed(reg)
        mtime_before = reg.stat().st_mtime_ns
        removed = deregister_context("ctxMISSING", registry_path=reg)
        assert removed is False
        assert set(load_registry(reg).contexts) == {"ctxA", "ctxB"}
        # Registry must not have been rewritten (no needless mtime churn).
        assert reg.stat().st_mtime_ns == mtime_before

    def test_handles_empty_registry(self, tmp_path: Path) -> None:
        """Deregistering against an empty registry returns False without creating the file."""
        reg = tmp_path / "registry.json"
        removed = deregister_context("ctxA", registry_path=reg)
        assert removed is False
        assert not reg.exists()

    def test_removes_context_with_no_artifact_references(self, tmp_path: Path) -> None:
        """Deregistering a context not referenced by any artifact still succeeds."""
        reg = tmp_path / "registry.json"
        # Artifact exists but does not reference ctxOrphan — covers the
        # `if context_id in entry.referenced_by:` → False branch.
        data = RegistryData(
            contexts={"ctxOrphan": ContextEntry(path="/o", last_setup_utc="t", artifacts=[])},
            artifacts={
                "h1": ArtifactEntry(type="cert_bundle", path="/p.pem", content_hash="h1", referenced_by=["ctxOther"]),
            },
        )
        save_registry(data, reg)
        assert deregister_context("ctxOrphan", registry_path=reg) is True
        after = load_registry(reg)
        assert after.contexts == {}
        # Unrelated artifact reference must remain untouched.
        assert after.artifacts["h1"].referenced_by == ["ctxOther"]

    def test_uses_default_path_when_omitted(self, tmp_path: Path, monkeypatch) -> None:
        default_path = tmp_path / "default" / "registry.json"
        default_path.parent.mkdir(parents=True)
        _seed(default_path)
        monkeypatch.setattr(registry, "get_registry_path", lambda: default_path)
        assert deregister_context("ctxA") is True
        assert set(load_registry(default_path).contexts) == {"ctxB"}
