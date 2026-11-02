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


def test_deleted_file_context_line_uses_exact_left_side_anchor() -> None:
    deleted = "--- a/src/a.py\n+++ /dev/null\n@@ -3,1 +2,0 @@\n context\n-old line\n"

    result = select_review_anchor(deleted, source_path="src/a.py", source_line=3)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.anchor.side, result.used_fallback) == (
        "src/a.py",
        3,
        "LEFT",
        False,
    )


def test_replacement_line_prefers_right_side_anchor() -> None:
    replacement = (
        "diff --git a/src/a.py b/src/a.py\n--- a/src/a.py\n+++ b/src/a.py\n@@ -3 +3 @@\n-old line\n+new line\n"
    )

    result = select_review_anchor(replacement, source_path="src/a.py", source_line=3)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.anchor.side, result.used_fallback) == (
        "src/a.py",
        3,
        "RIGHT",
        False,
    )


def test_invalid_suggestion_falls_back_to_first_added_line() -> None:
    result = select_review_anchor(
        _DIFF,
        source_path="src/missing.py",
        source_line=100,
        suggested_path="src/b.py",
        suggested_line=999,
    )

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.used_fallback) == ("src/a.py", 3, True)


def test_deletion_only_diff_uses_left_side_anchor() -> None:
    deleted_only = (
        "diff --git a/src/a.py b/src/a.py\n"
        "deleted file mode 100644\n"
        "--- a/src/a.py\n"
        "+++ /dev/null\n"
        "@@ -3,1 +2,0 @@\n"
        "-old line\n"
    )

    result = select_review_anchor(deleted_only, source_path="src/a.py", source_line=3)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.anchor.side, result.used_fallback) == (
        "src/a.py",
        3,
        "LEFT",
        False,
    )


def test_new_file_diff_uses_right_side_anchor() -> None:
    new_file = (
        "diff --git a/src/new.py b/src/new.py\n"
        "new file mode 100644\n"
        "--- /dev/null\n"
        "+++ b/src/new.py\n"
        "@@ -0,0 +1 @@\n"
        "+new line\n"
    )

    result = select_review_anchor(new_file, source_path="src/new.py", source_line=1)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.anchor.side, result.used_fallback) == (
        "src/new.py",
        1,
        "RIGHT",
        False,
    )
