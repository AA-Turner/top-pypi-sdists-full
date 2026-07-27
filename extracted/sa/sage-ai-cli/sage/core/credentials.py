"""Secure credential bootstrap helpers for SAGE.

These helpers intentionally keep raw secret values out of model prompts.
SAGE can import existing credentials from the local environment or config,
generate local-only secrets when safe, and persist them to `.env` files
without ever asking the model to fabricate values.
"""

from __future__ import annotations

import configparser
import json
import os
import re
import secrets
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping
from urllib.parse import quote

HOME_ENV_PATH = Path.home() / ".sage" / ".env"
PROJECT_ENV_FILENAMES = (".env", ".env.local")
DISCOVERY_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".sh",
}
DISCOVERY_SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "dist",
    "build",
    "htmlcov",
    ".sage",
}
DISCOVERY_LIMIT = 600

ENV_PATTERNS = (
    re.compile(r"""os\.environ(?:\.get)?\(\s*["']([A-Z][A-Z0-9_]+)["']"""),
    re.compile(r"""os\.getenv\(\s*["']([A-Z][A-Z0-9_]+)["']"""),
    re.compile(r"""env_var\s*=\s*["']([A-Z][A-Z0-9_]+)["']"""),
    re.compile(r"""process\.env\.([A-Z][A-Z0-9_]+)"""),
    re.compile(r"""Deno\.env\.get\(\s*["']([A-Z][A-Z0-9_]+)["']"""),
    re.compile(r"""import\.meta\.env\.([A-Z][A-Z0-9_]+)"""),
)

EXTERNAL_CREDENTIAL_URLS: dict[str, str] = {
    "OPENAI_API_KEY": "https://platform.openai.com/api-keys",
    "ANTHROPIC_API_KEY": "https://console.anthropic.com/settings/keys",
    "GEMINI_API_KEY": "https://aistudio.google.com/app/apikey",
    "SAGE_GEMINI_API_KEY": "https://aistudio.google.com/app/apikey",
    "GROQ_API_KEY": "https://console.groq.com/keys",
    "SAGE_GROQ_API_KEY": "https://console.groq.com/keys",
    "OPENROUTER_API_KEY": "https://openrouter.ai/keys",
    "SAGE_OPENROUTER_API_KEY": "https://openrouter.ai/keys",
    "CEREBRAS_API_KEY": "https://cloud.cerebras.ai",
    "SAGE_CEREBRAS_API_KEY": "https://cloud.cerebras.ai",
    "SAMBANOVA_API_KEY": "https://cloud.sambanova.ai",
    "SAGE_SAMBANOVA_API_KEY": "https://cloud.sambanova.ai",
    "TOGETHER_API_KEY": "https://api.together.xyz/settings/api-keys",
    "SAGE_TOGETHER_API_KEY": "https://api.together.xyz/settings/api-keys",
    "MISTRAL_API_KEY": "https://console.mistral.ai/api-keys/",
    "SAGE_MISTRAL_API_KEY": "https://console.mistral.ai/api-keys/",
    "COHERE_API_KEY": "https://dashboard.cohere.com/api-keys",
    "SAGE_COHERE_API_KEY": "https://dashboard.cohere.com/api-keys",
    "DEEPSEEK_API_KEY": "https://platform.deepseek.com/api_keys",
    "SAGE_DEEPSEEK_API_KEY": "https://platform.deepseek.com/api_keys",
    "DEEPINFRA_API_KEY": "https://deepinfra.com/dash/api_keys",
    "SAGE_DEEPINFRA_API_KEY": "https://deepinfra.com/dash/api_keys",
    "GITHUB_TOKEN": "https://github.com/settings/tokens",
    "STRIPE_API_KEY": "https://dashboard.stripe.com/apikeys",
    "STRIPE_SECRET_KEY": "https://dashboard.stripe.com/apikeys",
}

CONFIG_API_KEY_ALIASES: dict[str, str] = {
    "SAGE_GEMINI_API_KEY": "gemini",
    "GEMINI_API_KEY": "gemini",
    "SAGE_GROQ_API_KEY": "groq",
    "GROQ_API_KEY": "groq",
    "SAGE_OPENROUTER_API_KEY": "openrouter",
    "OPENROUTER_API_KEY": "openrouter",
    "SAGE_CEREBRAS_API_KEY": "cerebras",
    "CEREBRAS_API_KEY": "cerebras",
    "SAGE_SAMBANOVA_API_KEY": "sambanova",
    "SAMBANOVA_API_KEY": "sambanova",
    "SAGE_TOGETHER_API_KEY": "together",
    "TOGETHER_API_KEY": "together",
    "SAGE_MISTRAL_API_KEY": "mistral",
    "MISTRAL_API_KEY": "mistral",
    "SAGE_COHERE_API_KEY": "cohere",
    "COHERE_API_KEY": "cohere",
    "SAGE_DEEPSEEK_API_KEY": "deepseek",
    "DEEPSEEK_API_KEY": "deepseek",
    "SAGE_DEEPINFRA_API_KEY": "deepinfra",
    "DEEPINFRA_API_KEY": "deepinfra",
    "GITHUB_TOKEN": "github",
}

CLOUD_PROVIDER_ALIASES: dict[str, str] = {
    "gcp": "gcp",
    "gcloud": "gcp",
    "google cloud": "gcp",
    "google cloud platform": "gcp",
    "cloud run": "gcp",
    "aws": "aws",
    "amazon web services": "aws",
    "ecs": "aws",
    "lambda": "aws",
    "azure": "azure",
    "azure cloud": "azure",
    "azure app service": "azure",
    "cloudflare": "cloudflare",
    "workers": "cloudflare",
    "vercel": "vercel",
    "railway": "railway",
    "render": "render",
    "fly": "flyio",
    "fly.io": "flyio",
    "flyio": "flyio",
}

CLOUD_PROVIDER_LABELS: dict[str, str] = {
    "gcp": "Google Cloud",
    "aws": "AWS",
    "azure": "Azure",
    "cloudflare": "Cloudflare",
    "vercel": "Vercel",
    "railway": "Railway",
    "render": "Render",
    "flyio": "Fly.io",
}

CLOUD_PROVIDER_SETUP_URLS: dict[str, str] = {
    "gcp": "https://cloud.google.com/sdk/gcloud",
    "aws": "https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html",
    "azure": "https://learn.microsoft.com/cli/azure/get-started-with-azure-cli",
    "cloudflare": "https://developers.cloudflare.com/fundamentals/api/get-started/create-token/",
    "vercel": "https://vercel.com/docs/cli",
    "railway": "https://docs.railway.com/guides/cli",
    "render": "https://render.com/docs/blueprint-spec",
    "flyio": "https://fly.io/docs/hands-on/install-flyctl/",
}


@dataclass(frozen=True)
class CredentialRecord:
    """Metadata for one imported or generated credential."""

    name: str
    source: str
    kind: str


@dataclass
class CredentialBootstrapResult:
    """Result of bootstrapping credential files for a project."""

    project_root: Path
    env_path: Path
    example_path: Path
    values: dict[str, str] = field(default_factory=dict)
    loaded_env_files: list[str] = field(default_factory=list)
    imported: list[CredentialRecord] = field(default_factory=list)
    generated: list[CredentialRecord] = field(default_factory=list)
    missing_external: dict[str, str] = field(default_factory=dict)
    gitignore_updated: bool = False
    sqlite_database_path: Path | None = None
    cloud_provider: str | None = None

    def prompt_summary(self) -> str:
        """Return a prompt-safe summary with variable names only."""
        lines = [
            "## SECURE CREDENTIAL BOOTSTRAP (ALREADY PERFORMED BY SAGE)",
            "SAGE prepared secret storage outside the model so you must NOT invent, print, or echo raw credential values.",
        ]
        if self.cloud_provider:
            provider_label = CLOUD_PROVIDER_LABELS.get(self.cloud_provider, self.cloud_provider)
            lines.append(f"- Confirmed deployment target: {provider_label}.")
        if self.loaded_env_files:
            lines.append(
                "- Loaded local credential sources: "
                + ", ".join(self.loaded_env_files)
            )
        if self.imported:
            lines.append(
                "- Imported existing real credentials into `.env`: "
                + ", ".join(record.name for record in self.imported)
            )
        if self.generated:
            lines.append(
                "- Generated real local-only credentials: "
                + ", ".join(record.name for record in self.generated)
            )
        if self.sqlite_database_path:
            lines.append(
                "- Created a real local SQLite database backing file and stored its URL in `.env`."
            )
        if self.missing_external:
            missing = "; ".join(
                f"{name} ({url})" for name, url in sorted(self.missing_external.items())
            )
            lines.append(
                "- Missing external credentials were NOT fabricated: " + missing
            )
        lines.extend(
            [
                "Rules:",
                "- Reuse the `.env` and `.env.example` files SAGE already wrote.",
                "- Keep `.env.example` blank or redacted; never put fake values in it.",
                "- If you create app/database services, wire them to the existing env variable names.",
                "- If a cloud provider is confirmed, use only that provider's native deployment/auth/logging/rollback patterns.",
                "- If an external credential is still missing, report the exact variable name and acquisition URL instead of guessing.",
            ]
        )
        return "\n".join(lines)


def normalize_cloud_provider(value: str) -> str:
    """Normalize a cloud-provider name to a stable internal identifier."""
    candidate = (value or "").strip().lower()
    if not candidate:
        return ""

    if candidate in CLOUD_PROVIDER_ALIASES:
        return CLOUD_PROVIDER_ALIASES[candidate]

    for alias, provider in sorted(CLOUD_PROVIDER_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        if alias in candidate:
            return provider
    return ""


def detect_target_cloud_provider(request_text: str, preferred_cloud: str = "") -> str:
    """Detect the target cloud provider from the request or saved preference."""
    preferred = normalize_cloud_provider(preferred_cloud)
    if preferred:
        return preferred

    lower = (request_text or "").lower()
    for alias, provider in sorted(CLOUD_PROVIDER_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        if alias in lower:
            return provider
    return ""


def parse_env_file(path: Path) -> dict[str, str]:
    """Parse a simple dotenv file into a dictionary.

    Mirrors python-dotenv's behavior for the common cases:
      - Skips blank lines and #-prefixed comments
      - Strips `export ` prefix
      - Removes balanced surrounding single/double quotes
      - Strips trailing ` # comment` (whitespace + #) on UNQUOTED values
        (python-dotenv does this; without it, a line like
        `PORT=8090  # local` ends up with value `'8090  # local'`, which
        breaks any downstream code that expects a clean integer.)
    """
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    try:
        content = path.read_text("utf-8")
    except OSError:
        return values

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, raw_value = line.split("=", 1)
        key = key.strip()
        value = raw_value.strip()
        if not key:
            continue
        # Strip inline comment from an unquoted value. We only treat `#` as a
        # comment when there's whitespace before it; `#` inside a value like
        # `password=ab#cd` shouldn't be split. Don't strip if the value is
        # quoted — the `#` is then part of the string.
        is_quoted = (len(value) >= 2 and value[0] == value[-1]
                     and value[0] in {'"', "'"})
        if not is_quoted:
            # Find the first `#` that's preceded by whitespace
            for i, ch in enumerate(value):
                if ch == "#" and i > 0 and value[i - 1].isspace():
                    value = value[:i].rstrip()
                    break
        if is_quoted:
            value = value[1:-1]
        values[key] = value
    return values


def find_project_root(start_path: Path | None = None) -> Path:
    """Find the project root by searching upwards for marker files."""
    curr = (start_path or Path.cwd()).resolve()
    # Check current and parents for common project markers
    for parent in [curr, *curr.parents]:
        if (parent / "pyproject.toml").exists() or (parent / ".git").exists() or (parent / ".env").exists():
            # If we found a root, also check if it has an 'ai-platform' subdirectory
            # which is our actual project root in this repo structure.
            if (parent / "ai-platform" / ".env").exists():
                return parent / "ai-platform"
            return parent
    return curr


def load_project_env_files(project_root: Path, override: bool = False) -> list[str]:
    """Load shared and project-local `.env` files into `os.environ`."""
    # Discover actual project root if we're in a subdirectory or repo root
    actual_root = find_project_root(project_root)
    
    loaded: list[str] = []
    original_env_keys = set(os.environ)
    
    # Paths to search for .env files
    search_paths = [
        HOME_ENV_PATH,
        *(actual_root / name for name in PROJECT_ENV_FILENAMES)
    ]
    
    # Special case: if we're in the repo root but .env is in ai-platform/
    if actual_root.name != "ai-platform" and (actual_root / "ai-platform" / ".env").exists():
        search_paths.append(actual_root / "ai-platform" / ".env")

    # Vite frontend secrets (Firebase VITE_*, etc.)
    fe_env = actual_root / "frontend" / ".env"
    if fe_env.exists():
        search_paths.append(fe_env)

    for path in search_paths:
        if not path.exists():
            continue
            
        values = parse_env_file(path)
        if not values:
            continue
        for key, value in values.items():
            if override or key not in original_env_keys or path != HOME_ENV_PATH:
                os.environ[key] = value
        loaded.append(str(path))
    return loaded


def discover_required_env_vars(project_root: Path, request_text: str = "") -> list[str]:
    """Discover likely credential/env variables referenced by the project."""
    discovered: set[str] = set()

    for match in re.findall(r"\b([A-Z][A-Z0-9_]{2,})\b", request_text):
        if _looks_like_env_var(match):
            discovered.add(match)

    file_count = 0
    from sage.core.project import safe_walk
    for path in safe_walk(project_root):
        if file_count >= DISCOVERY_LIMIT:
            break
        if not path.is_file():
            continue
        if path.name.startswith(".env"):
            discovered.update(parse_env_file(path).keys())
            file_count += 1
            continue
        if path.suffix.lower() not in DISCOVERY_EXTENSIONS:
            continue
        try:
            text = path.read_text("utf-8", errors="ignore")
        except OSError:
            continue
        for pattern in ENV_PATTERNS:
            discovered.update(match for match in pattern.findall(text) if _looks_like_env_var(match))
        file_count += 1

    request_lower = request_text.lower()
    if any(token in request_lower for token in ("database", "db url", "database url", "postgres", "sql")):
        discovered.add("DATABASE_URL")
    if any(token in request_lower for token in ("secret", "credential", ".env", "auth", "jwt", "token")):
        if not any(_is_local_secret_var(name) for name in discovered):
            discovered.add("APP_SECRET_KEY")

    return sorted(discovered)


def bootstrap_project_credentials(
    project_root: Path,
    request_text: str = "",
    *,
    config_api_keys: Mapping[str, str] | None = None,
    preferred_cloud: str = "",
) -> CredentialBootstrapResult:
    """Create or refresh secure project credential files without exposing values to the model."""
    project_root = project_root.resolve()
    load_sources = load_project_env_files(project_root, override=False)

    env_path = project_root / ".env"
    example_path = project_root / ".env.example"
    existing_project_env = parse_env_file(env_path)
    home_env = parse_env_file(HOME_ENV_PATH)
    required_vars = discover_required_env_vars(project_root, request_text)
    cloud_provider = detect_target_cloud_provider(request_text, preferred_cloud)
    cloud_bundle, cloud_missing = _build_cloud_bundle(cloud_provider)
    if cloud_bundle:
        required_vars = sorted(set(required_vars) | set(cloud_bundle))

    result = CredentialBootstrapResult(
        project_root=project_root,
        env_path=env_path,
        example_path=example_path,
        loaded_env_files=load_sources,
        cloud_provider=cloud_provider or None,
    )

    resolved_values = dict(existing_project_env)
    database_bundle, sqlite_path = _build_database_bundle(project_root, required_vars, request_text)
    result.sqlite_database_path = sqlite_path

    for name in required_vars:
        if name in resolved_values:
            continue

        value, source = _resolve_existing_value(
            name,
            config_api_keys=config_api_keys or {},
            home_env=home_env,
            project_env=existing_project_env,
        )
        if value is not None:
            resolved_values[name] = value
            result.imported.append(
                CredentialRecord(name=name, source=source, kind=_classify_credential_kind(name))
            )
            continue

        generated = None
        if name in database_bundle:
            generated = database_bundle[name]
        elif name in cloud_bundle:
            generated = cloud_bundle[name]
        elif _is_local_secret_var(name):
            generated = _generate_local_secret(name)
        elif _is_database_component_var(name) and name in database_bundle:
            generated = database_bundle[name]

        if generated is not None:
            resolved_values[name] = generated
            result.generated.append(
                CredentialRecord(name=name, source="generated", kind=_classify_credential_kind(name))
            )
            continue

        if _is_external_credential_var(name):
            result.missing_external[name] = EXTERNAL_CREDENTIAL_URLS.get(
                name,
                f"https://www.google.com/search?q={name}+api+key",
            )

    for name, url in cloud_missing.items():
        result.missing_external.setdefault(name, url)

    result.values = resolved_values
    _write_env_file(env_path, resolved_values)
    _write_env_example(example_path, required_vars, resolved_values, result.missing_external)
    result.gitignore_updated = _ensure_gitignore(project_root)
    try:
        from sage.core.env_sync import ensure_gitignore_for_monorepo

        if ensure_gitignore_for_monorepo(project_root):
            result.gitignore_updated = True
    except Exception:
        pass
    return result


def _resolve_existing_value(
    name: str,
    *,
    config_api_keys: Mapping[str, str],
    home_env: Mapping[str, str],
    project_env: Mapping[str, str],
) -> tuple[str | None, str]:
    """Resolve an existing credential value without generating a new one."""
    if name in project_env:
        return project_env[name], "project_env"
    if name in os.environ:
        return os.environ[name], "environment"
    if name in home_env:
        return home_env[name], "home_env"

    config_key = CONFIG_API_KEY_ALIASES.get(name)
    if config_key and config_api_keys.get(config_key):
        return str(config_api_keys[config_key]), "sage_config"
    return None, ""


def _build_database_bundle(
    project_root: Path,
    required_vars: list[str],
    request_text: str,
) -> tuple[dict[str, str], Path | None]:
    """Generate concrete local database-related values when the request needs them."""
    relevant = {name for name in required_vars if _is_database_url_var(name) or _is_database_component_var(name)}
    if not relevant and "database" not in request_text.lower() and "db" not in request_text.lower():
        return {}, None

    prefers_postgres = any(
        name.startswith(("POSTGRES_", "PG"))
        for name in relevant
    ) or any(token in request_text.lower() for token in ("postgres", "postgresql"))

    slug = _slugify(project_root.name or "app")
    if prefers_postgres:
        password = secrets.token_urlsafe(24)
        user = "sage"
        db_name = slug
        url = f"postgresql://{user}:{quote(password)}@localhost:5432/{db_name}"
        return (
            {
                "DATABASE_URL": url,
                "POSTGRES_USER": user,
                "POSTGRES_PASSWORD": password,
                "POSTGRES_DB": db_name,
                "DB_HOST": "localhost",
                "DB_PORT": "5432",
            },
            None,
        )

    data_dir = project_root / ".sage" / "generated"
    data_dir.mkdir(parents=True, exist_ok=True)
    sqlite_path = data_dir / f"{slug}.db"
    sqlite_path.touch(exist_ok=True)
    url = f"sqlite:///{sqlite_path}"
    return (
        {
            "DATABASE_URL": url,
            "SQLALCHEMY_DATABASE_URI": url,
        },
        sqlite_path,
    )


def _build_cloud_bundle(provider: str) -> tuple[dict[str, str], dict[str, str]]:
    """Import concrete cloud metadata/credentials for a confirmed deployment target."""
    normalized = normalize_cloud_provider(provider)
    if not normalized:
        return {}, {}

    builders = {
        "gcp": _build_gcp_bundle,
        "aws": _build_aws_bundle,
        "azure": _build_azure_bundle,
        "cloudflare": lambda: _build_token_provider_bundle(
            "cloudflare",
            ("CLOUDFLARE_API_TOKEN", "CLOUDFLARE_ACCOUNT_ID"),
        ),
        "vercel": lambda: _build_token_provider_bundle(
            "vercel",
            ("VERCEL_TOKEN", "VERCEL_ORG_ID", "VERCEL_PROJECT_ID"),
        ),
        "railway": lambda: _build_token_provider_bundle("railway", ("RAILWAY_TOKEN",)),
        "render": lambda: _build_token_provider_bundle("render", ("RENDER_API_KEY",)),
        "flyio": lambda: _build_token_provider_bundle(
            "flyio",
            ("FLY_API_TOKEN", "FLY_APP_NAME", "FLY_REGION"),
        ),
    }
    builder = builders.get(normalized)
    if not builder:
        return {"CLOUD_PROVIDER": normalized}, {}
    return builder()


def _build_gcp_bundle() -> tuple[dict[str, str], dict[str, str]]:
    bundle: dict[str, str] = {"CLOUD_PROVIDER": "gcp"}
    missing: dict[str, str] = {}

    project = (
        os.environ.get("GOOGLE_CLOUD_PROJECT")
        or os.environ.get("CLOUDSDK_CORE_PROJECT")
        or _run_cli_text(["gcloud", "config", "get-value", "project"])
    )
    region = (
        os.environ.get("GOOGLE_CLOUD_REGION")
        or os.environ.get("CLOUDSDK_COMPUTE_REGION")
        or _run_cli_text(["gcloud", "config", "get-value", "run/region"])
        or _run_cli_text(["gcloud", "config", "get-value", "compute/region"])
    )
    account = os.environ.get("GOOGLE_CLOUD_ACCOUNT") or _run_cli_text(
        ["gcloud", "config", "get-value", "account"]
    )
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds_path:
        adc_path = Path.home() / ".config" / "gcloud" / "application_default_credentials.json"
        if adc_path.exists():
            creds_path = str(adc_path)

    if project:
        bundle["GOOGLE_CLOUD_PROJECT"] = project
    else:
        missing["GOOGLE_CLOUD_PROJECT"] = CLOUD_PROVIDER_SETUP_URLS["gcp"]
    if region:
        bundle["GOOGLE_CLOUD_REGION"] = region
    if account:
        bundle["GOOGLE_CLOUD_ACCOUNT"] = account
    if creds_path:
        bundle["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path
    elif not account:
        missing["GOOGLE_APPLICATION_CREDENTIALS"] = CLOUD_PROVIDER_SETUP_URLS["gcp"]

    return bundle, missing


def _build_aws_bundle() -> tuple[dict[str, str], dict[str, str]]:
    bundle: dict[str, str] = {"CLOUD_PROVIDER": "aws"}
    missing: dict[str, str] = {}

    profile = os.environ.get("AWS_PROFILE") or "default"
    region = (
        os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION")
        or _run_cli_text(["aws", "configure", "get", "region"])
        or _load_aws_config_value(profile, "region")
    )

    if region:
        bundle["AWS_REGION"] = region
        bundle["AWS_DEFAULT_REGION"] = region
    else:
        missing["AWS_REGION"] = CLOUD_PROVIDER_SETUP_URLS["aws"]

    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    session_token = os.environ.get("AWS_SESSION_TOKEN")

    if not (access_key and secret_key):
        aws_profile = _load_aws_profile(profile)
        access_key = access_key or aws_profile.get("aws_access_key_id", "")
        secret_key = secret_key or aws_profile.get("aws_secret_access_key", "")
        session_token = session_token or aws_profile.get("aws_session_token", "")
        if aws_profile:
            bundle["AWS_PROFILE"] = profile

    if access_key and secret_key:
        bundle["AWS_ACCESS_KEY_ID"] = access_key
        bundle["AWS_SECRET_ACCESS_KEY"] = secret_key
        if session_token:
            bundle["AWS_SESSION_TOKEN"] = session_token
    elif profile and _load_aws_profile(profile):
        bundle["AWS_PROFILE"] = profile
    else:
        missing["AWS_PROFILE"] = CLOUD_PROVIDER_SETUP_URLS["aws"]

    identity = _run_cli_json(["aws", "sts", "get-caller-identity", "--output", "json"])
    if isinstance(identity, dict):
        account_id = str(identity.get("Account") or "").strip()
        if account_id:
            bundle["AWS_ACCOUNT_ID"] = account_id

    return bundle, missing


def _build_azure_bundle() -> tuple[dict[str, str], dict[str, str]]:
    bundle: dict[str, str] = {"CLOUD_PROVIDER": "azure"}
    missing: dict[str, str] = {}

    for key in (
        "AZURE_CLIENT_ID",
        "AZURE_CLIENT_SECRET",
        "AZURE_TENANT_ID",
        "AZURE_SUBSCRIPTION_ID",
        "AZURE_LOCATION",
    ):
        value = os.environ.get(key)
        if value:
            bundle[key] = value

    account = _run_cli_json(["az", "account", "show", "-o", "json"])
    if isinstance(account, dict):
        subscription_id = str(account.get("id") or "").strip()
        tenant_id = str(account.get("tenantId") or "").strip()
        name = str(account.get("name") or "").strip()
        if subscription_id:
            bundle.setdefault("AZURE_SUBSCRIPTION_ID", subscription_id)
        if tenant_id:
            bundle.setdefault("AZURE_TENANT_ID", tenant_id)
        if name:
            bundle["AZURE_SUBSCRIPTION_NAME"] = name

    if "AZURE_SUBSCRIPTION_ID" not in bundle:
        missing["AZURE_SUBSCRIPTION_ID"] = CLOUD_PROVIDER_SETUP_URLS["azure"]

    return bundle, missing


def _build_token_provider_bundle(
    provider: str,
    env_names: tuple[str, ...],
) -> tuple[dict[str, str], dict[str, str]]:
    bundle: dict[str, str] = {"CLOUD_PROVIDER": provider}
    missing: dict[str, str] = {}

    for env_name in env_names:
        value = os.environ.get(env_name)
        if value:
            bundle[env_name] = value

    if not any(env_name in bundle for env_name in env_names):
        primary = env_names[0]
        missing[primary] = CLOUD_PROVIDER_SETUP_URLS.get(provider, "https://www.google.com")

    return bundle, missing


def _run_cli_text(command: list[str]) -> str:
    """Run a CLI command and return a stripped text result when available."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return ""

    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def _run_cli_json(command: list[str]) -> dict[str, object] | None:
    """Run a CLI command that returns JSON."""
    output = _run_cli_text(command)
    if not output:
        return None
    try:
        parsed = json.loads(output)
    except json.JSONDecodeError:
        return None
    if isinstance(parsed, dict):
        return parsed
    return None


def _load_aws_profile(profile: str) -> dict[str, str]:
    """Load a profile from ~/.aws/credentials if available."""
    credentials_path = Path.home() / ".aws" / "credentials"
    if not credentials_path.exists():
        return {}

    parser = configparser.RawConfigParser()
    try:
        parser.read(credentials_path, encoding="utf-8")
    except (configparser.Error, OSError):
        return {}

    if not parser.has_section(profile):
        return {}
    return {key: value for key, value in parser.items(profile)}


def _load_aws_config_value(profile: str, key: str) -> str:
    """Read one setting from ~/.aws/config."""
    config_path = Path.home() / ".aws" / "config"
    if not config_path.exists():
        return ""

    parser = configparser.RawConfigParser()
    try:
        parser.read(config_path, encoding="utf-8")
    except (configparser.Error, OSError):
        return ""

    section_names = [profile, f"profile {profile}"]
    for section in section_names:
        if parser.has_section(section) and parser.has_option(section, key):
            return parser.get(section, key).strip()
    return ""


def _generate_local_secret(name: str) -> str:
    """Generate a strong local-only secret value."""
    if "PASSWORD" in name or name.endswith("_PASS"):
        return secrets.token_urlsafe(24)
    if name.endswith("_USER") and _is_database_component_var(name):
        return "sage"
    if name.endswith("_DB") and _is_database_component_var(name):
        return "sage_app"
    return secrets.token_urlsafe(48)


def _write_env_file(path: Path, values: Mapping[str, str]) -> None:
    """Write the resolved credential values to `.env` with restrictive permissions."""
    lines = [
        "# Managed by SAGE secure credential bootstrap.",
        "# Do not commit this file.",
        "",
    ]
    for key in sorted(values):
        lines.append(f"{key}={_format_env_value(values[key])}")
    path.write_text("\n".join(lines) + "\n", "utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass


def _write_env_example(
    path: Path,
    required_vars: list[str],
    values: Mapping[str, str],
    missing_external: Mapping[str, str],
) -> None:
    """Write `.env.example` with keys only and no secret payloads."""
    names = sorted(set(required_vars) | set(values) | set(missing_external))
    lines = [
        "# Managed by SAGE secure credential bootstrap.",
        "# Fill in external credentials locally; keep this file value-free.",
        "",
    ]
    for name in names:
        lines.append(f"{name}=")
    if missing_external:
        lines.append("")
        lines.append("# External credentials to obtain manually:")
        for name, url in sorted(missing_external.items()):
            lines.append(f"# {name}: {url}")
    path.write_text("\n".join(lines) + "\n", "utf-8")


def _ensure_gitignore(project_root: Path) -> bool:
    """Ensure `.gitignore` protects local env files without hiding `.env.example`."""
    gitignore_path = project_root / ".gitignore"
    if gitignore_path.exists():
        content = gitignore_path.read_text("utf-8")
        lines = content.splitlines()
    else:
        lines = []

    changed = False
    for entry in (".env", ".env.local", "!.env.example"):
        if entry not in lines:
            lines.append(entry)
            changed = True

    if changed:
        gitignore_path.write_text("\n".join(lines).rstrip() + "\n", "utf-8")
    return changed


def _looks_like_env_var(value: str) -> bool:
    """Return True for probable environment-variable names."""
    if not value or len(value) < 3:
        return False
    if "_" not in value and not value.endswith(("URL", "KEY", "TOKEN", "PORT")):
        return False
    return value.isupper()


def _is_external_credential_var(name: str) -> bool:
    """Return True when a variable is likely provided by an external service."""
    if name in EXTERNAL_CREDENTIAL_URLS:
        return True
    return name.endswith("_API_KEY") or name in {"GITHUB_TOKEN", "STRIPE_SECRET_KEY"}


def _is_local_secret_var(name: str) -> bool:
    """Return True when SAGE can safely generate the value locally."""
    if _is_external_credential_var(name):
        return False
    local_markers = (
        "SECRET",
        "JWT",
        "SESSION",
        "ADMIN_TOKEN",
        "APP_KEY",
        "ENCRYPTION",
        "PASSWORD",
        "PASS",
        "AUTH_TOKEN",
        "ACCESS_TOKEN",
        "REFRESH_TOKEN",
    )
    return any(marker in name for marker in local_markers)


def _is_database_url_var(name: str) -> bool:
    return name.endswith("DATABASE_URL") or name in {"DATABASE_URL", "DB_URL", "SQLALCHEMY_DATABASE_URI"}


def _is_database_component_var(name: str) -> bool:
    return name.startswith(("POSTGRES_", "PG", "DB_"))


def _classify_credential_kind(name: str) -> str:
    if _is_database_url_var(name):
        return "database_url"
    if _is_database_component_var(name):
        return "database_component"
    if _is_external_credential_var(name):
        return "external_credential"
    return "local_secret"


def _format_env_value(value: str) -> str:
    """Quote values only when necessary for dotenv compatibility."""
    if not value:
        return ""
    if re.search(r"\s|#|['\"]", value):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return value


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "app"
