"""Finite trusted Windows selector-policy version contract."""

import json

import pytest

from agentic_devtools.cli.ci.windows_selector_policy import (
    V2_EXTENSION_EXPANSIONS,
    V2_EXTENSION_SELECTORS,
    SelectorPolicy,
    _parse_source,
    _validate_policy,
    is_registered_policy,
    validate_candidate_policy,
)
from agentic_devtools.cli.ci.windows_specific import (
    _FROZEN_V1_EXPANSIONS as EXPECTED_EXPANSIONS,
)
from agentic_devtools.cli.ci.windows_specific import (
    _FROZEN_V1_SELECTORS as EXPECTED_SELECTORS,
)


def _v2_policy() -> SelectorPolicy:
    return SelectorPolicy(
        (*EXPECTED_SELECTORS[:-1], *V2_EXTENSION_SELECTORS, EXPECTED_SELECTORS[-1]),
        (*EXPECTED_EXPANSIONS.items(), *V2_EXTENSION_EXPANSIONS),
    )


def _source(policy: SelectorPolicy, version: int | None = None) -> str:
    marker = f"SELECTOR_POLICY_VERSION = {version!r}\n" if version is not None else ""
    return f"EXPECTED_SELECTORS = {policy.selectors!r}\nEXPECTED_EXPANSIONS = {dict(policy.expansions)!r}\n{marker}"


def _manifest(policy: SelectorPolicy, version: int | None = None) -> str:
    payload: dict[str, object] = {
        "selectors": list(policy.selectors),
        "expansions": {key: list(values) for key, values in policy.expansions},
    }
    if version is not None:
        payload["policy_version"] = version
    return json.dumps(payload)


def test_accepts_only_legacy_unmarked_v1():
    policy = validate_candidate_policy(
        _source(SelectorPolicy(EXPECTED_SELECTORS, tuple(EXPECTED_EXPANSIONS.items()))),
        _manifest(SelectorPolicy(EXPECTED_SELECTORS, tuple(EXPECTED_EXPANSIONS.items()))),
        EXPECTED_SELECTORS,
        EXPECTED_EXPANSIONS,
    )
    assert policy.selectors == EXPECTED_SELECTORS
    assert policy.expansions == tuple(EXPECTED_EXPANSIONS.items())
    assert len(policy.selectors) == 15
    assert len(policy.selectors) - len(policy.expansions) + sum(len(ids) for _, ids in policy.expansions) == 21


def test_legacy_source_and_value_helpers_return_immutable_data():
    source = _source(SelectorPolicy(EXPECTED_SELECTORS, tuple(EXPECTED_EXPANSIONS.items())))
    parsed = _parse_source(source, EXPECTED_SELECTORS, EXPECTED_EXPANSIONS)
    validated = _validate_policy(
        EXPECTED_SELECTORS,
        EXPECTED_EXPANSIONS,
        EXPECTED_SELECTORS,
        EXPECTED_EXPANSIONS,
    )
    assert parsed == validated
    with pytest.raises(ValueError):
        _parse_source(source + "SELECTOR_POLICY_VERSION = 1\n", EXPECTED_SELECTORS, EXPECTED_EXPANSIONS)
    with pytest.raises(ValueError):
        _validate_policy(None, EXPECTED_EXPANSIONS, EXPECTED_SELECTORS, EXPECTED_EXPANSIONS)
    with pytest.raises(ValueError):
        _validate_policy(EXPECTED_SELECTORS, None, EXPECTED_SELECTORS, EXPECTED_EXPANSIONS)


@pytest.mark.parametrize(
    "source",
    [
        "not valid Python !",
        "EXPECTED_SELECTORS = ()",
        "EXPECTED_SELECTORS = ()\nEXPECTED_EXPANSIONS = dict()",
        "EXPECTED_SELECTORS = ()\nEXPECTED_EXPANSIONS = {}\nEXPECTED_EXPANSIONS = {}",
    ],
)
def test_rejects_invalid_source_syntax_bindings_and_literals(source):
    with pytest.raises(ValueError):
        validate_candidate_policy(source, "{}", EXPECTED_SELECTORS, EXPECTED_EXPANSIONS)


def test_rejects_duplicate_expansion_literal_keys():
    policy = SelectorPolicy(EXPECTED_SELECTORS, tuple(EXPECTED_EXPANSIONS.items()))
    key = EXPECTED_SELECTORS[0]
    source = f"EXPECTED_SELECTORS = {policy.selectors!r}\nEXPECTED_EXPANSIONS = {{{key!r}: (), {key!r}: ()}}\n"
    with pytest.raises(ValueError, match="Duplicate"):
        validate_candidate_policy(source, _manifest(policy), EXPECTED_SELECTORS, EXPECTED_EXPANSIONS)


def test_rejects_non_object_manifest():
    policy = SelectorPolicy(EXPECTED_SELECTORS, tuple(EXPECTED_EXPANSIONS.items()))
    with pytest.raises(ValueError, match="object"):
        validate_candidate_policy(_source(policy), "null", EXPECTED_SELECTORS, EXPECTED_EXPANSIONS)


def test_accepts_exact_registered_v2_as_immutable_policy():
    candidate = _v2_policy()
    assert V2_EXTENSION_SELECTORS == (
        "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py"
        "::TestFindConsumerTestPaths::test_windows_conftest_path_returns_posix_directory",
        "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py"
        "::TestFindConsumerTestPaths::test_helper_consumers_are_sorted_posix_paths",
        "tests/unit/cli/checks/commands/test__collect_extra_test_targets.py"
        "::TestCollectExtraTestTargets::test_support_consumer_not_duplicated[tests/unit/other/test_bar.py]",
        "tests/unit/cli/checks/commands/test__collect_extra_test_targets.py"
        "::TestCollectExtraTestTargets::test_support_consumer_not_duplicated[tests/unit/other]",
    )
    policy = validate_candidate_policy(
        _source(candidate, 2),
        _manifest(candidate, 2),
        EXPECTED_SELECTORS,
        EXPECTED_EXPANSIONS,
    )
    assert policy == candidate
    assert policy.selectors[14:18] == V2_EXTENSION_SELECTORS
    assert policy.expansions[-1] == (
        V2_EXTENSION_SELECTORS[1],
        ("consumer_names0", "consumer_names1"),
    )
    assert len(policy.selectors) == 19
    assert len(policy.selectors) - len(policy.expansions) + sum(len(ids) for _, ids in policy.expansions) == 26
    assert sum(len(dict(policy.expansions)[selector]) for selector in policy.selectors[:2]) == 8
    with pytest.raises(AttributeError):
        policy.selectors = ()


def test_runner_registry_accepts_only_exact_immutable_cohorts():
    v1 = SelectorPolicy(EXPECTED_SELECTORS, tuple(EXPECTED_EXPANSIONS.items()))
    v2 = _v2_policy()
    assert is_registered_policy(v1, EXPECTED_SELECTORS, EXPECTED_EXPANSIONS)
    assert is_registered_policy(v2, EXPECTED_SELECTORS, EXPECTED_EXPANSIONS)
    assert not is_registered_policy(SelectorPolicy((), ()), EXPECTED_SELECTORS, EXPECTED_EXPANSIONS)
    assert not is_registered_policy((v1.selectors, v1.expansions), EXPECTED_SELECTORS, EXPECTED_EXPANSIONS)


@pytest.mark.parametrize("version", [0, 1, 3, True, "2"])
def test_rejects_unsupported_or_explicit_v1_source_version(version):
    candidate = SelectorPolicy(EXPECTED_SELECTORS, tuple(EXPECTED_EXPANSIONS.items()))
    with pytest.raises(ValueError):
        validate_candidate_policy(
            _source(candidate, version),
            _manifest(candidate, version),
            EXPECTED_SELECTORS,
            EXPECTED_EXPANSIONS,
        )


def test_rejects_explicit_null_v1_source_marker():
    candidate = SelectorPolicy(EXPECTED_SELECTORS, tuple(EXPECTED_EXPANSIONS.items()))
    with pytest.raises(ValueError):
        validate_candidate_policy(
            _source(candidate, None) + "SELECTOR_POLICY_VERSION = None\n",
            _manifest(candidate),
            EXPECTED_SELECTORS,
            EXPECTED_EXPANSIONS,
        )


@pytest.mark.parametrize(
    ("source", "manifest"),
    [
        (_source(_v2_policy(), 2), _manifest(SelectorPolicy(EXPECTED_SELECTORS, tuple(EXPECTED_EXPANSIONS.items())))),
        (_source(SelectorPolicy(EXPECTED_SELECTORS, tuple(EXPECTED_EXPANSIONS.items()))), _manifest(_v2_policy(), 2)),
        (_source(_v2_policy(), 2), _manifest(_v2_policy(), 3)),
        (_source(_v2_policy(), 2), _manifest(_v2_policy(), True)),
        (_source(_v2_policy(), 2), _manifest(_v2_policy())[:-1]),
        (
            _source(_v2_policy(), 2),
            _manifest(SelectorPolicy(EXPECTED_SELECTORS, tuple(EXPECTED_EXPANSIONS.items())), 2),
        ),
        (
            _source(SelectorPolicy(EXPECTED_SELECTORS, tuple(EXPECTED_EXPANSIONS.items()))),
            '{"selectors":[],"expansions":{},"policy_version":1}',
        ),
        (
            _source(SelectorPolicy(EXPECTED_SELECTORS, tuple(EXPECTED_EXPANSIONS.items()))),
            '{"selectors":[],"expansions":{},"extra":true}',
        ),
        (
            _source(SelectorPolicy(EXPECTED_SELECTORS, tuple(EXPECTED_EXPANSIONS.items()))),
            '{"selectors":[],"selectors":[],"expansions":{}}',
        ),
        (
            _source(SelectorPolicy(EXPECTED_SELECTORS, tuple(EXPECTED_EXPANSIONS.items()))),
            '{"selectors":[],"expansions":{"x":[],"x":[]}}',
        ),
    ],
)
def test_rejects_version_schema_mismatch_and_duplicate_json_keys(source, manifest):
    with pytest.raises(ValueError):
        validate_candidate_policy(source, manifest, EXPECTED_SELECTORS, EXPECTED_EXPANSIONS)


@pytest.mark.parametrize("drift", ["reordered", "duplicate", "removed", "added"])
def test_rejects_v2_selector_cohort_drift(drift):
    policy = _v2_policy()
    selectors = list(policy.selectors)
    if drift == "reordered":
        selectors[2], selectors[3] = selectors[3], selectors[2]
    elif drift == "duplicate":
        selectors[2] = selectors[1]
    elif drift == "removed":
        selectors.pop(2)
    else:
        selectors[2] = "tests/unit/other/test_unapproved.py::test_case"
    drifted = SelectorPolicy(tuple(selectors), policy.expansions)
    with pytest.raises(ValueError):
        validate_candidate_policy(
            _source(drifted, 2),
            _manifest(drifted, 2),
            EXPECTED_SELECTORS,
            EXPECTED_EXPANSIONS,
        )


@pytest.mark.parametrize("drift", ["reordered", "changed", "duplicate", "missing", "extra"])
def test_rejects_v2_expansion_drift(drift):
    policy = _v2_policy()
    expansions = list(policy.expansions)
    if drift == "reordered":
        expansions.reverse()
    elif drift == "changed":
        expansions[-1] = (V2_EXTENSION_SELECTORS[1], ("consumer_names1", "consumer_names0"))
    elif drift == "duplicate":
        expansions[-1] = (V2_EXTENSION_SELECTORS[1], ("consumer_names0", "consumer_names0"))
    elif drift == "missing":
        expansions.pop()
    else:
        expansions.append(("unapproved", ("value",)))
    drifted = SelectorPolicy(policy.selectors, tuple(expansions))
    with pytest.raises(ValueError):
        validate_candidate_policy(
            _source(drifted, 2),
            _manifest(drifted, 2),
            EXPECTED_SELECTORS,
            EXPECTED_EXPANSIONS,
        )


def test_candidate_source_is_parsed_without_execution(tmp_path):
    candidate = _v2_policy()
    marker = tmp_path / "executed"
    source = _source(candidate, 2) + f"\nother = 1\nfrom pathlib import Path\nPath({str(marker)!r}).touch()\n"
    validate_candidate_policy(source, _manifest(candidate, 2), EXPECTED_SELECTORS, EXPECTED_EXPANSIONS)
    assert not marker.exists()
