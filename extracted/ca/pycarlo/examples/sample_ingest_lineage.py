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
        --key-id <INGESTION_KEY_ID> \
        --key-token <INGESTION_KEY_SECRET> \
        --resource-uuid <WAREHOUSE_UUID> \
        --resource-type snowflake \
        --asset-prefix lineage_run_01

Usage (column-level lineage):
    python sample_ingest_lineage.py \
        --key-id <INGESTION_KEY_ID> \
        --key-token <INGESTION_KEY_SECRET> \
        --resource-uuid <WAREHOUSE_UUID> \
        --resource-type snowflake \
        --asset-prefix lineage_run_01 \
        --column-lineage
"""

from __future__ import annotations

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
DEFAULT_ASSET_PREFIX = "run_01"
MANUAL_INGESTION_DATABASE = "manual_ingestion"
MANUAL_INGESTION_SCHEMA = "test"
SEARCH_LIMIT = 20

GET_TABLE_LINEAGE_QUERY_V2 = """
    query getTableLineageV2(
      $mcons: [String]!
      $direction: LineageGraphTraversalDirection!
      $filters: [LineageFilter]
    ) {
      getTableLineageV2(
        mcons: $mcons
        direction: $direction
        filters: $filters
      ) {
        nodes {
          displayName
          mcon
          objectType
          elementId
        }
        edges {
          source
          destination
          sourceId
          destinationId
          hidden
        }
      }
    }
"""
SEARCH_QUERY = """
    query search($query: String!, $limit: Int!) {
        search(
            query: $query
            limit: $limit
            offset: 0
            fullResults: true
            operator: "AND"
        ) {
            totalHits
            results {
                mcon
                displayName
                objectType
            }
        }
    }
"""


def asset_name(prefix: str, suffix: str) -> str:
    return f"{prefix}_{suffix}"


def build_table_lineage_events(prefix: str) -> list[LineageEvent]:
    """Create sample table lineage aligned with the metadata sample assets."""
    destination_table: str = asset_name(prefix, "c")
    source_a: str = asset_name(prefix, "a")
    source_b: str = asset_name(prefix, "b")
    downstream_view: str = asset_name(prefix, "view_c")
    return [
        LineageEvent(
            destination=LineageAssetRef(
                type="TABLE",
                name=destination_table,
                database=MANUAL_INGESTION_DATABASE,
                schema=MANUAL_INGESTION_SCHEMA,
            ),
            sources=[
                LineageAssetRef(
                    type="TABLE",
                    name=source_a,
                    database=MANUAL_INGESTION_DATABASE,
                    schema=MANUAL_INGESTION_SCHEMA,
                ),
                LineageAssetRef(
                    type="TABLE",
                    name=source_b,
                    database=MANUAL_INGESTION_DATABASE,
                    schema=MANUAL_INGESTION_SCHEMA,
                ),
            ],
        ),
        LineageEvent(
            destination=LineageAssetRef(
                type="VIEW",
                name=downstream_view,
                database=MANUAL_INGESTION_DATABASE,
                schema=MANUAL_INGESTION_SCHEMA,
            ),
            sources=[
                LineageAssetRef(
                    type="TABLE",
                    name=destination_table,
                    database=MANUAL_INGESTION_DATABASE,
                    schema=MANUAL_INGESTION_SCHEMA,
                ),
            ],
        ),
    ]


def build_column_lineage_events(prefix: str) -> list[LineageEvent]:
    """Create sample column lineage aligned with the metadata sample assets."""
    destination_table: str = asset_name(prefix, "c")
    source_a: str = asset_name(prefix, "a")
    source_b: str = asset_name(prefix, "b")
    source_a_asset_id = f"{prefix}_src_a"
    source_b_asset_id = f"{prefix}_src_b"
    destination_asset_id = f"{prefix}_dest_c"

    return [
        LineageEvent(
            destination=LineageAssetRef(
                type="TABLE",
                name=destination_table,
                database=MANUAL_INGESTION_DATABASE,
                schema=MANUAL_INGESTION_SCHEMA,
                asset_id=destination_asset_id,
            ),
            sources=[
                LineageAssetRef(
                    type="TABLE",
                    name=source_a,
                    database=MANUAL_INGESTION_DATABASE,
                    schema=MANUAL_INGESTION_SCHEMA,
                    asset_id=source_a_asset_id,
                ),
                LineageAssetRef(
                    type="TABLE",
                    name=source_b,
                    database=MANUAL_INGESTION_DATABASE,
                    schema=MANUAL_INGESTION_SCHEMA,
                    asset_id=source_b_asset_id,
                ),
            ],
            fields=[
                ColumnLineageField(
                    name="event_id",
                    source_fields=[
                        ColumnLineageSourceField(
                            asset_id=source_a_asset_id,
                            field_name="id",
                        ),
                    ],
                ),
                ColumnLineageField(
                    name="event_type",
                    source_fields=[
                        ColumnLineageSourceField(
                            asset_id=source_b_asset_id,
                            field_name="status",
                        ),
                    ],
                ),
            ],
        ),
    ]


def build_cross_warehouse_lineage_events(
    prefix: str,
    *,
    source_resource_uuid: str,
    source_resource_type: str,
    dest_resource_uuid: str,
    dest_resource_type: str,
) -> list[LineageEvent]:
    """Create a cross-warehouse table->table lineage event.

    Each asset names its own warehouse via ``resource_uuid`` / ``resource_type``.
    The top-level resource is omitted from the ``send_lineage`` call so the source
    and destination can live in different warehouses.
    """
    return [
        LineageEvent(
            destination=LineageAssetRef(
                type="TABLE",
                name=asset_name(prefix, "dest"),
                database=MANUAL_INGESTION_DATABASE,
                schema=MANUAL_INGESTION_SCHEMA,
                resource_uuid=dest_resource_uuid,
                resource_type=dest_resource_type,
            ),
            sources=[
                LineageAssetRef(
                    type="TABLE",
                    name=asset_name(prefix, "src"),
                    database=MANUAL_INGESTION_DATABASE,
                    schema=MANUAL_INGESTION_SCHEMA,
                    resource_uuid=source_resource_uuid,
                    resource_type=source_resource_type,
                ),
            ],
        ),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Send sample lineage to Monte Carlo via pycarlo IngestionService",
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
        "--column-lineage",
        action="store_true",
        help="Send column-level lineage instead of table-level",
    )
    parser.add_argument(
        "--cross-warehouse",
        action="store_true",
        help=(
            "Send cross-warehouse table->table lineage (source and destination in "
            "different warehouses). Uses per-asset resource_uuid/resource_type and "
            "omits the top-level resource."
        ),
    )
    parser.add_argument(
        "--source-resource-uuid",
        help="Source asset's warehouse UUID (cross-warehouse mode)",
    )
    parser.add_argument(
        "--source-resource-type",
        default="snowflake",
        help="Source asset's resource type (cross-warehouse mode)",
    )
    parser.add_argument(
        "--dest-resource-uuid",
        help="Destination asset's warehouse UUID (cross-warehouse mode)",
    )
    parser.add_argument(
        "--dest-resource-type",
        default="bigquery",
        help="Destination asset's resource type (cross-warehouse mode)",
    )
    parser.add_argument(
        "--payload-file",
        help="Path to a JSON file with a custom payload (uses send_lineage_raw)",
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
        with open(args.payload_file, encoding="utf-8") as file_handle:
            payload = json.load(file_handle)
        print(f"Sending raw lineage payload from {args.payload_file} ...")
        result = service.send_lineage_raw(payload=payload)
    elif args.cross_warehouse:
        source_wh = args.source_resource_uuid or args.resource_uuid
        dest_wh = args.dest_resource_uuid or args.resource_uuid
        events = build_cross_warehouse_lineage_events(
            args.asset_prefix,
            source_resource_uuid=source_wh,
            source_resource_type=args.source_resource_type,
            dest_resource_uuid=dest_wh,
            dest_resource_type=args.dest_resource_type,
        )
        print(
            f"Sending {len(events)} cross-warehouse lineage event(s) "
            f"(source warehouse {source_wh}, destination warehouse {dest_wh}) ..."
        )
        # No top-level resource: each asset carries its own resource_uuid.
        result = service.send_lineage(events=events)
    else:
        if args.column_lineage:
            events = build_column_lineage_events(args.asset_prefix)
            label = "column-level"
        else:
            events = build_table_lineage_events(args.asset_prefix)
            label = "table-level"

        print(
            "Sample assets: "
            f"{asset_name(args.asset_prefix, 'a')}, "
            f"{asset_name(args.asset_prefix, 'b')}, "
            f"{asset_name(args.asset_prefix, 'c')}, "
            f"{asset_name(args.asset_prefix, 'view_c')}"
        )
        print(
            f"Sending {len(events)} {label} lineage event(s) to resource {args.resource_uuid} ..."
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
