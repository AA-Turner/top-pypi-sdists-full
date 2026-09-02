"""Tests for embed_marker."""

from agentic_devtools.cli.github.issue_dedup import embed_marker


class TestEmbedMarker:
    """Tests for the embed_marker function."""

    def test_appends_marker_to_clean_body(self) -> None:
        """Marker is appended to a body that has no markers."""
        body = "Issue description here"
        sig = "abc123def456abcd"
        result = embed_marker(body, sig)
        assert result.endswith("<!-- agdt-dedup-sig:abc123def456abcd -->")
        assert "Issue description here" in result

    def test_idempotent_for_same_sig(self) -> None:
        """Embedding the same signature twice is idempotent."""
        body = "Issue description here"
        sig = "abc123def456abcd"
        first = embed_marker(body, sig)
        second = embed_marker(first, sig)
        assert first == second

    def test_multi_marker_different_sigs(self) -> None:
        """Different signatures can coexist in the same body."""
        body = "Issue description"
        sig1 = "aaaa1111bbbb2222"
        sig2 = "cccc3333dddd4444"
        result = embed_marker(embed_marker(body, sig1), sig2)
        assert "<!-- agdt-dedup-sig:aaaa1111bbbb2222 -->" in result
        assert "<!-- agdt-dedup-sig:cccc3333dddd4444 -->" in result

    def test_empty_body(self) -> None:
        """Works with empty body string."""
        result = embed_marker("", "abc123def456abcd")
        assert result == "<!-- agdt-dedup-sig:abc123def456abcd -->"

    def test_body_with_trailing_newline(self) -> None:
        """Body ending with newline gets marker appended directly."""
        body = "Some text\n"
        result = embed_marker(body, "abc123def456abcd")
        assert result == "Some text\n<!-- agdt-dedup-sig:abc123def456abcd -->"

    def test_body_without_trailing_newline(self) -> None:
        """Body without trailing newline gets newline+marker."""
        body = "Some text"
        result = embed_marker(body, "abc123def456abcd")
        assert result == "Some text\n<!-- agdt-dedup-sig:abc123def456abcd -->"
