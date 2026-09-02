"""Tests for register_context."""

from pathlib import Path

from agentic_devtools.cli.setup import registry
from agentic_devtools.cli.setup.registry import (
    compute_content_hash,
    derive_context_id,
    load_registry,
    register_context,
)


class TestRegisterContext:
    """Tests for register_context."""

    def test_registers_new_context_and_artifacts(self, tmp_path: Path) -> None:
        """A new context is recorded with its artifact references."""
        reg = tmp_path / "registry.json"
        repo = tmp_path / "repo"
        repo.mkdir()
        cert = tmp_path / "unified.pem"
        cert.write_text("PEM-A")
        context_id = register_context(repo, [("cert_bundle", cert)], registry_path=reg)
        data = load_registry(reg)
        assert context_id == derive_context_id(repo)
        assert data.contexts[context_id].path == str(repo.resolve())
        assert data.contexts[context_id].artifacts == [compute_content_hash(cert)]

    def test_register_context_keeps_prior_repo_artifact_refs(self, tmp_path: Path) -> None:
        """Registering a second repo context keeps previously registered artifact refs."""
        reg = tmp_path / "registry.json"
        repo_a = tmp_path / "a"
        repo_b = tmp_path / "b"
        repo_a.mkdir()
        repo_b.mkdir()
        cert_a = tmp_path / "a.pem"
        cert_b = tmp_path / "b.pem"
        cert_a.write_text("CERT-A")
        cert_b.write_text("CERT-B")

        id_a = register_context(repo_a, [("cert_bundle", cert_a)], registry_path=reg)
        id_b = register_context(repo_b, [("cert_bundle", cert_b)], registry_path=reg)

        data = load_registry(reg)
        assert id_a != id_b
        assert set(data.contexts) == {id_a, id_b}
        # Repo A's artifact ref survives the repo B registration.
        assert compute_content_hash(cert_a) in data.artifacts
        assert compute_content_hash(cert_b) in data.artifacts

    def test_deduplicates_shared_content_across_contexts(self, tmp_path: Path) -> None:
        """Identical artifact content is stored once, referenced by both contexts."""
        reg = tmp_path / "registry.json"
        repo_a = tmp_path / "a"
        repo_b = tmp_path / "b"
        repo_a.mkdir()
        repo_b.mkdir()
        npmrc = tmp_path / "npmrc"
        npmrc.write_text("registry=https://example")

        id_a = register_context(repo_a, [("npmrc", npmrc)], registry_path=reg)
        id_b = register_context(repo_b, [("npmrc", npmrc)], registry_path=reg)

        data = load_registry(reg)
        shared_hash = compute_content_hash(npmrc)
        assert len(data.artifacts) == 1
        assert sorted(data.artifacts[shared_hash].referenced_by) == sorted([id_a, id_b])

    def test_rerun_same_clone_updates_without_duplicates(self, tmp_path: Path) -> None:
        """Re-running setup for the same clone reuses the context and dedups artifacts."""
        reg = tmp_path / "registry.json"
        repo = tmp_path / "repo"
        repo.mkdir()
        cert = tmp_path / "unified.pem"
        cert.write_text("PEM")

        first = register_context(repo, [("cert_bundle", cert)], registry_path=reg)
        second = register_context(repo, [("cert_bundle", cert)], registry_path=reg)

        data = load_registry(reg)
        assert first == second
        assert len(data.contexts) == 1
        assert data.contexts[first].artifacts == [compute_content_hash(cert)]
        assert len(data.artifacts) == 1

    def test_empty_artifact_list_registers_bare_context(self, tmp_path: Path) -> None:
        """A context with no artifacts is still recorded."""
        reg = tmp_path / "registry.json"
        repo = tmp_path / "repo"
        repo.mkdir()
        context_id = register_context(repo, [], registry_path=reg)
        data = load_registry(reg)
        assert data.contexts[context_id].artifacts == []
        assert data.artifacts == {}

    def test_uses_default_path_when_omitted(self, tmp_path: Path, monkeypatch) -> None:
        """When registry_path is omitted, get_registry_path is consulted."""
        default_path = tmp_path / "default" / "registry.json"
        monkeypatch.setattr(registry, "get_registry_path", lambda: default_path)
        repo = tmp_path / "repo"
        repo.mkdir()
        context_id = register_context(repo, [])
        assert load_registry(default_path).contexts[context_id].path == str(repo.resolve())
