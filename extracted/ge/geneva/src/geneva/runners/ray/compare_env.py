#!/usr/bin/env python3
# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
compare_ray_env.py

Compare local environment vs a Ray worker environment.

Usage:
  python compare_ray_env.py                   # connect to existing cluster
  python compare_ray_env.py --address local   # start new local cluster
  python compare_ray_env.py --env-prefix PY   # filter env vars by prefix
  python compare_ray_env.py --show-all        # print full snapshots
"""
# ruff: noqa: T201

import argparse
import json
import logging
import os
import platform
import sys
from typing import Any, TypedDict

# importlib.metadata is stdlib on 3.8+, backport for older
try:
    from importlib.metadata import distributions
except ImportError:
    from importlib_metadata import distributions  # type: ignore

_LOG = logging.getLogger(__name__)


def _get_context_runtime_env() -> dict[str, Any] | None:
    """Build a runtime_env dict from the active Geneva context's manifest.

    Returns None if no Geneva context is active or the manifest has no
    pip/conda dependencies.
    """
    try:
        from geneva._context import get_current_context
    except ImportError:
        return None

    ctx = get_current_context()
    if ctx is None or ctx.manifest is None:
        return None

    manifest = ctx.manifest
    # NOTE: This duplicates the pip/conda resolution logic from the canonical
    # source in _mgr.py init_ray(). If this logic changes, update both
    # places. See PR #541 for discussion on keeping vs extracting.
    ray_pip: str | list[str] | None = (
        manifest.requirements_path
        if manifest.requirements_path
        else (manifest.pip if manifest.pip else None)
    )
    ray_conda: str | dict[str, Any] | None = (
        manifest.conda_environment_path
        if manifest.conda_environment_path
        else (manifest.conda if manifest.conda else None)
    )

    if ray_pip is None and ray_conda is None:
        return None

    runtime_env: dict[str, Any] = {}
    if ray_pip is not None:
        runtime_env["pip"] = ray_pip
    if ray_conda is not None:
        runtime_env["conda"] = ray_conda

    _LOG.debug("Built runtime_env from Geneva context manifest: %s", runtime_env)
    return runtime_env


# Type definitions for structured return values


class PythonInfo(TypedDict):
    """Python version and implementation information."""

    version: str
    executable: str
    implementation: str


class PlatformInfo(TypedDict):
    """Platform/OS information."""

    system: str
    release: str
    machine: str
    processor: str


class EnvSnapshot(TypedDict):
    """Complete environment snapshot."""

    python: PythonInfo
    platform: PlatformInfo
    cwd: str
    env: dict[str, str]
    sys_path: list[str]
    packages: dict[str, str]


class EnvVarDiff(TypedDict):
    """Single environment variable difference."""

    key: str
    local: str | None
    remote: str | None


class EnvDiffs(TypedDict):
    """Environment variable differences."""

    only_local: list[str]
    only_remote: list[str]
    diffs: list[EnvVarDiff]


class PackageDiffs(TypedDict):
    """Package version differences."""

    only_local: list[str]
    only_remote: list[str]
    version_mismatch: list[tuple[str, str, str]]


class SysPathDiffs(TypedDict):
    """sys.path differences."""

    only_local: list[str]
    only_remote: list[str]
    intersection_count: int
    local_count: int
    remote_count: int


class ComparisonResult(TypedDict):
    """Complete comparison result."""

    local: EnvSnapshot
    remote: EnvSnapshot
    env_diffs: EnvDiffs
    pkg_diffs: PackageDiffs
    sys_path_diffs: SysPathDiffs


def snapshot_env() -> EnvSnapshot:
    """Collect a concise environment snapshot."""
    # Packages as {name: version}
    pkgs: dict[str, str] = {}
    for d in distributions():
        meta = d.metadata
        if meta is None:
            continue
        name = (meta.get("Name") or "").strip()
        if not name:
            # Some distributions can be missing metadata name; skip them
            continue
        version = d.version or meta.get("Version", "").strip()
        pkgs[name.lower()] = version

    return EnvSnapshot(
        python=PythonInfo(
            version=sys.version.replace("\n", " "),
            executable=sys.executable,
            implementation=platform.python_implementation(),
        ),
        platform=PlatformInfo(
            system=platform.system(),
            release=platform.release(),
            machine=platform.machine(),
            processor=platform.processor(),
        ),
        cwd=os.getcwd(),
        env=dict(os.environ),
        sys_path=list(sys.path),
        packages=pkgs,  # normalized to lowercase names
    )


def _filter_env(env: dict[str, str], prefix: str | None) -> dict[str, str]:
    """Filter environment variables by prefix.

    Parameters
    ----------
        env
            Dictionary of environment variables
        prefix
            Optional prefix to filter by (e.g., "PY" for Python-related vars)

    Returns
    -------
        Filtered dictionary, or original if no prefix specified
    """
    if not prefix:
        return env
    return {k: v for k, v in env.items() if k.startswith(prefix)}


def diff_env(
    local_env: dict[str, str], remote_env: dict[str, str], prefix: str | None
) -> EnvDiffs:
    """Compare environment variables between local and remote environments.

    Parameters
    ----------
        local_env
            Local environment variables
        remote_env
            Remote environment variables
        prefix
            Optional prefix to filter variables

    Returns
    -------
        EnvDiffs with keys
            only_local, only_remote, diffs
    """
    local_f = _filter_env(local_env, prefix)
    remote_f = _filter_env(remote_env, prefix)

    only_local = sorted(set(local_f) - set(remote_f))
    only_remote = sorted(set(remote_f) - set(local_f))
    common = sorted(set(local_f) & set(remote_f))

    diffs: list[EnvVarDiff] = [
        EnvVarDiff(key=k, local=local_f.get(k), remote=remote_f.get(k))
        for k in common
        if (local_f.get(k) or "") != (remote_f.get(k) or "")
    ]

    return EnvDiffs(only_local=only_local, only_remote=only_remote, diffs=diffs)


def diff_packages(
    local_pkgs: dict[str, str], remote_pkgs: dict[str, str]
) -> PackageDiffs:
    """Compare installed packages between local and remote environments.

    Parameters
    ----------
        local_pkgs
            Local packages as {name: version}
        remote_pkgs
            Remote packages as {name: version}

    Returns
    -------
        PackageDiffs with keys
            only_local, only_remote, version_mismatch
    """
    only_local = sorted(set(local_pkgs) - set(remote_pkgs))
    only_remote = sorted(set(remote_pkgs) - set(local_pkgs))
    common = sorted(set(local_pkgs) & set(remote_pkgs))

    version_mismatch: list[tuple[str, str, str]] = []
    for name in common:
        lv = local_pkgs.get(name, "")
        rv = remote_pkgs.get(name, "")
        if lv != rv:
            version_mismatch.append((name, lv, rv))

    return PackageDiffs(
        only_local=only_local,
        only_remote=only_remote,
        version_mismatch=version_mismatch,
    )


def diff_list(name: str, a: list[str], b: list[str]) -> SysPathDiffs:
    """Compare two lists and return set differences.

    Parameters
    ----------
        name
            Name of the list being compared (for reference)
        a
            Local list
        b
            Remote list

    Returns
    -------
        SysPathDiffs with counts and unique elements from each list
    """
    set_a, set_b = set(a), set(b)
    return SysPathDiffs(
        only_local=sorted(set_a - set_b),
        only_remote=sorted(set_b - set_a),
        intersection_count=len(set_a & set_b),
        local_count=len(set_a),
        remote_count=len(set_b),
    )


def pretty_section(title: str) -> None:
    """Print a formatted section header.

    Parameters
    ----------
        title
            Section title to display
    """
    print(f"\n=== {title} ===")  # noqa: T201


def print_env_diffs(env_diffs: EnvDiffs) -> None:  # noqa: T201
    """Print environment variable differences in a readable format.

    Parameters
    ----------
        env_diffs
            EnvDiffs from diff_env() containing differences
    """
    pretty_section("ENV VARS: keys only in LOCAL")
    for k in env_diffs["only_local"]:
        print(f"  + {k}")

    pretty_section("ENV VARS: keys only in REMOTE")
    for k in env_diffs["only_remote"]:
        print(f"  + {k}")

    pretty_section("ENV VARS: differing values")
    for d in env_diffs["diffs"]:
        print(f"  * {d['key']}")
        print(f"    local : {d['local']}")
        print(f"    remote: {d['remote']}")


def print_pkg_diffs(pkg_diffs: PackageDiffs) -> None:  # noqa: T201
    """Print package differences in a readable format.

    Parameters
    ----------
        pkg_diffs
            PackageDiffs from diff_packages() containing differences
    """
    pretty_section("PACKAGES: only in LOCAL")
    for k in pkg_diffs["only_local"]:
        print(f"  + {k}")

    pretty_section("PACKAGES: only in REMOTE")
    for k in pkg_diffs["only_remote"]:
        print(f"  + {k}")

    pretty_section("PACKAGES: version mismatches")
    for name, lv, rv in pkg_diffs["version_mismatch"]:
        print(f"  * {name}: local={lv}  remote={rv}")


def print_headline(local: EnvSnapshot, remote: EnvSnapshot) -> None:  # noqa: T201
    """Print summary of Python and platform info for local and remote.

    Parameters
    ----------
        local
            Local environment snapshot
        remote
            Remote environment snapshot
    """
    pretty_section("PYTHON / PLATFORM")
    print("Local:")
    print(f"  Python: {local['python']['version']}")
    print(f"  Impl  : {local['python']['implementation']}")
    print(f"  Exec  : {local['python']['executable']}")
    local_os = (
        f"  OS    : {local['platform']['system']} "
        f"{local['platform']['release']} ({local['platform']['machine']})"
    )
    print(local_os)
    print("\nRemote:")
    print(f"  Python: {remote['python']['version']}")
    print(f"  Impl  : {remote['python']['implementation']}")
    print(f"  Exec  : {remote['python']['executable']}")
    remote_os = (
        f"  OS    : {remote['platform']['system']} "
        f"{remote['platform']['release']} ({remote['platform']['machine']})"
    )
    print(remote_os)


def get_comparison_result(
    env_prefix: str | None = None,
    auto_init: bool = False,
    ray_address: str | None = "auto",
    runtime_env: dict[str, Any] | None = None,
) -> ComparisonResult:
    """Compare local environment with Ray worker environment (data only).

    Returns comparison data without printing. Use compare_ray_environments()
    if you want formatted console output.

    By default, requires Ray to already be initialized. Use auto_init=True
    to allow automatic Ray initialization.

    When called inside a Geneva context (``db.context(cluster=...,
    manifest=...)``), the manifest's pip/conda dependencies are automatically
    applied to the remote snapshot task so that the comparison reflects the
    actual worker environment.  Pass an explicit ``runtime_env`` to override.

    Parameters
    ----------
    env_prefix
        Optional prefix to filter environment variables (e.g., 'PY').
    auto_init
        If True, initialize Ray automatically. If False (default),
        require Ray to already be initialized.
    ray_address
        Ray address (only used when auto_init=True). Default 'auto'
        connects to existing cluster. Use None to start a new local cluster.
    runtime_env
        Optional Ray runtime_env dict to apply to the remote snapshot task.
        If not provided, the runtime_env is auto-detected from the active
        Geneva context's manifest (if any).

    Returns
    -------
    ComparisonResult
        Contains local, remote, env_diffs, pkg_diffs, and sys_path_diffs.

    Raises
    ------
    ImportError
        If Ray is not installed.
    RuntimeError
        If Ray is not initialized and auto_init=False.
    """
    # Local snapshot first
    local = snapshot_env()

    # Import ray lazily with a helpful message if missing
    try:
        import ray  # type: ignore
    except ImportError as e:
        raise ImportError(
            "Ray is not installed. Install with: pip install ray (or ray[default])"
        ) from e

    # Check Ray initialization
    if not ray.is_initialized():
        if not auto_init:
            raise RuntimeError(
                "Ray is not initialized. Either:\n"
                "  1. Run within a Geneva context:\n"
                "     with db.context(cluster=..., manifest=...):\n"
                "  2. Initialize Ray first: ray.init()\n"
                "  3. Pass auto_init=True to auto-initialize Ray"
            )
        # Auto-init requested
        ray.init(address=ray_address, logging_level="ERROR")

    # Auto-detect runtime_env from Geneva context if not explicitly provided
    if runtime_env is None:
        runtime_env = _get_context_runtime_env()

    # Define remote task
    @ray.remote
    def _remote_task_snapshot() -> EnvSnapshot:
        return snapshot_env()

    # Gather remote snapshot, applying runtime_env if available
    if runtime_env:
        _LOG.info("Comparing with Geneva context runtime_env: %s", runtime_env)
        remote: EnvSnapshot = ray.get(
            _remote_task_snapshot.options(runtime_env=runtime_env).remote()
        )
    else:
        _LOG.info("Comparing with base Ray worker environment (no manifest detected)")
        remote = ray.get(_remote_task_snapshot.remote())

    # Compute diffs
    env_diffs = diff_env(local["env"], remote["env"], env_prefix)
    pkg_diffs = diff_packages(local["packages"], remote["packages"])
    sys_path_diffs = diff_list("sys.path", local["sys_path"], remote["sys_path"])

    if ray.util.client.ray.is_connected():  # type: ignore[attr-defined]
        ray.util.client.ray.disconnect()  # type: ignore[attr-defined]

    return ComparisonResult(
        local=local,
        remote=remote,
        env_diffs=env_diffs,
        pkg_diffs=pkg_diffs,
        sys_path_diffs=sys_path_diffs,
    )


def compare_ray_environments(  # noqa: T201
    env_prefix: str | None = None,
    show_all: bool = False,
    include_sys_path: bool = True,
    auto_init: bool = False,
    ray_address: str | None = "auto",
    runtime_env: dict[str, Any] | None = None,
) -> ComparisonResult:
    """Compare and print Ray worker environment vs local environment.

    Prints a formatted report to console and returns the data. Use
    get_comparison_result() if you only want the data without printing.

    By default, requires Ray to already be initialized. Use auto_init=True
    to allow automatic Ray initialization.

    When called inside a Geneva context, the manifest's pip/conda
    dependencies are automatically applied to the remote snapshot task.

    Parameters
    ----------
    env_prefix
        Optional prefix to filter environment variables (e.g., 'PY').
    show_all
        If True, also print full snapshots as JSON.
    include_sys_path
        If True, include sys.path comparison.
    auto_init
        If True, initialize Ray automatically. If False (default),
        require Ray to already be initialized.
    ray_address
        Ray address (only used when auto_init=True). Default 'auto'
        connects to existing cluster. Use None to start a new local cluster.
    runtime_env
        Optional Ray runtime_env dict to apply to the remote snapshot task.
        If not provided, auto-detected from the active Geneva context's
        manifest (if any).

    Returns
    -------
    ComparisonResult
        Comparison results (same as get_comparison_result).

    Raises
    ------
    RuntimeError
        If Ray is not initialized and auto_init=False

    Examples
    --------
    In a Geneva context (Ray already initialized, manifest auto-detected):

        result = compare_ray_environments()

    With an explicit runtime_env override:

        result = compare_ray_environments(runtime_env={"pip": ["emoji==2.14.1"]})

    Auto-init and connect to existing cluster:

        result = compare_ray_environments(auto_init=True)

    Auto-init a new local cluster:

        result = compare_ray_environments(auto_init=True, ray_address=None)
    """
    result = get_comparison_result(env_prefix, auto_init, ray_address, runtime_env)

    # Print headline
    print_headline(result["local"], result["remote"])

    # Print ENV diffs
    print_env_diffs(result["env_diffs"])

    # Print package diffs
    print_pkg_diffs(result["pkg_diffs"])

    # Print sys.path diffs
    if include_sys_path:
        sp_diffs = result["sys_path_diffs"]
        pretty_section("sys.path differences")
        print(f"  Only in LOCAL ({len(sp_diffs['only_local'])}):")
        for p in sp_diffs["only_local"]:
            print(f"    + {p}")
        print(f"  Only in REMOTE ({len(sp_diffs['only_remote'])}):")
        for p in sp_diffs["only_remote"]:
            print(f"    + {p}")
        shared_msg = (
            f"  Shared entries: {sp_diffs['intersection_count']} "
            f"(local={sp_diffs['local_count']}, "
            f"remote={sp_diffs['remote_count']})"
        )
        print(shared_msg)

    # Print full snapshots if requested
    if show_all:
        pretty_section("FULL SNAPSHOT: LOCAL")
        print(json.dumps(result["local"], indent=2, sort_keys=True))
        pretty_section("FULL SNAPSHOT: REMOTE")
        print(json.dumps(result["remote"], indent=2, sort_keys=True))

    return result


def main() -> None:
    """Main entry point for CLI usage."""
    ap = argparse.ArgumentParser(description="Compare local env vs Ray worker env.")
    ap.add_argument(
        "--address",
        default="auto",
        help=(
            "Ray address. Default 'auto' connects to existing cluster. "
            "Use 'local' to start new local Ray cluster."
        ),
    )
    ap.add_argument(
        "--env-prefix",
        default=None,
        help="Only compare env vars starting with this prefix (e.g., 'PY').",
    )
    ap.add_argument(
        "--show-all",
        action="store_true",
        help="Print full snapshots (JSON) in addition to diffs.",
    )
    ap.add_argument(
        "--no-sys-path", action="store_true", help="Skip sys.path comparison."
    )
    ap.add_argument(
        "--no-auto-init",
        action="store_true",
        help="Require Ray to be already initialized (don't auto-init).",
    )
    args = ap.parse_args()

    # Handle special 'local' keyword to start new Ray cluster
    address = None if args.address == "local" else args.address

    try:
        compare_ray_environments(
            env_prefix=args.env_prefix,
            show_all=args.show_all,
            include_sys_path=not args.no_sys_path,
            auto_init=not args.no_auto_init,
            ray_address=address,
        )
    except (ImportError, RuntimeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)  # noqa: T201
        sys.exit(2)


if __name__ == "__main__":
    main()
