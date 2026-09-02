"""Tests for build_signature."""

from agentic_devtools.cli.github.issue_dedup import build_signature


class TestBuildSignature:
    """Tests for the build_signature function."""

    def test_normal_error_class(self) -> None:
        """Produces a 16-char hex string for a normal input."""
        result = build_signature("SSL_Handshake_Failure")
        assert len(result) == 16
        assert all(c in "0123456789abcdef" for c in result)

    def test_deterministic(self) -> None:
        """Same input always produces same output."""
        a = build_signature("some_error")
        b = build_signature("some_error")
        assert a == b

    def test_whitespace_strip(self) -> None:
        """Leading/trailing whitespace is stripped before hashing."""
        a = build_signature("  SSL_Handshake_Failure  ")
        b = build_signature("SSL_Handshake_Failure")
        assert a == b

    def test_lowercase_normalization(self) -> None:
        """Input is lowercased before hashing."""
        a = build_signature("SSL_Handshake_Failure")
        b = build_signature("ssl_handshake_failure")
        assert a == b

    def test_empty_string(self) -> None:
        """Empty string produces SHA-256 of empty string (first 16 hex)."""
        result = build_signature("")
        # SHA-256 of "" = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
        assert result == "e3b0c44298fc1c14"

    def test_whitespace_only_becomes_empty(self) -> None:
        """Whitespace-only input is treated as empty string after strip."""
        result = build_signature("   ")
        assert result == "e3b0c44298fc1c14"

    def test_different_inputs_differ(self) -> None:
        """Different inputs produce different signatures."""
        a = build_signature("error_a")
        b = build_signature("error_b")
        assert a != b
