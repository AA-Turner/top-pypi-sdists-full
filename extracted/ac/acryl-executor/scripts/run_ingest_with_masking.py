#!/usr/bin/env python3
"""
Python wrapper for DataHub ingestion with secret masking support.

Registers secrets before calling DataHub CLI to enable secret masking in subprocess output.

Environment Variables:
    DATAHUB_ENABLE_SECRET_MASKING: Set to "true" to enable secret masking (default: true)
    DATAHUB_SECRET_NAMES: Comma-separated list of secret env var names to mask
    EXECUTOR_TASK_MEMORY_LIMIT: Memory limit in bytes (optional)
"""

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


def check_report_to_support(datahub_binary: Path) -> bool:
    """Check if DataHub CLI supports --report-to flag."""
    try:
        result = subprocess.run(
            [str(datahub_binary), "ingest", "run", "--help"],
            capture_output=True,
            text=True,
        )
        return "report-to" in result.stdout
    except Exception as e:
        print(f"Warning: Failed to check --report-to support: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point."""
    # Parse command-line arguments
    if len(sys.argv) < 4:
        print(
            f"Usage: {sys.argv[0]} <venv_path> <recipe_file> <report_out_file> [debug_mode]",
            file=sys.stderr,
        )
        sys.exit(1)

    venv_path = sys.argv[1]
    recipe_file = sys.argv[2]
    report_out_file = sys.argv[3]
    debug_mode = sys.argv[4] if len(sys.argv) > 4 else "false"

    # Step 1: Validate venv
    venv_python, venv_datahub = validate_venv(venv_path)

    # Step 2: Activate venv
    activate_venv(venv_path)

    # Step 3: Apply memory limit (if set)
    setup_memory_limit()

    # Step 4: Register secrets for masking (BEFORE importing/running DataHub CLI)
    # This ensures secrets are masked in the subprocess's own logging
    register_secrets()

    # Step 5: Check for --report-to support
    has_report_to = check_report_to_support(venv_datahub)

    if has_report_to:
        print(
            "This version of datahub supports report-to functionality", file=sys.stderr
        )
        # Remove existing report file
        report_path = Path(report_out_file)
        if report_path.exists():
            report_path.unlink()
    else:
        print(
            "Warning: This version of datahub does not support --report-to",
            file=sys.stderr,
        )

    # Step 6: Build command arguments for DataHub CLI
    # Call the venv's datahub binary as a subprocess to ensure it uses the venv's packages
    cmd = [str(venv_datahub)]

    # Add debug flag if enabled
    if debug_mode.lower() == "true":
        cmd.append("--debug")

    # Add ingest command
    cmd.extend(["ingest", "run", "-c", recipe_file])

    # Add report-to option if supported
    if has_report_to:
        cmd.extend(["--report-to", report_out_file])

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
