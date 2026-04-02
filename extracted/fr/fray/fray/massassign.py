"""
Fray Mass Assignment / HTTP Parameter Pollution Module.

Detects:
  1. Mass assignment — hidden params (role, admin, is_admin, verified, etc.)
     accepted by the server and changing behavior
  2. HTTP Parameter Pollution (HPP) — duplicate params handled differently
     by front-end vs back-end
  3. Parameter type juggling — sending arrays, objects, booleans where
     strings are expected

Technique:
  - Discover baseline response
  - Inject privilege-escalation params (role=admin, admin=true, etc.)
  - Detect behavioral changes (status code, body length, new content)
  - HPP: send duplicate params with conflicting values
  - Type juggling: send param[]=value, param=true, param=0

Usage:
    scanner = MassAssignScanner(url, method="POST", body_params={"name": "test"})
    result = scanner.scan()

Zero external dependencies — stdlib only.
"""

import http.client
import json
import re
import ssl
import time
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple


# ── Hidden parameter names to probe ────────────────────────────────────

_PRIVILEGE_PARAMS = [
    # Role / permission escalation
    ("role", ["admin", "administrator", "superadmin", "root", "manager"]),
    ("admin", ["true", "1", "yes"]),
    ("is_admin", ["true", "1", "yes"]),
    ("isAdmin", ["true", "1"]),
    ("is_staff", ["true", "1"]),
    ("is_superuser", ["true", "1"]),
    ("privilege", ["admin", "root", "elevated"]),
    ("access_level", ["admin", "99", "root"]),
    ("user_type", ["admin", "superadmin"]),
    ("group", ["admin", "administrators"]),
    ("permissions", ["all", "*", "admin"]),

    # Account state
    ("verified", ["true", "1"]),
    ("email_verified", ["true", "1"]),
    ("active", ["true", "1"]),
    ("approved", ["true", "1"]),
    ("banned", ["false", "0"]),
    ("locked", ["false", "0"]),
    ("disabled", ["false", "0"]),

    # Financial / billing
    ("balance", ["999999", "0"]),
    ("credits", ["999999"]),
    ("discount", ["100", "99"]),
    ("price", ["0", "0.01"]),
    ("amount", ["0"]),
    ("plan", ["enterprise", "premium", "unlimited"]),
    ("subscription", ["premium", "enterprise"]),

    # Internal fields
    ("id", ["1"]),
    ("user_id", ["1"]),
    ("account_id", ["1"]),
    ("org_id", ["1"]),
    ("tenant_id", ["1"]),
    ("debug", ["true", "1"]),
    ("test", ["true", "1"]),
    ("internal", ["true", "1"]),
]

# HPP test pairs — conflicting values for the same param
_HPP_STRATEGIES = [
    # Duplicate param with different value
    "duplicate",
    # Array notation
    "array",
    # JSON body override
    "json_override",
    # Mixed: query string + body
    "mixed_location",
]


# ── Data Classes ───────────────────────────────────────────────────────

class MassAssignFinding:
    __slots__ = ("technique", "param", "value", "evidence", "confidence",
                 "severity", "details")

    def __init__(self, technique: str = "", param: str = "", value: str = "",
                 evidence: str = "", confidence: str = "likely",
                 severity: str = "medium", details: Optional[Dict] = None):
        self.technique = technique
        self.param = param
        self.value = value
        self.evidence = evidence
        self.confidence = confidence
        self.severity = severity
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {k: getattr(self, k) for k in self.__slots__}


class MassAssignResult:
    def __init__(self, url: str):
        self.url = url
        self.vulnerable = False
        self.findings: List[MassAssignFinding] = []
        self.techniques_tested: List[str] = []
        self.requests_made = 0
        self.duration_ms = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "vulnerable": self.vulnerable,
            "findings": [f.to_dict() for f in self.findings],
            "techniques_tested": self.techniques_tested,
            "requests_made": self.requests_made,
            "duration_ms": self.duration_ms,
        }


# ── Scanner ────────────────────────────────────────────────────────────

class MassAssignScanner:
    """Mass assignment and HTTP parameter pollution scanner."""

    def __init__(self, url: str, method: str = "POST",
                 body_params: Optional[Dict[str, str]] = None,
                 cookie: str = "", timeout: int = 10,
                 verify_ssl: bool = True, level: int = 1):
        self.url = url
        self.method = method.upper()
        self.body_params = body_params or {}
        self.cookie = cookie
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.level = min(max(level, 1), 3)

        parsed = urllib.parse.urlparse(url)
        self._scheme = parsed.scheme
        self._host = parsed.hostname or ""
        self._port = parsed.port or (443 if parsed.scheme == "https" else 80)
        self._path = parsed.path or "/"
        self._query_params = dict(urllib.parse.parse_qsl(parsed.query))
        self._requests = 0

        # Baseline
        self._baseline_status = 0
        self._baseline_body = ""
        self._baseline_length = 0

    def _request(self, query_params: Optional[Dict] = None,
                 body_params: Optional[Dict] = None,
                 content_type: str = "form",
                 raw_body: Optional[str] = None) -> Tuple[int, str, float]:
        """Send HTTP request with given parameters."""
        qp = query_params or dict(self._query_params)
        bp = body_params or dict(self.body_params)

        qs = urllib.parse.urlencode(qp, quote_via=urllib.parse.quote) if qp else ""
        path = f"{self._path}?{qs}" if qs else self._path

        hdrs = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "*/*",
        }
        if self.cookie:
            hdrs["Cookie"] = self.cookie

        body_bytes = None
        if self.method in ("POST", "PUT", "PATCH"):
            if raw_body:
                body_bytes = raw_body.encode()
            elif content_type == "json":
                hdrs["Content-Type"] = "application/json"
                body_bytes = json.dumps(bp).encode()
            else:
                hdrs["Content-Type"] = "application/x-www-form-urlencoded"
                body_bytes = urllib.parse.urlencode(bp).encode()

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
            conn.request(self.method, path, body=body_bytes, headers=hdrs)
            resp = conn.getresponse()
            body = resp.read(1024 * 512).decode("utf-8", errors="replace")
            status = resp.status
            conn.close()
        except Exception:
            return 0, "", 0

        self._requests += 1
        return status, body, (time.monotonic() - t0) * 1000

    def _get_baseline(self) -> None:
        """Establish baseline response."""
        status, body, _ = self._request()
        self._baseline_status = status
        self._baseline_body = body
        self._baseline_length = len(body)

    def _is_different(self, status: int, body: str) -> Optional[str]:
        """Check if response significantly differs from baseline."""
        diffs = []
        if status != self._baseline_status:
            diffs.append(f"status {self._baseline_status}->{status}")
        length_diff = abs(len(body) - self._baseline_length)
        if length_diff > 50 and length_diff / max(self._baseline_length, 1) > 0.1:
            diffs.append(f"length {self._baseline_length}->{len(body)}")

        # Check for new privilege-related content
        priv_indicators = [
            r"admin", r"authorized", r"granted", r"elevated",
            r"premium", r"success", r"verified", r"approved",
        ]
        for pat in priv_indicators:
            if re.search(pat, body, re.IGNORECASE) and \
               not re.search(pat, self._baseline_body, re.IGNORECASE):
                diffs.append(f"new content: '{pat}'")

        return "; ".join(diffs) if diffs else None

    # ── Technique 1: Mass assignment ───────────────────────────────────

    def test_mass_assignment(self) -> List[MassAssignFinding]:
        """Inject hidden privilege-escalation parameters."""
        findings = []

        for param_name, values in _PRIVILEGE_PARAMS:
            # Skip if param already exists in the request
            if param_name in self.body_params or param_name in self._query_params:
                continue

            for value in values[:2]:  # Test top 2 values per param
                # Inject in body (POST/PUT/PATCH)
                if self.method in ("POST", "PUT", "PATCH"):
                    bp = dict(self.body_params)
                    bp[param_name] = value
                    status, body, _ = self._request(body_params=bp)

                    diff = self._is_different(status, body)
                    if diff:
                        severity = "critical" if param_name in ("role", "admin", "is_admin", "isAdmin", "is_superuser") \
                                   else "high" if param_name in ("verified", "price", "balance", "plan") \
                                   else "medium"
                        findings.append(MassAssignFinding(
                            technique="mass_assignment",
                            param=param_name,
                            value=value,
                            evidence=diff,
                            confidence="likely",
                            severity=severity,
                            details={"location": "body"},
                        ))
                        break  # One value per param is enough

                    # Also try JSON content type
                    if self.level >= 2:
                        status_j, body_j, _ = self._request(body_params=bp,
                                                             content_type="json")
                        diff_j = self._is_different(status_j, body_j)
                        if diff_j:
                            findings.append(MassAssignFinding(
                                technique="mass_assignment",
                                param=param_name,
                                value=value,
                                evidence=diff_j,
                                confidence="likely",
                                severity="high",
                                details={"location": "json_body"},
                            ))
                            break

                # Inject in query string (GET or as additional params)
                qp = dict(self._query_params)
                qp[param_name] = value
                status_q, body_q, _ = self._request(query_params=qp)
                diff_q = self._is_different(status_q, body_q)
                if diff_q:
                    findings.append(MassAssignFinding(
                        technique="mass_assignment",
                        param=param_name,
                        value=value,
                        evidence=diff_q,
                        confidence="likely",
                        severity="medium",
                        details={"location": "query"},
                    ))

        return findings

    # ── Technique 2: HTTP Parameter Pollution ──────────────────────────

    def test_hpp(self) -> List[MassAssignFinding]:
        """Test HTTP parameter pollution with duplicate parameters."""
        findings = []

        for param_name in list(self._query_params.keys()) + list(self.body_params.keys()):
            orig_value = self._query_params.get(param_name) or self.body_params.get(param_name, "")

            # Strategy 1: Duplicate param in query string
            qs = urllib.parse.urlencode(self._query_params, quote_via=urllib.parse.quote)
            qs += f"&{urllib.parse.quote(param_name)}=fray_hpp_test"
            path = f"{self._path}?{qs}" if qs else self._path

            hdrs = {"User-Agent": "Mozilla/5.0", "Accept": "*/*"}
            if self.cookie:
                hdrs["Cookie"] = self.cookie

            body_bytes = None
            if self.method in ("POST", "PUT", "PATCH"):
                hdrs["Content-Type"] = "application/x-www-form-urlencoded"
                body_bytes = urllib.parse.urlencode(self.body_params).encode()

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
                conn.request(self.method, path, body=body_bytes, headers=hdrs)
                resp = conn.getresponse()
                body = resp.read(1024 * 512).decode("utf-8", errors="replace")
                status = resp.status
                conn.close()
                self._requests += 1
            except Exception:
                continue

            # Check if the polluted value appears
            if "fray_hpp_test" in body and "fray_hpp_test" not in self._baseline_body:
                findings.append(MassAssignFinding(
                    technique="hpp_duplicate",
                    param=param_name,
                    value="fray_hpp_test",
                    evidence="polluted value reflected in response",
                    confidence="confirmed",
                    severity="medium",
                    details={"strategy": "duplicate_query_param"},
                ))

            diff = self._is_different(status, body)
            if diff and "fray_hpp_test" not in body:
                findings.append(MassAssignFinding(
                    technique="hpp_duplicate",
                    param=param_name,
                    value="fray_hpp_test",
                    evidence=diff,
                    confidence="likely",
                    severity="low",
                    details={"strategy": "duplicate_query_param"},
                ))

            # Strategy 2: Array notation param[]=value
            if self.level >= 2:
                qp_arr = dict(self._query_params)
                qp_arr[f"{param_name}[]"] = orig_value
                status_a, body_a, _ = self._request(query_params=qp_arr)
                diff_a = self._is_different(status_a, body_a)
                if diff_a:
                    findings.append(MassAssignFinding(
                        technique="hpp_array",
                        param=f"{param_name}[]",
                        value=orig_value,
                        evidence=diff_a,
                        confidence="likely",
                        severity="low",
                        details={"strategy": "array_notation"},
                    ))

        return findings

    # ── Technique 3: Type juggling ─────────────────────────────────────

    def test_type_juggling(self) -> List[MassAssignFinding]:
        """Test parameter type juggling (arrays, booleans, objects)."""
        if self.level < 2:
            return []

        findings = []
        all_params = {**self._query_params, **self.body_params}

        for param_name, orig_value in all_params.items():
            juggle_values = [
                ("true", "boolean_true"),
                ("false", "boolean_false"),
                ("null", "null"),
                ("0", "zero"),
                ("-1", "negative"),
                ("[]", "empty_array"),
                ("{}", "empty_object"),
                ("undefined", "undefined"),
                ("NaN", "nan"),
            ]

            for jvalue, jname in juggle_values:
                if jvalue == orig_value:
                    continue

                if param_name in self.body_params:
                    bp = dict(self.body_params)
                    bp[param_name] = jvalue
                    status, body, _ = self._request(body_params=bp)
                else:
                    qp = dict(self._query_params)
                    qp[param_name] = jvalue
                    status, body, _ = self._request(query_params=qp)

                diff = self._is_different(status, body)
                if diff:
                    findings.append(MassAssignFinding(
                        technique="type_juggling",
                        param=param_name,
                        value=jvalue,
                        evidence=diff,
                        confidence="possible",
                        severity="low",
                        details={"juggle_type": jname, "original": orig_value},
                    ))

        return findings

    # ── Full scan ──────────────────────────────────────────────────────

    def scan(self) -> MassAssignResult:
        """Run all mass assignment and HPP tests."""
        result = MassAssignResult(self.url)
        t0 = time.monotonic()

        self._get_baseline()

        # Technique 1: Mass assignment
        result.techniques_tested.append("mass_assignment")
        ma_findings = self.test_mass_assignment()
        result.findings.extend(ma_findings)

        # Technique 2: HPP
        result.techniques_tested.append("hpp")
        hpp_findings = self.test_hpp()
        result.findings.extend(hpp_findings)

        # Technique 3: Type juggling (level 2+)
        if self.level >= 2:
            result.techniques_tested.append("type_juggling")
            tj_findings = self.test_type_juggling()
            result.findings.extend(tj_findings)

        result.vulnerable = any(f.confidence in ("confirmed", "likely") for f in result.findings)
        result.requests_made = self._requests
        result.duration_ms = int((time.monotonic() - t0) * 1000)
        return result
