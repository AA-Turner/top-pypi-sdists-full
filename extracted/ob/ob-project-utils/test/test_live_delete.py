"""
Live test: register + delete_data_asset / delete_model_asset against the real platform.

Verifies both halves of the SDK semantics on both register and delete:
  - register: catalog PATCH + flowproject metadata add (if not already there)
  - delete:   catalog DELETE + flowproject metadata remove
Requires metadata to exist for the target project/branch (an obproject-deploy
has run at least once).

Usage:
    source .venv/bin/activate
    python test/test_live_delete.py [--project PROJECT] [--branch BRANCH]

Requires real Metaflow config and OBP_API_SERVER / OBP_PERIMETER in scope.
Skipped from PR CI by convention (see CLAUDE.md).
"""

import argparse
import sys
import time
import uuid

from obproject.assets import Asset, _make_request


def _check_present(client, kind, name, label):
    """Assert that an asset name appears in the catalog."""
    listing_fn = client.list_data_assets if kind == "data" else client.list_model_assets
    items = listing_fn().get("items", [])
    names = [item["asset"]["id"] for item in items]
    assert name in names, f"{label}: expected {kind} asset {name!r} in catalog, got {names}"
    print(f"  [present] {kind} asset {name!r} ({label})")


def _check_absent(client, kind, name, label):
    """Assert that an asset name does NOT appear in the catalog."""
    listing_fn = client.list_data_assets if kind == "data" else client.list_model_assets
    items = listing_fn().get("items", [])
    names = [item["asset"]["id"] for item in items]
    assert name not in names, f"{label}: {kind} asset {name!r} still in catalog after delete: {names}"
    print(f"  [absent]  {kind} asset {name!r} ({label})")


def _metadata_url(client):
    return (
        f"/v1/perimeters/{client.perimeter}/projects/{client.project}"
        f"/branches/{client.branch}/latestflowproject"
    )


def _metadata_names(client, kind):
    try:
        spec = _make_request(
            client.base_url, client.service_headers, "GET", _metadata_url(client),
        )
    except Exception:
        return []
    return [a.get("id") for a in spec.get(kind, [])]


def _check_metadata_present(client, kind, name, label):
    names = _metadata_names(client, kind)
    assert name in names, (
        f"{label}: {kind}/{name!r} missing from flowproject metadata: {names}"
    )
    print(f"  [present] {kind} metadata {name!r} ({label})")


def _check_metadata_absent(client, kind, name, label):
    names = _metadata_names(client, kind)
    assert name not in names, (
        f"{label}: {kind}/{name!r} still in flowproject metadata after delete: {names}"
    )
    print(f"  [absent]  {kind} metadata {name!r} ({label})")


def run(project, branch):
    # Outside any Metaflow run, current.pathspec isn't a valid task ID, so we
    # pass an explicit user-entity ref — same pattern as register_and_list.py.
    client = Asset(
        project=project,
        branch=branch,
        entity_ref={"entity_kind": "user", "entity_id": "test_live_delete"},
    )
    print(f"Connected: {client.base_url} (perimeter={client.perimeter})")
    print(f"Target: {project}/{branch}\n")

    # Unique names so reruns don't collide and a stale leftover from a previous
    # failed run can't make the test silently pass.
    suffix = uuid.uuid4().hex[:8]
    data_name = f"delete_sdk_data_{suffix}"
    model_name = f"delete_sdk_model_{suffix}"

    # --- data asset round-trip --------------------------------------------------
    print(f"Registering data asset {data_name!r}...")
    client.register_data_asset(
        data_name,
        kind="external",
        description="ephemeral asset created by test_live_delete.py",
        blobs=["s3://no-such-bucket/test-fixture"],
        tags={"created_by": "test_live_delete"},
    )
    _check_present(client, "data", data_name, "post-register")
    _check_metadata_present(client, "data", data_name, "post-register")

    print(f"Deleting data asset {data_name!r}...")
    result = client.delete_data_asset(data_name)
    assert result.catalog_deleted, f"first delete: expected catalog_deleted=True, got {result}"
    assert result.metadata_updated, f"first delete: expected metadata_updated=True, got {result}"
    print(f"  [result]  {result}")
    _check_absent(client, "data", data_name, "post-delete")
    _check_metadata_absent(client, "data", data_name, "post-delete")

    print(f"Re-deleting data asset {data_name!r} (idempotency)...")
    result = client.delete_data_asset(data_name)
    assert not result.catalog_deleted, f"re-delete: expected catalog_deleted=False, got {result}"
    assert not result.metadata_updated, f"re-delete: expected metadata_updated=False, got {result}"
    print(f"  [result]  {result}")

    # --- model asset round-trip -------------------------------------------------
    print(f"\nRegistering model asset {model_name!r}...")
    client.register_model_asset(
        model_name,
        kind="external",
        description="ephemeral asset created by test_live_delete.py",
        blobs=["s3://no-such-bucket/test-fixture"],
        tags={"created_by": "test_live_delete"},
    )
    _check_present(client, "models", model_name, "post-register")
    _check_metadata_present(client, "models", model_name, "post-register")

    print(f"Deleting model asset {model_name!r}...")
    result = client.delete_model_asset(model_name)
    assert result.catalog_deleted, f"first delete: expected catalog_deleted=True, got {result}"
    assert result.metadata_updated, f"first delete: expected metadata_updated=True, got {result}"
    print(f"  [result]  {result}")
    _check_absent(client, "models", model_name, "post-delete")
    _check_metadata_absent(client, "models", model_name, "post-delete")

    print(f"Re-deleting model asset {model_name!r} (idempotency)...")
    result = client.delete_model_asset(model_name)
    assert not result.catalog_deleted, f"re-delete: expected catalog_deleted=False, got {result}"
    assert not result.metadata_updated, f"re-delete: expected metadata_updated=False, got {result}"
    print(f"  [result]  {result}")

    # --- read_only guard --------------------------------------------------------
    print("\nVerifying read_only client refuses delete...")
    ro = Asset(
        project=project,
        branch=branch,
        entity_ref={"entity_kind": "user", "entity_id": "test_live_delete"},
        read_only=True,
    )
    try:
        ro.delete_data_asset("anything")
    except RuntimeError as e:
        assert "read_only" in str(e), f"unexpected error message: {e}"
        print(f"  [refused] read_only data delete: {e}")
    else:
        raise AssertionError("read_only client should have refused delete_data_asset")

    try:
        ro.delete_model_asset("anything")
    except RuntimeError as e:
        assert "read_only" in str(e), f"unexpected error message: {e}"
        print(f"  [refused] read_only model delete: {e}")
    else:
        raise AssertionError("read_only client should have refused delete_model_asset")

    print("\nAll live delete checks passed.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default="ob_project_starter",
                        help="OB project to register/delete in (default: %(default)s)")
    parser.add_argument("--branch", default="main",
                        help="branch within the project (default: %(default)s)")
    args = parser.parse_args()
    try:
        run(args.project, args.branch)
    except AssertionError as e:
        print(f"\nFAIL: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
