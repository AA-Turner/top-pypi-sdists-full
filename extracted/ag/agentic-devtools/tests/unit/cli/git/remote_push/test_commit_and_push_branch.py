"""Tests for commit_and_push_branch."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.git.remote_push import commit_and_push_branch


class TestCommitAndPushBranch:
    """Tests for commit_and_push_branch()."""

    # ------------------------------------------------------------------ helpers

    @staticmethod
    def _make_fake_run(
        fail_on: str | None = None,
        git_calls: list | None = None,
        failure_stderr: str = "fatal: some git error",
    ):
        """Return a fake subprocess.run side_effect.

        If *fail_on* is given, calls that contain that string fail;
        all other calls succeed.  Call records are appended to *git_calls*.
        """
        success = MagicMock(returncode=0, stdout="", stderr="")
        failure = MagicMock(returncode=1, stdout="", stderr=failure_stderr)

        def fake_run(cmd: list, **_: object) -> MagicMock:
            if git_calls is not None:
                git_calls.append(list(cmd))
            if fail_on and fail_on in cmd:
                return failure
            return success

        return fake_run

    # --------------------------------------------------------------- bare push

    def test_bare_origin_push_by_default(self, tmp_path: Path) -> None:
        """Without token_remote_url, push targets bare 'origin'."""
        git_calls: list[list[str]] = []

        with patch("subprocess.run", side_effect=self._make_fake_run(git_calls=git_calls)):
            commit_and_push_branch(
                repo_path=str(tmp_path),
                branch="my-branch",
                add_paths=["some/file.md"],
                commit_message="chore: test",
            )

        push_call = next(c for c in git_calls if "push" in c)
        assert "origin" in push_call
        assert not any("x-access-token" in str(a) for a in push_call)

    def test_token_remote_url_used_when_provided(self, tmp_path: Path) -> None:
        """When token_remote_url is set, push uses that URL instead of 'origin'."""
        token_url = "https://x-access-token:test-pat@github.com/org/repo.git"
        git_calls: list[list[str]] = []

        with patch("subprocess.run", side_effect=self._make_fake_run(git_calls=git_calls)):
            commit_and_push_branch(
                repo_path=str(tmp_path),
                branch="my-branch",
                add_paths=["some/file.md"],
                commit_message="chore: test",
                token_remote_url=token_url,
            )

        push_call = next(c for c in git_calls if "push" in c)
        assert token_url in push_call

    def test_empty_string_token_remote_url_falls_back_to_origin(self, tmp_path: Path) -> None:
        """An empty string token_remote_url must fall back to the bare 'origin' remote.

        ``is not None`` would treat "" as an explicit remote and produce
        ``git push "" ...``.  The truthy check (``if token_remote_url``) must
        fall back to ``remote`` for any falsy value.
        """
        git_calls: list[list[str]] = []

        with patch("subprocess.run", side_effect=self._make_fake_run(git_calls=git_calls)):
            commit_and_push_branch(
                repo_path=str(tmp_path),
                branch="my-branch",
                add_paths=[],
                commit_message="chore: test",
                token_remote_url="",
            )

        push_call = next(c for c in git_calls if "push" in c)
        assert "origin" in push_call
        assert "" not in push_call  # empty string must not appear as a remote arg

    # ------------------------------------------------------------- start_point

    def test_start_point_used_in_checkout(self, tmp_path: Path) -> None:
        """When start_point is given, checkout uses it as the branch base."""
        git_calls: list[list[str]] = []
        sha = "a" * 40

        with patch("subprocess.run", side_effect=self._make_fake_run(git_calls=git_calls)):
            commit_and_push_branch(
                repo_path=str(tmp_path),
                branch="my-branch",
                add_paths=[],
                commit_message="chore: test",
                start_point=sha,
            )

        checkout_call = next(c for c in git_calls if "checkout" in c)
        assert sha in checkout_call
        assert "-B" in checkout_call

    def test_no_start_point_checkout_without_base(self, tmp_path: Path) -> None:
        """Without start_point, checkout -B is called without an extra argument."""
        git_calls: list[list[str]] = []

        with patch("subprocess.run", side_effect=self._make_fake_run(git_calls=git_calls)):
            commit_and_push_branch(
                repo_path=str(tmp_path),
                branch="my-branch",
                add_paths=[],
                commit_message="chore: test",
            )

        checkout_call = next(c for c in git_calls if "checkout" in c)
        # The SHA is not present; call ends after branch name
        assert checkout_call[-1] == "my-branch"

    # ------------------------------------------------------------ skip_checkout

    def test_skip_checkout_omits_checkout_command(self, tmp_path: Path) -> None:
        """When skip_checkout=True, no git checkout call is made."""
        git_calls: list[list[str]] = []

        with patch("subprocess.run", side_effect=self._make_fake_run(git_calls=git_calls)):
            commit_and_push_branch(
                repo_path=str(tmp_path),
                branch="my-branch",
                add_paths=["file.md"],
                commit_message="chore: test",
                skip_checkout=True,
            )

        assert not any("checkout" in c for c in git_calls)

    def test_skip_checkout_false_includes_checkout(self, tmp_path: Path) -> None:
        """When skip_checkout=False (default), git checkout is called."""
        git_calls: list[list[str]] = []

        with patch("subprocess.run", side_effect=self._make_fake_run(git_calls=git_calls)):
            commit_and_push_branch(
                repo_path=str(tmp_path),
                branch="my-branch",
                add_paths=[],
                commit_message="chore: test",
                skip_checkout=False,
            )

        assert any("checkout" in c for c in git_calls)

    # ------------------------------------------------------------ allow_empty

    def test_allow_empty_flag_passed_to_commit(self, tmp_path: Path) -> None:
        """allow_empty=True adds --allow-empty to the git commit call."""
        git_calls: list[list[str]] = []

        with patch("subprocess.run", side_effect=self._make_fake_run(git_calls=git_calls)):
            commit_and_push_branch(
                repo_path=str(tmp_path),
                branch="my-branch",
                add_paths=[],
                commit_message="chore: test",
                allow_empty=True,
            )

        commit_call = next(c for c in git_calls if "commit" in c)
        assert "--allow-empty" in commit_call

    def test_no_allow_empty_by_default(self, tmp_path: Path) -> None:
        """Without allow_empty, --allow-empty is not added to the commit."""
        git_calls: list[list[str]] = []

        with patch("subprocess.run", side_effect=self._make_fake_run(git_calls=git_calls)):
            commit_and_push_branch(
                repo_path=str(tmp_path),
                branch="my-branch",
                add_paths=[],
                commit_message="chore: test",
            )

        commit_call = next(c for c in git_calls if "commit" in c)
        assert "--allow-empty" not in commit_call

    # ------------------------------------------------------------- force push

    def test_force_push_by_default(self, tmp_path: Path) -> None:
        """Push includes --force by default."""
        git_calls: list[list[str]] = []

        with patch("subprocess.run", side_effect=self._make_fake_run(git_calls=git_calls)):
            commit_and_push_branch(
                repo_path=str(tmp_path),
                branch="my-branch",
                add_paths=[],
                commit_message="chore: test",
            )

        push_call = next(c for c in git_calls if "push" in c)
        assert "--force" in push_call

    def test_non_force_push_when_disabled(self, tmp_path: Path) -> None:
        """When force=False, --force is not added to the push."""
        git_calls: list[list[str]] = []

        with patch("subprocess.run", side_effect=self._make_fake_run(git_calls=git_calls)):
            commit_and_push_branch(
                repo_path=str(tmp_path),
                branch="my-branch",
                add_paths=[],
                commit_message="chore: test",
                force=False,
            )

        push_call = next(c for c in git_calls if "push" in c)
        assert "--force" not in push_call

    # -------------------------------------------------------- refspec in push

    def test_push_refspec_matches_branch(self, tmp_path: Path) -> None:
        """Push uses HEAD:refs/heads/<branch> refspec."""
        git_calls: list[list[str]] = []
        branch = "audit/my-branch"

        with patch("subprocess.run", side_effect=self._make_fake_run(git_calls=git_calls)):
            commit_and_push_branch(
                repo_path=str(tmp_path),
                branch=branch,
                add_paths=[],
                commit_message="chore: test",
            )

        push_call = next(c for c in git_calls if "push" in c)
        assert f"HEAD:refs/heads/{branch}" in push_call

    # ------------------------------------------------------------ error raises

    def test_nonzero_git_return_raises_called_process_error(self, tmp_path: Path) -> None:
        """A non-zero git exit code raises subprocess.CalledProcessError."""
        git_failure = MagicMock(returncode=1, stdout="", stderr="fatal: not a git repo")

        with patch("subprocess.run", return_value=git_failure):
            with pytest.raises(subprocess.CalledProcessError):
                commit_and_push_branch(
                    repo_path=str(tmp_path),
                    branch="my-branch",
                    add_paths=[],
                    commit_message="chore: test",
                )

    # ------------------------------------------------------ token redaction

    def test_token_redacted_from_error_when_token_url_provided(self, tmp_path: Path) -> None:
        """When token_remote_url is given, the embedded secret is redacted from errors."""
        secret = "super-secret-pat"
        token_url = f"https://x-access-token:{secret}@github.com/org/repo.git"
        with patch(
            "subprocess.run",
            side_effect=self._make_fake_run(
                fail_on=token_url,
                failure_stderr=f"error: Permission denied to https://x-access-token:{secret}@github.com/",
            ),
        ):
            with pytest.raises(subprocess.CalledProcessError) as exc_info:
                commit_and_push_branch(
                    repo_path=str(tmp_path),
                    branch="my-branch",
                    add_paths=[],
                    commit_message="chore: test",
                    token_remote_url=token_url,
                )

        # The secret must not appear in the exception details.
        assert secret not in str(exc_info.value.stderr)
        assert "***" in str(exc_info.value.stderr)
        assert secret not in str(exc_info.value.cmd)
        assert "***" in str(exc_info.value.cmd)
        assert exc_info.value.cmd[:3] == ["git", "-C", str(tmp_path.resolve())]

    def test_no_redaction_when_no_token_url(self, tmp_path: Path) -> None:
        """Without token_remote_url, error messages are passed through unchanged."""
        err_msg = "fatal: remote: Write access to repository not granted."
        git_failure = MagicMock(returncode=1, stdout="", stderr=err_msg)

        with patch("subprocess.run", return_value=git_failure):
            with pytest.raises(subprocess.CalledProcessError) as exc_info:
                commit_and_push_branch(
                    repo_path=str(tmp_path),
                    branch="my-branch",
                    add_paths=[],
                    commit_message="chore: test",
                )

        assert err_msg in str(exc_info.value.stderr)

    def test_no_password_in_token_url_skips_secret_extraction(self, tmp_path: Path) -> None:
        """token_remote_url with no password: embedded_secret stays empty.

        When token_remote_url is provided but contains no password component,
        the secret extraction logic is skipped and embedded_secret stays empty.
        """
        # A URL without credentials — urlparse().password is None, so the
        # if _parsed.password: branch is False and embedded_secret stays ""
        token_url = "https://github.com/org/repo.git"
        git_calls: list[list[str]] = []

        with patch("subprocess.run", side_effect=self._make_fake_run(git_calls=git_calls)):
            commit_and_push_branch(
                repo_path=str(tmp_path),
                branch="my-branch",
                add_paths=[],
                commit_message="chore: test",
                token_remote_url=token_url,
            )

        push_call = next(c for c in git_calls if "push" in c)
        assert token_url in push_call

    def test_full_url_redacted_from_error_when_url_appears_verbatim(self, tmp_path: Path) -> None:
        """Full URL is replaced with <redacted-url> when it appears verbatim in error.

        When token_remote_url has no password (so embedded_secret is empty) and the
        full URL itself appears verbatim in the error message, the URL is replaced
        with '<redacted-url>' to prevent it from leaking in exceptions.
        """
        # Use a no-password URL so embedded_secret is ""; the full URL itself
        # appears in the error, triggering the second branch of _redact (line 93).
        token_url = "https://github.com/org/repo.git"
        git_failure = MagicMock(
            returncode=1,
            stdout="",
            stderr=f"error: Permission denied to {token_url}",
        )

        with patch("subprocess.run", return_value=git_failure):
            with pytest.raises(subprocess.CalledProcessError) as exc_info:
                commit_and_push_branch(
                    repo_path=str(tmp_path),
                    branch="my-branch",
                    add_paths=[],
                    commit_message="chore: test",
                    token_remote_url=token_url,
                )

        assert "<redacted-url>" in str(exc_info.value.stderr)
        assert token_url not in str(exc_info.value.stderr)
