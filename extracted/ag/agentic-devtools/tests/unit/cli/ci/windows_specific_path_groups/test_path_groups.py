"""Tests for the exact Windows-specific product-path table."""

from agentic_devtools.cli.ci.windows_specific_path_groups import _PRODUCT_PATHS

EXPECTED_PRODUCT_PATHS = {
    "agentic_devtools/cli/setup/dependency_checker.py": "setup-check",
    "tests/unit/cli/setup/dependency_checker/test__check_editable_install.py": "setup-check",
    "agentic_devtools/adapters/pull_request_create.py": "portability",
    "tests/unit/adapters/pull_request_create/test_githubpullrequestcreateadapter.py": "portability",
    "agentic_devtools/agdt_gitignore.py": "portability",
    "tests/unit/agdt_gitignore/test_ensure_agdt_gitignore.py": "portability",
    "agentic_devtools/ai_providers/availability.py": "portability",
    "tests/unit/ai_providers/availability/test__write_files_atomically.py": "portability",
    "tests/unit/ai_providers/availability/test_curate_availability_matrix.py": "portability",
    "tests/unit/ai_providers/availability/test_render_adoption_note.py": "portability",
    "agentic_devtools/ai_providers/copilot_discovery.py": "portability",
    "tests/unit/ai_providers/copilot_discovery/test_resolve_acp_command.py": "portability",
    "agentic_devtools/cli/audit/instruction_resolver.py": "portability",
    "tests/unit/cli/audit/instruction_resolver/test_resolve_instruction_files.py": "portability",
    "agentic_devtools/cli/audit/output_format.py": "portability",
    "tests/unit/cli/audit/output_format/test_write_batch_output.py": "portability",
    ".gitattributes": "benchmark",
    "tests/workflows/test_phase0_review_benchmark.py": "benchmark",
    "agentic_devtools/cli/ci/windows_process_tree.py": "portability",
    "agentic_devtools/cli/ci/windows_specific.py": "portability",
    "agentic_devtools/cli/ci/windows_specific_path_groups.py": "portability",
    "tests/unit/cli/ci/windows_process_tree/__init__.py": "portability",
    "tests/unit/cli/ci/windows_process_tree/test_run_bounded_process.py": "portability",
    "tests/unit/cli/ci/windows_process_tree/test__start_windows_process.py": "portability",
    "tests/unit/cli/ci/windows_process_tree/test__run_windows_process.py": "portability",
    "tests/unit/cli/ci/windows_process_tree/test__cleanup_process.py": "portability",
    "agentic_devtools/cli/ci/windows_process_cleanup.py": "portability",
    "tests/unit/cli/ci/windows_process_cleanup/__init__.py": "portability",
    "tests/unit/cli/ci/windows_process_cleanup/test__attempt_cleanup.py": "portability",
    "tests/unit/cli/ci/windows_process_cleanup/test__attempt_process_cleanup.py": "portability",
    "tests/unit/cli/ci/windows_process_cleanup/test__close_stream_bounded.py": "portability",
    "tests/unit/cli/ci/windows_process_cleanup/test__close_process_resources.py": "portability",
    "tests/unit/cli/ci/windows_process_cleanup/test__drain_and_reap_process.py": "portability",
    "tests/unit/cli/ci/windows_process_cleanup/test_processcleanupdiagnostic.py": "portability",
    "tests/unit/cli/ci/windows_process_cleanup/test_processcleanuperror.py": "portability",
    "tests/unit/cli/ci/windows_specific/test_run_selected_tests.py": "portability",
    "agentic_devtools/cli/checks/changed_files.py": "portability",
    "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py": "portability",
    "tests/unit/cli/checks/commands/test__collect_extra_test_targets.py": "portability",
}


def test_product_path_table_is_exact():
    assert _PRODUCT_PATHS == EXPECTED_PRODUCT_PATHS


def test_path_group_module_routes_itself_to_portability():
    assert _PRODUCT_PATHS["agentic_devtools/cli/ci/windows_specific_path_groups.py"] == "portability"
