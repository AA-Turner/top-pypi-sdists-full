#!/usr/bin/env python3
"""
Script to fetch all simulator artifacts and their target fields.

Usage:
    python scripts/get_all_artifact_targets.py

Requires PLATO_API_KEY environment variable to be set.
"""

import json
import os
import sys

import httpx

from plato._generated.api.v1.cluster.get_snapshot_lineage import (
    sync as get_snapshot_lineage,
)
from plato._generated.api.v1.simulator.get_all_simulators_info import (
    sync as get_all_simulators_info,
)


def main():
    api_key = os.environ.get("PLATO_API_KEY")
    if not api_key:
        print("Error: PLATO_API_KEY environment variable is required", file=sys.stderr)
        sys.exit(1)

    base_url = os.environ.get("PLATO_BASE_URL", "https://plato.so")

    headers = {"X-API-Key": api_key}

    with httpx.Client(base_url=base_url, headers=headers, timeout=60.0) as client:
        # Step 1: Get all simulator info (contains all artifact IDs)
        print("Fetching all simulators...", file=sys.stderr)
        simulators = get_all_simulators_info(client, x_api_key=api_key)

        # Step 2: Extract all artifact IDs
        artifact_ids = []
        for sim in simulators:
            for artifact in sim.get("artifacts", []):
                artifact_ids.append(
                    {
                        "artifact_id": artifact["artifact_id"],
                        "simulator_name": sim["simulator_name"],
                    }
                )

        print(f"Found {len(artifact_ids)} artifacts", file=sys.stderr)

        # Step 3: For each artifact, get lineage with full details to get target
        results = []
        for i, item in enumerate(artifact_ids):
            artifact_id = item["artifact_id"]
            print(
                f"[{i + 1}/{len(artifact_ids)}] Fetching target for {artifact_id}...",
                file=sys.stderr,
            )

            try:
                lineage_response = get_snapshot_lineage(
                    client,
                    artifact_id=artifact_id,
                    include_full_details=True,
                )
                artifact_details = lineage_response.get("artifact", {})
                target = artifact_details.get("target")

                results.append(
                    {
                        "artifact_id": artifact_id,
                        "simulator_name": item["simulator_name"],
                        "target": target,
                    }
                )
            except Exception as e:
                print(f"  Error fetching {artifact_id}: {e}", file=sys.stderr)
                results.append(
                    {
                        "artifact_id": artifact_id,
                        "simulator_name": item["simulator_name"],
                        "target": None,
                        "error": str(e),
                    }
                )

        # Output full dataset as JSON
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
