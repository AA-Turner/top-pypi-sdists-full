"""Finite trusted registry and validator for Windows selector-policy versions."""

from __future__ import annotations

import ast
import json
from typing import NamedTuple

from agentic_devtools.cli.ci.windows_specific_cli import _check_bindings, _unique_object


class SelectorPolicy(NamedTuple):
    selectors: tuple[str, ...]
    expansions: tuple[tuple[str, tuple[str, ...]], ...]


V2_EXTENSION_SELECTORS = (
    "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py"
    "::TestFindConsumerTestPaths::test_windows_conftest_path_returns_posix_directory",
    "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py"
    "::TestFindConsumerTestPaths::test_helper_consumers_are_sorted_posix_paths",
    "tests/unit/cli/checks/commands/test__collect_extra_test_targets.py"
    "::TestCollectExtraTestTargets::test_support_consumer_not_duplicated[tests/unit/other/test_bar.py]",
    "tests/unit/cli/checks/commands/test__collect_extra_test_targets.py"
    "::TestCollectExtraTestTargets::test_support_consumer_not_duplicated[tests/unit/other]",
)
V2_EXTENSION_EXPANSIONS = (
    (
        V2_EXTENSION_SELECTORS[1],
        ("consumer_names0", "consumer_names1"),
    ),
)
_EXPECTATION_NAMES = {"EXPECTED_SELECTORS", "EXPECTED_EXPANSIONS", "SELECTOR_POLICY_VERSION"}


def _v1_policy(selectors: tuple[str, ...], expansions: dict[str, tuple[str, ...]]) -> SelectorPolicy:
    return SelectorPolicy(selectors, tuple(expansions.items()))


def _v2_policy(v1: SelectorPolicy) -> SelectorPolicy:
    selectors = (*v1.selectors[:-1], *V2_EXTENSION_SELECTORS, v1.selectors[-1])
    expansions = (*v1.expansions, *V2_EXTENSION_EXPANSIONS)
    return SelectorPolicy(selectors, expansions)


def _validate_policy(
    selectors: object,
    expansions: object,
    expected_selectors: tuple[str, ...],
    expected_expansions: dict[str, tuple[str, ...]],
    *,
    json_arrays: bool = False,
) -> SelectorPolicy:
    """Validate exact frozen v1 values and return immutable, ordered policy data."""
    sequence_type = list if json_arrays else tuple
    if not isinstance(selectors, sequence_type) or tuple(selectors) != expected_selectors:
        raise ValueError("Selectors must exactly match the frozen ordered policy")
    if not isinstance(expansions, dict) or tuple(expansions) != tuple(expected_expansions):
        raise ValueError("Expansion keys must exactly match the frozen ordered policy")
    for key, ids in expansions.items():
        if not isinstance(ids, sequence_type) or tuple(ids) != expected_expansions[key]:
            raise ValueError("Expansion IDs must exactly match the frozen ordered policy")
    return SelectorPolicy(tuple(selectors), tuple((key, tuple(ids)) for key, ids in expansions.items()))


def _source_values(source: str) -> tuple[object, object, bool, object | None]:
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError("Invalid policy source syntax") from exc
    assignments: dict[str, ast.Assign] = {}
    for statement in tree.body:
        if isinstance(statement, ast.Assign) and len(statement.targets) == 1:
            target = statement.targets[0]
            if isinstance(target, ast.Name) and target.id in _EXPECTATION_NAMES:
                if target.id in assignments:
                    raise ValueError("Duplicate policy assignment")
                assignments[target.id] = statement
    required = _EXPECTATION_NAMES - {"SELECTOR_POLICY_VERSION"}
    if not required.issubset(assignments):
        raise ValueError("Missing simple top-level expectation assignments")
    _check_bindings(tree, {id(statement.targets[0]) for statement in assignments.values()}, _EXPECTATION_NAMES)
    values: dict[str, object] = {}
    for name, statement in assignments.items():
        try:
            value = ast.literal_eval(statement.value)
        except (ValueError, TypeError, SyntaxError) as exc:
            raise ValueError("Policy values must be safe literals") from exc
        if (
            isinstance(statement.value, ast.Dict)
            and isinstance(value, dict)
            and len(statement.value.keys) != len(value)
        ):
            raise ValueError("Duplicate expansion literal keys")
        values[name] = value
    return (
        values["EXPECTED_SELECTORS"],
        values["EXPECTED_EXPANSIONS"],
        "SELECTOR_POLICY_VERSION" in assignments,
        values.get("SELECTOR_POLICY_VERSION"),
    )


def _parse_source(
    source: str, expected_selectors: tuple[str, ...], expected_expansions: dict[str, tuple[str, ...]]
) -> SelectorPolicy:
    """Parse the legacy unmarked source and reject explicit version markers."""
    selectors, expansions, has_version, _version = _source_values(source)
    if has_version:
        raise ValueError("Version 1 policy source must not declare SELECTOR_POLICY_VERSION")
    return _validate_policy(selectors, expansions, expected_selectors, expected_expansions)


def validate_candidate_policy(
    source: str,
    manifest_source: str,
    expected_selectors: tuple[str, ...],
    expected_expansions: dict[str, tuple[str, ...]],
) -> SelectorPolicy:
    """Validate one exact legacy policy or the single trusted v2 extension."""
    v1 = _v1_policy(expected_selectors, expected_expansions)
    selectors, expansions, has_version, source_version = _source_values(source)
    try:
        manifest = json.loads(manifest_source, object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, ValueError) as exc:
        raise ValueError("Invalid selector policy manifest") from exc
    if not isinstance(manifest, dict):
        raise ValueError("Manifest must be an object")

    if not has_version:
        expected = v1
        if manifest.keys() != {"selectors", "expansions"}:
            raise ValueError("Legacy manifest must contain exactly selectors and expansions")
    elif type(source_version) is int and source_version == 2:
        expected = _v2_policy(v1)
        if manifest.keys() != {"selectors", "expansions", "policy_version"}:
            raise ValueError("Version 2 manifest must contain exactly selectors, expansions, and policy_version")
        version = manifest["policy_version"]
        if type(version) is not int or version != 2:
            raise ValueError("Manifest policy_version must be 2")
    else:
        raise ValueError("Only the registered version 2 policy extension is supported")

    expected_expansions = dict(expected.expansions)
    _validate_policy(
        selectors,
        expansions,
        expected.selectors,
        expected_expansions,
    )
    _validate_policy(
        manifest["selectors"],
        manifest["expansions"],
        expected.selectors,
        expected_expansions,
        json_arrays=True,
    )
    return expected


def is_registered_policy(
    policy: object,
    expected_selectors: tuple[str, ...],
    expected_expansions: dict[str, tuple[str, ...]],
) -> bool:
    """Return whether a runner input is exactly one of the two trusted cohorts."""
    if not isinstance(policy, SelectorPolicy):
        return False
    v1 = _v1_policy(expected_selectors, expected_expansions)
    return policy == v1 or policy == _v2_policy(v1)
