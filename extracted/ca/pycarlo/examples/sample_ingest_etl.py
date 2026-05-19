#!/usr/bin/env python3
"""
Send ETL metadata and run events to Monte Carlo using the pycarlo
IngestionService.

This example walks through the full ETL flow:
    1. Register a job declaratively via ``send_etl_metadata``.
    2. Emit a run-start event via ``send_etl_runs`` (status=in_progress).
    3. Emit a run-complete event via ``send_etl_runs`` (status=success).

Prerequisites:
    1. Install pycarlo locally:  pip install -e /path/to/python-sdk
    2. Create an integration key with Ingestion scope:
         montecarlo integrations create-key --scope Ingestion

Usage:
    python sample_ingest_etl.py \\
        --key-id  <INGESTION_KEY_ID> \\
        --key-token <INGESTION_KEY_SECRET> \\
        --resource-uuid <RESOURCE_UUID> \\
        --resource-type airflow
"""

import argparse
import json
from datetime import datetime, timedelta, timezone

from pycarlo.core import Client, Session
from pycarlo.features.ingestion import (
    AssetRef,
    EtlAsset,
    EtlRunEvent,
    IngestionService,
    Owner,
    Schedule,
)
from pycarlo.features.ingestion.models import Tag

DEFAULT_ENDPOINT = "https://integrations.getmontecarlo.com"
DEFAULT_JOB_SOURCE_ID = "sample_dag.load_orders"


def _iso_now(offset_seconds: int = 0) -> str:
    return (
        (datetime.now(timezone.utc) + timedelta(seconds=offset_seconds))
        .isoformat()
        .replace("+00:00", "Z")
    )


def build_sample_asset(job_source_id: str) -> EtlAsset:
    return EtlAsset(
        job_source_id=job_source_id,
        name="Load orders (sample)",
        description="Sample ETL job for /ingest/v1/etl/metadata.",
        folder="sample/etl",
        is_paused=False,
        job_url="https://airflow.example/dags/sample_dag/graph",
        schedule=Schedule(
            kind="cron",
            cron_expression="0 0 * * *",
            timezone="UTC",
            paused=False,
            # ``next_run_at`` intentionally omitted — consumer-side serialization
            # of ``EtlJob.schedule`` doesn't handle pydantic-parsed datetimes
            # yet; restore once that lands.
        ),
        owner=Owner(
            primary_email="data-eng@example.com",
            primary_name="Data Engineering",
            notification_emails=["alerts@example.com"],
            team="data-eng",
        ),
        properties=[
            Tag(key="team", value="data-eng"),
            Tag(key="env", value="prod"),
        ],
    )


def build_run_start_event(job_source_id: str, run_source_id: str, start_time: str) -> EtlRunEvent:
    return EtlRunEvent(
        job_source_id=job_source_id,
        run_source_id=run_source_id,
        status="in_progress",
        event_time=start_time,
        start_time=start_time,
        trigger="SCHEDULE",
        attempt_number=1,
        run_url=f"https://airflow.example/dags/sample_dag/runs/{run_source_id}",
    )


def build_run_complete_event(
    job_source_id: str, run_source_id: str, start_time: str
) -> EtlRunEvent:
    # ``start_time`` must be stable across all emissions for the same run —
    # consumer uses it as the partition key, so drift produces duplicate rows.
    end = _iso_now(60)
    return EtlRunEvent(
        job_source_id=job_source_id,
        run_source_id=run_source_id,
        status="success",
        event_time=end,
        start_time=start_time,
        end_time=end,
        trigger="SCHEDULE",
        attempt_number=1,
        run_url=f"https://airflow.example/dags/sample_dag/runs/{run_source_id}",
        inputs=[
            AssetRef(
                asset_type="TABLE",
                role="INPUT",
                fully_qualified_name="analytics:prod_internal_bi.tam_weekly_customer_health_score",
            )
        ],
        outputs=[
            AssetRef(
                asset_type="TABLE",
                role="OUTPUT",
                fully_qualified_name="analytics:prod_internal_bi.account_health_scoring",
            )
        ],
    )


def _print_step(label: str, result: dict | None) -> None:
    invocation_id = IngestionService.extract_invocation_id(result)
    print(f"{label} response: {json.dumps(result, indent=2) if result else '(empty)'}")
    if invocation_id:
        print(f"{label} invocation ID: {invocation_id}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Send sample ETL metadata + run events to Monte Carlo "
        "via pycarlo IngestionService",
    )
    parser.add_argument("--key-id", required=True, help="Ingestion key ID (x-mcd-id)")
    parser.add_argument("--key-token", required=True, help="Ingestion key token (x-mcd-token)")
    parser.add_argument(
        "--endpoint",
        default=DEFAULT_ENDPOINT,
        help=f"Integration Gateway endpoint (default: {DEFAULT_ENDPOINT})",
    )
    parser.add_argument(
        "--resource-uuid",
        default="your-resource-uuid",
        help="Resource UUID",
    )
    parser.add_argument(
        "--resource-type",
        default="airflow",
        help="Resource type (e.g. airflow, dbt)",
    )
    parser.add_argument(
        "--job-source-id",
        default=DEFAULT_JOB_SOURCE_ID,
        help="Source-system job ID",
    )
    parser.add_argument(
        "--run-source-id",
        default="sample-run-001",
        help="Run source ID for the start/complete pair",
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

    print("Step 1/3 — register job declaratively via send_etl_metadata ...")
    asset = build_sample_asset(args.job_source_id)
    meta_result = service.send_etl_metadata(
        resource_uuid=args.resource_uuid,
        resource_type=args.resource_type,
        events=[asset],
    )
    _print_step("Metadata", meta_result)

    run_start_time = _iso_now()
    print("\nStep 2/3 — emit run-start event via send_etl_runs (in_progress) ...")
    start_result = service.send_etl_runs(
        resource_uuid=args.resource_uuid,
        resource_type=args.resource_type,
        events=[build_run_start_event(args.job_source_id, args.run_source_id, run_start_time)],
    )
    _print_step("Run start", start_result)

    print("\nStep 3/3 — emit run-complete event via send_etl_runs (success) ...")
    end_result = service.send_etl_runs(
        resource_uuid=args.resource_uuid,
        resource_type=args.resource_type,
        events=[build_run_complete_event(args.job_source_id, args.run_source_id, run_start_time)],
    )
    _print_step("Run complete", end_result)

    print("\nDone.")


if __name__ == "__main__":
    main()
