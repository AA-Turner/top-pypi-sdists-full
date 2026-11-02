"""Configuration management."""

import math
import os
from dataclasses import dataclass

DEFAULT_BASE_URL = "http://agentplatform.aliyun-inc.com"
CLUSTER_HEADER = "X-Cluster"


@dataclass(frozen=True)
class EnvVarSpec:
    """User-facing environment variable metadata."""

    name: str
    description: str
    category: str
    default: str | None = None
    required: str = "no"
    secret: bool = False
    legacy: bool = False
    overridden_by: tuple[str, ...] = ()


ENV_VAR_SPECS: tuple[EnvVarSpec, ...] = (
    EnvVarSpec(
        name="AP_ARTIFACT_MANIFEST_WAIT_TIMEOUT",
        description="Per-job artifact manifest wait budget in seconds, including polling and HTTP retries.",
        category="http",
        default="1800",
    ),
    EnvVarSpec(
        name="AP_BASE_URL",
        description="Agent Platform API endpoint.",
        category="connection",
        default=DEFAULT_BASE_URL,
    ),
    EnvVarSpec(
        name="AP_CLUSTER",
        description="Target cluster. Overrides X-Cluster in AP_HEADERS.",
        category="connection",
        required="conditional",
        overridden_by=("--cluster",),
    ),
    EnvVarSpec(
        name="AP_HEADERS",
        description="Extra HTTP headers, comma-separated as Header: value.",
        category="connection",
        required="conditional",
        secret=True,
    ),
    EnvVarSpec(
        name="AP_API_KEY",
        description="Single API key used by the CLI.",
        category="auth",
        required="yes",
        secret=True,
    ),
    EnvVarSpec(
        name="AP_AGENTHUB_REF",
        description="Default Agent-Hub branch or commit for template/job commands.",
        category="agenthub",
        overridden_by=("--agenthub-ref",),
    ),
    EnvVarSpec(
        name="AP_VERBOSE",
        description="Enable HTTP request/response logs and verbose tracebacks.",
        category="logging",
        default="false",
        overridden_by=("--verbose", "-v"),
    ),
    EnvVarSpec(
        name="AP_FORMAT",
        description="Default output format for commands: table or json. Empty keeps each command's own default.",
        category="output",
        default="",
        overridden_by=("--format",),
    ),
    EnvVarSpec(
        name="AP_VERBOSE_BODY_LIMIT",
        description="Body summary threshold in bytes for verbose logs.",
        category="logging",
        default="4096",
    ),
    EnvVarSpec(
        name="AP_VERBOSE_FULL_BODY",
        description="Print full verbose response/request bodies.",
        category="logging",
        default="false",
    ),
    EnvVarSpec(
        name="AP_VERBOSE_REDACTION",
        description="Mask sensitive fields in verbose logs.",
        category="logging",
        default="true",
    ),
    EnvVarSpec(
        name="AP_HTTP_MAX_ATTEMPTS",
        description="Total attempts for read-only HTTP requests; 0/1 disables retry.",
        category="http",
        default="3",
    ),
    EnvVarSpec(
        name="AP_CONNECT_TIMEOUT",
        description="HTTP connect timeout in seconds; 0 means no timeout.",
        category="http",
        default="300",
    ),
    EnvVarSpec(
        name="AP_REQUEST_TIMEOUT",
        description="HTTP read/request timeout in seconds; 0 means no timeout.",
        category="http",
        default="86400",
    ),
    EnvVarSpec(
        name="AP_CACHE_DIR",
        description="Default job export root and optional group export override.",
        category="export",
        default="~/.cache/agentplatform",
    ),
)


class ConfigurationError(Exception):
    """Raised when required client configuration is missing or invalid."""


def _parse_bool(value: str | None) -> bool:
    """Parse a boolean environment variable."""
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_bool_default(value: str | None, default: bool) -> bool:
    """Parse a boolean environment variable with an explicit default."""
    if value is None or not value.strip():
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_positive_int(value: str | None, default: int) -> int:
    """Parse a positive-integer environment variable."""
    if value is None or not value.strip():
        return default
    parsed = int(value)
    if parsed <= 0:
        raise ValueError("environment variable must be a positive integer")
    return parsed


def _parse_non_negative_int(name: str, value: str | None, default: int) -> int:
    """Parse a non-negative integer config value."""
    if value is None or not value.strip():
        return default
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be a non-negative integer") from exc
    if parsed < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    return parsed


# AP_FORMAT accepts these user-facing values (empty means "keep command default").
# plain = each command's original human output; table = prettified view; json = structured.
AP_FORMAT_CHOICES: tuple[str, ...] = ("plain", "table", "json")
# Internal render formats produced after normalization.
_RENDER_FORMATS = {"plain", "json", "yaml"}


def normalize_output_format(
    value: str | None, default: str = "plain", keep_table: bool = False
) -> str:
    """Resolve and normalize a command output format.

    Priority: explicit ``value`` (from ``--format``) > ``AP_FORMAT`` env > ``default``.
    ``None`` means the caller did not pass ``--format`` and env/default should apply.

    ``keep_table`` controls whether ``table`` is a distinct format: commands that
    provide a dedicated table/detail renderer pass ``keep_table=True`` so ``table``
    is preserved; all other commands leave it ``False`` so ``table`` folds to
    ``plain`` and their original (verbatim) output is used. ``text`` always folds to
    ``plain``. Raises ``ValueError`` on invalid input (callers convert to a CLI error).
    """
    if value is not None:
        resolved = value.strip().lower()
    else:
        env = os.environ.get("AP_FORMAT", "").strip().lower()
        if env and env not in AP_FORMAT_CHOICES:
            raise ValueError("AP_FORMAT must be one of: plain, table, json")
        resolved = env or default
    if resolved == "text":
        resolved = "plain"
    if resolved == "table" and not keep_table:
        resolved = "plain"
    allowed = _RENDER_FORMATS | ({"table"} if keep_table else set())
    if resolved not in allowed:
        raise ValueError("output format must be one of plain/table/json/yaml")
    return resolved


def has_cluster_header(headers: dict[str, str]) -> bool:
    return any(key.lower() == "x-cluster" and value.strip() for key, value in headers.items())


def _set_cluster_header(headers: dict[str, str], cluster: str) -> None:
    for key in list(headers):
        if key.lower() == "x-cluster":
            del headers[key]
    headers[CLUSTER_HEADER] = cluster


@dataclass
class Config:
    """CLI 配置

    认证: 支持以下方式
        - AP_API_KEY: CLI 当前请求使用的单个 API Key（推荐）
        - AP_API_KEYS: 向后兼容；CLI 侧只接受单个 key，服务端才使用逗号分隔列表
        - AP_TOKEN_KEY: 向后兼容的旧环境变量名
    """

    base_url: str
    headers: dict
    agenthub_ref: str | None
    verbose: bool = False
    verbose_body_limit: int = 4096
    verbose_full_body: bool = False
    verbose_redaction: bool = True
    token_key: str | None = None
    http_max_attempts: int = 3
    artifact_manifest_wait_timeout: float = 1800

    @classmethod
    def from_env(cls, cluster: str | None = None) -> "Config":
        """从环境变量加载配置"""
        base_url = os.environ.get("AP_BASE_URL") or DEFAULT_BASE_URL
        base_url_explicitly_set = "AP_BASE_URL" in os.environ

        headers: dict[str, str] = {}
        headers_str = os.environ.get("AP_HEADERS", "")
        if headers_str:
            for h in headers_str.split(","):
                if ":" in h:
                    k, v = h.split(":", 1)
                    headers[k.strip()] = v.strip()

        token_key = _resolve_token_key()

        effective_cluster = (
            cluster.strip() if cluster is not None else os.environ.get("AP_CLUSTER", "").strip()
        )
        if effective_cluster:
            _set_cluster_header(headers, effective_cluster)

        # 网关要求：携带 Env header 才能放行 /apis/ 路径。
        # 根据 cluster 注入对应的 Env header：debug→debug, test→test, 其他→product。
        # 用户也可通过 AP_HEADERS="Env:xxx" 显式设定。
        if not any(k.lower() == "env" for k in headers):
            cluster_lower = effective_cluster.lower()
            if cluster_lower == "debug":
                headers["Env"] = "debug"
            elif cluster_lower == "test":
                headers["Env"] = "test"
            else:
                headers["Env"] = "product"

        # 本地模式自动切换 base_url：当 headers 中包含 X-Cluster:local 时，
        # 将 base_url 覆盖为本地 Agent-Platform 服务地址，
        # 避免请求发到远程 nginx 服务器导致 405 错误。
        # 仅在用户未通过 AP_BASE_URL 环境变量显式设置时生效。
        if not base_url_explicitly_set:
            for key, value in headers.items():
                if key.lower() == "x-cluster" and value.lower() == "local":
                    base_url = "http://localhost:9000"
                    break

        return cls(
            base_url=base_url.rstrip("/"),
            headers=headers,
            agenthub_ref=os.environ.get("AP_AGENTHUB_REF"),
            verbose=_parse_bool(os.environ.get("AP_VERBOSE")),
            verbose_body_limit=_parse_positive_int(os.environ.get("AP_VERBOSE_BODY_LIMIT"), 4096),
            verbose_full_body=_parse_bool(os.environ.get("AP_VERBOSE_FULL_BODY")),
            verbose_redaction=_parse_bool_default(os.environ.get("AP_VERBOSE_REDACTION"), True),
            token_key=token_key,
            artifact_manifest_wait_timeout=_manifest_wait_timeout(),
            http_max_attempts=_parse_non_negative_int(
                "AP_HTTP_MAX_ATTEMPTS",
                os.environ.get("AP_HTTP_MAX_ATTEMPTS"),
                3,
            ),
        )


def _resolve_token_key() -> str | None:
    """Resolve the single API key used by the CLI."""
    for env_name in ("AP_API_KEY", "AP_API_KEYS", "AP_TOKEN_KEY"):
        value = os.environ.get(env_name)
        if value is None or not value.strip():
            continue
        token_key = value.strip()
        if "," in token_key:
            raise ConfigurationError(
                f"{env_name} must contain exactly one API key for the CLI; "
                "server-side AP_API_KEYS is the comma-separated allowlist."
            )
        return token_key
    return None


def get_config(
    verbose: bool | None = None,
    agenthub_ref: str | None = None,
    http_max_attempts: int | None = None,
    cluster: str | None = None,
) -> Config:
    """Return the current configuration."""
    config = Config.from_env(cluster=cluster)
    if verbose is not None:
        config.verbose = verbose
    if agenthub_ref is not None:
        config.agenthub_ref = agenthub_ref.strip() or None
    if http_max_attempts is not None:
        config.http_max_attempts = http_max_attempts
    return config


def _manifest_wait_timeout() -> float:
    name = "AP_ARTIFACT_MANIFEST_WAIT_TIMEOUT"
    raw = os.environ.get(name, "1800")
    try:
        value = float(raw)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be a finite positive number") from exc
    if not math.isfinite(value) or value <= 0:
        raise ConfigurationError(f"{name} must be a finite positive number")
    return value
