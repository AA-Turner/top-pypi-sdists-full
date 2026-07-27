"""Security auditing for SAGE-written code.

This module provides ambient security scanning that runs on every file
that SAGE writes or modifies.

Features:
- Pattern-based vulnerability detection (fallback)
- Integration with bandit (Python)
- Integration with semgrep (multi-language)
- OWASP Top 10 vulnerability patterns

P3 Items 115-118: Extract security auditing from main.py.
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

__all__ = [
    "SecurityAuditor",
    "SecurityFinding",
    "SecuritySeverity",
]


class SecuritySeverity:
    """Security severity levels."""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass
class SecurityFinding:
    """A security vulnerability finding."""

    severity: str  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    file: str
    line: int
    rule: str
    message: str
    cwe: str | None = None
    owasp: str | None = None  # OWASP Top 10 category

    def to_dict(self) -> dict:
        return {
            "severity": self.severity,
            "file": self.file,
            "line": self.line,
            "rule": self.rule,
            "message": self.message,
            "cwe": self.cwe,
            "owasp": self.owasp,
        }


class SecurityAuditor:
    """Ambient security scanning for SAGE-written code.

    Provides three layers of scanning:
    1. Pattern-based detection (always available)
    2. Bandit scanning (Python files, if installed)
    3. Semgrep scanning (multi-language, if installed)
    """

    # Common vulnerability patterns (fallback if no tools installed)
    # Format: (pattern, severity, cwe, message, owasp)
    PATTERNS: dict[str, tuple[str, str, str, str, str | None]] = {
        "hardcoded_secret": (
            r'(?:password|secret|api_key|apikey|token|auth)\s*=\s*["\'][^"\']{8,}["\']',
            SecuritySeverity.HIGH,
            "CWE-798",
            "Hardcoded credential detected",
            "A07:2021 Identification and Authentication Failures",
        ),
        "sql_injection": (
            r'(?:execute|cursor\.execute|raw)\s*\(\s*["\'].*%s.*["\']',
            SecuritySeverity.CRITICAL,
            "CWE-89",
            "Potential SQL injection (use parameterized queries)",
            "A03:2021 Injection",
        ),
        "command_injection": (
            r"(?:os\.system|subprocess\.call|subprocess\.run|eval|exec)\s*\([^)]*\+",
            SecuritySeverity.CRITICAL,
            "CWE-78",
            "Potential command injection",
            "A03:2021 Injection",
        ),
        "shell_true": (
            r"subprocess\.\w+\([^)]*shell\s*=\s*True",
            SecuritySeverity.HIGH,
            "CWE-78",
            "Avoid shell=True to prevent command injection",
            "A03:2021 Injection",
        ),
        "xss_vuln": (
            r"innerHTML\s*=|document\.write\s*\(|\.html\s*\([^)]*\+",
            SecuritySeverity.HIGH,
            "CWE-79",
            "Potential XSS vulnerability",
            "A03:2021 Injection",
        ),
        "path_traversal": (
            r"open\s*\([^)]*\.\.\/",
            SecuritySeverity.HIGH,
            "CWE-22",
            "Potential path traversal",
            "A01:2021 Broken Access Control",
        ),
        "weak_crypto": (
            r"(?:md5|sha1)\s*\(",
            SecuritySeverity.MEDIUM,
            "CWE-327",
            "Weak cryptographic algorithm (use SHA-256+)",
            "A02:2021 Cryptographic Failures",
        ),
        "debug_enabled": (
            r"(?:DEBUG\s*=\s*True|debug\s*=\s*true|app\.debug\s*=\s*True)",
            SecuritySeverity.LOW,
            "CWE-489",
            "Debug mode enabled in production code",
            "A05:2021 Security Misconfiguration",
        ),
        "private_key": (
            r"-----BEGIN (?:RSA |DSA |EC )?PRIVATE KEY-----",
            SecuritySeverity.CRITICAL,
            "CWE-321",
            "Private key in source code",
            "A02:2021 Cryptographic Failures",
        ),
        "aws_key": (
            r"(?:AKIA|ABIA|ACCA|ASIA)[A-Z0-9]{16}",
            SecuritySeverity.CRITICAL,
            "CWE-798",
            "AWS access key detected",
            "A07:2021 Identification and Authentication Failures",
        ),
        "jwt_secret": (
            r'(?:jwt[_-]?secret|JWT_SECRET)\s*=\s*["\'][^"\']+["\']',
            SecuritySeverity.HIGH,
            "CWE-798",
            "Hardcoded JWT secret",
            "A02:2021 Cryptographic Failures",
        ),
        "insecure_random": (
            r"(?:random\.random|Math\.random)\s*\(",
            SecuritySeverity.MEDIUM,
            "CWE-330",
            "Insecure random (use secrets module for security)",
            "A02:2021 Cryptographic Failures",
        ),
        "ssrf_url": (
            r"requests\.(?:get|post|put|delete)\s*\([^)]*\+",
            SecuritySeverity.MEDIUM,
            "CWE-918",
            "Potential SSRF (validate URLs)",
            "A10:2021 Server-Side Request Forgery",
        ),
        "unsafe_yaml": (
            r"yaml\.load\s*\([^)]*\)",
            SecuritySeverity.HIGH,
            "CWE-502",
            "Unsafe YAML load (use yaml.safe_load)",
            "A08:2021 Software and Data Integrity Failures",
        ),
        "pickle_load": (
            r"pickle\.load\s*\(",
            SecuritySeverity.HIGH,
            "CWE-502",
            "Unsafe pickle deserialization",
            "A08:2021 Software and Data Integrity Failures",
        ),
    }

    # File extensions for each scanner
    PYTHON_EXTENSIONS = {".py", ".pyw"}
    SEMGREP_EXTENSIONS = {
        ".py",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".go",
        ".java",
        ".rb",
        ".php",
        ".c",
        ".cpp",
        ".cs",
    }

    def __init__(self, cwd: Path):
        self.cwd = cwd
        self._has_bandit = self._check_tool("bandit")
        self._has_semgrep = self._check_tool("semgrep")

    def _check_tool(self, tool: str) -> bool:
        """Check if a security tool is installed."""
        try:
            result = subprocess.run(
                [tool, "--version"],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except Exception:
            return False

    @property
    def available_scanners(self) -> list[str]:
        """List available security scanners."""
        scanners = ["patterns"]
        if self._has_bandit:
            scanners.append("bandit")
        if self._has_semgrep:
            scanners.append("semgrep")
        return scanners

    def scan_file(self, filepath: str) -> list[SecurityFinding]:
        """Scan a single file for security issues.

        Args:
            filepath: Relative path to file from cwd

        Returns:
            List of security findings
        """
        findings: list[SecurityFinding] = []
        full_path = self.cwd / filepath

        if not full_path.exists():
            return findings

        suffix = full_path.suffix.lower()

        # Run bandit for Python files
        if suffix in self.PYTHON_EXTENSIONS and self._has_bandit:
            findings.extend(self._run_bandit(filepath))

        # Run semgrep for supported files
        if suffix in self.SEMGREP_EXTENSIONS and self._has_semgrep:
            findings.extend(self._run_semgrep(filepath))

        # Always run pattern-based detection as fallback/supplement
        findings.extend(self._pattern_scan(filepath))

        return self._deduplicate_findings(findings)

    def scan_files(self, filepaths: list[str]) -> list[SecurityFinding]:
        """Scan multiple files and return all findings.

        Args:
            filepaths: List of relative paths

        Returns:
            Sorted, deduplicated list of findings
        """
        all_findings = []
        for fp in filepaths:
            all_findings.extend(self.scan_file(fp))
        return self._deduplicate_findings(all_findings)

    def scan_content(self, content: str, filepath: str = "<inline>") -> list[SecurityFinding]:
        """Scan content string for security issues.

        Useful for scanning before writing a file.

        Args:
            content: File content to scan
            filepath: Filename for reporting

        Returns:
            List of security findings
        """
        findings: list[SecurityFinding] = []
        lines = content.split("\n")

        for name, (pattern, severity, cwe, message, owasp) in self.PATTERNS.items():
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append(
                        SecurityFinding(
                            severity=severity,
                            file=filepath,
                            line=i,
                            rule=f"sage/{name}",
                            message=message,
                            cwe=cwe,
                            owasp=owasp,
                        )
                    )

        return self._deduplicate_findings(findings)

    def _run_bandit(self, filepath: str) -> list[SecurityFinding]:
        """Run bandit on a Python file."""
        findings = []
        try:
            result = subprocess.run(
                ["bandit", "-f", "json", "-q", str(self.cwd / filepath)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.cwd,
            )
            if result.stdout:
                data = json.loads(result.stdout)
                for issue in data.get("results", []):
                    sev = issue.get("issue_severity", "MEDIUM").upper()
                    findings.append(
                        SecurityFinding(
                            severity=sev,
                            file=filepath,
                            line=issue.get("line_number", 0),
                            rule=f"bandit/{issue.get('test_id', '')}",
                            message=issue.get("issue_text", ""),
                            cwe=issue.get("issue_cwe", {}).get("id")
                            if isinstance(issue.get("issue_cwe"), dict)
                            else None,
                        )
                    )
        except Exception:
            pass
        return findings

    def _run_semgrep(self, filepath: str) -> list[SecurityFinding]:
        """Run semgrep on a file."""
        findings = []
        try:
            result = subprocess.run(
                ["semgrep", "--json", "--config", "auto", str(self.cwd / filepath)],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=self.cwd,
            )
            if result.stdout:
                data = json.loads(result.stdout)
                for issue in data.get("results", []):
                    sev = issue.get("extra", {}).get("severity", "WARNING").upper()
                    if sev == "WARNING":
                        sev = SecuritySeverity.MEDIUM
                    elif sev == "ERROR":
                        sev = SecuritySeverity.HIGH
                    findings.append(
                        SecurityFinding(
                            severity=sev,
                            file=filepath,
                            line=issue.get("start", {}).get("line", 0),
                            rule=f"semgrep/{issue.get('check_id', '')}",
                            message=issue.get("extra", {}).get("message", ""),
                            cwe=issue.get("extra", {}).get("metadata", {}).get("cwe"),
                            owasp=issue.get("extra", {}).get("metadata", {}).get("owasp"),
                        )
                    )
        except Exception:
            pass
        return findings

    def _pattern_scan(self, filepath: str) -> list[SecurityFinding]:
        """Fallback pattern-based scanning."""
        findings = []
        full_path = self.cwd / filepath

        try:
            content = full_path.read_text(encoding="utf-8", errors="ignore")
            lines = content.split("\n")

            for name, (pattern, severity, cwe, message, owasp) in self.PATTERNS.items():
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        findings.append(
                            SecurityFinding(
                                severity=severity,
                                file=filepath,
                                line=i,
                                rule=f"sage/{name}",
                                message=message,
                                cwe=cwe,
                                owasp=owasp,
                            )
                        )
        except Exception:
            pass

        return findings

    def _deduplicate_findings(self, findings: list[SecurityFinding]) -> list[SecurityFinding]:
        """Deduplicate findings by (file, line, rule) and sort by severity."""
        seen = set()
        unique = []
        for f in findings:
            key = (f.file, f.line, f.rule)
            if key not in seen:
                seen.add(key)
                unique.append(f)

        # Sort by severity
        severity_order = {
            SecuritySeverity.CRITICAL: 0,
            SecuritySeverity.HIGH: 1,
            SecuritySeverity.MEDIUM: 2,
            SecuritySeverity.LOW: 3,
            SecuritySeverity.INFO: 4,
        }
        return sorted(unique, key=lambda x: severity_order.get(x.severity, 5))

    def format_findings(self, findings: list[SecurityFinding]) -> str:
        """Format findings for display.

        Args:
            findings: List of findings to format

        Returns:
            Formatted string for display
        """
        if not findings:
            return "✅ No security issues found."

        severity_icons = {
            SecuritySeverity.CRITICAL: "🔴",
            SecuritySeverity.HIGH: "🟠",
            SecuritySeverity.MEDIUM: "🟡",
            SecuritySeverity.LOW: "🔵",
            SecuritySeverity.INFO: "⚪",
        }

        lines = ["🔒 Security Scan Results:"]
        for f in findings:
            icon = severity_icons.get(f.severity, "⚪")
            cwe_str = f" ({f.cwe})" if f.cwe else ""
            lines.append(f"  {icon} [{f.severity}] {f.file}:{f.line} — {f.message}{cwe_str}")

        return "\n".join(lines)

    def has_critical_findings(self, findings: list[SecurityFinding]) -> bool:
        """Check if there are any critical or high severity findings."""
        return any(
            f.severity in {SecuritySeverity.CRITICAL, SecuritySeverity.HIGH} for f in findings
        )

    def get_summary(self, findings: list[SecurityFinding]) -> dict:
        """Get a summary of findings by severity.

        Returns:
            Dict with counts per severity level
        """
        from collections import Counter

        counts = Counter(f.severity for f in findings)
        return {
            "total": len(findings),
            "critical": counts.get(SecuritySeverity.CRITICAL, 0),
            "high": counts.get(SecuritySeverity.HIGH, 0),
            "medium": counts.get(SecuritySeverity.MEDIUM, 0),
            "low": counts.get(SecuritySeverity.LOW, 0),
            "info": counts.get(SecuritySeverity.INFO, 0),
        }
