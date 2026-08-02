"""Single shared ``glab`` runner — the one place the package shells out to ``glab``.

Neutral in dependencies (never imports ``internal/`` or any command group) so
every layer can consume it. It never calls ``sys.exit`` nor raises on a ``glab``
failure: :func:`run_glab` always returns a :class:`GlabResult` and the JSON
helpers return ``None`` on failure, leaving the reaction to the caller. Every
invocation carries a timeout and handles a missing binary, so no call can hang.
"""

import json
import os
import subprocess
from dataclasses import dataclass
from typing import Any

GLAB_MISSING_RC = 127
GLAB_TIMEOUT_RC = 124

DEFAULT_HOST = "gitlab.com"


@dataclass
class GlabResult:
    """Outcome of a ``glab`` invocation. ``returncode`` is ``127`` when the binary
    is absent and ``124`` on timeout, so a caller can react without a hang or an
    exception ever escaping the runner."""

    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def run_glab(*args: str, timeout: int = 30, stdin_data: str | None = None) -> GlabResult:
    """Run ``glab <args>`` and return a :class:`GlabResult`.

    Encoding is forced to utf-8 with ``errors="replace"`` so a CLI emitting
    cp1252/cp850 bytes (Windows FR locale) never crashes the reader thread.
    ``stdin`` is closed (``DEVNULL``) unless ``stdin_data`` is provided, so an
    interactive prompt can never block the call.
    """
    try:
        result = subprocess.run(
            ["glab", *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            input=stdin_data,
            stdin=None if stdin_data is not None else subprocess.DEVNULL,
        )
    except FileNotFoundError:
        return GlabResult(GLAB_MISSING_RC, "", "glab is not installed or not in PATH")
    except subprocess.TimeoutExpired:
        return GlabResult(GLAB_TIMEOUT_RC, "", f"glab timed out after {timeout}s")
    return GlabResult(result.returncode, (result.stdout or "").strip(), (result.stderr or "").strip())


def run_glab_bytes(*args: str, timeout: int = 120) -> bytes | None:
    """Run ``glab <args>`` and return raw stdout bytes (for binary downloads), or
    ``None`` on any failure (missing binary, timeout, non-zero exit)."""
    try:
        result = subprocess.run(
            ["glab", *args],
            capture_output=True,
            timeout=timeout,
            stdin=subprocess.DEVNULL,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return result.stdout


def glab_api(
    path: str,
    *extra: str,
    method: str = "",
    fields: list[str] | None = None,
    stdin_data: str | None = None,
    timeout: int = 30,
) -> Any | None:
    """Call ``glab api <path>`` and parse the JSON response, or ``None`` on failure.

    ``method`` maps to ``-X`` (e.g. ``POST``/``PUT``); ``fields`` are ``-f key=value``
    body parameters; ``extra`` are passed verbatim (headers, flags). Returns ``None``
    silently on a failed call, empty body, or invalid JSON — callers that care about
    the reason should use :func:`run_glab` directly.
    """
    args = ["api"]
    if method:
        args += ["-X", method]
    args.append(path)
    args += list(extra)
    for kv in fields or []:
        args += ["-f", kv]
    res = run_glab(*args, timeout=timeout, stdin_data=stdin_data)
    if not res.ok or not res.stdout:
        return None
    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError:
        return None


def glab_api_paginated(endpoint: str, per_page: int = 100, timeout: int = 30) -> list[dict[str, Any]]:
    """Fetch every page of a GitLab API list endpoint (stops on a short/empty page)."""
    results: list[dict[str, Any]] = []
    page = 1
    while True:
        sep = "&" if "?" in endpoint else "?"
        data = glab_api(f"{endpoint}{sep}per_page={per_page}&page={page}", timeout=timeout)
        if not isinstance(data, list) or not data:
            break
        results.extend(data)
        if len(data) < per_page:
            break
        page += 1
    return results


def resolve_current_project() -> tuple[str, str]:
    """Return ``(project_id, project_path)`` for the repo in the CWD.

    Both are empty strings when ``glab repo view`` fails (no repo, glab absent,
    invalid JSON) — the single replacement for the ``glab repo view --output json``
    dance duplicated across the package.
    """
    res = run_glab("repo", "view", "--output", "json")
    if not res.ok or not res.stdout:
        return "", ""
    try:
        data = json.loads(res.stdout)
    except json.JSONDecodeError:
        return "", ""
    return str(data.get("id", "") or ""), str(data.get("path_with_namespace", "") or "")


def gitlab_token(host: str = DEFAULT_HOST) -> str:
    """Resolve a GitLab token: ``GLAB_TOKEN``/``GITLAB_TOKEN`` env, then the ``glab``
    CLI config (``glab config get token``), then ``glab auth status -t``.

    Returns an empty string when nothing resolves. This is the single token
    resolver — no code parses ``~/.config/glab-cli/config.yml`` by hand.
    """
    for var in ("GLAB_TOKEN", "GITLAB_TOKEN"):
        token = os.environ.get(var, "")
        if token:
            return token
    res = run_glab("config", "get", "token", "--host", host, timeout=10)
    if res.ok and res.stdout:
        return res.stdout
    res = run_glab("auth", "status", "-t", timeout=10)
    for line in (res.stdout + "\n" + res.stderr).splitlines():
        if "Token:" in line:
            token = line.split("Token:")[-1].strip()
            if token:
                return token
    return ""
