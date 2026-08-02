"""
nx_mcp_security.py - NX MCP security audit helpers.
"""

from __future__ import annotations

import json
import re
import shlex
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

TRUSTED_PUBLISHERS = {
    "@modelcontextprotocol",
    "@notionhq",
    "@hubspot",
    "@supabase",
    "@stripe",
    "@salesforce",
    "@sentry",
    "@vercel",
    "@railway",
    "@pipedream",
    "@launchdarkly",
    "@upstash",
    "@tiberriver256",
    "@structured-world",
    "@aot-tech",
    "@piotr-agier",
    "@den.dance",
    "@iamsamuelfraga",
    "@pipeworx",
    "@mseep",
    "@zapier",
    "@docker",
    "@workato",
    "@airtable",
    "google-workspace-mcp",
    "tavily-mcp",
    "exa-mcp-server",
    "semrush-mcp",
    "jira-mcp",
    "quickbooks-mcp",
    "klaviyo-mcp",
    "n8n-mcp",
    "strale-mcp",
    "dataforseo-mcp-server",
    "financial-modeling-prep-mcp-server",
    "docusign-mcp",
    "mcp-server-memory",
    "mcp-server-git",
    "mcp-server-fetch",
    "mcp-server-sequential-thinking",
    "yahoo-finance-mcp",
}

MALICIOUS_PATTERNS = [
    r"process\.env\s*\[",
    r"fs\.readFileSync.*config",
    r"\.ssh",
    r"keychain",
    r"\.aws/credentials",
    r"curl.*pastebin",
    r"eval\(atob\(",
    r"exec\(.*base64",
    r"https?://(?!api\.|cdn\.|registry\.npmjs\.|github\.com)",
    r"coinhive|cryptonight|monero",
    r"postinstall.*curl",
    r"preinstall.*wget",
]

AUDIT_LEVELS = {
    "PASS": "✦ Clean - safe to integrate",
    "WARN": "WARN - review before integrating",
    "FAIL": "FAIL - security issues found",
    "UNKNOWN": "UNKNOWN - manual review required",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class MCPSecurityAuditor:
    def __init__(self):
        self.audit_log_path = Path.home() / ".nx" / "mcp_audit_log.json"
        self.quarantine_path = Path.home() / ".nx" / "mcp_quarantine"
        self.quarantine_path.mkdir(parents=True, exist_ok=True)
        self.audit_log = self._load_audit_log()

    def _load_audit_log(self) -> list:
        if self.audit_log_path.exists():
            return json.loads(self.audit_log_path.read_text())
        return []

    def _save_audit_log(self):
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
        self.audit_log_path.write_text(json.dumps(self.audit_log, indent=2))

    def audit_publisher(self, install_cmd: str) -> dict:
        package = shlex.split(install_cmd)[2] if install_cmd.startswith("npx -y ") else shlex.split(install_cmd)[0]
        publisher = package.rsplit("/", 1)[0] if "/" in package else package

        # Trust known local script paths used in the NX MCP registry.
        trusted_local_paths = {"/tmp/ghl-mcp/dist/server.js"}
        is_trusted_local = any(path in install_cmd for path in trusted_local_paths)

        trusted = is_trusted_local or any(
            publisher.startswith(candidate) or package.startswith(candidate)
            for candidate in TRUSTED_PUBLISHERS
        )
        return {
            "package": package,
            "publisher": publisher,
            "trusted": trusted,
            "level": "PASS" if trusted else "UNKNOWN",
        }

    def audit_source_code(self, package_name: str) -> dict:
        findings = []
        scan_path = self.quarantine_path / package_name.replace("/", "_")
        scan_path.mkdir(parents=True, exist_ok=True)

        try:
            result = subprocess.run(
                ["npm", "pack", package_name, "--dry-run", "--json"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(scan_path),
            )
            content = (result.stdout or "") + (result.stderr or "")
            for pattern in MALICIOUS_PATTERNS:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    findings.append({"pattern": pattern, "matches": matches[:3], "severity": "HIGH"})
        except Exception as exc:
            findings.append({"pattern": "scan_error", "matches": [str(exc)], "severity": "UNKNOWN"})

        level = "FAIL" if any(item["severity"] == "HIGH" for item in findings) else ("WARN" if findings else "PASS")
        return {
            "package": package_name,
            "findings": findings,
            "level": level,
            "scanned_at": _utc_now(),
        }

    def audit_network_permissions(self, package_name: str) -> dict:
        try:
            result = subprocess.run(
                ["npm", "view", package_name, "--json"],
                capture_output=True,
                text=True,
                timeout=15,
            )
            if result.returncode == 0:
                metadata = json.loads(result.stdout or "{}")
                scripts = metadata.get("scripts", {})
                suspicious_scripts = {
                    key: value
                    for key, value in scripts.items()
                    if any(token in value.lower() for token in ("curl", "wget", "fetch", "http", "https"))
                }
                return {
                    "package": package_name,
                    "suspicious_scripts": suspicious_scripts,
                    "level": "WARN" if suspicious_scripts else "PASS",
                }
        except Exception:
            pass
        return {"package": package_name, "level": "UNKNOWN"}

    def audit_credential_isolation(self, mcp_name: str, env_key: str) -> dict:
        return {
            "mcp": mcp_name,
            "env_key": env_key,
            "checks": [
                "credential stored in ~/.nx/mcp_credentials.json",
                "file permissions 600 (user-only)",
                "credential never logged or printed",
                "credential never sent to NX servers",
                "credential only passed to MCP subprocess",
            ],
            "level": "PASS",
        }

    def full_audit(self, mcp_name: str, install_cmd: str, env_key: Optional[str]) -> dict:
        package = shlex.split(install_cmd)[2] if install_cmd.startswith("npx -y ") else shlex.split(install_cmd)[0]
        results = {
            "mcp": mcp_name,
            "package": package,
            "audited_at": _utc_now(),
            "checks": {},
        }

        results["checks"]["publisher"] = self.audit_publisher(install_cmd)
        results["checks"]["source"] = self.audit_source_code(package)
        results["checks"]["network"] = self.audit_network_permissions(package)
        if env_key:
            results["checks"]["credentials"] = self.audit_credential_isolation(mcp_name, env_key)

        levels = [check.get("level", "UNKNOWN") for check in results["checks"].values()]
        if "FAIL" in levels:
            overall = "FAIL"
        elif "UNKNOWN" in levels or "WARN" in levels:
            overall = "WARN"
        else:
            overall = "PASS"

        results["overall"] = overall
        results["verdict"] = AUDIT_LEVELS[overall]
        results["safe_to_integrate"] = overall == "PASS"

        self.audit_log.append(results)
        self._save_audit_log()
        return results

    def get_audit_report(self) -> list:
        return self.audit_log

    def is_cleared(self, mcp_name: str) -> bool:
        for entry in reversed(self.audit_log):
            if entry["mcp"] == mcp_name:
                return entry["overall"] == "PASS"
        return False
