"""Frozen, issue-pinned Windows selectors and independent changed-path routing."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections.abc import Collection, Mapping, Sequence
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Literal, cast

from agentic_devtools.cli.ci import windows_specific_cli
from agentic_devtools.cli.ci.windows_process_tree import run_bounded_process
from agentic_devtools.cli.ci.windows_selector_policy import _EXPECTATION_NAMES as _EXPECTATION_NAMES
from agentic_devtools.cli.ci.windows_selector_policy import (
    SelectorPolicy,
    is_registered_policy,
    validate_candidate_policy,
)
from agentic_devtools.cli.ci.windows_selector_policy import _parse_source as _parse_legacy_source
from agentic_devtools.cli.ci.windows_selector_policy import _source_values as _source_values
from agentic_devtools.cli.ci.windows_selector_policy import _validate_policy as _validate_legacy_policy
from agentic_devtools.cli.ci.windows_specific_cli import _run_cli
from agentic_devtools.cli.ci.windows_specific_path_groups import _PRODUCT_PATHS, ProductGroup

__all__ = [
    "ProductGroup",
    "SelectorPolicy",
    "EXPECTED_SELECTORS",
    "EXPECTED_EXPANSIONS",
    "load_policy",
    "select_groups",
    "run_selected_tests",
    "audit_test_results",
    "evaluate_gate",
    "main",
]


# Frozen by #4565; changes require a separately reviewed, safely staged policy issue.
_FROZEN_V1_SELECTORS = (
    "tests/unit/cli/setup/dependency_checker/test__check_editable_install.py"
    "::TestCheckEditableInstall::test_windows_case_insensitive_comparison",
    "tests/unit/cli/setup/dependency_checker/test__check_editable_install.py"
    "::TestCheckEditableInstall::test_windows_hint_uses_power_shell_literal_quoting",
    "tests/unit/adapters/pull_request_create/test_githubpullrequestcreateadapter.py"
    "::test_github_adapter_accepts_server_urls_with_path_prefix",
    "tests/unit/adapters/pull_request_create/test_githubpullrequestcreateadapter.py"
    "::test_github_adapter_accepts_custom_server_url_without_path_prefix",
    "tests/unit/agdt_gitignore/test_ensure_agdt_gitignore.py"
    "::TestEnsureAgdtGitignore::test_does_not_write_canonical_crlf_content",
    "tests/unit/ai_providers/availability/test__write_files_atomically.py"
    "::test_write_files_atomically_preserves_existing_mode",
    "tests/unit/ai_providers/availability/test__write_files_atomically.py"
    "::test_write_files_atomically_falls_back_to_chmod_when_fchmod_unavailable",
    "tests/unit/ai_providers/availability/test__write_files_atomically.py"
    "::test_write_files_atomically_rolls_back_read_only_target_on_replace_failure",
    "tests/unit/ai_providers/availability/test__write_files_atomically.py"
    "::test_write_files_atomically_rolls_back_with_chmod_fallback_on_replace_failure",
    "tests/unit/ai_providers/availability/test_curate_availability_matrix.py"
    "::test_curate_availability_matrix_defaults_to_repo_root_paths",
    "tests/unit/ai_providers/availability/test_render_adoption_note.py"
    "::test_render_adoption_note_renders_custom_evidence_path_in_safe_code_span",
    "tests/unit/ai_providers/copilot_discovery/test_resolve_acp_command.py"
    "::test_raises_provider_error_for_malformed_command_override",
    "tests/unit/cli/audit/instruction_resolver/test_resolve_instruction_files.py"
    "::TestGithubInstructionsLoading::test_symlink_outside_repo_is_skipped",
    "tests/unit/cli/audit/output_format/test_write_batch_output.py::TestWriteBatchOutput::test_stale_observations_marked",
    "tests/workflows/test_phase0_review_benchmark.py::test_phase0_review_benchmark_verdicts",
)
_FROZEN_V1_EXPANSIONS = {
    _FROZEN_V1_SELECTORS[0]: ("linux", "win32"),
    _FROZEN_V1_SELECTORS[1]: ("R&D", "path with spaces", "O'Brien", "$cash", "`tick", "(build)"),
}

EXPECTED_SELECTORS = (
    "tests/unit/cli/setup/dependency_checker/test__check_editable_install.py"
    "::TestCheckEditableInstall::test_windows_case_insensitive_comparison",
    "tests/unit/cli/setup/dependency_checker/test__check_editable_install.py"
    "::TestCheckEditableInstall::test_windows_hint_uses_power_shell_literal_quoting",
    "tests/unit/adapters/pull_request_create/test_githubpullrequestcreateadapter.py"
    "::test_github_adapter_accepts_server_urls_with_path_prefix",
    "tests/unit/adapters/pull_request_create/test_githubpullrequestcreateadapter.py"
    "::test_github_adapter_accepts_custom_server_url_without_path_prefix",
    "tests/unit/agdt_gitignore/test_ensure_agdt_gitignore.py"
    "::TestEnsureAgdtGitignore::test_does_not_write_canonical_crlf_content",
    "tests/unit/ai_providers/availability/test__write_files_atomically.py"
    "::test_write_files_atomically_preserves_existing_mode",
    "tests/unit/ai_providers/availability/test__write_files_atomically.py"
    "::test_write_files_atomically_falls_back_to_chmod_when_fchmod_unavailable",
    "tests/unit/ai_providers/availability/test__write_files_atomically.py"
    "::test_write_files_atomically_rolls_back_read_only_target_on_replace_failure",
    "tests/unit/ai_providers/availability/test__write_files_atomically.py"
    "::test_write_files_atomically_rolls_back_with_chmod_fallback_on_replace_failure",
    "tests/unit/ai_providers/availability/test_curate_availability_matrix.py"
    "::test_curate_availability_matrix_defaults_to_repo_root_paths",
    "tests/unit/ai_providers/availability/test_render_adoption_note.py"
    "::test_render_adoption_note_renders_custom_evidence_path_in_safe_code_span",
    "tests/unit/ai_providers/copilot_discovery/test_resolve_acp_command.py"
    "::test_raises_provider_error_for_malformed_command_override",
    "tests/unit/cli/audit/instruction_resolver/test_resolve_instruction_files.py"
    "::TestGithubInstructionsLoading::test_symlink_outside_repo_is_skipped",
    "tests/unit/cli/audit/output_format/test_write_batch_output.py::TestWriteBatchOutput::test_stale_observations_marked",
    "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py"
    "::TestFindConsumerTestPaths::test_windows_conftest_path_returns_posix_directory",
    "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py"
    "::TestFindConsumerTestPaths::test_helper_consumers_are_sorted_posix_paths",
    "tests/unit/cli/checks/commands/test__collect_extra_test_targets.py"
    "::TestCollectExtraTestTargets::test_support_consumer_not_duplicated[tests/unit/other/test_bar.py]",
    "tests/unit/cli/checks/commands/test__collect_extra_test_targets.py"
    "::TestCollectExtraTestTargets::test_support_consumer_not_duplicated[tests/unit/other]",
    "tests/workflows/test_phase0_review_benchmark.py::test_phase0_review_benchmark_verdicts",
)
EXPECTED_EXPANSIONS = {
    "tests/unit/cli/setup/dependency_checker/test__check_editable_install.py"
    "::TestCheckEditableInstall::test_windows_case_insensitive_comparison": ("linux", "win32"),
    "tests/unit/cli/setup/dependency_checker/test__check_editable_install.py"
    "::TestCheckEditableInstall::test_windows_hint_uses_power_shell_literal_quoting": (
        "R&D",
        "path with spaces",
        "O'Brien",
        "$cash",
        "`tick",
        "(build)",
    ),
    "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py"
    "::TestFindConsumerTestPaths::test_helper_consumers_are_sorted_posix_paths": ("consumer_names0", "consumer_names1"),
}
SELECTOR_POLICY_VERSION = 2

_GROUPS: frozenset[ProductGroup] = frozenset({"setup-check", "portability", "benchmark"})
_BENCHMARK_PREFIXES = ("tests/fixtures/reviewing-agent-benchmark/", "agentic_devtools/cli/phase0_review/")
_SHARED_PATHS = {"pyproject.toml", "tests/conftest.py"}
_CONTRACT_PATHS = {
    ".github/windows-specific-tests.json",
    ".github/workflows/pr-windows-specific-tests.yml",
    ".github/workflows/pr-smart-module-tests.yml",
    "tests/workflows/test_windows_specific_ci.py",
    "tests/workflows/test_windows_specific_fixture_bytes.py",
    "agentic_devtools/cli/ci/windows_specific.py",
    "agentic_devtools/cli/ci/windows_specific_cli.py",
    "agentic_devtools/cli/ci/windows_fixture_bytes.py",
}
_CONTRACT_PREFIXES = (
    "tests/unit/cli/ci/windows_specific/",
    "tests/unit/cli/ci/windows_specific_cli/",
    "tests/unit/cli/ci/windows_fixture_bytes/",
)
_NODE_ID_PATTERN = re.compile(
    r"(?:(?!\.{1,2}(?:/|$))[^/\\:\s]+/)*(?!\.{1,2}(?:/|$))[^/\\:\s]+\.py"
    r"(?:::[A-Za-z_]\w*)+(?:\[[^\r\n]+\])?"
)
_COLLECTION_SUMMARY_PATTERN = re.compile(
    r"(?P<count>\d+) (?P<unit>test|tests|item|items) collected(?: in \d+(?:\.\d+)?s)?"
)

JobResult = Literal["success", "failure", "cancelled", "skipped"]
JobResultInput = JobResult | None


def _validate_policy(selectors: object, expansions: object, *, json_arrays: bool = False) -> SelectorPolicy:
    return _validate_legacy_policy(
        selectors, expansions, EXPECTED_SELECTORS, EXPECTED_EXPANSIONS, json_arrays=json_arrays
    )


def _parse_source(source: str) -> SelectorPolicy:
    """Extract legacy literal expectations without executing source statements."""
    return _parse_legacy_source(source, EXPECTED_SELECTORS, EXPECTED_EXPANSIONS)


def _parse_registered_source(source: str) -> SelectorPolicy:
    selectors, expansions, has_version, version = _source_values(source)
    manifest: dict[str, object] = {"selectors": selectors, "expansions": expansions}
    if has_version:
        manifest["policy_version"] = version
    try:
        manifest_source = json.dumps(manifest)
    except (TypeError, ValueError) as exc:
        raise ValueError("Trusted-base policy values must be JSON-compatible") from exc
    return validate_candidate_policy(source, manifest_source, _FROZEN_V1_SELECTORS, _FROZEN_V1_EXPANSIONS)


def load_policy(
    manifest_path: str | Path,
    base_policy_path: str | Path,
    head_policy_path: str | Path,
    *,
    applicable_groups: Collection[ProductGroup],
    bootstrap: bool,
) -> SelectorPolicy:
    """Return trusted-base policy after exact source/manifest/seed verification.

    Bootstrap is allowed only for an absent base and no applicable product groups.
    Source/schema/drift errors raise ValueError; file access errors propagate.
    """
    if not isinstance(bootstrap, bool):
        raise ValueError("bootstrap must be a boolean")
    if any(
        not isinstance(path, (str, Path)) or not str(path)
        for path in (manifest_path, base_policy_path, head_policy_path)
    ):
        raise ValueError("Policy paths must be nonempty strings or Path objects")
    if (
        isinstance(applicable_groups, (str, bytes))
        or not isinstance(applicable_groups, Collection)
        or any(not isinstance(group, str) or group not in _GROUPS for group in applicable_groups)
    ):
        raise ValueError("applicable_groups must contain only known product groups")
    missing_base = False
    try:
        base_stream = Path(base_policy_path).open(encoding="utf-8")
    except FileNotFoundError:
        if not bootstrap:
            raise
        if applicable_groups:
            raise ValueError("Bootstrap cannot select product groups") from None
        trusted = SelectorPolicy(_FROZEN_V1_SELECTORS, tuple(_FROZEN_V1_EXPANSIONS.items()))
        missing_base = True
    else:
        with base_stream as stream:
            source = stream.read()
        if bootstrap:
            raise ValueError("Bootstrap requires an absent trusted-base policy")
        trusted = _parse_registered_source(source)
    candidate = validate_candidate_policy(
        Path(head_policy_path).read_text(encoding="utf-8"),
        Path(manifest_path).read_text(encoding="utf-8"),
        _FROZEN_V1_SELECTORS,
        _FROZEN_V1_EXPANSIONS,
    )
    if missing_base and candidate != trusted:
        raise ValueError("Bootstrap can validate only the legacy policy")
    return candidate if not missing_base else trusted


def select_groups(changed_paths: Sequence[str]) -> tuple[frozenset[ProductGroup], bool]:
    """Classify normalized relative paths; reject invalid input with ValueError."""
    if isinstance(changed_paths, (str, bytes)) or not isinstance(changed_paths, Sequence):
        raise ValueError("changed_paths must be a sequence of repository-relative paths")
    groups: set[ProductGroup] = set()
    contract_required = False
    for path in changed_paths:
        if (
            not isinstance(path, str)
            or not path
            or "\\" in path
            or "\0" in path
            or PureWindowsPath(path).drive
            or any(part in {"", ".", ".."} for part in path.split("/"))
        ):
            raise ValueError(f"Path is not normalized and repository-relative: {path!r}")
        if path in _SHARED_PATHS:
            groups.update(_GROUPS)
        if path in _PRODUCT_PATHS:
            groups.add(_PRODUCT_PATHS[path])
        if path.startswith(_BENCHMARK_PREFIXES):
            groups.add("benchmark")
        if path in _SHARED_PATHS or path in _CONTRACT_PATHS or path.startswith(_CONTRACT_PREFIXES):
            contract_required = True
    return frozenset(groups), contract_required


def _parse_collection_output(output: str) -> tuple[str, ...]:
    if not isinstance(output, str):
        raise ValueError("Collection output must be text")
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if len(lines) < 2:
        raise ValueError("Collection output must contain node IDs and one final summary")
    match = _COLLECTION_SUMMARY_PATTERN.fullmatch(lines[-1])
    if match is None:
        raise ValueError("Collection output has no valid final summary")
    count, unit = int(match.group("count")), match.group("unit")
    invalid_summary = count != len(lines) - 1 or (count == 1) != (unit in {"test", "item"})
    if invalid_summary:
        raise ValueError("Invalid collection summary")
    node_ids = lines[:-1]
    invalid_ids = any(_NODE_ID_PATTERN.fullmatch(node_id) is None for node_id in node_ids) or len(set(node_ids)) != len(
        node_ids
    )
    if invalid_ids:
        raise ValueError("Invalid or duplicate node ID")
    return tuple(node_ids)


def audit_test_results(
    collection_output: str,
    execution_output: str,
    junit_xml: str | bytes,
    expected_ids: Collection[str],
    *,
    collection_returncode: int,
    execution_returncode: int,
) -> dict[str, bool | list[str] | int]:
    def require(condition: bool, message: str) -> None:
        if not condition:
            raise ValueError(message)

    if collection_returncode:
        raise subprocess.CalledProcessError(
            collection_returncode, ["pytest", "--collect-only"], output=collection_output
        )
    if execution_returncode:
        raise subprocess.CalledProcessError(execution_returncode, ["pytest"], output=execution_output)
    require(
        isinstance(execution_output, str) and re.search(r"\bdeselected\b", execution_output, re.IGNORECASE) is None,
        "Execution output is invalid or reports deselected tests",
    )
    require(
        not isinstance(expected_ids, (str, bytes)) and isinstance(expected_ids, Collection),
        "Expected IDs must be a collection of node IDs",
    )
    expected = tuple(expected_ids)
    require(
        bool(expected)
        and all(isinstance(item, str) and _NODE_ID_PATTERN.fullmatch(item) for item in expected)
        and len(set(expected)) == len(expected),
        "Expected IDs must be unique valid pytest node IDs",
    )
    collected = _parse_collection_output(collection_output)
    require(set(collected) == set(expected), "Collected IDs do not match expected IDs")
    require(isinstance(junit_xml, (str, bytes)), "JUnit XML must be text or bytes")
    try:
        root = ET.fromstring(junit_xml)
    except ET.ParseError as exc:
        raise ValueError("JUnit XML is malformed") from exc
    require(
        root.tag == "testsuite"
        or root.tag == "testsuites"
        and len(root) > 0
        and all(child.tag == "testsuite" for child in root),
        "JUnit XML must have a testsuite or testsuites root",
    )
    has_outcome_marker = any(element.tag in {"skipped", "failure", "error"} for element in root.iter())
    require(not has_outcome_marker, "JUnit report contains skipped or failed test outcome markers")
    suites = (root,) if root.tag == "testsuite" else tuple(root)
    split_ids = [(item, item.split("[", 1)[0].split("::")) for item in expected]
    expected_pairs = {
        (
            ".".join((*PurePosixPath(parts[0]).with_suffix("").parts, *parts[1:-1])),
            f"{parts[-1]}{item[len('::'.join(parts)) :]}",
        ): item
        for item, parts in split_ids
    }
    require(len(expected_pairs) == len(expected), "Expected IDs produce ambiguous JUnit identities")
    all_cases = sum(1 for _ in root.iter("testcase"))
    cases = [case for suite in suites for case in suite if case.tag == "testcase"]
    require(len(cases) == all_cases, "JUnit report contains a testcase outside an allowed position")
    require(bool(cases), "JUnit report contains no testcases")
    executed: list[str] = []
    seen: set[tuple[str, str]] = set()
    for case in cases:
        pair = (case.get("classname", ""), case.get("name", ""))
        require(all(pair), "JUnit testcase is missing classname or name")
        require(pair not in seen, "JUnit report contains duplicate testcase identities")
        seen.add(pair)
        node_id = expected_pairs.get(pair)
        require(node_id is not None, "JUnit report contains an unexpected testcase identity")
        executed.append(cast(str, node_id))
    require(set(executed) == set(expected), "JUnit execution IDs do not match expected IDs")
    ids = sorted(expected)
    return {"ok": True, "collected_ids": ids, "executed_ids": ids, "skipped": 0}


def run_selected_tests(
    test_root: str | Path,
    policy: SelectorPolicy,
    applicable_groups: Collection[ProductGroup],
    *,
    junit_path: str | Path,
) -> dict[str, bool | list[str] | int]:
    def require(condition: bool, message: str) -> None:
        if not condition:
            raise ValueError(message)

    require(isinstance(policy, SelectorPolicy), "policy must be a SelectorPolicy")
    require(
        is_registered_policy(policy, _FROZEN_V1_SELECTORS, _FROZEN_V1_EXPANSIONS),
        "Policy is not one of the exact trusted selector cohorts",
    )
    expansions = dict(policy.expansions)
    require(
        not isinstance(applicable_groups, (str, bytes))
        and isinstance(applicable_groups, Collection)
        and bool(applicable_groups)
        and all(isinstance(group, str) and group in _GROUPS for group in applicable_groups)
        and len(set(applicable_groups)) == len(applicable_groups),
        "applicable_groups must be a nonempty collection of unique known groups",
    )
    root = Path(test_root).resolve()
    report = (Path(junit_path) if Path(junit_path).is_absolute() else root / Path(junit_path)).absolute()
    group_order = ("setup-check",) * 2 + ("portability",) * (len(policy.selectors) - 3) + ("benchmark",)
    selectors = tuple(s for i, s in enumerate(policy.selectors) if group_order[i] in applicable_groups)
    expected = tuple(f"{s}[{p}]" if s in expansions else s for s in selectors for p in expansions.get(s, ("",)))
    env = os.environ.copy()
    if "benchmark" in applicable_groups:
        env["AGDT_RUN_PHASE0_REVIEW_BENCHMARK"] = "1"

    args = [sys.executable, "-m", "pytest", "--collect-only", "-q", "--no-cov", "--override-ini=addopts=", *selectors]
    collection = run_bounded_process(args, cwd=root, env=env, timeout=600)
    require(
        set(_parse_collection_output(collection.stdout)) == set(expected),
        "Collected IDs do not match the selected trusted policy",
    )
    require(not os.path.lexists(report), f"JUnit destination already exists: {report}")
    execution = run_bounded_process(
        [sys.executable, "-m", "pytest", "--no-cov", "--override-ini=addopts=", f"--junitxml={report}", *selectors],
        cwd=root,
        env=env,
        timeout=600,
    )
    return audit_test_results(
        collection.stdout,
        execution.stdout,
        report.read_bytes(),
        expected,
        collection_returncode=collection.returncode,
        execution_returncode=execution.returncode,
    )


def evaluate_gate(
    selection: Mapping[str, object],
    linux_result: JobResultInput,
    windows_result: JobResultInput,
) -> dict[str, bool | str]:
    fail: dict[str, bool | str] = {"ok": False, "error_code": "selection_failed"}
    if not isinstance(selection, Mapping):
        return fail
    if selection.get("ok") is False:
        code = selection.get("error_code")
        valid_error = set(selection) == {"ok", "error_code"} and isinstance(code, str) and bool(code)
        return {"ok": False, "error_code": cast(str, code)} if valid_error else fail
    groups = selection.get("product_groups")
    keys = {"ok", "product_groups", "contract_required", "windows_required", "bootstrap_allowed"}
    flags = ("contract_required", "windows_required", "bootstrap_allowed")
    if (
        set(selection) != keys
        or selection.get("ok") is not True
        or not isinstance(groups, list)
        or any(not isinstance(group, str) or group not in _GROUPS for group in groups)
        or len(set(groups)) != len(groups)
        or any(not isinstance(selection.get(key), bool) for key in flags)
        or selection["windows_required"] != bool(groups)
        or (groups and selection["bootstrap_allowed"])
    ):
        return fail
    results = (linux_result, windows_result)
    valid_results = {"success", "failure", "cancelled", "skipped"}
    if not all(result is None or isinstance(result, str) and result in valid_results for result in results):
        return fail
    if (
        any(result in {"failure", "cancelled"} for result in results)
        or selection["contract_required"]
        and linux_result != "success"
        or groups
        and windows_result != "success"
    ):
        return {"ok": False, "error_code": "required_evidence_missing"}
    return {"ok": True, "classification": "native-evidence" if groups else "not-applicable"}


def main(argv: Sequence[str] | None = None) -> int:
    """Run the focused Windows CI command dispatcher with trusted APIs."""
    policy_loader: windows_specific_cli._LoadPolicy[SelectorPolicy, ProductGroup] = load_policy
    group_selector: windows_specific_cli._SelectGroups[ProductGroup] = select_groups
    test_runner: windows_specific_cli._RunSelectedTests[SelectorPolicy, ProductGroup] = run_selected_tests
    gate_evaluator: windows_specific_cli._EvaluateGate[Literal["success", "failure", "cancelled", "skipped"]] = (
        evaluate_gate
    )
    return _run_cli(
        argv,
        load_policy=policy_loader,
        select_groups=group_selector,
        run_selected_tests=test_runner,
        evaluate_gate=gate_evaluator,
    )


if __name__ == "__main__":
    raise SystemExit(main())
