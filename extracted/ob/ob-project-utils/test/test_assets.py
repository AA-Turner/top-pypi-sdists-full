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
    Asset,
    AssetInstance,
    EntityRef,
)
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
    print("\nAll offline tests passed.")
