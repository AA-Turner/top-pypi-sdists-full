"""Tests for seed_worktree_trust_result."""

from agentic_devtools.cli.copilot import trust
from agentic_devtools.cli.copilot.trust import (
    TrustMutationResult,
    _normalize_path,
    seed_worktree_trust_result,
)


class TestSeedWorktreeTrustResult:
    """Tests for seed_worktree_trust_result."""

    def test_noop_in_test_environment(self, tmp_path):
        """No-ops under pytest; returns sentinel with both flags False."""
        result = seed_worktree_trust_result(str(tmp_path))
        assert result == TrustMutationResult(False)
        assert result.added is False

    def test_noop_when_disabled(self, monkeypatch, tmp_path):
        """No-ops when auto-trust is disabled."""
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.setattr(trust, "is_auto_trust_enabled", lambda: False)
        result = seed_worktree_trust_result(str(tmp_path))
        assert result == TrustMutationResult(False)

    def test_refuses_outside_repos_parent(self, monkeypatch, tmp_path):
        """Refuses a path outside repos_parent without calling ensure."""
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.setattr(trust, "is_auto_trust_enabled", lambda: True)
        called: list[int] = []
        monkeypatch.setattr(
            trust,
            "_ensure_trusted_folder",
            lambda *a, **k: called.append(1) or TrustMutationResult(True, True),
        )
        result = seed_worktree_trust_result(str(tmp_path / "outside"), repos_parent=str(tmp_path / "repos"))
        assert result == TrustMutationResult(False)
        assert called == []

    def test_returns_full_result_on_success(self, monkeypatch, tmp_path, capsys):
        """Returns succeeded=True, added=True and prints a notice when a new entry is written."""
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.setattr(trust, "is_auto_trust_enabled", lambda: True)
        monkeypatch.setattr(trust, "_ensure_trusted_folder", lambda *a, **k: TrustMutationResult(True, True))
        target = tmp_path / "ws"
        result = seed_worktree_trust_result(str(target))
        assert result.succeeded is True
        assert result.added is True
        assert _normalize_path(str(target)) in capsys.readouterr().out

    def test_returns_added_true_when_write_succeeded_but_verify_failed(self, monkeypatch, tmp_path, capsys):
        """Returns added=True (ownership) even when post-write verification failed."""
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.setattr(trust, "is_auto_trust_enabled", lambda: True)
        monkeypatch.setattr(trust, "_ensure_trusted_folder", lambda *a, **k: TrustMutationResult(False, added=True))
        result = seed_worktree_trust_result(str(tmp_path / "ws"))
        assert result.succeeded is False
        assert result.added is True
        assert capsys.readouterr().out == ""

    def test_returns_succeeded_true_added_false_when_already_trusted(self, monkeypatch, tmp_path, capsys):
        """Returns succeeded=True, added=False when the entry was already present."""
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.setattr(trust, "is_auto_trust_enabled", lambda: True)
        monkeypatch.setattr(trust, "_ensure_trusted_folder", lambda *a, **k: TrustMutationResult(True))
        result = seed_worktree_trust_result(str(tmp_path / "ws"))
        assert result.succeeded is True
        assert result.added is False
        assert capsys.readouterr().out == ""
