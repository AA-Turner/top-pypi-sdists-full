"""Tests for preserving the parent-first blocked comment and labels."""

import json
from unittest.mock import call, patch

from agentic_devtools.cli.speckit.resolve_hierarchy import _handle_parent_spec_missing


def test_posts_the_original_comment_and_updates_blocked_labels(tmp_path, monkeypatch) -> None:
    event = tmp_path / "event.json"
    event.write_text(json.dumps({"label": {"name": "speckit-trigger"}}), encoding="utf-8")
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event))
    monkeypatch.setenv("GITHUB_RUN_ID", "123")
    with patch(
        "agentic_devtools.cli.speckit.resolve_hierarchy._gh_api_call",
        side_effect=["comment", "removed", "removed", "label", "added"],
    ) as api_call:
        _handle_parent_spec_missing(issue_number=42, parent_number="10", repo="owner/repo", token="token")

    assert api_call.call_args_list[0].kwargs["body"]["body"] == "\n".join(
        [
            "✋ **SpecKit: Parent issue must be specked first**",
            "",
            "This issue (#42) is a sub-issue of #10, which has not been processed by SpecKit yet. "
            "Please add the `speckit` label to #10 first and wait for it to complete before "
            "re-triggering this issue.",
            "",
            "---",
            "_This comment was posted by the [SpecKit GitHub Action](https://github.com/owner/repo/actions/runs/123)._",
        ]
    )
    assert api_call.call_args_list[1].args[0].endswith("/labels/speckit-trigger")
    assert api_call.call_args_list[-1].kwargs["body"] == {"labels": ["speckit:blocked"]}


def test_blocked_label_side_effect_failures_are_nonfatal(tmp_path, monkeypatch, capsys) -> None:
    event = tmp_path / "bad-event.json"
    event.write_text("{", encoding="utf-8")
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event))
    monkeypatch.setenv("SPECKIT_COMMENT_ON_ISSUE", "false")
    errors = [
        RuntimeError("404 missing label"),
        RuntimeError("remove failed"),
        RuntimeError("404 label missing"),
        RuntimeError("422 already exists"),
        RuntimeError("add failed"),
    ]
    with patch("agentic_devtools.cli.speckit.resolve_hierarchy._gh_api_call", side_effect=errors) as api_call:
        _handle_parent_spec_missing(issue_number=42, parent_number="10", repo="owner/repo", token="")

    assert api_call.call_count == 5
    warning = capsys.readouterr().err
    assert "remove failed" in warning
    assert "add failed" in warning
    assert not any("/comments" in item.args[0] for item in api_call.call_args_list)


def test_creates_a_missing_blocked_label_and_warns_on_api_errors(monkeypatch, capsys) -> None:
    monkeypatch.delenv("GITHUB_EVENT_PATH", raising=False)
    monkeypatch.setenv("SPECKIT_COMMENT_ON_ISSUE", "false")
    with patch(
        "agentic_devtools.cli.speckit.resolve_hierarchy._gh_api_call",
        side_effect=[
            "removed",
            "removed",
            RuntimeError("404 missing speckit"),
            RuntimeError("creation failed"),
            RuntimeError("adding failed"),
        ],
    ) as api_call:
        _handle_parent_spec_missing(issue_number=42, parent_number="10", repo="owner/repo", token="token")

    assert api_call.call_args_list[0] == call(
        "/repos/owner/repo/issues/42/labels/speckit",
        method="DELETE",
        token="token",
    )
    warning = capsys.readouterr().err
    assert "failed to create speckit:blocked label" in warning
    assert "failed to add speckit:blocked label" in warning


def test_continues_after_comment_failure_and_skips_empty_trigger_label(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(tmp_path / "missing-event.json"))
    monkeypatch.setenv("GITHUB_RUN_ID", "123")
    monkeypatch.setenv("SPECKIT_TRIGGER_LABEL", "")
    with patch(
        "agentic_devtools.cli.speckit.resolve_hierarchy._gh_api_call",
        side_effect=[
            RuntimeError("comment failed"),
            "removed",
            "label",
            "added",
        ],
    ) as api_call:
        _handle_parent_spec_missing(issue_number=42, parent_number="10", repo="owner/repo", token="token")

    assert api_call.call_count == 4
    assert api_call.call_args_list[1].args[0].endswith("/labels/speckit%3Aprocessing")
    assert "failed to post parent-first comment" in capsys.readouterr().err


def test_warns_when_blocked_label_lookup_fails_for_another_reason(monkeypatch, capsys) -> None:
    monkeypatch.delenv("GITHUB_EVENT_PATH", raising=False)
    monkeypatch.setenv("SPECKIT_COMMENT_ON_ISSUE", "false")
    with patch(
        "agentic_devtools.cli.speckit.resolve_hierarchy._gh_api_call",
        side_effect=["removed", "removed", RuntimeError("permission denied"), "added"],
    ):
        _handle_parent_spec_missing(issue_number=42, parent_number="10", repo="owner/repo", token="token")
    assert "failed to get speckit:blocked label" in capsys.readouterr().err
