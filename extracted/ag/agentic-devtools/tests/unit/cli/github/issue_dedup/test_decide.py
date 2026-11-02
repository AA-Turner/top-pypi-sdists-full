"""Tests for decide."""

from agentic_devtools.cli.github.issue_dedup import decide


class TestDecide:
    """Tests for the decide function."""

    def test_empty_matches_returns_create(self) -> None:
        """Empty matches list results in create action."""
        result = decide([], "abc123def456abcd")
        assert result == {"action": "create"}

    def test_single_valid_match_returns_upvote_augment(self) -> None:
        """Single valid match results in upvote-augment."""
        sig = "abc123def456abcd"
        matches = [{"number": 42, "body": "text\n<!-- agdt-dedup-sig:abc123def456abcd -->"}]
        result = decide(matches, sig)
        assert result == {"action": "upvote-augment", "issue_number": 42}

    def test_smallest_number_tiebreaker(self) -> None:
        """Multiple matches: lowest issue number wins."""
        sig = "abc123def456abcd"
        marker = "<!-- agdt-dedup-sig:abc123def456abcd -->"
        matches = [
            {"number": 100, "body": f"text\n{marker}"},
            {"number": 5, "body": f"other\n{marker}"},
            {"number": 50, "body": f"more\n{marker}"},
        ]
        result = decide(matches, sig)
        assert result == {"action": "upvote-augment", "issue_number": 5}

    def test_malformed_entries_filtered(self) -> None:
        """Entries without valid number are filtered out."""
        sig = "abc123def456abcd"
        marker = "<!-- agdt-dedup-sig:abc123def456abcd -->"
        matches: list[dict] = [
            {"number": "not-a-number", "body": f"text\n{marker}"},
            {"number": -1, "body": f"text\n{marker}"},
            {"number": 0, "body": f"text\n{marker}"},
            {"number": None, "body": f"text\n{marker}"},
            {"body": f"text\n{marker}"},  # missing number
        ]
        result = decide(matches, sig)
        assert result == {"action": "create"}

    def test_all_malformed_returns_create(self) -> None:
        """All malformed entries results in create action."""
        sig = "abc123def456abcd"
        matches: list[dict] = [
            {"number": "bad", "body": "no marker"},
            {"number": 0, "body": "also bad"},
        ]
        result = decide(matches, sig)
        assert result == {"action": "create"}

    def test_duplicate_numbers_deduped(self) -> None:
        """Duplicate issue numbers are deduplicated."""
        sig = "abc123def456abcd"
        marker = "<!-- agdt-dedup-sig:abc123def456abcd -->"
        matches = [
            {"number": 10, "body": f"first\n{marker}"},
            {"number": 10, "body": f"duplicate\n{marker}"},
            {"number": 5, "body": f"lowest\n{marker}"},
        ]
        result = decide(matches, sig)
        assert result == {"action": "upvote-augment", "issue_number": 5}

    def test_marker_not_in_body_filtered(self) -> None:
        """Issues without the marker in their body are filtered."""
        sig = "abc123def456abcd"
        matches = [
            {"number": 1, "body": "no marker here"},
            {
                "number": 2,
                "body": "wrong marker\n<!-- agdt-dedup-sig:different_sig_here -->",
            },
        ]
        result = decide(matches, sig)
        assert result == {"action": "create"}

    def test_mixed_valid_and_invalid(self) -> None:
        """Valid matches are found among invalid ones."""
        sig = "abc123def456abcd"
        marker = "<!-- agdt-dedup-sig:abc123def456abcd -->"
        matches: list[dict] = [
            {"number": "bad", "body": f"text\n{marker}"},
            {"number": 99, "body": "no marker"},
            {"number": 7, "body": f"valid\n{marker}"},
        ]
        result = decide(matches, sig)
        assert result == {"action": "upvote-augment", "issue_number": 7}
