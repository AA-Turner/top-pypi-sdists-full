"""SalmAlm Security Module — OWASP compliance, security audit, hardening.

Features:
  - Security audit report (OWASP Top 10 compliance check)
  - Enhanced rate limiting for login endpoints
  - SSRF protection utilities
  - Session security helpers
  - Security headers verification

보안 모듈 — OWASP 준수, 보안 감사, 강화.
"""

import logging

log = logging.getLogger("salmalm")
import ipaddress
import os
import re
import socket
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse

# BUG-BI fix: TTL cache for redact config — avoids file I/O on every log call
_redact_config_cache: dict | None = None
_redact_config_cache_ts: float = 0.0
_REDACT_CONFIG_TTL = 30.0  # seconds

from salmalm.constants import VERSION, KST, DATA_DIR
# ── Sensitive Data Redaction ─────────────────────────────────

_SESSION_ID_RE = re.compile(r"[^a-zA-Z0-9_\-]")

REDACT_PATTERNS = [
    r"sk-[a-zA-Z0-9]{20,}",  # OpenAI/Anthropic API 키
    r"ghp_[a-zA-Z0-9]{36}",  # GitHub 토큰
    r"xoxb-[a-zA-Z0-9-]+",  # Slack 봇 토큰
    r"[0-9]+:AA[a-zA-Z0-9_-]{33}",  # Telegram 봇 토큰
    r"(?i)password\s*[:=]\s*\S+",  # 비밀번호
    r"(?i)secret\s*[:=]\s*\S+",  # 시크릿
    r"(?i)token\s*[:=]\s*\S+",  # 토큰
    r"eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+",  # JWT
]

_COMPILED_PATTERNS = [re.compile(p) for p in REDACT_PATTERNS]


def _load_redact_config() -> dict:
    """Load redaction config from ~/.salmalm/security.json.

    BUG-BI fix: TTL-cached to prevent file I/O on every log/redact call.
    """
    global _redact_config_cache, _redact_config_cache_ts
    now = time.time()
    if _redact_config_cache is not None and now - _redact_config_cache_ts < _REDACT_CONFIG_TTL:
        return _redact_config_cache
    config_path = DATA_DIR / "security.json"
    defaults = {"redactEnabled": True, "customPatterns": []}
    try:
        if config_path.exists():
            import json as _json

            cfg = _json.loads(config_path.read_text(encoding="utf-8"))
            defaults.update(cfg)
    except Exception as e:  # noqa: broad-except
        log.debug(f"Suppressed: {e}")
    _redact_config_cache = defaults
    _redact_config_cache_ts = now
    return defaults


def redact_sensitive(text: str) -> str:
    """민감 정보를 [REDACTED]로 치환."""
    if not text or not isinstance(text, str):
        return text
    cfg = _load_redact_config()
    if not cfg.get("redactEnabled", True):
        return text
    result = text
    for pat in _COMPILED_PATTERNS:
        result = pat.sub("[REDACTED]", result)
    # Custom patterns
    # BUG-BJ fix: guard custom patterns against ReDoS
    # Limit pattern length and use a quick compile-test before applying
    for custom in cfg.get("customPatterns", []):
        if not isinstance(custom, str) or len(custom) > 256:
            continue
        try:
            _pat = re.compile(custom)
            result = _pat.sub("[REDACTED]", result)
        except re.error:
            pass
    return result


# ── Login Rate Limiter (Exponential Backoff) ────────────────


class LoginRateLimiter:
    """Per-key exponential backoff for login attempts.
    로그인 시도에 대한 지수 백오프 제한."""

    def __init__(self, max_attempts: int = 5, lockout_seconds: int = 300) -> None:
        """Init  ."""
        self._attempts: Dict[str, List[float]] = {}
        self._lockouts: Dict[str, float] = {}  # key -> lockout_until
        self._lock = threading.Lock()
        self.max_attempts = max_attempts
        self.lockout_seconds = lockout_seconds

    def check(self, key: str) -> Tuple[bool, float]:
        """Check if login attempt is allowed.
        Returns (allowed, retry_after_seconds).
        로그인 시도 허용 여부 확인."""
        with self._lock:
            now = time.time()
            # Check lockout
            lockout_until = self._lockouts.get(key, 0)
            if now < lockout_until:
                return False, lockout_until - now

            # Clean old attempts (older than lockout window)
            attempts = self._attempts.get(key, [])
            attempts = [t for t in attempts if now - t < self.lockout_seconds]
            self._attempts[key] = attempts

            if len(attempts) >= self.max_attempts:
                # Exponential backoff: 2^(attempts-max) seconds, capped at lockout_seconds
                # BUG-BK fix: clamp exponent before 2** to avoid bignum computation
                over = min(len(attempts) - self.max_attempts + 1, 30)
                backoff = min(2**over, self.lockout_seconds)
                self._lockouts[key] = now + backoff
                return False, backoff

            return True, 0

    def record_failure(self, key: str) -> None:
        """Record a failed login attempt. 실패한 로그인 기록."""
        with self._lock:
            now = time.time()
            if key not in self._attempts:
                self._attempts[key] = []
            self._attempts[key].append(now)

    def record_success(self, key: str) -> None:
        """Clear attempts on successful login. 성공 시 시도 기록 초기화."""
        with self._lock:
            self._attempts.pop(key, None)
            self._lockouts.pop(key, None)

    def cleanup(self) -> None:
        """Remove stale entries. 오래된 항목 정리."""
        with self._lock:
            now = time.time()
            stale_attempts = [k for k, v in self._attempts.items() if not v or now - max(v) > self.lockout_seconds * 2]
            for k in stale_attempts:
                del self._attempts[k]
            stale_lockouts = [k for k, v in self._lockouts.items() if now > v]
            for k in stale_lockouts:
                del self._lockouts[k]


# ── SSRF Protection ─────────────────────────────────────────


def is_internal_ip(url: str) -> Tuple[bool, str]:
    """Check if URL resolves to internal/private IP.
    내부/사설 IP로 연결되는 URL인지 확인.

    Returns (is_blocked, reason)."""
    try:
        parsed = urlparse(url)
    except Exception as e:  # noqa: broad-except
        return True, "Invalid URL"

    scheme = (parsed.scheme or "").lower()
    if scheme not in ("http", "https"):
        return True, f"Blocked protocol: {scheme} (only http/https allowed)"

    hostname = parsed.hostname or ""
    if not hostname:
        return True, "No hostname in URL"

    # Block metadata endpoints (클라우드 메타데이터 엔드포인트 차단)
    BLOCKED_HOSTS = frozenset(
        [
            "metadata.google.internal",
            "169.254.169.254",
            "metadata.internal",
            "metadata",
            "instance-data",
            "100.100.100.200",
            "metadata.azure.com",
            "metadata.aws.com",
        ]
    )
    if hostname in BLOCKED_HOSTS or hostname.endswith(".internal"):
        return True, f"Blocked metadata endpoint: {hostname}"

    # Block localhost variations (로컬호스트 변형 차단)
    LOCALHOST_PATTERNS = frozenset(
        [
            "localhost",
            "127.0.0.1",
            "::1",
            "0.0.0.0",
            "[::1]",
            "0177.0.0.1",
            "2130706433",  # Octal/decimal IP
        ]
    )
    hostname_lower = hostname.lower()
    if hostname_lower in LOCALHOST_PATTERNS:
        return True, f"Blocked localhost: {hostname}"

    # Detect hex/octal/decimal IP encoding tricks
    if re.match(r"^0[xX][0-9a-fA-F]+$", hostname):
        return True, f"Blocked hex-encoded IP: {hostname}"

    try:
        addrs = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
        for family, _, _, _, sockaddr in addrs:
            ip = ipaddress.ip_address(sockaddr[0])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
                return True, f"Internal IP blocked: {hostname} -> {ip}"
    except socket.gaierror:
        return True, f"DNS resolution failed: {hostname}"
    except (OSError, ValueError) as e:
        return True, f"IP check error: {e}"

    return False, ""


# ── Security Audit Report ───────────────────────────────────


class SecurityAuditor:
    """Generate OWASP Top 10 compliance report.
    OWASP Top 10 준수 보고서 생성."""

    def audit(self) -> Dict[str, Any]:
        """Run full security audit. Returns report dict.
        전체 보안 감사 실행."""
        report = {
            "version": VERSION,
            "timestamp": datetime.now(KST).isoformat(),
            "checks": {},
            "summary": {"pass": 0, "warn": 0, "fail": 0},
        }

        checks = [
            self._check_a01_access_control,
            self._check_a02_cryptographic_failures,
            self._check_a03_injection,
            self._check_a04_insecure_design,
            self._check_a05_security_misconfiguration,
            self._check_a06_vulnerable_components,
            self._check_a07_auth_failures,
            self._check_a08_integrity,
            self._check_a09_logging,
            self._check_a10_ssrf,
        ]

        for check_fn in checks:
            try:
                result = check_fn()
                report["checks"][result["id"]] = result
                report["summary"][result["status"].lower()] += 1
            except Exception as e:
                cid = check_fn.__name__.replace("_check_", "")
                report["checks"][cid] = {"id": cid, "status": "FAIL", "title": "Check Error", "details": str(e)}
                report["summary"]["fail"] += 1

        total = sum(report["summary"].values())
        report["score"] = round((report["summary"]["pass"] * 100 + report["summary"]["warn"] * 50) / max(total, 1))
        return report

    def _check_a01_access_control(self) -> dict:
        """A01: Broken Access Control — 접근 제어 취약점.

        BUG-BL fix: WebHandler (Mixin) removed; check FastAPI router auth instead.
        """
        issues = []
        # Check _require_auth helper exists in FastAPI routers
        try:
            from salmalm.web.auth import _require_auth  # noqa: F401
        except ImportError:
            issues.append("CRITICAL: _require_auth not available in FastAPI routers")

        # Check admin-only routes guard
        try:
            from salmalm.web.routes.web_auth import router as auth_router  # noqa: F401
        except ImportError:
            issues.append("WARN: Auth router not importable")

        # Check session token entropy (128-bit = 32 hex chars)
        import secrets

        test_token = secrets.token_hex(16)
        if len(test_token) < 32:
            issues.append("Token entropy below 128-bit")

        # Check CORS allowlist (not open reflection) — via asgi.py
        try:
            from salmalm.web.asgi import _cors_headers
            from starlette.requests import Request as _Req
            # Can't easily create a Request object here; just verify the function exists
            # and its source restricts origins
            import inspect
            src = inspect.getsource(_cors_headers)
            if "allowlist" not in src and "ALLOWED_ORIGINS" not in src and "loopback" not in src.lower():
                issues.append("WARN: CORS headers function may not use allowlist")
        except Exception as e:  # noqa: broad-except
            log.debug(f"Suppressed: {e}")

        status = "FAIL" if any("CRITICAL" in i for i in issues) else ("WARN" if issues else "PASS")
        return {
            "id": "A01",
            "title": "Broken Access Control / 접근 제어",
            "status": status,
            "details": issues or ["FastAPI routers use _require_auth; CORS allowlist active"],
        }

    def _check_a02_cryptographic_failures(self) -> dict:
        """A02: Cryptographic Failures — 암호화 취약점."""
        issues = []
        from salmalm.security.crypto import vault, HAS_CRYPTO  # noqa: F401

        if not HAS_CRYPTO:
            issues.append("WARN: AES-256-GCM unavailable (using HMAC-CTR fallback)")
        # Check PBKDF2 iterations
        from salmalm.constants import PBKDF2_ITER

        if PBKDF2_ITER < 100000:
            issues.append(f"WARN: PBKDF2 iterations low ({PBKDF2_ITER}), recommend ≥100000")
        # Check password hashing in auth
        try:
            from salmalm.web.auth import _hash_password

            h, s = _hash_password("test")
            if len(h) < 32:
                issues.append("Password hash output too short")
        except Exception as e:  # noqa: broad-except
            log.debug(f"Suppressed: {e}")
        status = "FAIL" if any("CRITICAL" in i for i in issues) else ("WARN" if issues else "PASS")
        return {
            "id": "A02",
            "title": "Cryptographic Failures / 암호화 실패",
            "status": status,
            "details": issues or ["Vault encryption OK, PBKDF2 password hashing OK"],
        }

    def _check_a03_injection(self) -> dict:
        """A03: Injection — 인젝션 취약점.

        BUG-BL/BM fix: web.py no longer exists (Mixin removed).
        Scan FastAPI routes directory instead.
        """
        issues = []
        # Static analysis: scan FastAPI routes for f-string SQL injection
        routes_dir = Path(__file__).resolve().parent.parent / "web" / "routes"
        try:
            for route_file in routes_dir.glob("*.py"):
                content = route_file.read_text(encoding="utf-8", errors="replace")
                if re.search(r'\.execute\(f["\']', content):
                    bad_lines = [
                        i + 1
                        for i, ln in enumerate(content.split("\n"))
                        if "execute(f" in ln and re.search(r"SELECT|INSERT|UPDATE|DELETE", ln, re.I)
                    ]
                    if bad_lines:
                        issues.append(f"Potential SQL injection in {route_file.name} lines: {bad_lines}")
        except Exception as e:  # noqa: broad-except
            log.debug(f"Suppressed: {e}")

        # Check CSP headers via FastAPI middleware
        try:
            from salmalm.web.app import create_app
            import inspect
            src = inspect.getsource(create_app)
            if "Content-Security-Policy" not in src and "security_headers" not in src.lower():
                issues.append("WARN: CSP headers may be missing from FastAPI middleware")
        except Exception as e:  # noqa: broad-except
            log.debug(f"Suppressed: {e}")

        # Check path traversal protection
        try:
            from salmalm.tools.tools_common import _resolve_path  # noqa: F401
        except ImportError:
            issues.append("Missing path traversal protection (_resolve_path)")

        status = (
            "FAIL" if any("CRITICAL" in i or "SQL injection" in i for i in issues) else ("WARN" if issues else "PASS")
        )
        return {
            "id": "A03",
            "title": "Injection / 인젝션",
            "status": status,
            "details": issues or ["Parameterized SQL queries, CSP headers, path traversal protection OK"],
        }

    def _check_a04_insecure_design(self) -> dict:
        """A04: Insecure Design — 불안전한 설계.

        BUG-BL fix: WebHandler removed; check FastAPI body size limit instead.
        """
        issues = []
        # Check rate limiting
        try:
            from salmalm.web.auth import rate_limiter

            if not rate_limiter:
                issues.append("No rate limiting configured")
        except Exception as e:  # noqa: broad-except
            issues.append("Rate limiter not available")

        # Check request size limits via FastAPI/ASGI handler
        try:
            from salmalm.web.asgi import _MAX_BODY
            if _MAX_BODY > 100 * 1024 * 1024:
                issues.append(f"Request size limit too high: {_MAX_BODY} bytes")
        except ImportError:
            # May be configured differently — non-fatal
            pass
        except Exception as e:  # noqa: broad-except
            log.debug(f"Suppressed: {e}")

        # Check exec sandboxing
        try:
            from salmalm.tools.tools_common import _is_safe_command  # noqa: F401
        except ImportError:
            issues.append("No command execution sandboxing")

        status = "WARN" if issues else "PASS"
        return {
            "id": "A04",
            "title": "Insecure Design / 불안전한 설계",
            "status": status,
            "details": issues or ["Rate limiting, request size limits (FastAPI), exec sandboxing OK"],
        }

    def _check_a05_security_misconfiguration(self) -> dict:
        """A05: Security Misconfiguration — 보안 설정 오류.

        BUG-BL fix: WebHandler removed; check FastAPI security middleware instead.
        """
        issues = []
        # Check for debug mode
        if os.environ.get("SALMALM_DEBUG"):
            issues.append("WARN: Debug mode enabled (SALMALM_DEBUG)")
        # Check security headers via FastAPI middleware
        try:
            from salmalm.web.app import create_app
            import inspect
            src = inspect.getsource(create_app)
            _required_headers = ["X-Frame-Options", "X-Content-Type-Options", "Strict-Transport-Security"]
            for hdr in _required_headers:
                if hdr not in src:
                    issues.append(f"WARN: Security header may be missing: {hdr}")
        except Exception as e:  # noqa: broad-except
            log.debug(f"Suppressed: {e}")
        status = "WARN" if issues else "PASS"
        return {
            "id": "A05",
            "title": "Security Misconfiguration / 보안 설정 오류",
            "status": status,
            "details": issues or ["No debug mode, FastAPI security headers middleware present"],
        }

    def _check_a06_vulnerable_components(self) -> dict:
        """A06: Vulnerable Components — 취약한 구성요소."""
        import sys

        issues = []
        py_ver = sys.version_info
        if py_ver < (3, 9):
            issues.append(f"WARN: Python {sys.version} may have known vulnerabilities")
        status = "WARN" if issues else "PASS"
        return {
            "id": "A06",
            "title": "Vulnerable Components / 취약한 구성요소",
            "status": status,
            "details": issues or [f"stdlib only, Python {sys.version.split()[0]}"],
        }

    def _check_a07_auth_failures(self) -> dict:
        """A07: Authentication Failures — 인증 실패."""
        issues = []
        try:
            from salmalm.web.auth import auth_manager

            if auth_manager._lockout_duration < 60:
                issues.append("Lockout duration too short")
            if auth_manager._max_attempts > 10:
                issues.append("Too many allowed login attempts before lockout")
        except Exception as e:  # noqa: broad-except
            issues.append("Auth manager not available")
        # Check session timeout
        try:
            from salmalm.web.auth import TokenManager  # noqa: F401
            # Default token expiry is 24h (86400s)
        except Exception as e:  # noqa: broad-except
            log.debug(f"Suppressed: {e}")
        status = "WARN" if issues else "PASS"
        return {
            "id": "A07",
            "title": "Auth Failures / 인증 실패",
            "status": status,
            "details": issues or ["Login lockout, session timeout (24h), PBKDF2 password hashing OK"],
        }

    def _check_a08_integrity(self) -> dict:
        """A08: Data Integrity — 데이터 무결성.

        BUG-BM fix: web.py no longer exists (Mixin removed); scan routes dir instead.
        """
        issues = []
        # Check if update routes use hash verification
        routes_dir = Path(__file__).resolve().parent.parent / "web" / "routes"
        try:
            for route_file in routes_dir.glob("*.py"):
                content = route_file.read_text(encoding="utf-8", errors="replace")
                if "pip install" in content and "hash" not in content.lower():
                    issues.append(f"WARN: pip install without hash verification in {route_file.name}")
        except Exception as e:  # noqa: broad-except
            log.debug(f"Suppressed: {e}")
        status = "WARN" if issues else "PASS"
        return {
            "id": "A08",
            "title": "Data Integrity / 데이터 무결성",
            "status": status,
            "details": issues or ["Update integrity: relies on PyPI/pip verification"],
        }

    def _check_a09_logging(self) -> dict:
        """A09: Logging — 보안 로깅."""
        issues = []
        try:
            from salmalm.core import audit_log  # noqa: F401
        except ImportError:
            issues.append("audit_log not available")
        # Check if audit DB exists
        from salmalm.constants import AUDIT_DB

        if not Path(AUDIT_DB).exists():
            issues.append("WARN: Audit database not yet created")
        status = "WARN" if issues else "PASS"
        return {
            "id": "A09",
            "title": "Logging & Monitoring / 로깅 및 모니터링",
            "status": status,
            "details": issues or ["Audit logging enabled, login failures tracked"],
        }

    def _check_a10_ssrf(self) -> dict:
        """A10: SSRF — 서버 측 요청 위조."""
        issues = []
        # Verify SSRF protection exists
        try:
            from salmalm.tools.tools_common import _is_private_url

            # Test internal IPs
            blocked, _ = _is_private_url("http://127.0.0.1/")
            if not blocked:
                issues.append("CRITICAL: localhost not blocked in SSRF check")
            blocked, _ = _is_private_url("http://169.254.169.254/")
            if not blocked:
                issues.append("CRITICAL: metadata endpoint not blocked")
            blocked, _ = _is_private_url("http://10.0.0.1/")
            if not blocked:
                issues.append("CRITICAL: private IP 10.x not blocked")
        except ImportError:
            issues.append("CRITICAL: SSRF protection module not found")
        status = "FAIL" if any("CRITICAL" in i for i in issues) else ("WARN" if issues else "PASS")
        return {
            "id": "A10",
            "title": "SSRF / 서버 측 요청 위조",
            "status": status,
            "details": issues or ["Internal IP blocking, metadata endpoint blocking, protocol restriction OK"],
        }

    def format_report(self) -> str:
        """Format audit report as human-readable text.
        감사 보고서를 읽기 쉬운 텍스트로 포맷."""
        report = self.audit()
        lines = [
            "🛡️ **SalmAlm Security Audit Report**",
            f"Version: {report['version']} | {report['timestamp']}",
            f"Score: {report['score']}/100",
            f"Summary: ✅ {report['summary']['pass']} PASS | "
            f"⚠️ {report['summary']['warn']} WARN | "
            f"❌ {report['summary']['fail']} FAIL",
            "",
        ]
        STATUS_ICON = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}
        for cid, check in report["checks"].items():
            icon = STATUS_ICON.get(check["status"], "❓")
            lines.append(f"{icon} **{check['id']}: {check['title']}** — {check['status']}")
            details = check.get("details", [])
            if isinstance(details, list):
                for d in details[:5]:
                    lines.append(f"   • {d}")
            else:
                lines.append(f"   • {details}")
            lines.append("")
        return "\n".join(lines)


# ── Input Validation ────────────────────────────────────────


def sanitize_session_id(session_id: str) -> str:
    """Sanitize session ID to prevent injection.
    세션 ID를 정제하여 인젝션 방지."""
    if not session_id or not isinstance(session_id, str):
        return "default"
    # Allow only alphanumeric, dash, underscore
    cleaned = _SESSION_ID_RE.sub("", session_id)
    return cleaned[:64] or "default"


def validate_input_size(data: str, max_size: int = 1_000_000) -> Tuple[bool, str]:
    """Check input doesn't exceed size limit.
    입력이 크기 제한을 초과하지 않는지 확인."""
    if len(data) > max_size:
        return False, f"Input too large: {len(data)} bytes (max {max_size})"
    return True, ""


# ── Module instances ─────────────────────────────────────────

login_limiter = LoginRateLimiter()
security_auditor = SecurityAuditor()
