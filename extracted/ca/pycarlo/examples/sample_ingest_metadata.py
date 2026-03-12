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


def build_sample_events() -> list[RelationalAsset]:
    return [
        RelationalAsset(
            type="TABLE",
            metadata=AssetMetadata(
                name="fede_10",
                database="manual_ingestion",
                schema="test",
                description="Test table",
                created_on="2026-03-06T00:00:00Z",
            ),
            tags=[
                Tag(key="team", value="data-eng"),
                Tag(key="pii", value="false"),
            ],
            fields=[
                AssetField(name="event_id", type="VARCHAR(36)", description="Primary key"),
                AssetField(name="event_type", type="VARCHAR(100)", description="FK to customers"),
                AssetField(name="payload", type="VARIANT"),
                AssetField(name="ingested_at", type="TIMESTAMP_NTZ"),
            ],
            volume=AssetVolume(row_count=1_500_000, byte_count=524_288_000),
            freshness=AssetFreshness(last_update_time="2026-03-02T14:30:00Z"),
        ),
        RelationalAsset(
            type="TABLE",
            metadata=AssetMetadata(
                name="fede_11",
                database="manual_ingestion",
                schema="test",
                description="Test table",
                created_on="2026-03-06T11:12:00Z",
            ),
            tags=[
                Tag(key="team", value="data-eng"),
                Tag(key="pii", value="false"),
            ],
            fields=[
                AssetField(name="event_id", type="VARCHAR(36)", description="Primary key"),
                AssetField(name="event_type", type="VARCHAR(100)", description="FK to customers"),
                AssetField(name="payload", type="VARIANT"),
                AssetField(name="ingested_at", type="TIMESTAMP_NTZ"),
            ],
            volume=AssetVolume(row_count=1_500_000, byte_count=524_288_000),
            freshness=AssetFreshness(last_update_time="2026-03-02T15:30:00Z"),
        ),
        RelationalAsset(
            type="TABLE",
            metadata=AssetMetadata(
                name="fede_12",
                database="manual_ingestion",
                schema="test",
                description="Test table",
                created_on="2026-03-06T10:15:00Z",
            ),
            tags=[
                Tag(key="team", value="data-eng"),
                Tag(key="pii", value="false"),
            ],
            fields=[
                AssetField(name="id", type="INTEGER"),
                AssetField(name="customer_id", type="INTEGER"),
                AssetField(name="amount", type="DECIMAL(10,2)"),
                AssetField(name="status", type="VARCHAR(50)"),
                AssetField(name="created_at", type="TIMESTAMP_NTZ"),
            ],
            volume=AssetVolume(row_count=1_500_000, byte_count=524_288_000),
            freshness=AssetFreshness(last_update_time="2026-03-06T15:30:00Z"),
        ),
        RelationalAsset(
            type="VIEW",
            metadata=AssetMetadata(
                name="fede_view_11",
                database="manual_ingestion",
                schema="test",
                description="Test view",
                view_query="SELECT * FROM manual_ingestion.test.fede",
            ),
            fields=[
                AssetField(name="id", type="INTEGER"),
                AssetField(name="customer_id", type="INTEGER"),
                AssetField(name="amount", type="DECIMAL(10,2)"),
                AssetField(name="status", type="VARCHAR(50)"),
                AssetField(name="created_at", type="TIMESTAMP_NTZ"),
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
        events = build_sample_events()
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
