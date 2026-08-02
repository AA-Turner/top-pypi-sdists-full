"""Detect and install project dependencies for CI.

Usage:
    pysae-ai-tools ci prepare [--dir /path/to/project] [--deep]

Detects project type from marker files (.nvmrc, pyproject.toml, etc.)
and installs dependencies with the appropriate package manager.

With --deep, scans subdirectories for additional packages (monorepo support).
Stops descending into a directory once a marker is found (no nested detection).

Output (JSON, one line per action + final summary):
    {"action": "detect", "packages": [{"path": ".", ...}, {"path": "frontend", ...}]}
    {"action": "install", "path": ".", "tool": "uv", "status": "ok", "version": "..."}
    {"action": "done", "installed": [".:uv"], "failed": []}
"""

import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Annotated

import typer

# Directories to always skip during deep scan
_SKIP_DIRS = frozenset(
    {
        "node_modules",
        ".venv",
        "venv",
        "__pycache__",
        ".git",
        ".tox",
        "dist",
        "build",
        ".eggs",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
    }
)


class NodePackageManager(StrEnum):
    NPM = "npm"
    YARN = "yarn"
    PNPM = "pnpm"


class PythonPackageManager(StrEnum):
    UV = "uv"
    PIP = "pip"


@dataclass
class PackageDetection:
    """A single detected package within the project."""

    path: str
    has_node: bool = False
    node_pm: NodePackageManager | None = None
    nvmrc_version: str = ""
    has_python: bool = False
    python_pm: PythonPackageManager | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "path": self.path,
            "node": self.has_node,
            "python": self.has_python,
            "node_pm": str(self.node_pm) if self.node_pm else None,
            "python_pm": str(self.python_pm) if self.python_pm else None,
            "nvmrc_version": self.nvmrc_version or None,
        }


@dataclass
class InstallResult:
    path: str
    tool: str
    status: str
    version: str = ""
    error: str = ""

    def to_json(self) -> str:
        d: dict[str, str] = {"action": "install", "path": self.path, "tool": self.tool, "status": self.status}
        if self.version:
            d["version"] = self.version
        if self.error:
            d["error"] = self.error
        return json.dumps(d)


@dataclass
class PrepareReport:
    installed: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps({"action": "done", "installed": self.installed, "failed": self.failed})


def _run(cmd: str, cwd: str | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return the result."""
    merged_env = {**os.environ, **(env or {})}
    return subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=cwd,
        env=merged_env,
        timeout=300,
    )


def _detect_single(directory: Path) -> PackageDetection | None:
    """Detect project markers in a single directory. Returns None if nothing found."""
    detection = PackageDetection(path="")
    found = False

    # Node.js detection
    if (directory / ".nvmrc").exists():
        detection.has_node = True
        detection.nvmrc_version = (directory / ".nvmrc").read_text(encoding="utf-8").strip()
        found = True

        if (directory / "yarn.lock").exists():
            detection.node_pm = NodePackageManager.YARN
        elif (directory / "pnpm-lock.yaml").exists():
            detection.node_pm = NodePackageManager.PNPM
        elif (directory / "package-lock.json").exists():
            detection.node_pm = NodePackageManager.NPM
        elif (directory / "package.json").exists():
            detection.node_pm = NodePackageManager.NPM

    # Python detection
    pyproject = directory / "pyproject.toml"
    if pyproject.exists():
        content = pyproject.read_text(encoding="utf-8")
        detection.has_python = True
        found = True
        if (directory / "uv.lock").exists() or "[tool.uv]" in content:
            detection.python_pm = PythonPackageManager.UV
        elif "[project]" in content:
            detection.python_pm = PythonPackageManager.PIP

    return detection if found else None


def detect(project_dir: str, deep: bool = False) -> list[PackageDetection]:
    """Detect project types from marker files.

    With deep=False, only checks the root directory.
    With deep=True, scans subdirectories (max 3 levels deep).
    Stops descending into a directory once a marker is found.
    """
    root = Path(project_dir)
    packages: list[PackageDetection] = []

    # Always check root
    root_detection = _detect_single(root)
    if root_detection:
        root_detection.path = "."
        packages.append(root_detection)

    if not deep:
        return packages

    # Deep scan -- BFS with max depth 3, skip dirs with markers (already detected)
    dirs_with_markers = {root} if root_detection else set[Path]()

    def _scan(directory: Path, depth: int) -> None:
        if depth > 3:
            return
        try:
            entries = sorted(directory.iterdir())
        except PermissionError:
            return
        for entry in entries:
            if not entry.is_dir():
                continue
            if entry.name in _SKIP_DIRS or entry.name.startswith("."):
                continue

            detection = _detect_single(entry)
            if detection:
                detection.path = str(entry.relative_to(root))
                packages.append(detection)
                dirs_with_markers.add(entry)
                # Don't descend further -- this dir is a package root
            else:
                _scan(entry, depth + 1)

    _scan(root, 1)
    return packages


def install_node(detection: PackageDetection, project_dir: str) -> list[InstallResult]:
    """Install Node.js via nvm and packages via the detected package manager."""
    pkg_dir = str(Path(project_dir) / detection.path)
    results: list[InstallResult] = []

    nvm_script = 'export NVM_DIR="${NVM_DIR:-$HOME/.nvm}" && [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"'
    r = _run(f"{nvm_script} && nvm install && nvm use && node --version", cwd=pkg_dir)
    if r.returncode == 0:
        version = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
        results.append(InstallResult(path=detection.path, tool="nvm", status="ok", version=version))
    else:
        results.append(InstallResult(path=detection.path, tool="nvm", status="failed", error=r.stderr.strip()[:200]))
        return results

    pm = detection.node_pm
    if pm == NodePackageManager.NPM:
        cmd = f"{nvm_script} && npm ci"
    elif pm == NodePackageManager.YARN:
        cmd = f"{nvm_script} && corepack enable && yarn install --frozen-lockfile"
    elif pm == NodePackageManager.PNPM:
        cmd = f"{nvm_script} && corepack enable && pnpm install --frozen-lockfile"
    else:
        return results

    r = _run(cmd, cwd=pkg_dir)
    tool_name = str(pm) if pm else "npm"
    if r.returncode == 0:
        results.append(InstallResult(path=detection.path, tool=tool_name, status="ok"))
    else:
        results.append(
            InstallResult(path=detection.path, tool=tool_name, status="failed", error=r.stderr.strip()[:200])
        )

    return results


def install_python(detection: PackageDetection, project_dir: str) -> list[InstallResult]:
    """Install Python dependencies via the detected package manager."""
    pkg_dir = str(Path(project_dir) / detection.path)
    results: list[InstallResult] = []

    pm = detection.python_pm
    if pm == PythonPackageManager.UV:
        cmd = "uv sync --frozen" if (Path(pkg_dir) / "uv.lock").exists() else "uv sync"
        r = _run(cmd, cwd=pkg_dir)
        if r.returncode == 0:
            version_r = _run("uv run python --version", cwd=pkg_dir)
            version = version_r.stdout.strip() if version_r.returncode == 0 else ""
            results.append(InstallResult(path=detection.path, tool="uv", status="ok", version=version))
        else:
            results.append(InstallResult(path=detection.path, tool="uv", status="failed", error=r.stderr.strip()[:200]))

    elif pm == PythonPackageManager.PIP:
        r = _run("pip install -e .", cwd=pkg_dir)
        if r.returncode == 0:
            version_r = _run("python --version", cwd=pkg_dir)
            version = version_r.stdout.strip() if version_r.returncode == 0 else ""
            results.append(InstallResult(path=detection.path, tool="pip", status="ok", version=version))
        else:
            results.append(
                InstallResult(path=detection.path, tool="pip", status="failed", error=r.stderr.strip()[:200])
            )

    return results


def prepare(project_dir: str, deep: bool = False, json_output: bool = False) -> PrepareReport:
    """Detect and install all dependencies for a project."""
    packages = detect(project_dir, deep=deep)
    if json_output:
        print(json.dumps({"action": "detect", "packages": [p.to_dict() for p in packages]}))

    report = PrepareReport()

    if not packages:
        if json_output:
            print(json.dumps({"action": "skip", "reason": "No .nvmrc or pyproject.toml found"}))
        else:
            print("  - No dependencies to install")
        return report

    for pkg in packages:
        if pkg.has_node:
            for result in install_node(pkg, project_dir):
                label = f"{pkg.path}:{result.tool}"
                if json_output:
                    print(result.to_json())
                elif result.status == "ok":
                    version = f" ({result.version})" if result.version else ""
                    print(f"  + {label}{version}")
                else:
                    print(f"  x {label}: {result.error}")
                if result.status == "ok":
                    report.installed.append(label)
                else:
                    report.failed.append(label)

        if pkg.has_python:
            for result in install_python(pkg, project_dir):
                label = f"{pkg.path}:{result.tool}"
                if json_output:
                    print(result.to_json())
                elif result.status == "ok":
                    version = f" ({result.version})" if result.version else ""
                    print(f"  + {label}{version}")
                else:
                    print(f"  x {label}: {result.error}")
                if result.status == "ok":
                    report.installed.append(label)
                else:
                    report.failed.append(label)

    if json_output:
        print(report.to_json())
    return report


cli = typer.Typer()


@cli.command()
def main(
    dir: Annotated[
        str,
        typer.Option("--dir", help="Project directory (default: current directory)"),
    ] = ".",
    deep: Annotated[
        bool,
        typer.Option("--deep", help="Scan subdirectories for monorepo packages (max 3 levels)"),
    ] = False,
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Output JSON lines (default: human-readable)"),
    ] = False,
) -> None:
    """Install project dependencies (Node.js via nvm, Python via uv/pip)."""
    project_dir = os.path.abspath(dir)
    report = prepare(project_dir, deep=deep, json_output=json_output)

    if report.failed:
        sys.exit(1)


if __name__ == "__main__":
    cli()
