"""Tests for PublishAction."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.pipeline.actions.publish import PublishAction
from agentic_devtools.cli.ci.pipeline.delivery import InitialDeliveryOutcome
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.runner import run_pipeline
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.shared.retry import ProviderRateLimitError
from tests.unit.cli.ci.pipeline._verified_pr_provider import verified_pr_provider


class TestPublishAction:
    """Tests for publish action evaluation and execution."""

    def test_skip_when_not_draft(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, is_draft=False, has_changes=True)
        derived = DerivedState(snapshot)
        action = PublishAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "not a draft" in result.details

    def test_skip_when_no_changes(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, is_draft=True, has_changes=False)
        derived = DerivedState(snapshot)
        action = PublishAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP

    def test_skip_when_wip_title(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, is_draft=True, has_changes=True, title="[WIP] work in progress")
        derived = DerivedState(snapshot)
        action = PublishAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "WIP" in result.details

    def test_execute_when_draft_ready(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=True,
            has_changes=True,
            title="feat: add feature",
            head_sha="abc123",
            base_branch="main",
            head_branch="feature/x",
            base_repo_full_name="owner/repo",
        )
        derived = DerivedState(snapshot)
        action = PublishAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.publish.is_copilot_session_active_via_agent_task",
            return_value=False,
        ):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    @pytest.mark.parametrize("active_session", [True, None])
    def test_skip_when_session_active_or_inventory_unavailable(self, active_session: bool | None) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=True,
            has_changes=True,
            title="feat: add feature",
            base_repo_full_name="owner/repo",
            head_branch="copilot/issue-1-fix",
        )
        action = PublishAction()
        provider = MagicMock()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.publish.is_copilot_session_active_via_agent_task",
            return_value=active_session,
        ) as mock_detector:
            summary = run_pipeline(provider, snapshot, [action])
        mock_detector.assert_called_once_with(
            "owner/repo",
            1,
            head_branch="copilot/issue-1-fix",
            pr_id=None,
            head_sha=snapshot.head_sha,
            provider=provider,
        )
        result = summary.results[0]
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["no_active_session"] is False
        assert "publish blocked" in result.details
        provider.squash_before_publish.assert_not_called()
        provider.publish_pr.assert_not_called()

    def test_execute_updates_derived_state(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=True,
            has_changes=True,
            title="feat: add feature",
            head_sha="abc123",
            base_branch="main",
            head_branch="feature/x",
        )
        derived = DerivedState(snapshot)
        provider = verified_pr_provider(1, "abc123", ["src/main.py"])
        result = PublishAction().execute(provider, snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert result.details == "Published draft PR after pre-publish branch preparation"
        assert result.invalidates_snapshot is True
        assert derived.is_draft is False
        provider.squash_before_publish.assert_called_once()
        provider.publish_pr.assert_called_once_with(1)

    @pytest.mark.parametrize(
        ("post_preparation_outcome", "should_publish"),
        [
            (InitialDeliveryOutcome.NO_DELIVERY, False),
            (InitialDeliveryOutcome.UNKNOWN, False),
            (InitialDeliveryOutcome.DELIVERED, True),
        ],
    )
    def test_wip_draft_rechecks_delivery_after_branch_preparation(
        self,
        post_preparation_outcome: InitialDeliveryOutcome,
        should_publish: bool,
    ) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=True,
            has_changes=True,
            files=["src/main.py"],
            title="[wip] completed work",
            head_sha="abc123",
            base_branch="main",
            head_branch="feature/x",
        )
        derived = DerivedState(snapshot)
        derived.set("latest_session_state", SessionState(SessionOutcome.FINISHED))
        provider = MagicMock()
        action = PublishAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.publish.classify_initial_delivery",
            side_effect=[InitialDeliveryOutcome.DELIVERED, post_preparation_outcome],
        ) as classify:
            result = action.execute(provider, snapshot, derived)
        assert classify.call_count == 2
        if should_publish:
            assert result.decision is ActionDecision.EXECUTE
            provider.update_pr_title.assert_called_once_with(1, "completed work")
            provider.publish_pr.assert_called_once_with(1)
        else:
            assert result.decision is ActionDecision.SKIP
            assert result.invalidates_snapshot is True
            assert result.preserves_diff_fingerprint is True
            provider.update_pr_title.assert_not_called()
            provider.publish_pr.assert_not_called()
        provider.squash_before_publish.assert_called_once()

    def test_successful_wip_evaluation_checks_fresh_active_session_inventory(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=True,
            has_changes=True,
            files=["src/main.py"],
            title="[WIP] completed work",
        )
        derived = DerivedState(snapshot)
        derived.set("latest_session_state", SessionState(SessionOutcome.FINISHED))
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.publish.is_copilot_session_active_via_agent_task",
                return_value=False,
            ) as mock_detector,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.publish.classify_initial_delivery",
                return_value=InitialDeliveryOutcome.DELIVERED,
            ),
        ):
            result = PublishAction().evaluate(snapshot, derived)
        assert result.decision is ActionDecision.EXECUTE
        assert result.preconditions["no_active_session"] is True
        mock_detector.assert_called_once()

    def test_successful_wip_draft_is_blocked_by_fresh_active_writer(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=True,
            has_changes=True,
            files=["src/main.py"],
            title="[WIP] completed work",
            base_repo_full_name="owner/repo",
            head_branch="copilot/feature",
        )
        derived = DerivedState(snapshot)
        derived.set("latest_session_state", SessionState(SessionOutcome.FINISHED))
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.publish.is_copilot_session_active_via_agent_task",
                return_value=True,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.publish.classify_initial_delivery",
                return_value=InitialDeliveryOutcome.DELIVERED,
            ),
        ):
            result = PublishAction().evaluate(snapshot, derived)

        assert result.decision is ActionDecision.SKIP
        assert result.preconditions["no_active_session"] is False
        assert "publish blocked" in result.details

    @pytest.mark.parametrize(
        "outcome",
        [InitialDeliveryOutcome.NO_DELIVERY, InitialDeliveryOutcome.UNKNOWN],
    )
    def test_empty_or_unknown_wip_delivery_cannot_be_published(self, outcome: InitialDeliveryOutcome) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=True,
            has_changes=True,
            files=["src/main.py"],
            title="[WIP] completed work",
        )
        derived = DerivedState(snapshot)
        derived.set("latest_session_state", SessionState(SessionOutcome.FINISHED))
        provider = MagicMock()
        derived.set("provider", provider)

        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.publish.classify_initial_delivery",
            return_value=outcome,
        ):
            result = PublishAction().evaluate(snapshot, derived)

        assert result.decision is ActionDecision.SKIP
        provider.squash_before_publish.assert_not_called()
        provider.publish_pr.assert_not_called()

    def test_execute_rechecks_wip_delivery_before_success_side_effects(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=True,
            has_changes=True,
            files=["src/main.py"],
            title="[WIP] completed work",
        )
        derived = DerivedState(snapshot)
        derived.set("latest_session_state", SessionState(SessionOutcome.FINISHED))
        provider = MagicMock()

        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.publish.classify_initial_delivery",
            return_value=InitialDeliveryOutcome.UNKNOWN,
        ):
            result = PublishAction().execute(provider, snapshot, derived)

        assert result.decision is ActionDecision.SKIP
        provider.squash_before_publish.assert_not_called()
        provider.publish_pr.assert_not_called()

    def test_post_preparation_rate_limit_preserves_snapshot_invalidation(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=True,
            has_changes=True,
            files=["src/main.py"],
            title="[WIP] completed work",
        )
        derived = DerivedState(snapshot)
        derived.set("latest_session_state", SessionState(SessionOutcome.FINISHED))
        provider = MagicMock()
        error = ProviderRateLimitError(provider="github", is_rate_limit=True)
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.publish.classify_initial_delivery",
                side_effect=[InitialDeliveryOutcome.DELIVERED, error],
            ),
            pytest.raises(ProviderRateLimitError) as exc_info,
        ):
            PublishAction().execute(provider, snapshot, derived)

        assert exc_info.value is error
        assert getattr(exc_info.value, "invalidates_snapshot", False) is True
        assert getattr(exc_info.value, "preserves_diff_fingerprint", False) is True
        provider.squash_before_publish.assert_called_once()
        provider.update_pr_title.assert_not_called()
        provider.publish_pr.assert_not_called()

    def test_post_preparation_non_rate_limit_error_blocks_publication(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=True,
            has_changes=True,
            files=["src/main.py"],
            title="[WIP] completed work",
        )
        derived = DerivedState(snapshot)
        derived.set("latest_session_state", SessionState(SessionOutcome.FINISHED))
        provider = MagicMock()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.publish.classify_initial_delivery",
            side_effect=[
                InitialDeliveryOutcome.DELIVERED,
                ProviderRateLimitError(provider="github", is_rate_limit=False),
            ],
        ):
            result = PublishAction().execute(provider, snapshot, derived)
        assert result.decision is ActionDecision.SKIP
        assert result.invalidates_snapshot is True
        provider.update_pr_title.assert_not_called()
        provider.publish_pr.assert_not_called()

    @pytest.mark.parametrize(
        ("is_draft", "has_changes", "session_state"),
        [
            (False, True, SessionState(SessionOutcome.FINISHED)),
            (True, False, SessionState(SessionOutcome.FINISHED)),
            (True, True, None),
            (True, True, SessionState(SessionOutcome.FAILED)),
        ],
    )
    def test_wip_execution_requires_draft_changes_and_finished_session(
        self,
        is_draft: bool,
        has_changes: bool,
        session_state: SessionState | None,
    ) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=is_draft,
            has_changes=has_changes,
            files=["src/main.py"] if has_changes else [],
            title="[WIP] work",
        )
        derived = DerivedState(snapshot)
        if session_state is not None:
            derived.set("latest_session_state", session_state)
        provider = MagicMock()
        result = PublishAction().execute(provider, snapshot, derived)
        assert result.decision is ActionDecision.SKIP
        provider.squash_before_publish.assert_not_called()

    def test_successful_wip_with_empty_title_text_fails_before_squash(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=True,
            has_changes=True,
            files=["src/main.py"],
            title="[WIP]",
        )
        derived = DerivedState(snapshot)
        derived.set("latest_session_state", SessionState(SessionOutcome.FINISHED))
        provider = MagicMock()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.publish.classify_initial_delivery",
            return_value=InitialDeliveryOutcome.DELIVERED,
        ):
            result = PublishAction().execute(provider, snapshot, derived)
        assert result.decision is ActionDecision.FAILED
        assert "no title text" in result.error
        provider.squash_before_publish.assert_not_called()
        provider.publish_pr.assert_not_called()

    def test_title_normalization_failure_does_not_publish(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=True,
            has_changes=True,
            files=["src/main.py"],
            title="[WIP] completed work",
            head_sha="abc123",
            base_branch="main",
            head_branch="feature/x",
        )
        derived = DerivedState(snapshot)
        derived.set("latest_session_state", SessionState(SessionOutcome.FINISHED))
        provider = MagicMock()
        provider.update_pr_title.side_effect = RuntimeError("title update failed")
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.publish.classify_initial_delivery",
            return_value=InitialDeliveryOutcome.DELIVERED,
        ):
            result = PublishAction().execute(provider, snapshot, derived)
        assert result.decision is ActionDecision.FAILED
        assert result.error == "title update failed"
        provider.publish_pr.assert_not_called()

    def test_title_normalization_reraises_rate_limit(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=True,
            has_changes=True,
            files=["src/main.py"],
            title="[WIP] completed work",
        )
        derived = DerivedState(snapshot)
        derived.set("latest_session_state", SessionState(SessionOutcome.FINISHED))
        provider = MagicMock()
        provider.update_pr_title.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
        )
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.publish.classify_initial_delivery",
                return_value=InitialDeliveryOutcome.DELIVERED,
            ),
            pytest.raises(ProviderRateLimitError) as exc_info,
        ):
            PublishAction().execute(provider, snapshot, derived)
        assert bool(getattr(exc_info.value, "invalidates_snapshot", False)) is True
        assert bool(getattr(exc_info.value, "preserves_diff_fingerprint", False)) is True

    def test_execute_fails_when_squash_before_publish_raises(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=True,
            has_changes=True,
            title="feat: add feature",
            head_sha="abc123",
            base_branch="main",
            head_branch="feature/x",
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.squash_before_publish.side_effect = RuntimeError("push failed")
        action = PublishAction()
        result = action.execute(provider, snapshot, derived)
        assert result.decision == ActionDecision.FAILED
        assert result.details == "squash_before_publish failed"
        assert result.error == "push failed"
        assert result.invalidates_snapshot is True
        assert result.preserves_diff_fingerprint is True
        provider.publish_pr.assert_not_called()

    def test_execute_fails_when_publish_raises(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=True,
            has_changes=True,
            title="feat: add feature",
            head_sha="abc123",
            base_branch="main",
            head_branch="feature/x",
        )
        derived = DerivedState(snapshot)
        provider = verified_pr_provider(1, "abc123", ["src/main.py"])
        provider.publish_pr.side_effect = RuntimeError("publish failed")
        action = PublishAction()
        result = action.execute(provider, snapshot, derived)
        assert result.decision == ActionDecision.FAILED
        assert result.details == "publish_pr failed"
        assert result.error == "publish failed"
        assert result.invalidates_snapshot is True
        assert result.preserves_diff_fingerprint is True

    def test_execute_reraises_rate_limit_from_squash(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=True,
            has_changes=True,
            title="feat: add feature",
            head_sha="abc123",
            base_branch="main",
            head_branch="feature/x",
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.squash_before_publish.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
        )
        action = PublishAction()
        with pytest.raises(ProviderRateLimitError) as exc_info:
            action.execute(provider, snapshot, derived)
        assert bool(getattr(exc_info.value, "invalidates_snapshot", False)) is True
        assert bool(getattr(exc_info.value, "preserves_diff_fingerprint", False)) is True

    def test_execute_reraises_rate_limit_from_publish(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=True,
            has_changes=True,
            title="feat: add feature",
            head_sha="abc123",
            base_branch="main",
            head_branch="feature/x",
        )
        derived = DerivedState(snapshot)
        provider = verified_pr_provider(1, "abc123", ["src/main.py"])
        provider.publish_pr.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
        )
        action = PublishAction()
        with pytest.raises(ProviderRateLimitError) as exc_info:
            action.execute(provider, snapshot, derived)
        assert bool(getattr(exc_info.value, "invalidates_snapshot", False)) is True
        assert bool(getattr(exc_info.value, "preserves_diff_fingerprint", False)) is True
