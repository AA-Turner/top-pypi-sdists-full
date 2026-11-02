"""Tests for CLI Windows-selection flags on exact successor routes."""

import json
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.windows_specific import select_groups
from agentic_devtools.cli.ci.windows_specific_cli import _Dispatcher

SUCCESSOR_PATHS = [
    pytest.param(["agentic_devtools/cli/ci/windows_process_tree.py"], False, id="process-tree-module"),
    pytest.param(["agentic_devtools/cli/ci/windows_specific.py"], True, id="selector-module"),
    pytest.param(["agentic_devtools/cli/ci/windows_specific_path_groups.py"], False, id="route-table-module"),
    pytest.param(["tests/unit/cli/ci/windows_process_tree/__init__.py"], False, id="process-tree-package"),
    pytest.param(["tests/unit/cli/ci/windows_process_tree/test_run_bounded_process.py"], False, id="process-tree-test"),
    pytest.param(["agentic_devtools/cli/checks/changed_files.py"], False, id="changed-files-module"),
    pytest.param(
        ["tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py"],
        False,
        id="consumer-path-test",
    ),
    pytest.param(
        ["tests/unit/cli/checks/commands/test__collect_extra_test_targets.py"],
        False,
        id="consumer-target-test",
    ),
    pytest.param(
        ["tests/unit/cli/ci/windows_process_tree/test__run_windows_process.py"],
        False,
        id="process-tree-run-test",
    ),
    pytest.param(["agentic_devtools/cli/ci/windows_process_cleanup.py"], False, id="process-cleanup-module"),
    pytest.param(
        ["tests/unit/cli/ci/windows_process_cleanup/test__attempt_cleanup.py"],
        False,
        id="process-cleanup-attempt-test",
    ),
    pytest.param(
        ["tests/unit/cli/ci/windows_process_cleanup/test__attempt_process_cleanup.py"],
        False,
        id="process-cleanup-process-attempt-test",
    ),
    pytest.param(
        ["tests/unit/cli/ci/windows_process_cleanup/test__drain_and_reap_process.py"],
        False,
        id="process-cleanup-drain-reap-test",
    ),
    pytest.param(
        ["tests/unit/cli/ci/windows_process_cleanup/test_processcleanupdiagnostic.py"],
        False,
        id="process-cleanup-diagnostic-test",
    ),
    pytest.param(
        ["tests/unit/cli/ci/windows_process_cleanup/test_processcleanuperror.py"],
        False,
        id="process-cleanup-error-test",
    ),
    pytest.param(
        ["tests/unit/cli/ci/windows_process_cleanup/test__close_stream_bounded.py"],
        False,
        id="process-cleanup-stream-test",
    ),
    pytest.param(
        ["tests/unit/cli/ci/windows_process_cleanup/test__close_process_resources.py"],
        False,
        id="process-cleanup-resources-test",
    ),
    pytest.param(
        ["tests/unit/cli/ci/windows_process_tree/test__cleanup_process.py"],
        False,
        id="process-tree-cleanup-test",
    ),
    pytest.param(["tests/unit/cli/ci/windows_specific/test_run_selected_tests.py"], True, id="caller-test"),
    pytest.param(
        [
            "agentic_devtools/cli/ci/windows_process_tree.py",
            "agentic_devtools/cli/ci/windows_specific.py",
            "agentic_devtools/cli/ci/windows_specific_path_groups.py",
            "agentic_devtools/cli/ci/windows_process_cleanup.py",
            "tests/unit/cli/ci/windows_process_tree/__init__.py",
            "tests/unit/cli/ci/windows_process_tree/test_run_bounded_process.py",
            "tests/unit/cli/ci/windows_process_tree/test__run_windows_process.py",
            "tests/unit/cli/ci/windows_process_tree/test__cleanup_process.py",
            "tests/unit/cli/ci/windows_process_cleanup/__init__.py",
            "tests/unit/cli/ci/windows_process_cleanup/test__attempt_cleanup.py",
            "tests/unit/cli/ci/windows_process_cleanup/test__attempt_process_cleanup.py",
            "tests/unit/cli/ci/windows_process_cleanup/test__close_stream_bounded.py",
            "tests/unit/cli/ci/windows_process_cleanup/test__close_process_resources.py",
            "tests/unit/cli/ci/windows_process_cleanup/test__drain_and_reap_process.py",
            "tests/unit/cli/ci/windows_process_cleanup/test_processcleanupdiagnostic.py",
            "tests/unit/cli/ci/windows_process_cleanup/test_processcleanuperror.py",
            "tests/unit/cli/ci/windows_specific/test_run_selected_tests.py",
            "agentic_devtools/cli/checks/changed_files.py",
            "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py",
            "tests/unit/cli/checks/commands/test__collect_extra_test_targets.py",
        ],
        True,
        id="all-successor-paths",
    ),
]


@pytest.mark.parametrize(("paths", "contract_required"), SUCCESSOR_PATHS)
def test_select_reports_windows_required_for_successor_paths(monkeypatch, capsys, paths, contract_required):
    monkeypatch.setenv("WINDOWS_CI_BASE_POLICY", "trusted-policy.py")
    dispatcher = _Dispatcher(Mock(return_value=object()), select_groups, Mock(), Mock())
    status = dispatcher.run(
        [
            "select",
            "--changed-paths-json",
            json.dumps(paths),
            "--manifest",
            "manifest.json",
            "--head-policy",
            "head.py",
        ]
    )

    captured = capsys.readouterr()
    assert status == 0
    assert captured.err == ""
    lines = captured.out.splitlines()
    assert len(lines) == 1
    selection = json.loads(lines[0])
    assert set(selection) == {
        "ok",
        "product_groups",
        "contract_required",
        "windows_required",
        "bootstrap_allowed",
    }
    assert type(selection["ok"]) is bool
    assert type(selection["product_groups"]) is list
    assert type(selection["contract_required"]) is bool
    assert type(selection["windows_required"]) is bool
    assert type(selection["bootstrap_allowed"]) is bool
    assert selection == {
        "ok": True,
        "product_groups": ["portability"],
        "contract_required": contract_required,
        "windows_required": True,
        "bootstrap_allowed": False,
    }
