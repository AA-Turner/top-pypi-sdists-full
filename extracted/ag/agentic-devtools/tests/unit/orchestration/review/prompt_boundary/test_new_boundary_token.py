"""Tests for new_boundary_token (FR-013)."""

from agentic_devtools.orchestration.review.prompt_boundary import new_boundary_token


class TestNewBoundaryToken:
    def test_returns_hex_string(self):
        token = new_boundary_token()
        assert isinstance(token, str)
        assert len(token) == 32
        int(token, 16)  # parses as hex

    def test_tokens_are_unique(self):
        assert new_boundary_token() != new_boundary_token()
