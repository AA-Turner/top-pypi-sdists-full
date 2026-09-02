"""Tests for triage_command and _apply_depth_to_queue."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.azure_devops.pr_review_triage import (
    _apply_depth_to_queue,
    triage_command,
)

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_triage"
_HELPERS = "agentic_devtools.cli.azure_devops.helpers.resolve_review_artifact_dir_name"


def _state(values):
    def _get(key, default=None):
        return values.get(key, default)

    return _get


def _row(key, path, *, mode="diff", changed=5):
    return {"fileKey": key, "normalizedPath": path, "reviewMode": mode, "changedLines": changed}


def _setup(tmp_path, manifest, queue=None):
    prompts_dir = tmp_path / "pull-request-review" / "dir1"
    prompts_dir.mkdir(parents=True)
    (prompts_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    if queue is not None:
        (prompts_dir / "queue.json").write_text(json.dumps(queue), encoding="utf-8")
    return prompts_dir


def _patches(tmp_path, values, argv):
    return (
        patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
        patch(f"{_MODULE}.get_value", side_effect=_state(values)),
        patch(f"{_MODULE}.resolve_repo_root", return_value=str(tmp_path)),
        patch(_HELPERS, return_value="dir1"),
        patch("sys.argv", argv),
    )


class TestTriageCommand:
    def test_writes_manifest_and_queue(self, tmp_path):
        manifest = {"files": [_row("a", "/src/auth/login.py"), _row("b", "/docs/x.md")]}
        queue = {"pending": [{"normalizedPath": "/src/auth/login.py"}, {"normalizedPath": "/docs/x.md"}]}
        prompts_dir = _setup(tmp_path, manifest, queue)
        values = {"pull_request_id": "1", "review.commit_hash_short": "abc"}
        p = _patches(tmp_path, values, ["cmd", "--pr", "1"])
        with p[0], p[1], p[2], p[3], p[4]:
            triage_command()
        written = json.loads((prompts_dir / "manifest.json").read_text(encoding="utf-8"))
        assert written["files"][0]["reviewDepth"] == "deep"
        queue_after = json.loads((prompts_dir / "queue.json").read_text(encoding="utf-8"))
        assert queue_after["pending"][0]["reviewDepth"] == "deep"
        assert queue_after["pending"][1]["reviewDepth"] == "light"

    def test_pr_from_state(self, tmp_path):
        manifest = {"files": [_row("a", "/src/a.py")]}
        _setup(tmp_path, manifest)
        values = {"pull_request_id": "9", "review.commit_hash_short": "abc"}
        p = _patches(tmp_path, values, ["cmd"])
        with p[0], p[1], p[2], p[3], p[4]:
            triage_command()
        written = json.loads((tmp_path / "pull-request-review" / "dir1" / "manifest.json").read_text("utf-8"))
        assert "triage" in written

    def test_dry_run_writes_nothing(self, tmp_path, capsys):
        manifest = {"files": [_row("a", "/src/a.py")]}
        prompts_dir = _setup(tmp_path, manifest)
        values = {"pull_request_id": "1", "review.commit_hash_short": "abc"}
        p = _patches(tmp_path, values, ["cmd", "--pr", "1", "--dry-run"])
        with p[0], p[1], p[2], p[3], p[4]:
            triage_command()
        reloaded = json.loads((prompts_dir / "manifest.json").read_text(encoding="utf-8"))
        assert "triage" not in reloaded
        assert "[dry-run]" in capsys.readouterr().out

    def test_demotions_reported(self, tmp_path, capsys):
        files = [_row(f"f{i}", f"/src/x{i}.py", changed=25) for i in range(11)]
        _setup(tmp_path, {"files": files})
        values = {"pull_request_id": "1", "review.commit_hash_short": "abc"}
        p = _patches(tmp_path, values, ["cmd", "--pr", "1"])
        with p[0], p[1], p[2], p[3], p[4]:
            triage_command()
        assert "Demoted" in capsys.readouterr().out

    def test_exit_when_no_pr(self, tmp_path):
        with patch(f"{_MODULE}.get_value", side_effect=_state({})), patch("sys.argv", ["cmd"]):
            with pytest.raises(SystemExit) as exc:
                triage_command()
            assert exc.value.code == 1

    def test_exit_when_pr_id_not_integer(self, tmp_path):
        values = {"pull_request_id": "not-a-number"}
        with (
            patch(f"{_MODULE}.get_value", side_effect=_state(values)),
            patch("sys.argv", ["cmd"]),
        ):
            with pytest.raises(SystemExit) as exc:
                triage_command()
            assert exc.value.code == 1

    def test_exit_when_manifest_missing(self, tmp_path):
        values = {"pull_request_id": "1", "review.commit_hash_short": "abc"}
        p = _patches(tmp_path, values, ["cmd", "--pr", "1"])
        with p[0], p[1], p[2], p[3], p[4]:
            with pytest.raises(SystemExit) as exc:
                triage_command()
            assert exc.value.code == 1

    def test_exit_when_manifest_invalid_json(self, tmp_path):
        prompts_dir = tmp_path / "pull-request-review" / "dir1"
        prompts_dir.mkdir(parents=True)
        (prompts_dir / "manifest.json").write_text("{ bad json", encoding="utf-8")
        values = {"pull_request_id": "1", "review.commit_hash_short": "abc"}
        p = _patches(tmp_path, values, ["cmd", "--pr", "1"])
        with p[0], p[1], p[2], p[3], p[4]:
            with pytest.raises(SystemExit) as exc:
                triage_command()
            assert exc.value.code == 1

    def test_exit_when_manifest_open_os_error(self, tmp_path):
        manifest = {"files": [_row("a", "/src/a.py")]}
        _setup(tmp_path, manifest)
        values = {"pull_request_id": "1", "review.commit_hash_short": "abc"}
        p = _patches(tmp_path, values, ["cmd", "--pr", "1"])
        with p[0], p[1], p[2], p[3], p[4], patch("builtins.open", side_effect=OSError("boom")):
            with pytest.raises(SystemExit) as exc:
                triage_command()
            assert exc.value.code == 1


class TestApplyDepthToQueue:
    def _manifest(self):
        return {"files": [{"normalizedPath": "/src/a.py", "reviewDepth": "deep", "reviewDepthReasons": ["r"]}]}

    def test_missing_queue_noop(self, tmp_path):
        _apply_depth_to_queue(tmp_path, self._manifest())  # no queue.json → no error

    def test_bad_json_noop(self, tmp_path):
        (tmp_path / "queue.json").write_text("{ bad", encoding="utf-8")
        _apply_depth_to_queue(tmp_path, self._manifest())

    def test_os_error_noop(self, tmp_path):
        (tmp_path / "queue.json").mkdir()
        _apply_depth_to_queue(tmp_path, self._manifest())

    def test_pending_not_list_noop(self, tmp_path):
        (tmp_path / "queue.json").write_text(json.dumps({"pending": {}}), encoding="utf-8")
        _apply_depth_to_queue(tmp_path, self._manifest())

    def test_updates_matching_entries_only(self, tmp_path):
        queue = {"pending": [None, {"normalizedPath": "/other"}, {"normalizedPath": "/src/a.py"}]}
        (tmp_path / "queue.json").write_text(json.dumps(queue), encoding="utf-8")
        _apply_depth_to_queue(tmp_path, self._manifest())
        result = json.loads((tmp_path / "queue.json").read_text(encoding="utf-8"))
        assert result["pending"][2]["reviewDepth"] == "deep"
        assert "reviewDepth" not in result["pending"][1]

    def test_write_os_error_noop(self, tmp_path, capsys):
        queue = {"pending": [{"normalizedPath": "/src/a.py"}]}
        queue_path = tmp_path / "queue.json"
        queue_path.write_text(json.dumps(queue), encoding="utf-8")
        real_open = open

        def _open(path, *args, **kwargs):
            mode = args[0] if args else kwargs.get("mode", "r")
            if Path(path) == queue_path and "w" in mode:
                raise OSError("disk full")
            return real_open(path, *args, **kwargs)

        with patch("builtins.open", side_effect=_open):
            _apply_depth_to_queue(tmp_path, self._manifest())
        assert "Warning" in capsys.readouterr().err

    def test_falls_back_to_pr_scoped_dir_when_hash_scoped_manifest_missing(self, tmp_path):
        # When manifest is absent in the hash-scoped directory (stale state), the command
        # should find and use the manifest in the PR-scoped fallback directory.
        manifest = {"files": [_row("a", "/src/a.py")]}
        fallback_dir = tmp_path / "pull-request-review" / "PR99"
        fallback_dir.mkdir(parents=True)
        (fallback_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        # State points at a stale hash-scoped directory that has NO manifest.json
        values = {"pull_request_id": "99", "review.commit_hash_short": "stalehash0099"}
        p = _patches(tmp_path, values, ["cmd", "--pr", "99"])
        with p[0], p[1], p[2], p[3], p[4]:
            triage_command()
        written = json.loads((fallback_dir / "manifest.json").read_text(encoding="utf-8"))
        assert "triage" in written

    def test_exit_when_manifest_missing_and_dir_name_equals_fallback(self, tmp_path):
        # When dir_name already equals "PR<id>" (resolve_review_artifact_dir_name returns the
        # PR-scoped name), the inner fallback branch (dir_name != fallback_dir) is False so
        # execution jumps directly to the error path at line 323.
        values = {"pull_request_id": "5"}
        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", side_effect=_state(values)),
            patch(f"{_MODULE}.resolve_repo_root", return_value=str(tmp_path)),
            patch(_HELPERS, return_value="PR5"),  # dir_name == fallback_dir == "PR5"
            patch("sys.argv", ["cmd", "--pr", "5"]),
        ):
            with pytest.raises(SystemExit) as exc:
                triage_command()
            assert exc.value.code == 1

    def test_delegates_state_missing_fallback_to_resolver(self, tmp_path):
        """When review.commit_hash_short is absent, delegate fallback to resolver (#1182)."""
        manifest = {"files": [_row("a", "/src/a.py")]}
        prompts_dir = tmp_path / "pull-request-review" / "2fea8cdf46c8"
        prompts_dir.mkdir(parents=True)
        (prompts_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        values = {"pull_request_id": "25553"}
        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", side_effect=_state(values)),
            patch(f"{_MODULE}.resolve_repo_root", return_value=str(tmp_path)),
            patch(_HELPERS, return_value="2fea8cdf46c8") as resolver,
            patch("sys.argv", ["cmd", "--pr", "25553"]),
        ):
            triage_command()
        resolver.assert_called_once_with(25553, None, backfill=True)
        written = json.loads((prompts_dir / "manifest.json").read_text(encoding="utf-8"))
        assert "triage" in written
