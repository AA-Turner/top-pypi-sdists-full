"""In-process, deduplicated cache of AWS Secrets Manager secrets.

A single ``get-secret-value`` call returns the whole secret (every key), so the
cache is keyed per secret id and callers pick the keys they need. Because the
network round-trip dominates, :func:`preload` warms many ids at once through a
thread pool, collapsing N sequential fetches into roughly one wall-clock fetch.

Secrets are held in memory only — never written to disk (unlike the opt-in
value cache in :mod:`pysae_ai_tools.env.cache`, which is for non-secret values).
"""

import json
import subprocess
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from ..common import winpath

_MAX_WORKERS = 8

_cache: dict[str, dict[str, str]] = {}
_lock = Lock()


class SecretError(RuntimeError):
    """Raised when a secret cannot be fetched or a key is absent."""


def user_secret_id(theme: str, env: str | None = None) -> str:
    """Return the caller's per-user secret id ``iam/<username>[/<env>]/<theme>``.

    The username comes from ``aws sts get-caller-identity`` (memoised). Raises
    :class:`SecretError` when it cannot be determined.
    """
    from .aws import current_aws_username

    username = current_aws_username()
    if not username:
        raise SecretError("could not determine the AWS username (`aws sts get-caller-identity`)")
    return f"iam/{username}/{env}/{theme}" if env else f"iam/{username}/{theme}"


def _aws_fetch(secret_id: str) -> dict[str, str]:
    """Fetch and parse a secret from AWS Secrets Manager (no caching)."""
    # `aws` may have just been installed (e.g. by `tools install`) into a dir
    # on the Windows registry PATH but not yet in this process's PATH.
    winpath.refresh_process_path_from_registry(force=True)
    try:
        result = subprocess.run(
            [
                "aws",
                "secretsmanager",
                "get-secret-value",
                "--secret-id",
                secret_id,
                "--query",
                "SecretString",
                "--output",
                "text",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
            timeout=15,
        )
    except FileNotFoundError as exc:
        raise SecretError("aws CLI not found — install it with `pysae-ai-tools tools install aws`") from exc
    except subprocess.TimeoutExpired as exc:
        raise SecretError(f"timed out reading {secret_id}") from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or "").strip().splitlines()
        last = detail[-1] if detail else f"exit code {exc.returncode}"
        raise SecretError(f"failed to read {secret_id}: {last}") from exc
    try:
        data = json.loads(result.stdout.strip())
    except json.JSONDecodeError as exc:
        raise SecretError(f"{secret_id}: invalid JSON ({exc})") from exc
    if not isinstance(data, dict):
        raise SecretError(f"{secret_id}: secret is not a JSON object")
    return {str(k): str(v) for k, v in data.items()}


def fetch_secret(secret_id: str) -> dict[str, str]:
    """Return the whole secret ``secret_id``, hitting the in-process cache first."""
    with _lock:
        cached = _cache.get(secret_id)
    if cached is not None:
        return cached
    data = _aws_fetch(secret_id)
    with _lock:
        _cache[secret_id] = data
    return data


def get_key(secret_id: str, key: str) -> str:
    """Return one key from ``secret_id``. Raises :class:`SecretError` if absent/empty."""
    data = fetch_secret(secret_id)
    value = data.get(key, "")
    if not value:
        raise SecretError(f"{secret_id}: key '{key}' not found or empty")
    return value


def preload(secret_ids: Iterable[str]) -> None:
    """Fetch every not-yet-cached id in parallel, best-effort.

    Failures are swallowed here: the individual resolver that needs a given
    secret will surface the error later (and try its fallbacks). This is purely
    a latency optimisation, so it must never abort the install.
    """
    with _lock:
        pending = sorted({sid for sid in secret_ids if sid and sid not in _cache})
    if not pending:
        return
    with ThreadPoolExecutor(max_workers=min(_MAX_WORKERS, len(pending))) as executor:
        fetched = list(executor.map(_safe_fetch, pending))
    with _lock:
        for secret_id, data in fetched:
            if data is not None:
                _cache[secret_id] = data


def _safe_fetch(secret_id: str) -> tuple[str, dict[str, str] | None]:
    try:
        return secret_id, _aws_fetch(secret_id)
    except SecretError:
        return secret_id, None


def reset() -> None:
    """Clear the in-process cache (test helper)."""
    with _lock:
        _cache.clear()
