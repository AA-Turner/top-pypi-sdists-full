"""Token-signing and GitHub-bootstrap helpers for the SDK-owned Koyeb provider.

The helpers used by ``koyeb_sandbox`` must preserve the verifier's wire contract.
Contract changes require fixed token and command-output tests.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import shlex
import time
import urllib.parse
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Protocol

from .proxy_lifecycle import SandboxProxyIdentity

SANDBOX_PROXY_TOKEN_HEADER = "X-Sandbox-Proxy-Token"
SANDBOX_PROXY_CA_CERT_ENV = "SANDBOX_PROXY_CA_CERT"
SANDBOX_PROXY_URL_ENV = "SANDBOX_PROXY_URL"
SANDBOX_PROXY_TOKEN_ENV = "SANDBOX_PROXY_TOKEN"
SANDBOX_PROXY_GITHUB_PROXY_ENV = "SANDBOX_PROXY_GITHUB_PROXY"
GH_TOKEN_ENV = "GH_TOKEN"
GITHUB_TOKEN_ENV = "GITHUB_TOKEN"
GH_HOST_ENV = "GH_HOST"
GH_ENTERPRISE_TOKEN_ENV = "GH_ENTERPRISE_TOKEN"
GITHUB_ENTERPRISE_TOKEN_ENV = "GITHUB_ENTERPRISE_TOKEN"
REQUESTS_CA_BUNDLE_ENV = "REQUESTS_CA_BUNDLE"
SSL_CERT_FILE_ENV = "SSL_CERT_FILE"

_DEFAULT_SANDBOX_PROXY_TOKEN_TTL_SECONDS = 7 * 24 * 60 * 60
_DEFAULT_GITHUB_HOST = "github.com"
_GITHUB_PROVIDER = "github"
_EGRESS_PROVIDER = "egress"
_GITHUB_REPO_SCOPE_SELECTED_REPOS = "selected_repos"
_GITHUB_REPO_SCOPE_ALL_ACCESSIBLE_REPOS = "all_accessible_repos"
_PROVIDER_LABEL = "GitHub sandbox proxy bootstrap"
_DEFAULT_SAFE_DIRECTORY = "/workspace"
_SETUP_LOG_PREFIX = "sandbox-proxy github setup"
_RUNTIME_CONFIG_DIR = "/tmp/sandbox-proxy"
_CA_CERT_FILENAME = "sandbox-proxy-ca.crt"
_CA_BUNDLE_PATH = f"{_RUNTIME_CONFIG_DIR}/sandbox-proxy-ca-bundle.crt"
_GH_PROXY_CONFIG_PATH = f"{_RUNTIME_CONFIG_DIR}/github-gh-proxy"


class _IdentityLike(Protocol):
    customer_id: str | None
    organization_id: str | None
    workspace_id: str | None
    user_id: str | None


@dataclass(frozen=True, slots=True)
class GitHubProxyTokenRenewal:
    env: Mapping[str, str]
    expires_at: int


class SandboxProxyTokenSigner:
    def __init__(self, *, secret: str, ttl_seconds: int = _DEFAULT_SANDBOX_PROXY_TOKEN_TTL_SECONDS) -> None:
        normalized_secret = secret.strip()
        if not normalized_secret:
            raise ValueError("Sandbox proxy token signing secret must not be empty")
        if ttl_seconds <= 0:
            raise ValueError("Sandbox proxy token TTL must be positive")

        self._secret = normalized_secret.encode("utf-8")
        self._ttl_seconds = ttl_seconds

    def issue_github_token(
        self,
        *,
        identity: SandboxProxyIdentity | _IdentityLike,
        repos: Iterable[str] | None = None,
        all_accessible_repos: bool = False,
        now: int | None = None,
    ) -> str:
        repo_scope = (
            _GITHUB_REPO_SCOPE_ALL_ACCESSIBLE_REPOS if all_accessible_repos else _GITHUB_REPO_SCOPE_SELECTED_REPOS
        )
        normalized_repos = (
            frozenset() if all_accessible_repos else normalize_github_repos(() if repos is None else repos)
        )
        return self._issue(
            identity=identity,
            provider_scope={
                "provider": _GITHUB_PROVIDER,
                "repo_scope": repo_scope,
                "repos": sorted(normalized_repos),
            },
            now=now,
        )

    def issue_egress_token(
        self,
        *,
        identity: SandboxProxyIdentity | _IdentityLike,
        now: int | None = None,
    ) -> str:
        return self._issue(
            identity=identity,
            provider_scope={"provider": _EGRESS_PROVIDER},
            now=now,
        )

    def _issue(
        self,
        *,
        identity: SandboxProxyIdentity | _IdentityLike,
        provider_scope: dict[str, object],
        now: int | None,
    ) -> str:
        issued_at = int(time.time()) if now is None else now
        subject = _extract_subject(identity)
        payload = {
            "sub": {
                "customer_id": subject.customer_id,
                "organization_id": subject.organization_id,
                "user_id": subject.user_id,
                "workspace_id": subject.workspace_id,
            },
            "provider_scope": provider_scope,
            "exp": issued_at + self._ttl_seconds,
        }
        payload_json = json.dumps(payload, separators=(",", ":"), sort_keys=True)
        encoded_payload = base64.urlsafe_b64encode(payload_json.encode("utf-8")).decode("ascii").rstrip("=")
        signature = hmac.new(
            self._secret,
            encoded_payload.encode("ascii"),
            hashlib.sha256,
        ).digest()
        encoded_signature = base64.urlsafe_b64encode(signature).decode("ascii").rstrip("=")
        return f"{encoded_payload}.{encoded_signature}"


def normalize_github_repos(repos: Iterable[str]) -> frozenset[str]:
    if isinstance(repos, (str, Mapping)):
        raise ValueError("GitHub repo whitelist must be a sequence of owner/repo values")
    return frozenset(_normalize_github_repo(repo) for repo in repos)


def build_github_proxy_sandbox_setup(
    *,
    identity: SandboxProxyIdentity,
    proxy_url: str,
    ca_cert: str,
    signing_secret: str,
    repo_whitelist: Iterable[str] | None = None,
    all_accessible_repos: bool = False,
    ttl_seconds: int | None = None,
    now: int | None = None,
    safe_directories: list[str] | None = None,
    github_host: str = _DEFAULT_GITHUB_HOST,
) -> tuple[dict[str, str], str]:
    if identity is None:
        raise ValueError("GitHub sandbox proxy bootstrap requires identity")

    proxy_url = _require_text(_PROVIDER_LABEL, "proxy_url", proxy_url)
    _require_non_empty(_PROVIDER_LABEL, "ca_cert", ca_cert)
    repos = _resolve_repo_whitelist(repo_whitelist)
    safe_directories = safe_directories or [_DEFAULT_SAFE_DIRECTORY]
    safe_directories = [_require_text(_PROVIDER_LABEL, "safe_directories", directory) for directory in safe_directories]
    host = _GitHubHost.from_host(github_host)
    renewal = build_github_proxy_token_renewal(
        identity=identity,
        proxy_url=proxy_url,
        signing_secret=signing_secret,
        repo_whitelist=repos,
        all_accessible_repos=all_accessible_repos,
        ttl_seconds=ttl_seconds,
        now=now,
        github_host=github_host,
    )
    env = {
        SANDBOX_PROXY_URL_ENV: proxy_url,
        SANDBOX_PROXY_CA_CERT_ENV: ca_cert,
        **renewal.env,
        REQUESTS_CA_BUNDLE_ENV: _CA_BUNDLE_PATH,
        SSL_CERT_FILE_ENV: _CA_BUNDLE_PATH,
    }
    return dict(env), _build_setup_command(safe_directories, host)


def build_github_proxy_token_renewal(
    *,
    identity: SandboxProxyIdentity,
    proxy_url: str,
    signing_secret: str,
    repo_whitelist: Iterable[str] | None = None,
    all_accessible_repos: bool = False,
    ttl_seconds: int | None = None,
    now: int | None = None,
    github_host: str = _DEFAULT_GITHUB_HOST,
) -> GitHubProxyTokenRenewal:
    if identity is None:
        raise ValueError("GitHub sandbox proxy token renewal requires identity")

    issued_at = int(time.time()) if now is None else now
    proxy_url = _require_text(_PROVIDER_LABEL, "proxy_url", proxy_url)
    repos = _resolve_repo_whitelist(repo_whitelist)
    resolved_ttl_seconds = ttl_seconds if ttl_seconds is not None else _DEFAULT_SANDBOX_PROXY_TOKEN_TTL_SECONDS
    host = _GitHubHost.from_host(github_host)
    signer = SandboxProxyTokenSigner(secret=signing_secret, ttl_seconds=resolved_ttl_seconds)
    github_token = signer.issue_github_token(
        identity=identity,
        repos=repos,
        all_accessible_repos=all_accessible_repos,
        now=issued_at,
    )
    egress_token = signer.issue_egress_token(identity=identity, now=issued_at)
    env = {
        SANDBOX_PROXY_TOKEN_ENV: github_token,
        GH_TOKEN_ENV: github_token,
        GITHUB_TOKEN_ENV: github_token,
        SANDBOX_PROXY_GITHUB_PROXY_ENV: _build_authenticated_proxy_url(proxy_url, egress_token),
    }
    if host.git_host != _DEFAULT_GITHUB_HOST:
        env[GH_HOST_ENV] = host.git_host
    if host.is_enterprise:
        env[GH_ENTERPRISE_TOKEN_ENV] = github_token
        env[GITHUB_ENTERPRISE_TOKEN_ENV] = github_token
    return GitHubProxyTokenRenewal(env=MappingProxyType(env), expires_at=issued_at + resolved_ttl_seconds)


def build_github_proxy_token_renewal_command(github_host: str = _DEFAULT_GITHUB_HOST) -> str:
    host = _GitHubHost.from_host(github_host)
    return f"""{_build_proxy_config_command(host)}
{_build_extra_header_command(host)}
{_build_gh_config_command()}"""


def _extract_subject(identity: SandboxProxyIdentity | _IdentityLike) -> SandboxProxyIdentity:
    return SandboxProxyIdentity(
        customer_id=_require_text("Sandbox proxy token", "sub.customer_id", identity.customer_id),
        user_id=_require_text("Sandbox proxy token", "sub.user_id", identity.user_id),
        workspace_id=_require_text("Sandbox proxy token", "sub.workspace_id", identity.workspace_id),
        organization_id=_require_text(
            "Sandbox proxy token",
            "sub.organization_id",
            identity.organization_id,
        ),
    )


def _normalize_github_repo(repo: str) -> str:
    normalized = urllib.parse.unquote(urllib.parse.urlsplit(repo.strip()).path).strip("/")
    if normalized.endswith(".git"):
        normalized = normalized[:-4]
    if normalized.count("/") != 1:
        raise ValueError("GitHub repo scope must be in the form owner/repo")
    return normalized.lower()


def _resolve_repo_whitelist(repo_whitelist: Iterable[str] | None) -> frozenset[str]:
    if repo_whitelist is None:
        return frozenset()
    return normalize_github_repos(repo_whitelist)


def _build_authenticated_proxy_url(proxy_url: str, token: str) -> str:
    parsed = urllib.parse.urlsplit(proxy_url)
    if not parsed.scheme or not parsed.hostname:
        return proxy_url
    host = parsed.hostname
    if ":" in host and not host.startswith("["):
        host = f"[{host}]"
    port = f":{parsed.port}" if parsed.port is not None else ""
    return urllib.parse.urlunsplit(
        (
            parsed.scheme,
            f"sandbox-proxy:{urllib.parse.quote(token, safe='')}@{host}{port}",
            parsed.path,
            parsed.query,
            parsed.fragment,
        )
    )


def _build_setup_command(safe_directories: list[str], host: _GitHubHost) -> str:
    safe_directories_commands = "\n".join(
        f"git config --global --add safe.directory {shlex.quote(directory)}" for directory in safe_directories
    )
    return f"""{_build_ca_setup_block(_build_setup_log_command("write-ca-bundle"))}
{_build_setup_log_command("add-safe-directories")}
{safe_directories_commands}
{_build_setup_log_command("configure-proxy")}
{build_github_proxy_token_renewal_command(host.host)}
{_build_setup_log_command("configure-gh-wrapper")}
{_build_gh_wrapper_command(host)}
{_build_setup_log_command("configure-ca")}
git config --global http.sslCAInfo {shlex.quote(_CA_BUNDLE_PATH)}
{_build_setup_log_command("complete")}
"""


def _build_ca_setup_block(step_log_command: str) -> str:
    return f"""set -eu
{step_log_command}
_config_dir="{_RUNTIME_CONFIG_DIR}"
_proxy_ca_path="$_config_dir/{_CA_CERT_FILENAME}"
_proxy_ca_bundle_path="$_config_dir/sandbox-proxy-ca-bundle.crt"
mkdir -p "$_config_dir"
SANDBOX_PROXY_CA_PATH="$_proxy_ca_path" \\
SANDBOX_PROXY_CA_BUNDLE_PATH="$_proxy_ca_bundle_path" \\
python3 - <<'__SANDBOX_PROXY_CA__'
from __future__ import annotations

import os
import pathlib

cert_path = pathlib.Path(os.environ["SANDBOX_PROXY_CA_PATH"])
bundle_path = pathlib.Path(os.environ["SANDBOX_PROXY_CA_BUNDLE_PATH"])
ca_cert = os.environ["{SANDBOX_PROXY_CA_CERT_ENV}"]
system_bundle = ""
for candidate in (
    "/etc/ssl/certs/ca-certificates.crt",
    "/etc/pki/tls/certs/ca-bundle.crt",
    "/etc/ssl/cert.pem",
):
    candidate_path = pathlib.Path(candidate)
    if candidate_path.is_file():
        system_bundle = candidate_path.read_text(encoding="utf-8")
        break

cert_path.write_text(ca_cert, encoding="utf-8")
bundle_path.write_text(f"{{system_bundle.rstrip()}}\\n{{ca_cert}}", encoding="utf-8")
cert_path.chmod(0o644)
bundle_path.chmod(0o644)
__SANDBOX_PROXY_CA__"""


def _build_proxy_config_command(host: _GitHubHost) -> str:
    return (
        f"git config --global {host.url_config_prefix}.proxy "
        f'"${{{SANDBOX_PROXY_GITHUB_PROXY_ENV}}}"\n'
        f"git config --global {host.url_config_prefix}.proxyAuthMethod basic"
    )


def _build_extra_header_command(host: _GitHubHost) -> str:
    return (
        f'_proxy_header_value="{SANDBOX_PROXY_TOKEN_HEADER}: ${{{SANDBOX_PROXY_TOKEN_ENV}}}" && '
        f'git config --global {host.url_config_prefix}.extraHeader "$_proxy_header_value"'
    )


def _build_gh_config_command() -> str:
    return f"""_gh_proxy_config_path={shlex.quote(_GH_PROXY_CONFIG_PATH)}
_gh_proxy_config_tmp="${{_gh_proxy_config_path}}.$$"
mkdir -p "$(dirname "$_gh_proxy_config_path")"
( umask 077 && {{
  printf '%s\\n' "${{{SANDBOX_PROXY_GITHUB_PROXY_ENV}}}"
  printf '%s\\n' "${{{SANDBOX_PROXY_TOKEN_ENV}}}"
}} > "$_gh_proxy_config_tmp" && mv -f "$_gh_proxy_config_tmp" "$_gh_proxy_config_path" )"""


def _build_setup_log_command(step: str) -> str:
    return f"printf '%s\\n' {shlex.quote(f'{_SETUP_LOG_PREFIX}: {step}')} >&2"


def _build_gh_wrapper_command(host: _GitHubHost) -> str:
    host_exports: list[str] = []
    if host.git_host != _DEFAULT_GITHUB_HOST:
        host_exports.append(f"export {GH_HOST_ENV}={shlex.quote(host.git_host)}")
    if host.is_enterprise:
        host_exports.extend(
            [
                f'export {GH_ENTERPRISE_TOKEN_ENV}="$_token"',
                f'export {GITHUB_ENTERPRISE_TOKEN_ENV}="$_token"',
            ]
        )
    return f"""_gh_wrapper_dir="${{HOME:?}}/.local/bin"
_gh_wrapper_path="$_gh_wrapper_dir/gh"
_gh_profile="${{HOME:?}}/.profile"
mkdir -p "$_gh_wrapper_dir"
cat > "$_gh_wrapper_path" <<'__SANDBOX_PROXY_GH_WRAPPER__'
#!/bin/sh
# SANDBOX_PROXY_GH_WRAPPER=1
set -eu

_gh_proxy_config_path={shlex.quote(_GH_PROXY_CONFIG_PATH)}
_proxy=""
_token=""
if [ -r "$_gh_proxy_config_path" ]; then
  {{
    IFS= read -r _proxy || true
    IFS= read -r _token || true
  }} < "$_gh_proxy_config_path"
fi

if [ -z "$_proxy" ]; then
  _proxy="${{{SANDBOX_PROXY_GITHUB_PROXY_ENV}:-}}"
fi
if [ -z "$_proxy" ]; then
  echo "SANDBOX_PROXY_GITHUB_PROXY or gh runtime config is required for proxied gh" >&2
  exit 1
fi

if [ -z "$_token" ]; then
  _token="${{{SANDBOX_PROXY_TOKEN_ENV}:-}}"
fi
if [ -z "$_token" ]; then
  _token="${{{GH_TOKEN_ENV}:-}}"
fi
if [ -z "$_token" ]; then
  _token="${{{GITHUB_TOKEN_ENV}:-}}"
fi
if [ -z "$_token" ]; then
  echo "SANDBOX_PROXY_TOKEN/GH_TOKEN or gh runtime config is required for proxied gh" >&2
  exit 1
fi

export HTTP_PROXY="$_proxy"
export HTTPS_PROXY="$_proxy"
export http_proxy="$_proxy"
export https_proxy="$_proxy"
export GH_TOKEN="$_token"
export GITHUB_TOKEN="$_token"
{chr(10).join(host_exports)}

# Trust the proxy's CA; see _build_gh_wrapper_command.
_ca_bundle={shlex.quote(_CA_BUNDLE_PATH)}
if [ -r "$_ca_bundle" ]; then
  export SSL_CERT_FILE="$_ca_bundle"
fi

_real_gh="${{SANDBOX_PROXY_REAL_GH:-}}"
if [ -z "$_real_gh" ]; then
  _real_gh="/usr/bin/gh"
fi
if [ ! -x "$_real_gh" ]; then
  _wrapper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
  _old_ifs=$IFS
  IFS=:
  for _dir in ${{PATH:-}}; do
    if [ -z "$_dir" ]; then
      _dir=.
    fi
    if [ "$_dir" = "$_wrapper_dir" ]; then
      continue
    fi
    _candidate="$_dir/gh"
    if [ -x "$_candidate" ]; then
      _real_gh="$_candidate"
      break
    fi
  done
  IFS=$_old_ifs
fi

if [ ! -x "$_real_gh" ]; then
  echo "real gh CLI is missing from the sandbox image" >&2
  exit 127
fi

exec "$_real_gh" "$@"
__SANDBOX_PROXY_GH_WRAPPER__
chmod 0755 "$_gh_wrapper_path"
touch "$_gh_profile"
if ! grep -Fq 'SANDBOX_PROXY_GH_PATH=1' "$_gh_profile"; then
  {{
    printf '\\n%s\\n' '# SANDBOX_PROXY_GH_PATH=1'
    printf '%s\\n' 'export PATH="$HOME/.local/bin${{PATH:+:$PATH}}"'
  }} >> "$_gh_profile"
fi
export PATH="$_gh_wrapper_dir${{PATH:+:$PATH}}"
_gh_on_path=$(command -v gh || true)
if [ "$_gh_on_path" != "$_gh_wrapper_path" ]; then
  echo "gh wrapper is not first on PATH; resolved ${{_gh_on_path:-missing}}" >&2
  exit 1
fi
"""


@dataclass(frozen=True, slots=True)
class _GitHubHost:
    host: str

    @classmethod
    def from_host(cls, value: str | None) -> _GitHubHost:
        if not value:
            return cls(_DEFAULT_GITHUB_HOST)
        if "/" in value or value != value.strip().lower():
            raise ValueError(
                "GITHUB_INTEGRATION_HOST must be a bare lowercase hostname "
                f"like 'github.com' or 'ghe.example.com', got {value!r}"
            )
        return cls(value)

    @property
    def git_host(self) -> str:
        return self.host

    @property
    def is_enterprise(self) -> bool:
        return self.host != _DEFAULT_GITHUB_HOST and not self.host.endswith(".ghe.com")

    @property
    def url_config_prefix(self) -> str:
        return f"http.https://{self.host}/"


def _require_text(provider_label: str, name: str, value: object) -> str:
    _require_non_empty(provider_label, name, value)
    return str(value).strip()


def _require_non_empty(provider_label: str, name: str, value: object) -> None:
    if value is None or not str(value).strip():
        raise ValueError(f"{provider_label} requires {name}")
