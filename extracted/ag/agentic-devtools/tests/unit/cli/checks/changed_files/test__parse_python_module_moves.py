"""Tests for pairing source moves without broadening ordinary edits."""

from subprocess import CompletedProcess
from unittest.mock import patch

import pytest

from agentic_devtools.cli.checks.changed_files import _parse_python_module_moves


@pytest.mark.parametrize(
    "status",
    [
        "",
        "M\0agentic_devtools/source.py\0",
        "A\0agentic_devtools/new.py\0",
        "R100\0old.txt\0new.txt\0",
        "M\0old.txt\0A\0new.txt\0",
        "T\0agentic_devtools/source.py\0",
    ],
)
def test_non_moves_are_empty(status, tmp_path):
    assert _parse_python_module_moves(status, ["git", "diff"], "main...HEAD", tmp_path) == []


@pytest.mark.parametrize(
    "content", [None, "unrelated = 42\n", "return None\n", "x = 1\ny = 2\nz = 3\nw = 4\nv = 5\nu = 6\nt = 7"]
)
def test_requires_readable_new_content_with_substantial_overlap(tmp_path, content):
    if content is not None:
        (tmp_path / "new.py").write_text(content, encoding="utf-8")
    with patch("agentic_devtools.cli.checks.changed_files.subprocess.run") as run:
        run.return_value = CompletedProcess([], 0, "-x = 1\n-y = 2\n-z = 3\n")
        assert _parse_python_module_moves("D\0old.py\0A\0new.py\0", ["git", "diff"], "main...HEAD", tmp_path) == []


def test_modified_and_added_modules_with_only_common_error_handling_are_not_a_move(tmp_path):
    (tmp_path / "new.py").write_text(
        "def find_process(name):\n"
        "    try:\n"
        "        return lookup_process(name)\n"
        "    except OSError:\n"
        "        return None\n",
        encoding="utf-8",
    )
    removed = (
        "@@ -1,5 +1,0 @@\n"
        "-def read_config(path):\n"
        "-    try:\n"
        "-        return path.read_text()\n"
        "-    except OSError:\n"
        "-        return None\n"
    )
    with patch("agentic_devtools.cli.checks.changed_files.subprocess.run") as run:
        run.return_value = CompletedProcess([], 0, removed)
        assert (
            _parse_python_module_moves(
                "M\0old.py\0A\0new.py\0",
                ["git", "diff"],
                "main...HEAD",
                tmp_path,
            )
            == []
        )


def test_decode_error_skips_new_module(tmp_path):
    (tmp_path / "new.py").write_bytes(b"\xff")
    with patch("agentic_devtools.cli.checks.changed_files._removed_python_lines", return_value=set()):
        assert _parse_python_module_moves("D\0old.py\0A\0new.py\0", ["git", "diff"], "main...HEAD", tmp_path) == []
