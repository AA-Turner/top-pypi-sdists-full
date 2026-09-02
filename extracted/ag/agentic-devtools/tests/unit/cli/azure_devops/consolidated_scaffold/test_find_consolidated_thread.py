"""Tests for find_consolidated_thread."""

from agentic_devtools.cli.azure_devops.consolidated_review import build_consolidated_marker
from agentic_devtools.cli.azure_devops.consolidated_scaffold import find_consolidated_thread


def _consolidated_comment(pr: int = 42, commit: str = "abc123") -> str:
    return f"{build_consolidated_marker(pr, commit)}\n## 🔍 Pull Request Review"


class TestFindConsolidatedThread:
    """Tests for find_consolidated_thread."""

    def test_finds_consolidated_thread(self):
        threads = [
            {"id": 10, "comments": [{"id": 1, "content": "system message"}]},
            {"id": 11, "comments": [{"id": 2, "content": _consolidated_comment()}]},
        ]
        assert find_consolidated_thread(threads) == (11, 2)

    def test_returns_last_match_without_commit_hash(self):
        """Without a commit_hash, falls back to the last (newest) consolidated thread."""
        threads = [
            {"id": 11, "comments": [{"id": 2, "content": _consolidated_comment()}]},
            {"id": 12, "comments": [{"id": 3, "content": _consolidated_comment()}]},
        ]
        assert find_consolidated_thread(threads) == (12, 3)

    def test_falls_back_to_highest_thread_id_not_list_order(self):
        """Fallback selection should use the newest thread id, not payload order."""
        threads = [
            {"id": 99, "comments": [{"id": 3, "content": _consolidated_comment(commit="bbb222")}]},
            {"id": 5, "comments": [{"id": 6, "content": _consolidated_comment(commit="ccc333")}]},
            {"id": 200, "comments": [{"id": 2, "content": _consolidated_comment(commit="aaa111")}]},
        ]
        assert find_consolidated_thread(threads) == (200, 2)
        assert find_consolidated_thread(threads, commit_hash="missing") == (200, 2)

    def test_prefers_commit_hash_match(self):
        """With a commit_hash, returns the thread whose marker embeds that exact SHA."""
        threads = [
            {"id": 11, "comments": [{"id": 2, "content": _consolidated_comment(commit="aaa111")}]},
            {"id": 12, "comments": [{"id": 3, "content": _consolidated_comment(commit="bbb222")}]},
        ]
        assert find_consolidated_thread(threads, commit_hash="aaa111") == (11, 2)
        assert find_consolidated_thread(threads, commit_hash="bbb222") == (12, 3)

    def test_falls_back_to_last_when_no_commit_match(self):
        """Falls back to the last candidate when no thread matches the requested commit."""
        threads = [
            {"id": 11, "comments": [{"id": 2, "content": _consolidated_comment(commit="aaa111")}]},
            {"id": 12, "comments": [{"id": 3, "content": _consolidated_comment(commit="bbb222")}]},
        ]
        assert find_consolidated_thread(threads, commit_hash="ccc333") == (12, 3)

    def test_none_when_no_consolidated_comment(self):
        threads = [
            {"id": 10, "comments": [{"id": 1, "content": "<!-- agdt-review:v1 type:overall-summary pr:42 -->"}]},
            {"id": 11, "comments": [{"id": 2, "content": "plain comment"}]},
        ]
        assert find_consolidated_thread(threads) is None

    def test_none_for_empty_threads(self):
        assert find_consolidated_thread([]) is None

    def test_skips_deleted_thread(self):
        threads = [
            {"id": 11, "isDeleted": True, "comments": [{"id": 2, "content": _consolidated_comment()}]},
        ]
        assert find_consolidated_thread(threads) is None

    def test_skips_thread_with_no_comments(self):
        threads = [
            {"id": 11, "comments": []},
            {"id": 12, "comments": [{"id": 3, "content": _consolidated_comment()}]},
        ]
        assert find_consolidated_thread(threads) == (12, 3)

    def test_skips_thread_with_missing_comments_key(self):
        threads = [
            {"id": 11},
            {"id": 12, "comments": [{"id": 3, "content": _consolidated_comment()}]},
        ]
        assert find_consolidated_thread(threads) == (12, 3)

    def test_skips_deleted_first_comment(self):
        threads = [
            {"id": 11, "comments": [{"id": 2, "isDeleted": True, "content": _consolidated_comment()}]},
        ]
        assert find_consolidated_thread(threads) is None

    def test_finds_consolidated_comment_after_deleted_first(self):
        """Should find consolidated marker when first comment is deleted but a later one carries it."""
        threads = [
            {
                "id": 11,
                "comments": [
                    {"id": 1, "isDeleted": True, "content": "deleted system comment"},
                    {"id": 2, "content": _consolidated_comment()},
                ],
            }
        ]
        assert find_consolidated_thread(threads) == (11, 2)

    def test_uses_newest_marker_comment_within_thread(self):
        """Cross-identity fallback replies should win over older marker comments."""
        threads = [
            {
                "id": 11,
                "comments": [
                    {"id": 2, "content": _consolidated_comment(commit="aaa111")},
                    {"id": 7, "content": _consolidated_comment(commit="aaa111")},
                ],
            }
        ]
        assert find_consolidated_thread(threads) == (11, 7)
        assert find_consolidated_thread(threads, commit_hash="aaa111") == (11, 7)

    def test_candidate_without_commit_token_not_in_commit_map(self):
        """Consolidated comment with no commit: token still added to candidates but not commit map."""
        no_hash_content = f"{build_consolidated_marker(42, commit_hash=None)}\n## Review"
        threads = [{"id": 11, "comments": [{"id": 2, "content": no_hash_content}]}]
        # Finds the thread via the candidates fallback (not via commit-hash map)
        assert find_consolidated_thread(threads) == (11, 2)
        # With a requested commit hash that doesn't match, still falls back to the last candidate
        assert find_consolidated_thread(threads, commit_hash="deadbeef") == (11, 2)
