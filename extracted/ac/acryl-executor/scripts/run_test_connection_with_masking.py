#!/usr/bin/env python3
"""
Python wrapper for DataHub test connection with secret masking support.

Registers secrets before calling DataHub CLI to enable secret masking in subprocess output.

Environment Variables:
    DATAHUB_ENABLE_SECRET_MASKING: Set to "true" to enable secret masking (default: true)
    DATAHUB_SECRET_NAMES: Comma-separated list of secret env var names to mask
    EXECUTOR_TASK_MEMORY_LIMIT: Memory limit in bytes (optional)
"""

import json
import os
import resource
import subprocess
import sys
from pathlib import Path

from datahub.masking.bootstrap import initialize_secret_masking
from datahub.masking.masking_filter import SecretMaskingFilter
from datahub.masking.secret_registry import SecretRegistry


def parse_bool_env(env_var: str, default: bool = True) -> bool:
    """Parse boolean from environment variable."""
    value = os.getenv(env_var, "").lower()
    if value in ("true", "1", "yes"):
        return True
    elif value in ("false", "0", "no"):
        return False
    return default


def setup_memory_limit() -> None:
    """Apply memory limit if EXECUTOR_TASK_MEMORY_LIMIT is set."""
    memory_limit = os.environ.get("EXECUTOR_TASK_MEMORY_LIMIT")
    if not memory_limit:
        return

    try:
        limit_bytes = int(memory_limit)
        print(f"Setting memory limit to {limit_bytes} bytes", file=sys.stderr)
        resource.setrlimit(resource.RLIMIT_AS, (limit_bytes, limit_bytes))
    except Exception as e:
        print(f"Warning: Failed to set memory limit: {e}", file=sys.stderr)


def validate_venv(venv_path: str) -> tuple[Path, Path]:
    """Validate venv exists and has required components."""
    venv_python = Path(venv_path) / "bin" / "python"
    venv_datahub = Path(venv_path) / "bin" / "datahub"

    if not venv_python.exists():
        print(f"ERROR: Python binary not found in venv: {venv_python}", file=sys.stderr)
        sys.exit(1)

    if not venv_datahub.exists():
        print(f"ERROR: DataHub CLI not found in venv: {venv_datahub}", file=sys.stderr)
        sys.exit(1)

    return venv_python, venv_datahub


def activate_venv(venv_path: str) -> None:
    """Activate virtual environment by setting PATH and VIRTUAL_ENV."""
    os.environ["VIRTUAL_ENV"] = venv_path
    os.environ["PATH"] = f"{venv_path}/bin:{os.environ.get('PATH', '')}"


def register_secrets() -> None:
    """Register secrets with DataHub masking framework if enabled."""
    # Check if masking is enabled (default: true)
    masking_enabled = parse_bool_env("DATAHUB_ENABLE_SECRET_MASKING", default=True)

    if not masking_enabled:
        print(
            "Secret masking is DISABLED via DATAHUB_ENABLE_SECRET_MASKING=false",
            file=sys.stderr,
        )
        return

    # Get the list of secret names from parent process
    secret_names_str = os.getenv("DATAHUB_SECRET_NAMES", "")
    if not secret_names_str:
        print(
            "Warning: No secret names provided via DATAHUB_SECRET_NAMES",
            file=sys.stderr,
        )
        return

    secret_names = [
        name.strip() for name in secret_names_str.split(",") if name.strip()
    ]
    if not secret_names:
        print(
            "Warning: Empty secret names list from DATAHUB_SECRET_NAMES",
            file=sys.stderr,
        )
        return

    try:
        # Initialize masking infrastructure (logging filter, exception hook)
        initialize_secret_masking(force=True)

        # Register only the specified environment variables as secrets
        # The parent process has already resolved secrets and set them in the environment
        registry = SecretRegistry.get_instance()
        for var_name in secret_names:
            var_value = os.environ.get(var_name)
            if var_value:
                registry.register_secret(var_name, var_value)

        print(
            f"Secret masking enabled: registered {registry.get_count()} secret(s)",
            file=sys.stderr,
        )

    except Exception as e:
        print(
            f"Warning: Failed to initialize secret masking: {e}. Continuing without masking.",
            file=sys.stderr,
        )


def check_test_connection_support(datahub_binary: Path) -> bool:
    """Check if DataHub CLI supports --test-source-connection flag."""
    try:
        result = subprocess.run(
            [str(datahub_binary), "ingest", "run", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return "test-source-connection" in result.stdout
    except Exception as e:
        print(
            f"Warning: Failed to check --test-source-connection support: {e}",
            file=sys.stderr,
        )
        return False


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
    """Main entry point."""
    # Parse command-line arguments
    if len(sys.argv) < 4:
        print(
            f"Usage: {sys.argv[0]} <venv_path> <recipe_file> <report_out_file>",
            file=sys.stderr,
        )
        sys.exit(1)

    venv_path = sys.argv[1]
    recipe_file = sys.argv[2]
    report_out_file = sys.argv[3]

    print(f"recipe is at {recipe_file}", file=sys.stderr)

    # Step 1: Validate venv
    venv_python, venv_datahub = validate_venv(venv_path)

    # Step 2: Activate venv
    activate_venv(venv_path)

    # Step 3: Apply memory limit (if set)
    setup_memory_limit()

    # Step 4: Register secrets for masking (BEFORE importing/running DataHub CLI)
    # This ensures secrets are masked in the subprocess's own logging
    register_secrets()

    # Step 5: Check for --test-source-connection support
    has_test_connection = check_test_connection_support(venv_datahub)

    if not has_test_connection:
        create_unsupported_report(report_out_file)
        sys.exit(0)  # Exit 0 means we succeeded at trying and know why we failed

    print(
        "This version of datahub supports test-source-connection functionality",
        file=sys.stderr,
    )

    # Remove existing report file
    report_path = Path(report_out_file)
    if report_path.exists():
        report_path.unlink()

    # Step 6: Build command arguments for DataHub CLI
    # Call the venv's datahub binary as a subprocess to ensure it uses the venv's packages
    cmd = [
        str(venv_datahub),
        "ingest",
        "-c",
        recipe_file,
        "--test-source-connection",
        "--report-to",
        report_out_file,
    ]

    # Step 7: Execute DataHub CLI from the venv as a subprocess
    # Stream output line-by-line while applying secret masking
    print(f"Executing: {' '.join(cmd)}", file=sys.stderr)

    registry = SecretRegistry.get_instance()
    masking_filter = SecretMaskingFilter(secret_registry=registry)

    # Use Popen to stream output in real-time
    process = subprocess.Popen(
        cmd,
        env=os.environ.copy(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # Merge stderr into stdout for unified streaming
        text=True,
        bufsize=1,  # Line buffered
    )

    # Stream and mask output line-by-line
    if process.stdout:
        for line in process.stdout:
            masked_line = masking_filter.mask_text(line)
            print(masked_line, end="", flush=True)

    # Wait for process to complete
    returncode = process.wait()
    sys.exit(returncode)


if __name__ == "__main__":
    main()
