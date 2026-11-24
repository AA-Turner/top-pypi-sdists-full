"""AN EDIT MISS, A FOLDER ON THE WRONG MACHINE, OR A BROWSER OPEN ELSEWHERE IS NEVER A PLATFORM ERROR (2026-11-21).

Live open ``tool_execution_failed`` rows: ``fs_edit (patch_ambiguous)`` "old_str matches 2 places …
nothing was written" (fa3b500f), ``git_ingest (local_path_on_bound_box)`` "runs on the server and
cannot see '/tmp/…' on the attached computer" (662ec5a4) and ``cloud_browser
(browser_open_on_other_machine)`` "This browser is open on another Cloud Computer. Close it there"
(a64d4454, 78461556). Each is a sentence the model or person acts on; nothing broke on our side.

SUT: the executor's real ``_is_expected_domain_failure``. Real failures stay filed.
"""

from __future__ import annotations

import pytest

from matrx_ai.tools.executor import _is_expected_domain_failure


@pytest.mark.parametrize(
    ("tool_name", "error_type"),
    [
        ("fs_edit", "patch_ambiguous"),
        ("fs_edit", "patch_no_match"),
        ("notes", "patch_ambiguous"),
        ("context_patch", "patch_no_match"),
        ("kindcomp_patch_code", "patch_no_match"),
        ("git_ingest", "local_path_on_bound_box"),
        ("cloud_browser", "browser_open_on_other_machine"),
    ],
)
def test_the_refusal_is_not_filed(tool_name: str, error_type: str) -> None:
    assert _is_expected_domain_failure(tool_name=tool_name, error_type=error_type, message="x")


@pytest.mark.parametrize(
    ("tool_name", "error_type"),
    [
        ("git_ingest", "execution"),
        ("fs_edit", "execution"),
        ("cloud_browser", "worker_unreachable"),
        # The box-path refusal is git_ingest's own; another tool's code of that name is not assumed.
        ("fs_read", "local_path_on_bound_box"),
        ("ask_person", "configuration"),
    ],
)
def test_a_real_failure_is_still_filed(tool_name: str, error_type: str) -> None:
    assert not _is_expected_domain_failure(tool_name=tool_name, error_type=error_type, message="x")
