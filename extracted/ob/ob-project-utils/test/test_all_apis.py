"""
Comprehensive exploratory test of the Outerbounds Assets API.

Walks through every API operation in a logical order, printing what it does
and what it gets back. Designed to be readable as documentation -- you can
hand this to someone to explain what the API can do.

Requires: configured credentials (outerbounds package installed, logged in).
Uses the 'ob_project_starter' project on the 'main' branch.

Usage:
    python test/test_all_apis.py
"""

import json
import time
from datetime import datetime
from obproject.assets import (
    Asset,
    AssetInstance,
    EntityRef,
    _make_request,
)

PROJECT = "ob_project_starter"
BRANCH = "main"
DATA_ASSET = "xkcd"
MODEL_ASSET = "explainer-vlm"


def pp(label, obj):
    """Pretty-print a JSON-like object with a label."""
    if isinstance(obj, dict):
        print(f"  {label}: {json.dumps(obj, indent=4, default=str)}")
    else:
        print(f"  {label}: {obj}")


def section(title):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")


def main():
    # ----------------------------------------------------------------
    # Setup: create an Asset client (auto-discovers credentials & URL)
    # ----------------------------------------------------------------
    a = Asset(
        project=PROJECT,
        branch=BRANCH,
        entity_ref={"entity_kind": "user", "entity_id": "api-test-script"},
    )
    print(f"Connected to {a.base_url}")
    print(f"  perimeter: {a.perimeter}")
    print(f"  project:   {a.project}")
    print(f"  branch:    {a.branch}")

    # We'll use _make_request for APIs that don't have a Python wrapper yet
    # (alias operations). This is the same HTTP helper the Asset class uses.
    def api(method, path, body=None):
        if method == "DELETE":
            url = f"{a.base_url.rstrip('/')}{path}"
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            headers.update(a.service_headers)
            resp = __import__("requests").request(method, url, headers=headers)
            resp.raise_for_status()
            return None
        return _make_request(a.base_url, a.service_headers, method, path, body)

    def asset_path(kind, name):
        return f"/v1/perimeters/{a.perimeter}/projects/{a.project}/branches/{a.branch}/{kind}/{name}"

    # ================================================================
    #  1. LIST ASSETS
    #     Discover what data and model assets exist in the project.
    # ================================================================
    section("1. List assets")

    data_assets = a.list_data_assets()
    data_items = data_assets.get("items", [])
    print(f"Data assets ({len(data_items)}):")
    for item in data_items:
        name = item["asset"]["id"]
        latest = item.get("latest_instance")
        latest_ts = latest["created_at"] if latest else "no instances"
        print(f"  - {name} (latest: {latest_ts})")

    model_assets = a.list_model_assets()
    model_items = model_assets.get("items", [])
    print(f"\nModel assets ({len(model_items)}):")
    for item in model_items:
        name = item["asset"]["id"]
        latest = item.get("latest_instance")
        latest_ts = latest["created_at"] if latest else "no instances"
        print(f"  - {name} (latest: {latest_ts})")

    # ================================================================
    #  2. REGISTER NEW INSTANCES
    #     Push a new version of an asset. The backend creates the asset
    #     if it doesn't exist, or appends a new instance if it does.
    #     Each registration is idempotent by (entity_ref + content).
    # ================================================================
    section("2. Register new instances")

    ts = int(time.time())

    print(f"Registering data asset instance for '{DATA_ASSET}'...")
    a.register_data_asset(
        DATA_ASSET,
        kind="artifact",
        blobs=[f"s3://test-bucket/xkcd-{ts}"],
        annotations={"source": "api-test", "timestamp": str(ts)},
        tags={"env": "test"},
        description=f"Test instance from test_all_apis.py at {ts}",
    )
    print("  Done.")

    print(f"Registering model asset instance for '{MODEL_ASSET}'...")
    a.register_model_asset(
        MODEL_ASSET,
        kind="vlm",
        blobs=[f"HuggingFaceTB/SmolVLM-test-{ts}"],
        annotations={"version": f"test-{ts}"},
        description=f"Test model instance at {ts}",
    )
    print("  Done.")

    # ================================================================
    #  3. LIST INSTANCES (version history)
    #     Browse all recent instances of an asset, newest first.
    #     Returns typed AssetInstance namedtuples via an iterator.
    # ================================================================
    section("3. List instances (version history)")

    print(f"Instances of data asset '{DATA_ASSET}':")
    data_instances = list(a.list_data_asset_instances(DATA_ASSET))
    for i, inst in enumerate(data_instances):
        print(f"  [{i}] id={inst.id}")
        print(f"      created_at={inst.created_at}  by={inst.created_by.entity_id}")
        print(f"      blobs={inst.blobs}  annotations={inst.annotations}")

    print(f"\nInstances of model asset '{MODEL_ASSET}':")
    model_instances = list(a.list_model_asset_instances(MODEL_ASSET))
    for i, inst in enumerate(model_instances):
        print(f"  [{i}] id={inst.id}")
        print(f"      created_at={inst.created_at}  by={inst.created_by.entity_id}")
        print(f"      blobs={inst.blobs}")

    # Verify types are correct
    if data_instances:
        inst = data_instances[0]
        assert isinstance(inst, AssetInstance), "Should be AssetInstance namedtuple"
        assert isinstance(inst.created_at, datetime), "created_at should be datetime"
        assert isinstance(inst.created_by, EntityRef), "created_by should be EntityRef"
        print("\n  Type checks passed: AssetInstance, datetime, EntityRef all correct.")

    # ================================================================
    #  4. PEEK (read without tracking consumption)
    #     Retrieves the instance data via GET. Does NOT record that
    #     this entity consumed the asset (unlike consume_*).
    # ================================================================
    section("4. Peek at instances (non-tracking read)")

    if data_instances:
        target = data_instances[0]
        print(f"Peeking at data asset '{DATA_ASSET}' instance {target.id[:40]}...")
        result = a.peek_data_asset(DATA_ASSET, instance=target.id)
        pp("created_at", result["created_at"])
        pp("created_by", result["created_by"])
        pp("blobs", result.get("data_properties", {}).get("blobs"))

    print()
    if model_instances:
        target = model_instances[0]
        print(f"Peeking at model asset '{MODEL_ASSET}' instance {target.id[:40]}...")
        result = a.peek_model_asset(MODEL_ASSET, instance=target.id)
        pp("created_at", result["created_at"])
        pp("created_by", result["created_by"])
        pp("blobs", result.get("model_properties", {}).get("blobs"))

    # peek also works with "latest"
    print(f"\nPeeking at '{DATA_ASSET}' instance='latest' (shorthand for newest)...")
    result = a.peek_data_asset(DATA_ASSET, instance="latest")
    pp("id", result["id"])
    pp("created_at", result["created_at"])

    # ================================================================
    #  5. CONSUME (read with tracking)
    #     Same as peek but records that this entity consumed the asset.
    #     This powers the lineage graph (who produced/consumed what).
    # ================================================================
    section("5. Consume an instance (tracking read)")

    print(f"Consuming latest instance of '{DATA_ASSET}'...")
    result = a.consume_data_asset(DATA_ASSET, instance="latest")
    pp("id", result["id"])
    pp("created_at", result["created_at"])
    print("  (This consumption is now recorded in the lineage graph.)")

    # ================================================================
    #  6. ALIASES
    #     Named pointers to specific instances. Think of them like
    #     "production", "staging", "approved" -- human-readable names
    #     that can be reassigned to different instances over time.
    #
    #     Aliases are managed via REST and consumed via the @alias syntax:
    #       a.peek_data_asset("xkcd", instance="@production")
    # ================================================================
    section("6. Aliases")

    if not data_instances:
        print("  Skipping alias tests -- no data instances available.")
        return

    target_instance = data_instances[0]

    # 6a. Set an alias: point "staging" at the newest instance
    print(f"Setting alias 'staging' -> {target_instance.id[:40]}...")
    result = api("PUT", f"{asset_path('data', DATA_ASSET)}/aliases/staging", {
        "instance_id": target_instance.id,
        "entity_ref": {"entity_kind": "user", "entity_id": "api-test-script"},
    })
    pp("set alias response", result)

    # 6b. Get a single alias by name
    print(f"\nGetting alias 'staging'...")
    result = api("GET", f"{asset_path('data', DATA_ASSET)}/aliases/staging")
    pp("alias", result)

    # 6c. List all aliases for an asset
    print(f"\nListing all aliases for '{DATA_ASSET}'...")
    result = api("GET", f"{asset_path('data', DATA_ASSET)}/aliases")
    for alias in result.get("aliases", []):
        print(f"  @{alias['name']} -> {alias['instance_id'][:40]}...")
        print(f"    updated_at={alias['updated_at']}  by={alias['updated_by']['entity_id']}")
        if alias.get("recent_history"):
            print(f"    history: {len(alias['recent_history'])} entries")

    # 6d. Consume via alias: use @staging as the instance reference
    print(f"\nConsuming '{DATA_ASSET}' via alias '@staging'...")
    result = a.consume_data_asset(DATA_ASSET, instance="@staging")
    pp("id", result["id"])
    pp("created_at", result["created_at"])
    print("  (Resolved @staging to the actual instance ID.)")

    # 6e. Peek via alias works too
    print(f"\nPeeking at '{DATA_ASSET}' via alias '@staging' (no consumption tracked)...")
    result = a.peek_data_asset(DATA_ASSET, instance="@staging")
    pp("id", result["id"])

    # 6f. Reassign alias to a different instance
    if len(data_instances) >= 2:
        older_instance = data_instances[1]
        print(f"\nReassigning 'staging' -> {older_instance.id[:40]}...")
        api("PUT", f"{asset_path('data', DATA_ASSET)}/aliases/staging", {
            "instance_id": older_instance.id,
            "entity_ref": {"entity_kind": "user", "entity_id": "api-test-script"},
        })
        result = api("GET", f"{asset_path('data', DATA_ASSET)}/aliases/staging")
        print(f"  Now points to: {result['alias']['instance_id'][:40]}...")
        history = result["alias"].get("recent_history", [])
        print(f"  History has {len(history)} entries (alias remembers previous assignments).")

    # 6g. Set alias on model assets too
    if model_instances:
        print(f"\nSetting alias 'canary' on model '{MODEL_ASSET}'...")
        api("PUT", f"{asset_path('models', MODEL_ASSET)}/aliases/canary", {
            "instance_id": model_instances[0].id,
            "entity_ref": {"entity_kind": "user", "entity_id": "api-test-script"},
        })
        result = api("GET", f"{asset_path('models', MODEL_ASSET)}/aliases")
        for alias in result.get("aliases", []):
            print(f"  @{alias['name']} -> {alias['instance_id'][:40]}...")

    # 6h. All-alias history: a single timeline of every alias change
    #      for an asset, across all alias names.  Supports pagination via
    #      ?continuation=... but typically the first page is enough.
    #      NEW API - may not be deployed yet on all clusters.
    def show_alias_history(kind, asset_name):
        print(f"\nFetching all-alias history for {kind} asset '{asset_name}'...")
        try:
            resp = api("GET", f"{asset_path(kind, asset_name)}/alias-history")
        except Exception as e:
            print(f"  Not available yet ({e})")
            return
        entries = resp.get("entries", [])
        continuation = resp.get("continuation")
        print(f"  {len(entries)} history entries (continuation={'yes' if continuation else 'none'})")
        for e in entries:
            iid = e["instance_id"]
            label = f"{iid[:40]}..." if iid else "(deleted)"
            print(f"    @{e['alias_name']}  ->  {label}  "
                  f"at {e['updated_at']}  by {e['updated_by']['entity_id']}")

    show_alias_history("data", DATA_ASSET)
    if model_instances:
        show_alias_history("models", MODEL_ASSET)

    # 6i. Clean up: delete the test aliases
    print(f"\nCleaning up: deleting alias 'staging' from '{DATA_ASSET}'...")
    api("DELETE", f"{asset_path('data', DATA_ASSET)}/aliases/staging")
    print("  Deleted.")

    if model_instances:
        print(f"Cleaning up: deleting alias 'canary' from '{MODEL_ASSET}'...")
        api("DELETE", f"{asset_path('models', MODEL_ASSET)}/aliases/canary")
        print("  Deleted.")

    # Verify deletion
    result = api("GET", f"{asset_path('data', DATA_ASSET)}/aliases")
    remaining = [a["name"] for a in result.get("aliases", [])]
    print(f"\n  Remaining aliases for '{DATA_ASSET}': {remaining or '(none)'}")

    # 6j. Check alias history again after deletion - deletions should
    #     appear as entries with empty instance_id.
    print("\n  Checking alias history after deletion (expect deletion entries)...")
    show_alias_history("data", DATA_ASSET)

    # ================================================================
    #  7. ASSET SUMMARY (internal, powers the UI)
    #     Returns instances + lineage (produced_by, consumed_by).
    #     This is what list_*_asset_instances calls under the hood.
    # ================================================================
    section("7. Asset summary (lineage)")

    from obproject.assets import get_data_asset_summary
    summary = get_data_asset_summary(
        a.base_url, a.service_headers,
        perimeter=a.perimeter, project=a.project,
        branch=a.branch, asset=DATA_ASSET,
    )
    print(f"Summary for '{DATA_ASSET}':")
    print(f"  recent_instances: {len(summary.get('recent_instances', []))}")
    print(f"  recently_produced_by: {len(summary.get('recently_produced_by', []))}")
    print(f"  recently_consumed_by: {len(summary.get('recently_consumed_by', []))}")

    if summary.get("recently_consumed_by"):
        consumer = summary["recently_consumed_by"][0]
        print(f"\n  Last consumer: {consumer.get('entity_ref', {}).get('entity_id')}")

    # ================================================================
    section("Done! All APIs exercised successfully.")


if __name__ == "__main__":
    main()
