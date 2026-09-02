"""Tests for takeover_eval_prs()."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.audit import takeover as takeover_mod
from agentic_devtools.cli.audit.takeover import takeover_eval_prs


def _meta(head_sha: str = "sha", head_branch: str = "copilot/x", base_branch: str = "main") -> MagicMock:
    meta = MagicMock()
    meta.head_sha = head_sha
    meta.head_branch = head_branch
    meta.base_branch = base_branch
    return meta


def _brief(number: int, head_branch: str = "copilot/x", created_at: str = "2026-01-01") -> dict:
    return {"number": number, "head_branch": head_branch, "created_at": created_at}


class TestTakeoverEvalPrs:
    """Tests for the scheduled eval-PR takeover orchestration."""

    def test_no_candidates(self) -> None:
        provider = MagicMock()
        provider.list_open_copilot_pr_briefs.return_value = []
        result = takeover_eval_prs(provider, repo="o/r", max_prs=1)
        assert result == {"candidates": 0, "processed": []}

    @patch.object(takeover_mod, "is_copilot_session_active_via_agent_task", return_value=False)
    def test_processes_eligible_pr(self, _session: MagicMock) -> None:
        provider = MagicMock()
        provider.list_open_copilot_pr_briefs.return_value = [_brief(11)]
        provider.list_pr_files.return_value = ["audit-batches/a/agent-output/x.md"]
        provider.get_pr_metadata.return_value = _meta()
        provider.get_commit_author_login.return_value = "Copilot"
        result = takeover_eval_prs(provider, repo="o/r", max_prs=1)
        assert result["candidates"] == 1
        assert result["processed"] == [{"pr_number": 11, "outcome": "squashed"}]
        provider.squash_before_publish.assert_called_once()

    @patch.object(takeover_mod, "is_copilot_session_active_via_agent_task", return_value=False)
    def test_skips_non_agent_output(self, _session: MagicMock) -> None:
        provider = MagicMock()
        provider.list_open_copilot_pr_briefs.return_value = [_brief(12)]
        provider.list_pr_files.return_value = ["src/main.py"]
        result = takeover_eval_prs(provider, repo="o/r", max_prs=1)
        assert result["processed"] == []
        provider.get_pr_metadata.assert_not_called()

    @patch.object(takeover_mod, "is_copilot_session_active_via_agent_task", return_value=False)
    def test_skips_human_authored_head(self, _session: MagicMock) -> None:
        provider = MagicMock()
        provider.list_open_copilot_pr_briefs.return_value = [_brief(13)]
        provider.list_pr_files.return_value = ["audit-batches/a/agent-output/x.md"]
        provider.get_pr_metadata.return_value = _meta()
        provider.get_commit_author_login.return_value = "AMARSNIK_swica"
        result = takeover_eval_prs(provider, repo="o/r", max_prs=1)
        assert result["processed"] == []
        provider.squash_before_publish.assert_not_called()

    @patch.object(takeover_mod, "is_copilot_session_active_via_agent_task", return_value=False)
    def test_treats_author_lookup_failure_as_not_eligible(self, _session: MagicMock) -> None:
        provider = MagicMock()
        provider.list_open_copilot_pr_briefs.return_value = [_brief(14)]
        provider.list_pr_files.return_value = ["audit-batches/a/agent-output/x.md"]
        provider.get_pr_metadata.return_value = _meta()
        provider.get_commit_author_login.side_effect = RuntimeError("api down")
        result = takeover_eval_prs(provider, repo="o/r", max_prs=1)
        assert result["processed"] == []

    @patch.object(takeover_mod, "is_copilot_session_active_via_agent_task", return_value=True)
    def test_skips_when_session_active(self, _session: MagicMock) -> None:
        provider = MagicMock()
        provider.list_open_copilot_pr_briefs.return_value = [_brief(15)]
        provider.list_pr_files.return_value = ["audit-batches/a/agent-output/x.md"]
        provider.get_pr_metadata.return_value = _meta()
        provider.get_commit_author_login.return_value = "copilot-swe-agent[bot]"
        result = takeover_eval_prs(provider, repo="o/r", max_prs=1)
        assert result["processed"] == []
        provider.squash_before_publish.assert_not_called()

    @patch.object(takeover_mod, "is_copilot_session_active_via_agent_task", return_value=False)
    def test_respects_max_prs(self, _session: MagicMock) -> None:
        provider = MagicMock()
        provider.list_open_copilot_pr_briefs.return_value = [
            _brief(21, head_branch="copilot/a", created_at="2026-01-01"),
            _brief(22, head_branch="copilot/b", created_at="2026-01-02"),
        ]
        provider.list_pr_files.return_value = ["audit-batches/a/agent-output/x.md"]
        provider.get_pr_metadata.return_value = _meta()
        provider.get_commit_author_login.return_value = "Copilot"
        result = takeover_eval_prs(provider, repo="o/r", max_prs=1)
        assert result["candidates"] == 2
        assert len(result["processed"]) == 1

    def test_skips_malformed_brief(self) -> None:
        provider = MagicMock()
        provider.list_open_copilot_pr_briefs.return_value = [{"not_a_number": "bad"}]
        result = takeover_eval_prs(provider, repo="o/r", max_prs=1)
        assert result["processed"] == []
        provider.list_pr_files.assert_not_called()

    def test_skips_on_list_pr_files_error(self) -> None:
        provider = MagicMock()
        provider.list_open_copilot_pr_briefs.return_value = [_brief(30)]
        provider.list_pr_files.side_effect = RuntimeError("network error")
        result = takeover_eval_prs(provider, repo="o/r", max_prs=1)
        assert result["processed"] == []
        provider.get_pr_metadata.assert_not_called()

    def test_skips_on_get_pr_metadata_error(self) -> None:
        provider = MagicMock()
        provider.list_open_copilot_pr_briefs.return_value = [_brief(31)]
        provider.list_pr_files.return_value = ["audit-batches/a/agent-output/x.md"]
        provider.get_pr_metadata.side_effect = RuntimeError("api error")
        result = takeover_eval_prs(provider, repo="o/r", max_prs=1)
        assert result["processed"] == []
        provider.squash_before_publish.assert_not_called()
