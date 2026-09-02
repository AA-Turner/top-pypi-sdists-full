"""Tests for _looks_like_auth_error."""

from __future__ import annotations

from agentic_devtools.orchestration.nodes._issue_retrieval import _looks_like_auth_error


class TestLooksLikeAuthError:
    """Tests for authentication error detection."""

    def test_returns_false_for_generic_exception(self) -> None:
        assert _looks_like_auth_error(Exception("Connection refused")) is False

    def test_returns_true_for_401_status(self) -> None:
        assert _looks_like_auth_error(Exception("HTTP 401 Unauthorized")) is True

    def test_returns_true_for_403_status(self) -> None:
        assert _looks_like_auth_error(Exception("HTTP 403 Forbidden")) is True

    def test_returns_true_for_authentication_keyword(self) -> None:
        assert _looks_like_auth_error(Exception("Authentication failed")) is True

    def test_returns_true_for_unauthorized_keyword(self) -> None:
        assert _looks_like_auth_error(Exception("Unauthorized access")) is True

    def test_returns_true_for_invalid_credentials(self) -> None:
        assert _looks_like_auth_error(Exception("Invalid credentials provided")) is True

    def test_case_insensitive_matching(self) -> None:
        assert _looks_like_auth_error(Exception("AUTHENTICATION FAILED")) is True

    def test_returns_false_for_unrelated_http_error(self) -> None:
        assert _looks_like_auth_error(Exception("HTTP 500 Internal Server Error")) is False
