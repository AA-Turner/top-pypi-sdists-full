import json
import subprocess
import sys
from typing import Dict, List, Optional, Sequence

from packaging.version import Version

from abstra_internals.repositories.linter.models import (
    LinterFix,
    LinterIssue,
    LinterRule,
)
from abstra_internals.services.requirements import RequirementsRepository
from abstra_internals.settings import Settings


class UpgradePackage(LinterFix):
    def __init__(self, package_name: str, fix_version: str) -> None:
        self.package_name = package_name
        self.fix_version = fix_version
        self.label = f"Update {package_name} to {fix_version}"

    @property
    def name(self) -> str:
        return f"UpgradePackage:{self.package_name}"

    def fix(self):
        requirements = RequirementsRepository.load()
        requirements.ensure(self.package_name, self.fix_version)
        RequirementsRepository.save(requirements)

        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                f"{self.package_name}=={self.fix_version}",
            ],
            check=False,
        )


class VulnerableDependencyFound(LinterIssue):
    def __init__(
        self,
        package_name: str,
        version: str,
        vuln_ids: List[str],
        fix_version: str,
        descriptions: List[str],
    ) -> None:
        ids = ", ".join(vuln_ids)
        if fix_version:
            self.label = (
                f"{package_name}=={version} has {len(vuln_ids)} "
                f"{'vulnerability' if len(vuln_ids) == 1 else 'vulnerabilities'}: "
                f"{ids}. Update to {fix_version} to fix the vulnerability."
            )
            self.fixes = [UpgradePackage(package_name, fix_version)]
        else:
            descs = (
                "\n".join(
                    f"- {vid}: {d}" for vid, d in zip(vuln_ids, descriptions) if d
                )
                if descriptions
                else ""
            )
            vuln_count = len(vuln_ids)
            vuln_word = "vulnerability" if vuln_count == 1 else "vulnerabilities"
            no_fix_hint = (
                "No fix is available in another version. "
                "We suggest you to remove this dependency and adapt your code accordingly."
            )
            summary = (
                f"{package_name}=={version} has {vuln_count} "
                f"{vuln_word}: {ids}. {no_fix_hint}"
            )
            self.label = f"{summary}\n{descs}" if descs else summary
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
    """Parse pip-audit JSON, grouping vulnerabilities per package."""
    if not stdout.strip():
        return []

    try:
        report = json.loads(stdout)
    except json.JSONDecodeError:
        return []

    # Group by package: {name: {version, vuln_ids, fix_versions, descriptions}}
    grouped: Dict[str, Dict] = {}
    for dep in report.get("dependencies", []):
        name = dep.get("name")
        version = dep.get("version")
        if not name or not version:
            continue

        if name not in grouped:
            grouped[name] = {
                "version": version,
                "vuln_ids": [],
                "fix_versions": [],
                "descriptions": [],
            }

        for vuln in dep.get("vulns", []):
            vuln_id = vuln.get("id", "")
            if vuln_id:
                grouped[name]["vuln_ids"].append(vuln_id)

            description = vuln.get("description", "")
            if description:
                grouped[name]["descriptions"].append(description)

            for fv in vuln.get("fix_versions", []):
                if fv:
                    grouped[name]["fix_versions"].append(fv)

    issues: List[LinterIssue] = []
    for name, info in grouped.items():
        if not info["vuln_ids"]:
            continue

        best_fix = _highest_version(info["fix_versions"])

        issues.append(
            VulnerableDependencyFound(
                package_name=name,
                version=info["version"],
                vuln_ids=info["vuln_ids"],
                fix_version=best_fix,
                descriptions=info["descriptions"],
            )
        )

    return issues


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
    """Scans requirements.txt for known CVEs — blocks deploy."""

    label = "Vulnerable dependencies in requirements.txt"
    type = "security"
    fix_with_ai = True

    def find_issues(self) -> Sequence[LinterIssue]:
        requirements_path = Settings.root_path / "requirements.txt"
        if not requirements_path.exists():
            return []

        return _run_pip_audit(["-r", str(requirements_path)])
