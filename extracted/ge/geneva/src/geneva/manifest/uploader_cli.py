# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Common CLI utilities for UDF manifest upload scripts.

This module provides reusable command-line interface functions for uploading
UDF manifests to Geneva and adding columns to tables. It eliminates boilerplate
across UDF upload scripts by centralizing common functionality like argument
parsing, dry-run diagnostics, zip generation, and upload workflows.
"""

import argparse
import logging
import os
import site
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import geneva
from geneva.packager.autodetect import get_paths_to_package, package_local_env_into_zips
from geneva.packager.zip import _DEFAULT_IGNORES, WorkspaceZipper


def create_upload_parser(
    description: str,
    default_manifest_name: str,
) -> argparse.ArgumentParser:
    """
    Create standardized argument parser for UDF upload scripts.

    Parameters
    ----------
        description
            Description of what this UDF does
        default_manifest_name
            Default name for the manifest (e.g., "simple-udfs-v1")

    Returns
    -------
        Configured ArgumentParser with all standard upload arguments
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--bucket", required=True, help="Geneva bucket path (e.g., gs://bucket/path)"
    )
    parser.add_argument(
        "--manifest-name",
        default=default_manifest_name,
        help=f"Manifest name (default: {default_manifest_name})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run mode - create manifest but don't upload",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed file list in dry-run mode (use with --dry-run)",
    )
    parser.add_argument(
        "--generate-zip",
        action="store_true",
        help="Generate manifest zip files locally in dry-run mode (use with --dry-run)",
    )
    parser.add_argument(
        "--zip-output-dir",
        default=".geneva",
        help="Output directory for generated zips (default: .geneva)",
    )
    return parser


def run_dry_run_diagnostics(
    manifest: Any,
    args: argparse.Namespace,
    logger: logging.Logger,
) -> None:
    """
    Execute dry-run diagnostics showing paths, files, and sizes to be packaged.

    Parameters
    ----------
        manifest
            The manifest object to diagnose
        args
            Parsed command-line arguments
        logger
            Logger instance for output
    """
    logger.info("=== DRY RUN MODE ===")
    logger.info("Python executable: %s", sys.executable)
    logger.info("Python version: %s", sys.version)
    logger.info("Current directory: %s", Path.cwd())
    logger.info("site.getsitepackages(): %s", site.getsitepackages())

    paths = get_paths_to_package(skip_site_packages=False)
    logger.info("\nPaths that will be packaged (%s total):", len(paths))

    total_files = 0
    total_size = 0

    for i, p in enumerate(paths, 1):
        if not p.exists():
            logger.info("  %s. %s (not found)", i, p)
            continue

        if not p.is_dir():
            logger.info("  %s. %s (not a directory)", i, p)
            continue

        # Get directory size
        result = subprocess.run(["du", "-sh", str(p)], capture_output=True, text=True)
        dir_size = result.stdout.split()[0] if result.returncode == 0 else "unknown"
        logger.info("\n  %s. %s (%s)", i, p, dir_size)

        # If verbose, show detailed file list
        if args.verbose:
            try:
                # Use WorkspaceZipper to scan files (applies ignore patterns)
                ignores = _DEFAULT_IGNORES.copy()
                zipper = WorkspaceZipper(
                    p, output_dir=Path(args.zip_output_dir), ignore_regexs=ignores
                )
                checksum, path_total_size, files = zipper.checksum()

                total_files += len(files)
                total_size += path_total_size

                size_mb = path_total_size / (1024**2)
                logger.info("     Files to package: %s (%.1f MB)", len(files), size_mb)

                # Show first 50 files, last 10 files
                if len(files) <= 60:
                    for arcname, size in files:
                        logger.info("       - %s (%.1f KB)", arcname, size / 1024)
                else:
                    logger.info("     First 50 files:")
                    for arcname, size in files[:50]:
                        logger.info("       - %s (%.1f KB)", arcname, size / 1024)
                    logger.info("     ... (%s files omitted) ...", len(files) - 60)
                    logger.info("     Last 10 files:")
                    for arcname, size in files[-10:]:
                        logger.info("       - %s (%.1f KB)", arcname, size / 1024)

            except Exception as e:
                logger.warning("     Could not scan files: %s", e)
        else:
            logger.info("     (use --verbose to see file list)")

    if args.verbose:
        total_size_mb = total_size / (1024**2)
        logger.info(
            "\nTotal: %s files, %.1f MB across all paths",
            total_files,
            total_size_mb,
        )


def generate_local_zips(
    manifest: Any,
    zip_output_dir: str,
    logger: logging.Logger,
) -> None:
    """
    Generate manifest zip files locally for inspection.

    Parameters
    ----------
        manifest
            The manifest object with package configuration
        zip_output_dir
            Directory where zip files should be created
        logger
            Logger instance for output
    """
    logger.info("\n=== GENERATING ZIP FILES LOCALLY ===")
    zip_output = Path(zip_output_dir)
    zip_output.mkdir(parents=True, exist_ok=True)

    logger.info("Output directory: %s", zip_output.absolute())

    try:
        # Package into zip files
        zips = package_local_env_into_zips(
            zip_output,
            skip_site_packages=manifest.skip_site_packages,
            create_zips=True,
        )

        logger.info("\n✓ Created %s zip file set(s):", len(zips))
        for zip_set in zips:
            if not zip_set:
                continue
            for zip_path in zip_set:
                if isinstance(zip_path, Path) and zip_path.exists():
                    size_mb = zip_path.stat().st_size / (1024**2)
                    logger.info("  - %s (%.1f MB)", zip_path.name, size_mb)

        logger.info("\nInspect with:")
        logger.info("  unzip -l %s/*.zip | less", zip_output)
        logger.info("  unzip -l %s/*.part*.zip | less  # for sharded zips", zip_output)

    except Exception as e:
        logger.error("Failed to generate zips: %s", e)
        import traceback

        traceback.print_exc()


def upload_manifest_and_add_columns(
    bucket: str,
    manifest_name: str,
    manifest: Any,
    table_name: str,
    columns_fn: Callable[[], dict[str, Callable]],
    logger: logging.Logger,
) -> None:
    """
    Upload manifest to Geneva and add columns to table.

    Parameters
    ----------
        bucket
            Geneva bucket path (e.g., gs://bucket/path)
        manifest_name
            Name for the manifest
        manifest
            The manifest object to upload
        table_name
            Name of table to add columns to
        columns_fn
            Function that returns column definitions
        logger
            Logger instance for output
    """
    # Connect and upload
    logger.info("Connecting to %s", bucket)
    conn = geneva.connect(bucket)

    logger.info("Uploading manifest '%s'", manifest_name)
    conn.define_manifest(manifest_name, manifest)

    logger.info("✓ Successfully uploaded manifest '%s' to %s", manifest_name, bucket)

    # Add columns to table
    logger.info("Opening table '%s'", table_name)
    tbl = conn.open_table(table_name)

    columns = columns_fn()
    logger.info("Adding columns: %s", list(columns.keys()))
    tbl.add_columns(columns)  # type: ignore[arg-type]

    logger.info("✓ Successfully added columns to table '%s'", table_name)
    logger.info("  Columns: %s", list(columns.keys()))


def main_upload_workflow(
    get_columns_fn: Callable[[], dict[str, Callable]],
    create_manifest_fn: Callable[[str], Any],
    description: str,
    default_manifest_name: str,
    logger: logging.Logger | None = None,
) -> None:
    """
    Complete upload workflow that handles all common logic.

    This is the main entry point that orchestrates:
    1. Argument parsing
    2. Dry-run or actual upload
    3. Manifest creation
    4. Column addition

    UDF scripts only need to call this with their specific:
    - get_columns function
    - create_manifest function
    - description string
    - default manifest name

    Parameters
    ----------
        get_columns_fn
            Function that returns dict mapping column names
            to UDF functions
        create_manifest_fn
            Function that takes manifest name and returns
            manifest object
        description
            Description of what this UDF does
        default_manifest_name
            Default name for the manifest
        logger
            Optional logger instance (creates default if not provided)

    Examples
    --------
        ```python
        from geneva.manifest.uploader_cli import main_upload_workflow
        from manifest import create_manifest
        from my_udfs import my_udf_func

        def get_columns():
            return {"my_column": my_udf_func}

        if __name__ == "__main__":
            main_upload_workflow(
                get_columns_fn=get_columns,
                create_manifest_fn=create_manifest,
                description="Upload my UDFs manifest",
                default_manifest_name="my-udfs-v1",
            )
        ```
    """
    # Setup logger if not provided
    if logger is None:
        logger = logging.getLogger(__name__)

    # Parse arguments
    parser = create_upload_parser(description, default_manifest_name)
    args = parser.parse_args()

    # Get table name from environment (skip in dry-run mode)
    table_name = os.getenv("GENEVA_TABLE_NAME")
    if not args.dry_run and not table_name:
        raise ValueError(
            "GENEVA_TABLE_NAME environment variable must be set "
            "(e.g., export GENEVA_TABLE_NAME=oxford_pets_shared_abc123)"
        )

    # Dry run: Show diagnostic information
    if args.dry_run:
        run_dry_run_diagnostics(None, args, logger)

    # Create manifest in UDF's environment
    logger.info("\nCreating manifest '%s' in UDF environment", args.manifest_name)
    manifest = create_manifest_fn(args.manifest_name)

    logger.info("Manifest summary:")
    logger.info("  Name: %s", manifest.name)
    logger.info("  pip dependencies: %s", manifest.pip)
    logger.info("  requirements_path: %s", manifest.requirements_path)
    logger.info("  conda dependencies: %s", manifest.conda)
    logger.info("  conda_environment_path: %s", manifest.conda_environment_path)
    logger.info("  py_modules: %s", manifest.py_modules)
    logger.info("  skip_site_packages: %s", manifest.skip_site_packages)

    if args.dry_run:
        # Generate zip files locally if requested
        if args.generate_zip:
            generate_local_zips(manifest, args.zip_output_dir, logger)

        logger.info("\n=== DRY RUN: Skipping upload and column addition ===")
        logger.info("Would upload manifest '%s' to %s", args.manifest_name, args.bucket)
        if table_name:
            columns_list = list(get_columns_fn().keys())
            logger.info("Would add columns to table '%s': %s", table_name, columns_list)
        logger.info("✓ Dry run completed successfully")
        return

    # Upload and add columns
    if table_name is None:
        raise ValueError("GENEVA_TABLE_NAME must be set for non-dry-run execution")
    upload_manifest_and_add_columns(
        args.bucket,
        args.manifest_name,
        manifest,
        table_name,
        get_columns_fn,
        logger,
    )
