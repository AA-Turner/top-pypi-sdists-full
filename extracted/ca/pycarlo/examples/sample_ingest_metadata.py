#!/usr/bin/env python3
"""
Send relational-asset metadata to Monte Carlo using the pycarlo IngestionService.

Prerequisites:
    1. Install pycarlo locally:  pip install -e /path/to/python-sdk
    2. Create an integration key with Ingestion scope:
         montecarlo integrations create-key --scope Ingestion
       Or via the GraphQL API / UI.

Usage:
    python sample_ingest_metadata.py \
        --key-id  <INGESTION_KEY_ID> \
        --key-token <INGESTION_KEY_SECRET> \
        --resource-uuid <WAREHOUSE_UUID> \
        --resource-type snowflake
"""

import argparse
import json

from pycarlo.core import Client, Session
from pycarlo.features.ingestion import IngestionService
from pycarlo.features.ingestion.models import (
    AssetField,
    AssetFreshness,
    AssetMetadata,
    AssetVolume,
    RelationalAsset,
    Tag,
)

DEFAULT_ENDPOINT = "https://integrations.getmontecarlo.com"
DEFAULT_ASSET_PREFIX = "run_01"
MANUAL_INGESTION_DATABASE = "manual_ingestion"
MANUAL_INGESTION_SCHEMA = "test"


def asset_name(prefix: str, suffix: str) -> str:
    return f"{prefix}_{suffix}"


def build_sample_events(prefix: str) -> list[RelationalAsset]:
    return [
        RelationalAsset(
            type="TABLE",
            metadata=AssetMetadata(
                name=asset_name(prefix, "a"),
                database=MANUAL_INGESTION_DATABASE,
                schema="test",
                description="Sample source table 1 for lineage",
                created_on="2026-01-15T00:00:00Z",
            ),
            tags=[
                Tag(key="team", value="data-eng"),
                Tag(key="pii", value="false"),
            ],
            fields=[
                AssetField(name="id", type="INTEGER", description="Primary key"),
                AssetField(name="amount", type="DECIMAL(10,2)"),
                AssetField(name="created_at", type="TIMESTAMP_NTZ"),
            ],
            volume=AssetVolume(row_count=1_000_000, byte_count=111_111_111),
            freshness=AssetFreshness(last_update_time="2026-03-12T14:30:00Z"),
        ),
        RelationalAsset(
            type="TABLE",
            metadata=AssetMetadata(
                name=asset_name(prefix, "b"),
                database=MANUAL_INGESTION_DATABASE,
                schema=MANUAL_INGESTION_SCHEMA,
                description="Sample source table 2 for lineage",
            ),
            fields=[
                AssetField(name="status", type="VARCHAR(50)"),
                AssetField(name="created_at", type="TIMESTAMP_NTZ"),
            ],
            freshness=AssetFreshness(last_update_time="2026-03-12T15:00:00Z"),
        ),
        RelationalAsset(
            type="TABLE",
            metadata=AssetMetadata(
                name=asset_name(prefix, "c"),
                database=MANUAL_INGESTION_DATABASE,
                schema=MANUAL_INGESTION_SCHEMA,
                description="Sample destination table for lineage",
                created_on="2026-01-15T00:00:00Z",
            ),
            tags=[
                Tag(key="team", value="data-eng"),
                Tag(key="pii", value="false"),
            ],
            fields=[
                AssetField(name="event_id", type="INTEGER", description="Derived event identifier"),
                AssetField(name="event_type", type="VARCHAR(50)", description="Derived event type"),
            ],
            volume=AssetVolume(row_count=500_000, byte_count=55_555_555),
            freshness=AssetFreshness(last_update_time="2026-03-12T16:00:00Z"),
        ),
        RelationalAsset(
            type="VIEW",
            metadata=AssetMetadata(
                name=asset_name(prefix, "view_c"),
                database=MANUAL_INGESTION_DATABASE,
                schema=MANUAL_INGESTION_SCHEMA,
                description="Sample downstream view for lineage",
                view_query=(
                    "SELECT event_id, event_type FROM "
                    f"{MANUAL_INGESTION_DATABASE}.{MANUAL_INGESTION_SCHEMA}."
                    f"{asset_name(prefix, 'c')}"
                ),
            ),
            fields=[
                AssetField(name="event_id", type="INTEGER"),
                AssetField(name="event_type", type="VARCHAR(50)"),
            ],
        ),
    ]


def main():
    parser = argparse.ArgumentParser(
        description="Send sample metadata to Monte Carlo via pycarlo IngestionService",
    )
    parser.add_argument("--key-id", required=True, help="Ingestion key ID (x-mcd-id)")
    parser.add_argument("--key-token", required=True, help="Ingestion key token (x-mcd-token)")
    parser.add_argument(
        "--endpoint",
        default=DEFAULT_ENDPOINT,
        help=f"Integration Gateway endpoint (default: {DEFAULT_ENDPOINT})",
    )
    parser.add_argument("--resource-uuid", default="your-warehouse-uuid", help="Resource UUID")
    parser.add_argument(
        "--resource-type",
        default="snowflake",
        help="Resource type (e.g. snowflake, bigquery)",
    )
    parser.add_argument(
        "--payload-file",
        help="Path to a JSON file with a custom payload (uses send_metadata_raw)",
    )
    parser.add_argument(
        "--asset-prefix",
        default=DEFAULT_ASSET_PREFIX,
        help=(
            "Prefix for the sample assets so metadata and lineage can target a fresh "
            f"shared set (default: {DEFAULT_ASSET_PREFIX})"
        ),
    )
    args = parser.parse_args()

    client = Client(
        session=Session(
            mcd_id=args.key_id,
            mcd_token=args.key_token,
            endpoint=args.endpoint,
            scope="Ingestion",
        )
    )
    service = IngestionService(mc_client=client)

    if args.payload_file:
        with open(args.payload_file) as f:
            payload = json.load(f)
        print(f"Sending raw payload from {args.payload_file} ...")
        result = service.send_metadata_raw(payload=payload)
    else:
        events = build_sample_events(args.asset_prefix)
        print(
            "Sample assets: "
            f"{asset_name(args.asset_prefix, 'a')}, "
            f"{asset_name(args.asset_prefix, 'b')}, "
            f"{asset_name(args.asset_prefix, 'c')}, "
            f"{asset_name(args.asset_prefix, 'view_c')}"
        )
        print(f"Sending {len(events)} relational assets to resource {args.resource_uuid} ...")
        result = service.send_metadata(
            resource_uuid=args.resource_uuid,
            resource_type=args.resource_type,
            events=events,
        )

    invocation_id = service.extract_invocation_id(result)
    print(f"Response: {json.dumps(result, indent=2) if result else '(empty)'}")
    if invocation_id:
        print(f"Invocation ID: {invocation_id}")
    print("Done.")


if __name__ == "__main__":
    main()
