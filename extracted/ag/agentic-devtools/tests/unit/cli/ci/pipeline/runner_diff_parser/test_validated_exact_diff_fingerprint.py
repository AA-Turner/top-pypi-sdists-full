"""Tests for validated_exact_diff_fingerprint."""

import hashlib

import pytest

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import validated_exact_diff_fingerprint


def test_validates_complete_hunks_and_hashes_full_diff() -> None:
    """A complete text patch with context and no-newline markers receives an exact hash."""
    exact_diff = (
        "diff --git a/fix.py b/fix.py\n"
        "--- a/fix.py\n"
        "+++ b/fix.py\n"
        "@@ -1,2 +1,2 @@\n"
        " keep\n"
        "-old\n"
        "+new\n"
        r"\ No newline at end of file"
        "\n"
    )

    assert validated_exact_diff_fingerprint(exact_diff, ["fix.py"], {"fix.py": 2}) == (
        f"exact-diff-sha256:{hashlib.sha256(exact_diff.encode('utf-8')).hexdigest()}"
    )


def test_accepts_no_newline_marker_between_complete_hunk_lines() -> None:
    """A no-newline marker between deletion and addition lines does not alter hunk counts."""
    exact_diff = (
        "diff --git a/fix.py b/fix.py\n"
        "@@ -1 +1 @@\n"
        "-old\n"
        r"\ No newline at end of file"
        "\n"
        "+new\n"
    )

    assert validated_exact_diff_fingerprint(exact_diff, ["fix.py"], {"fix.py": 2}).startswith("exact-diff-sha256:")


def test_accepts_mode_changing_pure_rename_without_content_changes() -> None:
    """A pure rename with a supported mode change is valid without content hunks."""
    exact_diff = (
        "diff --git a/script.sh b/renamed.sh\n"
        "old mode 100644\n"
        "new mode 100755\n"
        "similarity index 100%\n"
        "rename from script.sh\n"
        "rename to renamed.sh\n"
    )

    assert validated_exact_diff_fingerprint(exact_diff, ["renamed.sh"], {"renamed.sh": 0}).startswith(
        "exact-diff-sha256:"
    )


def test_resolves_ambiguous_paths_with_tab_separated_unified_headers() -> None:
    """Separator tabs in unquoted unified headers do not become part of the path."""
    exact_diff = (
        "diff --git a/dir b/name.py b/dir b/name.py\n"
        "--- a/dir b/name.py\t\n"
        "+++ b/dir b/name.py\t\n"
        "@@ -1 +1 @@\n"
        "-old\n"
        "+new\n"
        "diff --git a/name.py b/name.py\n"
        "@@ -1 +1 @@\n"
        "-old\n"
        "+new\n"
    )

    assert validated_exact_diff_fingerprint(
        exact_diff,
        ["dir b/name.py", "name.py"],
        {"dir b/name.py": 2, "name.py": 2},
    ).startswith("exact-diff-sha256:")


def test_ignores_header_like_hunk_lines_when_disambiguating_paths() -> None:
    """Hunk deletions and additions that resemble path headers are not metadata."""
    exact_diff = (
        "diff --git a/dir b/name.py b/dir b/name.py\n"
        '--- "a/dir b/name.py"\n'
        '+++ "b/dir b/name.py"\n'
        "@@ -1 +1 @@\n"
        "--- obsolete\n"
        "+++ replacement\n"
        "diff --git a/name.py b/name.py\n"
        "@@ -1 +1 @@\n"
        "-old\n"
        "+new\n"
    )

    assert validated_exact_diff_fingerprint(
        exact_diff,
        ["dir b/name.py", "name.py"],
        {"dir b/name.py": 2, "name.py": 2},
    ).startswith("exact-diff-sha256:")


def test_rejects_entirely_omitted_final_hunk_using_provider_change_counts() -> None:
    """A structurally complete prefix is rejected when provider totals reveal a missing hunk."""
    full_patches = (
        "diff --git a/fix.py b/fix.py\n"
        "--- a/fix.py\n"
        "+++ b/fix.py\n"
        "@@ -1 +1 @@\n-old\n+same\n"
        "@@ -10 +10 @@\n-old-final\n+first-final\n",
        "diff --git a/fix.py b/fix.py\n"
        "--- a/fix.py\n"
        "+++ b/fix.py\n"
        "@@ -1 +1 @@\n-old\n+same\n"
        "@@ -10 +10 @@\n-old-final\n+different-final\n",
    )

    for full_diff in full_patches:
        truncated_diff = full_diff[: full_diff.rfind("@@ -10 +10 @@")]
        assert validated_exact_diff_fingerprint(truncated_diff, ["fix.py"], {"fix.py": 4}) == ""


def _fixture_change_counts(exact_diff: str, expected_files: list[str]) -> dict[str, int]:
    """Report the fixture's textual additions and deletions without trusting hunk headers."""
    changed_lines = sum(
        line.startswith(("+", "-")) and not line.startswith(("+++", "---")) for line in exact_diff.splitlines()
    )
    return {path: changed_lines if len(set(expected_files)) == 1 else 0 for path in expected_files}


@pytest.mark.parametrize(
    ("exact_diff", "expected_files"),
    [
        ("", ["file.py"]),
        ("diff --git \n", ["file.py"]),
        ("diff --git a/file.py b/file.py\n", ["file.py"]),
        ("diff --git a/file.py b/file.py\n@@ -1 +1 @@\n-old\n+new", ["file.py"]),
        ("diff --git a/file.py b/file.py\n@@ -1 +1 @@\n-old\n+new\n", []),
        ("diff --git a/file.py b/file.py\n@@ -1 +1 @@\n-old\n+new\n", ["file.py", "file.py"]),
        ("preamble\ndiff --git a/file.py b/file.py\n@@ -1 +1 @@\n-old\n+new\n", ["file.py"]),
        ("diff --git a/file.py\n@@ -1 +1 @@\n-old\n+new\n", ["file.py"]),
        ('diff --git a/file.py "b/file.py\n@@ -1 +1 @@\n-old\n+new\n', ["file.py"]),
        ('diff --git "a/file.py b/file.py\n@@ -1 +1 @@\n-old\n+new\n', ["file.py"]),
        (
            'diff --git "a/file.py' + "\\" + "\n@@ -1 +1 @@\n-old\n+new\n",
            ["file.py"],
        ),
        ("diff --git x/file.py b/file.py\n@@ -1 +1 @@\n-old\n+new\n", ["file.py"]),
        ("diff --git a/file.py x/file.py\n@@ -1 +1 @@\n-old\n+new\n", ["file.py"]),
        (r'diff --git "a/file\q.py" "b/file\q.py"' + "\n@@ -1 +1 @@\n-old\n+new\n", ["file.py"]),
        ('diff --git "a/\\377.py" "b/\\377.py"\n@@ -1 +1 @@\n-old\n+new\n', ["�.py"]),
        ("diff --git a/other.py b/other.py\n@@ -1 +1 @@\n-old\n+new\n", ["file.py"]),
        (
            "diff --git a/file.py b/file.py\n@@ -1 +1 @@\n-old\n+new\n"
            "diff --git a/file.py b/file.py\n@@ -1 +1 @@\n-old\n+new\n",
            ["file.py"],
        ),
        ("diff --git a/file.py b/file.py\n@@ malformed\n-old\n+new\n", ["file.py"]),
        ("diff --git a/file.py b/file.py\n@@ -1,2 +1,2 @@\n-old\n+new\n", ["file.py"]),
        ("diff --git a/file.py b/file.py\n@@ -1 +1,2 @@\n-old\n-two\n", ["file.py"]),
        ("diff --git a/file.py b/file.py\n@@ -1 +1 @@\n-old\n+new\n+extra\n", ["file.py"]),
        ("diff --git a/file.py b/file.py\n@@ -1 +1 @@\ninvalid\n+new\n", ["file.py"]),
        (
            "diff --git a/file.py b/file.py\n@@ -1 +1 @@\n-old\n+new\ntrailing text\n",
            ["file.py"],
        ),
        ("diff --git a/file.py b/file.py\nBinary files a/file.py and b/file.py differ\n", ["file.py"]),
        ("diff --git a/file.py b/file.py\nGIT binary patch\n", ["file.py"]),
        ("diff --git a/file.py b/file.py\nunsupported metadata\n", ["file.py"]),
        ("diff --git a/file.py b/file.py\nindex 123..456\n", ["file.py"]),
        (
            "diff --git a/script.sh b/script.sh\nold mode 100644\nnew mode 120000\n",
            ["script.sh"],
        ),
        (
            "diff --git a/script.sh b/script.sh\nold mode 100644\nnew mode 100755\n",
            ["script.sh"],
        ),
        ("diff --git a/file.py b/file.py\n@@ -0,0 +0,0 @@\n", ["file.py"]),
        ("diff --git a/file.py b/file.py\n@@ -1 +1 @@\n\\ No newline at end of file\n-old\n+new\n", ["file.py"]),
        ('diff --git "a/file.py"x "b/file.py"\n@@ -1 +1 @@\n-old\n+new\n', ["file.py"]),
        ('diff --git "a/file.py" "b/file.py" suffix\n@@ -1 +1 @@\n-old\n+new\n', ["file.py"]),
        ("diff --git a/file.py b/\n@@ -1 +1 @@\n-old\n+new\n", [""]),
        ("diff --git a/dir b/name.py b/dir b/name.py\n", ["dir b/name.py", "name.py"]),
        (
            'diff --git a/dir b/name.py b/dir b/name.py\n--- "a/unterminated\n+++ b/dir b/name.py\n',
            ["dir b/name.py", "name.py"],
        ),
        (
            "diff --git a/dir b/name.py b/dir b/name.py\n--- a/dir b/name.py\n+++ x/dir b/name.py\n",
            ["dir b/name.py", "name.py"],
        ),
        (
            'diff --git a/old.py b/dir b/name.py\nrename from "unterminated\nrename to dir b/name.py\n',
            ["dir b/name.py", "name.py"],
        ),
        (
            "diff --git a/file.py b/file.py\nsimilarity index 50%\nsimilarity index 50%\n@@ -1 +1 @@\n-old\n+new\n",
            ["file.py"],
        ),
        (
            "diff --git a/old.py b/new.py\nsimilarity index 50%\nrename from old.py\nrename to new.py\n",
            ["new.py"],
        ),
        (
            "diff --git a/old.py b/new.py\nrename from other.py\nrename to new.py\n",
            ["new.py"],
        ),
        (
            "diff --git a/old.py b/new.py\nrename from \nrename to new.py\n",
            ["new.py"],
        ),
        (
            "diff --git a/__init__.py b/__init__.py\n"
            "new file mode 100644\n"
            "index malformed\n"
            "--- /dev/null\n"
            "+++ b/__init__.py\n",
            ["__init__.py"],
        ),
        (
            "diff --git a/__init__.py b/__init__.py\n"
            "new file mode 100644\n"
            "index 00000000..e69de29\n"
            "--- /dev/null\n"
            "+++ b/__init__.py\n",
            ["__init__.py"],
        ),
        (
            "diff --git a/__init__.py b/__init__.py\n"
            "new file mode 100644\n"
            "index 1234567..e69de29\n"
            "--- /dev/null\n"
            "+++ b/__init__.py\n",
            ["__init__.py"],
        ),
        (
            "diff --git a/__init__.py b/__init__.py\n"
            "new file mode 100644\n"
            "index 0000000..1234567\n"
            "--- /dev/null\n"
            "+++ b/__init__.py\n",
            ["__init__.py"],
        ),
        (
            "diff --git a/__init__.py b/__init__.py\n"
            "new file mode invalid\n"
            "index 0000000..e69de29\n"
            "--- /dev/null\n"
            "+++ b/__init__.py\n",
            ["__init__.py"],
        ),
        (
            "diff --git a/empty.py b/empty.py\ndeleted file mode 120000\nindex e69de29..0000000\n",
            ["empty.py"],
        ),
        (
            "diff --git a/empty.py b/empty.py\ndeleted file mode 100644\nindex malformed\n",
            ["empty.py"],
        ),
        (
            "diff --git a/empty.py b/empty.py\ndeleted file mode 100644\nindex e69de29..00000000\n",
            ["empty.py"],
        ),
        (
            "diff --git a/empty.py b/empty.py\ndeleted file mode 100644\nindex 1234567..0000000\n",
            ["empty.py"],
        ),
        (
            "diff --git a/empty.py b/empty.py\ndeleted file mode 100644\nindex e69de29..1234567\n",
            ["empty.py"],
        ),
        (
            'diff --git a/old.py b/new.py\nrename from "old.py\nrename to new.py\n',
            ["new.py"],
        ),
        (
            'diff --git a/old.py b/new.py\nrename from "old.py" suffix\nrename to new.py\n',
            ["new.py"],
        ),
        (
            "diff --git a/old.py b/new.py\nrename from old.py\nrename from old.py\nrename to new.py\n",
            ["new.py"],
        ),
        (
            "diff --git a/old.py b/new.py\nrename from old.py\nrename to new.py\nrename to new.py\n",
            ["new.py"],
        ),
        ("diff --git a/old.py b/new.py\nrename from old.py\n", ["new.py"]),
        (
            "diff --git a/old.py b/new.py\n"
            "old mode 100600\n"
            "new mode 100755\n"
            "similarity index 100%\n"
            "rename from old.py\n"
            "rename to new.py\n",
            ["new.py"],
        ),
        (
            "diff --git a/old.py b/new.py\n"
            "old mode 100644\n"
            "new mode 100600\n"
            "similarity index 100%\n"
            "rename from old.py\n"
            "rename to new.py\n",
            ["new.py"],
        ),
        (
            "diff --git a/old.py b/new.py\n"
            "old mode 100644\n"
            "new mode 100644\n"
            "similarity index 100%\n"
            "rename from old.py\n"
            "rename to new.py\n",
            ["new.py"],
        ),
    ],
    ids=[
        "empty",
        "empty-header",
        "header-only",
        "missing-terminal-newline",
        "empty-inventory",
        "duplicate-expected-path",
        "preamble",
        "missing-second-path",
        "unterminated-new-path",
        "unterminated-quote",
        "trailing-escape",
        "invalid-old-prefix",
        "invalid-new-prefix",
        "unknown-escape",
        "invalid-utf8-path",
        "inventory-mismatch",
        "duplicate-file-header",
        "malformed-hunk",
        "truncated-hunk",
        "over-counted-deletion",
        "overlong-hunk",
        "invalid-hunk-line",
        "trailing-content",
        "opaque-binary",
        "git-binary-patch",
        "unsupported-metadata",
        "metadata-only",
        "unsupported-mode-only-change",
        "ambiguous-truncated-mode-prefix",
        "empty-hunk",
        "orphan-no-newline-marker",
        "malformed-quoted-old-separator",
        "quoted-new-path-extra-text",
        "empty-destination",
        "ambiguous-without-patch-paths",
        "ambiguous-malformed-old-patch-path",
        "ambiguous-invalid-new-patch-prefix",
        "ambiguous-malformed-rename-metadata",
        "duplicate-similarity-index",
        "truncated-modified-rename",
        "mismatched-pure-rename",
        "empty-rename-source",
        "malformed-empty-file-index",
        "mismatched-empty-hash-length",
        "nonzero-empty-file-old-hash",
        "nonempty-new-file-hash",
        "invalid-empty-file-mode",
        "invalid-empty-deletion-mode",
        "malformed-empty-deletion-index",
        "mismatched-empty-deletion-hash-length",
        "nonempty-empty-deletion-old-hash",
        "nonzero-empty-deletion-new-hash",
        "malformed-rename-from",
        "rename-from-with-extra-text",
        "duplicate-rename-from",
        "duplicate-rename-to",
        "orphaned-rename-from",
        "invalid-old-mode-in-rename",
        "invalid-new-mode-in-rename",
        "unchanged-mode-in-rename",
    ],
)
def test_rejects_untrusted_or_incomplete_diff(exact_diff: str, expected_files: list[str]) -> None:
    """Malformed, truncated, opaque, and mismatched patches cannot be fingerprinted."""
    assert (
        validated_exact_diff_fingerprint(exact_diff, expected_files, _fixture_change_counts(exact_diff, expected_files))
        == ""
    )
