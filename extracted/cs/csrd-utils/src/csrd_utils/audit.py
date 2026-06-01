"""Security hardening audit checks for generated services."""

import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Literal


@dataclass
class AuditFinding:
    """A single hardening finding."""

    rule: str
    severity: Literal["high", "medium", "low"]
    message: str
    file: str
    evidence: str
    remediation: str


@dataclass
class AuditReport:
    """Structured audit output."""

    ok: bool
    findings: list[AuditFinding] = field(default_factory=list)

    def to_payload(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "findings": [asdict(finding) for finding in self.findings],
            "summary": {
                "high": sum(1 for finding in self.findings if finding.severity == "high"),
                "medium": sum(1 for finding in self.findings if finding.severity == "medium"),
                "low": sum(1 for finding in self.findings if finding.severity == "low"),
            },
        }


_WEAK_PASSWORDS = r"(?:change_me|change_me_root|app|sandbox|password|root)"
_WEAK_IDENTIFIERS = r"(?:service_user|service_db|service_rabbit|app|sandbox)"
_WEAK_JWT_SECRETS = r"(?:changeme[^\s]*|secret|test|jwt[_-]?secret|please[_-]?change)"

# Infra ports that should not be host-bound in production
_INFRA_PORT_PATTERNS = re.compile(
    r'"(?:0\.0\.0\.0:)?(\d+):(\d+)"',
)
_SENSITIVE_INFRA_PORTS = {"5432", "3306", "6379", "5672", "15672", "27017"}


def _scan_file(path: Path, root: Path) -> list[AuditFinding]:
    findings: list[AuditFinding] = []

    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return findings

    rel = str(path.relative_to(root))

    password_hits = re.findall(
        rf"(?:DB_PASSWORD|POSTGRES_PASSWORD|MYSQL_PASSWORD|MARIADB_PASSWORD)\s*[:=]\s*['\"]?({_WEAK_PASSWORDS})['\"]?",
        text,
        flags=re.IGNORECASE,
    )
    if password_hits:
        findings.append(
            AuditFinding(
                rule="weak-db-password-default",
                severity="high",
                message="Weak default database password is configured.",
                file=rel,
                evidence=password_hits[0],
                remediation="Set a strong DB password via environment configuration.",
            )
        )

    root_hits = re.findall(
        rf"(?:MYSQL_ROOT_PASSWORD|MARIADB_ROOT_PASSWORD)\s*[:=]\s*['\"]?({_WEAK_PASSWORDS})['\"]?",
        text,
        flags=re.IGNORECASE,
    )
    if root_hits:
        findings.append(
            AuditFinding(
                rule="weak-root-db-password-default",
                severity="high",
                message="Weak root database password is configured.",
                file=rel,
                evidence=root_hits[0],
                remediation="Set a strong root password and avoid shared defaults.",
            )
        )

    identifier_hits = re.findall(
        rf"(?:DB_USER|POSTGRES_USER|MYSQL_USER|MARIADB_USER|DB_NAME|POSTGRES_DB|MYSQL_DATABASE|MARIADB_DATABASE|RABBITMQ_(?:DEFAULT_)?USER)\s*[:=]\s*['\"]?({_WEAK_IDENTIFIERS})['\"]?",
        text,
        flags=re.IGNORECASE,
    )
    if identifier_hits:
        findings.append(
            AuditFinding(
                rule="weak-db-identifier-default",
                severity="medium",
                message="Weak default DB user/database identifier is configured.",
                file=rel,
                evidence=identifier_hits[0],
                remediation="Set DB_USER and DB_NAME to service-specific values per environment.",
            )
        )

    if "include_actuator_endpoints=True" in text or "INCLUDE_ACTUATOR_ENDPOINTS=true" in text:
        findings.append(
            AuditFinding(
                rule="actuator-endpoints-enabled",
                severity="medium",
                message="Actuator endpoints are enabled by default.",
                file=rel,
                evidence="include_actuator_endpoints=True",
                remediation="Set INCLUDE_ACTUATOR_ENDPOINTS=false unless required on trusted networks.",
            )
        )

    if 'allow_origins=["*"]' in text or "allow_origins=['*']" in text:
        findings.append(
            AuditFinding(
                rule="cors-wildcard-origin",
                severity="medium",
                message="CORS wildcard origin is configured.",
                file=rel,
                evidence='allow_origins=["*"]',
                remediation="Restrict CORS to known trusted origins.",
            )
        )

    if "guest:guest" in text:
        findings.append(
            AuditFinding(
                rule="rabbitmq-guest-default",
                severity="medium",
                message="RabbitMQ guest credentials are configured.",
                file=rel,
                evidence="guest:guest",
                remediation="Set RABBITMQ_USER and RABBITMQ_PASSWORD explicitly.",
            )
        )

    if "--reload" in text:
        findings.append(
            AuditFinding(
                rule="dev-reload-usage",
                severity="low",
                message="Development reload mode appears in runnable commands.",
                file=rel,
                evidence="--reload",
                remediation="Avoid reload mode in production run commands.",
            )
        )

    # ── New rules (M3 expansion) ──────────────────────────────────────

    # Weak JWT secret
    jwt_hits = re.findall(
        rf"JWT_SECRET\s*[:=]\s*['\"]?({_WEAK_JWT_SECRETS})['\"]?",
        text,
        flags=re.IGNORECASE,
    )
    if jwt_hits:
        findings.append(
            AuditFinding(
                rule="weak-jwt-secret",
                severity="high",
                message="JWT signing secret uses a weak or default value.",
                file=rel,
                evidence=jwt_hits[0],
                remediation='Generate a strong random secret: python -c "import secrets; print(secrets.token_urlsafe(48))"',
            )
        )

    # Weak RabbitMQ password
    rabbit_pw_hits = re.findall(
        rf"RABBITMQ_(?:DEFAULT_)?PASS(?:WORD)?\s*[:=]\s*['\"]?({_WEAK_PASSWORDS})['\"]?",
        text,
        flags=re.IGNORECASE,
    )
    if rabbit_pw_hits:
        findings.append(
            AuditFinding(
                rule="weak-rabbitmq-password",
                severity="high",
                message="RabbitMQ password uses a weak default.",
                file=rel,
                evidence=rabbit_pw_hits[0],
                remediation="Set a strong RABBITMQ_PASSWORD via environment configuration.",
            )
        )

    # Redis URL without authentication
    redis_no_auth = re.findall(
        r"(?:REDIS_URL|BROKER_URL|CELERY_BROKER_URL|RESULT_BACKEND)\s*[:=]\s*['\"]?(redis://[^:@\s]*:\d+)",
        text,
        flags=re.IGNORECASE,
    )
    if redis_no_auth:
        findings.append(
            AuditFinding(
                rule="redis-no-auth",
                severity="medium",
                message="Redis URL has no password — any network client can read/write data.",
                file=rel,
                evidence=redis_no_auth[0],
                remediation="Add requirepass to Redis and use redis://:PASSWORD@host:port in URLs.",
            )
        )

    # Exposed infra ports in docker-compose (only scan compose files)
    if path.name in ("docker-compose.yml", "docker-compose.yaml"):
        for match in _INFRA_PORT_PATTERNS.finditer(text):
            host_port = match.group(1)
            if host_port in _SENSITIVE_INFRA_PORTS:
                # Check if bound to 127.0.0.1 — that's acceptable
                full_match = match.group(0)
                if "127.0.0.1" not in full_match:
                    findings.append(
                        AuditFinding(
                            rule="exposed-infra-port",
                            severity="medium",
                            message=f"Infrastructure port {host_port} is bound to all interfaces.",
                            file=rel,
                            evidence=full_match,
                            remediation="Bind to 127.0.0.1 for dev or remove host mapping for prod.",
                        )
                    )

    # Debug mode enabled
    debug_hits = re.findall(
        r"(?:^|\n)\s*DEBUG\s*[:=]\s*['\"]?(?:true|1|yes)['\"]?",
        text,
        flags=re.IGNORECASE,
    )
    if debug_hits:
        findings.append(
            AuditFinding(
                rule="debug-mode-enabled",
                severity="medium",
                message="Debug mode is enabled — may expose stack traces and internal state.",
                file=rel,
                evidence="DEBUG=true",
                remediation="Set DEBUG=false in production environments.",
            )
        )

    # Shell-form CMD in Dockerfiles (no signal forwarding)
    if path.name.startswith("Dockerfile"):
        cmd_hits = re.findall(r"^CMD\s+(?!exec\b)(?!\[)(.+)$", text, flags=re.MULTILINE)
        if cmd_hits:
            findings.append(
                AuditFinding(
                    rule="shell-form-cmd",
                    severity="medium",
                    message="Dockerfile CMD uses shell form without exec — no signal forwarding.",
                    file=rel,
                    evidence=f"CMD {cmd_hits[0][:60]}",
                    remediation="Use 'CMD exec ...' or CMD in JSON array form for proper signal handling.",
                )
            )

    return findings


def run_audit(service_root: Path) -> AuditReport:
    """Scan a service path for insecure defaults and weak auto-configuration."""
    root = service_root.resolve()
    findings: list[AuditFinding] = []

    if not root.exists() or not root.is_dir():
        findings.append(
            AuditFinding(
                rule="invalid-service-path",
                severity="high",
                message="Service path does not exist or is not a directory.",
                file=str(service_root),
                evidence=str(service_root),
                remediation="Provide a valid service root path.",
            )
        )
        return AuditReport(ok=False, findings=findings)

    candidates: list[Path] = []
    include_names = {
        "docker-compose.yml",
        "docker-compose.yaml",
        ".env",
        ".env.example",
        "README.md",
        "settings.py",
    }

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if (
            path.name in include_names
            or path.name.startswith("Dockerfile")
            or path.suffix in {".py", ".yml", ".yaml", ".env", ".md"}
        ):
            candidates.append(path)

    seen: set[tuple[str, str, str]] = set()
    for path in candidates:
        for finding in _scan_file(path, root):
            key = (finding.rule, finding.file, finding.evidence)
            if key in seen:
                continue
            seen.add(key)
            findings.append(finding)

    has_high = any(finding.severity == "high" for finding in findings)
    return AuditReport(ok=not has_high, findings=findings)
