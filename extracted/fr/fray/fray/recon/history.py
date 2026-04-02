"""Recon history — save, load, diff, and print comparison of recon results."""

import json
import re
from typing import Any, Dict, Optional


_RECON_HISTORY_DIR = None


def _get_history_dir():
    """Return ~/.fray/recon/ directory, creating if needed."""
    global _RECON_HISTORY_DIR
    if _RECON_HISTORY_DIR is None:
        from pathlib import Path
        d = Path.home() / ".fray" / "recon"
        d.mkdir(parents=True, exist_ok=True)
        _RECON_HISTORY_DIR = d
    return _RECON_HISTORY_DIR


def _save_recon_history(result: Dict[str, Any]) -> None:
    """Save recon result to ~/.fray/recon/<host>_<timestamp>.json."""
    try:
        host = result.get("host", "unknown")
        ts = result.get("timestamp", "").replace(":", "-").replace("+", "p")
        safe_host = re.sub(r'[^\w.-]', '_', host)
        path = _get_history_dir() / f"{safe_host}_{ts}.json"
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        # Also save as "latest" symlink-style file for quick --compare last
        latest = _get_history_dir() / f"{safe_host}_latest.json"
        latest.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def _load_previous_recon(host: str) -> Optional[Dict[str, Any]]:
    """Load the most recent previous recon for a host."""
    try:
        safe_host = re.sub(r'[^\w.-]', '_', host)
        latest = _get_history_dir() / f"{safe_host}_latest.json"
        if latest.exists():
            return json.loads(latest.read_text(encoding="utf-8"))
    except Exception:
        pass
    return None


def diff_recon(current: Dict[str, Any], previous: Dict[str, Any]) -> Dict[str, Any]:
    """Compare two recon results and produce a structured diff.

    Returns a dict with 'changes' (list of diffs) and 'summary' (counts).
    """
    changes = []

    def _diff_field(label, cur_val, prev_val, severity="info"):
        if cur_val != prev_val:
            changes.append({"field": label, "old": prev_val, "new": cur_val, "severity": severity})

    # Risk score
    cur_atk = current.get("attack_surface", {})
    prev_atk = previous.get("attack_surface", {})
    _diff_field("risk_score", cur_atk.get("risk_score", 0), prev_atk.get("risk_score", 0),
                severity="high" if cur_atk.get("risk_score", 0) > prev_atk.get("risk_score", 0) else "info")
    _diff_field("risk_level", cur_atk.get("risk_level"), prev_atk.get("risk_level"))

    # Technologies
    cur_techs = set(current.get("fingerprint", {}).get("technologies", {}).keys())
    prev_techs = set(previous.get("fingerprint", {}).get("technologies", {}).keys())
    new_techs = cur_techs - prev_techs
    removed_techs = prev_techs - cur_techs
    if new_techs:
        changes.append({"field": "technologies_added", "old": None, "new": sorted(new_techs), "severity": "info"})
    if removed_techs:
        changes.append({"field": "technologies_removed", "old": sorted(removed_techs), "new": None, "severity": "info"})

    # Subdomains
    cur_subs = set(current.get("subdomains", {}).get("subdomains", []))
    prev_subs = set(previous.get("subdomains", {}).get("subdomains", []))
    new_subs = cur_subs - prev_subs
    removed_subs = prev_subs - cur_subs
    if new_subs:
        changes.append({"field": "subdomains_added", "old": None, "new": sorted(new_subs)[:20], "severity": "medium"})
    if removed_subs:
        changes.append({"field": "subdomains_removed", "old": sorted(removed_subs)[:20], "new": None, "severity": "info"})

    # Frontend libs / CVEs
    cur_fl = current.get("frontend_libs", {})
    prev_fl = previous.get("frontend_libs", {})
    _diff_field("vulnerable_frontend_libs", cur_fl.get("vulnerable_libs", 0), prev_fl.get("vulnerable_libs", 0),
                severity="high" if cur_fl.get("vulnerable_libs", 0) > prev_fl.get("vulnerable_libs", 0) else "info")
    _diff_field("sri_missing", cur_fl.get("sri_missing", 0), prev_fl.get("sri_missing", 0))

    cur_cves = {v["id"] for v in cur_fl.get("vulnerabilities", [])}
    prev_cves = {v["id"] for v in prev_fl.get("vulnerabilities", [])}
    new_cves = cur_cves - prev_cves
    fixed_cves = prev_cves - cur_cves
    if new_cves:
        changes.append({"field": "cves_new", "old": None, "new": sorted(new_cves), "severity": "high"})
    if fixed_cves:
        changes.append({"field": "cves_fixed", "old": sorted(fixed_cves), "new": None, "severity": "info"})

    # Security headers
    cur_hdr = current.get("headers", {})
    prev_hdr = previous.get("headers", {})
    _diff_field("security_headers_score", cur_hdr.get("score", 0), prev_hdr.get("score", 0))

    # TLS
    cur_tls = current.get("tls", {})
    prev_tls = previous.get("tls", {})
    _diff_field("tls_version", cur_tls.get("tls_version"), prev_tls.get("tls_version"))
    _diff_field("cert_days_remaining", cur_tls.get("cert_days_remaining"), prev_tls.get("cert_days_remaining"))

    # DNS
    cur_dns_a = set(current.get("dns", {}).get("a", []))
    prev_dns_a = set(previous.get("dns", {}).get("a", []))
    if cur_dns_a != prev_dns_a:
        changes.append({"field": "dns_a_changed", "old": sorted(prev_dns_a), "new": sorted(cur_dns_a), "severity": "medium"})

    # WAF
    _diff_field("waf_vendor", cur_atk.get("waf_vendor"), prev_atk.get("waf_vendor"), severity="high")

    # Origin IP
    _diff_field("origin_ip_exposed", cur_atk.get("origin_ip_exposed", False), prev_atk.get("origin_ip_exposed", False),
                severity="critical" if cur_atk.get("origin_ip_exposed") and not prev_atk.get("origin_ip_exposed") else "info")

    # Filter out no-change entries
    changes = [c for c in changes if c["old"] != c["new"]]

    n_high = sum(1 for c in changes if c.get("severity") in ("critical", "high"))
    n_med = sum(1 for c in changes if c.get("severity") == "medium")

    return {
        "changes": changes,
        "total_changes": len(changes),
        "high_severity_changes": n_high,
        "medium_severity_changes": n_med,
        "current_timestamp": current.get("timestamp"),
        "previous_timestamp": previous.get("timestamp"),
    }


def print_recon_diff(diff: Dict[str, Any]) -> None:
    """Pretty-print a recon diff to terminal."""
    from fray.output import console, print_header
    print_header("Fray Recon — Comparison with Previous Scan")
    console.print(f"  Previous: {diff.get('previous_timestamp', '?')}")
    console.print(f"  Current:  {diff.get('current_timestamp', '?')}")
    console.print()

    changes = diff.get("changes", [])
    if not changes:
        console.print("  [green]No changes detected[/green]")
        return

    console.print(f"  [bold]{len(changes)} change(s)[/bold]"
                  f" ({diff['high_severity_changes']} high, {diff['medium_severity_changes']} medium)")
    console.print()

    sev_colors = {"critical": "bold red", "high": "red", "medium": "yellow", "info": "dim"}
    for c in changes:
        sc = sev_colors.get(c.get("severity", "info"), "dim")
        field = c["field"]
        old_val = c.get("old")
        new_val = c.get("new")
        if old_val is None:
            console.print(f"    [{sc}]+[/{sc}] {field}: {new_val}")
        elif new_val is None:
            console.print(f"    [{sc}]-[/{sc}] {field}: {old_val}")
        else:
            console.print(f"    [{sc}]~[/{sc}] {field}: {old_val} → {new_val}")
    console.print()
