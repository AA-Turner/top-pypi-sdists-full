# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""CLI commands for the EU regression runner."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

from cyclopts import Parameter

from airbyte_ops_mcp.cli._base import App
from airbyte_ops_mcp.regression_tests.eu_runner.job_spec import build_batch_job
from airbyte_ops_mcp.regression_tests.eu_runner.verdict import (
    build_verdict,
    validate_verdict,
)

eu_runner_app = App(name="eu-runner", help="EU Cloud Batch regression runner.")


@eu_runner_app.command(name="build-job-spec")
def build_job_spec(
    job_id: Annotated[str, Parameter(help="Cloud Batch job ID.")],
    source_archive_uri: Annotated[str, Parameter(help="GCS source archive URI.")],
    run_prefix_uri: Annotated[str, Parameter(help="GCS run-prefix URI.")],
    cli_args_json: Annotated[str, Parameter(help="JSON array of CLI arguments.")],
    github_run_id: Annotated[str, Parameter(help="GitHub Actions run ID.")],
    connector: Annotated[str, Parameter(help="Connector name for the Batch label.")],
    max_run_duration_seconds: Annotated[
        int, Parameter(help="Batch deadline in seconds.")
    ],
    out: Annotated[Path, Parameter(help="Write the Batch Job JSON here.")],
    seed_state_staged: Annotated[
        bool,
        Parameter(
            help="A seed state was staged as state.json under the run prefix; "
            "the VM then stops when it cannot download it."
        ),
    ] = False,
    target_image: Annotated[
        str,
        Parameter(
            help="The image the workflow built and staged as target-image.tar "
            "under the run prefix; the VM loads it and stops unless the archive "
            "holds that image alone. Empty when nothing was staged."
        ),
    ] = "",
    machine_type: str = "e2-standard-2",
    cpu_milli: int = 2000,
    memory_mib: int = 6144,
    disk_gb: int = 30,
) -> None:
    """Write a Batch v1 Job JSON file."""
    job = build_batch_job(
        job_id=job_id,
        source_archive_uri=source_archive_uri,
        run_prefix_uri=run_prefix_uri,
        cli_args=json.loads(cli_args_json),
        github_run_id=github_run_id,
        connector=connector,
        max_run_duration_seconds=max_run_duration_seconds,
        seed_state_staged=seed_state_staged,
        target_image=target_image,
        machine_type=machine_type,
        cpu_milli=cpu_milli,
        memory_mib=memory_mib,
        disk_gb=disk_gb,
    )
    out.write_text(json.dumps(job, indent=2) + "\n", encoding="utf-8")


@eu_runner_app.command(name="render-summary")
def render_summary(
    batch_url: Annotated[str, Parameter(help="Cloud Batch job URL.")],
    logs_url: Annotated[str, Parameter(help="Cloud Logging URL.")],
    report_url: Annotated[str, Parameter(help="Report object URL.")],
    verdict: Annotated[Path, Parameter(help="Metadata verdict JSON.")],
) -> None:
    """Print the GitHub step-summary Markdown."""
    safe_verdict = None
    try:
        safe_verdict = json.loads(verdict.read_text(encoding="utf-8"))
        validate_verdict(safe_verdict)
    except Exception:
        safe_verdict = None
    lines = [
        "## EU connector regression",
        "",
        f"- [Cloud Batch job]({batch_url})",
        f"- [Cloud Logging]({logs_url})",
        f"- [HTML report]({report_url})",
    ]
    if safe_verdict is None:
        lines.extend(["", "verdict missing or invalid"])
    else:
        not_exercised_only = safe_verdict["not_exercised"] and not (
            safe_verdict["incomplete"]
            or safe_verdict["regression_detected"]
            or safe_verdict["both_failed"]
        )
        result = (
            "INCOMPLETE"
            if safe_verdict["incomplete"]
            else "NOT EXERCISED"
            if not_exercised_only
            else "passed"
            if safe_verdict["success"]
            else "failed"
        )
        lines.extend(
            [
                "",
                f"- **Result:** {result}",
                f"- **Both failed:** {safe_verdict['both_failed']}",
                f"- **Incomplete:** {safe_verdict['incomplete']}",
                f"- **Not exercised:** {safe_verdict['not_exercised']}",
                "",
                "| Command | Control exit | Target exit | Passed |",
                "|---|---:|---:|:---:|",
            ]
        )
        for item in safe_verdict.get("commands", []):
            lines.append(
                f"| {item['command']} | {item['control_exit_code']} | "
                f"{item['target_exit_code']} | {item['passed']} |"
            )
    print("\n".join(lines))


@eu_runner_app.command(name="write-verdict")
def write_verdict(
    output_dir: Annotated[Path, Parameter(help="Run output directory.")],
    out: Annotated[Path, Parameter(help="Write the metadata-only verdict here.")],
) -> None:
    """Write a masked metadata-only verdict JSON."""
    verdict = build_verdict(output_dir)
    out.write_text(json.dumps(verdict, indent=2) + "\n", encoding="utf-8")
