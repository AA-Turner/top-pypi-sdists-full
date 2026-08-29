#!/usr/bin/env python3
"""
Send BI asset metadata to Monte Carlo using the pycarlo IngestionService.

Maps to ``POST /ingest/v1/bi/metadata`` — the producer half of the Pandora BI
ingest contract. This registers a couple of BI assets (a dashboard and the
dataset it derives from) with BI→BI lineage, warehouse-table ``inputs``, an
owner, tags, and free-form attributes.

.. warning::
    This script makes a **live, authenticated POST**. It is intended for a
    **non-prod / dev** Integration Gateway. There is **no default endpoint** —
    you must pass one explicitly (or set ``MCD_API_ENDPOINT``) so this can never
    silently send data (including owner emails) to production.

Prerequisites:
    1. Install pycarlo locally:  pip install -e /path/to/python-sdk
    2. Create an integration key with Ingestion scope:
         montecarlo integrations create-key --scope Ingestion

Credentials come from the environment (never CLI args, which leak into shell
history and the process table) — the SDK's standard default-profile vars:
    export MCD_DEFAULT_API_ID=<INGESTION_KEY_ID>
    export MCD_DEFAULT_API_TOKEN=<INGESTION_KEY_SECRET>

Usage:
    export MCD_DEFAULT_API_ID=... MCD_DEFAULT_API_TOKEN=...
    python sample_ingest_bi.py \\
        --endpoint https://integrations.<dev-domain> \\
        --resource-uuid <CUSTOM_BI_CONNECTOR_CONTAINER_UUID>

    # --endpoint / --resource-uuid may instead be supplied via
    # MCD_API_ENDPOINT / MCD_BI_CONTAINER_UUID.
"""

import argparse
import json
import os
import sys

from pycarlo.core import Client, Session
from pycarlo.features.ingestion import (
    AssetRef,
    BiAsset,
    BiAssetRef,
    BiOwner,
    IngestionService,
)
from pycarlo.features.ingestion.models import Tag

DEFAULT_RESOURCE_TYPE = "custom-bi-connector"


def build_sample_assets() -> list[BiAsset]:
    dataset = BiAsset(
        asset_source_id="sample.orders_dataset",
        name="Orders dataset (sample)",
        asset_type="dataset",
        description="Sample BI dataset for /ingest/v1/bi/metadata.",
        folder="Sample/Finance",
        owner=BiOwner(email="data-eng@example.com", name="Data Engineering"),
        is_certified=True,
        # Warehouse tables upstream of this asset — reuses the shared AssetRef
        # (see BiAsset.inputs).
        inputs=[
            AssetRef(
                asset_type="TABLE",
                role="INPUT",
                fully_qualified_name="analytics:prod_internal_bi.account_health_scoring",
            )
        ],
        properties=[Tag(key="team", value="data-eng"), Tag(key="tier", value="gold")],
        attributes={"source": "sample", "workspace": "finance"},
    )

    dashboard = BiAsset(
        asset_source_id="sample.revenue_dashboard",
        name="Revenue dashboard (sample)",
        asset_type="dashboard",
        asset_url="https://bi.example.com/dashboards/revenue",
        owner=BiOwner(email="analytics@example.com"),
        view_count=128,
        # BI→BI lineage: this dashboard derives from the dataset above.
        upstream_assets=[
            BiAssetRef(
                asset_source_id="sample.orders_dataset",
                relationship_type="DERIVES_FROM",
            )
        ],
        properties=[Tag(key="team", value="analytics")],
    )

    return [dataset, dashboard]


def _print_step(label: str, result: dict | None) -> None:
    invocation_id = IngestionService.extract_invocation_id(result)
    print(f"{label} response: {json.dumps(result, indent=2) if result else '(empty)'}")
    if invocation_id:
        print(f"{label} invocation ID: {invocation_id}")


def _require(value: str | None, name: str) -> str:
    if not value:
        print(
            f"Error: {name} is required and was not provided. See the module docstring for setup.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return value


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Send sample BI asset metadata to Monte Carlo via pycarlo IngestionService",
    )
    parser.add_argument(
        "--endpoint",
        default=os.environ.get("MCD_API_ENDPOINT"),
        help="Integration Gateway endpoint (or set MCD_API_ENDPOINT). "
        "REQUIRED — no default, to avoid accidentally targeting production.",
    )
    parser.add_argument(
        "--resource-uuid",
        default=os.environ.get("MCD_BI_CONTAINER_UUID"),
        help="custom-bi-connector container UUID (or set MCD_BI_CONTAINER_UUID)",
    )
    parser.add_argument(
        "--resource-type",
        default=DEFAULT_RESOURCE_TYPE,
        help=f"Resource type (default: {DEFAULT_RESOURCE_TYPE})",
    )
    args = parser.parse_args()

    # Credentials come from the environment only — never CLI args.
    key_id = _require(os.environ.get("MCD_DEFAULT_API_ID"), "MCD_DEFAULT_API_ID (env)")
    key_token = _require(os.environ.get("MCD_DEFAULT_API_TOKEN"), "MCD_DEFAULT_API_TOKEN (env)")
    endpoint = _require(args.endpoint, "--endpoint / MCD_API_ENDPOINT")
    resource_uuid = _require(args.resource_uuid, "--resource-uuid / MCD_BI_CONTAINER_UUID")

    client = Client(
        session=Session(
            mcd_id=key_id,
            mcd_token=key_token,
            endpoint=endpoint,
            scope="Ingestion",
        )
    )

    # Session lets the MCD_API_ENDPOINT env var override the endpoint passed
    # above (see core/session.py). Guard against a stray env var silently
    # redirecting this POST to the wrong (e.g. prod) gateway — otherwise the
    # "explicit endpoint" safety of this script would be defeated.
    env_endpoint = os.environ.get("MCD_API_ENDPOINT")
    if env_endpoint and env_endpoint != endpoint:
        print(
            f"Error: MCD_API_ENDPOINT ({env_endpoint}) overrides --endpoint ({endpoint}); "
            "the request would target the env-var host. Unset MCD_API_ENDPOINT or align them.",
            file=sys.stderr,
        )
        raise SystemExit(2)

    service = IngestionService(mc_client=client)

    # Print the endpoint the session actually resolved to (not just the arg),
    # so what is logged matches what is POSTed.
    print(f"Sending sample BI metadata to {client.session_endpoint} ...")
    result = service.send_bi_metadata(
        resource_uuid=resource_uuid,
        resource_type=args.resource_type,
        events=build_sample_assets(),
    )
    _print_step("BI metadata", result)
    print("\nDone.")


if __name__ == "__main__":
    main()
