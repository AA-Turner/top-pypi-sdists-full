"""Only identical authenticated exhausted summaries suppress watchdog wakeups."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_SUPPRESSED_COMMENTS, CopilotGateVerdict
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot
from agentic_devtools.cli.ci.pipeline.summary import SUMMARY_SENTINEL
from agentic_devtools.cli.ci.repair_accounting import exhausted_repair_is_unchanged
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


@pytest.mark.parametrize(
    "body,head,key,expected",
    [
        ("unrelated", "head", "a" * 64, False),
        (SUMMARY_SENTINEL, "head", "a" * 64, False),
        (f"{SUMMARY_SENTINEL}\n<!-- repair-dispatch:exhausted:old:{'a' * 64} -->", "head", "a" * 64, False),
        (f"{SUMMARY_SENTINEL}\n<!-- repair-dispatch:exhausted:head:{'a' * 64} -->", "head", "a" * 64, True),
        (f"{SUMMARY_SENTINEL}\n<!-- repair-dispatch:exhausted:head:{'a' * 64} -->", "head", "b" * 64, False),
        (f"{SUMMARY_SENTINEL}\n<!-- repair-dispatch:exhausted:head:{'a' * 64} -->", "changed", "a" * 64, False),
    ],
)
def test_exhausted_repair_is_unchanged(body, head, key, expected) -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "bot"
    provider.list_issue_comments.return_value = [IssueCommentInfo(1, "bot", body)]
    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.snapshot_builder.build_pr_state_snapshot",
            return_value=PRStateSnapshot(pr_number=42, head_sha=head),
        ),
        patch("agentic_devtools.cli.ci.repair_accounting.repair_observation_key", return_value=key),
    ):
        assert exhausted_repair_is_unchanged(provider, 42, "head") is expected


@pytest.mark.parametrize(
    "marker_head,current_head,current_key,expected",
    [
        ("head", "head", "a" * 64, True),
        ("head", "head", "b" * 64, False),
        ("head", "changed", "a" * 64, False),
    ],
)
def test_exhausted_hold_suppresses_only_the_same_work(marker_head, current_head, current_key, expected) -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "bot"
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(
            1,
            "bot",
            f"{SUMMARY_SENTINEL}\n<!-- repair-dispatch:exhausted-hold:{marker_head}:{'a' * 64} -->",
        )
    ]
    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.snapshot_builder.build_pr_state_snapshot",
            return_value=PRStateSnapshot(pr_number=42, head_sha=current_head),
        ),
        patch(
            "agentic_devtools.cli.ci.repair_accounting.repair_hold_observation_key",
            return_value=current_key,
        ),
    ):
        assert exhausted_repair_is_unchanged(provider, 42, "head") is expected


def test_unavailable_hold_stays_active_until_inventory_can_be_fingerprinted() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "bot"
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(
            1,
            "bot",
            f"{SUMMARY_SENTINEL}\n<!-- repair-dispatch:exhausted-hold:head:unavailable -->",
        )
    ]
    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.snapshot_builder.build_pr_state_snapshot",
            return_value=PRStateSnapshot(pr_number=42, head_sha="head"),
        ),
        patch(
            "agentic_devtools.cli.ci.repair_accounting.repair_hold_observation_key",
            side_effect=RuntimeError("inventory unavailable"),
        ),
    ):
        assert exhausted_repair_is_unchanged(provider, 42, "head") is True


def test_unavailable_hold_releases_for_one_verification_pass_when_inventory_recovers() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "bot"
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(
            1,
            "bot",
            f"{SUMMARY_SENTINEL}\n<!-- repair-dispatch:exhausted-hold:head:unavailable -->",
        )
    ]
    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.snapshot_builder.build_pr_state_snapshot",
            return_value=PRStateSnapshot(pr_number=42, head_sha="head"),
        ),
        patch(
            "agentic_devtools.cli.ci.repair_accounting.repair_hold_observation_key",
            return_value="a" * 64,
        ),
    ):
        assert exhausted_repair_is_unchanged(provider, 42, "head") is False


def test_fingerprinted_hold_releases_for_one_pass_when_thread_inventory_recovers() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "bot"
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(1, "bot", f"{SUMMARY_SENTINEL}\n<!-- repair-dispatch:exhausted-hold:head:{'a' * 64} -->")
    ]
    snapshot = PRStateSnapshot(pr_number=42, head_sha="head")
    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.snapshot_builder.build_pr_state_snapshot",
            return_value=snapshot,
        ),
        patch("agentic_devtools.cli.ci.repair_accounting.repair_observation_key", return_value="b" * 64),
        patch("agentic_devtools.cli.ci.repair_accounting.repair_hold_observation_key", return_value="a" * 64),
    ):
        assert exhausted_repair_is_unchanged(provider, 42, "head") is False


def test_fingerprinted_hold_uses_fallback_when_thread_inventory_is_still_unavailable() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "bot"
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(1, "bot", f"{SUMMARY_SENTINEL}\n<!-- repair-dispatch:exhausted-hold:head:{'a' * 64} -->")
    ]
    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.snapshot_builder.build_pr_state_snapshot",
            return_value=PRStateSnapshot(pr_number=42, head_sha="head"),
        ),
        patch(
            "agentic_devtools.cli.ci.repair_accounting.repair_observation_key",
            side_effect=RuntimeError("thread inventory unavailable"),
        ),
        patch("agentic_devtools.cli.ci.repair_accounting.repair_hold_observation_key", return_value="a" * 64),
    ):
        assert exhausted_repair_is_unchanged(provider, 42, "head") is True


def test_fingerprinted_hold_propagates_thread_inventory_rate_limit() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "bot"
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(1, "bot", f"{SUMMARY_SENTINEL}\n<!-- repair-dispatch:exhausted-hold:head:{'a' * 64} -->")
    ]
    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.snapshot_builder.build_pr_state_snapshot",
            return_value=PRStateSnapshot(pr_number=42, head_sha="head"),
        ),
        patch(
            "agentic_devtools.cli.ci.repair_accounting.repair_observation_key",
            side_effect=ProviderRateLimitError(),
        ),
        pytest.raises(ProviderRateLimitError),
    ):
        exhausted_repair_is_unchanged(provider, 42, "head")


@pytest.mark.parametrize("hold_type", ["exhausted", "exhausted-hold"])
@pytest.mark.parametrize("completion", ["repair-satisfied", "suppressed-deferral"])
def test_exhaustion_hold_releases_when_same_head_suppressed_gate_passes(hold_type: str, completion: str) -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "bot"
    hold = f"<!-- repair-dispatch:{hold_type}:head:{'a' * 64} -->"
    provider.list_issue_comments.return_value = [IssueCommentInfo(1, "bot", f"{SUMMARY_SENTINEL}\n{hold}")]
    snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="head",
        head_changed_since_review=False,
        repair_satisfied_review_id=42 if completion == "repair-satisfied" else None,
        suppressed_deferral_review_id=42 if completion == "suppressed-deferral" else None,
        copilot_gate_verdict=CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=42,
            body_comment_count=0,
            suppressed_count=1,
        ),
    )
    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.snapshot_builder.build_pr_state_snapshot",
            return_value=snapshot,
        ),
        patch("agentic_devtools.cli.ci.repair_accounting.repair_observation_key", return_value="a" * 64),
        patch("agentic_devtools.cli.ci.repair_accounting.repair_hold_observation_key", return_value="a" * 64),
    ):
        assert exhausted_repair_is_unchanged(provider, 42, "head") is False


@pytest.mark.parametrize("hold_type", ["exhausted", "exhausted-hold"])
@pytest.mark.parametrize(
    "ci_status,unresolved_threads,repairable_threads",
    [
        ("failing", 0, 0),
        ("passing", 0, 1),
        ("passing", 1, 0),
    ],
    ids=["failing-ci", "repairable-prior-review", "unresolved-prior-review"],
)
def test_passing_review_gate_does_not_release_hold_with_remaining_work(
    hold_type: str, ci_status: str, unresolved_threads: int, repairable_threads: int
) -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "bot"
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(
            1,
            "bot",
            f"{SUMMARY_SENTINEL}\n<!-- repair-dispatch:{hold_type}:head:{'a' * 64} -->",
        )
    ]
    snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="head",
        review_state="APPROVED",
        ci_status=ci_status,
        unresolved_threads=unresolved_threads,
        repairable_threads=repairable_threads,
        copilot_gate_verdict=CopilotGateVerdict(passed=True, reason="clean"),
    )
    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.snapshot_builder.build_pr_state_snapshot",
            return_value=snapshot,
        ),
        patch(
            "agentic_devtools.cli.ci.repair_accounting.repair_observation_key",
            side_effect=RuntimeError("thread inventory unavailable") if hold_type == "exhausted-hold" else None,
            return_value="a" * 64,
        ),
        patch("agentic_devtools.cli.ci.repair_accounting.repair_hold_observation_key", return_value="a" * 64),
    ):
        assert exhausted_repair_is_unchanged(provider, 42, "head") is True


@pytest.mark.parametrize("hold_type", ["exhausted", "exhausted-hold"])
def test_suppressed_completion_does_not_release_hold_with_degraded_thread_state(hold_type: str) -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "bot"
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(
            1,
            "bot",
            f"{SUMMARY_SENTINEL}\n<!-- repair-dispatch:{hold_type}:head:{'a' * 64} -->",
        )
    ]
    snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="head",
        unresolved_threads_degraded=True,
        head_changed_since_review=False,
        repair_satisfied_review_id=42,
        copilot_gate_verdict=CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=42,
            body_comment_count=0,
            suppressed_count=1,
        ),
    )
    observation_error = RuntimeError("thread inventory unavailable") if hold_type == "exhausted-hold" else None
    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.snapshot_builder.build_pr_state_snapshot",
            return_value=snapshot,
        ),
        patch(
            "agentic_devtools.cli.ci.repair_accounting.repair_observation_key",
            side_effect=observation_error,
            return_value="a" * 64,
        ),
        patch("agentic_devtools.cli.ci.repair_accounting.repair_hold_observation_key", return_value="a" * 64),
    ):
        assert exhausted_repair_is_unchanged(provider, 42, "head") is True


def test_exhausted_hold_propagates_provider_rate_limit() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "bot"
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(1, "bot", f"{SUMMARY_SENTINEL}\n<!-- repair-dispatch:exhausted-hold:head:{'a' * 64} -->")
    ]
    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.snapshot_builder.build_pr_state_snapshot",
            return_value=PRStateSnapshot(pr_number=42, head_sha="head"),
        ),
        patch(
            "agentic_devtools.cli.ci.repair_accounting.repair_hold_observation_key",
            side_effect=ProviderRateLimitError(),
        ),
        pytest.raises(ProviderRateLimitError),
    ):
        exhausted_repair_is_unchanged(provider, 42, "head")


def test_exhausted_observation_builds_snapshot_without_promoting_findings() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "bot"
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(1, "bot", f"{SUMMARY_SENTINEL}\n<!-- repair-dispatch:exhausted:head:{'a' * 64} -->")
    ]
    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.snapshot_builder.build_pr_state_snapshot",
            return_value=PRStateSnapshot(pr_number=42, head_sha="head"),
        ) as build_snapshot,
        patch("agentic_devtools.cli.ci.repair_accounting.repair_observation_key", return_value="a" * 64),
    ):
        assert exhausted_repair_is_unchanged(provider, 42, "head") is True

    build_snapshot.assert_called_once_with(provider, 42, promote_findings=False)


def test_exhausted_hold_builds_snapshot_without_promoting_findings() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "bot"
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(
            1,
            "bot",
            f"{SUMMARY_SENTINEL}\n<!-- repair-dispatch:exhausted-hold:head:{'a' * 64} -->",
        )
    ]
    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.snapshot_builder.build_pr_state_snapshot",
            return_value=PRStateSnapshot(pr_number=42, head_sha="head"),
        ) as build_snapshot,
        patch("agentic_devtools.cli.ci.repair_accounting.repair_hold_observation_key", return_value="a" * 64),
    ):
        assert exhausted_repair_is_unchanged(provider, 42, "head") is True

    build_snapshot.assert_called_once_with(provider, 42, promote_findings=False)
