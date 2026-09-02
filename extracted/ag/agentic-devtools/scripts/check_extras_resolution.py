#!/usr/bin/env python3
"""Verify that every declared extra in ``pyproject.toml`` resolves sanely.

For each entry under ``[project.optional-dependencies]`` this script uses
``uv pip install --dry-run`` to resolve the base package and the package with
the extra enabled (against an empty, throwaway virtual environment so the
resolution is not skewed by whatever happens to already be installed), then
compares the resolved package versions. If installing an extra would
*downgrade* any package relative to the base resolution, that is a strong
signal of an incoherent dependency bound (see
https://github.com/swai-factory/agentic-devtools/issues/3842), and the script
exits non-zero.

This script exits with status 0 when every extra resolves without regressing
the base resolution, or 1 when any extra downgrades a package.
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import venv
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover - exercised only on Python 3.10
    import tomli as tomllib

# Matches a single resolved-package line from `uv pip install --dry-run`, e.g.
# " + langgraph==1.2.11" or " + agentic-devtools @ file:///..." (no version).
_RESOLVED_LINE_RE = re.compile(r"^\s*\+\s+(?P<name>[A-Za-z0-9_.\-]+)(?:==(?P<version>\S+))?")


def get_declared_extras() -> list[str]:
    """Return the extra names declared under ``[project.optional-dependencies]``."""
    pyproject = REPO_ROOT / "pyproject.toml"
    with pyproject.open("rb") as handle:
        data = tomllib.load(handle)
    extras = data.get("project", {}).get("optional-dependencies", {})
    if not isinstance(extras, dict):
        raise RuntimeError("Expected [project.optional-dependencies] to be a table")
    return sorted(extras)


def resolve_dry_run(requirement: str, python_executable: str) -> dict[str, str]:
    """Return the {package_name: version} mapping ``uv`` would install for ``requirement``."""
    result = subprocess.run(  # noqa: S603
        ["uv", "pip", "install", "--python", python_executable, "--dry-run", requirement],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"uv pip install --dry-run {requirement!r} failed (exit {result.returncode}):\n"
            f"{result.stdout}\n{result.stderr}"
        )
    combined_output = result.stderr + result.stdout
    packages = _parse_resolved_versions(combined_output)
    if not packages:
        raise RuntimeError(
            f"uv pip install --dry-run {requirement!r} produced output but no packages could be "
            f"parsed — the output format may have changed.\nCaptured output:\n{combined_output}"
        )
    return packages


def _parse_resolved_versions(output: str) -> dict[str, str]:
    """Parse ``uv``'s ``+ name==version`` lines into a {name: version} mapping."""
    packages: dict[str, str] = {}
    for line in output.splitlines():
        match = _RESOLVED_LINE_RE.match(line)
        if match is None or match.group("version") is None:
            continue
        packages[match.group("name").lower()] = match.group("version")
    return packages


def find_regressions(base: dict[str, str], with_extra: dict[str, str]) -> list[str]:
    """Return messages describing packages that resolve lower with the extra than without it."""
    from packaging.version import InvalidVersion, Version

    regressions: list[str] = []
    for name, base_version in base.items():
        extra_version = with_extra.get(name)
        if extra_version is None:
            continue
        try:
            if Version(extra_version) < Version(base_version):
                regressions.append(f"{name}: base resolves to {base_version}, extra downgrades to {extra_version}")
        except InvalidVersion:
            continue
    return regressions


def main() -> int:
    extras = get_declared_extras()
    if not extras:
        print("No extras declared under [project.optional-dependencies]; nothing to check.")
        return 0

    with tempfile.TemporaryDirectory(prefix="agdt-extras-check-") as tmp_dir:
        venv_dir = Path(tmp_dir) / "venv"
        venv.create(venv_dir, with_pip=False)
        if sys.platform == "win32":
            python_executable = str(venv_dir / "Scripts" / "python.exe")
        else:
            python_executable = str(venv_dir / "bin" / "python")

        print(f"Resolving base install for {REPO_ROOT}...")
        base = resolve_dry_run(".", python_executable)

        failures: list[str] = []
        for extra in extras:
            print(f"Resolving extra '{extra}'...")
            with_extra = resolve_dry_run(f".[{extra}]", python_executable)
            regressions = find_regressions(base, with_extra)
            if regressions:
                failures.append(f"Extra '{extra}' regresses the base resolution:\n  " + "\n  ".join(regressions))

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1

    print("All declared extras resolve without regressing the base install.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
