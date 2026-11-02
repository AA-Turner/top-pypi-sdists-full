"""Tests for provider-side critique Agent Tasks dispatch helpers."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.critique_provider import CritiqueProviderDispatch
from agentic_devtools.cli.ci.models import CheckRunStatus
from agentic_devtools.cli.ci.provider import RepairDispatchNotAttemptedError
from agentic_devtools.cli.ci.retry import ProviderRateLimitError


def test_build_repair_body_uses_contract_prompt_without_accounting_suffix() -> None:
    provider = MagicMock()
    standard_builder = MagicMock()
    size_enforcer = MagicMock()
    prompt = "@copilot please address the following critique of this pr:\n\nA parser regression loses data."

    body = CritiqueProviderDispatch.build_repair_body(
        provider,
        standard_builder,
        size_enforcer,
        5_000,
        agent_task_prompt=prompt,
        head_sha="head",
        repair_type="review",
        failed_checks=[],
        review_comments=[],
        repository_full_name="owner/repo",
        pr_number=42,
        review_id=100,
        check_contexts={},
        declared_author_comment_count=0,
        declared_author_comment_counts_by_review=None,
    )

    assert body == prompt
    assert "repair-dispatch-findings" not in body
    standard_builder.assert_not_called()
    size_enforcer.assert_not_called()
    provider.assert_not_called()


@pytest.mark.parametrize("repair_type", ["review", "ci"])
def test_build_repair_body_keeps_standard_comment_evidence_path(repair_type: str) -> None:
    provider = MagicMock()
    standard_builder = MagicMock(return_value="@copilot fix the issue")
    size_enforcer = MagicMock(side_effect=lambda body, *, hard_limit: body)
    failed_checks = (
        [CheckRunStatus(id=1, name="build", status="completed", conclusion="failure")] if repair_type == "ci" else []
    )
    with (
        patch("agentic_devtools.cli.ci.critique_provider.repair_work_key", return_value="work"),
        patch(
            "agentic_devtools.cli.ci.critique_provider.RepairDispatchLedger",
            return_value=MagicMock(evidence_marker="<!-- evidence -->"),
        ),
    ):
        body = CritiqueProviderDispatch.build_repair_body(
            provider,
            standard_builder,
            size_enforcer,
            5_000,
            agent_task_prompt=None,
            head_sha="head",
            repair_type=repair_type,
            failed_checks=failed_checks,
            review_comments=[],
            repository_full_name="owner/repo",
            pr_number=42,
            review_id=100,
            check_contexts={},
            declared_author_comment_count=0,
            declared_author_comment_counts_by_review=None,
        )

    assert body == "@copilot fix the issue\n\n<!-- evidence -->"
    standard_builder.assert_called_once()
    size_enforcer.assert_called_once()
    provider.assert_not_called()


def test_validate_task_dispatch_allows_noncritique_and_valid_critique_requests() -> None:
    CritiqueProviderDispatch.validate_task_dispatch(None, False, "")
    CritiqueProviderDispatch.validate_task_dispatch("prompt", True, "owner/repo")


@pytest.mark.parametrize(
    ("use_agent_tasks", "repository_full_name"),
    [(False, "owner/repo"), (True, ""), (True, "repository-without-owner")],
)
def test_validate_task_dispatch_rejects_unavailable_critique_routes(
    use_agent_tasks: bool, repository_full_name: str
) -> None:
    with pytest.raises(RepairDispatchNotAttemptedError, match="requires the Agent Tasks API"):
        CritiqueProviderDispatch.validate_task_dispatch("prompt", use_agent_tasks, repository_full_name)


def test_must_not_fallback_for_critique_or_rate_limit_errors_only() -> None:
    assert CritiqueProviderDispatch.must_not_fallback("critique prompt", RuntimeError("failure"))
    assert CritiqueProviderDispatch.must_not_fallback(None, ProviderRateLimitError())
    assert not CritiqueProviderDispatch.must_not_fallback(None, ProviderRateLimitError(is_rate_limit=False))
    assert not CritiqueProviderDispatch.must_not_fallback(None, RuntimeError("failure"))
