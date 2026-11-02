"""Tests for build_manifest_command."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.azure_devops.pr_review_manifest import build_manifest_command

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_manifest"
_HELPERS = "agentic_devtools.cli.azure_devops.helpers.resolve_review_artifact_dir_name"

_PR_DETAILS = {
    "pullRequest": {
        "title": "T",
        "description": "d",
        "lastMergeSourceCommit": {"commitId": "abc123abc123def"},
    },
    "files": [
        {
            "path": "/src/a.py",
            "changeType": "M",
            "addedLineCount": 3,
            "removedLineCount": 1,
            "isBinary": False,
            "addedLines": [],
        }
    ],
}


def _state(values):
    def _get(key, default=None):
        return values.get(key, default)

    return _get


def _write_details(state_dir):
    (state_dir / "temp-get-pull-request-details-response.json").write_text(json.dumps(_PR_DETAILS), encoding="utf-8")


class TestBuildManifestCommand:
    def test_writes_artifacts(self, tmp_path):
        _write_details(tmp_path)
        values = {"pull_request_id": "123", "review.commit_hash_short": "abc123abc123", "jira.issue_key": "J-1"}
        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", side_effect=_state(values)),
            patch(f"{_MODULE}.resolve_repo_root", return_value=str(tmp_path)),
            patch(f"{_MODULE}.load_review_focus_areas", return_value=None),
            patch(_HELPERS, return_value="dir1"),
            patch("sys.argv", ["cmd", "--pr", "123"]),
        ):
            build_manifest_command()
        prompts_dir = tmp_path / "pull-request-review" / "dir1"
        assert (prompts_dir / "manifest.json").exists()
        assert (prompts_dir / "pr-context.md").exists()
        manifest = json.loads((prompts_dir / "manifest.json").read_text(encoding="utf-8"))
        assert manifest["budget"] is not None

    def test_pr_resolved_from_state(self, tmp_path):
        _write_details(tmp_path)
        values = {"pull_request_id": "77", "review.commit_hash_short": "abc123abc123", "jira.issue_key": None}
        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", side_effect=_state(values)),
            patch(f"{_MODULE}.resolve_repo_root", return_value=str(tmp_path)),
            patch(f"{_MODULE}.load_review_focus_areas", return_value=None),
            patch(_HELPERS, return_value="dir1"),
            patch("sys.argv", ["cmd"]),
        ):
            build_manifest_command()
        assert (tmp_path / "pull-request-review" / "dir1" / "manifest.json").exists()

    def test_dry_run_writes_nothing(self, tmp_path, capsys):
        _write_details(tmp_path)
        values = {"pull_request_id": "5", "review.commit_hash_short": "abc123abc123"}
        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", side_effect=_state(values)),
            patch(f"{_MODULE}.resolve_repo_root", return_value=str(tmp_path)),
            patch(f"{_MODULE}.load_review_focus_areas", return_value=None),
            patch(_HELPERS, return_value="dir1"),
            patch("sys.argv", ["cmd", "--pr", "5", "--dry-run"]),
        ):
            build_manifest_command()
        prompts_dir = tmp_path / "pull-request-review" / "dir1"
        assert not (prompts_dir / "manifest.json").exists()
        assert "[dry-run]" in capsys.readouterr().out

    def test_exit_when_no_pr(self, tmp_path):
        with (
            patch(f"{_MODULE}.get_value", side_effect=_state({})),
            patch("sys.argv", ["cmd"]),
        ):
            with pytest.raises(SystemExit) as exc:
                build_manifest_command()
            assert exc.value.code == 1

    def test_exit_when_details_missing(self, tmp_path):
        values = {"pull_request_id": "5", "review.commit_hash_short": "abc123abc123"}
        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", side_effect=_state(values)),
            patch(_HELPERS, return_value="dir1"),
            patch("sys.argv", ["cmd", "--pr", "5"]),
        ):
            with pytest.raises(SystemExit) as exc:
                build_manifest_command()
            assert exc.value.code == 1

    def test_exit_when_pr_id_not_integer(self, tmp_path):
        values = {"pull_request_id": "not-a-number"}
        with (
            patch(f"{_MODULE}.get_value", side_effect=_state(values)),
            patch("sys.argv", ["cmd"]),
        ):
            with pytest.raises(SystemExit) as exc:
                build_manifest_command()
            assert exc.value.code == 1

    def test_exit_when_details_invalid_json(self, tmp_path):
        (tmp_path / "temp-get-pull-request-details-response.json").write_text("{ bad json", encoding="utf-8")
        values = {"pull_request_id": "5", "review.commit_hash_short": "abc123abc123"}
        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", side_effect=_state(values)),
            patch(_HELPERS, return_value="dir1"),
            patch("sys.argv", ["cmd", "--pr", "5"]),
        ):
            with pytest.raises(SystemExit) as exc:
                build_manifest_command()
            assert exc.value.code == 1

    def test_exit_when_details_open_os_error(self, tmp_path):
        _write_details(tmp_path)
        values = {"pull_request_id": "5", "review.commit_hash_short": "abc123abc123"}
        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", side_effect=_state(values)),
            patch(_HELPERS, return_value="dir1"),
            patch("sys.argv", ["cmd", "--pr", "5"]),
            patch("builtins.open", side_effect=OSError("boom")),
        ):
            with pytest.raises(SystemExit) as exc:
                build_manifest_command()
            assert exc.value.code == 1

    def test_commit_hash_short_derived_from_pr_details(self, tmp_path):
        # When PR details contain a valid commit hash, the artifact directory should be
        # derived from it rather than from state — even when state has a stale value.
        _write_details(tmp_path)  # commitId = "abc123abc123def" -> short = "abc123abc123"
        values = {
            "pull_request_id": "123",
            "review.commit_hash_short": "stale000stale",  # stale state value — must not be used
            "jira.issue_key": "J-1",
        }
        captured_calls: list[tuple] = []
        real_resolve = __import__(
            "agentic_devtools.cli.azure_devops.helpers",
            fromlist=["resolve_review_artifact_dir_name"],
        ).resolve_review_artifact_dir_name

        def _capture(pr_id, hash_short, **kw):
            captured_calls.append((pr_id, hash_short))
            return real_resolve(pr_id, hash_short, **kw)

        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", side_effect=_state(values)),
            patch(f"{_MODULE}.resolve_repo_root", return_value=str(tmp_path)),
            patch(f"{_MODULE}.load_review_focus_areas", return_value=None),
            patch(_HELPERS, side_effect=_capture),
            patch("sys.argv", ["cmd", "--pr", "123"]),
        ):
            build_manifest_command()

        assert captured_calls, "resolve_review_artifact_dir_name was not called"
        _, used_hash_short = captured_calls[0]
        assert used_hash_short == "abc123abc123", ()

    def test_commit_hash_short_falls_back_to_state_when_details_lack_hash(self, tmp_path):
        # When PR details have no lastMergeSourceCommit, fall back to state value.
        details_no_hash = {
            "pullRequest": {"title": "T", "description": "d"},
            "files": [
                {
                    "path": "/src/a.py",
                    "changeType": "M",
                    "addedLineCount": 1,
                    "removedLineCount": 0,
                    "isBinary": False,
                    "addedLines": [],
                }
            ],
        }
        (tmp_path / "temp-get-pull-request-details-response.json").write_text(
            json.dumps(details_no_hash), encoding="utf-8"
        )
        values = {
            "pull_request_id": "42",
            "review.commit_hash_short": "fallback0012",
            "jira.issue_key": None,
        }
        captured_calls: list[tuple] = []
        real_resolve = __import__(
            "agentic_devtools.cli.azure_devops.helpers",
            fromlist=["resolve_review_artifact_dir_name"],
        ).resolve_review_artifact_dir_name

        def _capture(pr_id, hash_short, **kw):
            captured_calls.append((pr_id, hash_short))
            return real_resolve(pr_id, hash_short, **kw)

        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", side_effect=_state(values)),
            patch(f"{_MODULE}.resolve_repo_root", return_value=str(tmp_path)),
            patch(f"{_MODULE}.load_review_focus_areas", return_value=None),
            patch(_HELPERS, side_effect=_capture),
            patch("sys.argv", ["cmd", "--pr", "42"]),
        ):
            build_manifest_command()

        assert captured_calls, "resolve_review_artifact_dir_name was not called"
        _, used_hash_short = captured_calls[0]
        assert used_hash_short == "fallback0012", ()

    def test_commit_hash_short_falls_back_via_resolver_when_details_and_state_lack_hash(self, tmp_path):
        """When PR details AND state lack a hash, fallback should be delegated to resolver (#1182)."""
        details_no_hash = {
            "pullRequest": {"title": "T", "description": "d"},
            "files": [
                {
                    "path": "/src/a.py",
                    "changeType": "M",
                    "addedLineCount": 1,
                    "removedLineCount": 0,
                    "isBinary": False,
                    "addedLines": [],
                }
            ],
        }
        (tmp_path / "temp-get-pull-request-details-response.json").write_text(
            json.dumps(details_no_hash), encoding="utf-8"
        )
        values = {"pull_request_id": "25553", "jira.issue_key": None}
        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", side_effect=_state(values)),
            patch(f"{_MODULE}.resolve_repo_root", return_value=str(tmp_path)),
            patch(f"{_MODULE}.load_review_focus_areas", return_value=None),
            patch(_HELPERS, return_value="2fea8cdf46c8") as resolver,
            patch("sys.argv", ["cmd", "--pr", "25553"]),
        ):
            build_manifest_command()

        resolver.assert_called_once_with(25553, None, backfill=True)

    def test_manifest_commit_hash_short_uses_recovered_dir_name_when_details_and_state_lack_hash(self, tmp_path):
        """Manifest commitHashShort is set from resolver-recovered dir_name when both sources lack a hash."""
        details_no_hash = {
            "pullRequest": {"title": "T", "description": "d"},
            "files": [
                {
                    "path": "/src/a.py",
                    "changeType": "M",
                    "addedLineCount": 1,
                    "removedLineCount": 0,
                    "isBinary": False,
                    "addedLines": [],
                }
            ],
        }
        (tmp_path / "temp-get-pull-request-details-response.json").write_text(
            json.dumps(details_no_hash), encoding="utf-8"
        )
        values = {"pull_request_id": "25553", "jira.issue_key": None}
        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", side_effect=_state(values)),
            patch(f"{_MODULE}.resolve_repo_root", return_value=str(tmp_path)),
            patch(f"{_MODULE}.load_review_focus_areas", return_value=None),
            patch(_HELPERS, return_value="2fea8cdf46c8"),
            patch("sys.argv", ["cmd", "--pr", "25553"]),
        ):
            build_manifest_command()

        prompts_dir = tmp_path / "pull-request-review" / "2fea8cdf46c8"
        manifest = json.loads((prompts_dir / "manifest.json").read_text(encoding="utf-8"))
        assert manifest["commitHashShort"] == "2fea8cdf46c8"

    def test_commit_hash_short_falls_back_when_details_hash_is_unsafe(self, tmp_path):
        """Uses state/review-state fallback when PR details hash is present but unsafe."""
        details_with_unsafe_hash = {
            "pullRequest": {
                "title": "T",
                "description": "d",
                "lastMergeSourceCommit": {"commitId": "../not-a-safe-hash"},
            },
            "files": [
                {
                    "path": "/src/a.py",
                    "changeType": "M",
                    "addedLineCount": 1,
                    "removedLineCount": 0,
                    "isBinary": False,
                    "addedLines": [],
                }
            ],
        }
        (tmp_path / "temp-get-pull-request-details-response.json").write_text(
            json.dumps(details_with_unsafe_hash), encoding="utf-8"
        )
        values = {"pull_request_id": "25553", "jira.issue_key": None}
        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", side_effect=_state(values)),
            patch(f"{_MODULE}.resolve_repo_root", return_value=str(tmp_path)),
            patch(f"{_MODULE}.load_review_focus_areas", return_value=None),
            patch(_HELPERS, return_value="2fea8cdf46c8") as resolver,
            patch("sys.argv", ["cmd", "--pr", "25553"]),
        ):
            build_manifest_command()

        resolver.assert_called_once_with(25553, None, backfill=True)
