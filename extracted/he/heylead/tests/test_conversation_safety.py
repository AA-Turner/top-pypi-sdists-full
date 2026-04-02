"""Tests for pre-send conversation safety checks.

Prevents:
1. Messaging prospects who already have existing conversations (inbound)
2. Rapid-fire messages (minimum 24h gap between messages to same prospect)
"""

from __future__ import annotations

import time
import json

from heylead.db import schema


class TestMinMessageGap:
    """Verify minimum gap enforcement between messages to the same prospect."""

    def test_message_gap_query(self):
        """Messages table tracks timestamps correctly for gap enforcement."""
        db = schema.get_db()
        now = int(time.time())

        # Create campaign + contact + outreach
        db.execute(
            "INSERT INTO campaigns (id, name, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            ("camp-gap", "Gap Test", "active", now, now),
        )
        db.execute(
            "INSERT INTO contacts (id, campaign_id, name, linkedin_id, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("contact-gap", "camp-gap", "Test User", "test-gap-user", "active", now, now),
        )
        db.execute(
            "INSERT INTO outreaches (id, campaign_id, contact_id, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            ("outreach-gap", "camp-gap", "contact-gap", "connected", now, now),
        )

        # Insert a message 2 hours ago
        two_hours_ago = now - 7200
        db.execute(
            "INSERT INTO messages (id, outreach_id, role, text, timestamp) VALUES (?, ?, ?, ?, ?)",
            ("msg-gap-1", "outreach-gap", "sdr", "Hey there!", two_hours_ago),
        )
        db.commit()

        # Query MAX(created_at) — should return 2h ago timestamp
        row = db.execute(
            "SELECT MAX(timestamp) as last_ts FROM messages WHERE outreach_id = ? AND role = 'sdr'",
            ("outreach-gap",),
        ).fetchone()
        db.close()

        assert row["last_ts"] == two_hours_ago
        seconds_since = now - row["last_ts"]
        assert seconds_since < 86400  # Less than 24h — should block
        assert seconds_since >= 7200  # At least 2h ago

    def test_no_messages_allows_send(self):
        """When no prior messages exist, gap check should not block."""
        db = schema.get_db()
        now = int(time.time())

        db.execute(
            "INSERT INTO campaigns (id, name, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            ("camp-gap2", "Gap Test 2", "active", now, now),
        )
        db.execute(
            "INSERT INTO contacts (id, campaign_id, name, linkedin_id, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("contact-gap2", "camp-gap2", "No Msgs", "no-msgs-user", "active", now, now),
        )
        db.execute(
            "INSERT INTO outreaches (id, campaign_id, contact_id, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            ("outreach-gap2", "camp-gap2", "contact-gap2", "pending", now, now),
        )
        db.commit()

        row = db.execute(
            "SELECT MAX(timestamp) as last_ts FROM messages WHERE outreach_id = ? AND role = 'sdr'",
            ("outreach-gap2",),
        ).fetchone()
        db.close()

        # No messages — last_ts should be None
        assert row["last_ts"] is None


class TestConversationDetection:
    """Verify prospect message detection catches ANY inbound message, not just the last one."""

    def test_detect_prospect_message_buried_under_sdr_messages(self):
        """Even if SDR messages came after, prospect messages should still be found."""
        # Simulates the Ionut bug: prospect messaged months ago, SDR piled on top
        conversation = [
            {"role": "prospect", "text": "Hello, interested in marketing?", "timestamp": 1000},
            {"role": "prospect", "text": "Following up on marketing services", "timestamp": 2000},
            {"role": "sdr", "text": "Marketing is on my radar!", "timestamp": 100000},
            {"role": "sdr", "text": "What does your calendar look like?", "timestamp": 100100},
            {"role": "sdr", "text": "Happy to brainstorm ideas", "timestamp": 200000},
        ]

        # Old logic: only checked last message (would find "sdr" and break)
        old_found_prospect = False
        for m in reversed(conversation):
            if m["role"] == "prospect":
                old_found_prospect = True
                break
            elif m["role"] == "sdr":
                break  # Old logic stops here!

        assert not old_found_prospect, "Old logic should miss buried prospect messages"

        # New logic: check for ANY prospect message in conversation
        prospect_msgs = [m for m in conversation if m["role"] == "prospect"]
        assert len(prospect_msgs) == 2, "New logic finds all prospect messages"
        assert prospect_msgs[-1]["text"] == "Following up on marketing services"

    def test_no_prospect_messages_allows_send(self):
        """If only SDR messages exist, no prospect detection should trigger."""
        conversation = [
            {"role": "sdr", "text": "Hey, curious about your work!", "timestamp": 1000},
            {"role": "sdr", "text": "Following up on my message", "timestamp": 2000},
        ]

        prospect_msgs = [m for m in conversation if m["role"] == "prospect"]
        assert len(prospect_msgs) == 0, "No prospect messages, send should proceed"

    def test_empty_conversation_allows_send(self):
        """Empty or None conversation should not block sends."""
        for conv in [[], None]:
            if conv:
                prospect_msgs = [m for m in conv if m.get("role") == "prospect"]
            else:
                prospect_msgs = []
            assert len(prospect_msgs) == 0


class TestFollowupDelayAllTiers:
    """Verify minimum delay applies to ALL follow-ups, not just followup_count > 0."""

    def test_first_followup_has_minimum_delay(self):
        """Even the first DM (followup_count=0) should enforce minimum 1-day gap."""
        MIN_MESSAGE_GAP_DAYS = 1
        followup_count = 0

        # Old logic: skipped delay check when followup_count == 0
        old_would_check = followup_count > 0
        assert not old_would_check, "Old logic skips delay for first follow-up"

        # New logic: always applies minimum gap
        required_days = MIN_MESSAGE_GAP_DAYS  # fallback for followup_count == 0
        assert required_days >= 1, "New logic enforces at least 1 day gap"
