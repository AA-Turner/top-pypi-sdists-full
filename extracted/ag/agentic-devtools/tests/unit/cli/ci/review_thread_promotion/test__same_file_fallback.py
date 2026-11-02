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


def test_same_file_fallback_without_source_line_uses_first_added_line_in_file() -> None:
    result = select_review_anchor(_DIFF, source_path="src/a.py", source_line=None)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.used_fallback) == ("src/a.py", 3, True)
