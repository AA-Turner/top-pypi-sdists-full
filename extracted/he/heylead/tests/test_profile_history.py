"""Tests for profile change history and restore functionality."""

from __future__ import annotations

import asyncio
import base64
import json
from unittest.mock import AsyncMock, patch

from heylead.db.queries import (
    get_profile_change,
    get_profile_changes,
    get_setting,
    log_profile_change,
    mark_profile_change_reverted,
    save_setting,
)
from heylead.tools.profile_editor import apply_profile_change


# ── Query function tests ──


class TestLogProfileChange:
    def test_creates_record(self):
        change_id = log_profile_change("headline", "Old HL", "New HL", "manual")
        assert len(change_id) == 8
        record = get_profile_change(change_id)
        assert record is not None
        assert record["field"] == "headline"
        assert record["old_value"] == "Old HL"
        assert record["new_value"] == "New HL"
        assert record["source"] == "manual"
        assert record["status"] == "applied"

    def test_null_old_value(self):
        change_id = log_profile_change("summary", None, "New summary", "brand_strategy")
        record = get_profile_change(change_id)
        assert record is not None
        assert record["old_value"] is None
        assert record["source"] == "brand_strategy"


class TestGetProfileChanges:
    def test_returns_entries(self):
        id1 = log_profile_change("headline", "a", "b")
        id2 = log_profile_change("headline", "b", "c")
        changes = get_profile_changes(field="headline", limit=10)
        ids = [c["id"] for c in changes]
        assert id1 in ids
        assert id2 in ids

    def test_filters_by_field(self):
        log_profile_change("headline", "x", "y")
        log_profile_change("summary", "s1", "s2")
        headline_changes = get_profile_changes(field="headline")
        for c in headline_changes:
            assert c["field"] == "headline"

    def test_limit(self):
        for i in range(5):
            log_profile_change("headline", f"old{i}", f"new{i}")
        changes = get_profile_changes(limit=3)
        assert len(changes) <= 3

    def test_all_fields(self):
        log_profile_change("headline", "h1", "h2")
        log_profile_change("summary", "s1", "s2")
        all_changes = get_profile_changes()
        fields = {c["field"] for c in all_changes}
        assert "headline" in fields
        assert "summary" in fields


class TestGetProfileChange:
    def test_found(self):
        cid = log_profile_change("headline", "old", "new")
        assert get_profile_change(cid) is not None

    def test_not_found(self):
        assert get_profile_change("nonexist") is None


class TestMarkReverted:
    def test_marks_reverted(self):
        cid = log_profile_change("headline", "old", "new")
        mark_profile_change_reverted(cid)
        record = get_profile_change(cid)
        assert record["status"] == "reverted"


# ── apply_profile_change wrapper tests ──


class TestApplyProfileChange:
    def test_headline_success(self):
        save_setting("profile", {"headline": "Original HL", "provider_id": "prov1"})
        mock_client = AsyncMock()
        mock_client.update_profile_headline.return_value = {"success": True}

        result = asyncio.get_event_loop().run_until_complete(
            apply_profile_change(mock_client, "acc1", "prov1", "headline", "New HL", "manual")
        )

        assert result["success"] is True
        assert result["change_id"] is not None
        mock_client.update_profile_headline.assert_called_once_with("acc1", "prov1", "New HL")

        # Verify DB record
        record = get_profile_change(result["change_id"])
        assert record["field"] == "headline"
        assert record["old_value"] == "Original HL"
        assert record["new_value"] == "New HL"

        # Verify cache updated
        profile = get_setting("profile", {})
        assert profile["headline"] == "New HL"

    def test_summary_success(self):
        save_setting("profile", {"summary": "Old summary"})
        mock_client = AsyncMock()
        mock_client.update_profile_summary.return_value = {"success": True}

        result = asyncio.get_event_loop().run_until_complete(
            apply_profile_change(mock_client, "acc1", "prov1", "summary", "New summary")
        )

        assert result["success"] is True
        record = get_profile_change(result["change_id"])
        assert record["field"] == "summary"
        assert record["old_value"] == "Old summary"

    def test_photo_success(self):
        save_setting("profile", {})
        mock_client = AsyncMock()
        mock_client.upload_profile_photo.return_value = {"success": True}
        # get_own_profile returns no photo URL — old_value will be None
        mock_client.get_own_profile.return_value = {"profile_picture_url": ""}

        result = asyncio.get_event_loop().run_until_complete(
            apply_profile_change(
                mock_client, "acc1", "prov1", "photo", "<photo uploaded>",
                image_bytes=b"\xff\xd8\xff", content_type="image/jpeg",
            )
        )

        assert result["success"] is True
        mock_client.upload_profile_photo.assert_called_once_with(
            "acc1", "prov1", b"\xff\xd8\xff", "image/jpeg",
        )

        # Verify new_value stores base64 JSON (not placeholder)
        record = get_profile_change(result["change_id"])
        photo_data = json.loads(record["new_value"])
        assert "base64" in photo_data
        assert photo_data["content_type"] == "image/jpeg"
        assert base64.b64decode(photo_data["base64"]) == b"\xff\xd8\xff"

    def test_photo_missing_bytes(self):
        mock_client = AsyncMock()
        result = asyncio.get_event_loop().run_until_complete(
            apply_profile_change(mock_client, "acc1", "prov1", "photo", "<photo>")
        )
        assert result["success"] is False
        assert "image_bytes" in result["error"]

    def test_unsupported_field(self):
        mock_client = AsyncMock()
        result = asyncio.get_event_loop().run_until_complete(
            apply_profile_change(mock_client, "acc1", "prov1", "birthday", "1990-01-01")
        )
        assert result["success"] is False
        assert "Unsupported" in result["error"]

    def test_client_failure_no_log(self):
        save_setting("profile", {"headline": "Orig"})
        mock_client = AsyncMock()
        mock_client.update_profile_headline.return_value = {"success": False, "error": "API down"}

        result = asyncio.get_event_loop().run_until_complete(
            apply_profile_change(mock_client, "acc1", "prov1", "headline", "New HL")
        )

        assert result["success"] is False
        assert result["change_id"] is None
        assert "API down" in result["error"]


# ── profile_history tool handler tests ──


class TestProfileHistoryTool:
    def test_history_empty(self):
        from heylead.tools.profile_history import run_profile

        result = asyncio.get_event_loop().run_until_complete(
            run_profile("history", field="nonexistent_field")
        )
        assert "No profile changes" in result

    def test_history_shows_entries(self):
        from heylead.tools.profile_history import run_profile

        log_profile_change("headline", "old", "new", "manual")
        result = asyncio.get_event_loop().run_until_complete(
            run_profile("history")
        )
        assert "Profile Change History" in result
        assert "headline" in result

    def test_current_empty(self):
        from heylead.tools.profile_history import run_profile

        save_setting("profile", {})
        result = asyncio.get_event_loop().run_until_complete(
            run_profile("current")
        )
        # Either shows "No profile cached" or shows the empty profile
        assert "profile" in result.lower()

    def test_current_with_data(self):
        from heylead.tools.profile_history import run_profile

        save_setting("profile", {
            "first_name": "Test",
            "last_name": "User",
            "headline": "Engineer",
            "summary": "About me",
        })
        result = asyncio.get_event_loop().run_until_complete(
            run_profile("current")
        )
        assert "Test" in result
        assert "Engineer" in result

    def test_restore_no_id(self):
        from heylead.tools.profile_history import run_profile

        result = asyncio.get_event_loop().run_until_complete(
            run_profile("restore", change_id="")
        )
        assert "provide" in result.lower()

    def test_restore_not_found(self):
        from heylead.tools.profile_history import run_profile

        result = asyncio.get_event_loop().run_until_complete(
            run_profile("restore", change_id="xxxxxxxx")
        )
        assert "No change found" in result

    def test_restore_already_reverted(self):
        from heylead.tools.profile_history import run_profile

        cid = log_profile_change("headline", "old", "new")
        mark_profile_change_reverted(cid)
        result = asyncio.get_event_loop().run_until_complete(
            run_profile("restore", change_id=cid)
        )
        assert "already been reverted" in result

    @patch("heylead.linkedin.get_account_id", return_value="acc1")
    @patch("heylead.linkedin.get_linkedin_client")
    def test_restore_photo_legacy_placeholder(self, mock_get_client, mock_get_account):
        """Legacy records with placeholder text cannot be restored."""
        from heylead.tools.profile_history import run_profile

        save_setting("profile", {"provider_id": "prov1"})
        mock_get_client.return_value = AsyncMock()

        cid = log_profile_change("photo", "<prev>", "<new photo>")
        result = asyncio.get_event_loop().run_until_complete(
            run_profile("restore", change_id=cid)
        )
        assert "Cannot restore" in result
        assert "not in the expected format" in result

    @patch("heylead.linkedin.get_account_id", return_value="acc1")
    @patch("heylead.linkedin.get_linkedin_client")
    def test_restore_cover_photo_legacy_placeholder(self, mock_get_client, mock_get_account):
        """Legacy cover photo records with placeholder text cannot be restored."""
        from heylead.tools.profile_history import run_profile

        save_setting("profile", {"provider_id": "prov1"})
        mock_get_client.return_value = AsyncMock()

        cid = log_profile_change("cover_photo", "<prev>", "<new cover>")
        result = asyncio.get_event_loop().run_until_complete(
            run_profile("restore", change_id=cid)
        )
        assert "Cannot restore" in result
        assert "cover photo" in result.lower()

    def test_unknown_action(self):
        from heylead.tools.profile_history import run_profile

        result = asyncio.get_event_loop().run_until_complete(
            run_profile("invalid_action")
        )
        assert "Unknown action" in result


# ── New field apply_profile_change tests ──


class TestApplyProfileChangeNewFields:
    def test_custom_link_success(self):
        save_setting("profile", {"custom_link": None})
        mock_client = AsyncMock()
        mock_client.update_custom_link.return_value = {"success": True}

        import json
        link_data = json.dumps({"category": "WEBSITE", "url": "https://cal.com/me"})
        result = asyncio.get_event_loop().run_until_complete(
            apply_profile_change(mock_client, "acc1", "prov1", "custom_link", link_data)
        )

        assert result["success"] is True
        assert result["change_id"] is not None
        mock_client.update_custom_link.assert_called_once_with(
            "acc1", "prov1", "WEBSITE", "https://cal.com/me",
        )
        record = get_profile_change(result["change_id"])
        assert record["field"] == "custom_link"

    def test_custom_link_invalid_json(self):
        mock_client = AsyncMock()
        result = asyncio.get_event_loop().run_until_complete(
            apply_profile_change(mock_client, "acc1", "prov1", "custom_link", "not-json")
        )
        assert result["success"] is False
        assert "JSON" in result["error"]

    def test_location_success(self):
        save_setting("profile", {"location_id": "old-loc"})
        mock_client = AsyncMock()
        mock_client.update_location.return_value = {"success": True}

        result = asyncio.get_event_loop().run_until_complete(
            apply_profile_change(mock_client, "acc1", "prov1", "location", "105015875")
        )

        assert result["success"] is True
        mock_client.update_location.assert_called_once_with("acc1", "prov1", "105015875")
        profile = get_setting("profile", {})
        assert profile["location_id"] == "105015875"

    def test_skills_success(self):
        save_setting("profile", {"skills": ["Old"]})
        mock_client = AsyncMock()
        mock_client.update_skills.return_value = {"success": True}

        import json
        skills_json = json.dumps(["Python", "Leadership"])
        result = asyncio.get_event_loop().run_until_complete(
            apply_profile_change(mock_client, "acc1", "prov1", "skills", skills_json)
        )

        assert result["success"] is True
        mock_client.update_skills.assert_called_once_with(
            "acc1", "prov1", ["Python", "Leadership"],
        )
        profile = get_setting("profile", {})
        assert profile["skills"] == ["Python", "Leadership"]

    def test_skills_invalid_json(self):
        mock_client = AsyncMock()
        result = asyncio.get_event_loop().run_until_complete(
            apply_profile_change(mock_client, "acc1", "prov1", "skills", "not-json")
        )
        assert result["success"] is False
        assert "JSON" in result["error"]

    def test_experience_success(self):
        save_setting("profile", {})
        mock_client = AsyncMock()
        mock_client.update_experience.return_value = {"success": True}

        import json
        exp_data = json.dumps({"company_name": "Acme", "title": "CEO"})
        result = asyncio.get_event_loop().run_until_complete(
            apply_profile_change(mock_client, "acc1", "prov1", "experience", exp_data)
        )

        assert result["success"] is True
        mock_client.update_experience.assert_called_once_with(
            "acc1", "prov1", {"company_name": "Acme", "title": "CEO"},
        )

    def test_experience_invalid_json(self):
        mock_client = AsyncMock()
        result = asyncio.get_event_loop().run_until_complete(
            apply_profile_change(mock_client, "acc1", "prov1", "experience", "not-json")
        )
        assert result["success"] is False
        assert "JSON" in result["error"]

    def test_cover_photo_success(self):
        save_setting("profile", {})
        mock_client = AsyncMock()
        mock_client.upload_cover_photo.return_value = {"success": True}

        result = asyncio.get_event_loop().run_until_complete(
            apply_profile_change(
                mock_client, "acc1", "prov1", "cover_photo", "<cover uploaded>",
                image_bytes=b"\x89PNG", content_type="image/png",
            )
        )

        assert result["success"] is True
        mock_client.upload_cover_photo.assert_called_once_with(
            "acc1", "prov1", b"\x89PNG", "image/png",
        )

        # Verify new_value stores base64 JSON
        record = get_profile_change(result["change_id"])
        photo_data = json.loads(record["new_value"])
        assert photo_data["content_type"] == "image/png"
        assert base64.b64decode(photo_data["base64"]) == b"\x89PNG"
        # Cover photo old_value is always None (no API to fetch current)
        assert record["old_value"] is None

    def test_cover_photo_missing_bytes(self):
        mock_client = AsyncMock()
        result = asyncio.get_event_loop().run_until_complete(
            apply_profile_change(mock_client, "acc1", "prov1", "cover_photo", "<cover>")
        )
        assert result["success"] is False
        assert "image_bytes" in result["error"]

    def test_current_shows_new_fields(self):
        """Verify _show_current displays location, custom_link, and skills."""
        from heylead.tools.profile_history import run_profile

        save_setting("profile", {
            "first_name": "Test",
            "last_name": "User",
            "headline": "Engineer",
            "summary": "About me",
            "location_id": "105015875",
            "custom_link": {"category": "WEBSITE", "url": "https://example.com"},
            "skills": ["Python", "AI"],
        })
        result = asyncio.get_event_loop().run_until_complete(
            run_profile("current")
        )
        assert "105015875" in result
        assert "example.com" in result
        assert "Python" in result
        assert "AI" in result


# ── Photo storage and restore tests ──


class TestPhotoBase64Storage:
    """Verify photos are stored as base64 JSON for future restore."""

    def test_photo_old_value_fetch_fails_gracefully(self):
        """If fetching current photo fails, upload proceeds with old_value=None."""
        save_setting("profile", {})
        mock_client = AsyncMock()
        mock_client.upload_profile_photo.return_value = {"success": True}
        # Simulate failure fetching current photo
        mock_client.get_own_profile.side_effect = Exception("network error")

        result = asyncio.get_event_loop().run_until_complete(
            apply_profile_change(
                mock_client, "acc1", "prov1", "photo", "photo",
                image_bytes=b"\xff\xd8\xff", content_type="image/jpeg",
            )
        )

        assert result["success"] is True
        record = get_profile_change(result["change_id"])
        assert record["old_value"] is None  # Gracefully None
        # new_value still has base64
        photo_data = json.loads(record["new_value"])
        assert "base64" in photo_data

    def test_photo_old_value_fetched(self):
        """When _fetch_current_photo_b64 succeeds, old_value stores the current photo."""
        save_setting("profile", {})
        mock_client = AsyncMock()
        mock_client.upload_profile_photo.return_value = {"success": True}

        # Simulate _fetch_current_photo_b64 returning existing photo data
        old_photo_bytes = b"\x89PNG-old-photo-data"
        old_photo_b64 = json.dumps({
            "base64": base64.b64encode(old_photo_bytes).decode(),
            "content_type": "image/png",
        })

        with patch(
            "heylead.tools.profile_editor._fetch_current_photo_b64",
            return_value=old_photo_b64,
        ):
            result = asyncio.get_event_loop().run_until_complete(
                apply_profile_change(
                    mock_client, "acc1", "prov1", "photo", "photo",
                    image_bytes=b"\xff\xd8\xff-new", content_type="image/jpeg",
                )
            )

        assert result["success"] is True
        record = get_profile_change(result["change_id"])

        # old_value should contain the downloaded photo
        old_data = json.loads(record["old_value"])
        assert base64.b64decode(old_data["base64"]) == old_photo_bytes
        assert old_data["content_type"] == "image/png"

        # new_value should contain the uploaded photo
        new_data = json.loads(record["new_value"])
        assert base64.b64decode(new_data["base64"]) == b"\xff\xd8\xff-new"
        assert new_data["content_type"] == "image/jpeg"

    def test_history_shows_photo_size(self):
        """Profile history shows photo size instead of raw base64."""
        from heylead.tools.profile_history import run_profile

        photo_bytes = b"\xff\xd8\xff" * 100  # ~300 bytes
        photo_b64 = json.dumps({
            "base64": base64.b64encode(photo_bytes).decode(),
            "content_type": "image/jpeg",
        })
        log_profile_change("photo", None, photo_b64, "manual")

        result = asyncio.get_event_loop().run_until_complete(
            run_profile("history", field="photo")
        )
        assert "[Photo:" in result
        assert "KB" in result
        assert "image/jpeg" in result

    def test_history_shows_legacy_placeholder(self):
        """Legacy photo records show placeholder text instead of crashing."""
        from heylead.tools.profile_history import run_profile

        log_profile_change("photo", "<previous photo>", "<photo uploaded>", "manual")

        result = asyncio.get_event_loop().run_until_complete(
            run_profile("history", field="photo")
        )
        # Should display the legacy text without crashing
        assert "<previous photo>" in result or "<photo uploaded>" in result


class TestPhotoRestore:
    """Verify photo restore decodes base64 and re-uploads."""

    @patch("heylead.linkedin.get_account_id", return_value="acc1")
    @patch("heylead.linkedin.get_linkedin_client")
    def test_restore_photo_success(self, mock_get_client, mock_get_account):
        from heylead.tools.profile_history import run_profile

        # Create a photo change record with proper base64 data
        old_photo_bytes = b"\xff\xd8\xff-original"
        old_b64 = json.dumps({
            "base64": base64.b64encode(old_photo_bytes).decode(),
            "content_type": "image/jpeg",
        })
        new_b64 = json.dumps({
            "base64": base64.b64encode(b"\xff\xd8\xff-new").decode(),
            "content_type": "image/jpeg",
        })
        cid = log_profile_change("photo", old_b64, new_b64, "manual")

        # Mock the client for restore
        save_setting("profile", {"provider_id": "prov1"})
        mock_client = AsyncMock()
        mock_client.upload_profile_photo.return_value = {"success": True}
        mock_client.get_own_profile.return_value = {"profile_picture_url": ""}
        mock_get_client.return_value = mock_client

        result = asyncio.get_event_loop().run_until_complete(
            run_profile("restore", change_id=cid)
        )

        assert "Restored photo" in result
        assert "KB" in result
        mock_client.upload_profile_photo.assert_called_once()
        # Verify the re-uploaded bytes match the original
        call_args = mock_client.upload_profile_photo.call_args
        assert call_args[0][2] == old_photo_bytes  # image_bytes
        assert call_args[0][3] == "image/jpeg"  # content_type

        # Verify the original change is marked as reverted
        record = get_profile_change(cid)
        assert record["status"] == "reverted"

    @patch("heylead.linkedin.get_account_id", return_value="acc1")
    @patch("heylead.linkedin.get_linkedin_client")
    def test_restore_cover_photo_success(self, mock_get_client, mock_get_account):
        from heylead.tools.profile_history import run_profile

        old_cover_bytes = b"\x89PNG-cover-original"
        old_b64 = json.dumps({
            "base64": base64.b64encode(old_cover_bytes).decode(),
            "content_type": "image/png",
        })
        new_b64 = json.dumps({
            "base64": base64.b64encode(b"\x89PNG-cover-new").decode(),
            "content_type": "image/png",
        })
        cid = log_profile_change("cover_photo", old_b64, new_b64, "manual")

        save_setting("profile", {"provider_id": "prov1"})
        mock_client = AsyncMock()
        mock_client.upload_cover_photo.return_value = {"success": True}
        mock_get_client.return_value = mock_client

        result = asyncio.get_event_loop().run_until_complete(
            run_profile("restore", change_id=cid)
        )

        assert "Restored cover photo" in result
        mock_client.upload_cover_photo.assert_called_once()
        call_args = mock_client.upload_cover_photo.call_args
        assert call_args[0][2] == old_cover_bytes
        assert call_args[0][3] == "image/png"

    def test_restore_photo_no_old_value(self):
        """Cover photo first upload has no old_value — restore not possible."""
        from heylead.tools.profile_history import run_profile

        new_b64 = json.dumps({
            "base64": base64.b64encode(b"\x89PNG").decode(),
            "content_type": "image/png",
        })
        cid = log_profile_change("cover_photo", None, new_b64, "manual")

        result = asyncio.get_event_loop().run_until_complete(
            run_profile("restore", change_id=cid)
        )
        # old_value is None → "previous value was not recorded"
        assert "previous value was not recorded" in result
