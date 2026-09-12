"""Focused tests for the AI PR Loop dispatch helper."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.pipeline.models import ActionDecision

_SCRIPT_PATH = Path(__file__).parents[2] / ".agents" / "skills" / "ai-pr-loop-dispatch" / "render_dispatch.py"
_SPEC = importlib.util.spec_from_file_location("ai_pr_loop_dispatch", _SCRIPT_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError(f"Could not load dispatch helper from {_SCRIPT_PATH!s}")
_dispatch = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_dispatch)


class TestTaskLinksComment:
    """Tests for compact per-comment tracking replies."""

    def test_collapses_long_task_text_in_table_cell(self) -> None:
        record = {
            "is_suppressed": False,
            "status": "completed",
            "thread_resolved": True,
            "task_url": "https://github.com/owner/repo/tasks/task-1",
            "file_path": "src/example.py",
            "line_range": "10",
            "original_comment": "[Original comment](https://github.com/owner/repo/pull/1#discussion_r2)",
            "comment_type": "inline",
            "agent_comment": None,
            "agent_task_text": "A long result\n" * 20,
        }

        body = _dispatch._build_task_result_comment(
            review_url="https://github.com/owner/repo/pull/1#pullrequestreview-3", ordinal=1, record=record
        )

        assert "<details><summary>Agent task text</summary>" in body
        assert "<pre>A long result" in body
        assert "| Comment # | 1 |" in body
        assert "| Resolution decision | - |" in body
        assert "| Follow-up issue | - |" in body

    def test_wraps_pending_values_in_collapsible_details(self) -> None:
        record = {
            "status": "queued",
            "task_url": "https://github.com/owner/repo/tasks/task-1",
            "file_path": "src/example.py",
            "line_range": "None",
            "original_comment": "[Original comment](https://github.com/owner/repo/pull/1#discussion_r2)",
            "comment_type": "inline",
            "agent_comment": "🔃",
            "agent_task_text": "🔃",
            "follow_up_issue": "-",
            "resolution_decision": "-",
            "resolution_basis": "-",
            "resolution_text": "-",
        }

        body = _dispatch._build_task_result_comment(review_url="review", ordinal=1, record=record)

        assert "<details>\n<summary>Agent task text</summary>\n\n🔃\n\n</details>" in body
        assert "<details>\n<summary>Resolution text</summary>\n\n-\n\n</details>" in body

    def test_uses_pending_values_before_task_finishes(self) -> None:
        record = {
            "status": "queued",
            "thread_resolved": False,
            "task_url": "https://github.com/owner/repo/tasks/task-1",
            "file_path": "src/example.py",
            "line_range": "None",
            "original_comment": "None",
            "comment_type": "inline",
            "agent_comment": "🔃",
            "agent_task_text": "🔃",
            "follow_up_issue": "-",
            "resolution_decision": "-",
            "resolution_text": "-",
        }

        body = _dispatch._build_task_result_comment(review_url="review", ordinal=1, record=record)

        assert "| Agent task status | 🔃 queued |" in body
        assert "| Resolution decision | - |" in body

    def test_renders_complete_sdk_resolution_text(self) -> None:
        record = {
            "status": "completed",
            "thread_resolved": True,
            "task_url": "https://github.com/owner/repo/tasks/task-1",
            "file_path": "src/example.py",
            "line_range": "10",
            "original_comment": "[Original comment](https://github.com/owner/repo/pull/1#discussion_r2)",
            "comment_type": "inline",
            "agent_comment": "https://github.com/owner/repo/pull/1#discussion_r3",
            "agent_task_text": "Implemented the fix.",
            "follow_up_issue": "None",
            "resolution_decision": "resolve",
            "resolution_text": "RESOLVE\nThe diff addresses the requested behavior.",
            "resolution_basis": "Copilot SDK adjudication",
        }

        body = _dispatch._build_task_result_comment(review_url="review", ordinal=1, record=record)

        assert "| Resolution decision | Resolve |" in body
        assert "| Resolution basis | Copilot SDK adjudication |" in body
        assert "The diff addresses the requested behavior." in body
        assert "| Agent reply to original comment | [3]" in body

    def test_renders_tracking_reply_as_two_column_tables(self) -> None:
        record = {
            "status": "completed",
            "thread_resolved": True,
            "task_url": "https://github.com/owner/repo/tasks/task-1",
            "file_path": "src/example.py",
            "line_range": "10",
            "original_comment": "[392](https://github.com/owner/repo/pull/1#discussion_r2)",
            "comment_type": "inline",
            "agent_comment": "https://github.com/owner/repo/pull/1#discussion_r3",
            "agent_task_text": "Implemented the fix.",
            "follow_up_issue": "None",
            "resolution_decision": "resolve",
            "resolution_basis": "Copilot SDK adjudication",
            "resolution_text": "AI_PR_LOOP_RESOLVE\nThe diff addresses the comment.",
        }

        body = _dispatch._build_task_result_comment(review_url="review", ordinal=1, record=record)

        assert body.startswith("| Field | Details |\n|---|---|\n")
        assert "| Comment # | 1 |" in body
        assert "| Agent task status | ✅ completed |" in body
        assert "| Agent reply to original comment | [3]" in body
        assert "| Agent task | [task-1]" in body
        assert "| Original comment | [2]" in body
        assert "| Follow-up issue | None |" in body
        assert "| Resolution decision | Resolve |" in body
        assert "| Resolution basis | Copilot SDK adjudication |" in body
        assert body.count("| Field | Details |") == 2
        assert "**Comment #**" not in body


class TestResumeState:
    """Tests for reusing existing task records without duplicate dispatches."""

    def test_parser_defaults_to_sequential_and_resume_is_explicit(self) -> None:
        args = _dispatch._build_parser().parse_args(
            ["--review-url", "https://github.com/owner/repo/pull/1#pullrequestreview-2"]
        )

        assert args.parallel is False
        assert args.resume is False

    def test_loads_only_matching_task_records(self, tmp_path: Path) -> None:
        state_path = tmp_path / "state.json"
        state_path.write_text(
            '{"owner":"owner","repo":"repo","pr_number":1,"review_id":2,'
            '"records":[{"task_id":"task-1","comment_id":7}, {"comment_id":8}]}',
            encoding="utf-8",
        )

        records = _dispatch._load_monitor_records(
            path=state_path,
            owner="owner",
            repo="repo",
            pr_number=1,
            review_id=2,
        )

        assert records == [{"task_id": "task-1", "comment_id": 7}]

    def test_complete_record_is_reused_by_comment_id(self) -> None:
        existing = {"task_id": "task-1", "comment_id": 7}
        prepared = {"comment_id": 7}

        assert _dispatch._find_resume_record([existing], prepared) is existing

    def test_complete_record_requires_verified_delivery(self) -> None:
        complete = {
            "task_id": "task-1",
            "status": "completed",
            "resolution_decision": "resolve",
            "push_verification": "verified",
            "thread_resolved": True,
        }

        assert _dispatch._record_is_complete(complete) is True
        assert _dispatch._record_is_complete({**complete, "push_verification": "unverified"}) is False


class TestUnresolvedReviewComments:
    """Tests for filtering review comments before task creation."""

    def test_filters_resolved_threads_and_keeps_unresolved_and_suppressed_comments(self) -> None:
        provider = MagicMock()
        provider.list_review_thread_states.return_value = {
            1: (True, True),
            2: (False, True),
        }
        comments = [
            SimpleNamespace(id=1),
            SimpleNamespace(id=2),
            SimpleNamespace(id=-1),
        ]

        result = _dispatch._filter_unresolved_review_comments(provider=provider, pr_number=4110, comments=comments)

        assert [comment.id for comment in result] == [2, -1]
        provider.list_review_thread_states.assert_called_once_with(4110)

    def test_keeps_comments_when_provider_has_no_thread_state_support(self) -> None:
        provider = SimpleNamespace()
        comments = [SimpleNamespace(id=1)]

        result = _dispatch._filter_unresolved_review_comments(provider=provider, pr_number=4110, comments=comments)

        assert result == comments

    def test_keeps_comments_when_thread_state_lookup_degrades(self) -> None:
        provider = MagicMock()
        provider.list_review_thread_states.side_effect = NotImplementedError
        comments = [SimpleNamespace(id=1)]

        result = _dispatch._filter_unresolved_review_comments(provider=provider, pr_number=4110, comments=comments)

        assert result == comments

    def test_returns_noop_when_all_recovered_comments_are_resolved(self) -> None:
        provider = MagicMock()
        provider.list_review_thread_states.return_value = {1: (True, True)}
        comments = [SimpleNamespace(id=1, is_suppressed=False, html_url="comment")]

        with (
            patch.object(_dispatch, "_build_parser") as build_parser,
            patch.object(_dispatch, "_parse_review_url", return_value=("owner", "repo", 4110, 5176679383)),
            patch.object(_dispatch, "_load_review_body", return_value="review"),
            patch.object(_dispatch, "_load_head_sha") as load_head_sha,
            patch.object(_dispatch.importlib, "import_module") as import_module,
        ):
            build_parser.return_value.parse_args.return_value = SimpleNamespace(
                review_url="review-url",
                content_file=None,
                post_task_link=False,
                dispatch_task=False,
                monitor=False,
                resume=False,
                poll_interval_seconds=300.0,
            )
            import_module.return_value = SimpleNamespace(
                GitHubActionsProvider=lambda _repository: provider,
                _build_repair_comment=lambda **_kwargs: "unused",
                _deduplicate_review_comments=lambda _comments, _suppressed: comments,
                _parse_suppressed_from_review_body=lambda _body, source_review_id: [],
            )

            assert _dispatch.main() == 0

        load_head_sha.assert_not_called()

    def test_skips_existing_resolved_suppressed_thread_before_dispatch(self, tmp_path: Path) -> None:
        provider = MagicMock()
        provider.list_review_thread_states.side_effect = [{}, {42: (True, True)}]
        suppressed_comment = SimpleNamespace(
            id=-1,
            is_suppressed=True,
            html_url="",
            body="finding",
            path="src/example.py",
            line=None,
            start_line=None,
        )

        with (
            patch.object(_dispatch, "_build_parser") as build_parser,
            patch.object(_dispatch, "_parse_review_url", return_value=("owner", "repo", 4110, 5176679383)),
            patch.object(_dispatch, "_load_review_body", return_value="review"),
            patch.object(_dispatch, "_load_head_sha", return_value="head-sha"),
            patch.object(_dispatch, "_load_pr_ref", side_effect=["main", "feature"]),
            patch.object(_dispatch, "_ensure_suppressed_review_thread", return_value=(42, "comment-url")),
            patch.object(_dispatch, "_dispatch_agent_task") as dispatch_agent_task,
            patch.object(_dispatch.importlib, "import_module") as import_module,
        ):
            build_parser.return_value.parse_args.return_value = SimpleNamespace(
                review_url="review-url",
                content_file=None,
                head_sha=None,
                dispatch_task=True,
                model=None,
                base_ref=None,
                head_ref=None,
                parallel=False,
                resume=False,
                post_task_link=False,
                monitor=False,
                poll_interval_seconds=300.0,
                output_dir=tmp_path,
            )
            import_module.return_value = SimpleNamespace(
                GitHubActionsProvider=lambda _repository: provider,
                _build_repair_comment=lambda **_kwargs: "unused",
                _deduplicate_review_comments=lambda _comments, _suppressed: [suppressed_comment],
                _parse_suppressed_from_review_body=lambda _body, source_review_id: [],
            )
            provider.list_review_comments.return_value = []

            assert _dispatch.main() == 0

        dispatch_agent_task.assert_not_called()

    def test_refreshes_thread_state_before_each_sequential_dispatch(self, tmp_path: Path) -> None:
        provider = MagicMock()
        fresh_provider_one = MagicMock()
        fresh_provider_two = MagicMock()
        provider.list_review_thread_states.return_value = {}
        fresh_provider_one.list_review_thread_states.return_value = {}
        fresh_provider_two.list_review_thread_states.return_value = {2: (True, True)}
        comments = [
            SimpleNamespace(
                id=1,
                is_suppressed=False,
                html_url="https://github.com/owner/repo/pull/4110#discussion_r1",
                body="first",
                path="src/first.py",
                line=1,
                start_line=None,
            ),
            SimpleNamespace(
                id=2,
                is_suppressed=False,
                html_url="https://github.com/owner/repo/pull/4110#discussion_r2",
                body="second",
                path="src/second.py",
                line=2,
                start_line=None,
            ),
        ]

        with (
            patch.object(_dispatch, "_build_parser") as build_parser,
            patch.object(_dispatch, "_parse_review_url", return_value=("owner", "repo", 4110, 5176679383)),
            patch.object(_dispatch, "_load_review_body", return_value="review"),
            patch.object(_dispatch, "_load_head_sha", return_value="head-sha"),
            patch.object(_dispatch, "_load_pr_ref", side_effect=["main", "feature"]),
            patch.object(_dispatch, "_dispatch_agent_task", return_value=("task-1", "task-url")) as dispatch_agent_task,
            patch.object(_dispatch.importlib, "import_module") as import_module,
        ):
            build_parser.return_value.parse_args.return_value = SimpleNamespace(
                review_url="review-url",
                content_file=None,
                head_sha=None,
                dispatch_task=True,
                model="model",
                base_ref=None,
                head_ref=None,
                parallel=False,
                resume=False,
                post_task_link=False,
                monitor=False,
                poll_interval_seconds=300.0,
                output_dir=tmp_path,
            )
            import_module.return_value = SimpleNamespace(
                GitHubActionsProvider=MagicMock(side_effect=[provider, fresh_provider_one, fresh_provider_two]),
                _build_repair_comment=lambda **_kwargs: "repair",
                _deduplicate_review_comments=lambda _comments, _suppressed: comments,
                _parse_suppressed_from_review_body=lambda _body, source_review_id: [],
            )
            provider.list_review_comments.return_value = comments

            assert _dispatch.main() == 0

        assert provider.list_review_thread_states.call_count == 1
        assert fresh_provider_one.list_review_thread_states.call_count == 1
        assert fresh_provider_two.list_review_thread_states.call_count == 1
        dispatch_agent_task.assert_called_once()


class TestAgentCommentCorrelation:
    """Tests for correlating a completed task with its assigned reply."""

    def test_matches_copilot_reply_by_parent_comment_id(self) -> None:
        provider = MagicMock()
        provider.list_all_review_comments.return_value = [
            SimpleNamespace(
                id=3924189115,
                in_reply_to_id=3924123761,
                html_url="https://github.com/owner/repo/pull/1#discussion_r3924189115",
                author_login="Copilot",
            )
        ]
        record = {"comment_id": 3924123761}

        result = _dispatch._find_agent_comment_url(
            provider=provider,
            pr_number=1,
            record=record,
            task_text="Replied to comment 3924123761.",
        )

        assert result == ("https://github.com/owner/repo/pull/1#discussion_r3924189115", True)


class TestTaskPushRecovery:
    """Tests for remote push verification and bounded task retries."""

    def test_reachable_commit_must_touch_assigned_file(self) -> None:
        record = {"status": "completed", "file_path": ".agents/skills/example/SKILL.md"}

        with (
            patch.object(_dispatch, "_reachable_reported_commits", return_value=["abc1234"]),
            patch.object(_dispatch, "_commit_touches_file", return_value=False),
        ):
            result = _dispatch._push_verification_status(
                owner="owner",
                repo="repo",
                pr_number=1,
                record=record,
                task_text="Commit: abc1234",
                agent_comment_text="",
            )

        assert result == "unverified"

    def test_retry_posts_steering_comment_and_tracks_request(self) -> None:
        provider = MagicMock()
        provider.post_comment_as_pr_token.return_value = 42
        record = {
            "task_id": "task-1",
            "task_url": "https://github.com/owner/repo/tasks/task-1",
            "file_path": "src/example.py",
            "line_range": "10",
            "original_comment": "[Original](https://github.com/owner/repo/pull/1#discussion_r2)",
            "session_id": "session-1",
            "retry_count": 0,
        }

        result = _dispatch._request_task_retry(
            owner="owner",
            repo="repo",
            provider=provider,
            pr_number=1,
            branch="feature/test",
            record=record,
            reason="remote commit could not be verified",
            task_text="Commit: abc1234\nPush was blocked.",
        )

        assert result == 42
        assert record["retry_count"] == 1
        assert record["retry_status"] == "requested"
        assert record["agent_comment"] == "🔃"
        assert record["agent_task_text"] == "🔃"
        body = provider.post_comment_as_pr_token.call_args.args[1]
        assert body.startswith("@copilot")
        assert "remote commit could not be verified" in body
        assert "task-1" in body
        assert "feature/test" in body

    def test_reachable_commit_touching_assigned_file_is_verified(self) -> None:
        record = {"status": "completed", "file_path": ".agents/skills/example/SKILL.md"}

        with (
            patch.object(_dispatch, "_reachable_reported_commits", return_value=["abc1234"]),
            patch.object(_dispatch, "_commit_touches_file", return_value=True),
        ):
            result = _dispatch._push_verification_status(
                owner="owner",
                repo="repo",
                pr_number=1,
                record=record,
                task_text="Commit: abc1234",
                agent_comment_text="",
            )

        assert result == "verified"

    def test_no_code_change_does_not_require_a_push(self) -> None:
        record = {"status": "completed", "file_path": "src/example.py"}

        with patch.object(_dispatch, "_reachable_reported_commits") as reachable:
            result = _dispatch._push_verification_status(
                owner="owner",
                repo="repo",
                pr_number=1,
                record=record,
                task_text="No code changes were needed.",
                agent_comment_text="",
            )

        assert result == "not_required"
        reachable.assert_called_once()

    def test_push_blocked_marker_prevents_no_code_shortcut(self) -> None:
        record = {"status": "completed", "file_path": "src/example.py"}

        with patch.object(_dispatch, "_reachable_reported_commits", return_value=[]):
            result = _dispatch._push_verification_status(
                owner="owner",
                repo="repo",
                pr_number=1,
                record=record,
                task_text="NO_CODE_CHANGE: true\nPUSH_BLOCKED: GH013",
                agent_comment_text="",
            )

        assert result == "unverified"

    def test_retry_state_activates_a_new_session(self) -> None:
        record = {
            "session_id": "session-1",
            "retry_status": "requested",
            "status": "retry_requested",
            "agent_comment": "old-reply",
            "agent_task_text": "old result",
            "resolution_decision": "do_not_resolve",
            "resolution_text": "old decision",
            "thread_resolved": False,
        }

        activated = _dispatch._advance_task_retry(
            record,
            {"state": "in_progress", "sessions": [{"id": "session-2", "state": "in_progress"}]},
        )

        assert activated is True
        assert record["session_id"] == "session-2"
        assert record["retry_status"] == "running"
        assert record["status"] == "in_progress"
        assert record["session_ids"] == ["session-2"]
        assert record["agent_comment"] == "🔃"
        assert record["agent_task_text"] == "🔃"

    def test_retry_state_exhausts_without_a_new_session(self) -> None:
        record = {
            "session_id": "session-1",
            "retry_status": "requested",
            "retry_poll_count": 2,
            "status": "retry_requested",
            "agent_comment": "old-reply",
            "agent_task_text": "old result",
            "resolution_decision": "-",
            "resolution_text": "-",
            "thread_resolved": False,
        }

        activated = _dispatch._advance_task_retry(record, {"state": "completed", "sessions": []})

        assert activated is False
        assert record["retry_status"] == "exhausted"
        assert record["status"] == "failed"
        assert record["agent_comment"] == "None"
        assert record["agent_task_text"] == "Retry session did not start."
        assert record["push_verification"] == "unverified"
        assert record["resolution_decision"] == "do_not_resolve"


class TestTaskResultReply:
    """Tests for creating one tracking reply per review comment."""

    @patch.object(_dispatch, "_load_token", return_value="token")
    @patch("agentic_devtools.ai_providers.RequestsHttpTransport")
    def test_posts_tracking_reply_and_returns_metadata(self, transport_type: MagicMock, _mock_token: MagicMock) -> None:
        transport_type.return_value.request.return_value = SimpleNamespace(
            status_code=201,
            body={"id": 9, "html_url": "https://github.com/owner/repo/pull/1#discussion_r9"},
        )

        result = _dispatch._post_task_result_reply(
            owner="owner", repo="repo", pr_number=1, comment_id=2, body="tracking"
        )

        assert result == (9, "https://github.com/owner/repo/pull/1#discussion_r9")
        transport_type.return_value.request.assert_called_once()

    @patch.object(_dispatch, "_load_token", return_value="token")
    @patch("agentic_devtools.ai_providers.RequestsHttpTransport")
    def test_updates_review_comment_tracking_reply(self, transport_type: MagicMock, _mock_token: MagicMock) -> None:
        transport_type.return_value.request.return_value = SimpleNamespace(status_code=200)

        _dispatch._update_task_result_reply(owner="owner", repo="repo", comment_id=9, body="updated")

        request = transport_type.return_value.request.call_args
        assert request.args[1] == "https://api.github.com/repos/owner/repo/pulls/comments/9"


class TestFollowUpIssueCreation:
    """Tests for dispatcher-owned follow-up issue creation."""

    @patch.object(_dispatch, "_load_token", return_value="token")
    @patch("agentic_devtools.ai_providers.RequestsHttpTransport")
    def test_creates_issue_and_returns_link(self, transport_type: MagicMock, _mock_token: MagicMock) -> None:
        transport_type.return_value.request.return_value = SimpleNamespace(
            status_code=201,
            body={"number": 1234, "html_url": "https://github.com/owner/repo/issues/1234"},
        )

        result = _dispatch._create_follow_up_issue(
            owner="owner",
            repo="repo",
            issue={"title": "Follow up", "body": "Details", "labels": ["bug"], "type": "Bug"},
        )

        assert result == (1234, "https://github.com/owner/repo/issues/1234")
        request = transport_type.return_value.request.call_args
        assert request.kwargs["json_body"] == {
            "title": "Follow up",
            "body": "Details",
            "labels": ["bug"],
            "type": "Bug",
        }


class TestFollowUpIssue:
    """Tests for structured option-four follow-up issues."""

    def test_parses_structured_follow_up_block(self) -> None:
        task_text = """Decision: option 4
<!-- ai-pr-loop:follow-up-issue -->
```json
{"title":"Improve docs","labels":["documentation"],"type":"Task","body":"Add examples."}
```
"""

        assert _dispatch._parse_follow_up_issue(task_text) == {
            "title": "Improve docs",
            "labels": ["documentation"],
            "type": "Task",
            "body": "Add examples.",
        }

    def test_rejects_invalid_follow_up_block(self) -> None:
        assert _dispatch._parse_follow_up_issue("Decision: option 4") is None


class TestResolutionAdjudication:
    """Tests for the Copilot SDK resolution decision."""

    @patch.object(_dispatch, "_run_copilot_adjudication", return_value="AI_PR_LOOP_RESOLVE\nThe fix is present.")
    def test_first_marker_resolve_allows_resolution(self, _mock_call: MagicMock) -> None:
        assert _dispatch._should_resolve_comment({"status": "completed"}, "prompt") is True

    @patch.object(_dispatch, "_run_copilot_adjudication", return_value="Reasoning... AI_PR_LOOP_RESOLVE")
    def test_scans_response_for_resolve_marker(self, _mock_call: MagicMock) -> None:
        decision, text = _dispatch._adjudicate_resolution({"status": "completed"}, "prompt")

        assert decision == "resolve"
        assert text.endswith("AI_PR_LOOP_RESOLVE")

    @patch.object(_dispatch, "_run_copilot_adjudication", return_value="AI_PR_LOOP_DO_NOT_RESOLVE\nThe fix is absent.")
    def test_only_exact_marker_blocks_resolution(self, _mock_call: MagicMock) -> None:
        assert _dispatch._should_resolve_comment({"status": "completed"}, "prompt") is False

    @patch.object(
        _dispatch,
        "_run_copilot_adjudication",
        return_value="AI_PR_LOOP_RESOLVE then AI_PR_LOOP_DO_NOT_RESOLVE",
    )
    def test_first_marker_wins(self, _mock_call: MagicMock) -> None:
        assert _dispatch._should_resolve_comment({"status": "completed"}, "prompt") is True

    @patch.object(
        _dispatch,
        "_run_copilot_adjudication",
        return_value="Thoughts mention AI_PR_LOOP_DO_NOT_RESOLVE before AI_PR_LOOP_RESOLVE",
    )
    def test_first_marker_wins_when_veto_is_in_thought_text(self, _mock_call: MagicMock) -> None:
        assert _dispatch._should_resolve_comment({"status": "completed"}, "prompt") is False

    @patch.object(
        _dispatch,
        "_run_copilot_adjudication",
        return_value="AI_PR_LOOP_RESOLVE\nThe diff addresses the comment.",
    )
    def test_preserves_complete_sdk_resolution_text(self, _mock_call: MagicMock) -> None:
        decision, text = _dispatch._adjudicate_resolution({"status": "completed"}, "prompt")

        assert decision == "resolve"
        assert text == "AI_PR_LOOP_RESOLVE\nThe diff addresses the comment."

    @patch.object(_dispatch, "_run_copilot_adjudication", return_value="AI_PR_LOOP_RESOLVE")
    def test_defaults_to_resolution(self, _mock_call: MagicMock) -> None:
        assert _dispatch._should_resolve_comment({"status": "completed"}, "prompt") is True

    @patch.object(_dispatch, "_run_copilot_adjudication", return_value="")
    def test_sdk_failure_leaves_thread_unresolved(self, _mock_call: MagicMock) -> None:
        assert _dispatch._should_resolve_comment({"status": "completed"}, "prompt") is False

    def test_no_marker_leaves_thread_unresolved_after_retry_wrapper(self) -> None:
        with patch.object(_dispatch, "_run_copilot_adjudication", return_value="No decision marker"):
            decision, text = _dispatch._adjudicate_resolution({"status": "completed"}, "prompt")

        assert decision == "do_not_resolve"
        assert "left unresolved" in text

    @patch.object(_dispatch.time, "sleep")
    @patch.object(
        _dispatch,
        "_run_single_copilot_adjudication",
        side_effect=["No marker", "Still no marker", "AI_PR_LOOP_RESOLVE\nDone"],
    )
    def test_retries_markerless_sdk_responses(self, call: MagicMock, sleep: MagicMock) -> None:
        assert _dispatch._run_copilot_adjudication("prompt") == "AI_PR_LOOP_RESOLVE\nDone"
        assert call.call_count == 3
        assert sleep.call_count == 2

    @patch.object(_dispatch.time, "sleep")
    @patch.object(
        _dispatch,
        "_run_single_copilot_adjudication",
        side_effect=[RuntimeError("transient"), "AI_PR_LOOP_DO_NOT_RESOLVE\nNo fix"],
    )
    def test_retries_transient_sdk_failure(self, call: MagicMock, sleep: MagicMock) -> None:
        assert _dispatch._run_copilot_adjudication("prompt") == "AI_PR_LOOP_DO_NOT_RESOLVE\nNo fix"
        assert call.call_count == 2
        sleep.assert_called_once_with(1.0)

    def test_deterministic_line_diff_is_resolution_basis(self) -> None:
        diff = """diff --git a/src/example.py b/src/example.py
--- a/src/example.py
+++ b/src/example.py
@@ -1,1 +1,2 @@
 line one
+line two
"""
        record = {"file_path": "src/example.py", "start_line": 2, "end_line": 2}

        assert _dispatch._deterministic_resolution_basis(diff, record) == "deterministic line diff"

    def test_adjudication_prompt_prioritizes_markers_and_reachable_commits(self) -> None:
        prompt = _dispatch._build_resolution_adjudication_prompt(
            record={"file_path": "src/example.py", "line_range": "2"},
            task_text="Implemented in abc1234.",
            file_diff="diff",
            deterministic_basis="deterministic line diff",
            reachable_commits=["abc1234"],
        )

        assert "absolute first characters" in prompt
        assert "first occurrence" in prompt
        assert "supporting context, not as automatic proof" in prompt
        assert '"deterministic_post_dispatch_evidence": "deterministic line diff"' in prompt
        assert '"reachable_reported_commits": [' in prompt
        assert "abc1234" in prompt

    @patch.object(_dispatch, "_PR_COMMIT_CACHE", {})
    @patch.object(_dispatch.subprocess, "run")
    def test_reports_only_reachable_commit_prefixes(self, run: MagicMock) -> None:
        run.return_value = SimpleNamespace(stdout="1111111111111111111111111111111111111111\n2222222\n")

        result = _dispatch._reachable_reported_commits(
            owner="owner",
            repo="repo",
            pr_number=1,
            reported=["2222222", "3333333"],
        )

        assert result == ["2222222"]


class TestTaskLogRecovery:
    """Tests for retaining useful task logs when the task command reports failure."""

    @patch.object(_dispatch.subprocess, "run")
    def test_keeps_log_output_when_agent_task_command_returns_nonzero(self, run: MagicMock) -> None:
        run.return_value = SimpleNamespace(returncode=1, stdout="", stderr="complete task log")

        assert _dispatch._load_task_log(owner="owner", repo="repo", session_id="session") == "complete task log"

    @patch.dict(_dispatch.os.environ, {"GH_TOKEN": "agent-task-token"}, clear=True)
    @patch.object(_dispatch.subprocess, "run")
    def test_agent_task_cli_does_not_inherit_rest_token(self, run: MagicMock) -> None:
        run.return_value = SimpleNamespace(returncode=0, stdout="complete task log", stderr="")

        _dispatch._load_task_log(owner="owner", repo="repo", session_id="session")

        assert "GH_TOKEN" not in run.call_args.kwargs["env"]

    def test_extracts_final_response_with_terminal_encoding_variant(self) -> None:
        log = """\nΓÅ╣∩╕Å End subagent: agdt.address-copilot-review.evaluate-and-respond
## Copilot Review Comment Resolution Summary
Already fixed in commit 6778531.
"""

        assert "Already fixed in commit" in _dispatch._extract_task_text(log)

    def test_terminal_task_text_uses_snapshot_message(self) -> None:
        assert _dispatch._terminal_task_text({"message": "Task finished."}) == "Task finished."

    def test_terminal_task_text_falls_back_when_snapshot_has_no_text(self) -> None:
        assert "no session log was available" in _dispatch._terminal_task_text({})


class TestFinalizedRecordRecovery:
    """Tests for resuming records that already have a final resolution."""

    def test_does_not_lookup_reply_body_for_finalized_record(self) -> None:
        provider = MagicMock()
        record = {
            "status": "completed",
            "agent_task_text": None,
            "agent_comment": "https://github.com/owner/repo/pull/1#discussion_r3",
            "resolution_decision": "resolve",
            "resolution_text": "Resolved.",
            "thread_resolved": True,
            "follow_up_issue": "None",
        }

        _dispatch._finalize_task_record(
            owner="owner",
            repo="repo",
            pr_number=1,
            provider=provider,
            record=record,
            snapshot={},
        )

        provider.list_all_review_comments.assert_not_called()

    @patch.object(_dispatch, "_build_file_change_evidence", return_value="diff")
    @patch.object(_dispatch, "_adjudicate_resolution", return_value=("resolve", "AI_PR_LOOP_RESOLVE\nDone"))
    @patch.object(_dispatch, "_deterministic_resolution_basis", return_value="deterministic line diff")
    @patch.object(_dispatch, "_load_post_task_diff", return_value="diff")
    @patch.object(_dispatch, "_push_verification_status", return_value="verified")
    def test_deterministic_diff_still_flows_through_adjudication(
        self,
        _push_verification: MagicMock,
        _load_diff: MagicMock,
        _deterministic_basis: MagicMock,
        adjudicate: MagicMock,
        _file_evidence: MagicMock,
    ) -> None:
        provider = MagicMock()
        record = {
            "status": "completed",
            "agent_task_text": "Implemented in abc1234.",
            "agent_comment": None,
            "agent_comment_text": "",
            "resolution_decision": "-",
            "resolution_text": "-",
            "thread_resolved": False,
            "follow_up_issue": "-",
            "file_path": "src/example.py",
            "line_range": "2",
            "start_line": 2,
            "end_line": 2,
            "initial_head_sha": "a" * 40,
        }

        with patch.object(_dispatch, "_resolve_completed_inline_comment"):
            _dispatch._finalize_task_record(
                owner="owner",
                repo="repo",
                pr_number=1,
                provider=provider,
                record=record,
                snapshot={},
            )

        adjudicate.assert_called_once()
        assert record["resolution_decision"] == "resolve"
        assert record["resolution_basis"] == "Copilot SDK adjudication (deterministic line diff)"


class TestFinalizedRecordPushRetry:
    """Tests for retrying a completed task whose commit is not remotely verified."""

    @patch.object(_dispatch, "_push_verification_status", return_value="unverified")
    def test_requests_retry_before_resolution_adjudication(self, _push_verification: MagicMock) -> None:
        provider = MagicMock()
        provider.post_comment_as_pr_token.return_value = 42
        record = {
            "status": "completed",
            "agent_task_text": "Commit: abc1234\nPush was blocked.",
            "agent_comment": None,
            "agent_comment_text": "",
            "resolution_decision": "-",
            "resolution_text": "-",
            "thread_resolved": False,
            "follow_up_issue": "-",
            "retry_count": 0,
            "file_path": "src/example.py",
        }

        _dispatch._finalize_task_record(
            owner="owner",
            repo="repo",
            pr_number=1,
            provider=provider,
            record=record,
            snapshot={"sessions": [{"id": "session-1", "state": "completed"}]},
        )

        provider.post_comment_as_pr_token.assert_called_once()
        assert record["retry_comment_id"] == 42
        assert record["status"] == "retry_requested"
        assert record["resolution_decision"] == "-"


class TestSuppressedReviewComment:
    """Tests for converting a suppressed finding into a review comment thread."""

    def test_builds_line_anchored_review_comment_payload(self) -> None:
        comment = SimpleNamespace(path="src/example.py:42", body="Please fix this")

        payload = _dispatch._build_suppressed_review_comment_payload(
            comment=comment,
            head_sha="a" * 40,
            marker="<!-- ai-pr-loop-dispatch-suppressed:7:1 -->",
        )

        assert payload == {
            "body": "<!-- ai-pr-loop-dispatch-suppressed:7:1 -->\n\nPlease fix this",
            "commit_id": "a" * 40,
            "path": "src/example.py",
            "line": 42,
            "side": "RIGHT",
        }

    @patch.object(_dispatch, "_load_token", return_value="token")
    @patch("agentic_devtools.ai_providers.RequestsHttpTransport")
    def test_retries_line_anchor_as_file_comment_after_validation_error(
        self, transport_type: MagicMock, _mock_token: MagicMock
    ) -> None:
        transport_type.return_value.request.side_effect = [
            SimpleNamespace(status_code=422, body={"message": "line is not part of diff"}),
            SimpleNamespace(
                status_code=201,
                body={"id": 11, "html_url": "https://github.com/owner/repo/pull/1#discussion_r11"},
            ),
        ]
        comment = SimpleNamespace(path="tests/example.py:35", body="Please fix this")

        result = _dispatch._post_suppressed_review_comment(
            owner="owner",
            repo="repo",
            pr_number=1,
            comment=comment,
            head_sha="a" * 40,
            marker="<!-- marker -->",
        )

        assert result == (11, "https://github.com/owner/repo/pull/1#discussion_r11")
        fallback_payload = transport_type.return_value.request.call_args_list[1].kwargs["json_body"]
        assert fallback_payload == {
            "body": "<!-- marker -->\n\nPlease fix this",
            "commit_id": "a" * 40,
            "path": "tests/example.py",
            "subject_type": "file",
        }


class TestTakeoverGate:
    """Tests for the post-monitor takeover gate."""

    def test_requires_completed_tasks_and_resolved_threads(self) -> None:
        complete = {"status": "completed", "thread_resolved": True, "push_verification": "verified"}
        unresolved = {"status": "completed", "thread_resolved": False}
        active = {"status": "in_progress", "thread_resolved": False}
        unverified = {"status": "completed", "thread_resolved": True, "push_verification": "unverified"}

        assert _dispatch._tasks_ready_for_takeover([complete]) is True
        assert _dispatch._tasks_ready_for_takeover([unresolved]) is False
        assert _dispatch._tasks_ready_for_takeover([active]) is False
        assert _dispatch._tasks_ready_for_takeover([unverified]) is False
        assert _dispatch._tasks_ready_for_takeover([]) is False

    @patch("agentic_devtools.cli.ci.pipeline.actions.takeover.TakeOverAutomationCommitAction")
    @patch("agentic_devtools.cli.ci.pipeline.snapshot.build_pr_state_snapshot")
    def test_executes_real_takeover_action_after_gate(
        self,
        build_snapshot: MagicMock,
        action_type: MagicMock,
    ) -> None:
        snapshot = MagicMock()
        build_snapshot.return_value = snapshot
        action = action_type.return_value
        action.evaluate.return_value = SimpleNamespace(decision=ActionDecision.EXECUTE)
        action.execute.return_value = SimpleNamespace(decision=ActionDecision.EXECUTE)
        provider = MagicMock()

        _dispatch._run_takeover_after_monitor(
            owner="owner",
            repo="repo",
            pr_number=1,
            provider=provider,
        )

        build_snapshot.assert_called_once_with(provider, 1)
        action.evaluate.assert_called_once()
        action.execute.assert_called_once()
