"""Tests for collection update normalization and id alias."""

import pytest

from cpsl.db import _normalize_update, _with_id_alias


class TestNormalizeUpdate:
    def test_plain_dict_wraps_in_set(self):
        assert _normalize_update({"status": "sent"}) == {"$set": {"status": "sent"}}

    def test_multiple_plain_fields(self):
        result = _normalize_update({"status": "sent", "owner": "eli"})
        assert result == {"$set": {"status": "sent", "owner": "eli"}}

    def test_operator_doc_passes_through(self):
        doc = {"$set": {"status": "sent"}}
        assert _normalize_update(doc) == {"$set": {"status": "sent"}}

    def test_multiple_operators_pass_through(self):
        doc = {"$set": {"status": "sent"}, "$inc": {"count": 1}}
        result = _normalize_update(doc)
        assert result == doc

    def test_mixed_raises(self):
        with pytest.raises(ValueError, match="mixes operator keys"):
            _normalize_update({"status": "sent", "$inc": {"count": 1}})

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="must not be empty"):
            _normalize_update({})

    def test_outreach_style_plain_update(self):
        """Regression: the exact pattern from outreach.py that triggered the bug."""
        update = {
            "outreach_status": "sent",
            "outreach_phase": "initial",
            "reply_classification": "no-reply",
            "last_contact": "2026-04-18",
            "emails_sent": "1",
        }
        result = _normalize_update(update)
        assert result == {"$set": update}

    def test_settings_explicit_set_unchanged(self):
        """settings.py already uses $set explicitly — must remain unchanged."""
        doc = {"$set": {"value": 42, "_settings_key": "foo"}}
        assert _normalize_update(doc) == doc

    def test_inc_sent_helper_pattern(self):
        """Regression: _inc_sent returns plain fields that get spread into the update."""
        base = {
            "thread_id": "tid_123",
            "outreach_status": "sent",
            "outreach_phase": "initial",
            "reply_classification": "no-reply",
        }
        inc_sent = {"last_contact": "2026-04-18", "emails_sent": "1"}
        update = {**base, **inc_sent}
        result = _normalize_update(update)
        assert "$set" in result
        assert result["$set"]["thread_id"] == "tid_123"
        assert result["$set"]["emails_sent"] == "1"


class TestIdAlias:
    def test_adds_id_from_underscore_id(self):
        doc = {"_id": "abc123", "name": "foo"}
        result = _with_id_alias(doc)
        assert result["id"] == "abc123"
        assert result["_id"] == "abc123"

    def test_preserves_existing_id(self):
        doc = {"_id": "abc123", "id": "custom", "name": "foo"}
        result = _with_id_alias(doc)
        assert result["id"] == "custom"
        assert result["_id"] == "abc123"

    def test_no_underscore_id(self):
        doc = {"name": "foo"}
        result = _with_id_alias(doc)
        assert "id" not in result

    def test_mutates_in_place(self):
        doc = {"_id": "abc123"}
        result = _with_id_alias(doc)
        assert result is doc
