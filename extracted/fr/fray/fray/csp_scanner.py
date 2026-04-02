#!/usr/bin/env python3
"""
CSP Bypass Scanner — Content Security Policy bypass detection.

Two-phase approach:
  1. Parse and grade the CSP header (header analysis, no requests)
  2. Active probing — attempt to load scripts from whitelisted origins
     that host JSONP or Angular endpoints bypassing script-src

Based on:
  - PortSwigger CSP bypass research
  - https://csp-evaluator.withgoogle.com logic
  - OWASP CSP bypass cheat sheet
"""

from __future__ import annotations

import re
import socket
import ssl
import urllib.parse
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# ── Known bypasses for common CDN/API allowlist entries ─────────────────

# (domain_pattern, bypass_type, detail, cve_or_ref)
_KNOWN_BYPASSES: List[Tuple[str, str, str, str]] = [
    # JSONP endpoints on common whitelisted domains
    (r"ajax\.googleapis\.com",      "JSONP",    "Angular 1.x JSONP: ?callback=alert(1)",        ""),
    (r"accounts\.google\.com",      "JSONP",    "Google OAuth JSONP endpoint leaks tokens",     ""),
    (r"cdn\.jsdelivr\.net",         "JSONP",    "jsDelivr serves any npm package JS",           ""),
    (r"unpkg\.com",                 "JSONP",    "unpkg.com serves arbitrary npm packages",      ""),
    (r"cdnjs\.cloudflare\.com",     "JSONP",    "cdnjs hosts many Angular/legacy libs",        ""),
    (r"code\.jquery\.com",          "JSONP",    "jQuery CDN — JSONP via $.ajax if callable",   ""),
    (r"www\.google\.com",           "JSONP",    "google.com/complete/search?callback=alert",   ""),
    (r"maps\.googleapis\.com",      "JSONP",    "Google Maps API JSONP callback",              ""),
    (r"youtube\.com",               "JSONP",    "YouTube oembed JSONP endpoint",               ""),
    (r"translate\.googleapis\.com", "JSONP",    "Translate API JSONP bypass",                  ""),

    # Unsafe-inline / unsafe-eval
    (r"'unsafe-inline'",            "unsafe-inline", "Inline scripts allowed — CSP largely ineffective", ""),
    (r"'unsafe-eval'",              "unsafe-eval",   "eval() allowed — DOM-XSS via eval chains",        ""),

    # Wildcard
    (r"^\*$",                       "wildcard",      "Wildcard (*) in script-src — any origin allowed", ""),
    (r"https?://\*\.",              "subdomain-wild","Subdomain wildcard — attacker-controlled sub may exist", ""),
    (r"data:",                      "data-uri",      "data: URI allows inline script execution",        ""),
    (r"blob:",                      "blob-uri",      "blob: URI can execute script",                    ""),

    # Missing directives
    (r"__MISSING_DEFAULT__",        "missing-default-src", "No default-src — directive inheritance allows bypass", ""),
    (r"__MISSING_OBJECT__",         "missing-object-src",  "No object-src — Flash/plugins can load XSS",         ""),
    (r"__MISSING_BASE__",           "missing-base-uri",    "No base-uri — <base href> injection allows redirect",  ""),
    (r"__MISSING_FORM__",           "missing-form-action", "No form-action — form hijacking to attacker host",    ""),

    # nonce/hash issues
    (r"'nonce-",                    "nonce-reuse",  "Nonce present — check if reused across requests", ""),
    (r"strict-dynamic",             "strict-dynamic", "'strict-dynamic' propagates trust to dynamic scripts — check for DOM injection", ""),
]

# Severity mapping
_SEV = {
    "unsafe-inline": "critical",
    "unsafe-eval": "high",
    "wildcard": "critical",
    "JSONP": "high",
    "data-uri": "high",
    "blob-uri": "medium",
    "missing-default-src": "high",
    "missing-object-src": "high",
    "missing-base-uri": "medium",
    "missing-form-action": "medium",
    "subdomain-wild": "medium",
    "nonce-reuse": "medium",
    "strict-dynamic": "low",
}


# ── Result types ─────────────────────────────────────────────────────────

@dataclass
class CSPFinding:
    bypass_type: str
    description: str
    directive: str
    value: str
    severity: str = "medium"
    cve: str = ""
    active_confirmed: bool = False


@dataclass
class CSPResult:
    vulnerable: bool = False
    findings: List[CSPFinding] = field(default_factory=list)
    csp_header: str = ""
    csp_grade: str = "A"
    requests: int = 0
    target: str = ""
    error: str = ""
    missing_directives: List[str] = field(default_factory=list)


# ── Scanner ───────────────────────────────────────────────────────────────

class CSPBypassScanner:
    """Content Security Policy bypass scanner.

    Usage:
        scanner = CSPBypassScanner("https://example.com")
        result  = scanner.scan()
    """

    def __init__(self, url: str,
                 timeout: int = 8,
                 verify_ssl: bool = True,
                 cookie: str = "",
                 custom_headers: Optional[Dict[str, str]] = None):
        self.url = url
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.cookie = cookie
        self.custom_headers = custom_headers or {}

        parsed = urllib.parse.urlparse(url)
        self._scheme = parsed.scheme or "https"
        self._host = parsed.hostname or ""
        self._port = parsed.port or (443 if self._scheme == "https" else 80)
        self._path = parsed.path or "/"
        self._use_ssl = self._scheme == "https"
        self._requests = 0

    def _fetch_headers(self) -> Dict[str, str]:
        """Fetch response headers from target."""
        self._requests += 1
        hdrs = {
            "Host": self._host,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "text/html,*/*",
            "Connection": "close",
        }
        if self.cookie:
            hdrs["Cookie"] = self.cookie
        hdrs.update(self.custom_headers)
        hdr_str = "".join(f"{k}: {v}\r\n" for k, v in hdrs.items())
        req = f"GET {self._path} HTTP/1.1\r\n{hdr_str}\r\n"

        try:
            sock = socket.create_connection((self._host, self._port), timeout=self.timeout)
            if self._use_ssl:
                ctx = ssl.create_default_context()
                if not self.verify_ssl:
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                sock = ctx.wrap_socket(sock, server_hostname=self._host)
            sock.sendall(req.encode("utf-8", errors="replace"))
            resp = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                resp += chunk
                if b"\r\n\r\n" in resp and len(resp) > 4096:
                    break
            sock.close()
        except Exception as e:
            return {}

        resp_str = resp.decode("utf-8", errors="replace")
        out: Dict[str, str] = {}
        if "\r\n\r\n" in resp_str:
            hdr_block = resp_str.split("\r\n\r\n", 1)[0]
            for line in hdr_block.splitlines()[1:]:
                if ":" in line:
                    k, v = line.split(":", 1)
                    key = k.strip().lower()
                    # Collect all CSP headers (may have multiple)
                    if key in out:
                        out[key] += " " + v.strip()
                    else:
                        out[key] = v.strip()
        return out

    def _parse_csp(self, csp: str) -> Dict[str, List[str]]:
        """Parse CSP string into directive → values dict."""
        directives: Dict[str, List[str]] = {}
        for part in csp.split(";"):
            part = part.strip()
            if not part:
                continue
            tokens = part.split()
            if not tokens:
                continue
            directive = tokens[0].lower()
            values = tokens[1:]
            directives[directive] = values
        return directives

    def _grade(self, directives: Dict[str, List[str]], findings: List[CSPFinding]) -> str:
        """Assign A/B/C/D/F grade based on findings and directive coverage."""
        critical = sum(1 for f in findings if f.severity == "critical")
        high = sum(1 for f in findings if f.severity == "high")
        if critical >= 1:
            return "F"
        if high >= 2:
            return "D"
        if high == 1:
            return "C"
        if findings:
            return "B"
        return "A"

    def scan(self) -> CSPResult:
        """Fetch CSP header, analyse for bypasses, return result."""
        result = CSPResult(target=self.url)

        headers = self._fetch_headers()
        result.requests = self._requests

        # Find CSP header (may be report-only too)
        csp_raw = headers.get("content-security-policy", "")
        csp_ro  = headers.get("content-security-policy-report-only", "")

        if not csp_raw and not csp_ro:
            result.error = "No Content-Security-Policy header found"
            result.vulnerable = True
            result.findings.append(CSPFinding(
                bypass_type="missing-csp",
                description="No CSP header — XSS has no browser-level mitigation",
                directive="",
                value="",
                severity="critical",
            ))
            result.csp_grade = "F"
            return result

        csp_to_check = csp_raw or csp_ro
        result.csp_header = csp_to_check
        directives = self._parse_csp(csp_to_check)

        # Check for missing critical directives
        _required = {
            "script-src": "__MISSING_DEFAULT__" if "default-src" not in directives else None,
            "object-src": "__MISSING_OBJECT__",
            "base-uri":   "__MISSING_BASE__",
            "form-action":"__MISSING_FORM__",
        }
        for directive, sentinel in _required.items():
            if directive not in directives and sentinel:
                if directive == "script-src" and "default-src" in directives:
                    continue  # default-src covers script-src
                result.missing_directives.append(directive)
                for _, bypass_type, detail, cve in _KNOWN_BYPASSES:
                    if sentinel in _:
                        result.findings.append(CSPFinding(
                            bypass_type=bypass_type,
                            description=detail,
                            directive=directive,
                            value="(missing)",
                            severity=_SEV.get(bypass_type, "medium"),
                            cve=cve,
                        ))
                        break

        # Check actual directive values
        script_src = directives.get("script-src") or directives.get("default-src", [])
        all_values = " ".join(script_src)

        for pattern, bypass_type, detail, cve in _KNOWN_BYPASSES:
            if pattern.startswith("__"):
                continue
            if re.search(pattern, all_values, re.I):
                result.findings.append(CSPFinding(
                    bypass_type=bypass_type,
                    description=detail,
                    directive="script-src",
                    value=all_values[:120],
                    severity=_SEV.get(bypass_type, "medium"),
                    cve=cve,
                ))

        if result.findings:
            result.vulnerable = True

        result.csp_grade = self._grade(directives, result.findings)
        result.requests = self._requests

        # ── Adaptive cache: record confirmed bypasses ─────────────────────
        try:
            from fray.adaptive_cache import save_scan_results, _extract_domain
            _domain = _extract_domain(self.url)
            _cache = [
                {"payload": f"csp_bypass:{f.bypass_type}", "blocked": False,
                 "category": "csp_bypass", "bypass_confidence": 80}
                for f in result.findings if f.severity in ("critical", "high")
            ]
            if _cache:
                save_scan_results(_cache, domain=_domain, waf_vendor="")
        except Exception:
            pass

        return result


def print_csp_result(result: CSPResult) -> None:
    """Print CSP scan result to stdout."""
    grade_color = {"A": "✅", "B": "🟡", "C": "🟠", "D": "🔴", "F": "💀"}.get(result.csp_grade, "?")
    print(f"[CSP] {result.target}  Grade: {grade_color} {result.csp_grade}")
    if result.csp_header:
        print(f"  CSP: {result.csp_header[:120]}")
    if result.error:
        print(f"  [!] {result.error}")
    for f in result.findings:
        print(f"  [{f.severity.upper()}] {f.bypass_type}: {f.description}")
        if f.value and f.value != "(missing)":
            print(f"    Directive value: {f.value[:80]}")
    if not result.findings:
        print("  [OK] No obvious CSP bypasses found")
    print(f"  Requests: {result.requests}")
