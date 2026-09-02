"""Tests for worktree.create_worktree."""

from types import SimpleNamespace

from agentic_devtools.cli.git import worktree


class TestCreateWorktree:
    """Tests for create_worktree."""

    def test_success_adapts_cli_result_and_forwards_arguments(self, monkeypatch):
        """Successful CLI worktree creation is adapted to SetupResult(mode='created')."""
        calls = []

        def fake_cli_create_worktree(issue_key, *, branch_name, use_existing_branch, start_point):
            calls.append(
                {
                    "issue_key": issue_key,
                    "branch_name": branch_name,
                    "use_existing_branch": use_existing_branch,
                    "start_point": start_point,
                }
            )
            return SimpleNamespace(
                success=True,
                worktree_path="/repo/1900",
                branch_name="feature/1900/focused-tests",
                error_message=None,
            )

        monkeypatch.setattr(worktree, "_cli_create_worktree", fake_cli_create_worktree)

        result = worktree.create_worktree("#1900", "Add focused tests", start_point="origin/main")

        assert result.error is None
        assert result.worktree_path == "/repo/1900"
        assert result.branch_name == "feature/1900/focused-tests"
        assert result.mode == "created"
        assert calls == [
            {
                "issue_key": "1900",
                "branch_name": "feature/1900/focused-tests",
                "use_existing_branch": False,
                "start_point": "origin/main",
            }
        ]

    def test_branch_name_override_and_use_existing_branch_are_forwarded(self, monkeypatch):
        """An explicit branch_name bypasses generated branch naming and is forwarded."""
        captured = {}

        def fake_cli_create_worktree(issue_key, *, branch_name, use_existing_branch, start_point):
            captured.update(
                issue_key=issue_key,
                branch_name=branch_name,
                use_existing_branch=use_existing_branch,
                start_point=start_point,
            )
            return SimpleNamespace(
                success=True,
                worktree_path="/repo/1900",
                branch_name=branch_name,
                error_message=None,
            )

        monkeypatch.setattr(worktree, "_cli_create_worktree", fake_cli_create_worktree)

        result = worktree.create_worktree(
            "1900",
            "ignored description",
            branch_name="feature/1900/from-origin",
            use_existing_branch=True,
            start_point="origin/main",
        )

        assert result.mode == "created"
        assert result.branch_name == "feature/1900/from-origin"
        assert captured == {
            "issue_key": "1900",
            "branch_name": "feature/1900/from-origin",
            "use_existing_branch": True,
            "start_point": "origin/main",
        }

    def test_failure_adapts_cli_error_to_corruption_blocked_state(self, monkeypatch):
        """A failed CLI result becomes a SetupResult with a corruption BlockedState."""
        monkeypatch.setattr(
            worktree,
            "_cli_create_worktree",
            lambda *args, **kwargs: SimpleNamespace(
                success=False,
                worktree_path="",
                branch_name="",
                error_message="Directory exists but is not a git worktree",
            ),
        )

        result = worktree.create_worktree("PROJECT-1234", "Add tests")

        assert result.worktree_path is None
        assert result.branch_name is None
        assert result.mode is None
        assert result.error is not None
        assert result.error.category == "corruption"
        assert result.error.message == "Directory exists but is not a git worktree"

    def test_failure_uses_default_error_message_when_cli_message_missing(self, monkeypatch):
        """A failed CLI result without an error message uses the default failure message (transient)."""
        monkeypatch.setattr(
            worktree,
            "_cli_create_worktree",
            lambda *args, **kwargs: SimpleNamespace(
                success=False,
                worktree_path="/repo/1900",
                branch_name="feature/1900/tests",
                error_message="",
            ),
        )

        result = worktree.create_worktree("#1900", "Add tests")

        assert result.worktree_path == "/repo/1900"
        assert result.branch_name == "feature/1900/tests"
        assert result.error is not None
        assert result.error.category == "transient"
        assert result.error.message == "Worktree creation failed"

    def test_transient_failure_does_not_classify_as_corruption(self, monkeypatch):
        """Lock contention and other recoverable git failures are classified as transient, not corruption.

        This preserves the retry path for temporary failures instead of escalating them to
        manual-cleanup corruption blocks.
        """
        monkeypatch.setattr(
            worktree,
            "_cli_create_worktree",
            lambda *args, **kwargs: SimpleNamespace(
                success=False,
                worktree_path=None,
                branch_name=None,
                error_message="error: could not lock config file: File exists",
            ),
        )

        result = worktree.create_worktree("1900", "Add tests")

        assert result.error is not None
        assert result.error.category == "transient"

    def test_system_exit_from_cli_helper_returns_transient_blocked_state(self, monkeypatch):
        """SystemExit raised by the CLI worktree helper is caught and returned as a transient block."""

        def _raise_system_exit(*args, **kwargs):
            raise SystemExit(1)

        monkeypatch.setattr(worktree, "_cli_create_worktree", _raise_system_exit)

        result = worktree.create_worktree("1900", "Add tests")

        assert result.error is not None
        assert result.error.category == "transient"
        assert "sys.exit(1)" in result.error.message

    def test_branch_already_exists_classified_as_context_mismatch(self, monkeypatch):
        """'branch already exists' errors are permanent and classified as context_mismatch.

        These require manual cleanup of the stale local branch and cannot be resolved by
        retrying, so they must not be sent through the transient retry path.
        """
        monkeypatch.setattr(
            worktree,
            "_cli_create_worktree",
            lambda *args, **kwargs: SimpleNamespace(
                success=False,
                worktree_path=None,
                branch_name=None,
                error_message="fatal: A branch named 'feature/1900/x' already exists",
            ),
        )

        result = worktree.create_worktree("1900", "Add tests")

        assert result.error is not None
        assert result.error.category == "context_mismatch"
