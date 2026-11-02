"""Tests for a focused review-anchor selection helper."""

from agentic_devtools.cli.ci.review_thread_promotion import select_review_anchor


def test_invalid_quoted_original_path_is_not_used_for_left_anchor() -> None:
    malformed_deleted_file = '--- "a/src/unterminated.py\n+++ /dev/null\n@@ -3,1 +2,0 @@\n context\n-old line\n'

    assert select_review_anchor(malformed_deleted_file, source_path="src/unterminated.py", source_line=3) is None


def test_unchanged_literal_source_path_uses_disclosed_fallback() -> None:
    diff = "diff --git a/src/a.py b/src/a.py\n--- a/src/a.py\n+++ b/src/a.py\n@@ -2,0 +3,1 @@\n+clean file change\n"

    result = select_review_anchor(
        diff,
        source_path="src/\u200ba.py",
        source_line=3,
        captured_tree_context=("base", "head", lambda _args: "src/\u200ba.py\0"),
    )

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.used_fallback, result.matched_source_path) == (
        "src/a.py",
        3,
        True,
        False,
    )
