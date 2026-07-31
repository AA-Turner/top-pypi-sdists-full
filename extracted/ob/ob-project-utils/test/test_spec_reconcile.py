# Unit tests for project-spec asset reconciliation. No network.
#
#   python -m pytest test/test_spec_reconcile.py -v

from deploy.deploy_obproject import (
    CATALOG_PAGE_LIMIT,
    _catalog_index,
    reconcile_asset_entries,
)


def disk_entry(asset_id, markdown="# card"):
    return {
        "id": asset_id,
        "display_name": asset_id.title(),
        "description": "from disk",
        "card_markdown": markdown,
        "icon": "cube",
    }


def spec_entry(asset_id, description="from spec"):
    return {
        "id": asset_id,
        "display_name": asset_id,
        "description": description,
        "card_markdown": "",
    }


def listing(*asset_ids, continuation=None):
    return {
        "items": [{"asset": {"id": a, "kind": "model"}} for a in asset_ids],
        "continuation": continuation,
    }


def ids_of(entries):
    return sorted(e["id"] for e in entries)


def test_runtime_registered_asset_survives_deploy():
    result = reconcile_asset_entries(
        disk_entries=[],
        remote_entries=[spec_entry("fraud_model")],
        catalog_ids={"fraud_model"},
        catalog_complete=True,
    )
    assert ids_of(result) == ["fraud_model"]


def test_disk_entry_wins_over_spec_entry():
    result = reconcile_asset_entries(
        disk_entries=[disk_entry("classifier")],
        remote_entries=[spec_entry("classifier")],
        catalog_ids={"classifier"},
        catalog_complete=True,
    )
    assert len(result) == 1
    assert result[0]["card_markdown"] == "# card"
    assert result[0]["description"] == "from disk"


def test_disk_and_runtime_assets_coexist():
    result = reconcile_asset_entries(
        disk_entries=[disk_entry("classifier")],
        remote_entries=[spec_entry("fraud_model")],
        catalog_ids={"classifier", "fraud_model"},
        catalog_complete=True,
    )
    assert ids_of(result) == ["classifier", "fraud_model"]


def test_catalog_only_asset_is_restored_to_spec():
    result = reconcile_asset_entries(
        disk_entries=[],
        remote_entries=[],
        catalog_ids={"orphaned_model"},
        catalog_complete=True,
    )
    assert ids_of(result) == ["orphaned_model"]
    assert result[0]["display_name"] == "orphaned_model"


def test_deleted_asset_is_pruned_when_catalog_is_complete():
    result = reconcile_asset_entries(
        disk_entries=[],
        remote_entries=[spec_entry("gone"), spec_entry("kept")],
        catalog_ids={"kept"},
        catalog_complete=True,
    )
    assert ids_of(result) == ["kept"]


def test_nothing_is_pruned_when_catalog_is_truncated():
    result = reconcile_asset_entries(
        disk_entries=[],
        remote_entries=[spec_entry("unseen"), spec_entry("kept")],
        catalog_ids={"kept"},
        catalog_complete=False,
    )
    assert ids_of(result) == ["kept", "unseen"]


def test_skip_assets_preserves_existing_spec():
    remote = [spec_entry("a"), spec_entry("b")]
    result = reconcile_asset_entries(
        disk_entries=[],
        remote_entries=remote,
        catalog_ids={"a", "b"},
        catalog_complete=True,
    )
    assert ids_of(result) == ["a", "b"]


def test_entries_without_ids_are_ignored():
    result = reconcile_asset_entries(
        disk_entries=[{"display_name": "no id"}],
        remote_entries=[{"display_name": "also no id"}],
        catalog_ids=set(),
        catalog_complete=True,
    )
    assert result == []


def test_catalog_index_reads_ids_and_completeness():
    ids, complete = _catalog_index(listing("a", "b"))
    assert ids == {"a", "b"}
    assert complete


def test_catalog_index_flags_continuation_as_incomplete():
    _, complete = _catalog_index(listing("a", continuation="token"))
    assert not complete


def test_catalog_index_flags_full_page_as_incomplete():
    full_page = listing(*(f"asset_{i}" for i in range(CATALOG_PAGE_LIMIT)))
    _, complete = _catalog_index(full_page)
    assert not complete


def test_catalog_index_handles_empty_response():
    ids, complete = _catalog_index({})
    assert ids == set()
    assert complete
