# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for registry store comparison helpers."""

from __future__ import annotations

import pytest

from airbyte_ops_mcp.registry.compare import (
    DEFAULT_TOLERATED_PATHS,
    _apply_tolerations,
    _extract_connector_version,
    _get_value_type_name,
    _is_ga_version,
    _parse_version,
    _resolve_best_version,
)

# ---------------------------------------------------------------------------
# _is_ga_version
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "version_str,expected",
    [
        pytest.param("1.0.0", True, id="stable_release"),
        pytest.param("2.3.4", True, id="multi_digit"),
        pytest.param("0.1.0", True, id="zero_major"),
        pytest.param("1.0.0a1", False, id="alpha"),
        pytest.param("1.0.0b2", False, id="beta"),
        pytest.param("1.0.0rc1", False, id="release_candidate"),
        pytest.param("1.0.0.dev1", False, id="dev_release"),
        pytest.param("not-a-version", False, id="invalid_string"),
        pytest.param("latest", False, id="latest_pseudo"),
    ],
)
def test_is_ga_version(version_str: str, expected: bool) -> None:
    assert _is_ga_version(version_str) == expected


# ---------------------------------------------------------------------------
# _parse_version
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "version_str,is_valid",
    [
        pytest.param("1.0.0", True, id="simple"),
        pytest.param("2.3.4rc1", True, id="prerelease"),
        pytest.param("garbage", False, id="invalid"),
        pytest.param("latest", False, id="latest"),
    ],
)
def test_parse_version(version_str: str, is_valid: bool) -> None:
    result = _parse_version(version_str)
    if is_valid:
        assert result is not None
    else:
        assert result is None


# ---------------------------------------------------------------------------
# _extract_connector_version
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "path,bucket,prefix,expected",
    [
        pytest.param(
            "my-bucket/metadata/airbyte/source-faker/7.0.0/metadata.yaml",
            "my-bucket",
            "",
            ("source-faker", "7.0.0"),
            id="no_prefix",
        ),
        pytest.param(
            "my-bucket/dev/test/metadata/airbyte/source-faker/7.0.0/metadata.yaml",
            "my-bucket",
            "dev/test/",
            ("source-faker", "7.0.0"),
            id="with_prefix",
        ),
        pytest.param(
            "my-bucket/metadata/airbyte/source-faker/latest/metadata.yaml",
            "my-bucket",
            "",
            None,
            id="latest_excluded",
        ),
        pytest.param(
            "my-bucket/metadata/airbyte/source-faker/release_candidate/metadata.yaml",
            "my-bucket",
            "",
            None,
            id="rc_excluded",
        ),
        pytest.param(
            "wrong-bucket/metadata/airbyte/source-faker/1.0.0/metadata.yaml",
            "my-bucket",
            "",
            None,
            id="wrong_bucket",
        ),
    ],
)
def test_extract_connector_version(
    path: str,
    bucket: str,
    prefix: str,
    expected: tuple[str, str] | None,
) -> None:
    assert _extract_connector_version(path, bucket, prefix) == expected


# ---------------------------------------------------------------------------
# _resolve_best_version
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "versions,expected",
    [
        pytest.param(["latest"], "latest", id="only_latest"),
        pytest.param(["1.0.0", "2.0.0", "3.0.0"], "3.0.0", id="highest_ga"),
        pytest.param(["1.0.0", "2.0.0rc1"], "1.0.0", id="ga_over_prerelease"),
        pytest.param(["1.0.0rc1", "2.0.0rc1"], "2.0.0rc1", id="highest_prerelease"),
        pytest.param(
            ["1.0.0", "2.0.0", "3.0.0rc1", "latest"],
            "2.0.0",
            id="ga_highest_ignoring_rc_and_latest",
        ),
        pytest.param(["garbage", "also-garbage"], "latest", id="all_unparseable"),
    ],
)
def test_resolve_best_version(versions: list[str], expected: str) -> None:
    assert _resolve_best_version(versions) == expected


# ---------------------------------------------------------------------------
# _get_value_type_name
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param(None, "null", id="none"),
        pytest.param(True, "bool", id="bool"),
        pytest.param(42, "int", id="int"),
        pytest.param(3.14, "float", id="float"),
        pytest.param("hello", "str", id="str"),
        pytest.param([1, 2], "list", id="list"),
        pytest.param({"a": 1}, "dict", id="dict"),
    ],
)
def test_get_value_type_name(value: object, expected: str) -> None:
    assert _get_value_type_name(value) == expected


# ---------------------------------------------------------------------------
# _apply_tolerations
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "store,ref,paths,exp_tolerated,exp_violations,store_key_removed",
    [
        pytest.param(
            {"generated": {"ts": "2026-01-01"}, "name": "foo"},
            {"generated": {"ts": "2026-02-02"}, "name": "foo"},
            ["generated/ts"],
            ["generated/ts"],
            [],
            True,
            id="value_differs_tolerated",
        ),
        pytest.param(
            {"generated": {"ts": "2026-01-01"}, "name": "foo"},
            {"generated": {"ts": "2026-01-01"}, "name": "foo"},
            ["generated/ts"],
            [],
            [],
            False,
            id="values_same_not_tolerated",
        ),
        pytest.param(
            {"generated": {"ts": "2026-01-01"}},
            {"generated": {}},
            ["generated/ts"],
            [],
            ["tolerated path 'generated/ts' present in store but missing in reference"],
            False,
            id="presence_mismatch",
        ),
        pytest.param(
            {"generated": {"ts": "2026-01-01"}},
            {"generated": {"ts": 12345}},
            ["generated/ts"],
            [],
            [
                "tolerated path 'generated/ts' has type mismatch at 'generated/ts': store=str, reference=int"
            ],
            False,
            id="type_mismatch",
        ),
        pytest.param(
            {"a": 1},
            {"a": 1},
            ["nonexistent/path"],
            [],
            [],
            False,
            id="path_missing_both_sides",
        ),
    ],
)
def test_apply_tolerations(
    store: dict,
    ref: dict,
    paths: list[str],
    exp_tolerated: list[str],
    exp_violations: list[str],
    store_key_removed: bool,
) -> None:
    store_copy, ref_copy, tolerated, violations = _apply_tolerations(store, ref, paths)
    assert tolerated == exp_tolerated
    assert violations == exp_violations
    # Verify originals are not mutated
    if "generated" in store and "ts" in store.get("generated", {}):
        assert "ts" in store["generated"]
    # Verify copies had the path removed when tolerated
    if store_key_removed and "generated" in store_copy:
        assert "ts" not in store_copy.get("generated", {})
    if store_key_removed and "generated" in ref_copy:
        assert "ts" not in ref_copy.get("generated", {})


# ---------------------------------------------------------------------------
# DEFAULT_TOLERATED_PATHS
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_default_tolerated_paths_non_empty() -> None:
    """Ensure the module exposes a non-empty set of default tolerated paths."""
    assert len(DEFAULT_TOLERATED_PATHS) > 0
    for p in DEFAULT_TOLERATED_PATHS:
        assert isinstance(p, str)
        assert "/" in p, f"Expected dpath expression with '/': {p}"
