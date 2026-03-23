#!/usr/bin/env python3
"""
Send query log events to Monte Carlo using the pycarlo IngestionService.

Prerequisites:
    1. Install pycarlo locally:  pip install -e /path/to/python-sdk
    2. Create an integration key with Ingestion scope:
         montecarlo integrations create-key --scope Ingestion
      Or via the GraphQL API / UI.

Usage:
    python sample_ingest_query_logs.py \
        --key-id <INGESTION_KEY_ID> \
        --key-token <INGESTION_KEY_SECRET> \
        --resource-uuid <WAREHOUSE_UUID> \
        --log-type snowflake \
        --asset-prefix query_logs_run_01
"""

import argparse
import json
import uuid
from datetime import datetime, timedelta, timezone

from pycarlo.core import Client, Session
from pycarlo.features.ingestion import IngestionService
from pycarlo.features.ingestion.models import QueryLogEntry

DEFAULT_ENDPOINT = "https://integrations.getmontecarlo.com"
DEFAULT_ASSET_PREFIX = "run_01"
MANUAL_INGESTION_DATABASE = "manual_ingestion"
MANUAL_INGESTION_SCHEMA = "test"


# Time window for sample events (used for verify search)
SAMPLE_START_TIME = datetime.now(timezone.utc) - timedelta(hours=1)
SAMPLE_END_TIME = datetime.now(timezone.utc) + timedelta(minutes=55)


def asset_name(prefix: str, suffix: str) -> str:
    return f"{prefix}_{suffix}"


def build_table_fqn(prefix: str, suffix: str) -> str:
    return f"{MANUAL_INGESTION_DATABASE}.{MANUAL_INGESTION_SCHEMA}.{asset_name(prefix, suffix)}"


def build_sample_events(prefix: str) -> tuple[list[QueryLogEntry], list[str]]:
    """Build sample events and return (events, query_ids) for verification."""
    now = datetime.now(timezone.utc)
    query_ids = [str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())]
    source_a = build_table_fqn(prefix, "a")
    source_b = build_table_fqn(prefix, "b")
    destination_c = build_table_fqn(prefix, "c")
    downstream_view = build_table_fqn(prefix, "view_c")

    print(f"Query IDs: {query_ids}")
    print(
        "Sample assets referenced by query logs: "
        f"{asset_name(prefix, 'a')}, "
        f"{asset_name(prefix, 'b')}, "
        f"{asset_name(prefix, 'c')}, "
        f"{asset_name(prefix, 'view_c')}"
    )

    events = [
        QueryLogEntry(
            start_time=SAMPLE_START_TIME,
            end_time=now - timedelta(minutes=58),
            query_text=(
                f"SELECT id, amount, created_at FROM {source_a} "
                "WHERE created_at >= CURRENT_DATE - INTERVAL '1 day' /**/"
            ),
            query_id=query_ids[0],
            user="analyst@company.com",
            returned_rows=1,
        ),
        QueryLogEntry(
            start_time=now - timedelta(minutes=57),
            end_time=now - timedelta(minutes=56),
            query_text=f"SELECT * FROM {destination_c} WHERE event_type = 'missing' /**/",
            query_id=query_ids[1],
            user="dev@company.com",
            error_code="NO_DATA",
            error_text="No matching rows found for sample query",
        ),
        QueryLogEntry(
            start_time=now - timedelta(minutes=58),
            end_time=now - timedelta(minutes=57),
            query_text=(
                "SELECT c.event_id, c.event_type, b.status "
                f"FROM {destination_c} c "
                f"LEFT JOIN {source_b} b ON c.event_type = b.status "
                "LIMIT 100 /**/"
            ),
            query_id=query_ids[2],
            user="bi_tool@company.com",
            returned_rows=100,
            extra={"warehouse": "COMPUTE_WH", "role": "ANALYST"},
        ),
        QueryLogEntry(
            start_time=now - timedelta(minutes=55),
            end_time=now - timedelta(minutes=54),
            query_text=(
                f"SELECT event_id, event_type FROM {downstream_view} "
                "ORDER BY event_id DESC LIMIT 25 /**/"
            ),
            query_id=str(uuid.uuid4()),
            user="analytics_app@company.com",
            returned_rows=25,
        ),
    ]
    return events, [*query_ids, events[3].query_id]


def main():
    parser = argparse.ArgumentParser(
        description="Send sample query logs to Monte Carlo via pycarlo IngestionService",
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
        "--log-type",
        default="snowflake",
        help="Log type (e.g. snowflake, bigquery) — the connection/warehouse type identifier",
    )
    parser.add_argument(
        "--payload-file",
        help="Path to a JSON file with a custom payload (uses send_query_logs_raw)",
    )
    parser.add_argument(
        "--asset-prefix",
        default=DEFAULT_ASSET_PREFIX,
        help=(
            "Prefix for the sample assets so query logs can target the same fresh "
            f"set used by metadata and lineage (default: {DEFAULT_ASSET_PREFIX})"
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
        result = service.send_query_logs_raw(payload=payload)
        print(f"Response: {json.dumps(result, indent=2) if result else '(empty)'}")
    else:
        events, query_ids = build_sample_events(args.asset_prefix)
        print(f"Sending {len(events)} query log events to resource {args.resource_uuid} ...")
        result = service.send_query_logs(
            resource_uuid=args.resource_uuid,
            log_type=args.log_type,
            events=events,
        )
        invocation_id = service.extract_invocation_id(result)
        if invocation_id:
            print(f"Invocation ID: {invocation_id}")
        print(f"Response: {json.dumps(result, indent=2) if result else '(empty)'}")

    print("Done.")


if __name__ == "__main__":
    main()
