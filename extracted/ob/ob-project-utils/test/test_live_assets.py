"""
Example: Listing asset instances with ob-project-utils

Shows how to discover assets, browse their version history,
and retrieve a specific instance by ID. All operations are read-only.

Usage:
    source .venv/bin/activate
    python test_live_assets.py
"""

from obproject.assets import Asset


def show_instances(name, instances):
    print(f"  {name}")
    for i, inst in enumerate(instances):
        print(f"    [{i}] {inst.created_at}  by {inst.created_by.entity_id}")
        if inst.blobs:
            print(f"        blobs: {inst.blobs}")
        if inst.annotations:
            print(f"        annotations: {inst.annotations}")
    print()


def main():
    a = Asset(project="ob_project_starter", branch="main")
    print(f"Connected: {a.base_url} (perimeter={a.perimeter})\n")

    # List data assets and their instances
    data_assets = a.list_data_assets().get("items", [])
    print(f"== {len(data_assets)} data asset(s) ==\n")
    for item in data_assets:
        name = item["asset"]["id"]

        # NEW: list_data_asset_instances returns an iterator of typed
        # AssetInstance namedtuples (id, created_at, created_by, annotations,
        # tags, blobs, kind, asset_kind).
        instances = list(a.list_data_asset_instances(name))
        show_instances(name, instances)

        # NEW: peek_data_asset retrieves an instance by ID without
        # tracking asset as being consumed.
        if len(instances) >= 1:
            target = instances[0]
            print(f"  Peeking at instance: {target.id}")
            ref = a.peek_data_asset(name, instance=target.id)
            print(f"    created_at: {ref['created_at']}")
            print(f"    created_by: {ref['created_by']}")
            print()

    # List model assets and their instances
    model_assets = a.list_model_assets().get("items", [])
    print(f"== {len(model_assets)} model asset(s) ==\n")
    for item in model_assets:
        name = item["asset"]["id"]

        # NEW: list_model_asset_instances -- same interface as above but
        # for model assets.
        instances = list(a.list_model_asset_instances(name))
        show_instances(name, instances)

        # NEW: peek_model_asset -- same as above for model assets.
        if len(instances) >= 1:
            target = instances[0]
            print(f"  Peeking at instance: {target.id}")
            ref = a.peek_model_asset(name, instance=target.id)
            print(f"    created_at: {ref['created_at']}")
            print(f"    created_by: {ref['created_by']}")
            print()


if __name__ == "__main__":
    main()
