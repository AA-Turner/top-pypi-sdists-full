"""
Path handling utilities for pytest artifact management.

This module contains logic for determining where artifacts should be stored
for individual tests, including sanitization of test names and resolution
of output directories.
"""

import re
from pathlib import Path

import pytest


def sanitize_for_artifacts(text: str) -> str:
    """
    Sanitize a test nodeid or name for use as a directory name.

    This function removes redundant prefixes and extensions (.py, test_, _test, tests/)
    and replaces characters that are not alphanumeric or hyphens with a
    single hyphen.

    Example:
        >>> sanitize_for_artifacts("tests/integration/user_creation_test.py::test_signin")
        'integration-user-creation-signin'

    Args:
        text: The text to sanitize (e.g., a test nodeid).

    Returns:
        A sanitized string safe for use as a directory name.
    """
    # Pytest nodeids often include the file extension. Strip `.py` to clean up the artifact name.
    # test_file.py::test_func => test_file::test_func
    text = re.sub(r"\.py(::|$)", r"\1", text)

    # If it's an absolute path, try to find 'tests/' and strip everything before it.
    # /Users/mike/tests/integration/file.py => tests/integration/file.py
    if text.startswith("/"):
        text = re.sub(r"^.*/tests/", "tests/", text)

    # `tests/` is a common top-level directory in python projects, adding noise to the artifact path.
    # tests/integration/file.py => integration/file.py
    text = re.sub(r"^(\./)?tests/", "", text)

    # Pytest requires tests to be prefixed with `test_`, making it redundant in artifact names.
    # integration/test_file::test_func => integration/file::func
    text = re.sub(r"(^|[/:]+)test_", r"\1", text)

    # Likewise, file names often use the `_test` suffix convention.
    # integration/user_test::func => integration/user::func
    text = re.sub(r"_test([/:]+|$)", r"\1", text)

    # Normalize remaining non-alphanumeric characters (like `::` and `/`) into hyphens for FS compatibility.
    # integration/file::func => integration-file-func
    sanitized = re.sub(r"[^A-Za-z0-9]+", "-", text)
    sanitized = re.sub(r"-+", "-", sanitized).strip("-")

    return sanitized or "unknown-test"


def get_artifact_dir(
    item: pytest.Item,
    base_dir: Path,
    *,
    create: bool = False,
    strip_base_dir: bool = True,
) -> Path:
    """
    Get or create the artifact directory for a specific test item.

    This function determines the subdirectory for the specific test item
    using its sanitized nodeid, relative to the provided base_dir.

    Args:
        item: The pytest.Item (test case) for which to get the directory.
        base_dir: The root output directory for artifacts.
        create: If True, creates the artifact directory and its parents if they do not exist.
        strip_base_dir: If True, strips any parent directories from the nodeid that are already part of the base_dir path.

    Returns:
        A pathlib.Path object pointing to the specific test's artifact directory.
    """
    if create:
        base_dir.mkdir(parents=True, exist_ok=True)

    # nodeid is the unique identifier for a pytest test, e.g. "path/to/test.py::test_func"
    nodeid = re.sub(r"^\./", "", item.nodeid)

    if strip_base_dir:
        # Extract just the file path portion of the nodeid before the "::" test separator
        node_file = nodeid.split("::")[0]
        node_dir_parts = Path(node_file).parent.parts

        # Compare against absolute path parts to ensure reliable overlap detection
        base_parts_set = set(base_dir.resolve().parts)

        # Iterate through the test's directory structure and strip any segments that exist in the base directory
        # This prevents redundant nesting when base_dir is already inside the test directory tree
        for part in node_dir_parts:
            if part == ".":
                continue

            if part in base_parts_set:
                if nodeid.startswith(part + "/"):
                    nodeid = nodeid[len(part) + 1 :]
            else:
                # Stop stripping once we hit a directory that isn't shared with the base output directory
                break

    per_test_dir = base_dir / sanitize_for_artifacts(nodeid)

    if create:
        per_test_dir.mkdir(parents=True, exist_ok=True)

    return per_test_dir
