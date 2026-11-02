"""Tests for seed_worktree_trust."""

from agentic_devtools.cli.copilot import trust
from agentic_devtools.cli.copilot.trust import (
    _normalize_path,
    seed_worktree_trust,
)


class TestSeedWorktreeTrust:
    """Tests for seed_worktree_trust."""

    def test_noop_in_test_environment(self, tmp_path):
        """No-ops under pytest (PYTEST_CURRENT_TEST is set)."""
        assert seed_worktree_trust(str(tmp_path)) is False

    def test_noop_when_disabled(self, monkeypatch, tmp_path):
        """No-ops when auto-trust is disabled."""
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.setattr(trust, "is_auto_trust_enabled", lambda: False)
        assert seed_worktree_trust(str(tmp_path)) is False

    def test_refuses_outside_repos_parent(self, monkeypatch, tmp_path):
        """Refuses to seed a path outside repos_parent and does not call ensure."""
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.setattr(trust, "is_auto_trust_enabled", lambda: True)
        called: list[int] = []
        monkeypatch.setattr(
            trust,
            "_ensure_trusted_folder",
            lambda *a, **k: called.append(1) or trust.TrustMutationResult(True, True),
        )
        result = seed_worktree_trust(str(tmp_path / "outside"), repos_parent=str(tmp_path / "repos"))
        assert result is False
        assert called == []

    def test_seeds_and_prints_on_success(self, monkeypatch, tmp_path, capsys):
        """Seeds (repos_parent=None) and prints a notice on success."""
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.setattr(trust, "is_auto_trust_enabled", lambda: True)
        monkeypatch.setattr(trust, "_ensure_trusted_folder", lambda *a, **k: trust.TrustMutationResult(True, True))
        target = tmp_path / "ws"
        assert seed_worktree_trust(str(target)) is True
        assert _normalize_path(str(target)) in capsys.readouterr().out

    def test_returns_false_when_ensure_fails(self, monkeypatch, tmp_path, capsys):
        """Returns False and prints nothing when ensure fails."""
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.setattr(trust, "is_auto_trust_enabled", lambda: True)
        monkeypatch.setattr(trust, "_ensure_trusted_folder", lambda *a, **k: trust.TrustMutationResult(False))
        assert seed_worktree_trust(str(tmp_path / "ws")) is False
        assert capsys.readouterr().out == ""

    def test_returns_false_when_write_succeeded_but_verify_failed(self, monkeypatch, tmp_path, capsys):
        """Returns False (succeeded=False) even when the locked write added the entry but
        post-write verification hit a transient read error (succeeded=False, added=True).
        Callers that need ownership should use seed_worktree_trust_result().added."""
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.setattr(trust, "is_auto_trust_enabled", lambda: True)
        monkeypatch.setattr(
            trust, "_ensure_trusted_folder", lambda *a, **k: trust.TrustMutationResult(False, added=True)
        )
        assert seed_worktree_trust(str(tmp_path / "ws")) is False
        assert capsys.readouterr().out == ""

    def test_seeds_child_within_repos_parent(self, monkeypatch, tmp_path):
        """Seeds a child path that is inside repos_parent."""
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.setattr(trust, "is_auto_trust_enabled", lambda: True)
        seen: dict[str, str] = {}

        def _fake(target, *, subtree_trust=False):
            seen["target"] = target
            return True

        monkeypatch.setattr(
            trust,
            "_ensure_trusted_folder",
            lambda target, **kwargs: _fake(target, **kwargs) and trust.TrustMutationResult(True, True),
        )
        child = tmp_path / "repos" / "KEY-1"
        assert seed_worktree_trust(str(child), repos_parent=str(tmp_path / "repos")) is True
        assert seen["target"] == _normalize_path(str(child))

    def test_returns_true_when_already_trusted(self, monkeypatch, tmp_path, capsys):
        """Returns True (succeeded=True) and prints nothing when already trusted (added=False)."""
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.setattr(trust, "is_auto_trust_enabled", lambda: True)
        monkeypatch.setattr(trust, "_ensure_trusted_folder", lambda *a, **k: trust.TrustMutationResult(True))

        assert seed_worktree_trust(str(tmp_path / "ws")) is True
        assert capsys.readouterr().out == ""
