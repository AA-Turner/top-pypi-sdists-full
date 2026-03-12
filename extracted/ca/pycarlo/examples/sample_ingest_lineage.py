#!/usr/bin/env python3
"""
Send lineage events (table-level and column-level) to Monte Carlo using pycarlo.

Prerequisites:
    1. Install pycarlo locally:  pip install -e /path/to/python-sdk
    2. Create an integration key with Ingestion scope:
         montecarlo integrations create-key --scope Ingestion --description "lineage test"
       Or via the GraphQL API / UI.

Usage (table-level lineage):
    python sample_ingest_lineage.py \
        --key-id  <INGESTION_KEY_ID> \
        --key-token <INGESTION_KEY_SECRET> \
        --resource-uuid <WAREHOUSE_UUID> \
        --resource-type snowflake

Usage (column-level lineage):
    python sample_ingest_lineage.py \
        --key-id  <INGESTION_KEY_ID> \
        --key-token <INGESTION_KEY_SECRET> \
        --resource-uuid <WAREHOUSE_UUID> \
        --resource-type snowflake \
        --column-lineage
"""

import argparse
import json

from pycarlo.core import Client, Session
from pycarlo.features.ingestion import IngestionService
from pycarlo.features.ingestion.models import (
    ColumnLineageField,
    ColumnLineageSourceField,
    LineageAssetRef,
    LineageEvent,
)

DEFAULT_ENDPOINT = "https://integrations.getmontecarlo.com"


def build_table_lineage_events() -> list[LineageEvent]:
    """Two table-level lineage edges: orders + customers -> order_summary."""
    return [
        LineageEvent(
            destination=LineageAssetRef(
                type="TABLE",
                name="fede_10",
                database="manual_ingestion",
                schema="test",
            ),
            sources=[
                LineageAssetRef(
                    type="TABLE",
                    name="fede_11",
                    database="manual_ingestion",
                    schema="test",
                ),
                LineageAssetRef(
                    type="TABLE",
                    name="fede_12",
                    database="manual_ingestion",
                    schema="test",
                ),
            ],
        ),
        LineageEvent(
            destination=LineageAssetRef(
                type="VIEW",
                name="fede_view_11",
                database="manual_ingestion",
                schema="test",
            ),
            sources=[
                LineageAssetRef(
                    type="TABLE",
                    name="fede_11",
                    database="manual_ingestion",
                    schema="test",
                ),
            ],
        ),
    ]


def build_column_lineage_events() -> list[LineageEvent]:
    """Column-level lineage: orders.amount + customers.name -> order_summary columns."""
    return [
        LineageEvent(
            destination=LineageAssetRef(
                type="TABLE",
                name="fede_10",
                database="manual_ingestion",
                schema="test",
                asset_id="dest_fede_10",
            ),
            sources=[
                LineageAssetRef(
                    type="TABLE",
                    name="fede_11",
                    database="manual_ingestion",
                    schema="test",
                    asset_id="src_fede_11",
                ),
                LineageAssetRef(
                    type="TABLE",
                    name="fede_12",
                    database="manual_ingestion",
                    schema="test",
                    asset_id="src_fede_12",
                ),
            ],
            fields=[
                ColumnLineageField(
                    name="event_id",
                    source_fields=[
                        ColumnLineageSourceField(
                            asset_id="src_fede_11",
                            field_name="event_id",
                        ),
                    ],
                ),
                ColumnLineageField(
                    name="event_type",
                    source_fields=[
                        ColumnLineageSourceField(
                            asset_id="src_fede_12",
                            field_name="customer_id",
                        ),
                    ],
                ),
            ],
        ),
    ]


def main():
    parser = argparse.ArgumentParser(
        description="Send sample lineage to Monte Carlo via pycarlo IngestionService",
    )
    parser.add_argument("--key-id", required=True, help="Ingestion key ID (x-mcd-id)")
    parser.add_argument(
        "--key-token", required=True, help="Ingestion key token (x-mcd-token)"
    )
    parser.add_argument(
        "--endpoint",
        default=DEFAULT_ENDPOINT,
        help=f"Integration Gateway endpoint (default: {DEFAULT_ENDPOINT})",
    )
    parser.add_argument(
        "--resource-uuid",
        default="your-warehouse-uuid",
        help="Resource UUID",
    )
    parser.add_argument(
        "--resource-type",
        default="snowflake",
        help="Resource type (e.g. snowflake, bigquery)",
    )
    parser.add_argument(
        "--column-lineage",
        action="store_true",
        help="Send column-level lineage instead of table-level",
    )
    parser.add_argument(
        "--payload-file",
        help="Path to a JSON file with a custom payload (uses send_lineage_raw)",
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
        print(f"Sending raw lineage payload from {args.payload_file} ...")
        result = service.send_lineage_raw(payload=payload)
    else:
        if args.column_lineage:
            events = build_column_lineage_events()
            label = "column-level"
        else:
            events = build_table_lineage_events()
            label = "table-level"

        print(
            f"Sending {len(events)} {label} lineage event(s) "
            f"to resource {args.resource_uuid} ..."
        )
        result = service.send_lineage(
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
