"""Tests for a focused review-anchor selection helper."""

from agentic_devtools.cli.ci.review_thread_promotion import select_review_anchor

_DIFF = """diff --git a/src/a.py b/src/a.py
--- a/src/a.py
+++ b/src/a.py
@@ -2,2 +2,3 @@
 context
+added one
 context
diff --git a/src/b.py b/src/b.py
--- a/src/b.py
+++ b/src/b.py
@@ -8,1 +8,2 @@
+added two
 context
"""


def test_suggested_replacement_line_prefers_right_side_anchor() -> None:
    replacement = (
        "diff --git a/src/a.py b/src/a.py\n--- a/src/a.py\n+++ b/src/a.py\n@@ -3 +3 @@\n-old line\n+new line\n"
    )

    result = select_review_anchor(
        replacement,
        source_path="src/unrelated.py",
        source_line=3,
        suggested_path="src/a.py",
        suggested_line=3,
    )

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.anchor.side, result.used_fallback) == (
        "src/a.py",
        3,
        "RIGHT",
        True,
    )


def test_nearest_same_file_changed_line_is_used_before_suggestion() -> None:
    result = select_review_anchor(
        _DIFF,
        source_path="src/a.py",
        source_line=100,
        suggested_path="src/b.py",
        suggested_line=8,
    )

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.used_fallback) == ("src/a.py", 3, True)


def test_valid_suggested_cross_file_line_is_used() -> None:
    result = select_review_anchor(
        _DIFF,
        source_path="src/missing.py",
        source_line=100,
        suggested_path="src/b.py",
        suggested_line=8,
    )

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.used_fallback) == ("src/b.py", 8, True)
