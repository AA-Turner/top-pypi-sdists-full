# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for registry store comparison helpers."""

from __future__ import annotations

import json
from contextlib import nullcontext
from pathlib import Path
from unittest.mock import Mock

import pytest

import airbyte_ops_mcp.cli.registry as registry_cli
import airbyte_ops_mcp.registry.compare as compare_module
from airbyte_ops_mcp.registry.store import RegistryStore

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
    assert compare_module._is_ga_version(version_str) == expected


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
    result = compare_module._parse_version(version_str)
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
    assert compare_module._extract_connector_version(path, bucket, prefix) == expected


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
    assert compare_module._resolve_best_version(versions) == expected


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
    assert compare_module._get_value_type_name(value) == expected


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
    store_copy, ref_copy, tolerated, violations = compare_module._apply_tolerations(
        store, ref, paths
    )
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
    assert len(compare_module.DEFAULT_TOLERATED_PATHS) > 0
    for p in compare_module.DEFAULT_TOLERATED_PATHS:
        assert isinstance(p, str)
        assert "/" in p, f"Expected dpath expression with '/': {p}"


@pytest.mark.unit
@pytest.mark.parametrize(
    "result,expected_substrings",
    [
        pytest.param(
            compare_module.CompareResult(
                store="candidate",
                reference_store="reference",
                connectors_only_in_store=["source-added"],
                connectors_only_in_reference=["source-dropped"],
                connectors_latest_forward=["source-forward"],
                connectors_latest_backward=["source-backward"],
            ),
            [
                "FAIL",
                "source-added",
                "source-dropped",
                "source-forward",
                "source-backward",
            ],
            id="failed_assertions",
        ),
        pytest.param(
            compare_module.CompareResult(
                store="candidate", reference_store="reference"
            ),
            ["PASS"],
            id="empty_assertions",
        ),
    ],
)
def test_assertion_summary(
    result: compare_module.CompareResult, expected_substrings: list[str]
) -> None:
    summary = result.assertion_summary()
    assert all(substring in summary for substring in expected_substrings)


@pytest.mark.unit
def test_compare_computes_all_assertion_categories(tmp_path: Path) -> None:
    """Index-only comparison identifies each connector safety category."""
    candidate = tmp_path / "candidate"
    reference = tmp_path / "reference"
    for root, versions in (
        (
            candidate,
            {
                "source-added": "1.0.0",
                "source-forward": "2.0.0",
                "source-backward": "1.0.0",
            },
        ),
        (
            reference,
            {
                "source-dropped": "1.0.0",
                "source-forward": "1.0.0",
                "source-backward": "2.0.0",
            },
        ),
    ):
        index = {
            "sources": [
                {
                    "dockerRepository": f"airbyte/{name}",
                    "dockerImageTag": version,
                }
                for name, version in versions.items()
            ],
            "destinations": [],
        }
        path = root / "registries/v0/cloud_registry.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(index))
        (root / "registries/v0/oss_registry.json").write_text(json.dumps(index))
        (root / "registries/v0/composite_registry.json").write_text(json.dumps(index))

    result = compare_module.compare_stores(
        store=RegistryStore.parse(f"coral:local:{candidate}"),
        reference=RegistryStore.parse(f"coral:local:{reference}"),
        with_artifacts=False,
    )

    assert result.connectors_only_in_store == ["source-added"]
    assert result.connectors_only_in_reference == ["source-dropped"]
    assert result.connectors_latest_forward == ["source-forward"]
    assert result.connectors_latest_backward == ["source-backward"]


@pytest.mark.unit
@pytest.mark.parametrize(
    "store_version,reference_version,expected_forward,expected_backward",
    [
        pytest.param("2.0.0", "1.0.0", ["source-test"], [], id="forward_move"),
        pytest.param("1.0.0", "2.0.0", [], ["source-test"], id="backward_move"),
    ],
)
def test_artifact_comparison_computes_latest_version_assertions(
    tmp_path: Path,
    store_version: str,
    reference_version: str,
    expected_forward: list[str],
    expected_backward: list[str],
) -> None:
    """Artifact comparison derives latest versions independently per store."""
    for root, version in (
        (tmp_path / "store", store_version),
        (tmp_path / "reference", reference_version),
    ):
        connector_root = root / f"metadata/airbyte/source-test/{version}"
        connector_root.mkdir(parents=True)
        (connector_root / "metadata.yaml").write_text("data: {}\n")
        for filename, content in (
            ("cloud.json", "{}\n"),
            ("oss.json", "{}\n"),
            ("spec.json", "{}\n"),
        ):
            (connector_root / filename).write_text(content)

    result = compare_module.compare_stores(
        RegistryStore.parse(f"coral:local:{tmp_path / 'store'}"),
        RegistryStore.parse(f"coral:local:{tmp_path / 'reference'}"),
        with_indexes=False,
    )

    assert result.connectors_latest_forward == expected_forward
    assert result.connectors_latest_backward == expected_backward


@pytest.mark.unit
@pytest.mark.parametrize(
    "path,expected_fs,unexpected_fs",
    [
        pytest.param(
            "/reference/metadata/*",
            "reference",
            "store",
            id="reference_path",
        ),
        pytest.param(
            "/candidate/metadata/*",
            "store",
            "reference",
            id="store_path",
        ),
    ],
)
def test_routed_filesystem_routes_glob_to_matching_store(
    path: str,
    expected_fs: str,
    unexpected_fs: str,
) -> None:
    """Glob operations use the filesystem owning the requested path."""
    store_fs = Mock()
    reference_fs = Mock()
    routed = compare_module._RoutedFileSystem(
        store_fs=store_fs,
        reference_fs=reference_fs,
        store_root="/candidate",
        reference_root="/reference",
    )

    routed.glob(path)

    expected = reference_fs if expected_fs == "reference" else store_fs
    unexpected = reference_fs if unexpected_fs == "reference" else store_fs
    expected.glob.assert_called_once_with(path)
    unexpected.glob.assert_not_called()


@pytest.mark.unit
@pytest.mark.parametrize(
    "store_data,reference_data,tolerated_paths,expected_status,expected_diff,expected_diff_line_count",
    [
        pytest.param(
            {
                "sources": [
                    {
                        "dockerRepository": "airbyte/source-test",
                        "dockerImageTag": "2.0.0",
                    }
                ],
                "destinations": [],
            },
            {
                "sources": [
                    {
                        "dockerRepository": "airbyte/source-test",
                        "dockerImageTag": "1.0.0",
                    }
                ],
                "destinations": [],
            },
            (),
            "content_differs",
            '+      "dockerImageTag": "2.0.0",',
            11,
            id="real_content_diff",
        ),
        pytest.param(
            {
                "sources": [
                    {
                        "dockerRepository": "airbyte/source-test",
                        "dockerImageTag": "1.0.0",
                        "generated": {"metrics": {"score": 2}},
                    }
                ],
                "destinations": [],
            },
            {
                "sources": [
                    {
                        "dockerRepository": "airbyte/source-test",
                        "dockerImageTag": "1.0.0",
                        "generated": {"metrics": {"score": 1}},
                    }
                ],
                "destinations": [],
            },
            ("generated/metrics",),
            "content_differs",
            '"score": 2',
            11,
            id="tolerated_diff_is_rendered",
        ),
        pytest.param(
            {
                "sources": [
                    {
                        "dockerRepository": "airbyte/source-b",
                        "dockerImageTag": "1.0.0",
                    },
                    {
                        "dockerRepository": "airbyte/source-a",
                        "dockerImageTag": "1.0.0",
                    },
                ],
                "destinations": [],
            },
            {
                "sources": [
                    {
                        "dockerRepository": "airbyte/source-a",
                        "dockerImageTag": "1.0.0",
                    },
                    {
                        "dockerRepository": "airbyte/source-b",
                        "dockerImageTag": "1.0.0",
                    },
                ],
                "destinations": [],
            },
            (),
            "match",
            "",
            0,
            id="entry_reordering_ignored",
        ),
    ],
)
def test_index_diff_uses_canonical_tolerated_unified_diff(
    store_data: dict[str, object],
    reference_data: dict[str, object],
    tolerated_paths: tuple[str, ...],
    expected_status: str,
    expected_diff: str,
    expected_diff_line_count: int,
) -> None:
    """Index diffs sort entries without removing tolerated values."""
    result = compare_module._compare_index_file_from_data(
        "registries/v0/cloud_registry.json",
        store_data,
        reference_data,
        tolerated_paths,
    )

    assert result.status == expected_status
    assert expected_diff in result.unified_diff
    assert result.diff_truncated is False
    assert result.diff_omitted_lines == 0
    assert result.diff_line_count == expected_diff_line_count


@pytest.mark.unit
def test_index_diff_reports_truncation(monkeypatch: pytest.MonkeyPatch) -> None:
    """Large canonical diffs include an explicit omitted-line marker."""
    store_data = {
        "sources": [
            {
                "dockerRepository": f"airbyte/source-{index}",
                "dockerImageTag": "2.0.0",
                "description": "x" * 100,
            }
            for index in range(300)
        ],
        "destinations": [],
    }
    reference_data = {
        "sources": [
            {
                "dockerRepository": f"airbyte/source-{index}",
                "dockerImageTag": "1.0.0",
                "description": "y" * 100,
            }
            for index in range(300)
        ],
        "destinations": [],
    }

    monkeypatch.setattr(compare_module, "_MAX_INDEX_DIFF_LINES", 10)
    result = compare_module._compare_index_file_from_data(
        "registries/v0/cloud_registry.json",
        store_data,
        reference_data,
    )

    assert result.diff_truncated is True
    assert result.diff_line_count > 10
    assert result.diff_omitted_lines == result.diff_line_count - 10
    assert f"{result.diff_omitted_lines} lines omitted" in result.unified_diff


@pytest.mark.unit
def test_compare_indexes_includes_composite_registry(tmp_path: Path) -> None:
    """Index-only comparisons include cloud, OSS, and composite indexes."""
    candidate = tmp_path / "candidate"
    reference = tmp_path / "reference"
    index = {
        "sources": [
            {
                "dockerRepository": "airbyte/source-test",
                "dockerImageTag": "1.0.0",
            }
        ],
        "destinations": [],
    }
    for root in (candidate, reference):
        index_root = root / "registries/v0"
        index_root.mkdir(parents=True)
        for filename in ("cloud", "oss", "composite"):
            (index_root / f"{filename}_registry.json").write_text(json.dumps(index))

    result = compare_module.compare_stores(
        RegistryStore.parse(f"coral:local:{candidate}"),
        RegistryStore.parse(f"coral:local:{reference}"),
        with_artifacts=False,
    )

    assert [diff.file for diff in result.index_diffs] == [
        "registries/v0/cloud_registry.json",
        "registries/v0/oss_registry.json",
        "registries/v0/composite_registry.json",
    ]
    assert all(diff.status == "match" for diff in result.index_diffs)


@pytest.mark.unit
def test_tolerated_index_changes_do_not_affect_assertion_categories(
    tmp_path: Path,
) -> None:
    """Assertion categories ignore configured paths while diffs remain visible."""
    candidate = tmp_path / "candidate"
    reference = tmp_path / "reference"
    candidate_index = {
        "sources": [
            {
                "dockerRepository": "airbyte/source-test",
                "dockerImageTag": "1.0.0",
                "generated": {"metrics": {"score": 2}},
            }
        ],
        "destinations": [],
    }
    reference_index = {
        "sources": [
            {
                "dockerRepository": "airbyte/source-test",
                "dockerImageTag": "1.0.0",
                "generated": {"metrics": {"score": 1}},
            }
        ],
        "destinations": [],
    }
    for root, index in ((candidate, candidate_index), (reference, reference_index)):
        index_root = root / "registries/v0"
        index_root.mkdir(parents=True)
        for filename in ("cloud", "oss", "composite"):
            (index_root / f"{filename}_registry.json").write_text(json.dumps(index))

    result = compare_module.compare_stores(
        RegistryStore.parse(f"coral:local:{candidate}"),
        RegistryStore.parse(f"coral:local:{reference}"),
        with_artifacts=False,
        tolerated_paths=("generated/metrics",),
    )

    assert result.connectors_only_in_store == []
    assert result.connectors_only_in_reference == []
    assert result.connectors_latest_forward == []
    assert result.connectors_latest_backward == []
    assert all(diff.status == "content_differs" for diff in result.index_diffs)
    assert all('"score": 2' in diff.unified_diff for diff in result.index_diffs)


@pytest.mark.unit
@pytest.mark.parametrize(
    "result,assert_stable,expected_exit",
    [
        pytest.param(
            compare_module.CompareResult(
                store="candidate",
                reference_store="reference",
                index_diffs=[
                    compare_module.IndexDiff(
                        file="registries/v0/cloud_registry.json",
                        status="content_differs",
                    )
                ],
            ),
            False,
            1,
            id="differences_without_assert_stable",
        ),
        pytest.param(
            compare_module.CompareResult(
                store="candidate",
                reference_store="reference",
                index_diffs=[
                    compare_module.IndexDiff(
                        file="registries/v0/cloud_registry.json",
                        status="content_differs",
                    )
                ],
            ),
            True,
            None,
            id="differences_with_clean_assertions",
        ),
        pytest.param(
            compare_module.CompareResult(
                store="candidate",
                reference_store="reference",
                connectors_only_in_store=["source-added"],
            ),
            True,
            1,
            id="assertion_violation",
        ),
    ],
)
def test_compare_cli_exit_semantics(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    result: compare_module.CompareResult,
    assert_stable: bool,
    expected_exit: int | None,
) -> None:
    monkeypatch.setattr(registry_cli, "compare_stores", lambda **kwargs: result)
    monkeypatch.setattr(registry_cli, "print_json", lambda value: None)
    monkeypatch.setattr(registry_cli.error_console, "print", lambda *args: None)

    context = (
        pytest.raises(SystemExit, match="1")
        if expected_exit is not None
        else nullcontext()
    )
    with context:
        registry_cli.compare_cmd(
            f"coral:local:{tmp_path / 'candidate'}",
            f"coral:local:{tmp_path / 'reference'}",
            assert_stable=assert_stable,
            with_artifacts=False,
        )


@pytest.mark.unit
@pytest.mark.parametrize(
    "store_target,reference_target",
    [
        pytest.param(
            "coral:local:{store}",
            "coral:prod",
            id="evaluated_store_local",
        ),
        pytest.param(
            "coral:prod",
            "coral:local:{reference}",
            id="reference_store_local",
        ),
        pytest.param(
            "coral:local:{store}",
            "coral:local:{reference}",
            id="both_stores_local",
        ),
    ],
)
def test_compare_cli_disables_artifacts_for_local_store(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    store_target: str,
    reference_target: str,
) -> None:
    """A local tree on either side cannot provide per-connector artifacts."""
    result = compare_module.CompareResult(
        store=str(tmp_path / "candidate"),
        reference_store=str(tmp_path / "reference"),
    )
    captured: dict[str, object] = {}

    def compare(**kwargs: object) -> compare_module.CompareResult:
        captured.update(kwargs)
        return result

    monkeypatch.setattr(registry_cli, "compare_stores", compare)
    monkeypatch.setattr(registry_cli, "print_json", lambda value: None)

    registry_cli.compare_cmd(
        store_target.format(store=tmp_path / "store"),
        reference_target.format(reference=tmp_path / "reference"),
    )

    assert captured["with_artifacts"] is False


@pytest.mark.unit
def test_reports_are_self_contained_and_put_diff_below_assertions(
    tmp_path: Path,
) -> None:
    """Text and HTML reports expose facts and per-index unified diffs."""
    result = compare_module.CompareResult(
        store="candidate",
        reference_store="reference",
        connectors_only_in_store=["source-added"],
        tolerated_paths=["generated/metrics"],
        compile_timestamp="2026-01-01T00:00:00+00:00",
        compared_at="2026-01-01T00:01:00+00:00",
        artifacts_compared=False,
        index_diffs=[
            compare_module.IndexDiff(
                file="registries/v0/cloud_registry.json",
                status="content_differs",
                unified_diff=(
                    "--- reference/registries/v0/cloud_registry.json\n"
                    "+++ evaluated/registries/v0/cloud_registry.json\n"
                    "@@ -1 +1 @@\n"
                    '-  "dockerImageTag": "1.0.0"\n'
                    '+  "dockerImageTag": "2.0.0"'
                ),
                diff_line_count=4,
            ),
            compare_module.IndexDiff(
                file="registries/v0/oss_registry.json",
                status="match",
            ),
        ],
    )
    text_path = tmp_path / "compare.txt"
    html_path = tmp_path / "compare.html"
    compare_module.write_text_report(result, str(text_path))
    compare_module.write_html_report(result, str(html_path))
    text = text_path.read_text()
    html = html_path.read_text()
    assert "connectors added: 1 (source-added)" in text
    assert "Per-connector artifacts: skipped." in text
    assert "COMPARISON SUMMARY" in text
    assert "INDEX DIFFS" in text
    assert "no differences" in text
    assert "diff is unsuppressed; assertion-ignored paths: generated/metrics" in text
    assert text.index("connectors added") < text.index("INDEX DIFFS")
    assert "PASS" not in text
    assert "FAIL" not in text
    assert "<details>" in html
    assert "<summary>Comparison summary</summary>" in html
    assert "cloud_registry.json" in html
    assert "source-added" in html
    assert "generated/metrics" in text
    assert "diff is unsuppressed; assertion-ignored paths: generated/metrics" in html
    assert "2026-01-01T00:00:00+00:00" in html
    assert "candidate" in text
    assert "PASS" not in html
    assert "FAIL" not in html
    assert "http://" not in html
    assert "https://" not in html
