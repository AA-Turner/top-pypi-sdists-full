"""GitHub Copilot authentication utilities.

Ported verbatim from upstream (CLI auth module).

Implements the OAuth device code flow used by the Copilot CLI and handles
token validation/exchange for the Copilot API.

Token type support (per GitHub docs):
  gho_          OAuth token           ✓  (default via copilot login)
  github_pat_   Fine-grained PAT      ✓  (needs Copilot Requests permission)
  ghu_          GitHub App token      ✓  (via environment variable)
  ghp_          Classic PAT           ✗  NOT SUPPORTED

Credential search order (matching Copilot CLI behaviour):
  1. COPILOT_GITHUB_TOKEN env var
  2. GH_TOKEN env var
  3. GITHUB_TOKEN env var
  4. gh auth token  CLI fallback
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
from cvc._subprocess_compat import HIDDEN_KW
import time
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

# OAuth device code flow constants (same client ID as opencode/Copilot CLI)
COPILOT_OAUTH_CLIENT_ID = "Ov23li8tweQw6odWQebz"
# Token type prefixes
_CLASSIC_PAT_PREFIX = "ghp_"
_SUPPORTED_PREFIXES = ("gho_", "github_pat_", "ghu_")

# Env var search order (matches Copilot CLI)
COPILOT_ENV_VARS = ("COPILOT_GITHUB_TOKEN", "GH_TOKEN", "GITHUB_TOKEN")

# Polling constants
_DEVICE_CODE_POLL_INTERVAL = 5  # seconds
_DEVICE_CODE_POLL_SAFETY_MARGIN = 3  # seconds


def validate_copilot_token(token: str) -> tuple[bool, str]:
    """Validate that a token is usable with the Copilot API.

    Returns (valid, message).
    """
    token = token.strip()
    if not token:
        return False, "Empty token"

    if token.startswith(_CLASSIC_PAT_PREFIX):
        return False, (
            "Classic Personal Access Tokens (ghp_*) are not supported by the "
            "Copilot API. Use one of:\n"
            "  → `cvc auth login copilot` to authenticate via OAuth\n"
            "  → A fine-grained PAT (github_pat_*) with Copilot Requests permission\n"
            "  → `gh auth login` with the default device code flow (produces gho_* tokens)"
        )

    return True, "OK"


def resolve_copilot_token() -> tuple[str, str]:
    """Resolve a GitHub token suitable for Copilot API use.

    Returns (token, source) where source describes where the token came from.
    Raises ValueError if only a classic PAT is available.
    """
    # 1. Check env vars in priority order
    for env_var in COPILOT_ENV_VARS:
        val = os.getenv(env_var, "").strip()
        if val:
            valid, msg = validate_copilot_token(val)
            if not valid:
                logger.warning(
                    "Token from %s is not supported: %s", env_var, msg
                )
                continue
            return val, env_var

    # 2. Fall back to gh auth token
    token = _try_gh_cli_token()
    if token:
        valid, msg = validate_copilot_token(token)
        if not valid:
            raise ValueError(
                f"Token from `gh auth token` is a classic PAT (ghp_*). {msg}"
            )
        return token, "gh auth token"

    return "", ""


def _gh_cli_candidates() -> list[str]:
    """Return candidate ``gh`` binary paths, including common Homebrew installs."""
    candidates: list[str] = []

    resolved = shutil.which("gh")
    if resolved:
        candidates.append(resolved)

    for candidate in (
        "/opt/homebrew/bin/gh",
        "/usr/local/bin/gh",
        str(Path.home() / ".local" / "bin" / "gh"),
    ):
        if candidate in candidates:
            continue
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            candidates.append(candidate)

    return candidates


def _try_gh_cli_token() -> Optional[str]:
    """Return a token from ``gh auth token`` when the GitHub CLI is available.

    When COPILOT_GH_HOST is set, passes ``--hostname`` so gh returns the
    correct host's token.  Also strips GITHUB_TOKEN / GH_TOKEN from the
    subprocess environment so ``gh`` reads from its own credential store
    (hosts.yml) instead of just echoing the env var back.
    """
    hostname = os.getenv("COPILOT_GH_HOST", "").strip()

    # Build a clean env so gh doesn't short-circuit on GITHUB_TOKEN / GH_TOKEN
    clean_env = {k: v for k, v in os.environ.items()
                 if k not in ("GITHUB_TOKEN", "GH_TOKEN")}

    for gh_path in _gh_cli_candidates():
        cmd = [gh_path, "auth", "token"]
        if hostname:
            cmd += ["--hostname", hostname]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5,
                env=clean_env,
                            **HIDDEN_KW,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
            logger.debug("gh CLI token lookup failed (%s): %s", gh_path, exc)
            continue
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    return None


# ─── OAuth Device Code Flow ────────────────────────────────────────────────

def copilot_device_code_login(
    *,
    host: str = "github.com",
    timeout_seconds: float = 300,
) -> Optional[str]:
    """Run the GitHub OAuth device code flow for Copilot.

    Prints instructions for the user, polls for completion, and returns
    the OAuth access token on success, or None on failure/cancellation.

    This replicates the flow used by opencode and the Copilot CLI.
    """
    import urllib.request
    import urllib.parse

    domain = host.rstrip("/")
    device_code_url = f"https://{domain}/login/device/code"
    access_token_url = f"https://{domain}/login/oauth/access_token"

    # Step 1: Request device code
    data = urllib.parse.urlencode({
        "client_id": COPILOT_OAUTH_CLIENT_ID,
        "scope": "read:user",
    }).encode()

    req = urllib.request.Request(
        device_code_url,
        data=data,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "CVC/1.0",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            device_data = json.loads(resp.read().decode())
    except Exception as exc:
        logger.error("Failed to initiate device authorization: %s", exc)
        print(f"  ✗ Failed to start device authorization: {exc}")
        return None

    verification_uri = device_data.get("verification_uri", "https://github.com/login/device")
    user_code = device_data.get("user_code", "")
    device_code = device_data.get("device_code", "")
    interval = max(device_data.get("interval", _DEVICE_CODE_POLL_INTERVAL), 1)

    if not device_code or not user_code:
        print("  ✗ GitHub did not return a device code.")
        return None

    # Step 2: Show instructions
    print()
    print(f"  Open this URL in your browser: {verification_uri}")
    print(f"  Enter this code: {user_code}")
    print()
    print("  Waiting for authorization...", end="", flush=True)

    # Step 3: Poll for completion
    deadline = time.monotonic() + timeout_seconds

    while time.monotonic() < deadline:
        time.sleep(interval + _DEVICE_CODE_POLL_SAFETY_MARGIN)

        poll_data = urllib.parse.urlencode({
            "client_id": COPILOT_OAUTH_CLIENT_ID,
            "device_code": device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        }).encode()

        poll_req = urllib.request.Request(
            access_token_url,
            data=poll_data,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "CVC/1.0",
            },
        )

        try:
            with urllib.request.urlopen(poll_req, timeout=10) as resp:
                result = json.loads(resp.read().decode())
        except Exception:
            print(".", end="", flush=True)
            continue

        if result.get("access_token"):
            print(" ✓")
            return result["access_token"]

        error = result.get("error", "")
        if error == "authorization_pending":
            print(".", end="", flush=True)
            continue
        elif error == "slow_down":
            # RFC 8628: add 5 seconds to polling interval
            server_interval = result.get("interval")
            if isinstance(server_interval, (int, float)) and server_interval > 0:
                interval = int(server_interval)
            else:
                interval += 5
            print(".", end="", flush=True)
            continue
        elif error == "expired_token":
            print()
            print("  ✗ Device code expired. Please try again.")
            return None
        elif error == "access_denied":
            print()
            print("  ✗ Authorization was denied.")
            return None
        elif error:
            print()
            print(f"  ✗ Authorization failed: {error}")
            return None

    print()
    print("  ✗ Timed out waiting for authorization.")
    return None


# ─── Copilot Token Exchange ────────────────────────────────────────────────

# Module-level cache for exchanged Copilot API tokens.
# Maps raw_token_fingerprint -> (api_token, expires_at_epoch).
_jwt_cache: dict[str, tuple[str, float]] = {}
_JWT_REFRESH_MARGIN_SECONDS = 120  # refresh 2 min before expiry

# Token exchange endpoint and headers (matching VS Code / Copilot CLI)
_TOKEN_EXCHANGE_URL = "https://api.github.com/copilot_internal/v2/token"
_EDITOR_VERSION = "vscode/1.104.1"
_EXCHANGE_USER_AGENT = "GitHubCopilotChat/0.26.7"


def _token_fingerprint(raw_token: str) -> str:
    """Short fingerprint of a raw token for cache keying (avoids storing full token)."""
    import hashlib
    return hashlib.sha256(raw_token.encode()).hexdigest()[:16]


_DEFAULT_COPILOT_API_URL = "https://api.individual.githubcopilot.com"


def exchange_copilot_token(
    raw_token: str, *, timeout: float = 10.0
) -> tuple[str, float, str]:
    """Exchange a raw GitHub token for a short-lived Copilot API token.

    Calls ``GET https://api.github.com/copilot_internal/v2/token`` with
    the raw GitHub token and returns ``(api_token, expires_at, api_url)``.

    The ``api_url`` is the account-specific Copilot API base. GitHub serves
    three different hostnames depending on the user's plan
    (``api.individual``, ``api.business``, ``api.enterprise``.githubcopilot.com),
    and hitting the wrong one returns a Cloudflare ``421 Misdirected Request``.
    Always honour the URL the exchange response declares.

    The returned token is a semicolon-separated string (not a standard JWT)
    used as ``Authorization: Bearer <token>`` for Copilot API requests.

    Results are cached in-process and reused until close to expiry.
    Raises ``ValueError`` on failure.
    """
    import urllib.request

    fp = _token_fingerprint(raw_token)

    # Check cache first
    cached = _jwt_cache.get(fp)
    if cached:
        # Tolerate older 2-tuple cache entries from before the api_url
        # field was added (e.g. left over after a hot reload).
        if len(cached) == 3:
            api_token, expires_at, api_url = cached
        else:
            api_token, expires_at = cached  # type: ignore[misc]
            api_url = _DEFAULT_COPILOT_API_URL
        if time.time() < expires_at - _JWT_REFRESH_MARGIN_SECONDS:
            return api_token, expires_at, api_url

    req = urllib.request.Request(
        _TOKEN_EXCHANGE_URL,
        method="GET",
        headers={
            "Authorization": f"token {raw_token}",
            "User-Agent": _EXCHANGE_USER_AGENT,
            "Accept": "application/json",
            "Editor-Version": _EDITOR_VERSION,
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode())
    except Exception as exc:
        raise ValueError(f"Copilot token exchange failed: {exc}") from exc

    api_token = data.get("token", "")
    expires_at = data.get("expires_at", 0)
    if not api_token:
        raise ValueError("Copilot token exchange returned empty token")

    # GitHub returns the account-specific Copilot API endpoint here.
    # Personal accounts → api.individual.githubcopilot.com
    # Business accounts → api.business.githubcopilot.com
    # Enterprise        → api.enterprise.githubcopilot.com
    # Using the wrong one gives Cloudflare 421 Misdirected Request.
    endpoints = data.get("endpoints") or {}
    api_url = (endpoints.get("api") or _DEFAULT_COPILOT_API_URL).rstrip("/")

    # Convert expires_at to float if needed
    expires_at = float(expires_at) if expires_at else time.time() + 1800

    _jwt_cache[fp] = (api_token, expires_at, api_url)
    logger.debug(
        "Copilot token exchanged, expires_at=%s api_url=%s",
        expires_at, api_url,
    )
    return api_token, expires_at, api_url


def get_copilot_api_token(raw_token: str) -> str:
    """Exchange a raw GitHub token for a Copilot API token, with fallback.

    Convenience wrapper: returns the exchanged token on success, or the
    raw token unchanged if the exchange fails (e.g. network error, unsupported
    account type). This preserves existing behaviour for accounts that don't
    need exchange while enabling access to internal-only models for those that do.
    """
    if not raw_token:
        return raw_token
    try:
        api_token, _, _ = exchange_copilot_token(raw_token)
        return api_token
    except Exception as exc:
        logger.debug("Copilot token exchange failed, using raw token: %s", exc)
        return raw_token


# ─── Dynamic Copilot Model Discovery ───────────────────────────────────────
#
# GitHub Copilot serves a ``GET /models`` endpoint on the account-scoped
# API base that returns the exact list of models the user's plan/org has
# enabled. This is the ONLY source of truth for what's actually available
# — the static ``fallback_models`` in cvc/providers/base.py is just a
# hint and can be wrong (e.g. after a new model launches and the org
# enables it, or when a plan upgrades).
#
# We cache the result in-process for ``_COPILOT_MODELS_CACHE_TTL`` seconds
# so we don't slam the API on every chat turn.
#
# Response shape (per Copilot OpenAI-compat surface):
#   {
#     "object": "list",
#     "data": [
#       {"id": "gpt-4o", "object": "model", "created": 1727000000,
#        "owned_by": "openai", "version": "...", "name": "...",
#        "capabilities": {...}, "billing": {...}, ...
#       },
#       ...
#     ]
#   }

_COPILOT_MODELS_CACHE: dict[str, tuple[float, dict[str, Any]]] = {}
_COPILOT_MODELS_CACHE_TTL = 600.0  # 10 min — fresh enough for org-policy changes


def _parse_copilot_models_response(data: Any) -> list[dict[str, Any]]:
    """Normalise the /models payload into a uniform shape for the dashboard.

    Returns a list of dicts: {id, name, owned_by, capabilities, raw}.
    """
    out: list[dict[str, Any]] = []
    if not isinstance(data, dict):
        return out
    items = data.get("data")
    if not isinstance(items, list):
        return out
    for m in items:
        if not isinstance(m, dict):
            continue
        mid = m.get("id") or m.get("name") or ""
        if not isinstance(mid, str) or not mid.strip():
            continue
        out.append({
            "id": mid.strip(),
            "name": (m.get("name") or mid.strip()),
            "owned_by": m.get("owned_by") or m.get("vendor") or "",
            "capabilities": m.get("capabilities") or {},
            "billing": m.get("billing") or {},
            "version": m.get("version") or "",
            "raw": m,
        })
    return out


def list_copilot_models(
    raw_token: str, *, force_refresh: bool = False, timeout: float = 8.0
) -> list[dict[str, Any]]:
    """Return the list of models available on the user's GitHub Copilot plan.

    Uses the exchanged Copilot API token + the account-specific base URL
    returned by ``/copilot_internal/v2/token``. Results are cached for
    10 minutes; pass ``force_refresh=True`` to bypass.

    Returns an empty list on any failure (no token, exchange failed,
    network error, malformed payload). Callers should fall back to the
    static ``fallback_models`` in that case.
    """
    if not raw_token:
        return []

    fp = _token_fingerprint(raw_token)
    now = time.time()
    if not force_refresh:
        cached = _COPILOT_MODELS_CACHE.get(fp)
        if cached and (now - cached[0]) < _COPILOT_MODELS_CACHE_TTL:
            return list(cached[1].get("models") or [])

    # Exchange token (this also gives us the account-specific api_url)
    try:
        api_token, expires_at, api_url = exchange_copilot_token(raw_token, timeout=timeout)
    except Exception as exc:
        logger.debug("list_copilot_models: token exchange failed: %s", exc)
        return []

    # Hit the /models endpoint on the account-specific base URL.
    import urllib.request
    url = f"{api_url}/models"
    req = urllib.request.Request(
        url,
        method="GET",
        headers={
            "Authorization": f"Bearer {api_token}",
            "User-Agent": _EXCHANGE_USER_AGENT,
            "Accept": "application/json",
            "Editor-Version": _EDITOR_VERSION,
            # Copilot requires this header for the /models endpoint on some plans
            "Copilot-Integration-Id": "vscode-chat",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw_data = json.loads(resp.read().decode())
    except Exception as exc:
        logger.debug("list_copilot_models: GET %s failed: %s", url, exc)
        return []

    models = _parse_copilot_models_response(raw_data)
    _COPILOT_MODELS_CACHE[fp] = (now, {"models": models, "expires_at": expires_at})
    logger.info("list_copilot_models: discovered %d models for account", len(models))
    return models


def clear_copilot_models_cache(raw_token: Optional[str] = None) -> None:
    """Clear the model list cache. If ``raw_token`` is given, only that
    account's cache is cleared; otherwise the entire cache is flushed.
    """
    if raw_token is None:
        _COPILOT_MODELS_CACHE.clear()
        return
    fp = _token_fingerprint(raw_token)
    _COPILOT_MODELS_CACHE.pop(fp, None)


# ─── Model fallback matching ────────────────────────────────────────────────
#
# When the user picks a model that their Copilot plan doesn't enable
# (e.g. requests Sonnet 5 but org hasn't rolled it out yet), the API
# returns 400 with a list of actually-available models. We parse that
# list and pick the closest match so the request succeeds instead of
# failing.

def pick_closest_copilot_model(
    requested: str, available: list[str]
) -> Optional[str]:
    """Pick the closest model from `available` to the one `requested`.

    Matching priority:
      1. Exact match
      2. Same family + same vendor (e.g. "claude-sonnet-4.6" → "claude-sonnet-4.5")
      3. Same family, latest available version
      4. Same vendor, any model
      5. None

    `available` may be model ids or full dicts from list_copilot_models().
    """
    if not available:
        return None
    # Normalise to bare id strings
    ids: list[str] = []
    for a in available:
        if isinstance(a, str):
            ids.append(a)
        elif isinstance(a, dict):
            mid = a.get("id")
            if isinstance(mid, str):
                ids.append(mid)
    if not ids:
        return None

    requested_lc = requested.lower().strip()

    # 1. Exact match
    for mid in ids:
        if mid.lower() == requested_lc:
            return mid

    # 2/3. Family match — split requested into tokens
    #    e.g. "claude-sonnet-4.6" → family="claude-sonnet", rest="4.6"
    req_tokens = requested_lc.replace("_", "-").split("-")
    # Score each candidate by token overlap
    scored: list[tuple[int, str]] = []
    for mid in ids:
        cand_lc = mid.lower()
        cand_tokens = cand_lc.replace("_", "-").split("-")
        # Count shared tokens in the same position
        overlap = sum(1 for r, c in zip(req_tokens, cand_tokens) if r == c)
        # Prefer longer family prefix matches (claude-sonnet-4.x beats claude-3.x)
        if overlap > 0:
            scored.append((overlap, mid))
    if scored:
        scored.sort(key=lambda x: (-x[0], x[1]))
        return scored[0][1]

    # 4. Vendor match (first token = vendor like "claude", "gpt", "gemini")
    if req_tokens:
        vendor = req_tokens[0]
        for mid in ids:
            if mid.lower().startswith(vendor + "-") or mid.lower().startswith(vendor):
                return mid

    return None


# ─── Copilot API Headers ───────────────────────────────────────────────────

def copilot_request_headers(
    *,
    is_agent_turn: bool = True,
    is_vision: bool = False,
) -> dict[str, str]:
    """Build the standard headers for Copilot API requests.

    Replicates the header set used by opencode and the Copilot CLI.
    These spoof VSCode Chat so the request is billed against the IDE
    quota (effectively unlimited for Copilot Pro) instead of the
    Premium Chat quota.
    """
    headers: dict[str, str] = {
        "Editor-Version": "vscode/1.104.1",
        "Editor-Plugin-Version": "copilot-chat/0.26.7",
        "User-Agent": "GitHubCopilotChat/0.26.7",
        "Copilot-Integration-Id": "vscode-chat",
        "Openai-Intent": "conversation-edits",
        "Openai-Organization": "github-copilot",
        "x-initiator": "agent" if is_agent_turn else "user",
    }
    if is_vision:
        headers["Copilot-Vision-Request"] = "true"

    return headers
