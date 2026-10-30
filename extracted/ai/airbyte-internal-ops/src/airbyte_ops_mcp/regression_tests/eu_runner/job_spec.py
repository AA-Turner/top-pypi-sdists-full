# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Build a Cloud Batch v1 job for an EU regression run."""

from __future__ import annotations

import json
import re
from importlib.resources import files

PROJECT = "internal-airbyte-ai-infra"
REGION = "europe-west9"
NETWORK = "connector-regression-eu"
SERVICE_ACCOUNT = (
    "connector-regression-eu-job@internal-airbyte-ai-infra.iam.gserviceaccount.com"
)

_CREDENTIAL_ENV = re.compile(
    r"(?:_CREDENTIALS$|_SECRET$|_TOKEN$|CLIENT_ID)", re.IGNORECASE
)
_LABEL_VALUE = re.compile(r"[^a-z0-9_-]")


def _label_value(value: str) -> str:
    sanitized = _LABEL_VALUE.sub("_", value.lower()).strip("_-")[:63]
    sanitized = re.sub(r"_+", "_", sanitized).rstrip("_-")
    if not sanitized:
        return "unknown"
    if not sanitized[0].isalnum():
        sanitized = f"x{sanitized}"
    return sanitized


def validate_environment(variables: dict[str, str]) -> None:
    """Reject Batch environment keys that can carry credentials."""
    for key in variables:
        if _CREDENTIAL_ENV.search(key):
            raise ValueError(
                f"Credential-like Batch environment key is forbidden: {key}"
            )


def build_batch_job(
    *,
    job_id: str,
    source_archive_uri: str,
    run_prefix_uri: str,
    cli_args: list[str],
    github_run_id: str,
    connector: str,
    max_run_duration_seconds: int,
    seed_state_staged: bool = False,
    target_image: str = "",
    machine_type: str = "e2-standard-2",
    cpu_milli: int = 2000,
    memory_mib: int = 6144,
    disk_gb: int = 30,
) -> dict:
    """Build the regional, no-external-IP Batch Job JSON."""
    variables = {
        "DO_NOT_TRACK": "1",
        "SOURCE_ARCHIVE_URI": source_archive_uri,
        "RUN_PREFIX_URI": run_prefix_uri,
        "CLI_ARGS_JSON": json.dumps(cli_args),
        "SEED_STATE_STAGED": "true" if seed_state_staged else "false",
        "TARGET_IMAGE": target_image,
    }
    validate_environment(variables)
    script = (
        files("airbyte_ops_mcp.regression_tests.eu_runner")
        .joinpath("vm-run.sh")
        .read_text(encoding="utf-8")
    )
    return {
        "taskGroups": [
            {
                "taskCount": 1,
                "taskSpec": {
                    "runnables": [{"script": {"text": script}}],
                    "computeResource": {
                        "cpuMilli": cpu_milli,
                        "memoryMib": memory_mib,
                    },
                    "maxRunDuration": f"{max_run_duration_seconds}s",
                    "maxRetryCount": 0,
                    "environment": {"variables": variables},
                },
            }
        ],
        "allocationPolicy": {
            "location": {"allowedLocations": [f"regions/{REGION}"]},
            "instances": [
                {
                    "policy": {
                        "machineType": machine_type,
                        "bootDisk": {"image": "batch-debian", "sizeGb": disk_gb},
                    }
                }
            ],
            "network": {
                "networkInterfaces": [
                    {
                        "network": f"projects/{PROJECT}/global/networks/{NETWORK}",
                        "subnetwork": (
                            f"projects/{PROJECT}/regions/{REGION}/subnetworks/{NETWORK}"
                        ),
                        "noExternalIpAddress": True,
                    }
                ]
            },
            "serviceAccount": {"email": SERVICE_ACCOUNT},
        },
        "labels": {
            "github_run_id": _label_value(github_run_id),
            "connector": _label_value(connector),
        },
        "logsPolicy": {"destination": "CLOUD_LOGGING"},
    }
