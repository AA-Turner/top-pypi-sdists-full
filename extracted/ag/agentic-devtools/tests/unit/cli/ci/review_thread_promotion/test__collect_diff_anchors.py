"""Tests for a focused review-anchor selection helper."""

from agentic_devtools.cli.ci.review_thread_promotion import select_review_anchor


def test_quoted_git_path_is_decoded_before_selecting_anchor() -> None:
    diff = (
        r'diff --git "a/src/a\tb\"c\\d\303\251.py" "b/src/a\tb\"c\\d\303\251.py"' + "\n"
        r'--- "a/src/a\tb\"c\\d\303\251.py"' + "\n"
        r'+++ "b/src/a\tb\"c\\d\303\251.py"' + "\n"
        "@@ -2,0 +3,1 @@\n+added line\n"
    )

    result = select_review_anchor(
        diff,
        source_path='src/a\tb"c\\dé.py',
        source_line=3,
    )

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.used_fallback) == (
        'src/a\tb"c\\dé.py',
        3,
        False,
    )


def test_raw_unicode_mode_only_path_blocks_normalized_alias_fallback() -> None:
    diff = (
        'diff --git "a/src/\u200ba\\tb.py" "b/src/\u200ba\\tb.py"\n'
        "old mode 100644\n"
        "new mode 100755\n"
        'diff --git "a/src/a\\tb.py" "b/src/a\\tb.py"\n'
        '--- "a/src/a\\tb.py"\n'
        '+++ "b/src/a\\tb.py"\n'
        "@@ -0,0 +3,1 @@\n"
        "+added line\n"
    )

    result = select_review_anchor(
        diff,
        source_path="src/\u200ba\tb.py",
        source_line=3,
    )

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.used_fallback) == ("src/a\tb.py", 3, True)


def test_invalid_quoted_git_path_is_not_used_as_an_anchor() -> None:
    diff = '+++ "b/src/unterminated.py\n@@ -2,0 +3,1 @@\n+added line\n'

    assert select_review_anchor(diff, source_path="src/unterminated.py", source_line=3) is None


def test_invalid_quoted_diff_header_path_is_not_used_as_an_anchor() -> None:
    diff = r'diff --git "a/src/\xzz.py" "b/src/\xzz.py"' + "\n"

    assert select_review_anchor(diff, source_path="src/invalid.py", source_line=1) is None


def test_empty_diff_header_paths_are_ignored() -> None:
    diff = "diff --git a/ b/\n--- a/\n+++ b/\n@@ -0,0 +1,1 @@\n+added line\n"

    assert select_review_anchor(diff, source_path="", source_line=1) is None


def test_added_line_starting_with_plus_keeps_following_line_number_correct() -> None:
    diff = (
        "diff --git a/src/a.py b/src/a.py\n"
        "--- a/src/a.py\n"
        "+++ b/src/a.py\n"
        "@@ -0,0 +3,2 @@\n"
        "++literal plus\n"
        "+following line\n"
    )

    result = select_review_anchor(diff, source_path="src/a.py", source_line=4)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.used_fallback) == ("src/a.py", 4, False)


def test_added_line_starting_with_header_prefix_is_not_treated_as_a_file_header() -> None:
    diff = (
        "diff --git a/src/a.py b/src/a.py\n"
        "--- a/src/a.py\n"
        "+++ b/src/a.py\n"
        "@@ -0,0 +1,1 @@\n"
        "+++ text\n"
        "\\ No newline at end of file\n"
    )

    result = select_review_anchor(diff, source_path="src/a.py", source_line=1)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.anchor.side, result.used_fallback) == (
        "src/a.py",
        1,
        "RIGHT",
        False,
    )


def test_deleted_line_starting_with_header_prefix_is_not_treated_as_a_file_header() -> None:
    diff = "diff --git a/src/a.py b/src/a.py\n--- a/src/a.py\n+++ b/src/a.py\n@@ -1,1 +1,0 @@\n--- text\n"

    result = select_review_anchor(diff, source_path="src/a.py", source_line=1)

    assert result is not None
    assert (result.anchor.path, result.anchor.line, result.anchor.side, result.used_fallback) == (
        "src/a.py",
        1,
        "LEFT",
        False,
    )


def test_empty_diff_has_no_valid_anchor() -> None:
    assert select_review_anchor("", source_path="src/a.py", source_line=3) is None
