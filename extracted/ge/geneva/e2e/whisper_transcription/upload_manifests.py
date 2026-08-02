#!/usr/bin/env python
# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Upload Whisper transcription UDF manifests from suite-level orchestration."""

from __future__ import annotations

import argparse
import importlib.util
import logging
import os
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import geneva

from geneva.manifest.uploader_cli import (
    generate_local_zips,
    run_dry_run_diagnostics,
    upload_manifest_and_add_columns,
)

logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

SYNC_CMD = ["uv", "sync", "--index-strategy", "unsafe-best-match"]
SUITE_DIR = Path(__file__).resolve().parent
GCS_RUN_DEPS = ["google-cloud-storage"]
AWS_RUN_DEPS = ["boto3", "awscli"]
AZURE_RUN_DEPS = ["azure-storage-blob", "azure-identity"]


@dataclass(frozen=True)
class ProfileConfig:
    name: str
    profile_dir: Path
    default_manifest_name: str
    columns_fn: Callable[[], dict[str, Callable]] | None


def _columns_whisper() -> dict[str, Callable]:
    from geneva.udfs.audio.whisper_transcription import download_audio

    return {
        "audio_bytes": download_audio,
    }


PROFILES: dict[str, ProfileConfig] = {
    "whisper_transcription": ProfileConfig(
        name="whisper_transcription",
        profile_dir=SUITE_DIR / "udfs" / "whisper_transcription",
        default_manifest_name="whisper-transcription-udfs-v1",
        columns_fn=_columns_whisper,
    ),
}


def _load_create_manifest(profile_dir: Path) -> Callable[[str], Any]:
    manifest_path = profile_dir / "manifest.py"
    spec = importlib.util.spec_from_file_location(
        f"{profile_dir.name}_manifest", manifest_path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load manifest module: {manifest_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    create_manifest = getattr(module, "create_manifest", None)
    if create_manifest is None:
        raise AttributeError(f"create_manifest not found in {manifest_path}")
    return create_manifest


def _parse_profiles(raw_profiles: list[str]) -> list[str]:
    if not raw_profiles:
        return list(PROFILES.keys())

    values: list[str] = []
    for raw in raw_profiles:
        values.extend(part.strip() for part in raw.split(",") if part.strip())

    if "all" in values:
        return list(PROFILES.keys())

    unknown = [name for name in values if name not in PROFILES]
    if unknown:
        raise ValueError(f"Unknown profile(s): {unknown}. Valid: {sorted(PROFILES)}")

    return list(dict.fromkeys(values))


def _run_command(cmd: list[str], cwd: Path, profile: str) -> None:
    result = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        env={
            **os.environ.copy(),
            "UV_CACHE_DIR": os.environ.get("UV_CACHE_DIR", "/tmp/.uv-cache"),
        },
    )
    if result.stdout:
        for line in result.stdout.splitlines():
            _LOG.info("[%s] %s", profile, line)
    if result.stderr:
        for line in result.stderr.splitlines():
            _LOG.warning("[%s] %s", profile, line)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed for profile '{profile}': {' '.join(cmd)}")


def _run_profile_subprocess(profile: str, args: argparse.Namespace) -> None:
    cfg = PROFILES[profile]
    _LOG.info("Syncing dependencies for profile '%s'", profile)
    _run_command(SYNC_CMD, cfg.profile_dir, profile)

    cmd = ["uv", "run"]
    if args.bucket.startswith("gs://"):
        for dep in GCS_RUN_DEPS:
            cmd.extend(["--with", dep])
    elif args.bucket.startswith("s3://"):
        for dep in AWS_RUN_DEPS:
            cmd.extend(["--with", dep])
    elif args.bucket.startswith("az://"):
        for dep in AZURE_RUN_DEPS:
            cmd.extend(["--with", dep])

    cmd.extend([
        "python",
        str(Path(__file__).resolve()),
        "--bucket",
        args.bucket,
        "--profile",
        profile,
        "--execute-profile",
    ])
    if args.manifest_name:
        cmd.extend(["--manifest-name", args.manifest_name])
    if args.dry_run:
        cmd.append("--dry-run")
    if args.verbose:
        cmd.append("--verbose")
    if args.generate_zip:
        cmd.append("--generate-zip")
    if args.zip_output_dir != ".geneva":
        cmd.extend(["--zip-output-dir", args.zip_output_dir])

    _LOG.info("Running upload for profile '%s'", profile)
    _run_command(cmd, cfg.profile_dir, profile)


def _execute_profile(profile: str, args: argparse.Namespace) -> None:
    cfg = PROFILES[profile]
    manifest_name = args.manifest_name or cfg.default_manifest_name

    create_manifest = _load_create_manifest(cfg.profile_dir)
    manifest = create_manifest(manifest_name)

    _LOG.info("Creating manifest '%s' for profile '%s'", manifest_name, profile)
    _LOG.info("Manifest summary: pip=%s py_modules=%s", manifest.pip, manifest.py_modules)

    if args.dry_run:
        run_dry_run_diagnostics(manifest, args, _LOG)
        if args.generate_zip:
            generate_local_zips(manifest, args.zip_output_dir, _LOG)
        _LOG.info("Dry run complete for profile '%s'", profile)
        return

    table_name = os.getenv("GENEVA_TABLE_NAME")
    if not table_name:
        raise ValueError("GENEVA_TABLE_NAME must be set for non-dry-run execution")

    upload_manifest_and_add_columns(
        args.bucket,
        manifest_name,
        manifest,
        table_name,
        cfg.columns_fn,
        _LOG,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Upload Whisper transcription UDF manifests"
    )
    parser.add_argument("--bucket", required=True, help="Geneva bucket path")
    parser.add_argument(
        "--profile",
        action="append",
        default=[],
        help=(
            "Profile name to upload. Can be repeated or comma-separated. "
            "Use 'all' (default) for all profiles."
        ),
    )
    parser.add_argument(
        "--manifest-name",
        default=None,
        help="Override manifest name (only valid with a single profile)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Dry run only")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed file list in dry-run mode",
    )
    parser.add_argument(
        "--generate-zip",
        action="store_true",
        help="Generate local zip files in dry-run mode",
    )
    parser.add_argument(
        "--zip-output-dir",
        default=".geneva",
        help="Output directory for generated zips",
    )
    parser.add_argument("--execute-profile", action="store_true", help=argparse.SUPPRESS)
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    selected_profiles = _parse_profiles(args.profile)
    if args.manifest_name and len(selected_profiles) != 1:
        raise ValueError("--manifest-name can only be used with a single profile")

    if args.execute_profile:
        if len(selected_profiles) != 1:
            raise ValueError("--execute-profile requires exactly one profile")
        _execute_profile(selected_profiles[0], args)
        return

    for profile in selected_profiles:
        _run_profile_subprocess(profile, args)


if __name__ == "__main__":
    main()
