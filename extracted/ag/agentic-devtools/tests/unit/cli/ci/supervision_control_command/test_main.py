"""Tests for the main symbol."""

from __future__ import annotations

import json
from argparse import Namespace
from typing import Any
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci import supervision_control as control
from agentic_devtools.cli.ci import supervision_control_command as control_command
from agentic_devtools.cli.ci.comment_format import normalize_ai_pr_loop_comment
from agentic_devtools.cli.ci.supervision_control import (
    CONTROL_MARKER,
    Checkpoint,
    HoldReceipt,
    PRObservation,
    QuarantineReceipt,
)
from agentic_devtools.cli.ci.supervision_control_command import (
    LOOP_WORKFLOW_FILES,
    MAX_MANAGED_PRS,
    main,
)
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def _decode_control_comment(body: str) -> dict[str, Any]:
    normalized = normalize_ai_pr_loop_comment(body)
    assert normalized is not None
    return json.loads(normalized.split("\n", 1)[1])


@pytest.fixture(autouse=True)
def provide_supervision_lease(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AGDT_SUPERVISION_LEASE_ID", "test-lease")


def _observation(number: int, head: str, *labels: str) -> PRObservation:
    return PRObservation(number, head, frozenset(labels))


def _install_fake_provider(
    monkeypatch: pytest.MonkeyPatch,
    workflows: dict[str, bool],
    prs: dict[int, dict[str, Any]],
    comments: list[str],
    existing_labels: set[str] | None = None,
    comment_author: str = "automation",
) -> list[list[str]]:
    issue: dict[str, Any] | None = None
    writes: list[list[str]] = []
    repo_labels = existing_labels if existing_labels is not None else {"ai-pr-loop-ignore", "ai-pr-loop-supervised"}

    def run_gh(arguments: list[str]) -> object:
        if arguments[:2] == ["api", "user"]:
            return {"login": "automation"}
        if arguments[:2] == ["workflow", "list"]:
            return [
                {
                    "name": name,
                    "path": f".github/workflows/{name}",
                    "state": "active" if enabled else "disabled_manually",
                }
                for name, enabled in workflows.items()
            ]
        if arguments[:2] == ["issue", "list"]:
            if issue is None:
                return []
            if arguments[arguments.index("--author") + 1].casefold() != issue["author"]["login"].casefold():
                return []
            return [
                {
                    **issue,
                    "labels": [label for label in issue["labels"] if label["name"] in repo_labels],
                }
            ]
        if arguments[:2] == ["api", "graphql"]:
            return {
                "data": {
                    "repository": {
                        "issue": {
                            "comments": {
                                "nodes": [{"author": {"login": comment_author}, "body": body} for body in comments],
                                "pageInfo": {"hasPreviousPage": False, "hasNextPage": False, "endCursor": None},
                            }
                        }
                    }
                }
            }
        if arguments[:2] == ["pr", "view"]:
            number = int(arguments[2])
            return {
                **prs[number],
                "labels": [{"name": label} for label in prs[number]["labels"]],
            }
        if arguments[:2] == ["pr", "list"]:
            assert arguments[arguments.index("--limit") + 1] == str(MAX_MANAGED_PRS + 1)
            return []
        if arguments[:2] == ["label", "list"]:
            search = arguments[arguments.index("--search") + 1]
            assert arguments[arguments.index("--limit") + 1] == "1000"
            return [{"name": label} for label in repo_labels if search in label]
        raise AssertionError(f"unexpected provider query: {arguments}")

    def run_gh_text(arguments: list[str]) -> str:
        nonlocal issue
        writes.append(arguments)
        if arguments[:2] == ["label", "create"]:
            repo_labels.add(arguments[2])
            return arguments[2]
        if arguments[:2] == ["issue", "create"]:
            issue = {
                "number": 42,
                "body": CONTROL_MARKER,
                "author": {"login": "automation"},
                "labels": [{"name": "ai-pr-loop-supervised"}],
            }
            return "https://github.com/owner/repo/issues/42"
        if arguments[:2] == ["issue", "comment"]:
            comments.append(arguments[arguments.index("--body") + 1])
            return "https://github.com/owner/repo/issues/42#issuecomment-1"
        if arguments[:2] == ["pr", "edit"]:
            number = int(arguments[2])
            label = arguments[-1]
            pr_labels = set(prs[number]["labels"])
            if arguments[-2] == "--add-label":
                pr_labels.add(label)
            elif arguments[-2] == "--remove-label":
                pr_labels.discard(label)
            prs[number]["labels"] = sorted(pr_labels)
            return f"https://github.com/owner/repo/pull/{number}"
        if arguments[:2] == ["workflow", "disable"]:
            workflows[arguments[2]] = False
            return ""
        if arguments[:2] == ["workflow", "enable"]:
            workflows[arguments[2]] = True
            return ""
        raise AssertionError(f"unexpected provider mutation: {arguments}")

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh", run_gh)
    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh_text", run_gh_text)
    return writes


def test_main_runs_each_supported_operation_and_recovers_durable_receipts(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    comments: list[str] = []
    writes = _install_fake_provider(monkeypatch, workflows, prs, comments)

    assert main(["--repo", "owner/repo", "status"]) == 0
    assert json.loads(capsys.readouterr().out)["control_issue"]["number"] is None
    monkeypatch.setenv("GITHUB_RUN_ATTEMPT", "1")
    assert main(["--repo", "owner/repo", "ensure-labels"]) == 0
    ensured = json.loads(capsys.readouterr().out)
    ensure_receipt_count = len(comments)
    assert ensured["idempotent"] is False
    assert ensured["idempotency_key"].startswith("owner/repo:ensure-labels:v1:")
    assert ensured["receipt"]["control_issue"] == 42
    assert ensured["receipt"]["control_issue_created"] is True
    assert ensured["receipt"]["labels_created"] == []
    assert ensured["receipt"]["labels_reused"] == ["ai-pr-loop-ignore", "ai-pr-loop-supervised"]
    monkeypatch.setenv("GITHUB_RUN_ATTEMPT", "2")
    assert main(["--repo", "owner/repo", "ensure-labels"]) == 0
    ensured_retry = json.loads(capsys.readouterr().out)
    assert ensured_retry["idempotent"] is True
    assert ensured_retry["idempotency_key"] == ensured["idempotency_key"]
    assert ensured_retry["receipt"] == ensured["receipt"]
    assert len(comments) == ensure_receipt_count
    assert ensured_retry["receipt"]["control_issue_created"] is True

    quarantine_args = ["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"]
    assert main(quarantine_args) == 0
    quarantine = json.loads(capsys.readouterr().out)
    assert quarantine["receipt"]["ignore_added"] == [7]
    first_write_count = len(writes)
    assert main(quarantine_args) == 0
    assert json.loads(capsys.readouterr().out)["idempotent"] is True
    assert len(writes) == first_write_count

    receipt_arg = json.dumps(quarantine["receipt"])
    assert main(["--repo", "owner/repo", "restore-prs", "--receipt", receipt_arg]) == 0
    restored = json.loads(capsys.readouterr().out)
    assert restored["changed"] == [7]
    assert restored["idempotency_key"] == f"{quarantine['idempotency_key']}:restore"
    assert restored["receipt"]["quarantine_key"] == quarantine["idempotency_key"]
    assert main(["--repo", "owner/repo", "restore-prs", "--receipt", receipt_arg]) == 0
    restored_retry = json.loads(capsys.readouterr().out)
    assert restored_retry["idempotent"] is True
    assert restored_retry["receipt"] == restored["receipt"]
    assert restored_retry["changed"] == [7]
    prs[7]["labels"].append("ai-pr-loop-ignore")
    removal_count = sum(write[-2:] == ["--remove-label", "ai-pr-loop-ignore"] for write in writes)
    with pytest.raises(RuntimeError, match="completed restore-prs state read-back mismatch"):
        main(["--repo", "owner/repo", "restore-prs", "--receipt", receipt_arg])
    assert "ai-pr-loop-ignore" in prs[7]["labels"]
    assert sum(write[-2:] == ["--remove-label", "ai-pr-loop-ignore"] for write in writes) == removal_count
    prs[7]["headRefOid"] = "head-moved"
    with pytest.raises(RuntimeError, match="completed restore-prs state read-back mismatch"):
        main(["--repo", "owner/repo", "restore-prs", "--receipt", receipt_arg])

    assert main(["--repo", "owner/repo", "hold"]) == 0
    hold = json.loads(capsys.readouterr().out)
    assert set(hold["receipt"]["previous_states"].values()) == {True}
    assert main(["--repo", "owner/repo", "hold"]) == 0
    assert json.loads(capsys.readouterr().out)["idempotent"] is True
    assert main(["--repo", "owner/repo", "resume", "--receipt", json.dumps(hold["receipt"])]) == 0
    resumed = json.loads(capsys.readouterr().out)
    assert resumed["idempotency_key"] == "run-1:resume"
    assert set(resumed["states"].values()) == {True}
    assert resumed["receipt"]["states"] == hold["receipt"]["previous_states"]
    assert main(["--repo", "owner/repo", "resume", "--receipt", json.dumps(hold["receipt"])]) == 0
    resumed_retry = json.loads(capsys.readouterr().out)
    assert resumed_retry["idempotent"] is True
    assert resumed_retry["receipt"] == resumed["receipt"]
    workflows[LOOP_WORKFLOW_FILES[0]] = False
    with pytest.raises(RuntimeError, match="workflow state read-back mismatch"):
        main(["--repo", "owner/repo", "resume", "--receipt", json.dumps(hold["receipt"])])
    assert workflows[LOOP_WORKFLOW_FILES[0]] is False

    checkpoint_args = ["--repo", "owner/repo", "checkpoint", "--run-id", "100", "--payload", '{"step":1}']
    assert main(checkpoint_args) == 0
    checkpoint = json.loads(capsys.readouterr().out)
    comment_count = len(comments)
    assert main(checkpoint_args) == 0
    assert json.loads(capsys.readouterr().out)["idempotency_key"] == checkpoint["idempotency_key"]
    assert len(comments) == comment_count
    assert main(["--repo", "owner/repo", "status"]) == 0
    assert json.loads(capsys.readouterr().out)["control_issue"]["checkpoint"]["run_id"] == "100"


def test_local_resume_reads_actions_authored_hold_receipt(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    monkeypatch.setenv("GITHUB_RUN_ID", "actions-run")
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    comments: list[str] = []
    _install_fake_provider(
        monkeypatch,
        workflows,
        {},
        comments,
        comment_author="github-actions[bot]",
    )

    assert main(["--repo", "owner/repo", "ensure-labels"]) == 0
    capsys.readouterr()
    assert main(["--repo", "owner/repo", "hold"]) == 0
    hold = json.loads(capsys.readouterr().out)

    assert main(["--repo", "owner/repo", "resume", "--receipt", json.dumps(hold["receipt"])]) == 0
    resumed = json.loads(capsys.readouterr().out)
    assert resumed["idempotency_key"] == "actions-run:resume"
    assert resumed["receipt"]["hold_key"] == hold["idempotency_key"]


def test_main_checkpoint_bootstraps_supervised_label_on_a_fresh_repository(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    comments: list[str] = []
    writes = _install_fake_provider(monkeypatch, workflows, {}, comments, existing_labels=set())

    assert main(["--repo", "owner/repo", "checkpoint", "--run-id", "100", "--payload", '{"step":1}']) == 0
    capsys.readouterr()

    assert any(write[:3] == ["label", "create", "ai-pr-loop-supervised"] for write in writes)
    assert any(write[:2] == ["issue", "create"] for write in writes)


def test_main_does_not_republish_a_stale_checkpoint_after_newer_checkpoint_is_indexed(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    comments: list[str] = []
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    writes = _install_fake_provider(monkeypatch, workflows, {}, comments)
    older_args = ["--repo", "owner/repo", "checkpoint", "--run-id", "100", "--payload", '{"step":"old"}']
    newer_args = ["--repo", "owner/repo", "checkpoint", "--run-id", "200", "--payload", '{"step":"new"}']

    assert main(older_args) == 0
    older = json.loads(capsys.readouterr().out)
    assert main(newer_args) == 0
    capsys.readouterr()
    comments.remove(f"{older['checkpoint']}\n\n🤖 AI PR Loop ·")
    write_count = len(writes)

    with pytest.raises(RuntimeError, match="stale checkpoint"):
        main(older_args)

    assert len(writes) == write_count
    assert main(["--repo", "owner/repo", "status"]) == 0
    assert json.loads(capsys.readouterr().out)["control_issue"]["checkpoint"]["run_id"] == "200"


@pytest.mark.parametrize("run_id", ["healthy-run", "run-1", ""])
def test_main_rejects_non_decimal_checkpoint_run_ids_before_mutating_provider(
    run_id: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    comments: list[str] = []
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    writes = _install_fake_provider(monkeypatch, workflows, {}, comments)

    with pytest.raises(ValueError, match="decimal"):
        main(["--repo", "owner/repo", "checkpoint", "--run-id", run_id, "--payload", '{"step":"current"}'])

    assert writes == []
    assert comments == []


def test_main_fails_closed_when_legacy_checkpoint_run_id_cannot_be_ordered(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    comments: list[str] = []
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    _install_fake_provider(monkeypatch, workflows, {}, comments)
    assert main(["--repo", "owner/repo", "checkpoint", "--run-id", "100", "--payload", '{"step":"current"}']) == 0
    monkeypatch.setattr(
        control_command,
        "latest_valid_checkpoint",
        lambda *_args: Checkpoint("legacy-run", {}, "owner/repo"),
    )

    with pytest.raises(RuntimeError, match="cannot safely order"):
        main(["--repo", "owner/repo", "checkpoint", "--run-id", "101", "--payload", '{"step":"retry"}'])


def test_main_adds_supervised_label_before_ignore_label(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    ignore_label, supervised_label = next(
        (f"ignore-{index}", f"supervised-{index}")
        for index in range(10000)
        if list({f"ignore-{index}", f"supervised-{index}"})[0] == f"ignore-{index}"
    )
    monkeypatch.setattr(control_command, "IGNORE_LABEL", ignore_label)
    monkeypatch.setattr(control_command, "SUPERVISED_LABEL", supervised_label)
    monkeypatch.setattr(control, "IGNORE_LABEL", ignore_label)
    monkeypatch.setattr(control, "SUPERVISED_LABEL", supervised_label)
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    prs = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    writes = _install_fake_provider(monkeypatch, {}, prs, [])

    assert main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"]) == 0
    capsys.readouterr()

    added_labels = [write[-1] for write in writes if write[:2] == ["pr", "edit"] and write[-2] == "--add-label"]
    assert added_labels == [supervised_label, ignore_label]


def test_main_ensure_labels_only_creates_missing_labels_without_force(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-ensure")
    writes = _install_fake_provider(monkeypatch, {}, {}, [], existing_labels=set())

    assert main(["--repo", "owner/repo", "ensure-labels"]) == 0
    result = json.loads(capsys.readouterr().out)

    creations = [write for write in writes if write[:2] == ["label", "create"]]
    assert {write[2] for write in creations} == {"ai-pr-loop-ignore", "ai-pr-loop-supervised"}
    assert all("--force" not in write for write in creations)
    assert result["receipt"]["labels_created"] == ["ai-pr-loop-ignore", "ai-pr-loop-supervised"]
    assert result["receipt"]["labels_reused"] == []
    assert result["receipt"]["control_issue_created"] is True


def test_main_ensure_labels_records_a_reused_control_issue(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-ensure")
    _install_fake_provider(monkeypatch, {}, {}, [])
    assert main(["--repo", "owner/repo", "checkpoint", "--run-id", "99", "--payload", "{}"]) == 0
    capsys.readouterr()

    assert main(["--repo", "owner/repo", "ensure-labels"]) == 0

    result = json.loads(capsys.readouterr().out)
    assert result["receipt"]["control_issue"] == 42
    assert result["receipt"]["control_issue_created"] is False


def test_main_hold_rejects_workflow_enabled_after_receipt_recovery(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    initially_disabled = LOOP_WORKFLOW_FILES[0]
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    workflows[initially_disabled] = False
    writes = _install_fake_provider(monkeypatch, workflows, {}, [])
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")

    assert main(["--repo", "owner/repo", "hold"]) == 0
    workflows[initially_disabled] = True
    disabled_count = sum(write[:2] == ["workflow", "disable"] for write in writes)

    with pytest.raises(RuntimeError, match="workflow state mismatch"):
        main(["--repo", "owner/repo", "hold"])

    assert workflows[initially_disabled] is True
    assert sum(write[:2] == ["workflow", "disable"] for write in writes) == disabled_count


def test_main_hold_rejects_an_external_disable_before_its_first_mutation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    writes = _install_fake_provider(monkeypatch, workflows, {}, [])
    original_workflow_states = control_command._workflow_states
    read_count = 0
    externally_disabled = LOOP_WORKFLOW_FILES[0]

    def disable_workflow_between_receipt_and_reread(repo: str) -> dict[str, bool]:
        nonlocal read_count
        read_count += 1
        if read_count == 2:
            workflows[externally_disabled] = False
        return original_workflow_states(repo)

    monkeypatch.setattr(control_command, "_workflow_states", disable_workflow_between_receipt_and_reread)

    with pytest.raises(RuntimeError, match="workflow state mismatch"):
        main(["--repo", "owner/repo", "hold"])

    assert workflows[externally_disabled] is False
    assert not any(write[:2] == ["workflow", "disable"] for write in writes)


def test_main_hold_persists_progress_to_resume_a_partial_retry(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    comments: list[str] = []
    _install_fake_provider(monkeypatch, workflows, {}, comments)
    original_write = control_command._run_gh_text
    fail_once = True
    interrupted_workflow = LOOP_WORKFLOW_FILES[1]

    def fail_second_workflow_disable(arguments: list[str]) -> str:
        nonlocal fail_once
        if arguments[:2] == ["workflow", "disable"] and arguments[2] == interrupted_workflow and fail_once:
            fail_once = False
            raise RuntimeError("simulated partial hold failure")
        return original_write(arguments)

    monkeypatch.setattr(control_command, "_run_gh_text", fail_second_workflow_disable)
    with pytest.raises(RuntimeError, match="partial hold failure"):
        main(["--repo", "owner/repo", "hold"])

    progress = [
        _decode_control_comment(body)
        for body in comments
        if body.startswith(f"{control_command.OPERATION_RECEIPT_MARKER}\n")
        and "disabled_workflows" in _decode_control_comment(body)
    ]
    assert progress[-1]["disabled_workflows"] == [LOOP_WORKFLOW_FILES[0]]
    monkeypatch.setattr(control_command, "_run_gh_text", original_write)

    assert main(["--repo", "owner/repo", "hold"]) == 0
    hold = json.loads(capsys.readouterr().out)
    assert set(workflows.values()) == {False}
    assert set(progress[-1]["disabled_workflows"]).issubset(hold["receipt"]["previous_states"])

    assert main(["--repo", "owner/repo", "resume", "--receipt", json.dumps(hold["receipt"])]) == 0
    assert set(workflows.values()) == {True}


def test_main_hold_recovers_when_disable_succeeds_before_progress_is_persisted(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    comments: list[str] = []
    writes = _install_fake_provider(monkeypatch, workflows, {}, comments)
    original_write = control_command._run_gh_text
    ambiguous_workflow = LOOP_WORKFLOW_FILES[0]
    fail_once = True

    def disable_then_timeout(arguments: list[str]) -> str:
        nonlocal fail_once
        result = original_write(arguments)
        if arguments[:2] == ["workflow", "disable"] and arguments[2] == ambiguous_workflow and fail_once:
            fail_once = False
            raise RuntimeError("simulated timeout after workflow disable")
        return result

    monkeypatch.setattr(control_command, "_run_gh_text", disable_then_timeout)
    with pytest.raises(RuntimeError, match="timeout after workflow disable"):
        main(["--repo", "owner/repo", "hold"])

    monkeypatch.setattr(control_command, "_run_gh_text", original_write)
    assert main(["--repo", "owner/repo", "hold"]) == 0

    progress = [
        _decode_control_comment(body)
        for body in comments
        if body.startswith(f"{control_command.OPERATION_RECEIPT_MARKER}\n")
        and "disabled_workflows" in _decode_control_comment(body)
    ]
    hold = json.loads(capsys.readouterr().out)
    assert ambiguous_workflow in progress[-1]["disabled_workflows"]
    assert all(not enabled for enabled in workflows.values())
    assert {write[2] for write in writes if write[:2] == ["workflow", "disable"]} == set(LOOP_WORKFLOW_FILES)

    assert main(["--repo", "owner/repo", "resume", "--receipt", json.dumps(hold["receipt"])]) == 0
    assert set(workflows.values()) == {True}


def test_main_hold_fails_if_recovered_progress_cannot_be_verified(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    _install_fake_provider(monkeypatch, workflows, {}, [])
    original_write = control_command._run_gh_text
    ambiguous_workflow = LOOP_WORKFLOW_FILES[0]
    fail_once = True

    def disable_then_timeout(arguments: list[str]) -> str:
        nonlocal fail_once
        result = original_write(arguments)
        if arguments[:2] == ["workflow", "disable"] and arguments[2] == ambiguous_workflow and fail_once:
            fail_once = False
            raise RuntimeError("simulated timeout after workflow disable")
        return result

    monkeypatch.setattr(control_command, "_run_gh_text", disable_then_timeout)
    with pytest.raises(RuntimeError, match="timeout after workflow disable"):
        main(["--repo", "owner/repo", "hold"])

    monkeypatch.setattr(control_command, "_run_gh_text", original_write)
    original_find_progress = control_command.find_hold_progress
    calls = 0

    def fail_recovery_readback(*args: Any) -> tuple[frozenset[str], frozenset[str]]:
        nonlocal calls
        calls += 1
        if calls == 2:
            return frozenset(), frozenset()
        return original_find_progress(*args)

    monkeypatch.setattr(control_command, "find_hold_progress", fail_recovery_readback)
    with pytest.raises(RuntimeError, match="hold progress read-back mismatch"):
        main(["--repo", "owner/repo", "hold"])


@pytest.mark.parametrize("failure_call", [2, 3])
def test_main_hold_fails_if_persisted_progress_cannot_be_verified(
    monkeypatch: pytest.MonkeyPatch, failure_call: int
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    _install_fake_provider(monkeypatch, workflows, {}, [])
    original_find_progress = control_command.find_hold_progress
    calls = 0

    def fail_progress_readback(*args: Any) -> tuple[frozenset[str], frozenset[str]]:
        nonlocal calls
        calls += 1
        if calls == failure_call:
            return frozenset(), frozenset()
        return original_find_progress(*args)

    monkeypatch.setattr(control_command, "find_hold_progress", fail_progress_readback)

    with pytest.raises(RuntimeError, match="hold progress read-back mismatch"):
        main(["--repo", "owner/repo", "hold"])


def test_main_rejects_an_ensure_labels_receipt_for_another_control_issue(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-ensure")
    _install_fake_provider(monkeypatch, {}, {}, [])
    monkeypatch.setattr(control_command, "_find_control_issue", lambda _repo: None)
    monkeypatch.setattr(control_command, "_control_issue", lambda _repo: 42)
    monkeypatch.setattr(
        control_command,
        "get_or_store_operation_receipt",
        lambda *_args: (
            {
                "labels_created": [],
                "labels_reused": ["ai-pr-loop-ignore", "ai-pr-loop-supervised"],
                "control_issue": 43,
                "control_issue_created": True,
            },
            False,
        ),
    )

    with pytest.raises(RuntimeError, match="does not match the control issue"):
        main(["--repo", "owner/repo", "ensure-labels"])


def test_main_ensure_labels_recovers_its_receipt_after_a_partial_failure(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-ensure")
    writes = _install_fake_provider(monkeypatch, {}, {}, [], existing_labels=set())
    original_write = control_command._run_gh_text
    failed = False

    def fail_second_label_creation(arguments: list[str]) -> str:
        nonlocal failed
        if arguments[:2] == ["label", "create"] and arguments[2] == "ai-pr-loop-ignore" and not failed:
            failed = True
            raise RuntimeError("simulated partial ensure-labels failure")
        return original_write(arguments)

    monkeypatch.setattr(control_command, "_run_gh_text", fail_second_label_creation)
    with pytest.raises(RuntimeError, match="partial ensure-labels failure"):
        main(["--repo", "owner/repo", "ensure-labels"])
    monkeypatch.setattr(control_command, "_run_gh_text", original_write)

    assert main(["--repo", "owner/repo", "ensure-labels"]) == 0
    result = json.loads(capsys.readouterr().out)

    assert result["idempotent"] is False
    assert result["receipt"]["labels_created"] == ["ai-pr-loop-ignore", "ai-pr-loop-supervised"]
    assert result["receipt"]["labels_reused"] == []
    assert [write[2] for write in writes if write[:2] == ["label", "create"]] == [
        "ai-pr-loop-supervised",
        "ai-pr-loop-ignore",
    ]


def test_main_ensure_labels_bootstraps_the_control_issue_label_first(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-ensure")
    writes = _install_fake_provider(monkeypatch, {}, {}, [], existing_labels=set())

    assert main(["--repo", "owner/repo", "ensure-labels"]) == 0

    supervised_create = next(
        i for i, write in enumerate(writes) if write[:2] == ["label", "create"] and write[2] == "ai-pr-loop-supervised"
    )
    issue_create = next(i for i, write in enumerate(writes) if write[:2] == ["issue", "create"])
    assert supervised_create < issue_create


def test_main_quarantine_creates_and_verifies_a_missing_ignore_label(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-quarantine")
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    writes = _install_fake_provider(monkeypatch, {}, prs, [], existing_labels={"ai-pr-loop-supervised"})

    assert main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"]) == 0

    result = json.loads(capsys.readouterr().out)
    ignore_create = next(i for i, write in enumerate(writes) if write[:3] == ["label", "create", "ai-pr-loop-ignore"])
    pr_edit = next(i for i, write in enumerate(writes) if write[:2] == ["pr", "edit"])
    assert result["receipt"]["ignore_added"] == [7]
    assert ignore_create < pr_edit


def test_main_restore_prs_does_not_remove_a_label_after_incomplete_quarantine(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-incomplete-quarantine")
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    comments: list[str] = []
    writes = _install_fake_provider(monkeypatch, {}, prs, comments)
    original_write = control_command._run_gh_text

    def fail_ignore_label_write(arguments: list[str]) -> str:
        if arguments[:2] == ["pr", "edit"] and arguments[-2:] == ["--add-label", "ai-pr-loop-ignore"]:
            return ""
        return original_write(arguments)

    monkeypatch.setattr(control_command, "_run_gh_text", fail_ignore_label_write)
    with pytest.raises(RuntimeError, match="label read-back mismatch"):
        main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"])

    quarantine_record = next(
        _decode_control_comment(body)
        for body in comments
        if body.startswith(f"{control_command.OPERATION_RECEIPT_MARKER}\n")
        and _decode_control_comment(body).get("operation") == "quarantine"
    )
    assert "completed" not in quarantine_record

    monkeypatch.setattr(control_command, "_run_gh_text", original_write)
    prs[7]["labels"].append("ai-pr-loop-ignore")
    assert (
        main(
            [
                "--repo",
                "owner/repo",
                "restore-prs",
                "--receipt",
                json.dumps(quarantine_record["receipt"]),
            ]
        )
        == 0
    )

    assert json.loads(capsys.readouterr().out)["changed"] == []
    assert "ai-pr-loop-ignore" in prs[7]["labels"]
    assert not any(write[-2:] == ["--remove-label", "ai-pr-loop-ignore"] for write in writes)


def test_main_quarantine_rejects_missing_completion_receipt_readback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-completion-readback")
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    _install_fake_provider(monkeypatch, {}, prs, [])
    monkeypatch.setattr(control_command, "_write_control_issue_state_index", lambda *_args: [])

    with pytest.raises(RuntimeError, match="completion receipt read-back mismatch"):
        main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"])


def test_main_quarantine_revalidates_heads_before_label_mutations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-quarantine")
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    writes = _install_fake_provider(monkeypatch, {}, prs, [])
    original_observations = control_command._observations
    observation_count = 0

    def move_head_before_mutation(repo: str, expected: dict[int, str]) -> list[PRObservation]:
        nonlocal observation_count
        observation_count += 1
        if observation_count == 2:
            prs[7]["headRefOid"] = "head-moved"
        return original_observations(repo, expected)

    monkeypatch.setattr(control_command, "_observations", move_head_before_mutation)

    with pytest.raises(RuntimeError, match="head read-back mismatch"):
        main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"])

    assert observation_count == 2
    assert not any(write[:2] == ["pr", "edit"] for write in writes)
    assert prs[7]["labels"] == []


def test_main_quarantine_compensates_new_labels_when_head_changes_during_write(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-quarantine")
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    writes = _install_fake_provider(monkeypatch, {}, prs, [])
    original_write = control_command._run_gh_text

    def move_head_after_ignore_label_write(arguments: list[str]) -> str:
        result = original_write(arguments)
        if arguments[:2] == ["pr", "edit"] and arguments[-2:] == ["--add-label", "ai-pr-loop-ignore"]:
            prs[7]["headRefOid"] = "head-moved"
        return result

    monkeypatch.setattr(control_command, "_run_gh_text", move_head_after_ignore_label_write)

    with pytest.raises(RuntimeError, match="head read-back mismatch"):
        main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"])

    assert prs[7]["headRefOid"] == "head-moved"
    assert prs[7]["labels"] == []
    assert {tuple(write[-2:]) for write in writes if write[:2] == ["pr", "edit"]} == {
        ("--add-label", "ai-pr-loop-ignore"),
        ("--add-label", "ai-pr-loop-supervised"),
        ("--remove-label", "ai-pr-loop-ignore"),
        ("--remove-label", "ai-pr-loop-supervised"),
    }


def test_main_quarantine_does_not_compensate_when_only_label_readback_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-quarantine")
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    writes = _install_fake_provider(monkeypatch, {}, prs, [])
    original_write = control_command._run_gh_text

    def skip_ignore_label_write(arguments: list[str]) -> str:
        if arguments[:2] == ["pr", "edit"] and arguments[-2:] == ["--add-label", "ai-pr-loop-ignore"]:
            return ""
        return original_write(arguments)

    monkeypatch.setattr(control_command, "_run_gh_text", skip_ignore_label_write)

    with pytest.raises(RuntimeError, match="label read-back mismatch"):
        main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"])

    assert prs[7]["headRefOid"] == "head-7"
    assert prs[7]["labels"] == ["ai-pr-loop-supervised"]
    assert not any(write[-2:] == ["--remove-label", "ai-pr-loop-supervised"] for write in writes)


def test_main_quarantine_skips_compensation_when_moved_head_has_no_new_labels(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-quarantine")
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    writes = _install_fake_provider(monkeypatch, {}, prs, [])
    original_write = control_command._run_gh_text

    def move_head_and_clear_labels(arguments: list[str]) -> str:
        result = original_write(arguments)
        if arguments[:2] == ["pr", "edit"] and arguments[-2:] == ["--add-label", "ai-pr-loop-ignore"]:
            prs[7]["headRefOid"] = "head-moved"
            prs[7]["labels"].clear()
        return result

    monkeypatch.setattr(control_command, "_run_gh_text", move_head_and_clear_labels)

    with pytest.raises(RuntimeError, match="head read-back mismatch"):
        main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"])

    assert prs[7]["labels"] == []
    assert not any(write[-2:] == ["--remove-label", "ai-pr-loop-ignore"] for write in writes)


def test_main_quarantine_skips_compensation_if_head_returns_to_expected_before_removal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-quarantine")
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    writes = _install_fake_provider(monkeypatch, {}, prs, [])
    original_observations = control_command._observations
    observation_count = 0

    def return_to_expected_head(repo: str, expected: dict[int, str]) -> list[PRObservation]:
        nonlocal observation_count
        observation_count += 1
        observations = original_observations(repo, expected)
        if observation_count == 3:
            prs[7]["headRefOid"] = "head-7"
        return observations

    original_write = control_command._run_gh_text

    def move_head_after_ignore_label_write(arguments: list[str]) -> str:
        result = original_write(arguments)
        if arguments[:2] == ["pr", "edit"] and arguments[-2:] == ["--add-label", "ai-pr-loop-ignore"]:
            prs[7]["headRefOid"] = "head-moved"
        return result

    monkeypatch.setattr(control_command, "_observations", return_to_expected_head)
    monkeypatch.setattr(control_command, "_run_gh_text", move_head_after_ignore_label_write)

    with pytest.raises(RuntimeError, match="head read-back mismatch"):
        main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"])

    assert observation_count == 4
    assert prs[7]["headRefOid"] == "head-7"
    assert "ai-pr-loop-ignore" in prs[7]["labels"]
    assert not any(write[-2:] == ["--remove-label", "ai-pr-loop-ignore"] for write in writes)


def test_main_quarantine_reports_failed_label_compensation_readback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-quarantine")
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    writes = _install_fake_provider(monkeypatch, {}, prs, [])
    original_write = control_command._run_gh_text

    def fail_compensation(arguments: list[str]) -> str:
        if arguments[:2] == ["pr", "edit"] and arguments[-2:] == ["--remove-label", "ai-pr-loop-ignore"]:
            writes.append(arguments)
            return ""
        result = original_write(arguments)
        if arguments[:2] == ["pr", "edit"] and arguments[-2:] == ["--add-label", "ai-pr-loop-ignore"]:
            prs[7]["headRefOid"] = "head-moved"
        return result

    monkeypatch.setattr(control_command, "_run_gh_text", fail_compensation)

    with pytest.raises(RuntimeError, match="compensation read-back mismatch"):
        main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"])

    assert "ai-pr-loop-ignore" in prs[7]["labels"]
    assert any(write[-2:] == ["--remove-label", "ai-pr-loop-ignore"] for write in writes)


@pytest.mark.parametrize("missing_label", ["ai-pr-loop-ignore", "ai-pr-loop-supervised"])
def test_main_ensure_labels_records_a_new_receipt_when_a_label_needs_repair(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], missing_label: str
) -> None:
    labels = {"ai-pr-loop-ignore", "ai-pr-loop-supervised"}
    writes = _install_fake_provider(monkeypatch, {}, {}, [], existing_labels=labels)
    monkeypatch.setenv("GITHUB_RUN_ID", "run-initial")
    assert main(["--repo", "owner/repo", "ensure-labels"]) == 0
    initial = json.loads(capsys.readouterr().out)

    labels.remove(missing_label)
    expected_reused = sorted(labels)
    monkeypatch.setenv("GITHUB_RUN_ID", "run-repair")
    assert main(["--repo", "owner/repo", "ensure-labels"]) == 0
    repaired = json.loads(capsys.readouterr().out)

    assert repaired["idempotent"] is False
    assert repaired["idempotency_key"] != initial["idempotency_key"]
    assert repaired["receipt"]["labels_created"] == [missing_label]
    assert repaired["receipt"]["labels_reused"] == expected_reused
    assert sum(write[:2] == ["issue", "create"] for write in writes) == 1


def test_main_restore_prs_preserves_a_superseding_quarantine_label(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-A")
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    writes = _install_fake_provider(monkeypatch, {}, prs, [])
    assert main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"]) == 0
    old_receipt = json.loads(capsys.readouterr().out)["receipt"]

    prs[7]["labels"].remove("ai-pr-loop-ignore")
    monkeypatch.setenv("GITHUB_RUN_ID", "run-B")
    assert main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"]) == 0
    capsys.readouterr()
    removal_count = sum(write[-2:] == ["--remove-label", "ai-pr-loop-ignore"] for write in writes)

    assert main(["--repo", "owner/repo", "restore-prs", "--receipt", json.dumps(old_receipt)]) == 0
    assert json.loads(capsys.readouterr().out)["changed"] == []

    assert sum(write[-2:] == ["--remove-label", "ai-pr-loop-ignore"] for write in writes) == removal_count
    assert "ai-pr-loop-ignore" in prs[7]["labels"]


def test_main_restore_prs_allows_a_new_quarantine_for_an_unrelated_pr(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-A")
    prs: dict[int, dict[str, Any]] = {
        7: {"number": 7, "headRefOid": "head-7", "labels": []},
        8: {"number": 8, "headRefOid": "head-8", "labels": []},
    }
    _install_fake_provider(monkeypatch, {}, prs, [])
    assert main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"]) == 0
    old_receipt = json.loads(capsys.readouterr().out)["receipt"]

    monkeypatch.setenv("GITHUB_RUN_ID", "run-B")
    assert main(["--repo", "owner/repo", "quarantine", "--pr", "8=head-8"]) == 0
    capsys.readouterr()

    assert main(["--repo", "owner/repo", "restore-prs", "--receipt", json.dumps(old_receipt)]) == 0

    assert "ai-pr-loop-ignore" not in prs[7]["labels"]
    assert "ai-pr-loop-ignore" in prs[8]["labels"]


def test_main_restore_prs_recovers_unaffected_members_after_quarantine_supersession(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-A")
    prs: dict[int, dict[str, Any]] = {
        7: {"number": 7, "headRefOid": "head-7", "labels": []},
        8: {"number": 8, "headRefOid": "head-8", "labels": []},
    }
    writes = _install_fake_provider(monkeypatch, {}, prs, [])
    assert main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7", "--pr", "8=head-8"]) == 0
    receipt_a = json.loads(capsys.readouterr().out)["receipt"]
    restore_a = ["--repo", "owner/repo", "restore-prs", "--receipt", json.dumps(receipt_a)]

    original_write = control_command._run_gh_text

    def fail_restoring_pr_8(arguments: list[str]) -> str:
        if arguments[:3] == ["pr", "edit", "8"] and arguments[-2:] == ["--remove-label", "ai-pr-loop-ignore"]:
            raise RuntimeError("simulated partial restore failure")
        return original_write(arguments)

    monkeypatch.setattr(control_command, "_run_gh_text", fail_restoring_pr_8)
    with pytest.raises(RuntimeError, match="partial restore failure"):
        main(restore_a)
    assert "ai-pr-loop-ignore" not in prs[7]["labels"]
    assert "ai-pr-loop-ignore" in prs[8]["labels"]

    monkeypatch.setattr(control_command, "_run_gh_text", original_write)
    monkeypatch.setenv("GITHUB_RUN_ID", "run-B")
    assert main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"]) == 0
    receipt_b = json.loads(capsys.readouterr().out)["receipt"]
    assert "ai-pr-loop-ignore" in prs[7]["labels"]

    assert main(restore_a) == 0
    restored_a = json.loads(capsys.readouterr().out)
    assert restored_a["changed"] == [7, 8]
    assert "ai-pr-loop-ignore" in prs[7]["labels"]
    assert "ai-pr-loop-ignore" not in prs[8]["labels"]

    assert main(["--repo", "owner/repo", "restore-prs", "--receipt", json.dumps(receipt_b)]) == 0
    capsys.readouterr()
    assert "ai-pr-loop-ignore" not in prs[7]["labels"]
    assert main(restore_a) == 0
    assert json.loads(capsys.readouterr().out)["idempotent"] is True
    assert sum(write[-2:] == ["--remove-label", "ai-pr-loop-ignore"] for write in writes) == 3


def test_main_no_op_quarantine_does_not_supersede_the_ignore_label_owner(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    _install_fake_provider(monkeypatch, {}, prs, [])
    monkeypatch.setenv("GITHUB_RUN_ID", "run-owner")
    assert main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"]) == 0
    owner_receipt = json.loads(capsys.readouterr().out)["receipt"]

    monkeypatch.setenv("GITHUB_RUN_ID", "run-no-op")
    assert main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"]) == 0
    no_op_receipt = json.loads(capsys.readouterr().out)["receipt"]
    assert no_op_receipt["ignore_added"] == []

    assert main(["--repo", "owner/repo", "restore-prs", "--receipt", json.dumps(owner_receipt)]) == 0
    assert "ai-pr-loop-ignore" not in prs[7]["labels"]
    assert main(["--repo", "owner/repo", "restore-prs", "--receipt", json.dumps(no_op_receipt)]) == 0
    assert "ai-pr-loop-ignore" not in prs[7]["labels"]


def test_main_quarantine_rejects_replay_after_restore(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    writes = _install_fake_provider(monkeypatch, {}, prs, [])
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    quarantine_args = ["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"]

    assert main(quarantine_args) == 0
    receipt = json.loads(capsys.readouterr().out)["receipt"]
    assert main(["--repo", "owner/repo", "restore-prs", "--receipt", json.dumps(receipt)]) == 0
    assert "ai-pr-loop-ignore" not in prs[7]["labels"]
    add_label_writes = sum(write[-2:] == ["--add-label", "ai-pr-loop-ignore"] for write in writes)

    with pytest.raises(RuntimeError, match="already been restored"):
        main(quarantine_args)

    assert "ai-pr-loop-ignore" not in prs[7]["labels"]
    assert sum(write[-2:] == ["--add-label", "ai-pr-loop-ignore"] for write in writes) == add_label_writes


def test_main_quarantine_rejects_a_completion_receipt_for_another_generation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    monkeypatch.setattr(control_command, "_control_issue", lambda _repo: 42)
    monkeypatch.setattr(control_command, "_observations", lambda _repo, _expected: [_observation(7, "head-7")])
    monkeypatch.setattr(control_command, "_run_gh", lambda _arguments: {"login": "automation"})
    monkeypatch.setattr(control_command, "_read_control_issue_comments", lambda *_args: [])
    monkeypatch.setattr(
        control_command,
        "find_completed_operation_receipt",
        lambda *_args: {"run_id": "other-run", "quarantine_key": "other-key", "changed": [7]},
    )

    with pytest.raises(RuntimeError, match="does not match the quarantine receipt"):
        main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"])


def test_main_resume_rejects_a_superseded_hold_receipt(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    _install_fake_provider(monkeypatch, workflows, {}, [])
    monkeypatch.setenv("GITHUB_RUN_ID", "run-A")
    assert main(["--repo", "owner/repo", "hold"]) == 0
    old_receipt = json.loads(capsys.readouterr().out)["receipt"]

    monkeypatch.setenv("GITHUB_RUN_ID", "run-B")
    with pytest.raises(RuntimeError, match="unresolved hold"):
        main(["--repo", "owner/repo", "hold"])

    monkeypatch.setenv("GITHUB_RUN_ID", "run-A")
    assert main(["--repo", "owner/repo", "resume", "--receipt", json.dumps(old_receipt)]) == 0

    assert set(workflows.values()) == {True}


def test_main_hold_rejects_replay_after_resume(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    writes = _install_fake_provider(monkeypatch, workflows, {}, [])
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")

    assert main(["--repo", "owner/repo", "hold"]) == 0
    receipt = json.loads(capsys.readouterr().out)["receipt"]
    assert main(["--repo", "owner/repo", "resume", "--receipt", json.dumps(receipt)]) == 0
    assert set(workflows.values()) == {True}
    disable_writes = sum(write[:2] == ["workflow", "disable"] for write in writes)

    with pytest.raises(RuntimeError, match="already been resumed"):
        main(["--repo", "owner/repo", "hold"])

    assert set(workflows.values()) == {True}
    assert sum(write[:2] == ["workflow", "disable"] for write in writes) == disable_writes


def test_main_allows_a_new_hold_after_the_previous_hold_is_resumed(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    _install_fake_provider(monkeypatch, workflows, {}, [])
    monkeypatch.setenv("GITHUB_RUN_ID", "run-A")
    assert main(["--repo", "owner/repo", "hold"]) == 0
    old_receipt = json.loads(capsys.readouterr().out)["receipt"]
    assert main(["--repo", "owner/repo", "resume", "--receipt", json.dumps(old_receipt)]) == 0
    capsys.readouterr()

    monkeypatch.setenv("GITHUB_RUN_ID", "run-B")
    assert main(["--repo", "owner/repo", "hold"]) == 0

    assert set(workflows.values()) == {False}


def test_main_rejects_an_unexpected_active_hold_receipt_type(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-new")
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._workflow_states",
        lambda _repo: dict.fromkeys(LOOP_WORKFLOW_FILES, True),
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._control_issue",
        lambda _repo: 42,
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh",
        lambda _arguments: {"login": "automation"},
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._read_control_issue_comments",
        lambda *_args: [],
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command.find_latest_operation_receipt_key",
        lambda *_args: "run-old:hold",
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command.find_operation_receipt",
        lambda *_args: {},
    )

    with pytest.raises(RuntimeError, match="active hold receipt is malformed"):
        main(["--repo", "owner/repo", "hold"])


def test_main_resume_rejects_a_receipt_superseded_in_existing_history(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    comments: list[str] = []
    _install_fake_provider(monkeypatch, workflows, {}, comments)
    monkeypatch.setenv("GITHUB_RUN_ID", "run-A")
    assert main(["--repo", "owner/repo", "hold"]) == 0
    old_receipt = json.loads(capsys.readouterr().out)["receipt"]
    newer_receipt = HoldReceipt("run-B", tuple(LOOP_WORKFLOW_FILES), dict.fromkeys(LOOP_WORKFLOW_FILES, True))
    comments.append(
        f"{control_command.OPERATION_RECEIPT_MARKER}\n"
        + json.dumps(
            {
                "idempotency_key": "run-B:hold",
                "operation": "hold",
                "receipt": control_command.hold_receipt_to_json(newer_receipt),
            }
        )
    )

    with pytest.raises(RuntimeError, match="active hold generation"):
        main(["--repo", "owner/repo", "resume", "--receipt", json.dumps(old_receipt)])

    assert set(workflows.values()) == {False}


def test_main_status_fails_closed_on_incomplete_workflow_or_truncated_pr_list(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    incomplete = dict(workflows)
    incomplete.pop(LOOP_WORKFLOW_FILES[0])
    _install_fake_provider(monkeypatch, incomplete, {}, [])
    with pytest.raises(RuntimeError, match="incomplete workflow evidence"):
        main(["--repo", "owner/repo", "status"])

    prs = {
        number: {"number": number, "headRefOid": f"head-{number}", "labels": []}
        for number in range(1, MAX_MANAGED_PRS + 2)
    }
    _install_fake_provider(monkeypatch, workflows, prs, [])

    def read_provider(arguments: list[str]) -> object:
        if arguments[:2] == ["api", "user"]:
            return {"login": "automation"}
        if arguments[:2] == ["issue", "list"]:
            return []
        if arguments[:2] == ["api", "graphql"]:
            return {
                "data": {
                    "repository": {
                        "issue": {
                            "comments": {
                                "nodes": [],
                                "pageInfo": {"hasPreviousPage": False, "hasNextPage": False, "endCursor": None},
                            }
                        }
                    }
                }
            }
        if arguments[:2] == ["workflow", "list"]:
            return [
                {
                    "name": name,
                    "path": f".github/workflows/{name}",
                    "state": "active",
                }
                for name in workflows
            ]
        return [
            {"number": number, "headRefOid": f"head-{number}", "labels": []} for number in range(1, MAX_MANAGED_PRS + 2)
        ]

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh", read_provider)
    with pytest.raises(RuntimeError, match="status limit"):
        main(["--repo", "owner/repo", "status"])


@pytest.mark.parametrize("payload", ["[]", "null", '"scalar"'])
def test_main_rejects_non_object_checkpoint_payload_before_provider_write(
    monkeypatch: pytest.MonkeyPatch, payload: str
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._control_issue",
        lambda _repo: pytest.fail("invalid payload must be rejected before creating the control issue"),
    )

    with pytest.raises(ValueError, match="payload must be a JSON object"):
        main(["--repo", "owner/repo", "checkpoint", "--run-id", "1", "--payload", payload])


def test_main_rejects_checkpoint_that_cannot_fit_in_state_index_before_provider_write(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    comments: list[str] = []
    writes = _install_fake_provider(monkeypatch, {}, {}, comments)
    payload = json.dumps({"data": '"' * 24_000})

    with pytest.raises(RuntimeError, match="control state index entry exceeds the comment size limit"):
        main(["--repo", "owner/repo", "checkpoint", "--run-id", "1", "--payload", payload])

    assert writes == []
    assert comments == []


def test_main_rejects_missing_authenticated_identity_for_control_comments(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        control_command,
        "_control_issue",
        lambda _repo: 42,
    )
    monkeypatch.setattr(control_command, "_run_gh", lambda _arguments: {})

    with pytest.raises(RuntimeError, match="authenticated GitHub identity"):
        main(["--repo", "owner/repo", "checkpoint", "--run-id", "1", "--payload", "{}"])


@pytest.mark.parametrize(
    ("operation", "receipt", "message"),
    [
        ("restore-prs", {"run_id": "run-1", "changed": [], "heads": {}, "ignore_added": []}, "quarantine"),
        (
            "resume",
            {"run_id": "run-1", "changed_workflows": [], "previous_states": dict.fromkeys(LOOP_WORKFLOW_FILES, False)},
            "hold",
        ),
    ],
)
def test_main_requires_a_trusted_control_issue_before_restoring(
    monkeypatch: pytest.MonkeyPatch,
    operation: str,
    receipt: dict[str, object],
    message: str,
) -> None:
    monkeypatch.setattr(control_command, "_find_control_issue", lambda _repo: None)

    with pytest.raises(RuntimeError, match=f"no trusted supervision control issue.*{message} receipt"):
        main(["--repo", "owner/repo", operation, "--receipt", json.dumps(receipt)])


def test_main_quarantine_rejects_a_changed_head_during_read_back(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    comments: list[str] = []
    _install_fake_provider(monkeypatch, workflows, prs, comments)
    original = prs[7]["headRefOid"]
    reads = 0

    def read_pr(arguments: list[str]) -> object:
        nonlocal reads
        if arguments[:2] == ["api", "user"]:
            return {"login": "automation"}
        if arguments[:2] == ["label", "list"]:
            return [{"name": "ai-pr-loop-ignore"}, {"name": "ai-pr-loop-supervised"}]
        if arguments[:2] == ["workflow", "list"]:
            return [{"name": name, "path": f".github/workflows/{name}", "state": "active"} for name in workflows]
        if arguments[:2] == ["issue", "list"]:
            if arguments[arguments.index("--author") + 1] != "automation":
                return []
            return [
                {
                    "number": 42,
                    "body": CONTROL_MARKER,
                    "author": {"login": "automation"},
                    "labels": [{"name": "ai-pr-loop-supervised"}],
                }
            ]
        if arguments[:2] == ["api", "graphql"]:
            return {
                "data": {
                    "repository": {
                        "issue": {
                            "comments": {
                                "nodes": [{"author": {"login": "automation"}, "body": body} for body in comments],
                                "pageInfo": {"hasPreviousPage": False, "hasNextPage": False, "endCursor": None},
                            }
                        }
                    }
                }
            }
        if arguments[:2] == ["pr", "view"]:
            reads += 1
            return {
                **prs[7],
                "headRefOid": original if reads == 1 else "moved",
                "labels": [{"name": label} for label in prs[7]["labels"]],
            }
        raise AssertionError(arguments)

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh", read_pr)
    with pytest.raises(RuntimeError, match="head read-back mismatch"):
        main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"])


def test_main_resume_does_not_enable_workflows_that_were_previously_disabled(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, False)
    writes = _install_fake_provider(monkeypatch, workflows, {}, [])
    assert main(["--repo", "owner/repo", "hold"]) == 0
    receipt = json.loads(capsys.readouterr().out)["receipt"]

    assert main(["--repo", "owner/repo", "resume", "--receipt", json.dumps(receipt)]) == 0

    assert json.loads(capsys.readouterr().out)["states"] == dict.fromkeys(LOOP_WORKFLOW_FILES, False)
    assert not any(write[:2] == ["workflow", "enable"] for write in writes)


def test_main_resume_rejects_incomplete_workflow_receipt_before_provider_reads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    receipt = {
        "run_id": "run-incomplete",
        "changed_workflows": ["ai-pr-loop.yml"],
        "previous_states": {"ai-pr-loop.yml": True},
    }
    monkeypatch.setattr(
        control_command,
        "_find_control_issue",
        lambda _repo: pytest.fail("incomplete receipts must fail before provider reads"),
    )

    with pytest.raises(RuntimeError, match="complete workflow set"):
        main(["--repo", "owner/repo", "resume", "--receipt", json.dumps(receipt)])


def test_main_resume_completes_after_a_partial_enable_failure(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    writes = _install_fake_provider(monkeypatch, workflows, {}, [])
    assert main(["--repo", "owner/repo", "hold"]) == 0
    receipt = json.loads(capsys.readouterr().out)["receipt"]

    original_write = control_command._run_gh_text
    enabled = 0

    def fail_after_first_enable(arguments: list[str]) -> str:
        nonlocal enabled
        if arguments[:2] == ["workflow", "enable"]:
            enabled += 1
            if enabled == 2:
                raise RuntimeError("simulated partial resume failure")
        return original_write(arguments)

    monkeypatch.setattr(control_command, "_run_gh_text", fail_after_first_enable)
    resume_args = ["--repo", "owner/repo", "resume", "--receipt", json.dumps(receipt)]
    with pytest.raises(RuntimeError, match="partial resume failure"):
        main(resume_args)
    monkeypatch.setattr(control_command, "_run_gh_text", original_write)

    assert main(resume_args) == 0

    resumed = json.loads(capsys.readouterr().out)
    assert resumed["idempotent"] is False
    assert resumed["states"] == dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    assert sum(write[:2] == ["workflow", "enable"] for write in writes) == len(LOOP_WORKFLOW_FILES)


def test_main_restore_prs_recovers_its_receipt_after_a_partial_failure(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-restore")
    prs: dict[int, dict[str, Any]] = {
        number: {"number": number, "headRefOid": f"head-{number}", "labels": []} for number in (7, 8)
    }
    writes = _install_fake_provider(monkeypatch, {}, prs, [])
    quarantine_args = ["--repo", "owner/repo", "quarantine", "--pr", "7=head-7", "--pr", "8=head-8"]
    assert main(quarantine_args) == 0
    quarantine = json.loads(capsys.readouterr().out)
    receipt_arg = json.dumps(quarantine["receipt"])

    original_write = control_command._run_gh_text
    restored = 0

    def fail_after_first_restore(arguments: list[str]) -> str:
        nonlocal restored
        if arguments[:2] == ["pr", "edit"] and arguments[-2:] == ["--remove-label", "ai-pr-loop-ignore"]:
            restored += 1
            if restored == 2:
                raise RuntimeError("simulated partial restore failure")
        return original_write(arguments)

    monkeypatch.setattr(control_command, "_run_gh_text", fail_after_first_restore)
    with pytest.raises(RuntimeError, match="partial restore failure"):
        main(["--repo", "owner/repo", "restore-prs", "--receipt", receipt_arg])
    monkeypatch.setattr(control_command, "_run_gh_text", original_write)

    assert main(["--repo", "owner/repo", "restore-prs", "--receipt", receipt_arg]) == 0
    result = json.loads(capsys.readouterr().out)

    assert result["idempotent"] is False
    assert result["idempotency_key"] == f"{quarantine['idempotency_key']}:restore"
    assert result["receipt"]["changed"] == [7, 8]
    assert all("ai-pr-loop-ignore" not in pr["labels"] for pr in prs.values())
    assert sum(write[-2:] == ["--remove-label", "ai-pr-loop-ignore"] for write in writes) == 2


def test_main_restore_prs_reapplies_ignore_label_after_head_changes_during_restore(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-head-race")
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    writes = _install_fake_provider(monkeypatch, {}, prs, [])
    assert main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"]) == 0
    quarantine = json.loads(capsys.readouterr().out)
    original_write = control_command._run_gh_text

    def push_during_restore(arguments: list[str]) -> str:
        result = original_write(arguments)
        if arguments[:2] == ["pr", "edit"] and arguments[-2:] == ["--remove-label", "ai-pr-loop-ignore"]:
            prs[7]["headRefOid"] = "head-moved"
        return result

    monkeypatch.setattr(control_command, "_run_gh_text", push_during_restore)

    with pytest.raises(RuntimeError, match="head read-back mismatch"):
        main(["--repo", "owner/repo", "restore-prs", "--receipt", json.dumps(quarantine["receipt"])])

    assert "ai-pr-loop-ignore" in prs[7]["labels"]
    assert any(write[:2] == ["pr", "edit"] and write[-2:] == ["--add-label", "ai-pr-loop-ignore"] for write in writes)


def test_main_restore_prs_reapplies_ignore_label_after_rate_limited_readback(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-rate-limited-readback")
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    original_run_gh = control_command._run_gh
    writes = _install_fake_provider(monkeypatch, {}, prs, [])
    assert main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"]) == 0
    quarantine = json.loads(capsys.readouterr().out)
    fake_run_gh = control_command._run_gh
    pr_view_calls = 0

    def rate_limit_restore_readback(arguments: list[str]) -> object:
        nonlocal pr_view_calls
        if arguments[:2] == ["pr", "view"]:
            pr_view_calls += 1
            if pr_view_calls == 2:
                return original_run_gh(arguments)
        return fake_run_gh(arguments)

    monkeypatch.setattr(control_command, "_run_gh", rate_limit_restore_readback)
    with (
        patch(
            "agentic_devtools.cli.ci.github_provider._run_readonly_gh_command",
            side_effect=ProviderRateLimitError(provider="github", credential_identity="reader"),
        ),
        pytest.raises(RuntimeError, match="GitHub CLI operation failed"),
    ):
        main(["--repo", "owner/repo", "restore-prs", "--receipt", json.dumps(quarantine["receipt"])])

    assert "ai-pr-loop-ignore" in prs[7]["labels"]
    assert any(write[:2] == ["pr", "edit"] and write[-2:] == ["--add-label", "ai-pr-loop-ignore"] for write in writes)


def test_main_restore_prs_fails_if_ignore_label_recovery_cannot_be_verified(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-head-race")
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    _install_fake_provider(monkeypatch, {}, prs, [])
    assert main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"]) == 0
    quarantine = json.loads(capsys.readouterr().out)
    original_write = control_command._run_gh_text

    def lose_ignore_label_recovery(arguments: list[str]) -> str:
        if arguments[:2] == ["pr", "edit"] and arguments[-2:] == ["--remove-label", "ai-pr-loop-ignore"]:
            result = original_write(arguments)
            prs[7]["headRefOid"] = "head-moved"
            return result
        if arguments[:2] == ["pr", "edit"] and arguments[-2:] == ["--add-label", "ai-pr-loop-ignore"]:
            return "https://github.com/owner/repo/pull/7"
        return original_write(arguments)

    monkeypatch.setattr(control_command, "_run_gh_text", lose_ignore_label_recovery)

    with pytest.raises(RuntimeError, match="failed to reapply the quarantine ignore label"):
        main(["--repo", "owner/repo", "restore-prs", "--receipt", json.dumps(quarantine["receipt"])])


def test_main_restore_prs_skips_read_back_when_receipt_owns_no_ignore_labels(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-no-ignore")
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": ["ai-pr-loop-ignore"]}}
    writes = _install_fake_provider(monkeypatch, {}, prs, [])
    assert main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"]) == 0
    quarantine = json.loads(capsys.readouterr().out)
    assert quarantine["receipt"]["ignore_added"] == []

    assert main(["--repo", "owner/repo", "restore-prs", "--receipt", json.dumps(quarantine["receipt"])]) == 0

    result = json.loads(capsys.readouterr().out)
    assert result["receipt"]["changed"] == []
    assert not any(
        write[:2] == ["pr", "edit"] and write[-2:] == ["--remove-label", "ai-pr-loop-ignore"] for write in writes
    )


def test_main_rejects_a_restore_receipt_for_another_quarantine_key(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-restore-mismatch")
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    _install_fake_provider(monkeypatch, {}, prs, [])
    assert main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"]) == 0
    quarantine = json.loads(capsys.readouterr().out)
    original = control_command.get_or_store_operation_receipt

    def mismatch_restore_receipt(*args: Any) -> tuple[Any, bool]:
        if args[3] == "restore-prs":
            return {"run_id": "run-restore-mismatch", "quarantine_key": "wrong-key", "changed": [7]}, True
        return original(*args)

    monkeypatch.setattr(control_command, "get_or_store_operation_receipt", mismatch_restore_receipt)

    with pytest.raises(RuntimeError, match="does not match the quarantine receipt"):
        main(["--repo", "owner/repo", "restore-prs", "--receipt", json.dumps(quarantine["receipt"])])


def test_main_rejects_a_resume_receipt_for_different_workflow_states(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-resume-mismatch")
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    _install_fake_provider(monkeypatch, workflows, {}, [])
    assert main(["--repo", "owner/repo", "hold"]) == 0
    hold = json.loads(capsys.readouterr().out)
    original = control_command.get_or_store_operation_receipt

    def mismatch_resume_receipt(*args: Any) -> tuple[Any, bool]:
        if args[3] == "resume":
            return {
                "run_id": "run-resume-mismatch",
                "hold_key": "run-resume-mismatch:hold",
                "states": {"ai-pr-loop.yml": False},
            }, True
        return original(*args)

    monkeypatch.setattr(control_command, "get_or_store_operation_receipt", mismatch_resume_receipt)

    with pytest.raises(RuntimeError, match="does not match the hold receipt"):
        main(["--repo", "owner/repo", "resume", "--receipt", json.dumps(hold["receipt"])])


@pytest.mark.parametrize("operation", ["restore-prs", "resume"])
def test_main_rejects_completion_records_that_do_not_match_the_source_receipt(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    operation: str,
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    _install_fake_provider(monkeypatch, workflows, prs, [])

    if operation == "restore-prs":
        assert main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"]) == 0
        source_receipt = json.loads(capsys.readouterr().out)["receipt"]
        completion = {
            "run_id": "forged-run",
            "quarantine_key": "run-1:quarantine:wrong",
            "changed": [7],
        }
    else:
        assert main(["--repo", "owner/repo", "hold"]) == 0
        source_receipt = json.loads(capsys.readouterr().out)["receipt"]
        completion = {
            "run_id": "forged-run",
            "hold_key": "run-1:hold",
            "states": source_receipt["previous_states"],
        }
    monkeypatch.setattr(control_command, "find_completed_operation_receipt", lambda *_args: completion)

    with pytest.raises(RuntimeError, match="does not match"):
        main(["--repo", "owner/repo", operation, "--receipt", json.dumps(source_receipt)])


@pytest.mark.parametrize(
    ("operation", "expected_message"),
    [
        ("restore-prs", "restore-prs completion receipt read-back mismatch"),
        ("resume", "resume completion receipt read-back mismatch"),
    ],
)
def test_main_fails_when_completion_receipt_read_back_is_missing(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    operation: str,
    expected_message: str,
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    _install_fake_provider(monkeypatch, workflows, prs, [])

    if operation == "restore-prs":
        assert main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"]) == 0
        source_receipt = json.loads(capsys.readouterr().out)["receipt"]
    else:
        assert main(["--repo", "owner/repo", "hold"]) == 0
        source_receipt = json.loads(capsys.readouterr().out)["receipt"]
    monkeypatch.setattr(control_command, "find_completed_operation_receipt", lambda *_args: None)

    with pytest.raises(RuntimeError, match=expected_message):
        main(["--repo", "owner/repo", operation, "--receipt", json.dumps(source_receipt)])


@pytest.mark.parametrize("operation", ["restore-prs", "resume"])
def test_main_rejects_receipts_without_an_exact_durable_match(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    operation: str,
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    writes = _install_fake_provider(monkeypatch, workflows, prs, [])

    if operation == "restore-prs":
        assert main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"]) == 0
        receipt = json.loads(capsys.readouterr().out)["receipt"]
        receipt["run_id"] = "forged-run"
        operation_args = ["--repo", "owner/repo", operation, "--receipt", json.dumps(receipt)]
        expected = "restore receipt does not match"
    else:
        assert main(["--repo", "owner/repo", "hold"]) == 0
        receipt = json.loads(capsys.readouterr().out)["receipt"]
        receipt["run_id"] = "forged-run"
        operation_args = ["--repo", "owner/repo", operation, "--receipt", json.dumps(receipt)]
        expected = "resume receipt does not match"

    with pytest.raises(RuntimeError, match=expected):
        main(operation_args)

    assert not any(
        write[:2] == ["workflow", "enable"]
        or (write[:2] == ["pr", "edit"] and write[-2:] == ["--remove-label", "ai-pr-loop-ignore"])
        for write in writes
    )


def test_main_ignores_receipt_comments_from_untrusted_authors(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    prs: dict[int, dict[str, Any]] = {7: {"number": 7, "headRefOid": "head-7", "labels": []}}
    writes = _install_fake_provider(monkeypatch, workflows, prs, [])
    assert main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"]) == 0
    receipt = json.loads(capsys.readouterr().out)["receipt"]

    original_read = control_command._run_gh

    def forge_comment_author(arguments: list[str]) -> object:
        result = original_read(arguments)
        if arguments[:2] == ["api", "graphql"]:
            assert isinstance(result, dict)
            comments = result["data"]["repository"]["issue"]["comments"]["nodes"]
            return {
                "data": {
                    "repository": {
                        "issue": {
                            "comments": {
                                "nodes": [
                                    {"author": {"login": "attacker"}, "body": comment["body"]} for comment in comments
                                ],
                                "pageInfo": {"hasPreviousPage": False, "hasNextPage": False, "endCursor": None},
                            }
                        }
                    }
                }
            }
        return result

    monkeypatch.setattr(control_command, "_run_gh", forge_comment_author)
    with pytest.raises(RuntimeError, match="does not match a durable quarantine receipt"):
        main(["--repo", "owner/repo", "restore-prs", "--receipt", json.dumps(receipt)])

    assert not any(
        write[:2] == ["pr", "edit"] and write[-2:] == ["--remove-label", "ai-pr-loop-ignore"] for write in writes
    )


def test_main_hold_fails_if_an_initially_disabled_workflow_becomes_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    workflows = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    previously_disabled = LOOP_WORKFLOW_FILES[-1]
    workflows[previously_disabled] = False
    prs: dict[int, dict[str, Any]] = {}
    comments: list[str] = []
    _install_fake_provider(monkeypatch, workflows, prs, comments)
    original_write = control_command._run_gh_text
    injected = False

    def enable_during_hold(arguments: list[str]) -> str:
        nonlocal injected
        result = original_write(arguments)
        if arguments[:2] == ["workflow", "disable"] and not injected:
            workflows[previously_disabled] = True
            injected = True
        return result

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh_text", enable_during_hold)
    with pytest.raises(RuntimeError, match="workflow state mismatch"):
        main(["--repo", "owner/repo", "hold"])


def test_main_requires_a_stable_run_id_for_durable_operations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("GITHUB_RUN_ID", raising=False)
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._observations",
        lambda _repo, _expected: [_observation(7, "head-7")],
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._workflow_states",
        lambda _repo: dict.fromkeys(LOOP_WORKFLOW_FILES, True),
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh",
        lambda _arguments: pytest.fail("provider reads must not occur before run ID validation"),
    )

    with pytest.raises(ValueError, match="GITHUB_RUN_ID"):
        main(["--repo", "owner/repo", "ensure-labels"])
    with pytest.raises(ValueError, match="GITHUB_RUN_ID"):
        main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"])
    with pytest.raises(ValueError, match="GITHUB_RUN_ID"):
        main(["--repo", "owner/repo", "hold"])


@pytest.mark.parametrize("operation", ["quarantine", "hold"])
def test_main_rejects_durable_receipts_that_do_not_match_the_operation(
    monkeypatch: pytest.MonkeyPatch, operation: str
) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._control_issue",
        lambda _repo: 42,
    )
    if operation == "quarantine":

        def run_gh(arguments: list[str]) -> object:
            if arguments[:2] == ["api", "user"]:
                return {"login": "automation"}
            if arguments[:2] == ["label", "list"]:
                return [{"name": "ai-pr-loop-ignore"}, {"name": "ai-pr-loop-supervised"}]
            return {"login": "automation"}

        monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh", run_gh)
        monkeypatch.setattr(
            "agentic_devtools.cli.ci.supervision_control_command._read_control_issue_comments",
            lambda *_args: [],
        )
        monkeypatch.setattr(
            "agentic_devtools.cli.ci.supervision_control_command._observations",
            lambda _repo, _expected: [_observation(7, "head-7")],
        )
        monkeypatch.setattr(
            "agentic_devtools.cli.ci.supervision_control_command.build_quarantine_output",
            lambda *_args: {
                "idempotency_key": "key",
                "receipt": QuarantineReceipt("run-1", (7,), {7: "wrong-head"}, (7,)),
            },
        )
        monkeypatch.setattr(
            "agentic_devtools.cli.ci.supervision_control_command.get_or_store_operation_receipt",
            lambda *_args: (QuarantineReceipt("run-1", (7,), {7: "wrong-head"}, (7,)), True),
        )
        with pytest.raises(RuntimeError, match="requested PR heads"):
            main(["--repo", "owner/repo", "quarantine", "--pr", "7=head-7"])
    else:
        monkeypatch.setattr(
            "agentic_devtools.cli.ci.supervision_control_command._run_gh",
            lambda _arguments: {"login": "automation"},
        )
        monkeypatch.setattr(
            "agentic_devtools.cli.ci.supervision_control_command._read_control_issue_comments",
            lambda *_args: [],
        )
        monkeypatch.setattr(
            "agentic_devtools.cli.ci.supervision_control_command._workflow_states",
            lambda _repo: dict.fromkeys(LOOP_WORKFLOW_FILES, True),
        )
        monkeypatch.setattr(
            "agentic_devtools.cli.ci.supervision_control_command.build_hold_output",
            lambda *_args: {"idempotency_key": "key", "receipt": HoldReceipt("run-1", (), {})},
        )
        monkeypatch.setattr(
            "agentic_devtools.cli.ci.supervision_control_command.get_or_store_operation_receipt",
            lambda *_args: (HoldReceipt("run-1", (), {}), True),
        )
        with pytest.raises(RuntimeError, match="complete workflow set"):
            main(["--repo", "owner/repo", "hold"])


def test_main_rejects_an_unsupported_operation(monkeypatch: pytest.MonkeyPatch) -> None:
    class UnsupportedParser:
        def parse_args(self, _argv: object = None) -> Namespace:
            return Namespace(repo="owner/repo", operation="unsupported")

    monkeypatch.setattr(control_command, "build_parser", UnsupportedParser)
    with pytest.raises(NotImplementedError, match="verified provider leaf"):
        main([])


def test_main_rejects_mutation_without_supervision_lease(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AGDT_SUPERVISION_LEASE_ID")
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh",
        lambda _arguments: pytest.fail("provider must not be called without the lease"),
    )

    with pytest.raises(ValueError, match="AGDT_SUPERVISION_LEASE_ID is required"):
        main(["--repo", "owner/repo", "checkpoint", "--run-id", "1", "--payload", "{}"])
