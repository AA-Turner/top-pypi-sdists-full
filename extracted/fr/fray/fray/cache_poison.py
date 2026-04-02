"""
Fray Web Cache Poisoning & Cache Deception Module.

#27 Cache Poisoning — inject malicious content via unkeyed headers:
  - X-Forwarded-Host, X-Forwarded-Scheme, X-Original-URL
  - X-Rewrite-URL, X-Forwarded-Proto, X-Host
  - Origin, X-Forwarded-Port, X-Forwarded-Prefix
  - Detects: reflected headers, XSS via cache, open redirect via cache

#28 Web Cache Deception — trick caches into storing private content:
  - Path confusion: /account.css, /account/x.jpg, /account%0a.css
  - Static extension appending, path traversal, dot segments
  - Detects: personalized content in cached responses

Usage:
    scanner = CachePoisonScanner(url, cookie="session=abc")
    result = scanner.scan()

Zero external dependencies — stdlib only.
"""

import http.client
import random
import re
import ssl
import string
import time
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple


# ── Unkeyed headers for cache poisoning ────────────────────────────────

_POISON_HEADERS = [
    ("X-Forwarded-Host", "fray-cache-test.example.com", "xfh"),
    ("X-Forwarded-Scheme", "nothttps", "xfs"),
    ("X-Forwarded-Proto", "nothttps", "xfp"),
    ("X-Forwarded-Port", "1337", "xfport"),
    ("X-Forwarded-Prefix", "/fray-prefix-test", "xfprefix"),
    ("X-Original-URL", "/fray-original-url-test", "xou"),
    ("X-Rewrite-URL", "/fray-rewrite-url-test", "xru"),
    ("X-Host", "fray-cache-test.example.com", "xhost"),
    ("X-Forwarded-Server", "fray-cache-test.example.com", "xfserver"),
    ("X-HTTP-Method-Override", "POST", "xmethod"),
    ("X-Custom-IP-Authorization", "127.0.0.1", "xcustom_ip"),
    ("Origin", "https://fray-cache-test.example.com", "origin"),
    ("X-Frame-Options", "", "xfo_remove"),  # Try removing
    ("Transfer-Encoding", "chunked", "te"),
    ("X-Forwarded-For", "127.0.0.1", "xff"),
]

# Double/multiple header tests
_DOUBLE_HEADERS = [
    ("Host", "fray-cache-test.example.com", "double_host"),
    ("Content-Type", "text/html", "double_ct"),
]

# Cache deception path suffixes
_DECEPTION_SUFFIXES = [
    (".css", "static_css"),
    (".js", "static_js"),
    (".jpg", "static_jpg"),
    (".png", "static_png"),
    (".gif", "static_gif"),
    (".ico", "static_ico"),
    (".svg", "static_svg"),
    (".woff2", "static_font"),
    (".pdf", "static_pdf"),
    ("/..%2f..%2f..%2f", "path_traversal"),
    ("%0a.css", "newline_css"),
    ("%00.css", "nullbyte_css"),
    ("/x.css", "subpath_css"),
    (";.css", "semicolon_css"),
    ("/.css", "slash_css"),
]

# Cache indicators in response headers
_CACHE_HIT_INDICATORS = [
    (r"x-cache.*?(hit|miss)", "x-cache"),
    (r"cf-cache-status.*?(hit|miss|dynamic|expired)", "cf-cache"),
    (r"x-varnish", "varnish"),
    (r"x-fastly", "fastly"),
    (r"age:\s*\d+", "age"),
    (r"x-served-by", "cdn-served"),
    (r"x-cache-hits:\s*\d+", "cache-hits"),
    (r"via.*?cache|varnish|cloudfront", "via-cache"),
    (r"x-drupal-cache", "drupal-cache"),
    (r"x-wp-cf-super-cache", "wp-cache"),
]


# ── Data Classes ───────────────────────────────────────────────────────

class CacheFinding:
    __slots__ = ("technique", "header", "value", "evidence", "confidence",
                 "severity", "details")

    def __init__(self, technique: str = "", header: str = "", value: str = "",
                 evidence: str = "", confidence: str = "likely",
                 severity: str = "medium", details: Optional[Dict] = None):
        self.technique = technique
        self.header = header
        self.value = value
        self.evidence = evidence
        self.confidence = confidence
        self.severity = severity
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {k: getattr(self, k) for k in self.__slots__}


class CacheResult:
    def __init__(self, url: str):
        self.url = url
        self.vulnerable = False
        self.cache_detected = False
        self.cache_type: Optional[str] = None
        self.findings: List[CacheFinding] = []
        self.techniques_tested: List[str] = []
        self.requests_made = 0
        self.duration_ms = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "vulnerable": self.vulnerable,
            "cache_detected": self.cache_detected,
            "cache_type": self.cache_type,
            "findings": [f.to_dict() for f in self.findings],
            "techniques_tested": self.techniques_tested,
            "requests_made": self.requests_made,
            "duration_ms": self.duration_ms,
        }


# ── Scanner ────────────────────────────────────────────────────────────

class CachePoisonScanner:
    """Web cache poisoning and cache deception scanner."""

    def __init__(self, url: str, cookie: str = "", timeout: int = 10,
                 verify_ssl: bool = True, level: int = 1):
        self.url = url
        self.cookie = cookie
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.level = min(max(level, 1), 3)

        parsed = urllib.parse.urlparse(url)
        self._scheme = parsed.scheme
        self._host = parsed.hostname or ""
        self._port = parsed.port or (443 if parsed.scheme == "https" else 80)
        self._path = parsed.path or "/"
        self._query = parsed.query
        self._requests = 0

        # State
        self._baseline_body = ""
        self._baseline_length = 0
        self._baseline_status = 0
        self._baseline_headers: Dict[str, str] = {}
        self._cache_type: Optional[str] = None

    def _random_buster(self) -> str:
        """Cache buster query parameter to ensure fresh responses."""
        return "fray_cb=" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))

    def _request(self, path: Optional[str] = None,
                 extra_headers: Optional[Dict[str, str]] = None,
                 cache_bust: bool = True) -> Tuple[int, str, Dict[str, str], float]:
        """Send request and return (status, body, headers_dict, elapsed_ms)."""
        p = path or self._path
        qs = self._query
        if cache_bust:
            buster = self._random_buster()
            qs = f"{qs}&{buster}" if qs else buster
        full_path = f"{p}?{qs}" if qs else p

        hdrs = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,*/*",
            "Accept-Language": "en-US,en;q=0.9",
        }
        if self.cookie:
            hdrs["Cookie"] = self.cookie
        if extra_headers:
            hdrs.update(extra_headers)

        t0 = time.monotonic()
        try:
            if self._scheme == "https":
                ctx = ssl.create_default_context()
                if not self.verify_ssl:
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                conn = http.client.HTTPSConnection(self._host, self._port,
                                                    timeout=self.timeout, context=ctx)
            else:
                conn = http.client.HTTPConnection(self._host, self._port,
                                                   timeout=self.timeout)
            conn.request("GET", full_path, headers=hdrs)
            resp = conn.getresponse()
            body = resp.read(1024 * 512).decode("utf-8", errors="replace")
            status = resp.status
            resp_headers = {k.lower(): v for k, v in resp.getheaders()}
            conn.close()
        except Exception:
            return 0, "", {}, 0

        self._requests += 1
        return status, body, resp_headers, (time.monotonic() - t0) * 1000

    def _get_baseline(self) -> None:
        """Establish baseline response."""
        status, body, hdrs, _ = self._request()
        self._baseline_status = status
        self._baseline_body = body
        self._baseline_length = len(body)
        self._baseline_headers = hdrs

    def _detect_cache(self) -> bool:
        """Detect if response passes through a cache layer."""
        all_headers = " ".join(f"{k}: {v}" for k, v in self._baseline_headers.items())
        for pat, name in _CACHE_HIT_INDICATORS:
            if re.search(pat, all_headers, re.IGNORECASE):
                self._cache_type = name
                return True
        return False

    # ── #27: Cache Poisoning ───────────────────────────────────────────

    def test_poison_headers(self) -> List[CacheFinding]:
        """Test unkeyed headers that may poison the cache."""
        findings = []

        for header_name, header_value, tag in _POISON_HEADERS:
            # Send request with the poisoned header
            _, body, resp_hdrs, _ = self._request(
                extra_headers={header_name: header_value}
            )

            # Check if our injected value is reflected
            reflected = False
            evidence_parts = []

            if header_value and header_value in body:
                reflected = True
                evidence_parts.append(f"value '{header_value}' reflected in body")

            # Check for behavioral changes
            if abs(len(body) - self._baseline_length) > 50:
                evidence_parts.append(f"body length changed ({self._baseline_length}->{len(body)})")

            # Check for redirect to our host
            location = resp_hdrs.get("location", "")
            if header_value and header_value in location:
                reflected = True
                evidence_parts.append(f"value reflected in Location header: {location[:100]}")

            # Check if the header appears in response headers
            for rk, rv in resp_hdrs.items():
                if header_value and header_value in rv and rk != header_name.lower():
                    reflected = True
                    evidence_parts.append(f"value reflected in {rk}: {rv[:100]}")

            if reflected or (evidence_parts and self.level >= 2):
                severity = "high" if reflected else "medium"
                confidence = "confirmed" if reflected else "likely"

                # Test if it's actually cached (send same request without header)
                if reflected:
                    _, body2, _, _ = self._request(cache_bust=False)
                    if header_value in body2:
                        severity = "critical"
                        evidence_parts.append("CACHED: poisoned response served without header")

                findings.append(CacheFinding(
                    technique="cache_poisoning",
                    header=header_name,
                    value=header_value,
                    evidence="; ".join(evidence_parts),
                    confidence=confidence,
                    severity=severity,
                    details={"tag": tag},
                ))

        return findings

    def test_poison_fat_get(self) -> List[CacheFinding]:
        """Test fat GET — sending body with GET request to override params."""
        if self.level < 2:
            return []

        findings = []
        marker = "fray_fatget_" + "".join(random.choices(string.digits, k=6))

        hdrs = {"Content-Type": "application/x-www-form-urlencoded"}
        # This is a manual request since we need GET with body
        qs = self._query
        buster = self._random_buster()
        qs = f"{qs}&{buster}" if qs else buster
        full_path = f"{self._path}?{qs}" if qs else self._path

        all_hdrs = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        if self.cookie:
            all_hdrs["Cookie"] = self.cookie

        try:
            if self._scheme == "https":
                ctx = ssl.create_default_context()
                if not self.verify_ssl:
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                conn = http.client.HTTPSConnection(self._host, self._port,
                                                    timeout=self.timeout, context=ctx)
            else:
                conn = http.client.HTTPConnection(self._host, self._port,
                                                   timeout=self.timeout)
            conn.request("GET", full_path, body=f"callback={marker}".encode(),
                         headers=all_hdrs)
            resp = conn.getresponse()
            body = resp.read(1024 * 512).decode("utf-8", errors="replace")
            conn.close()
            self._requests += 1
        except Exception:
            return findings

        if marker in body:
            findings.append(CacheFinding(
                technique="fat_get",
                header="GET body",
                value=f"callback={marker}",
                evidence=f"body parameter reflected in GET response",
                confidence="confirmed",
                severity="high",
                details={"marker": marker},
            ))

        return findings

    # ── #28: Web Cache Deception ───────────────────────────────────────

    def test_cache_deception(self) -> List[CacheFinding]:
        """Test web cache deception by appending static extensions."""
        findings = []

        # First, get authenticated response (with cookies)
        _, auth_body, _, _ = self._request()
        auth_length = len(auth_body)

        # Find personalized content markers (things that differ per user)
        personal_patterns = [
            r"(email|e-mail).*?[\w.+-]+@[\w.-]+",
            r"(username|user_name|login).*?[\w]+",
            r"(name|full_name|display_name).*?[\w\s]+",
            r"(balance|credits|points).*?\d+",
            r"(account|profile|dashboard)",
            r"(logout|sign.?out|log.?out)",
            r"(api[_-]?key|token|secret).*?[\w-]{8,}",
        ]

        has_personal = any(re.search(p, auth_body, re.IGNORECASE)
                          for p in personal_patterns)

        for suffix, tag in _DECEPTION_SUFFIXES:
            # Append suffix to the path
            deception_path = self._path.rstrip("/") + suffix
            _, body, hdrs, _ = self._request(path=deception_path)

            if not body:
                continue

            # Check if personalized content is still returned
            body_has_personal = any(re.search(p, body, re.IGNORECASE)
                                    for p in personal_patterns)

            # Check cache headers
            cached = False
            cache_evidence = []
            for pat, name in _CACHE_HIT_INDICATORS:
                all_h = " ".join(f"{k}: {v}" for k, v in hdrs.items())
                m = re.search(pat, all_h, re.IGNORECASE)
                if m:
                    cache_evidence.append(f"{name}: {m.group(0)[:50]}")
                    if "hit" in m.group(0).lower():
                        cached = True

            # Content similarity check
            length_ratio = len(body) / max(auth_length, 1)

            if body_has_personal and (cached or length_ratio > 0.8):
                severity = "critical" if cached else "high"
                evidence = f"personal content returned at {deception_path}"
                if cache_evidence:
                    evidence += f"; cache: {', '.join(cache_evidence)}"
                if cached:
                    evidence += "; CACHED: personal data exposed to other users"

                findings.append(CacheFinding(
                    technique="cache_deception",
                    header="path",
                    value=suffix,
                    evidence=evidence,
                    confidence="confirmed" if cached else "likely",
                    severity=severity,
                    details={"tag": tag, "deception_path": deception_path,
                             "cache_headers": cache_evidence},
                ))

            elif has_personal and length_ratio > 0.8 and not body_has_personal:
                # Response stripped personal data — good, but note the path works
                pass

            elif cache_evidence and length_ratio > 0.5:
                findings.append(CacheFinding(
                    technique="cache_deception",
                    header="path",
                    value=suffix,
                    evidence=f"path accepted ({len(body)}B), cache: {', '.join(cache_evidence)}",
                    confidence="possible",
                    severity="low",
                    details={"tag": tag, "deception_path": deception_path},
                ))

        return findings

    # ── Full scan ──────────────────────────────────────────────────────

    def scan(self) -> CacheResult:
        """Run all cache poisoning and deception tests."""
        result = CacheResult(self.url)
        t0 = time.monotonic()

        self._get_baseline()
        result.cache_detected = self._detect_cache()
        result.cache_type = self._cache_type

        # #27: Cache poisoning via headers
        result.techniques_tested.append("poison_headers")
        poison_findings = self.test_poison_headers()
        result.findings.extend(poison_findings)

        # Fat GET
        if self.level >= 2:
            result.techniques_tested.append("fat_get")
            fat_findings = self.test_poison_fat_get()
            result.findings.extend(fat_findings)

        # #28: Cache deception
        result.techniques_tested.append("cache_deception")
        deception_findings = self.test_cache_deception()
        result.findings.extend(deception_findings)

        result.vulnerable = any(f.confidence in ("confirmed", "likely")
                                for f in result.findings)
        result.requests_made = self._requests
        result.duration_ms = int((time.monotonic() - t0) * 1000)
        return result
