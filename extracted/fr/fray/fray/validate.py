#!/usr/bin/env python3
"""
Fray Validate — Blue Team WAF Configuration Validation Report

Usage:
    fray validate <url>                    Full WAF validation
    fray validate <url> --waf cloudflare   Validate specific WAF config
    fray validate <url> --categories xss,sqli  Test specific categories
    fray validate <url> --output report.json   Save results

Runs a comprehensive WAF validation:
    1. Detect WAF vendor
    2. Test security headers
    3. Test payload categories with coverage scoring
    4. Generate graded validation report (A-F)
    5. Provide actionable recommendations

Zero external dependencies — stdlib only.
"""

import http.client
import json
import os
import ssl
import sys
import urllib.parse
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from fray import __version__, PAYLOADS_DIR


class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'


# ── Security Header Checks ──────────────────────────────────────────────────

SECURITY_HEADERS = {
    "strict-transport-security": {
        "name": "HSTS",
        "description": "HTTP Strict Transport Security",
        "weight": 10,
        "recommended": "max-age=31536000; includeSubDomains; preload",
        "check": lambda v: "max-age=" in v.lower() and int(
            v.lower().split("max-age=")[1].split(";")[0].strip()
        ) >= 31536000 if "max-age=" in v.lower() else False,
    },
    "content-security-policy": {
        "name": "CSP",
        "description": "Content Security Policy",
        "weight": 15,
        "recommended": "default-src 'self'; script-src 'self'",
        "check": lambda v: "default-src" in v.lower() or "script-src" in v.lower(),
    },
    "x-content-type-options": {
        "name": "X-Content-Type-Options",
        "description": "Prevent MIME-type sniffing",
        "weight": 5,
        "recommended": "nosniff",
        "check": lambda v: v.lower().strip() == "nosniff",
    },
    "x-frame-options": {
        "name": "X-Frame-Options",
        "description": "Clickjacking protection",
        "weight": 5,
        "recommended": "DENY or SAMEORIGIN",
        "check": lambda v: v.upper().strip() in ("DENY", "SAMEORIGIN"),
    },
    "x-xss-protection": {
        "name": "X-XSS-Protection",
        "description": "Browser XSS filter",
        "weight": 3,
        "recommended": "1; mode=block",
        "check": lambda v: "1" in v,
    },
    "referrer-policy": {
        "name": "Referrer-Policy",
        "description": "Control referrer information",
        "weight": 5,
        "recommended": "strict-origin-when-cross-origin",
        "check": lambda v: v.lower().strip() in (
            "no-referrer", "strict-origin", "strict-origin-when-cross-origin",
            "same-origin", "no-referrer-when-downgrade"
        ),
    },
    "permissions-policy": {
        "name": "Permissions-Policy",
        "description": "Control browser features",
        "weight": 5,
        "recommended": "camera=(), microphone=(), geolocation=()",
        "check": lambda v: len(v) > 5,
    },
}

# ── WAF-Specific Recommendations ────────────────────────────────────────────

WAF_RECOMMENDATIONS: Dict[str, Dict] = {
    "cloudflare": {
        "name": "Cloudflare",
        "checks": [
            {"name": "Managed Ruleset", "description": "Enable OWASP Core Ruleset", "category": "rules"},
            {"name": "Bot Management", "description": "Enable Bot Fight Mode or Super Bot Fight Mode", "category": "bot"},
            {"name": "Rate Limiting", "description": "Set rate limits on sensitive endpoints", "category": "rate"},
            {"name": "Browser Integrity Check", "description": "Enable BIC to block headless browsers", "category": "bot"},
            {"name": "Challenge Passage", "description": "Set challenge passage TTL to 30 minutes", "category": "config"},
            {"name": "Security Level", "description": "Set to at least 'Medium' (recommended: 'High')", "category": "config"},
            {"name": "SSL Mode", "description": "Use 'Full (Strict)' SSL mode", "category": "tls"},
            {"name": "DNSSEC", "description": "Enable DNSSEC for domain", "category": "dns"},
            {"name": "Page Shield", "description": "Enable Page Shield for supply chain protection", "category": "advanced"},
        ],
    },
    "aws_waf": {
        "name": "AWS WAF",
        "checks": [
            {"name": "Managed Rules", "description": "Enable AWS Managed Rules (Core, SQLi, XSS)", "category": "rules"},
            {"name": "Rate-Based Rules", "description": "Configure rate-based rules for DDoS protection", "category": "rate"},
            {"name": "IP Reputation", "description": "Enable Amazon IP Reputation list", "category": "rules"},
            {"name": "Bot Control", "description": "Enable AWS WAF Bot Control", "category": "bot"},
            {"name": "Logging", "description": "Enable WAF logging to S3/CloudWatch", "category": "logging"},
            {"name": "Geographic Restrictions", "description": "Block traffic from unused regions", "category": "geo"},
            {"name": "Custom Rules", "description": "Add custom rules for application-specific attacks", "category": "rules"},
        ],
    },
    "imperva": {
        "name": "Imperva (Incapsula)",
        "checks": [
            {"name": "WAF Rules", "description": "Enable all WAF rule categories", "category": "rules"},
            {"name": "Advanced Bot Protection", "description": "Enable ABP with CAPTCHA challenges", "category": "bot"},
            {"name": "DDoS Protection", "description": "Enable infrastructure DDoS protection", "category": "ddos"},
            {"name": "API Security", "description": "Enable API schema validation", "category": "api"},
            {"name": "Client Classification", "description": "Enable client reputation database", "category": "bot"},
            {"name": "Custom Rules", "description": "Create custom security rules for app logic", "category": "rules"},
        ],
    },
    "akamai": {
        "name": "Akamai",
        "checks": [
            {"name": "Kona Site Defender", "description": "Enable KSD with latest rule updates", "category": "rules"},
            {"name": "Rate Controls", "description": "Configure rate controls per endpoint", "category": "rate"},
            {"name": "Bot Manager", "description": "Enable Bot Manager Premier", "category": "bot"},
            {"name": "Client Reputation", "description": "Enable client reputation scoring", "category": "bot"},
            {"name": "Slow POST Protection", "description": "Enable slow POST attack mitigation", "category": "ddos"},
            {"name": "API Gateway", "description": "Enable API security policies", "category": "api"},
        ],
    },
}

# Default recommendations for WAFs without specific entries
DEFAULT_RECOMMENDATIONS = [
    {"name": "OWASP Core Ruleset", "description": "Enable OWASP ModSecurity Core Rule Set (CRS)", "category": "rules"},
    {"name": "Rate Limiting", "description": "Configure rate limiting on API/login endpoints", "category": "rate"},
    {"name": "Bot Protection", "description": "Enable bot detection and challenge mechanisms", "category": "bot"},
    {"name": "Logging", "description": "Enable comprehensive WAF logging and alerting", "category": "logging"},
    {"name": "Custom Rules", "description": "Add application-specific custom rules", "category": "rules"},
]


# ── HTTP Utilities ───────────────────────────────────────────────────────────

def _fetch_headers(url: str, timeout: int = 10) -> Tuple[int, Dict[str, str]]:
    """Fetch HTTP response headers from a URL."""
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname
    port = parsed.port
    path = parsed.path or "/"
    use_ssl = parsed.scheme == "https"

    if use_ssl:
        ctx = ssl.create_default_context()
        port = port or 443
        conn = http.client.HTTPSConnection(host, port, context=ctx, timeout=timeout)
    else:
        port = port or 80
        conn = http.client.HTTPConnection(host, port, timeout=timeout)

    try:
        conn.request("GET", path, headers={"User-Agent": f"Fray/{__version__}"})
        resp = conn.getresponse()
        headers = {k.lower(): v for k, v in resp.getheaders()}
        status = resp.status
        conn.close()
        return status, headers
    except Exception as e:
        conn.close()
        return 0, {"error": str(e)}


def _test_payloads_quick(url: str, category: str, max_payloads: int = 10,
                          timeout: int = 8, delay: float = 0.3) -> Dict:
    """Quick payload test for a specific category. Returns summary dict."""
    from fray.tester import WAFTester
    tester = WAFTester(target=url, timeout=timeout, delay=delay)

    cat_dir = PAYLOADS_DIR / category
    if not cat_dir.exists():
        return {"category": category, "total": 0, "blocked": 0, "passed": 0, "block_rate": 0.0}

    all_payloads = []
    for pf in sorted(cat_dir.glob("*.json")) + sorted(cat_dir.glob("*.txt")):
        all_payloads.extend(tester.load_payloads(str(pf)))

    if not all_payloads:
        return {"category": category, "total": 0, "blocked": 0, "passed": 0, "block_rate": 0.0}

    results = tester.test_payloads(all_payloads, max_payloads=max_payloads)
    blocked = sum(1 for r in results if r.get("blocked"))
    passed = len(results) - blocked
    rate = (blocked / len(results) * 100) if results else 0.0

    bypassed_payloads = [
        {"payload": r.get("payload", "")[:80], "description": r.get("description", "")}
        for r in results if not r.get("blocked")
    ]

    return {
        "category": category,
        "total": len(results),
        "blocked": blocked,
        "passed": passed,
        "block_rate": round(rate, 1),
        "bypassed": bypassed_payloads,
    }


# ── Grading ──────────────────────────────────────────────────────────────────

def calculate_grade(header_score: float, waf_block_rate: float, waf_detected: bool) -> Tuple[str, int]:
    """Calculate overall grade based on headers and WAF performance."""
    # Header score: 0-48 points (based on weights)
    # WAF block rate: 0-40 points
    # WAF detection: 0-12 points

    waf_points = (waf_block_rate / 100.0) * 40 if waf_detected else 0
    detect_points = 12 if waf_detected else 0
    total = header_score + waf_points + detect_points

    if total >= 90:
        return "A", int(total)
    elif total >= 80:
        return "A-", int(total)
    elif total >= 70:
        return "B+", int(total)
    elif total >= 60:
        return "B", int(total)
    elif total >= 50:
        return "C+", int(total)
    elif total >= 40:
        return "C", int(total)
    elif total >= 30:
        return "D", int(total)
    else:
        return "F", int(total)


def grade_color(grade: str) -> str:
    """Get color for a grade."""
    if grade.startswith("A"):
        return Colors.GREEN
    elif grade.startswith("B"):
        return Colors.BLUE
    elif grade.startswith("C"):
        return Colors.YELLOW
    else:
        return Colors.RED


# ── Report Generation ────────────────────────────────────────────────────────

def run_validate(
    target: str,
    waf: Optional[str] = None,
    categories: Optional[List[str]] = None,
    max_payloads: int = 10,
    output: Optional[str] = None,
    timeout: int = 8,
    delay: float = 0.3,
    verbose: bool = False,
):
    """Main entry point for fray validate."""
    print(f"\n{Colors.BOLD}Fray Validate v{__version__}{Colors.END}")
    print(f"{Colors.DIM}{'━' * 60}{Colors.END}")
    print(f"  Target: {Colors.CYAN}{target}{Colors.END}")
    print()

    report: Dict = {
        "target": target,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "fray_version": __version__,
    }

    # ── Step 1: WAF Detection ────────────────────────────────────────────
    print(f"{Colors.DIM}[1/4] Detecting WAF...{Colors.END}")
    from fray.detector import WAFDetector
    detector = WAFDetector()
    detection = detector.detect_waf(target)

    detected_waf = detection.get("waf", "None")
    confidence = detection.get("confidence", 0)
    waf_detected = detected_waf != "None" and confidence > 20

    report["waf"] = {
        "detected": detected_waf,
        "confidence": confidence,
        "signatures": detection.get("signatures", []),
    }

    if waf_detected:
        print(f"  {Colors.GREEN}WAF Detected: {detected_waf} ({confidence}%){Colors.END}")
    else:
        print(f"  {Colors.RED}No WAF Detected{Colors.END}")

    # Use specified WAF or detected WAF for recommendations
    waf_key = waf or detected_waf.lower().split()[0] if waf_detected else waf
    if waf_key:
        waf_key = waf_key.lower().replace(" ", "_").replace("-", "_")

    # ── Step 2: Security Headers ─────────────────────────────────────────
    print(f"{Colors.DIM}[2/4] Checking security headers...{Colors.END}")
    status_code, headers = _fetch_headers(target, timeout=timeout)

    header_results = []
    header_score = 0.0
    max_header_score = sum(h["weight"] for h in SECURITY_HEADERS.values())

    for hdr_key, hdr_info in SECURITY_HEADERS.items():
        value = headers.get(hdr_key, "")
        present = bool(value)
        correct = False
        if present:
            try:
                correct = hdr_info["check"](value)
            except Exception:
                correct = False

        points = hdr_info["weight"] if correct else (hdr_info["weight"] * 0.5 if present else 0)
        header_score += points

        status_icon = f"{Colors.GREEN}PASS{Colors.END}" if correct else (
            f"{Colors.YELLOW}WEAK{Colors.END}" if present else f"{Colors.RED}MISS{Colors.END}"
        )
        header_results.append({
            "header": hdr_key,
            "name": hdr_info["name"],
            "present": present,
            "correct": correct,
            "value": value[:80] if value else "",
            "recommended": hdr_info["recommended"],
            "points": points,
            "max_points": hdr_info["weight"],
        })
        if verbose:
            val_display = f" = {value[:50]}" if value else ""
            print(f"    {status_icon}  {hdr_info['name']:<28}{val_display}")

    # Normalize header score to 48-point scale
    header_score_normalized = (header_score / max_header_score) * 48 if max_header_score > 0 else 0
    report["headers"] = {
        "status_code": status_code,
        "score": round(header_score_normalized, 1),
        "max_score": 48,
        "results": header_results,
    }

    passed_headers = sum(1 for h in header_results if h["correct"])
    total_headers = len(header_results)
    print(f"  Headers: {Colors.BOLD}{passed_headers}/{total_headers}{Colors.END} properly configured "
          f"({Colors.BOLD}{header_score_normalized:.0f}/48{Colors.END} pts)")

    # ── Step 3: Payload Testing ──────────────────────────────────────────
    print(f"{Colors.DIM}[3/4] Testing payload categories...{Colors.END}")

    test_categories = categories or ["xss", "sqli", "ssrf", "command_injection"]
    # Filter to categories that exist
    available = [d.name for d in PAYLOADS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]
    test_categories = [c for c in test_categories if c in available]

    category_results = []
    total_blocked = 0
    total_tested = 0

    for cat in test_categories:
        result = _test_payloads_quick(target, cat, max_payloads=max_payloads,
                                       timeout=timeout, delay=delay)
        category_results.append(result)
        total_blocked += result["blocked"]
        total_tested += result["total"]

        rate = result["block_rate"]
        rate_color = Colors.GREEN if rate >= 95 else (Colors.YELLOW if rate >= 80 else Colors.RED)
        print(f"    {cat:<25} {rate_color}{rate:>5.1f}%{Colors.END} "
              f"({result['blocked']}/{result['total']} blocked)")
        if verbose and result.get("bypassed"):
            for bp in result["bypassed"][:3]:
                print(f"      {Colors.RED}BYPASS:{Colors.END} {bp['description'][:60]}")

    overall_block_rate = (total_blocked / total_tested * 100) if total_tested > 0 else 0.0
    report["payload_tests"] = {
        "categories": category_results,
        "overall_block_rate": round(overall_block_rate, 1),
        "total_tested": total_tested,
        "total_blocked": total_blocked,
    }

    # ── Step 4: Grade & Recommendations ──────────────────────────────────
    print(f"{Colors.DIM}[4/4] Generating report...{Colors.END}")

    grade, score = calculate_grade(header_score_normalized, overall_block_rate, waf_detected)
    gc = grade_color(grade)

    report["grade"] = grade
    report["score"] = score

    # Recommendations
    recommendations = []

    # Header recommendations
    for hr in header_results:
        if not hr["correct"]:
            action = "Configure" if not hr["present"] else "Fix"
            recommendations.append({
                "priority": "high" if not hr["present"] else "medium",
                "category": "headers",
                "action": f"{action} {hr['name']}",
                "detail": f"Set {hr['header']}: {hr['recommended']}",
            })

    # WAF-specific recommendations
    waf_recs = WAF_RECOMMENDATIONS.get(waf_key, {}).get("checks", DEFAULT_RECOMMENDATIONS)
    for rec in waf_recs:
        recommendations.append({
            "priority": "medium",
            "category": rec["category"],
            "action": rec["name"],
            "detail": rec["description"],
        })

    # Category-specific recommendations based on bypass results
    for cr in category_results:
        if cr["block_rate"] < 100 and cr["passed"] > 0:
            recommendations.append({
                "priority": "high",
                "category": "waf_rules",
                "action": f"Improve {cr['category']} protection",
                "detail": f"{cr['passed']} payload(s) bypassed WAF in {cr['category']} category. "
                          f"Review and add custom rules.",
            })

    if not waf_detected:
        recommendations.insert(0, {
            "priority": "critical",
            "category": "waf",
            "action": "Deploy a WAF",
            "detail": "No WAF detected. Deploy Cloudflare, AWS WAF, or similar to protect against web attacks.",
        })

    report["recommendations"] = recommendations

    # ── Print Report ─────────────────────────────────────────────────────
    print(f"\n{Colors.DIM}{'━' * 60}{Colors.END}")
    print(f"\n  {Colors.BOLD}WAF Validation Report{Colors.END}")
    print(f"  {Colors.DIM}{target}{Colors.END}")
    print(f"  {Colors.DIM}{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}{Colors.END}")

    # Grade display
    print(f"\n  ┌─────────────────────────────┐")
    print(f"  │  Overall Grade: {gc}{Colors.BOLD}    {grade:<4}{Colors.END}     │")
    print(f"  │  Score:         {Colors.BOLD}{score}/100{Colors.END}       │")
    print(f"  └─────────────────────────────┘")

    # Summary table
    print(f"\n  {Colors.BOLD}Summary{Colors.END}")
    print(f"  {'WAF:':<25} {detected_waf} ({confidence}%)" if waf_detected else
          f"  {'WAF:':<25} {Colors.RED}Not detected{Colors.END}")
    print(f"  {'Headers:':<25} {passed_headers}/{total_headers} configured ({header_score_normalized:.0f}/48 pts)")
    print(f"  {'Block Rate:':<25} {overall_block_rate:.1f}% ({total_blocked}/{total_tested} payloads)")

    # Category breakdown
    print(f"\n  {Colors.BOLD}Category Breakdown{Colors.END}")
    print(f"  {'Category':<25} {'Block Rate':>10} {'Blocked':>10} {'Bypassed':>10}")
    print(f"  {'─' * 55}")
    for cr in category_results:
        rate = cr["block_rate"]
        rc = Colors.GREEN if rate >= 95 else (Colors.YELLOW if rate >= 80 else Colors.RED)
        print(f"  {cr['category']:<25} {rc}{rate:>9.1f}%{Colors.END} {cr['blocked']:>10} {cr['passed']:>10}")

    # Recommendations
    if recommendations:
        print(f"\n  {Colors.BOLD}Recommendations{Colors.END}")
        for i, rec in enumerate(recommendations[:10], 1):
            prio = rec["priority"]
            pc = Colors.RED if prio == "critical" else (Colors.RED if prio == "high" else Colors.YELLOW)
            print(f"  {i:>2}. {pc}[{prio.upper()}]{Colors.END} {rec['action']}")
            print(f"      {Colors.DIM}{rec['detail']}{Colors.END}")

    print(f"\n{Colors.DIM}{'━' * 60}{Colors.END}")
    print(f"  {Colors.DIM}Powered by Fray v{__version__} • https://github.com/dalisecurity/fray{Colors.END}\n")

    # Save output
    if output:
        with open(output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"  {Colors.GREEN}Report saved: {output}{Colors.END}\n")

    return report
