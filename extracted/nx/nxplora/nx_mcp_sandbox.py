"""
nx_mcp_sandbox.py - NX MCP sandbox state and isolation helpers.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

SANDBOX_ROOT = Path.home() / ".nx" / "mcp_sandbox"
CLEARED_PATH = Path.home() / ".nx" / "mcp_cleared.json"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_cleared() -> dict:
    if CLEARED_PATH.exists():
        return json.loads(CLEARED_PATH.read_text())
    return {}


def save_cleared(cleared: dict):
    CLEARED_PATH.parent.mkdir(parents=True, exist_ok=True)
    CLEARED_PATH.write_text(json.dumps(cleared, indent=2))


def sandbox_clone(repo_url: str, mcp_name: str) -> dict:
    """
    Clone an MCP repo into the NX sandbox without installing dependencies.
    """
    sandbox_path = SANDBOX_ROOT / mcp_name
    SANDBOX_ROOT.mkdir(parents=True, exist_ok=True)

    if sandbox_path.exists():
        shutil.rmtree(sandbox_path)

    try:
        result = subprocess.run(
            ["git", "clone", "--depth=1", repo_url, str(sandbox_path)],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except Exception as exc:
        return {"success": False, "error": str(exc), "mcp": mcp_name}

    if result.returncode != 0:
        return {"success": False, "error": result.stderr.strip(), "mcp": mcp_name}

    return {
        "success": True,
        "path": str(sandbox_path),
        "mcp": mcp_name,
        "cloned_at": _utc_now(),
    }


def sandbox_test(mcp_name: str, test_credential: str = "TEST_KEY") -> dict:
    """
    Perform a static sandbox review against a cloned MCP project.
    """
    sandbox_path = SANDBOX_ROOT / mcp_name
    if not sandbox_path.exists():
        return {
            "success": False,
            "error": f"Sandbox not found for {mcp_name}. Run sandbox_clone first.",
        }

    results = {
        "mcp": mcp_name,
        "tested_at": _utc_now(),
        "credential_used": test_credential,
        "checks": {},
    }

    pkg_path = sandbox_path / "package.json"
    if pkg_path.exists():
        pkg = json.loads(pkg_path.read_text())
        scripts = pkg.get("scripts", {})
        suspicious = {
            key: value
            for key, value in scripts.items()
            if any(token in value.lower() for token in ("curl", "wget", "eval", "base64", "exec"))
        }
        results["checks"]["scripts"] = {
            "suspicious": suspicious,
            "level": "FAIL" if suspicious else "PASS",
        }

    pkg_lock = sandbox_path / "package-lock.json"
    if pkg_lock.exists():
        lock_content = pkg_lock.read_text()
        known_malicious = ["event-stream", "flatmap-stream", "ua-parser-js", "coa", "rc"]
        found_malicious = [name for name in known_malicious if name in lock_content]
        results["checks"]["dependencies"] = {
            "malicious_found": found_malicious,
            "level": "FAIL" if found_malicious else "PASS",
        }

    env_access_patterns = []
    for src_file in list(sandbox_path.rglob("*.js"))[:50] + list(sandbox_path.rglob("*.ts"))[:50]:
        try:
            content = src_file.read_text(errors="ignore")
        except Exception:
            continue
        accesses = content.count("process.env")
        if accesses > 10:
            env_access_patterns.append({"file": src_file.name, "accesses": accesses})

    results["checks"]["env_access"] = {
        "patterns": env_access_patterns,
        "level": "WARN" if env_access_patterns else "PASS",
    }

    levels = [check.get("level", "UNKNOWN") for check in results["checks"].values()]
    if "FAIL" in levels:
        results["overall"] = "FAIL"
        results["safe_to_integrate"] = False
    elif "WARN" in levels:
        results["overall"] = "WARN"
        results["safe_to_integrate"] = False
    else:
        results["overall"] = "PASS"
        results["safe_to_integrate"] = True

    results["success"] = True
    return results


def mark_cleared(mcp_name: str, audit_results: dict):
    cleared = load_cleared()
    cleared[mcp_name] = {
        "cleared_at": _utc_now(),
        "overall": audit_results.get("overall"),
        "safe_to_integrate": audit_results.get("safe_to_integrate", False),
    }
    save_cleared(cleared)


def is_cleared(mcp_name: str) -> bool:
    cleared = load_cleared()
    return cleared.get(mcp_name, {}).get("safe_to_integrate", False)


def integrate_cleared(mcp_name: str) -> dict:
    if not is_cleared(mcp_name):
        return {
            "success": False,
            "error": f"{mcp_name} has not passed security audit. Run audit first.",
        }

    sandbox_path = SANDBOX_ROOT / mcp_name
    if not sandbox_path.exists():
        return {"success": False, "error": f"Sandbox path not found for {mcp_name}"}

    return {
        "success": True,
        "mcp": mcp_name,
        "status": "cleared_for_integration",
        "message": f"{mcp_name} passed security audit and is ready for production use",
    }
