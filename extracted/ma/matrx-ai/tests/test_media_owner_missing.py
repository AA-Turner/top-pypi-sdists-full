"""D1 (2026-10-22): a media save with no person in context reached the database as ``created_by = ''`` and failed as
``invalid input syntax for type uuid``. The save now refuses an empty owner by name, before any storage work."""

from types import SimpleNamespace

import pytest

from matrx_ai.media.media_persistence import MediaOwnerMissing, resolve_media_owner


def _fm(user_id=""):
    return SimpleNamespace(sync_engine=SimpleNamespace(user_id=user_id))


def test_no_owner_anywhere_is_refused_by_name(monkeypatch):
    monkeypatch.setattr("matrx_utils.ctx.get_active_user_id", lambda: "")
    with pytest.raises(MediaOwnerMissing, match="no signed-in person"):
        resolve_media_owner(_fm(), "ai_images")


def test_the_active_person_owns_the_save(monkeypatch):
    monkeypatch.setattr("matrx_utils.ctx.get_active_user_id", lambda: "u-1")
    assert resolve_media_owner(_fm(), "ai_images") == "u-1"
    assert resolve_media_owner(_fm("u-2"), "ai_images") == "u-2"
