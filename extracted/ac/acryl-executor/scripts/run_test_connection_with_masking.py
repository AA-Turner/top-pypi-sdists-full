#!/usr/bin/env python3
"""
Python wrapper for DataHub test connection with secret masking support.

Reads a JSON envelope from stdin containing __recipe_yaml__, __secrets__,
and __report_out_file__. Forwards to `datahub ingest -c - --test-source-connection`
via stdin. Secrets never touch environment variables or disk.
"""

import json
import sys
from pathlib import Path

from acryl.executor.execution.wrapper_common import (
    activate_venv,
    build_datahub_stdin,
    check_cli_flag_support,
    read_stdin_envelope,
    register_secrets_for_masking,
    run_datahub_subprocess,
    setup_memory_limit,
    validate_venv,
)


def create_unsupported_report(report_out_file: str) -> None:
    """Create a report indicating test-source-connection is not supported."""
    report = {
        "internal_failure": True,
        "internal_failure_reason": (
            "datahub library doesn't have test_connection feature. "
            "You are likely running an old version."
        ),
    }

    with open(report_out_file, "w") as f:
        json.dump(report, f, indent=2)

    print(
        "datahub ingest doesn't seem to have test_connection feature. "
        "You are likely running an old version",
        file=sys.stderr,
    )


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <venv_path>", file=sys.stderr)
        sys.exit(1)

    venv_path = sys.argv[1]

    _raw_envelope, envelope = read_stdin_envelope()
    recipe_yaml = envelope["__recipe_yaml__"]
    secrets = envelope.get("__secrets__", {})
    report_out_file = envelope["__report_out_file__"]

    _venv_python, venv_datahub = validate_venv(venv_path)
    activate_venv(venv_path)
    setup_memory_limit()
    register_secrets_for_masking(secrets)

    has_test_connection = check_cli_flag_support(venv_datahub, "test-source-connection")
    if not has_test_connection:
        create_unsupported_report(report_out_file)
        sys.exit(0)

    print(
        "This version of datahub supports test-source-connection functionality",
        file=sys.stderr,
    )
    report_path = Path(report_out_file)
    if report_path.exists():
        report_path.unlink()

    datahub_stdin = build_datahub_stdin(recipe_yaml, secrets)

    cmd = [
        str(venv_datahub),
        "ingest",
        "-c",
        "-",
        "--test-source-connection",
        "--report-to",
        report_out_file,
    ]

    sys.exit(run_datahub_subprocess(cmd, datahub_stdin))


if __name__ == "__main__":
    main()
