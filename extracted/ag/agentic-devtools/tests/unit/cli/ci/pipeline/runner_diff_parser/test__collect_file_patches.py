"""Tests for collecting file paths from exact diffs."""

import pytest

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _collect_file_patches


def _assert_collected_paths(exact_diff: str, expected_paths: list[str]) -> None:
    file_patches = _collect_file_patches(exact_diff.split("\n")[:-1], set(expected_paths))

    assert file_patches is not None
    assert [new_path for _, new_path, _ in file_patches] == expected_paths


@pytest.mark.parametrize(
    ("exact_diff", "expected_file"),
    [
        (
            "diff --git a/old.py b/new.py\n"
            "similarity index 50%\n"
            "rename from old.py\n"
            "rename to new.py\n"
            "@@ -1 +1 @@\n-old\n+new\n",
            "new.py",
        ),
        (
            "diff --git a/old.py b/new.py\nsimilarity index 100%\nrename from old.py\nrename to new.py\n",
            "new.py",
        ),
        (
            'diff --git "a/space\\tname.py" "b/space\\tname.py"\n@@ -1 +1 @@\n-old\n+new\n',
            "space\tname.py",
        ),
        (
            "diff --git a/my file.py b/my file.py\n@@ -1 +1 @@\n-old\n+new\n",
            "my file.py",
        ),
        (
            "diff --git a/trailing  b/trailing \n@@ -1 +1 @@\n-old\n+new\n",
            "trailing ",
        ),
        (
            "diff --git a/old file.py b/new file.py\n"
            "similarity index 100%\n"
            "rename from old file.py\n"
            "rename to new file.py\n",
            "new file.py",
        ),
        (
            "diff --git a/file.py b/file.py\n@@ -1 +1 @@\n-old\n+new\u2028suffix\n",
            "file.py",
        ),
        (
            "diff --git a/__init__.py b/__init__.py\n"
            "new file mode 100644\n"
            "index 0000000..e69de29\n"
            "--- /dev/null\n"
            "+++ b/__init__.py\n",
            "__init__.py",
        ),
        (
            'diff --git "a/caf\\303\\251.py" "b/caf\\303\\251.py"\n@@ -1 +1 @@\n-old\n+new\n',
            "café.py",
        ),
        (
            'diff --git "a/caf\\303\\251.py" "b/caf\\303\\251.py"\n'
            "similarity index 100%\n"
            'rename from "caf\\303\\251.py"\n'
            'rename to "caf\\303\\251.py"\n',
            "café.py",
        ),
        (
            "diff --git a/__init__.py b/__init__.py\nnew file mode 100644\nindex 0000000..e69de29\n",
            "__init__.py",
        ),
        (
            "diff --git a/empty.py b/empty.py\ndeleted file mode 100644\nindex e69de29..0000000\n",
            "empty.py",
        ),
    ],
    ids=(
        "rename-destination",
        "pure-rename",
        "escaped-tab",
        "unquoted-space",
        "unquoted-trailing-space",
        "unquoted-rename-spaces",
        "unicode-line-separator",
        "empty-file",
        "octal-utf8",
        "quoted-pure-rename",
        "canonical-empty-file",
        "empty-file-deletion",
    ),
)
def test_collects_decoded_destination_paths(exact_diff: str, expected_file: str) -> None:
    """Git-quoted and renamed paths are retained as decoded destination names."""
    _assert_collected_paths(exact_diff, [expected_file])


def test_resolves_ambiguous_diff_header_from_patch_paths() -> None:
    """Explicit unified-diff paths disambiguate headers when both destinations are inventoried."""
    exact_diff = (
        "diff --git a/dir b/name.py b/dir b/name.py\n"
        "--- a/dir b/name.py\n"
        "+++ b/dir b/name.py\n"
        "@@ -1 +1 @@\n-old\n+new\n"
        "diff --git a/name.py b/name.py\n"
        "--- a/name.py\n"
        "+++ b/name.py\n"
        "@@ -1 +1 @@\n-old\n+new\n"
    )

    _assert_collected_paths(exact_diff, ["dir b/name.py", "name.py"])


def test_resolves_ambiguous_pure_rename_header_from_rename_metadata() -> None:
    """Rename metadata disambiguates a pure rename when both destinations are inventoried."""
    exact_diff = (
        "diff --git a/old.py b/dir b/name.py\n"
        "similarity index 100%\n"
        "rename from old.py\n"
        "rename to dir b/name.py\n"
        "diff --git a/name.py b/name.py\n"
        "@@ -1 +1 @@\n-old\n+new\n"
    )

    _assert_collected_paths(exact_diff, ["dir b/name.py", "name.py"])


def test_resolves_ambiguous_new_file_header_from_destination_path() -> None:
    """An explicit destination path resolves an ambiguous header for a new file."""
    exact_diff = (
        "diff --git a/dir b/name.py b/dir b/name.py\n"
        "new file mode 100644\n"
        "--- /dev/null\n"
        "+++ b/dir b/name.py\n"
        "@@ -0,0 +1 @@\n+new\n"
        "diff --git a/name.py b/name.py\n"
        "@@ -1 +1 @@\n-old\n+new\n"
    )

    _assert_collected_paths(exact_diff, ["dir b/name.py", "name.py"])


@pytest.mark.parametrize(
    ("file_metadata", "index"),
    [
        ("new file mode 100644", "index 0000000..e69de29"),
        ("deleted file mode 100644", "index e69de29..0000000"),
    ],
    ids=("empty-file-addition", "empty-file-deletion"),
)
def test_resolves_ambiguous_empty_file_header_from_file_metadata(file_metadata: str, index: str) -> None:
    """File creation and deletion metadata resolve ambiguous empty-file headers."""
    exact_diff = (
        "diff --git a/dir b/name.py b/dir b/name.py\n"
        f"{file_metadata}\n"
        f"{index}\n"
        "diff --git a/name.py b/name.py\n"
        f"{file_metadata}\n"
        f"{index}\n"
    )

    _assert_collected_paths(exact_diff, ["dir b/name.py", "name.py"])
