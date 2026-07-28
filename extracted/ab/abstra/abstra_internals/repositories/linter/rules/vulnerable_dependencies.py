"""Vulnerable dependencies linter — currently DISABLED.

This rule shells out to `pip-audit` to scan requirements.txt for CVEs. In the
web-editor pod the subprocess consistently hits the 60s timeout (likely due to
egress constraints on the pip-as-subprocess network calls), returns silently
with no findings, and costs the user a full minute per requirements.txt save.

Until that's investigated and fixed, the rule is unregistered from
`rules/__init__.py` (no import, no instance, not in any group), so it never
runs. The class below stays in the codebase for reference and so the
investigation can resume from here."""

import json
import subprocess
import sys
from typing import Dict, List, Optional, Sequence, Tuple

from packaging.version import Version

from abstra_internals.repositories.linter.models import (
    LinterFix,
    LinterIssue,
    LinterRule,
)
from abstra_internals.services.requirements import RequirementsRepository
from abstra_internals.settings import Settings


class UpgradeAllPackages(LinterFix):
    def __init__(self, packages: List[Tuple[str, str]]) -> None:
        self.packages = packages
        self.label = "Update all packages"

    @property
    def name(self) -> str:
        return "UpgradeAllPackages"

    def fix(self):
        requirements = RequirementsRepository.load()
        for package_name, fix_version in self.packages:
            requirements.ensure(package_name, fix_version)
        RequirementsRepository.save(requirements)

        for package_name, fix_version in self.packages:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    f"{package_name}=={fix_version}",
                ],
                check=False,
            )


class VulnerableDependenciesFound(LinterIssue):
    title = "Vulnerable dependencies in requirements.txt"
    type = "warning"

    def __init__(
        self,
        fixable: List[Tuple[str, str, str]],
        unfixable: List[Tuple[str, str]],
    ) -> None:
        total = len(fixable) + len(unfixable)
        summary = (
            f"{total} {'dependency has' if total == 1 else 'dependencies have'}"
            " security updates available"
        )

        details: List[str] = []
        for name, version, fix_version in fixable:
            details.append(f"- {name} {version} → {fix_version}")
        for name, version in unfixable:
            details.append(
                f"- {name} {version} (no update available, consider removing)"
            )

        self.label = "\n".join([summary] + details)

        if fixable:
            self.fixes = [UpgradeAllPackages([(name, fv) for name, _, fv in fixable])]
        else:
            self.fixes = []


def _highest_version(versions: List[str]) -> str:
    """Return the highest version string from a list."""
    parsed = []
    for v in versions:
        try:
            parsed.append(Version(v))
        except Exception:
            continue
    if not parsed:
        return ""
    return str(max(parsed))


def _parse_findings(stdout: str) -> List[LinterIssue]:
    """Parse pip-audit JSON into a single grouped issue."""
    if not stdout.strip():
        return []

    try:
        report = json.loads(stdout)
    except json.JSONDecodeError:
        return []

    grouped: Dict[str, Dict] = {}
    for dep in report.get("dependencies", []):
        name = dep.get("name")
        version = dep.get("version")
        vulns = dep.get("vulns", [])
        if not name or not version or not vulns:
            continue

        if name not in grouped:
            grouped[name] = {
                "version": version,
                "fix_versions": [],
            }

        for vuln in vulns:
            for fv in vuln.get("fix_versions", []):
                if fv:
                    grouped[name]["fix_versions"].append(fv)

    fixable: List[Tuple[str, str, str]] = []
    unfixable: List[Tuple[str, str]] = []

    for name, info in grouped.items():
        best_fix = _highest_version(info["fix_versions"])
        if best_fix:
            fixable.append((name, info["version"], best_fix))
        else:
            unfixable.append((name, info["version"]))

    if not fixable and not unfixable:
        return []

    return [VulnerableDependenciesFound(fixable=fixable, unfixable=unfixable)]


def _run_pip_audit(extra_args: Optional[List[str]] = None) -> List[LinterIssue]:
    """Run pip-audit and return parsed issues."""
    cache_dir = str(Settings.root_path / ".abstra" / "pip_audit_cache")
    cmd = [
        sys.executable,
        "-m",
        "pip_audit",
        "-f",
        "json",
        "--progress-spinner=off",
        "--cache-dir",
        cache_dir,
    ]
    if extra_args:
        cmd.extend(extra_args)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        return []

    if result.returncode not in (0, 1):
        return []

    return _parse_findings(result.stdout)


class VulnerableRequirements(LinterRule):
    """Scans requirements.txt for known CVEs."""

    label = "Vulnerable dependencies in requirements.txt"

    def find_issues(self) -> Sequence[LinterIssue]:
        requirements_path = Settings.root_path / "requirements.txt"
        if not requirements_path.exists():
            return []

        return _run_pip_audit(["-r", str(requirements_path)])
