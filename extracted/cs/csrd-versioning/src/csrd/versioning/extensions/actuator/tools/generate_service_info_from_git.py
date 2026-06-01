"""Generate service metadata from git for the actuator ``/actuator/info`` endpoint.

Run this script at build time to write a JSON file consumed by
``InfoActuatorPlugin``.
"""

import argparse
import json
import os
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_DEFAULT_OUTPUT_PATH = "service_info.json"
_DOCKER_BUILD_ENV = "ACTUATOR_INFO_DOCKER_BUILD"
_DOCKER_BUILD_ENV_VALUE = "1"


def _git(*cmd: str, default: str = "") -> str:
    try:
        return subprocess.check_output(["git", *cmd], stderr=subprocess.DEVNULL, text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return default


def _iso_utc(value: str) -> str:
    if not value:
        return ""
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return ""
    return parsed.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _resolve_output_path() -> Path:
    return Path(os.getenv("ACTUATOR_INFO_OUTPUT_PATH", _DEFAULT_OUTPUT_PATH))


def _normalize_build_version(build_version: str) -> str:
    return build_version.strip()


def _assert_docker_build_context() -> None:
    if os.getenv(_DOCKER_BUILD_ENV) != _DOCKER_BUILD_ENV_VALUE:
        raise SystemExit(
            "generate_service_info_from_git.py is build-only and must run from Docker "
            f"with {_DOCKER_BUILD_ENV}={_DOCKER_BUILD_ENV_VALUE}."
        )


def _build_info(build_version: str = "") -> dict[str, Any]:
    normalized_build_version = _normalize_build_version(build_version)
    commit_time = _iso_utc(_git("log", "-1", "--format=%cI"))
    commit_full = _git("rev-parse", "HEAD")
    commit_abbrev = _git("rev-parse", "--short", "HEAD")
    remote_url = _git("remote", "get-url", "origin")
    service_name = remote_url.rsplit("/", 1)[-1].removesuffix(".git") if remote_url else ""

    resolved_version = normalized_build_version or _git("describe", "--tags", "--always")

    git_info: dict[str, Any] = {
        "branch": _git("rev-parse", "--abbrev-ref", "HEAD"),
        "commit": {
            "time": commit_time,
            "message": {
                "full": _git("log", "-1", "--format=%B"),
                "short": _git("log", "-1", "--format=%s"),
            },
            "id": {
                "abbrev": commit_abbrev,
                "full": commit_full,
                "describe": _git("describe", "--tags"),
            },
            "user": {
                "name": _git("log", "-1", "--format=%an"),
                "email": _git("log", "-1", "--format=%ae"),
            },
        },
        "dirty": str(bool(_git("status", "--porcelain"))).lower(),
        "remote": {"origin": {"url": remote_url}},
    }

    if normalized_build_version:
        git_info["build"] = {"version": normalized_build_version}

    return {
        "git": git_info,
        "build": {
            "artifact": service_name,
            "name": service_name,
            "group": "com.example",
            "version": resolved_version,
            "time": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate service metadata from git for InfoActuatorPlugin."
    )
    parser.add_argument(
        "--build-version",
        default="",
        help=(
            "Explicit release version injected by the CI pipeline "
            '(e.g. --build-version="${BUILD_VERSION}"). '
            "Populates build.version and git.build.version. "
            "Falls back to `git describe --tags --always` when omitted."
        ),
    )
    args = parser.parse_args()
    _assert_docker_build_context()

    info = _build_info(build_version=args.build_version)
    output_path = _resolve_output_path()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(info, indent=2), encoding="utf-8")
    abbrev = info.get("git", {}).get("commit", {}).get("id", {}).get("abbrev", "")
    print(f"Wrote {output_path} (commit {abbrev})")


if __name__ == "__main__":
    main()
