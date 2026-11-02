import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.adapters.pull_request_create import PullRequestCreateRequest, PullRequestCreateResult
from agentic_devtools.cli import pull_request_create


def _write_request_file(tmp_path: Path, payload: dict) -> str:
    request_file = tmp_path / "request.json"
    request_file.write_text(json.dumps(payload), encoding="utf-8")
    return str(request_file)


def test_run_request_snapshot_returns_failure_status(tmp_path: Path) -> None:
    request_file = _write_request_file(
        tmp_path,
        {"provider": "github", "source_branch": "feature", "title": "Title"},
    )
    with patch.object(
        pull_request_create,
        "dispatch_create_pull_request",
        return_value=PullRequestCreateResult(False, "github", "failed"),
    ) as dispatch:
        assert pull_request_create._run_request_snapshot(request_file) == 1

    assert dispatch.call_args.args[0] == PullRequestCreateRequest("github", "feature", "Title")


@pytest.mark.parametrize("previous_state_dir", [None, "previous-state-dir"])
def test_run_request_snapshot_dispatches_with_scheduled_state_dir(
    tmp_path: Path, monkeypatch, previous_state_dir: str | None
) -> None:
    request_file = _write_request_file(
        tmp_path,
        {"provider": "github", "source_branch": "feature", "title": "Title"},
    )
    if previous_state_dir is None:
        monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR", raising=False)
    else:
        monkeypatch.setenv("AGENTIC_DEVTOOLS_STATE_DIR", previous_state_dir)

    def _assert_scheduled_state_dir(_request) -> PullRequestCreateResult:
        assert os.environ["AGENTIC_DEVTOOLS_STATE_DIR"] == str(tmp_path)
        return PullRequestCreateResult(True, "github", "created")

    with patch.object(
        pull_request_create,
        "dispatch_create_pull_request",
        side_effect=_assert_scheduled_state_dir,
    ):
        assert pull_request_create._run_request_snapshot(request_file, str(tmp_path)) == 0

    if previous_state_dir is None:
        assert "AGENTIC_DEVTOOLS_STATE_DIR" not in os.environ
    else:
        assert os.environ["AGENTIC_DEVTOOLS_STATE_DIR"] == previous_state_dir


def test_run_request_snapshot_normalizes_reviewers_list(tmp_path: Path) -> None:
    request_file = _write_request_file(
        tmp_path,
        {
            "provider": "github",
            "source_branch": "feature",
            "title": "Title",
            "reviewers": ["alice", "bob"],
        },
    )
    with patch.object(
        pull_request_create,
        "dispatch_create_pull_request",
        return_value=PullRequestCreateResult(True, "github", "created"),
    ) as dispatch:
        status = pull_request_create._run_request_snapshot(request_file)

    assert status == 0
    assert dispatch.call_args.args[0].reviewers == ("alice", "bob")


def test_run_request_snapshot_reconstructs_full_persisted_payload(tmp_path: Path) -> None:
    request_file = _write_request_file(
        tmp_path,
        {
            "provider": "github",
            "source_branch": "feature",
            "title": "Title",
            "body": "Body",
            "target_branch": "develop",
            "draft": False,
            "reviewers": ["alice", "bob"],
            "dry_run": True,
        },
    )
    with patch.object(
        pull_request_create,
        "dispatch_create_pull_request",
        return_value=PullRequestCreateResult(True, "github", "dry_run"),
    ) as dispatch:
        status = pull_request_create._run_request_snapshot(request_file)

    assert status == 0
    assert dispatch.call_args.args[0] == PullRequestCreateRequest(
        "github",
        "feature",
        "Title",
        body="Body",
        target_branch="develop",
        draft=False,
        reviewers=("alice", "bob"),
        dry_run=True,
    )


def test_run_request_snapshot_deletes_request_file_after_reading(tmp_path: Path) -> None:
    request_file = _write_request_file(
        tmp_path,
        {"provider": "github", "source_branch": "feature", "title": "Title"},
    )
    with patch.object(
        pull_request_create,
        "dispatch_create_pull_request",
        return_value=PullRequestCreateResult(True, "github", "created"),
    ):
        pull_request_create._run_request_snapshot(request_file)

    assert not Path(request_file).exists()


def test_run_request_snapshot_deletes_request_file_even_when_request_validation_raises(tmp_path: Path) -> None:
    request_file = _write_request_file(
        tmp_path,
        {"provider": "github", "source_branch": "feature", "title": ""},
    )
    with pytest.raises(ValueError):
        pull_request_create._run_request_snapshot(request_file)

    assert not Path(request_file).exists()


def test_run_request_snapshot_rejects_non_dict_payload(tmp_path: Path) -> None:
    request_file = tmp_path / "request.json"
    request_file.write_text(json.dumps(["not", "a", "dict"]), encoding="utf-8")

    with pytest.raises(ValueError, match="JSON object"):
        pull_request_create._run_request_snapshot(str(request_file))


def test_run_request_snapshot_treats_cleanup_failure_as_best_effort(tmp_path: Path) -> None:
    """An OSError deleting the snapshot must not abort an already-read dispatch."""
    request_file = _write_request_file(
        tmp_path,
        {"provider": "github", "source_branch": "feature", "title": "Title"},
    )
    with (
        patch.object(
            pull_request_create,
            "dispatch_create_pull_request",
            return_value=PullRequestCreateResult(True, "github", "created"),
        ),
        patch.object(pull_request_create.Path, "unlink", side_effect=OSError("locked")),
    ):
        status = pull_request_create._run_request_snapshot(request_file)

    assert status == 0
