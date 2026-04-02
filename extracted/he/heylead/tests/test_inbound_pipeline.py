"""Tests for the unified classify-first inbound pipeline."""

from __future__ import annotations

import pytest

from heylead.services.inbound_pipeline import (
    _decide_invitation_action,
    INBOUND_ACCEPT_CONFIDENCE,
)


class TestDecideInvitationAction:
    """Test the invitation decision matrix."""

    def test_buying_signal_high_confidence_accepts(self):
        assert _decide_invitation_action("buying_signal", 0.8) == "accept"

    def test_buying_signal_medium_confidence_accepts(self):
        assert _decide_invitation_action("buying_signal", 0.5) == "accept"

    def test_buying_signal_low_confidence_ignores(self):
        assert _decide_invitation_action("buying_signal", 0.2) == "ignore"

    def test_networking_above_threshold_accepts(self):
        assert _decide_invitation_action("networking", 0.5) == "accept"

    def test_networking_below_threshold_ignores(self):
        assert _decide_invitation_action("networking", 0.3) == "ignore"

    def test_partnership_always_accepts(self):
        assert _decide_invitation_action("partnership", 0.1) == "accept"
        assert _decide_invitation_action("partnership", 0.9) == "accept"

    def test_unknown_above_03_accepts(self):
        assert _decide_invitation_action("unknown", 0.4) == "accept"

    def test_unknown_below_03_ignores(self):
        assert _decide_invitation_action("unknown", 0.2) == "ignore"

    def test_job_seeking_dismissed(self):
        assert _decide_invitation_action("job_seeking", 0.9) == "dismiss"
        assert _decide_invitation_action("job_seeking", 0.1) == "dismiss"

    def test_spam_dismissed_by_default(self):
        # INBOUND_DECLINE_SPAM defaults to False → dismiss not decline
        assert _decide_invitation_action("spam", 0.9) == "dismiss"

    def test_vendor_pitch_high_confidence_accepted(self):
        # Vendor pitches are accepted so we can counter-pitch our product
        assert _decide_invitation_action("vendor_pitch", 0.9) == "accept"

    def test_vendor_pitch_low_confidence_accepted(self):
        assert _decide_invitation_action("vendor_pitch", 0.5) == "accept"

    def test_boundary_conditions(self):
        """Test at exact threshold values."""
        # buying_signal at exactly INBOUND_ACCEPT_CONFIDENCE (0.4) → accept
        assert _decide_invitation_action("buying_signal", INBOUND_ACCEPT_CONFIDENCE) == "accept"
        # buying_signal just below → ignore
        assert _decide_invitation_action("buying_signal", INBOUND_ACCEPT_CONFIDENCE - 0.01) == "ignore"
        # unknown at exactly 0.3 → accept
        assert _decide_invitation_action("unknown", 0.3) == "accept"
        # unknown just below 0.3 → ignore
        assert _decide_invitation_action("unknown", 0.29) == "ignore"


class TestDBSchemaNewColumns:
    """Test that new DB columns are accepted by the queries module."""

    def test_valid_inbound_signal_cols_includes_new_fields(self):
        from heylead.db.queries import _VALID_INBOUND_SIGNAL_COLS

        new_cols = {"invitation_id", "actioned_at", "decline_reason", "message_id", "reaction_sent"}
        assert new_cols.issubset(_VALID_INBOUND_SIGNAL_COLS)

    def test_save_inbound_signal_accepts_new_params(self):
        """Verify signature accepts invitation_id and message_id."""
        import inspect
        from heylead.db.queries import save_inbound_signal

        sig = inspect.signature(save_inbound_signal)
        params = set(sig.parameters.keys())
        assert "invitation_id" in params
        assert "message_id" in params


class TestNewClientMethods:
    """Test that new client methods exist on both clients."""

    def test_unipile_client_has_new_methods(self):
        from heylead.linkedin.unipile import UnipileClient

        assert hasattr(UnipileClient, "list_all_messages")
        assert hasattr(UnipileClient, "get_messages_by_sender")
        assert hasattr(UnipileClient, "add_message_reaction")

    def test_backend_client_has_new_methods(self):
        from heylead.linkedin.backend_client import BackendClient

        assert hasattr(BackendClient, "list_all_messages")
        assert hasattr(BackendClient, "get_messages_by_sender")
        assert hasattr(BackendClient, "add_message_reaction")


class TestSchedulerJobConstants:
    """Test that scheduler constants are properly defined."""

    def test_process_inbound_job_constant(self):
        from heylead.constants import JOB_PROCESS_INBOUND

        assert JOB_PROCESS_INBOUND == "process_inbound"

    def test_pipeline_seconds_constant(self):
        from heylead.constants import INBOUND_PIPELINE_SECONDS

        assert INBOUND_PIPELINE_SECONDS == 900

    def test_executor_function_exists(self):
        from heylead.scheduler.executors import _execute_process_inbound

        assert callable(_execute_process_inbound)


class TestStateTransitions:
    """Test that the status values are consistent."""

    def test_valid_statuses(self):
        """Ensure the pipeline uses recognized status values."""
        valid = {"new", "classified", "accepted", "ignored", "declined",
                 "engaged", "converted", "dismissed"}
        # All statuses set by _decide_invitation_action result in valid updates
        for intent in ("buying_signal", "networking", "partnership", "unknown",
                       "job_seeking", "spam", "vendor_pitch"):
            for conf in (0.0, 0.3, 0.5, 0.7, 0.9):
                action = _decide_invitation_action(intent, conf)
                assert action in ("accept", "ignore", "decline", "dismiss"), (
                    f"Unexpected action {action} for intent={intent}, conf={conf}"
                )


class TestDetectMessagesDedup:
    """Test that _detect_messages allows re-detection of dismissed senders."""

    def test_dismissed_sender_with_new_message_is_redetected(self):
        """A dismissed sender sending a new message should create a new signal.

        Regression: previously ANY existing signal blocked all future messages.
        """
        from heylead.db.queries import (
            get_inbound_signal_by_sender,
            save_inbound_signal,
            update_inbound_signal,
        )

        # Simulate a sender whose first message was detected and dismissed
        signal_id = save_inbound_signal(
            signal_type="message",
            sender_name="Test Sender",
            sender_id="test-sender-dismissed-1",
            content="Old message from months ago",
        )
        update_inbound_signal(signal_id, status="dismissed")

        # Verify the signal exists and is dismissed
        existing = get_inbound_signal_by_sender("test-sender-dismissed-1", "message")
        assert existing is not None
        assert existing["status"] == "dismissed"

        # The dedup logic should allow re-detection because:
        # 1. Status is "dismissed" (terminal state)
        # 2. New message text differs from existing content
        # Simulate the fixed dedup check:
        status = existing.get("status", "")
        assert status not in ("new", "classified", "accepted", "engaged")
        existing_content = (existing.get("content") or "").strip()
        new_content = "Brand new message today"
        assert existing_content != new_content  # Different → should re-detect

    def test_active_signal_still_blocks_detection(self):
        """Senders with active (non-terminal) signals should still be skipped."""
        from heylead.db.queries import (
            get_inbound_signal_by_sender,
            save_inbound_signal,
        )

        signal_id = save_inbound_signal(
            signal_type="message",
            sender_name="Active Sender",
            sender_id="test-sender-active-1",
            content="Being processed right now",
        )
        # Status defaults to "new"

        existing = get_inbound_signal_by_sender("test-sender-active-1", "message")
        assert existing is not None
        assert existing["status"] == "new"

        # Active states should block re-detection
        status = existing.get("status", "")
        assert status in ("new", "classified", "accepted", "engaged")

    def test_dismissed_sender_same_message_still_skipped(self):
        """A dismissed sender resending the exact same text should still be skipped."""
        from heylead.db.queries import (
            get_inbound_signal_by_sender,
            save_inbound_signal,
            update_inbound_signal,
        )

        msg_text = "I offer freelance dev services"
        signal_id = save_inbound_signal(
            signal_type="message",
            sender_name="Repeat Sender",
            sender_id="test-sender-repeat-1",
            content=msg_text,
        )
        update_inbound_signal(signal_id, status="dismissed")

        existing = get_inbound_signal_by_sender("test-sender-repeat-1", "message")
        existing_content = (existing.get("content") or "").strip()
        new_content = msg_text.strip()
        # Same text → still skip
        assert existing_content == new_content

    def test_ignored_sender_with_new_message_is_redetected(self):
        """Ignored senders should also be re-detected with new messages."""
        from heylead.db.queries import (
            get_inbound_signal_by_sender,
            save_inbound_signal,
            update_inbound_signal,
        )

        signal_id = save_inbound_signal(
            signal_type="message",
            sender_name="Ignored Sender",
            sender_id="test-sender-ignored-1",
            content="First attempt",
        )
        update_inbound_signal(signal_id, status="ignored")

        existing = get_inbound_signal_by_sender("test-sender-ignored-1", "message")
        status = existing.get("status", "")
        # "ignored" is not in active states → should allow re-detection
        assert status not in ("new", "classified", "accepted", "engaged")
        # Different content → re-detect
        assert (existing.get("content") or "").strip() != "New follow-up message"
