"""Tests for validated CCR review-thread anchor selection."""

from agentic_devtools.cli.ci.review_thread_promotion import AnchorSelection, select_review_anchor

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


def _select_with_literal_path_absent(source_line: int) -> AnchorSelection | None:
    return select_review_anchor(
        _DIFF, source_path="src/\u200ba.py", source_line=source_line, source_path_exists_in_captured_trees=False
    )


def test_exact_source_line_is_preferred_without_fallback() -> None:
    result = select_review_anchor(_DIFF, source_path="src/a.py", source_line=3)

    assert result is not None
    assert result.anchor.path == "src/a.py"
    assert result.anchor.line == 3
    assert result.used_fallback is False


def test_exact_context_line_is_preferred_without_fallback() -> None:
    result = select_review_anchor(_DIFF, source_path="src/a.py", source_line=4)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.anchor.side, result.used_fallback) == (
        "src/a.py",
        4,
        "RIGHT",
        False,
    )


def test_zero_width_space_after_path_separator_keeps_exact_added_anchor() -> None:
    result = _select_with_literal_path_absent(3)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.anchor.side, result.used_fallback) == (
        "src/a.py",
        3,
        "RIGHT",
        False,
    )


def test_zero_width_space_after_path_separator_keeps_exact_context_anchor() -> None:
    result = _select_with_literal_path_absent(4)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.anchor.side, result.used_fallback) == (
        "src/a.py",
        4,
        "RIGHT",
        False,
    )


def test_zero_width_space_after_path_separator_uses_matching_file_for_fallback() -> None:
    result = _select_with_literal_path_absent(100)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.used_fallback) == ("src/a.py", 3, True)


def test_zero_width_space_inside_filename_is_not_removed() -> None:
    result = select_review_anchor(_DIFF, source_path="src/a\u200b.py", source_line=3)

    assert result is not None
    assert result.used_fallback is True


def test_clean_source_path_does_not_match_literal_zero_width_diff_filename() -> None:
    literal_path_diff = _DIFF.replace("src/a.py", "src/a\u200b.py")

    result = select_review_anchor(literal_path_diff, source_path="src/a.py", source_line=3)

    assert result is not None
    assert (result.anchor.path, result.used_fallback) == ("src/a\u200b.py", True)


def test_exact_literal_zero_width_path_wins_over_its_clean_equivalent() -> None:
    ambiguous = (
        "diff --git a/src/a.py b/src/a.py\n"
        "--- a/src/a.py\n"
        "+++ b/src/a.py\n"
        "@@ -2,0 +3,1 @@\n"
        "+clean\n"
        "diff --git a/src/\u200ba.py b/src/\u200ba.py\n"
        "--- a/src/\u200ba.py\n"
        "+++ b/src/\u200ba.py\n"
        "@@ -2,0 +3,1 @@\n"
        "+literal\n"
    )

    result = select_review_anchor(ambiguous, source_path="src/\u200ba.py", source_line=3)

    assert result is not None
    assert (result.anchor.path, result.used_fallback) == ("src/\u200ba.py", False)


def test_hunkless_literal_path_blocks_normalized_exact_anchor_match() -> None:
    diff = (
        "diff --git a/src/\u200ba.py b/src/\u200ba.py\n"
        "old mode 100644\n"
        "new mode 100755\n"
        "diff --git a/src/a.py b/src/a.py\n"
        "--- a/src/a.py\n"
        "+++ b/src/a.py\n"
        "@@ -2,0 +3,1 @@\n"
        "+clean file change\n"
    )

    result = select_review_anchor(diff, source_path="src/\u200ba.py", source_line=3)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.used_fallback) == ("src/a.py", 3, True)
    assert result.matched_source_path is False


def test_hunkless_mixed_quoted_rename_blocks_normalized_exact_anchor_match() -> None:
    diff = (
        r'diff --git a/src/old.py "b/src/\342\200\213a.py"' + "\n"
        "diff --git a/src/a.py b/src/a.py\n"
        "--- a/src/a.py\n"
        "+++ b/src/a.py\n"
        "@@ -2,0 +3,1 @@\n"
        "+clean file change\n"
    )

    result = select_review_anchor(diff, source_path="src/\u200ba.py", source_line=3)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.used_fallback) == ("src/a.py", 3, True)


def test_hunkless_ambiguous_unquoted_rename_blocks_normalized_exact_anchor_match() -> None:
    diff = (
        "diff --git a/src/\u200bfolder b/a.py b/src/\u200bfolder b/a.py\n"
        "old mode 100644\n"
        "new mode 100755\n"
        "diff --git a/src/folder b/a.py b/src/folder b/a.py\n"
        "--- a/src/folder b/a.py\n"
        "+++ b/src/folder b/a.py\n"
        "@@ -2,0 +3,1 @@\n"
        "+clean file change\n"
    )

    result = select_review_anchor(diff, source_path="src/\u200bfolder b/a.py", source_line=3)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.used_fallback, result.matched_source_path) == (
        "src/folder b/a.py",
        3,
        True,
        False,
    )


def test_hunkless_unquoted_rename_destination_blocks_normalized_exact_anchor_match() -> None:
    diff = (
        "diff --git a/src/old b/name.py b/src/\u200ba.py\n"
        "old mode 100644\n"
        "new mode 100755\n"
        "diff --git a/src/a.py b/src/a.py\n"
        "--- a/src/a.py\n"
        "+++ b/src/a.py\n"
        "@@ -2,0 +3,1 @@\n"
        "+clean file change\n"
    )

    result = select_review_anchor(diff, source_path="src/\u200ba.py", source_line=3)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.used_fallback, result.matched_source_path) == (
        "src/a.py",
        3,
        True,
        False,
    )


def test_hunkless_rename_destination_preserves_literal_b_directory_prefix() -> None:
    diff = (
        "diff --git a/src/old b/name.py b/b/src/\u200ba.py\n"
        "old mode 100644\n"
        "new mode 100755\n"
        "diff --git a/b/src/a.py b/b/src/a.py\n"
        "--- a/b/src/a.py\n"
        "+++ b/b/src/a.py\n"
        "@@ -2,0 +3,1 @@\n"
        "+clean file change\n"
    )

    result = select_review_anchor(diff, source_path="b/src/\u200ba.py", source_line=3)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.used_fallback, result.matched_source_path) == (
        "b/src/a.py",
        3,
        True,
        False,
    )


def test_hunkless_mixed_quoted_rename_with_spaced_source_blocks_normalized_match() -> None:
    diff = (
        r'diff --git a/src/old name.py "b/src/\342\200\213a.py"' + "\n"
        "diff --git a/src/a.py b/src/a.py\n"
        "--- a/src/a.py\n"
        "+++ b/src/a.py\n"
        "@@ -2,0 +3,1 @@\n"
        "+clean file change\n"
    )

    result = select_review_anchor(diff, source_path="src/\u200ba.py", source_line=3)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.used_fallback, result.matched_source_path) == (
        "src/a.py",
        3,
        True,
        False,
    )


def test_hunkless_quoted_rename_with_embedded_b_path_separator_blocks_normalized_match() -> None:
    diff = (
        r'diff --git a/src/old.py "b/src/\342\200\213folder b/a.py"' + "\n"
        "diff --git a/src/folder b/a.py b/src/folder b/a.py\n"
        "--- a/src/folder b/a.py\n"
        "+++ b/src/folder b/a.py\n"
        "@@ -2,0 +3,1 @@\n"
        "+clean file change\n"
    )

    result = select_review_anchor(diff, source_path="src/\u200bfolder b/a.py", source_line=3)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.used_fallback, result.matched_source_path) == (
        "src/folder b/a.py",
        3,
        True,
        False,
    )


def test_unmatched_diff_header_uses_file_markers_to_select_anchor() -> None:
    diff = "diff --git malformed\n--- a/src/a.py\n+++ b/src/a.py\n@@ -2,0 +3,1 @@\n+added line\n"

    result = select_review_anchor(diff, source_path="src/a.py", source_line=3)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.used_fallback) == ("src/a.py", 3, False)


def test_context_line_without_a_current_path_is_not_an_anchor() -> None:
    deleted = "--- a/src/a.py\n+++ /dev/null\n@@ -3,1 +2,0 @@\n context\n-old line\n"

    result = select_review_anchor(deleted, source_path="", source_line=2)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.anchor.side, result.used_fallback) == (
        "src/a.py",
        4,
        "LEFT",
        True,
    )
