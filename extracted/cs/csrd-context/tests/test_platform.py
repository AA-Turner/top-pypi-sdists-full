"""Tests for platform-level context variables."""

from csrd.context.platform import app_id_context, hit_id_context, user_info_context
from csrd.models.claims import UserClaims


class TestPlatformContextVars:
    def test_user_info_default_none(self):
        assert user_info_context.get() is None

    def test_user_info_set_and_get(self):
        claims = UserClaims(sub="user1", user_name="alice")
        token = user_info_context.set(claims)
        try:
            assert user_info_context.get().sub == "user1"
        finally:
            user_info_context.reset(token)

    def test_hit_id_default(self):
        assert hit_id_context.get() == "unknown"

    def test_app_id_default(self):
        assert app_id_context.get() == "unknown"

    def test_hit_id_set(self):
        token = hit_id_context.set("req-abc-123")
        try:
            assert hit_id_context.get() == "req-abc-123"
        finally:
            hit_id_context.reset(token)
