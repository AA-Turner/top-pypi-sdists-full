"""Tests for message-to-run router (#889)."""

from __future__ import annotations

from anteroom.services.message_router import resolve_disambiguation, route_message


def _run(run_id: str = "run-1", workflow_id: str = "issue_delivery", status: str = "running") -> dict:
    return {"id": run_id, "workflow_id": workflow_id, "status": status}


class TestRouteMessageNoRuns:
    def test_no_active_runs_spawns(self) -> None:
        result = route_message("deploy to staging", [])
        assert result.action == "spawn"

    def test_spawn_with_hint(self) -> None:
        result = route_message("deploy to staging", [])
        assert result.action == "spawn"
        assert result.spawn_hint == "deploy"

    def test_spawn_no_hint(self) -> None:
        result = route_message("hello world", [])
        assert result.action == "spawn"
        assert result.spawn_hint is None


class TestRouteMessageSingleRun:
    def test_cancel_that(self) -> None:
        result = route_message("cancel that", [_run()])
        assert result.action == "cancel"
        assert result.target_run_id == "run-1"

    def test_stop(self) -> None:
        result = route_message("stop", [_run()])
        assert result.action == "cancel"
        assert result.target_run_id == "run-1"

    def test_abort(self) -> None:
        result = route_message("abort", [_run()])
        assert result.action == "cancel"

    def test_nevermind(self) -> None:
        result = route_message("nevermind", [_run()])
        assert result.action == "cancel"

    def test_never_mind_two_words(self) -> None:
        result = route_message("never mind", [_run()])
        assert result.action == "cancel"

    def test_i_pushed_fixes(self) -> None:
        result = route_message("I pushed fixes", [_run()])
        assert result.action == "attach"
        assert result.target_run_id == "run-1"

    def test_done(self) -> None:
        result = route_message("done", [_run()])
        assert result.action == "attach"

    def test_ready(self) -> None:
        result = route_message("ready", [_run()])
        assert result.action == "attach"

    def test_finished(self) -> None:
        result = route_message("finished with the changes", [_run()])
        assert result.action == "attach"

    def test_heres(self) -> None:
        result = route_message("here's the updated config", [_run()])
        assert result.action == "attach"

    def test_actually_use_prod(self) -> None:
        result = route_message("actually use prod", [_run()])
        assert result.action == "update"
        assert result.target_run_id == "run-1"

    def test_wait(self) -> None:
        result = route_message("wait, change the branch", [_run()])
        assert result.action == "update"

    def test_use_x_instead(self) -> None:
        result = route_message("use staging instead", [_run()])
        assert result.action == "update"

    def test_replace_pattern(self) -> None:
        result = route_message("cancel that, deploy to prod instead", [_run()])
        assert result.action == "replace"
        assert result.target_run_id == "run-1"
        assert result.spawn_hint == "deploy"

    def test_unrecognized_spawns(self) -> None:
        result = route_message("tell me about the weather", [_run()])
        assert result.action == "spawn"


class TestRouteMessageMultipleRuns:
    def test_ambiguous_cancel_asks_user(self) -> None:
        runs = [_run("r1", "wf-a"), _run("r2", "wf-b")]
        result = route_message("cancel that", runs)
        assert result.action == "ask_user"
        assert result.clarification is not None
        assert "wf-a" in result.clarification
        assert "wf-b" in result.clarification

    def test_ambiguous_attach_asks_user(self) -> None:
        runs = [_run("r1"), _run("r2")]
        result = route_message("I pushed fixes", runs)
        assert result.action == "ask_user"

    def test_ambiguous_update_asks_user(self) -> None:
        runs = [_run("r1"), _run("r2")]
        result = route_message("actually use prod", runs)
        assert result.action == "ask_user"

    def test_no_intent_spawns(self) -> None:
        runs = [_run("r1"), _run("r2")]
        result = route_message("something unrelated", runs)
        assert result.action == "spawn"


# ---------------------------------------------------------------------------
# Disambiguation resolution (#889)
# ---------------------------------------------------------------------------


class TestResolveDisambiguation:
    def test_numeric_selection(self) -> None:
        runs = [_run("r1", "wf-a"), _run("r2", "wf-b")]
        assert resolve_disambiguation("1", runs) == "r1"
        assert resolve_disambiguation("2", runs) == "r2"
        assert resolve_disambiguation("#1", runs) == "r1"

    def test_out_of_range_returns_none(self) -> None:
        runs = [_run("r1")]
        assert resolve_disambiguation("5", runs) is None

    def test_ordinal_first_second(self) -> None:
        runs = [_run("r1"), _run("r2"), _run("r3")]
        assert resolve_disambiguation("the first one", runs) == "r1"
        assert resolve_disambiguation("second", runs) == "r2"
        assert resolve_disambiguation("third", runs) == "r3"

    def test_workflow_id_exact_match(self) -> None:
        runs = [_run("r1", "issue_delivery"), _run("r2", "code_review")]
        assert resolve_disambiguation("code_review", runs) == "r2"

    def test_workflow_id_substring_match(self) -> None:
        runs = [_run("r1", "issue_delivery"), _run("r2", "code_review")]
        assert resolve_disambiguation("review", runs) == "r2"

    def test_word_level_match(self) -> None:
        """Replies like 'the code review one' match by extracting words."""
        runs = [_run("r1", "issue_delivery"), _run("r2", "code_review")]
        assert resolve_disambiguation("the code review one", runs) == "r2"

    def test_word_level_unique_word(self) -> None:
        runs = [_run("r1", "deploy"), _run("r2", "code_review")]
        assert resolve_disambiguation("the deploy one", runs) == "r1"

    def test_ambiguous_word_returns_none(self) -> None:
        """If a word matches multiple runs, no resolution."""
        runs = [_run("r1", "code_deploy"), _run("r2", "code_review")]
        assert resolve_disambiguation("code", runs) is None

    def test_run_id_prefix_match(self) -> None:
        runs = [_run("abcd1234-5678-dead-beef"), _run("efgh5678-1234-cafe-babe")]
        assert resolve_disambiguation("abcd", runs) == "abcd1234-5678-dead-beef"

    def test_empty_text_returns_none(self) -> None:
        runs = [_run("r1")]
        assert resolve_disambiguation("", runs) is None

    def test_no_runs_returns_none(self) -> None:
        assert resolve_disambiguation("1", []) is None

    def test_no_match_returns_none(self) -> None:
        runs = [_run("r1", "deploy"), _run("r2", "review")]
        assert resolve_disambiguation("something completely different", runs) is None


# ---------------------------------------------------------------------------
# Cross-turn scenario tests (#889)
# ---------------------------------------------------------------------------


class TestCrossTurnScenarios:
    """Prove the routing model handles the scenarios from the #889 contract:
    deploy→cancel, code-review→attach, parallel runs→disambiguation."""

    def test_deploy_then_cancel(self) -> None:
        """User starts a deploy workflow, then says 'cancel that'."""
        runs = [_run("deploy-run-1", "deploy")]
        result = route_message("cancel that", runs)
        assert result.action == "cancel"
        assert result.target_run_id == "deploy-run-1"

    def test_deploy_then_replace(self) -> None:
        """User says 'cancel that and deploy to staging' — cancel + spawn = replace."""
        runs = [_run("deploy-run-1", "deploy")]
        result = route_message("cancel that and deploy to staging", runs)
        assert result.action == "replace"
        assert result.target_run_id == "deploy-run-1"

    def test_deploy_then_update(self) -> None:
        """User says 'actually deploy to staging instead' — update keyword."""
        runs = [_run("deploy-run-1", "deploy")]
        result = route_message("actually deploy to staging instead", runs)
        assert result.action == "update"
        assert result.target_run_id == "deploy-run-1"

    def test_code_review_then_attach(self) -> None:
        """User says 'I pushed fixes' to an active code review."""
        runs = [_run("review-run-1", "code_review")]
        result = route_message("I pushed fixes", runs)
        assert result.action == "attach"
        assert result.target_run_id == "review-run-1"

    def test_code_review_then_update(self) -> None:
        """User says 'actually focus on the auth module' — has 'actually' keyword."""
        runs = [_run("review-run-1", "code_review")]
        result = route_message("actually focus on the auth module", runs)
        assert result.action == "update"
        assert result.target_run_id == "review-run-1"

    def test_parallel_runs_disambiguation_then_cancel(self) -> None:
        """Two runs active, user picks one by number then cancels."""
        runs = [_run("r1", "deploy"), _run("r2", "code_review")]
        # First message is ambiguous
        result = route_message("cancel that", runs)
        assert result.action == "ask_user"

        # User replies with number — resolve to r1
        resolved_id = resolve_disambiguation("1", runs)
        assert resolved_id == "r1"
        # Re-route with just the selected run
        selected = [r for r in runs if r["id"] == resolved_id]
        result2 = route_message("cancel that", selected)
        assert result2.action == "cancel"
        assert result2.target_run_id == "r1"

    def test_parallel_runs_disambiguation_by_name(self) -> None:
        """User picks a run by workflow name."""
        runs = [_run("r1", "deploy"), _run("r2", "code_review")]
        resolved_id = resolve_disambiguation("the review one", runs)
        assert resolved_id == "r2"
