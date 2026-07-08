"""Full-branch tests for backend.email_service.

Strategy: mock httpx.post and os.environ so we exercise every provider
branch, both API-key-present and absent paths, plus the welcome template.
No real network calls.
"""

from __future__ import annotations

from unittest.mock import patch, MagicMock

import pytest

from backend.email_service import send_email, send_welcome_email


def _stub_response(status_code: int = 200) -> MagicMock:
    """Build a minimal httpx-style response mock."""
    r = MagicMock()
    r.status_code = status_code
    return r


class TestSendEmailBranches:
    """Every branch of send_email() — provider selection + auth + failure."""

    @pytest.fixture(autouse=True)
    def drop_sage_testing(self, monkeypatch):
        monkeypatch.delenv("SAGE_TESTING", raising=False)

    def test_no_provider_returns_false(self, monkeypatch):
        monkeypatch.delenv("EMAIL_PROVIDER", raising=False)
        assert send_email(to="x@y.com", subject="s", text="t") is False

    def test_unknown_provider_returns_false(self, monkeypatch):
        monkeypatch.setenv("EMAIL_PROVIDER", "bogus-mailer")
        assert send_email(to="x@y.com", subject="s", text="t") is False

    @pytest.mark.parametrize("provider,key_env", [
        ("resend",   "RESEND_API_KEY"),
        ("postmark", "POSTMARK_API_KEY"),
        ("sendgrid", "SENDGRID_API_KEY"),
    ])
    def test_provider_without_key_returns_false(self, monkeypatch, provider, key_env):
        monkeypatch.setenv("EMAIL_PROVIDER", provider)
        monkeypatch.delenv(key_env, raising=False)
        assert send_email(to="x@y.com", subject="s", text="t") is False

    @pytest.mark.parametrize("provider,key_env,success_code", [
        ("resend",   "RESEND_API_KEY",   200),
        ("resend",   "RESEND_API_KEY",   202),
        ("postmark", "POSTMARK_API_KEY", 200),
        ("sendgrid", "SENDGRID_API_KEY", 202),
    ])
    def test_provider_success(self, monkeypatch, provider, key_env, success_code):
        monkeypatch.setenv("EMAIL_PROVIDER", provider)
        monkeypatch.setenv(key_env, "fake-key")
        with patch("backend.email_service.httpx.post",
                   return_value=_stub_response(success_code)) as mock_post:
            result = send_email(
                to="user@example.com", subject="Test", html="<p>hi</p>",
                text="hi", reply_to="r@example.com",
            )
        assert result is True
        assert mock_post.called

    def test_provider_failure_returns_false(self, monkeypatch):
        monkeypatch.setenv("EMAIL_PROVIDER", "resend")
        monkeypatch.setenv("RESEND_API_KEY", "fake-key")
        with patch("backend.email_service.httpx.post",
                   return_value=_stub_response(500)):
            assert send_email(to="x@y.com", subject="s", text="t") is False

    def test_exception_in_send_returns_false(self, monkeypatch):
        """A network exception must not propagate — email is best-effort."""
        monkeypatch.setenv("EMAIL_PROVIDER", "resend")
        monkeypatch.setenv("RESEND_API_KEY", "fake-key")
        with patch("backend.email_service.httpx.post",
                   side_effect=RuntimeError("network exploded")):
            assert send_email(to="x@y.com", subject="s") is False


class TestWelcomeEmail:

    @pytest.fixture(autouse=True)
    def drop_sage_testing(self, monkeypatch):
        monkeypatch.delenv("SAGE_TESTING", raising=False)

    def test_no_display_name(self, monkeypatch):
        monkeypatch.delenv("EMAIL_PROVIDER", raising=False)
        # send_email returns False (no provider), but the wrapper still runs
        # which exercises the template + subject-building branches.
        assert send_welcome_email("new@user.com") is False

    def test_with_display_name(self, monkeypatch):
        monkeypatch.setenv("EMAIL_PROVIDER", "resend")
        monkeypatch.setenv("RESEND_API_KEY", "fake")
        captured = {}

        def _capture(*args, **kwargs):
            captured.update(kwargs)
            return _stub_response(200)

        with patch("backend.email_service.httpx.post", side_effect=_capture):
            ok = send_welcome_email("a@b.com", display_name="Alice")
        assert ok is True
        assert "Alice" in captured["json"]["subject"]
