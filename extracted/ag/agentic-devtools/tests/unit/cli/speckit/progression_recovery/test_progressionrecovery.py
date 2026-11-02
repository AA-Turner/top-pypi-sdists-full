"""Recovery decisions and provider-write ordering."""

import hashlib
import json
from datetime import UTC, datetime
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.shared.retry import RetryableError
from agentic_devtools.cli.speckit.progression_recovery import ProgressionRecovery

NOW = datetime(2026, 10, 13, 12, tzinfo=UTC)
START = "2026-10-13T08:00:00Z"
RECENT = "2026-10-13T11:00:00Z"


def snapshot(**changes):
    value = {
        "issue": {"number": 42, "state": "open"},
        "labels": {"speckit", "speckit:processing", "feature"},
        "initial_state": True,
        "root_issue": True,
        "events": [
            {
                "id": 7,
                "event": "labeled",
                "label": {"name": "speckit:processing"},
                "created_at": START,
                "actor": {"login": "github-actions[bot]"},
            }
        ],
        "comments": [],
        "pulls": [],
        "runs": [],
    }
    value.update(changes)
    return value


def comment(body, created_at=START, login="github-actions[bot]"):
    return {"id": 88, "body": body, "created_at": created_at, "user": {"login": login}}


def dispatch_marker(**changes):
    inputs = {
        "issue_number": "42",
        "phase": "2",
        "hierarchy_level": "feature",
        "spec_dir": "specs/42-demo",
        "spec_context": "",
    }
    inputs.update(changes)
    return "<!-- speckit:progression-dispatch schema_version=1 " + json.dumps(inputs) + " -->"


def recovery():
    return ProgressionRecovery("owner/repo", "workflow-token", api_call=Mock(), now=NOW)


class TestProgressionRecovery:
    def test_initial_replay_preserves_inputs(self):
        decision = recovery().classify(snapshot())
        assert decision["status"] == "replay"
        assert decision["inputs"] == {
            "issue_number": "42",
            "phase": "1",
            "hierarchy_level": "feature",
            "spec_dir": "",
            "spec_context": "",
        }

    def test_later_phase_requires_exact_dispatch_marker(self):
        value = snapshot(comments=[comment(dispatch_marker())])
        assert recovery().classify(value)["inputs"]["phase"] == "2"
        assert (
            recovery().classify(snapshot(labels={"speckit:processing", "speckit:phase-2", "feature"}))["status"]
            == "failed"
        )

    @pytest.mark.parametrize(
        "changes",
        [
            {"issue": {"number": 42, "state": "closed"}},
            {"labels": {"feature"}},
            {"labels": {"speckit:processing", "speckit:agent-assigned-phase-2"}},
            {"events": [{"id": 8, "event": "labeled", "label": {"name": "speckit:processing"}, "created_at": RECENT}]},
            {"runs": [{"status": "queued", "display_title": "SpecKit progression issue #42 phase 1"}]},
            {
                "runs": [
                    {
                        "status": "in_progress",
                        "display_title": "SpecKit Phase Progression",
                        "event": "workflow_dispatch",
                    }
                ]
            },
        ],
    )
    def test_active_or_recent_issues_untouched(self, changes):
        assert recovery().classify(snapshot(**changes))["status"] == "skip"

    def test_replay_reservation_precedes_dispatch_and_rechecks(self):
        worker = recovery()
        reserved = comment(
            "<!-- speckit:progression-recovery schema_version=1 epoch=7 inputs_sha256="
            + hashlib.sha256(json.dumps(recovery().classify(snapshot())["inputs"], sort_keys=True).encode()).hexdigest()
            + " -->",
            RECENT,
        )
        reserved["id"] = 101
        worker.inspect = Mock(side_effect=[snapshot(), snapshot(), snapshot(comments=[reserved])])
        worker.api_call.return_value = '{"id":101}'
        result = worker.recover(42)
        assert result["status"] == "replayed"
        calls = worker.api_call.call_args_list
        assert calls[0].kwargs["body"]["body"].startswith("<!-- speckit:progression-recovery")
        assert calls[1].args[0].endswith("/actions/workflows/speckit-phase-progression.yml/dispatches")
        assert calls[1].kwargs["body"]["inputs"]["phase"] == "1"
        assert worker.inspect.call_count == 3

    def test_failure_comment_and_label_before_removal(self):
        worker = recovery()
        worker.inspect = Mock(return_value=snapshot(labels={"speckit:processing"}))
        assert worker.recover(42)["status"] == "failed"
        calls = worker.api_call.call_args_list
        assert calls[0].kwargs["body"] == {"labels": ["speckit:failed"]}
        assert "#42" in calls[1].kwargs["body"]["body"]
        assert calls[2].kwargs["method"] == "DELETE"

    @pytest.mark.parametrize("failed_write", [0, 1, 2])
    def test_api_failure_does_not_clear_processing(self, failed_write):
        worker = recovery()
        worker.inspect = Mock(return_value=snapshot(labels={"speckit:processing"}))
        worker.api_call.side_effect = [""] * failed_write + [RuntimeError("provider error")]
        with pytest.raises(RuntimeError, match="provider error"):
            worker.recover(42)
        assert len(worker.api_call.call_args_list) == failed_write + 1

    def test_guard_change_prevents_mutation(self):
        worker = recovery()
        worker.inspect = Mock(side_effect=[snapshot(), snapshot(labels={"speckit:processing", "task"})])
        assert worker.recover(42)["status"] == "skip"
        worker.api_call.assert_not_called()

    @pytest.mark.parametrize(
        "repo,token",
        [("bad", "token"), ("a/../b", "token"), ("a/b?", "token"), ("a/b", " "), (None, "token"), ("a/b", None)],
    )
    def test_configuration_fails_before_api(self, repo, token):
        with pytest.raises(ValueError):
            ProgressionRecovery(repo, token)

    @pytest.mark.parametrize("repo", ["../repo", "./repo", "owner/..", "owner/."])
    def test_dot_path_components_fail_before_api(self, repo):
        api_call = Mock()
        with pytest.raises(ValueError, match="GITHUB_REPOSITORY must be in owner/repo format"):
            ProgressionRecovery(repo, "token", api_call=api_call)
        api_call.assert_not_called()

    def test_default_clock(self):
        assert ProgressionRecovery("owner/repo.git", "token").now.tzinfo is not None

    @pytest.mark.parametrize("stamp", [None, "2026-10-13T08:00:00", "invalid"])
    def test_invalid_durable_time(self, stamp):
        with pytest.raises(ValueError):
            recovery()._time(stamp)

    def test_reads_paginated_arrays_and_workflow_run_objects(self):
        worker = recovery()
        worker.api_call.return_value = '[{"number":42}]\n[{"number":43}]'
        assert worker._read("/issues") == [{"number": 42}, {"number": 43}]
        worker.api_call.return_value = '{"workflow_runs":[{"id":1}]}\n{"workflow_runs":[]}'
        assert worker._read("/runs", "workflow_runs") == [{"id": 1}]
        worker.api_call.return_value = '{"number":42}'
        assert worker._read("/issues/42", "object") == {"number": 42}

    @pytest.mark.parametrize(
        "payload,key",
        [
            (" ", None),
            ("{}", None),
            ("[null]", None),
            ("[]", "object"),
            ("{} {}", "object"),
            ('{"workflow_runs":null}', "workflow_runs"),
            ("null", "workflow_runs"),
        ],
    )
    def test_invalid_api_shapes(self, payload, key):
        worker = recovery()
        worker.api_call.return_value = payload
        with pytest.raises(RuntimeError):
            worker._read("/issues", key)

    def test_processing_scan_excludes_pull_requests(self):
        worker = recovery()
        worker.api_call.return_value = '[{"number":42},{"number":43,"pull_request":{}}]'
        assert worker.processing_issues() == [42]
        assert "state=open&labels=speckit%3Aprocessing" in worker.api_call.call_args.args[0]

    def test_inspection_reads_all_guard_evidence(self):
        worker = recovery()
        worker.api_call.side_effect = [
            '{"number":42,"state":"open","labels":[{"name":"speckit:processing"}]}',
            '{"truncated":false,"tree":[]}',
            '{"data":{"repository":{"issue":{"parent":null}}}}',
            "[]",
            "[]",
            "[]",
            '{"workflow_runs":[]}',
        ]
        evidence = worker.inspect(42)
        assert evidence["labels"] == {"speckit:processing"}
        assert len(worker.api_call.call_args_list) == 7
        assert evidence["initial_state"] is True
        assert evidence["root_issue"] is True

    def test_repository_history_cached_but_changed_pull_requests_are_refreshed(self):
        worker = recovery()
        old = {"number": 1, "state": "closed"}
        live = {"number": 2, "state": "open"}
        merged = {"number": 2, "state": "closed", "merged_at": RECENT}
        worker._read = Mock(
            side_effect=[
                [old],
                [{"number": 42}, {"number": 2, "pull_request": {}}],
                live,
                [{"number": 2, "pull_request": {}}],
                merged,
            ]
        )
        assert worker._cached_pulls() == [old]
        assert worker._cached_pulls() == [old, live]
        assert worker._cached_pulls() == [old, merged]
        endpoints = [call.args[0] for call in worker._read.call_args_list]
        assert endpoints.count("/pulls?state=all&per_page=100") == 1
        assert sum("since=" in endpoint for endpoint in endpoints) == 2

    def test_new_runs_and_preexisting_active_run_transitions_are_refreshed(self):
        worker = recovery()
        completed = {"id": 1, "status": "completed"}
        active = {"id": 2, "status": "in_progress"}
        finished = {"id": 2, "status": "completed"}
        new = {"id": 3, "status": "queued", "display_title": "issue #42"}
        worker._read = Mock(side_effect=[[completed, active], [new], *([[]] * 5), finished, [new], *([[]] * 5)])
        assert worker._cached_runs() == [completed, active]
        assert worker._cached_runs() == [new, completed, finished]
        assert worker._cached_runs() == [new, completed, finished]
        endpoints = [call.args[0] for call in worker._read.call_args_list]
        assert endpoints.count("/actions/workflows/speckit-phase-progression.yml/runs?per_page=100") == 1
        assert endpoints.count("/actions/runs/2") == 1
        assert sum("created=" in endpoint for endpoint in endpoints) == 2

    @pytest.mark.parametrize("live_kind", ["run", "pull"])
    def test_fresh_live_work_vetoes_prewrite_guard(self, live_kind):
        worker = recovery()
        value = snapshot()
        decision = worker.classify(value)
        pr = {
            "number": 77,
            "state": "open",
            "head": {"ref": "speckit/42/phase-1-specify"},
            "base": {"ref": "main"},
            "labels": [{"name": "speckit:phase-1"}],
            "user": {"login": "github-actions[bot]"},
        }
        worker._pulls_cache = []
        worker._runs_cache = []

        def read(endpoint, key=None):
            if endpoint.startswith("/issues?state=all&since="):
                return [{"number": 77, "pull_request": {}}] if live_kind == "pull" else []
            if endpoint == "/pulls/77":
                return pr
            if "status=" in endpoint:
                return []
            assert "created=" in endpoint
            return [{"id": 99, "status": "queued", "display_title": "issue #42"}] if live_kind == "run" else []

        worker._read = Mock(side_effect=read)

        def inspect(number):
            return snapshot(pulls=worker._cached_pulls(), runs=worker._cached_runs())

        worker.inspect = inspect
        assert worker._unchanged(42, decision) is False

    @pytest.mark.parametrize("number", [True, "42", 0])
    def test_inspection_rejects_invalid_number(self, number):
        with pytest.raises(ValueError):
            recovery().inspect(number)

    @pytest.mark.parametrize("labels", [None, [None], [{"name": None}]])
    def test_invalid_issue_labels(self, labels):
        worker = recovery()
        worker.api_call.return_value = json.dumps({"number": 42, "state": "open", "labels": labels})
        with pytest.raises(RuntimeError):
            worker.inspect(42)

    def test_requires_durable_event_not_updated_at(self):
        with pytest.raises(RuntimeError, match="no durable"):
            recovery().classify(snapshot(events=[{"event": "commented", "created_at": START}]))
        value = snapshot(issue={"number": 42, "state": "open", "updated_at": RECENT})
        assert recovery().classify(value)["status"] == "replay"

    def test_latest_processing_event_controls_epoch_and_age(self):
        value = snapshot()
        value["events"] += [
            {"id": 8, "event": "labeled", "label": {"name": "other"}, "created_at": RECENT},
            {"id": 9, "event": "labeled", "label": {"name": "speckit:processing"}, "created_at": RECENT},
        ]
        assert recovery().classify(value)["reason"] == "processing-is-recent"

    @pytest.mark.parametrize(
        "body",
        [
            "<!-- speckit:progression-dispatch bad -->",
            "<!-- speckit:progression-dispatch schema_version=1 {bad} -->",
            dispatch_marker(phase="9"),
        ],
    )
    def test_malformed_trusted_marker_fails_closed(self, body):
        value = snapshot(comments=[comment(body)])
        assert recovery().classify(value)["status"] == "failed"

    def test_untrusted_and_old_markers_do_not_authorize_later_phase(self):
        value = snapshot(
            labels={"speckit:processing"},
            comments=[
                comment(dispatch_marker(), login="attacker"),
                comment(dispatch_marker(), created_at="2026-10-12T08:00:00Z"),
                {"body": dispatch_marker(), "user": None},
            ],
        )
        assert recovery().classify(value)["status"] == "failed"

    def test_recent_dispatch_marker_defers_recovery(self):
        assert recovery().classify(snapshot(comments=[comment(dispatch_marker(), RECENT)]))["status"] == "skip"

    @pytest.mark.parametrize(
        "changes",
        [
            {"phase": "4"},
            {"issue_number": "43"},
            {"hierarchy_level": "unknown"},
            {"spec_dir": "../specs/42"},
            {"spec_dir": "specs/a/../42"},
            {"spec_dir": "specs//42"},
            {"spec_dir": "specs/./42"},
            {"spec_dir": None},
            {"spec_context": "../spec.md"},
            {"phase": 2},
            {"hierarchy_level": ""},
            {"extra": "input"},
        ],
    )
    def test_input_validation_rejects_inexact_replay(self, changes):
        inputs = {
            "issue_number": "42",
            "phase": "2",
            "hierarchy_level": "feature",
            "spec_dir": "specs/42-demo",
            "spec_context": "",
        }
        inputs.update(changes)
        with pytest.raises(ValueError):
            recovery()._validate_inputs(inputs, 42)

    def test_input_validation_requires_mapping_and_all_keys(self):
        for value in [None, [], {"phase": "2"}]:
            with pytest.raises(ValueError):
                recovery()._validate_inputs(value, 42)

    def test_task_phase_three_preserves_parent_spec_context(self):
        decision = recovery().classify(
            snapshot(
                comments=[
                    comment(dispatch_marker(phase="3", hierarchy_level="task", spec_context="specs/parent/spec.md"))
                ]
            )
        )
        assert decision["inputs"]["hierarchy_level"] == "task"
        assert decision["inputs"]["spec_dir"] == "specs/42-demo"
        assert decision["inputs"]["spec_context"] == "specs/parent/spec.md"

    def test_prior_reservation_suppresses_replay_then_surfaces_failure(self):
        marker = "<!-- speckit:progression-recovery schema_version=1 epoch=7 inputs_sha256=test -->"
        assert (
            recovery().classify(snapshot(comments=[comment(marker, RECENT)]))["reason"] == "recovery-already-reserved"
        )
        assert recovery().classify(snapshot(comments=[comment(marker)]))["status"] == "failed"
        assert (
            recovery().classify(snapshot(comments=[comment(marker.replace("epoch=7", "epoch=6"))]))["status"]
            == "replay"
        )

    @pytest.mark.parametrize(
        "labels,issue_type,status",
        [
            ({"speckit", "speckit:processing", "epic"}, None, "replay"),
            ({"speckit", "speckit:processing"}, {"name": "Feature"}, "replay"),
            ({"speckit", "speckit:processing", "task"}, None, "failed"),
            ({"speckit", "speckit:processing", "feature", "task"}, None, "failed"),
            ({"speckit:processing", "feature"}, None, "failed"),
            ({"speckit", "speckit:processing", "speckit:level-feature"}, None, "failed"),
        ],
    )
    def test_initial_hierarchy_is_not_guessed(self, labels, issue_type, status):
        value = snapshot(labels=labels, issue={"number": 42, "state": "open", "type": issue_type})
        assert recovery().classify(value)["status"] == status

    @pytest.mark.parametrize(
        "state,phase_label,login,base,branch,reason",
        [
            ("open", "speckit:phase-1", "github-actions[bot]", "main", "speckit/42/phase-1-specify", "open-phase-pr"),
            ("closed", "speckit:phase-1", "github-actions[bot]", "main", "speckit/42/phase-1-specify", "phase or"),
            # An untrusted, unmerged PR's branch name alone is not authenticated phase
            # evidence (#4254 review); the issue is still replayed as initial state.
            ("open", "speckit:phase-1", "attacker", "main", "speckit/42/phase-1-specify", "exact-dispatch-inputs"),
            ("open", "speckit:phase-1", "github-actions[bot]", "other", "speckit/42/phase-1-specify", "phase or"),
            ("open", "other", "github-actions[bot]", "main", "speckit/42/phase-1-specify", "phase or"),
            ("open", "speckit:phase-1", "github-actions[bot]", "main", "speckit/42/phase-1-plan", "phase or"),
            (
                "open",
                "speckit:phase-1",
                "github-actions[bot]",
                "main",
                "speckit/43/phase-1-specify",
                "exact-dispatch-inputs",
            ),
        ],
    )
    def test_legacy_phase_prs_validate_metadata(self, state, phase_label, login, base, branch, reason):
        pr = {
            "state": state,
            "head": {"ref": branch},
            "base": {"ref": base},
            "labels": [{"name": phase_label}],
            "user": {"login": login},
        }
        assert recovery().classify(snapshot(pulls=[pr]))["reason"].startswith(reason)

    def test_cloud_pr_needs_authoritative_source_marker(self):
        marker = (
            "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
            "issue=42 phase=2 hierarchy=feature correlation_id=12345678-1234-1234-1234-123456789abc -->"
        )
        pr = {
            "state": "open",
            "head": {"ref": "copilot/specify"},
            "body": marker,
            "base": {"ref": "speckit/42/phase-1-specify"},
            "user": {"login": "copilot-swe-agent[bot]"},
        }
        assert recovery().classify(snapshot(pulls=[pr], comments=[comment(marker)]))["reason"] == "open-cloud-phase-pr"
        assert recovery().classify(snapshot(pulls=[pr]))["status"] == "failed"
        pr["base"]["ref"] = "wrong"
        assert recovery().classify(snapshot(pulls=[pr], comments=[comment(marker)]))["status"] == "failed"

    def test_cancelled_matching_run_is_reported_in_terminal_comment(self):
        worker = recovery()
        run = {
            "status": "completed",
            "conclusion": "cancelled",
            "display_title": "issue #42",
            "html_url": "https://run",
        }
        worker.inspect = Mock(return_value=snapshot(labels={"speckit:processing"}, runs=[run]))
        worker.recover(42)
        assert "https://run" in worker.api_call.call_args_list[1].kwargs["body"]["body"]

    def test_other_issue_run_does_not_block_and_branch_run_does(self):
        assert (
            recovery().classify(
                snapshot(
                    runs=[
                        {"status": "queued", "display_title": "issue #43"},
                        {"status": "completed", "display_title": "unidentified"},
                    ]
                )
            )["status"]
            == "replay"
        )
        assert (
            recovery().classify(
                snapshot(
                    runs=[
                        {"status": "in_progress", "head_branch": "speckit/42/phase-1-specify"},
                    ]
                )
            )["status"]
            == "skip"
        )

    def test_skip_performs_no_writes(self):
        worker = recovery()
        worker.inspect = Mock(return_value=snapshot(labels=set()))
        assert worker.recover(42)["status"] == "skip"
        worker.api_call.assert_not_called()

    def test_failed_final_guard_retains_processing(self):
        worker = recovery()
        worker.inspect = Mock(
            side_effect=[
                snapshot(labels={"speckit:processing"}),
                snapshot(labels={"speckit:processing"}),
                snapshot(labels=set()),
            ]
        )
        assert worker.recover(42)["status"] == "skip"
        assert len(worker.api_call.call_args_list) == 2

    @pytest.mark.parametrize("response", ["[]", "{}", '{"id":"bad"}'])
    def test_bad_reservation_receipt_cannot_dispatch(self, response):
        worker = recovery()
        worker.inspect = Mock(return_value=snapshot())
        worker.api_call.return_value = response
        with pytest.raises(RuntimeError, match="reservation response"):
            worker.recover(42)
        assert len(worker.api_call.call_args_list) == 1

    def test_missing_reservation_readback_cannot_dispatch(self):
        worker = recovery()
        worker.inspect = Mock(return_value=snapshot())
        worker.api_call.return_value = '{"id":101}'
        with pytest.raises(RuntimeError, match="read back"):
            worker.recover(42)

    def test_work_started_after_reservation_cannot_dispatch(self):
        worker = recovery()
        digest = hashlib.sha256(json.dumps(worker.classify(snapshot())["inputs"], sort_keys=True).encode()).hexdigest()
        reserved = comment(
            f"<!-- speckit:progression-recovery schema_version=1 epoch=7 inputs_sha256={digest} -->", RECENT
        )
        reserved["id"] = 101
        worker.inspect = Mock(
            side_effect=[
                snapshot(),
                snapshot(),
                snapshot(comments=[reserved], runs=[{"status": "queued", "display_title": "issue #42"}]),
            ]
        )
        worker.api_call.return_value = '{"id":101}'
        assert worker.recover(42)["status"] == "skip"
        assert len(worker.api_call.call_args_list) == 1

    @pytest.mark.parametrize(
        "tree",
        [
            {"truncated": True, "tree": []},
            {"truncated": False, "tree": None},
            {"truncated": False, "tree": [None]},
            {"truncated": False, "tree": [{"path": None}]},
        ],
    )
    def test_incomplete_canonical_tree_preserves_processing(self, tree):
        worker = recovery()
        worker.api_call.side_effect = ['{"number":42,"state":"open","labels":[]}', json.dumps(tree)]
        with pytest.raises(RuntimeError, match="canonical spec tree"):
            worker.inspect(42)

    def test_existing_numbered_spec_disallows_initial_replay(self):
        worker = recovery()
        worker.api_call.side_effect = [
            '{"number":42,"state":"open","labels":[]}',
            '{"truncated":false,"tree":[{"path":"specs/features/042-demo/spec.md"}]}',
            '{"data":{"repository":{"issue":{"parent":null}}}}',
            "[]",
            "[]",
            "[]",
            '{"workflow_runs":[]}',
        ]
        assert worker.inspect(42)["initial_state"] is False
        assert worker.classify(snapshot(initial_state=False))["status"] == "failed"

    def test_later_completed_run_cannot_restart_phase_one(self):
        value = snapshot(runs=[{"status": "completed", "display_title": "issue #42 phase 2"}])
        assert recovery().classify(value)["status"] == "failed"

    @pytest.mark.parametrize("issue", [{}, {"number": 42, "state": "unknown"}])
    def test_inspection_rejects_identity_or_state_mismatch(self, issue):
        worker = recovery()
        worker.api_call.return_value = json.dumps(issue)
        with pytest.raises(RuntimeError, match="identity/state"):
            worker.inspect(42)

    def test_malformed_nested_metadata_is_controlled_error(self):
        with pytest.raises(RuntimeError, match="metadata object"):
            recovery().classify(snapshot(events=[{"event": "labeled", "label": "invalid"}]))
        with pytest.raises(RuntimeError, match="metadata text"):
            recovery().classify(snapshot(runs=[{"display_title": []}]))
        value = snapshot(events=[{"id": 7, "event": "labeled", "label": None}])
        with pytest.raises(RuntimeError, match="no durable"):
            recovery().classify(value)
        value = snapshot(events=[{"event": "labeled", "label": {"name": "speckit:processing"}, "created_at": START}])
        with pytest.raises(RuntimeError, match="event identity"):
            recovery().classify(value)

    def test_durable_dispatch_can_supply_age_without_label_event(self):
        value = snapshot(events=[], comments=[comment(dispatch_marker())])
        assert recovery().classify(value)["status"] == "replay"

    def test_dispatch_marker_identity_is_required(self):
        source = comment(dispatch_marker())
        del source["id"]
        with pytest.raises(RuntimeError, match="dispatch marker identity"):
            recovery().classify(snapshot(comments=[source]))

    def test_completed_phase_cannot_be_replayed(self):
        value = snapshot(
            labels={"speckit:processing", "speckit:phase-2-complete"}, comments=[comment(dispatch_marker())]
        )
        assert recovery().classify(value)["reason"] == "recorded dispatch phase is already complete"

    def test_new_phase_has_distinct_reservation_epoch(self):
        marker = comment(dispatch_marker())
        first = recovery().classify(snapshot(comments=[marker]))
        marker["id"] = 89
        marker["body"] = dispatch_marker(phase="3")
        second = recovery().classify(snapshot(comments=[marker]))
        assert first["epoch"] != second["epoch"]

    def test_same_second_dispatch_markers_break_ties_on_id(self):
        older = comment(dispatch_marker(phase="2"), created_at=START)
        older["id"] = 88
        newer = comment(dispatch_marker(phase="3"), created_at=START)
        newer["id"] = 90
        decision = recovery().classify(snapshot(comments=[older, newer]))
        assert decision["inputs"]["phase"] == "3"
        assert decision["epoch"].endswith("-dispatch-90")

    def test_dispatch_marker_identity_is_validated_before_tie_break_selection(self):
        older = comment(dispatch_marker(phase="2"), created_at=START)
        older["id"] = 88
        newer = comment(dispatch_marker(phase="3"), created_at=START)
        del newer["id"]
        with pytest.raises(RuntimeError, match="dispatch marker identity"):
            recovery().classify(snapshot(comments=[older, newer]))

    def test_same_second_cloud_markers_break_ties_on_id(self):
        def assigned(phase):
            return (
                "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
                f"issue=42 phase={phase} hierarchy=feature correlation_id=12345678-1234-1234-1234-123456789abc -->"
            )

        older = comment(assigned(2))
        older["id"] = 88
        newer = comment(assigned(3))
        newer["id"] = 90
        pr = {
            "state": "open",
            "head": {"ref": "copilot/plan"},
            "body": assigned(3),
            "base": {"ref": "speckit/42/phase-2-clarify"},
            "user": {"login": "copilot-swe-agent[bot]"},
        }
        decision = recovery().classify(snapshot(pulls=[pr], comments=[older, newer]))
        assert decision == {"issue_number": 42, "status": "skip", "reason": "open-cloud-phase-pr"}
        worker = recovery()
        worker.inspect = Mock(return_value=snapshot(pulls=[pr], comments=[older, newer]))
        assert worker.recover(42)["reason"] == "open-cloud-phase-pr"
        worker.api_call.assert_not_called()
        newer["id"] = True
        with pytest.raises(RuntimeError, match="cloud assignment marker identity"):
            recovery().classify(snapshot(pulls=[pr], comments=[older, newer]))

    def test_same_second_processing_events_break_ties_on_id(self):
        events = [
            {"id": 7, "event": "labeled", "label": {"name": "speckit:processing"}, "created_at": START},
            {"id": 9, "event": "labeled", "label": {"name": "speckit:processing"}, "created_at": START},
        ]
        assert recovery().classify(snapshot(events=events))["epoch"] == "9"
        events[0]["id"] = None
        with pytest.raises(RuntimeError, match="processing label event identity"):
            recovery().classify(snapshot(events=events))

    def test_legacy_fallback_tracking_is_left_to_existing_cleanup(self):
        value = snapshot(labels={"speckit:processing", "speckit:agent-fallback"})
        assert recovery().classify(value)["status"] == "skip"

    def test_trusted_comment_correlates_an_old_static_run_title(self):
        value = snapshot(
            comments=[comment("Workflow: https://github.com/owner/repo/actions/runs/123")],
            runs=[{"id": 123, "status": "completed", "html_url": "https://github.com/owner/repo/actions/runs/123"}],
        )
        assert recovery().classify(value)["last_run_url"].endswith("/123")

    def test_run_pull_request_metadata_correlates_source_phase(self):
        pr = {"number": 77, "state": "closed", "head": {"ref": "speckit/42/phase-1-specify"}}
        run = {"id": 123, "status": "completed", "pull_requests": [{"number": 77}], "html_url": "https://run"}
        assert recovery().classify(snapshot(pulls=[pr], runs=[run]))["last_run_url"] == "https://run"
        run["pull_requests"] = [None]
        assert recovery().classify(snapshot(pulls=[pr], runs=[run]))["last_run_url"] is None

    def test_malformed_run_pr_metadata_is_an_inspection_error(self):
        with pytest.raises(RuntimeError, match="run pull request metadata"):
            recovery().classify(snapshot(runs=[{"pull_requests": None}]))

    def test_future_completed_phase_also_blocks_old_dispatch(self):
        value = snapshot(
            labels={"speckit:processing", "speckit:phase-3-complete"}, comments=[comment(dispatch_marker())]
        )
        assert recovery().classify(value)["status"] == "failed"

    def test_transient_inspection_retries_only_the_read(self):
        worker = recovery()
        worker.api_call.side_effect = [RetryableError("temporary"), "[]"]
        with patch("agentic_devtools.cli.ci.retry.time.sleep"):
            assert worker._read("/issues") == []
        assert worker.api_call.call_count == 2

    def test_ambiguous_dispatch_failure_is_not_retried_or_cleared(self):
        worker = recovery()
        reserved = comment(
            "<!-- speckit:progression-recovery schema_version=1 epoch=7 inputs_sha256="
            + hashlib.sha256(json.dumps(recovery().classify(snapshot())["inputs"], sort_keys=True).encode()).hexdigest()
            + " -->",
            RECENT,
        )
        reserved["id"] = 101
        worker.inspect = Mock(side_effect=[snapshot(), snapshot(), snapshot(comments=[reserved])])
        worker.api_call.side_effect = ['{"id":101}', RuntimeError("transport disconnected")]
        with pytest.raises(RuntimeError, match="transport disconnected"):
            worker.recover(42)
        assert worker.api_call.call_count == 2
        assert all(call.kwargs["method"] == "POST" for call in worker.api_call.call_args_list)
        assert recovery().classify(snapshot(comments=[reserved]))["reason"] == "recovery-already-reserved"

    def test_changed_phase_epoch_after_guard_cannot_mutate(self):
        worker = recovery()
        changed = snapshot()
        changed["events"][0]["id"] = 9
        worker.inspect = Mock(side_effect=[snapshot(), changed])
        assert worker.recover(42)["reason"] == "state-changed"
        worker.api_call.assert_not_called()

    def test_overlapping_recovery_reservations_cannot_dispatch_twice(self):
        worker = recovery()
        other = comment(
            "<!-- speckit:progression-recovery schema_version=1 epoch=7 inputs_sha256="
            + hashlib.sha256(json.dumps(recovery().classify(snapshot())["inputs"], sort_keys=True).encode()).hexdigest()
            + " -->",
            RECENT,
        )
        other["id"] = 100
        own = {**other, "id": 101}
        worker.inspect = Mock(side_effect=[snapshot(), snapshot(), snapshot(comments=[own, other])])
        worker.api_call.return_value = '{"id":101}'
        assert worker.recover(42)["reason"] == "state-changed"
        assert worker.api_call.call_count == 1

    def test_initial_processing_event_must_be_trusted(self):
        value = snapshot()
        value["events"][0]["actor"] = {"login": "untrusted"}
        assert recovery().classify(value)["status"] == "failed"

    def test_merged_pr_run_name_correlates_without_dispatch_issue_input(self):
        own = {"number": 77, "state": "closed", "head": {"ref": "speckit/42/phase-1-specify"}}
        other = {"number": 78, "state": "closed", "head": {"ref": "speckit/43/phase-1-specify"}}
        run = {"status": "queued", "display_title": "SpecKit progression — PR #78"}
        decision = recovery().classify(snapshot(pulls=[other], runs=[run]))
        assert decision["status"] == "replay"
        run["display_title"] = "SpecKit progression — PR #77"
        assert recovery().classify(snapshot(pulls=[own], runs=[run]))["reason"] == "active-progression-run"

    def test_cloud_pr_run_name_correlates_marked_issue(self):
        marker = (
            "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
            "issue=43 phase=2 hierarchy=feature correlation_id=12345678-1234-1234-1234-123456789abc -->"
        )
        other = {"number": 78, "state": "closed", "head": {"ref": "copilot/clarify"}, "body": marker}
        run = {"status": "in_progress", "display_title": "SpecKit progression — PR #78"}
        assert recovery().classify(snapshot(pulls=[other], runs=[run]))["status"] == "replay"

    def test_unidentified_pr_run_remains_conservative(self):
        value = snapshot(
            pulls=[{"number": 80, "head": {"ref": "feature/ordinary"}}],
            runs=[{"status": "queued", "display_title": "SpecKit progression — PR #80"}],
        )
        assert recovery().classify(value)["reason"] == "active-progression-run"

    @pytest.mark.parametrize("state", ["open", "closed"])
    def test_untrusted_unmerged_noncanonical_branch_does_not_block_initial_restart(self, state):
        # An untrusted, unmerged PR's branch name alone is not authenticated phase
        # evidence (#4254 review); it must not block the issue from being replayed.
        value = snapshot(pulls=[{"number": 80, "state": state, "head": {"ref": "speckit/42/phase-3-plan-tasks"}}])
        assert recovery().classify(value)["status"] == "replay"

    @pytest.mark.parametrize("state", ["open", "closed"])
    def test_trusted_noncanonical_phase_branch_blocks_initial_restart(self, state):
        value = snapshot(
            pulls=[
                {
                    "number": 80,
                    "state": state,
                    "head": {"ref": "speckit/42/phase-3-plan-tasks"},
                    "user": {"login": "github-actions[bot]"},
                }
            ]
        )
        assert recovery().classify(value)["status"] == "failed"

    @pytest.mark.parametrize("state", ["open", "closed"])
    def test_merged_noncanonical_phase_branch_blocks_initial_restart(self, state):
        value = snapshot(
            pulls=[
                {
                    "number": 80,
                    "state": state,
                    "merged_at": START,
                    "head": {"ref": "speckit/42/phase-3-plan-tasks"},
                }
            ]
        )
        assert recovery().classify(value)["status"] == "failed"

    def test_removed_completed_phase_label_blocks_initial_restart(self):
        value = snapshot()
        value["events"].insert(0, {"event": "unlabeled", "label": {"name": "speckit:phase-2-complete"}})
        assert recovery().classify(value)["status"] == "failed"

    def test_non_label_event_is_not_prior_phase_evidence(self):
        value = snapshot()
        value["events"].insert(0, {"event": "commented", "label": {"name": "speckit:phase-2-complete"}})
        assert recovery().classify(value)["status"] == "replay"

    @pytest.mark.parametrize(
        "phase,hierarchy,expected_status",
        [("2", "auto", "replay"), ("3", "feature", "replay"), ("1", "task", "replay"), ("3", "task", "replay")],
    )
    def test_exact_recorded_defaults_are_preserved_without_guessing(self, phase, hierarchy, expected_status):
        value = snapshot(comments=[comment(dispatch_marker(phase=phase, hierarchy_level=hierarchy, spec_dir=""))])
        decision = recovery().classify(value)
        assert decision["status"] == expected_status
        assert decision["inputs"] == {
            "issue_number": "42",
            "phase": phase,
            "hierarchy_level": hierarchy,
            "spec_dir": "",
            "spec_context": "",
        }

    def test_legacy_task_phase_three_dispatch_without_spec_context_replays(self):
        inputs = {
            "issue_number": "42",
            "phase": "3",
            "hierarchy_level": "task",
            "spec_dir": "",
        }
        marker = "<!-- speckit:progression-dispatch schema_version=1 " + json.dumps(inputs) + " -->"

        decision = recovery().classify(snapshot(comments=[comment(marker)]))

        assert decision["status"] == "replay"
        assert decision["inputs"]["spec_context"] == ""

    def test_recorded_marker_can_be_surrounded_by_explanation_and_run_url(self):
        body = "Exact requested dispatch:\n" + dispatch_marker(hierarchy_level="auto")
        body += "\nSource run: https://github.com/owner/repo/actions/runs/123"
        assert recovery().classify(snapshot(comments=[comment(body)]))["inputs"]["hierarchy_level"] == "auto"

    def test_multiple_dispatch_markers_in_one_comment_fail_closed(self):
        body = dispatch_marker() + "\n" + dispatch_marker(phase="3")
        assert recovery().classify(snapshot(comments=[comment(body)]))["status"] == "failed"

    @pytest.mark.parametrize("root_issue", [False, None])
    def test_nested_or_unknown_parent_issue_cannot_infer_blank_spec_directory(self, root_issue):
        assert recovery().classify(snapshot(root_issue=root_issue))["status"] == "failed"

    @pytest.mark.parametrize("parent,expected", [(None, True), ({"number": 1}, False)])
    def test_provider_parent_inspection_proves_root_or_nested_issue(self, parent, expected):
        worker = recovery()
        worker.api_call.return_value = json.dumps({"data": {"repository": {"issue": {"parent": parent}}}})
        assert worker._root_issue(42) is expected
        assert worker.api_call.call_args.args[0] == "/graphql"
        assert worker.api_call.call_args.kwargs["body"]["variables"]["number"] == 42

    @pytest.mark.parametrize(
        "payload",
        [
            {"errors": [{"message": "permission denied"}]},
            {"data": {"repository": {"issue": {}}}},
            {"data": {"repository": {"issue": {"parent": []}}}},
        ],
    )
    def test_missing_or_invalid_parent_inspection_cannot_authorize_initial_replay(self, payload):
        worker = recovery()
        worker.api_call.return_value = json.dumps(payload)
        with pytest.raises(RuntimeError):
            worker._root_issue(42)

    def test_nested_issue_replays_only_its_exact_recorded_inputs(self):
        value = snapshot(root_issue=False, comments=[comment(dispatch_marker(hierarchy_level="auto", spec_dir=""))])
        assert recovery().classify(value)["inputs"]["spec_dir"] == ""

    @pytest.mark.parametrize(
        "requested,merged,status",
        [
            ("1", "1", "failed"),
            ("2", "2", "failed"),
            ("1", "3", "failed"),
            ("2", "1", "replay"),
            ("3", "3", "replay"),
            ("3", "4", "failed"),
            ("3", "5", "failed"),
        ],
    )
    def test_merged_phase_prs_reject_stale_markers_without_completion_labels(self, requested, merged, status):
        names = {"1": "specify", "2": "clarify", "3": "plan", "4": "tasks", "5": "analyze"}
        pr = {
            "number": 77,
            "state": "closed",
            "merged_at": START,
            "head": {"ref": f"speckit/42/phase-{merged}-{names[merged]}"},
        }
        value = snapshot(comments=[comment(dispatch_marker(phase=requested))], pulls=[pr])
        assert recovery().classify(value)["status"] == status

    def test_other_issue_run_pull_request_id_is_not_globally_unknown(self):
        other = {"number": 78, "state": "closed", "head": {"ref": "speckit/43/phase-1-specify"}}
        run = {"status": "queued", "pull_requests": [{"number": 78}]}
        assert recovery().classify(snapshot(pulls=[other], runs=[run]))["status"] == "replay"

    @pytest.mark.parametrize("merged,status", [(True, "failed"), (False, "replay")])
    def test_exact_marker_replays_closed_unmerged_phase_but_not_merged_phase(self, merged, status):
        pr = {"number": 77, "state": "closed", "merged": merged, "head": {"ref": "speckit/42/phase-2-clarify"}}
        assert recovery().classify(snapshot(pulls=[pr], comments=[comment(dispatch_marker())]))["status"] == status

    def test_merged_cloud_phase_also_rejects_superseded_recorded_input(self):
        cloud = (
            "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
            "issue=42 phase=2 hierarchy=feature correlation_id=12345678-1234-1234-1234-123456789abc -->"
        )
        pr = {"number": 77, "state": "closed", "merged_at": START, "head": {"ref": "copilot/clarify"}, "body": cloud}
        assert recovery().classify(snapshot(pulls=[pr], comments=[comment(dispatch_marker())]))["status"] == "failed"

    @pytest.mark.parametrize("events", [None, []])
    def test_recent_cloud_assignment_marker_protects_partial_label_failure(self, events):
        cloud = (
            "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
            "issue=42 phase=2 hierarchy=feature correlation_id=12345678-1234-1234-1234-123456789abc -->"
        )
        value = snapshot(comments=[comment(cloud, RECENT)])
        if events is not None:
            value["events"] = events
        assert recovery().classify(value)["reason"] == "recent-cloud-assignment-marker"

    def test_unrelated_cloud_assignment_marker_cannot_block_this_issue(self):
        cloud = (
            "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
            "issue=43 phase=2 hierarchy=feature correlation_id=12345678-1234-1234-1234-123456789abc -->"
        )
        assert recovery().classify(snapshot(comments=[comment(cloud, RECENT)]))["status"] == "replay"

    def test_stale_cloud_assignment_marker_can_supply_missing_event_age_without_guessing_inputs(self):
        cloud = (
            "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
            "issue=42 phase=2 hierarchy=feature correlation_id=12345678-1234-1234-1234-123456789abc -->"
        )
        assert recovery().classify(snapshot(events=[], comments=[comment(cloud)]))["status"] == "failed"

    def test_untrusted_cloud_assignment_marker_cannot_claim_live_work(self):
        cloud = (
            "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
            "issue=42 phase=2 hierarchy=feature correlation_id=12345678-1234-1234-1234-123456789abc -->"
        )
        value = snapshot(comments=[comment(cloud, RECENT, login="attacker")])
        assert recovery().classify(value)["status"] == "replay"

    def test_recent_malformed_progression_marker_waits_until_stale(self):
        value = snapshot(comments=[comment("<!-- speckit:progression-dispatch broken -->", RECENT)])
        assert recovery().classify(value)["reason"] == "processing-is-recent"

    @pytest.mark.parametrize("merged", [False, True])
    def test_exact_phase_three_repair_delegates_completed_artifact_validation_to_workflow(self, merged):
        pr = {"number": 77, "state": "closed", "merged": merged, "head": {"ref": "speckit/42/phase-3-plan"}}
        value = snapshot(
            labels={"speckit:processing", "speckit:phase-3-complete"},
            comments=[comment(dispatch_marker(phase="3"))],
            pulls=[pr],
        )
        decision = recovery().classify(value)
        assert decision["status"] == "replay"
        assert decision["inputs"]["phase"] == "3"

    @pytest.mark.parametrize("state,completed", [("closed", False), ("open", True)])
    def test_phase_three_repair_does_not_reopen_closed_or_completed_issue(self, state, completed):
        labels = {"speckit:processing"}
        if completed:
            labels.add("speckit:completed")
        value = snapshot(
            issue={"number": 42, "state": state}, labels=labels, comments=[comment(dispatch_marker(phase="3"))]
        )
        assert recovery().classify(value)["status"] == "skip"

    def test_later_completed_phase_still_vetoes_recorded_phase_three_replay(self):
        value = snapshot(
            labels={"speckit:processing", "speckit:phase-4-complete"}, comments=[comment(dispatch_marker(phase="3"))]
        )
        assert recovery().classify(value)["status"] == "failed"

    @pytest.mark.parametrize("own_id,expected", [(100, "replayed"), (101, "skip")])
    def test_same_input_reservations_elect_exactly_one_winner(self, own_id, expected):
        worker = recovery()
        digest = hashlib.sha256(json.dumps(worker.classify(snapshot())["inputs"], sort_keys=True).encode()).hexdigest()
        marker = f"<!-- speckit:progression-recovery schema_version=1 epoch=7 inputs_sha256={digest} -->"
        reservations = [{**comment(marker, RECENT), "id": number} for number in [101, 100]]
        worker.inspect = Mock(side_effect=[snapshot(), snapshot(), snapshot(comments=reservations)])
        worker.api_call.return_value = json.dumps({"id": own_id})
        assert worker.recover(42)["status"] == expected
        assert worker.api_call.call_count == (2 if expected == "replayed" else 1)

    @pytest.mark.parametrize(
        "kind", ["different-digest", "different-epoch", "untrusted", "invalid-id", "bool-id", "negative-id"]
    )
    def test_reservation_election_does_not_ignore_unrelated_or_invalid_evidence(self, kind):
        worker = recovery()
        decision = worker.classify(snapshot())
        digest = hashlib.sha256(json.dumps(decision["inputs"], sort_keys=True).encode()).hexdigest()
        marker = f"<!-- speckit:progression-recovery schema_version=1 epoch=7 inputs_sha256={digest} -->"
        own = {**comment(marker, RECENT), "id": 100}
        other = {**comment(marker, RECENT), "id": 99}
        if kind == "different-digest":
            other["body"] = marker.replace(digest, "other")
        elif kind == "different-epoch":
            other["body"] = marker.replace("epoch=7", "epoch=6")
        elif kind == "untrusted":
            other["user"] = {"login": "attacker"}
        else:
            other["id"] = {"invalid-id": None, "bool-id": True, "negative-id": -1}[kind]
        worker.inspect = Mock(return_value=snapshot(comments=[own, other]))
        if kind in {"invalid-id", "bool-id", "negative-id"}:
            with pytest.raises(RuntimeError, match="reservation identity"):
                worker._unchanged(42, decision, 100, marker)
        else:
            assert worker._unchanged(42, decision, 100, marker) is (kind != "different-digest")

    def test_own_reservation_must_be_trusted_and_exact(self):
        worker = recovery()
        worker.inspect = Mock(return_value=snapshot(comments=[{**comment("wrong"), "id": 100}]))
        with pytest.raises(RuntimeError, match="read back"):
            worker._unchanged(42, worker.classify(snapshot()), 100, "expected")

    def test_rerunning_old_completed_run_is_fresh_active_evidence(self):
        worker = recovery()
        worker._runs_cache = [{"id": 1, "status": "completed"}]
        rerun = {"id": 1, "status": "queued", "display_title": "issue #42"}
        worker._read = Mock(side_effect=[[], [], [rerun], [], [], []])
        assert worker.classify(snapshot(runs=worker._cached_runs()))["reason"] == "active-progression-run"
        assert "status=queued" in worker._read.call_args_list[2].args[0]
