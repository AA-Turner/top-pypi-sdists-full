# Test script for ob-project-utils asset API changes.
# Uses the low-level standalone functions directly (no Metaflow runtime needed).
#
# Usage:
#   source .venv/bin/activate
#   python test_assets.py

import os
import sys
import json
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ob-project-utils"))

from obproject.assets import (
    _make_request,
    _sanitize_branch_name,
    _parse_instance,
    list_data_assets,
    list_model_assets,
    get_data_asset_summary,
    get_model_asset_summary,
    get_data_asset,
    get_model_asset,
    delete_data_asset,
    delete_model_asset,
    promote_assets,
    Asset,
    AssetInstance,
    EntityRef,
)
import obproject.assets as assets_mod
from typing import Iterator


def test_sanitize_branch():
    assert _sanitize_branch_name("main") == "main"
    assert _sanitize_branch_name("user.alice@company.com") == "user_alice_at_company_com"
    assert _sanitize_branch_name("feature/new-model") == "feature_new_model"
    assert _sanitize_branch_name("UPPER_case") == "upper_case"
    assert _sanitize_branch_name("__leading__trailing__") == "leading_trailing"
    print("PASS: test_sanitize_branch")


def test_standalone_functions_exist():
    import inspect
    for fn in (get_data_asset_summary, get_model_asset_summary):
        sig = inspect.signature(fn)
        params = list(sig.parameters.keys())
        assert "base_url" in params
        assert "asset" in params
    print("PASS: test_standalone_functions_exist")


def test_asset_class_has_new_methods():
    assert hasattr(Asset, "_iter_asset_instances")
    assert hasattr(Asset, "list_data_asset_instances")
    assert hasattr(Asset, "list_model_asset_instances")
    print("PASS: test_asset_class_has_new_methods")


def test_docstrings_no_latest_n():
    for method_name in ["consume_data_asset", "consume_model_asset"]:
        method = getattr(Asset, method_name)
        doc = method.__doc__ or ""
        assert "latest-1" not in doc, f"{method_name} still mentions latest-1"
        assert "latest-N" not in doc, f"{method_name} still mentions latest-N"
    print("PASS: test_docstrings_no_latest_n")


def test_parse_instance():
    raw = {
        "asset": {"id": "xkcd", "kind": "data"},
        "id": "098230842649_task_deployer_abc123",
        "created_at": "2026-01-23T08:35:51Z",
        "created_by": {"entity_kind": "task", "entity_id": "MyFlow/123/start/456"},
        "data_properties": {
            "data_kind": "artifact",
            "blobs": ["s3://bucket/data"],
            "annotations": {"row_count": "100"},
        },
        "tags": [{"key": "env", "value": "prod"}],
    }
    inst = _parse_instance(raw)
    assert isinstance(inst, AssetInstance)
    assert inst.id == "098230842649_task_deployer_abc123"
    assert inst.created_at == datetime(2026, 1, 23, 8, 35, 51, tzinfo=timezone.utc)
    assert isinstance(inst.created_by, EntityRef)
    assert inst.created_by.entity_kind == "task"
    assert inst.created_by.entity_id == "MyFlow/123/start/456"
    assert inst.annotations == {"row_count": "100"}
    assert inst.tags == {"env": "prod"}
    assert inst.blobs == ["s3://bucket/data"]
    assert inst.kind == "data"
    assert inst.asset_kind == "artifact"
    assert inst[0] == inst.id
    print("PASS: test_parse_instance")


def test_parse_instance_model():
    raw = {
        "asset": {"id": "vlm", "kind": "model"},
        "id": "098230842649_task_deployer_def456",
        "created_at": "2026-01-23T08:35:51Z",
        "created_by": {"entity_kind": "task", "entity_id": "deployer"},
        "model_properties": {
            "model_kind": "vlm",
            "blobs": ["HuggingFaceTB/SmolVLM-Instruct"],
        },
    }
    inst = _parse_instance(raw)
    assert inst.asset_kind == "vlm"
    assert inst.blobs == ["HuggingFaceTB/SmolVLM-Instruct"]
    assert inst.annotations == {}
    assert inst.tags == {}
    print("PASS: test_parse_instance_model")


def test_types_exported():
    from obproject import AssetInstance, EntityRef
    assert AssetInstance is not None
    assert EntityRef is not None
    print("PASS: test_types_exported")


def test_iterator_interface():
    """Verify list_*_asset_instances returns an iterator (generator), not a list."""
    import inspect
    assert inspect.isgeneratorfunction(Asset._iter_asset_instances), \
        "_iter_asset_instances should be a generator"
    print("PASS: test_iterator_interface")


def test_delete_asset_methods_exist():
    """delete_*_asset surface is wired up (module fn + class method)."""
    import inspect
    for fn in (delete_data_asset, delete_model_asset):
        params = list(inspect.signature(fn).parameters.keys())
        assert "base_url" in params
        assert "asset" in params
    assert hasattr(Asset, "delete_data_asset")
    assert hasattr(Asset, "delete_model_asset")
    print("PASS: test_delete_asset_methods_exist")


def test_metadata_sync_helpers_exist():
    """Asset._add_to_metadata and _remove_from_metadata are the flowproject sync hooks."""
    import inspect
    assert hasattr(Asset, "_remove_from_metadata")
    assert list(inspect.signature(Asset._remove_from_metadata).parameters.keys()) == ["self", "kind", "name"]
    assert hasattr(Asset, "_add_to_metadata")
    assert list(inspect.signature(Asset._add_to_metadata).parameters.keys()) == ["self", "kind", "name", "description"]
    print("PASS: test_metadata_sync_helpers_exist")


def test_promote_default_kinds_skips_missing_kind():
    """kinds defaulted + named asset: kinds it isn't registered as are skipped, not errors."""
    from unittest import mock

    fake = mock.MagicMock()
    probed = []
    promoted_kinds = []

    def fake_exists(kind, name, branch=None):
        probed.append((kind, name, branch))
        return kind == "data"

    def fake_promote(source_branch, target_branch, name, kind, instance,
                     with_aliases=False, alias=None):
        promoted_kinds.append(kind)

    fake._asset_exists.side_effect = fake_exists
    fake._promote_single.side_effect = fake_promote

    with mock.patch.object(assets_mod, "Asset", return_value=fake):
        result = promote_assets(
            "proj", source="feature-v2", target="main", asset="my_asset"
        )

    assert result["promoted"] == [{"kind": "data", "name": "my_asset", "alias": "candidate"}]
    assert result["errors"] == []
    assert promoted_kinds == ["data"]
    # Probes hit the sanitized source branch, not the target
    assert probed and all(branch == "feature_v2" for _, _, branch in probed)
    print("PASS: test_promote_default_kinds_skips_missing_kind")


def test_promote_explicit_kinds_reports_missing_kind():
    """Explicit kinds keeps strict behavior: a failing kind is an error entry."""
    from unittest import mock
    import requests

    fake = mock.MagicMock()

    def fake_promote(source_branch, target_branch, name, kind, instance,
                     with_aliases=False, alias=None):
        if kind == "models":
            raise requests.HTTPError("404 Client Error: not found")

    fake._promote_single.side_effect = fake_promote

    with mock.patch.object(assets_mod, "Asset", return_value=fake):
        result = promote_assets(
            "proj", source="main", target="main",
            asset="my_asset", kinds=["data", "models"],
        )

    assert result["promoted"] == [{"kind": "data", "name": "my_asset", "alias": "candidate"}]
    assert len(result["errors"]) == 1
    assert result["errors"][0]["kind"] == "models"
    print("PASS: test_promote_explicit_kinds_reports_missing_kind")


def test_promote_default_kinds_asset_missing_everywhere():
    """kinds defaulted + asset registered as neither kind: one clear error, not silence."""
    from unittest import mock

    fake = mock.MagicMock()
    fake._asset_exists.side_effect = lambda kind, name, branch=None: False
    promoted_kinds = []
    fake._promote_single.side_effect = (
        lambda *a, **k: promoted_kinds.append(a[3])
    )

    with mock.patch.object(assets_mod, "Asset", return_value=fake):
        result = promote_assets("proj", source="main", target="main", asset="nope")

    assert result["promoted"] == []
    assert promoted_kinds == []
    assert len(result["errors"]) == 1
    assert result["errors"][0]["name"] == "nope"
    assert result["errors"][0]["kind"] is None
    assert "not found on source branch" in result["errors"][0]["error"]
    print("PASS: test_promote_default_kinds_asset_missing_everywhere")


def test_promote_same_branch_default_does_not_copy_aliases():
    """with_aliases auto-defaults to False when promoting within one branch."""
    from unittest import mock

    fake = mock.MagicMock()
    with_aliases_seen = []
    fake._asset_exists.side_effect = lambda kind, name, branch=None: kind == "data"
    fake._promote_single.side_effect = (
        lambda *a, **k: with_aliases_seen.append(k.get("with_aliases"))
    )

    with mock.patch.object(assets_mod, "Asset", return_value=fake):
        promote_assets("proj", source="Main", target="main", asset="x")

    # "Main" and "main" sanitize to the same branch, so no alias copy
    assert with_aliases_seen == [False]
    print("PASS: test_promote_same_branch_default_does_not_copy_aliases")


def test_promote_cross_branch_default_copies_aliases():
    """with_aliases auto-defaults to True across branches."""
    from unittest import mock

    fake = mock.MagicMock()
    with_aliases_seen = []
    fake._asset_exists.side_effect = lambda kind, name, branch=None: kind == "data"
    fake._promote_single.side_effect = (
        lambda *a, **k: with_aliases_seen.append(k.get("with_aliases"))
    )

    with mock.patch.object(assets_mod, "Asset", return_value=fake):
        promote_assets("proj", source="feature-v2", target="main", asset="x")

    assert with_aliases_seen == [True]
    print("PASS: test_promote_cross_branch_default_copies_aliases")


if __name__ == "__main__":
    print("=== Offline tests (no cluster needed) ===")
    test_sanitize_branch()
    test_standalone_functions_exist()
    test_asset_class_has_new_methods()
    test_docstrings_no_latest_n()
    test_parse_instance()
    test_parse_instance_model()
    test_types_exported()
    test_iterator_interface()
    test_delete_asset_methods_exist()
    test_metadata_sync_helpers_exist()
    test_promote_default_kinds_skips_missing_kind()
    test_promote_explicit_kinds_reports_missing_kind()
    test_promote_default_kinds_asset_missing_everywhere()
    test_promote_same_branch_default_does_not_copy_aliases()
    test_promote_cross_branch_default_copies_aliases()
    print("\nAll offline tests passed.")
