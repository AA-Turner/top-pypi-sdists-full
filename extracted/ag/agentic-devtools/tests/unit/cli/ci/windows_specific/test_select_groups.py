"""Exact product routing remains independent from Linux contract routing."""

import pytest

from agentic_devtools.cli.ci.windows_specific import select_groups

PRODUCT_PATHS = {
    "setup-check": [
        "agentic_devtools/cli/setup/dependency_checker.py",
        "tests/unit/cli/setup/dependency_checker/test__check_editable_install.py",
    ],
    "portability": [
        "agentic_devtools/adapters/pull_request_create.py",
        "tests/unit/adapters/pull_request_create/test_githubpullrequestcreateadapter.py",
        "agentic_devtools/agdt_gitignore.py",
        "tests/unit/agdt_gitignore/test_ensure_agdt_gitignore.py",
        "agentic_devtools/ai_providers/availability.py",
        "tests/unit/ai_providers/availability/test__write_files_atomically.py",
        "tests/unit/ai_providers/availability/test_curate_availability_matrix.py",
        "tests/unit/ai_providers/availability/test_render_adoption_note.py",
        "agentic_devtools/ai_providers/copilot_discovery.py",
        "tests/unit/ai_providers/copilot_discovery/test_resolve_acp_command.py",
        "agentic_devtools/cli/audit/instruction_resolver.py",
        "tests/unit/cli/audit/instruction_resolver/test_resolve_instruction_files.py",
        "agentic_devtools/cli/audit/output_format.py",
        "tests/unit/cli/audit/output_format/test_write_batch_output.py",
        "agentic_devtools/cli/ci/windows_process_cleanup.py",
        "tests/unit/cli/ci/windows_process_cleanup/__init__.py",
        "tests/unit/cli/ci/windows_process_cleanup/test__attempt_cleanup.py",
        "tests/unit/cli/ci/windows_process_cleanup/test__attempt_process_cleanup.py",
        "tests/unit/cli/ci/windows_process_cleanup/test__close_stream_bounded.py",
        "tests/unit/cli/ci/windows_process_cleanup/test__close_process_resources.py",
        "tests/unit/cli/ci/windows_process_cleanup/test__drain_and_reap_process.py",
        "tests/unit/cli/ci/windows_process_cleanup/test_processcleanupdiagnostic.py",
        "tests/unit/cli/ci/windows_process_cleanup/test_processcleanuperror.py",
        "tests/unit/cli/ci/windows_process_tree/test__run_windows_process.py",
        "tests/unit/cli/ci/windows_process_tree/test__cleanup_process.py",
        "agentic_devtools/cli/checks/changed_files.py",
        "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py",
        "tests/unit/cli/checks/commands/test__collect_extra_test_targets.py",
    ],
    "benchmark": [
        ".gitattributes",
        "tests/workflows/test_phase0_review_benchmark.py",
        "tests/fixtures/reviewing-agent-benchmark/file.json",
        "tests/fixtures/reviewing-agent-benchmark/nested/file.json",
        "agentic_devtools/cli/phase0_review/commands.py",
        "agentic_devtools/cli/phase0_review/nested/file.py",
    ],
}
CONTRACT_PATHS = [
    ".github/windows-specific-tests.json",
    ".github/workflows/pr-windows-specific-tests.yml",
    ".github/workflows/pr-smart-module-tests.yml",
    "tests/workflows/test_windows_specific_ci.py",
    "tests/workflows/test_windows_specific_fixture_bytes.py",
    "agentic_devtools/cli/ci/windows_fixture_bytes.py",
    "agentic_devtools/cli/ci/windows_specific_cli.py",
    "tests/unit/cli/ci/windows_specific/test_load_policy.py",
    "tests/unit/cli/ci/windows_specific/nested/file.py",
    "tests/unit/cli/ci/windows_specific_cli/test__run_cli.py",
    "tests/unit/cli/ci/windows_fixture_bytes/test_verify.py",
    "tests/unit/cli/ci/windows_fixture_bytes/nested/file.py",
]
SUCCESSOR_PATHS = [
    ("agentic_devtools/cli/ci/windows_process_tree.py", False),
    ("agentic_devtools/cli/ci/windows_specific.py", True),
    ("agentic_devtools/cli/ci/windows_specific_path_groups.py", False),
    ("tests/unit/cli/ci/windows_process_cleanup/test__attempt_cleanup.py", False),
    ("tests/unit/cli/ci/windows_process_cleanup/test__attempt_process_cleanup.py", False),
    ("tests/unit/cli/ci/windows_process_cleanup/test__drain_and_reap_process.py", False),
    ("tests/unit/cli/ci/windows_process_cleanup/test_processcleanupdiagnostic.py", False),
    ("tests/unit/cli/ci/windows_process_cleanup/test_processcleanuperror.py", False),
    ("tests/unit/cli/ci/windows_process_tree/__init__.py", False),
    ("tests/unit/cli/ci/windows_process_tree/test_run_bounded_process.py", False),
    ("tests/unit/cli/ci/windows_process_tree/test__run_windows_process.py", False),
    ("tests/unit/cli/ci/windows_specific/test_run_selected_tests.py", True),
    ("agentic_devtools/cli/checks/changed_files.py", False),
    ("tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py", False),
    ("tests/unit/cli/checks/commands/test__collect_extra_test_targets.py", False),
]


@pytest.mark.parametrize("group,path", [(group, path) for group, paths in PRODUCT_PATHS.items() for path in paths])
def test_each_product_path(group, path):
    assert select_groups([path]) == (frozenset({group}), False)


@pytest.mark.parametrize("path", CONTRACT_PATHS)
def test_contract_only_paths(path):
    assert select_groups([path]) == (frozenset(), True)


@pytest.mark.parametrize(("path", "contract_required"), SUCCESSOR_PATHS)
def test_successor_paths_select_portability(path, contract_required):
    assert select_groups([path]) == (frozenset({"portability"}), contract_required)


@pytest.mark.parametrize("path", ["pyproject.toml", "tests/conftest.py"])
def test_shared_inputs(path):
    assert select_groups([path]) == (frozenset(PRODUCT_PATHS), True)


@pytest.mark.parametrize(
    "path",
    [
        "README.md",
        "docs/windows-ci.md",
        ".github/workflows/README.md",
        "agentic_devtools/unrelated.py",
        "tests/unit/cli/setup/dependency_checker/test_other.py",
        "tests/fixtures/reviewing-agent-benchmark-other/file",
        "agentic_devtools/cli/phase0_review_other/file.py",
        "tests/unit/cli/ci/windows_specific_other/test_file.py",
        "tests/unit/cli/ci/windows_fixture_bytes_other/test_file.py",
        "agentic_devtools/cli/ci/windows_specific_path_groups_old.py",
        "agentic_devtools/cli/ci/windows_process_tree_helpers.py",
        "agentic_devtools/cli/checks/changed_files_extra.py",
        "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py.extra",
        "tests/unit/cli/checks/commands/test__collect_extra_test_targets.py_extra",
        "tests/unit/cli/checks/changed_files/test_unrelated.py",
        "tests/unit/cli/ci/windows_process_tree/README.md",
        "tests/unit/cli/ci/windows_process_tree/test_unrelated.py",
        "tests/fixtures/reviewing-agent-benchmark",
        "agentic_devtools/cli/phase0_review",
        "tests/unit/cli/ci/windows_specific",
        "tests/unit/cli/ci/windows_fixture_bytes",
        "nested/pyproject.toml",
    ],
)
def test_unrelated_and_prefix_lookalikes(path):
    assert select_groups([path]) == (frozenset(), False)


def test_combined_and_repeated_paths():
    products = [paths[0] for paths in PRODUCT_PATHS.values()]
    assert select_groups(products + products) == (frozenset(PRODUCT_PATHS), False)
    assert select_groups(products + CONTRACT_PATHS) == (frozenset(PRODUCT_PATHS), True)
    assert select_groups(products[:2]) == (frozenset({"setup-check", "portability"}), False)


def test_combined_and_repeated_consumer_paths():
    paths = [
        "agentic_devtools/cli/checks/changed_files.py",
        "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py",
        "tests/unit/cli/checks/commands/test__collect_extra_test_targets.py",
    ]
    assert select_groups(paths + paths) == (frozenset({"portability"}), False)
    assert select_groups(paths + CONTRACT_PATHS) == (frozenset({"portability"}), True)


def test_combined_successor_paths_select_portability_and_contract():
    paths = [path for path, _ in SUCCESSOR_PATHS]
    assert select_groups(paths) == (frozenset({"portability"}), True)


def test_empty_paths():
    assert select_groups([]) == (frozenset(), False)
    assert select_groups(()) == (frozenset(), False)


@pytest.mark.parametrize(
    "paths",
    [
        "pyproject.toml",
        b"pyproject.toml",
        None,
        123,
        {"pyproject.toml"},
        {"pyproject.toml": True},
        [None],
        [123],
        [b"pyproject.toml"],
        [""],
        ["/absolute"],
        ["//server/share"],
        ["C:/file"],
        ["C:file"],
        ["c:"],
        ["a\\file"],
        ["."],
        [".."],
        ["./file"],
        ["a/../file"],
        ["a/./file"],
        ["a//file"],
        ["a/"],
        ["a/\x00/file"],
    ],
)
def test_invalid_paths(paths):
    with pytest.raises(ValueError):
        select_groups(paths)


def test_invalid_path_after_applicable_path_is_not_ignored():
    with pytest.raises(ValueError):
        select_groups(["pyproject.toml", "../invalid"])
