"""where an agent's capture credential resolves from (tap folder, env, CLI config), and verify or revoke it with the server."""

from __future__ import annotations

import http.client
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

ENV_INGEST_TOKEN = "PROBE_INGEST_TOKEN"
ENV_TAP_PLUGIN_DIR = "PROBE_RESEARCH_TAP_PLUGIN_DIR"
ENV_CONFIG_PATH = "PROBE_CONFIG_PATH"
ENV_CODEX_INGEST_TOKEN = "PRBE_CODEX_TAP_TOKEN"
ENV_CODEX_TAP_PLUGIN_DIR = "PRBE_CODEX_TAP_PLUGIN_DIR"
ENV_PI_INGEST_TOKEN = "PROBE_PI_TAP_TOKEN"
ENV_PI_TAP_PLUGIN_DIR = "PROBE_PI_TAP_PLUGIN_DIR"

#: Per-source overrides for the tap's token/plugin-dir env vars, read from the
#: harness registry (probe/foundation/harness_registry/harnesses.json, `capture` of each captured
#: row). The tap package reads its own copy of the same file, so the two can no
#: longer drift (tests/test_harness_conformance.py). claude_code is the
#: registry's default; ENV_INGEST_TOKEN / ENV_TAP_PLUGIN_DIR remain its names.
def _capture_rows() -> dict:
    from probe.foundation.harness_registry import get_registry

    return {h.id: h.capture for h in get_registry().captured()}


_TAP_TOKEN_ENV_BY_SOURCE: dict[str, str] = {
    source: capture.token_env for source, capture in _capture_rows().items() if source != "claude_code"
}
_TAP_PLUGIN_DIR_ENV_BY_SOURCE: dict[str, str] = {
    source: capture.plugin_dir_env for source, capture in _capture_rows().items() if source != "claude_code"
}


def tap_token_env(source: str | None = None) -> str:
    """The env var name the tap reads a credential from, for `source` (or the
    ambient agent).

    Table-driven off `_TAP_TOKEN_ENV_BY_SOURCE` rather than a hand-typed
    two-way ternary: `doctor.py` and `capture.py` each used to spell
    `ENV_CODEX_INGEST_TOKEN if source == "codex" else ENV_INGEST_TOKEN`
    independently, and both silently named pi's leaked env var
    `PROBE_INGEST_TOKEN` instead of `PROBE_PI_TAP_TOKEN` -- correct-looking,
    wrong variable, in a warning whose whole point is telling someone which
    variable to unset.
    """
    selected = source or agent_source()
    return _TAP_TOKEN_ENV_BY_SOURCE.get(selected, ENV_INGEST_TOKEN)


def tap_plugin_dir(source: str | None = None) -> Path:
    """The capture tap's state folder for an agent, from its registry row:
    the override variable, else the current folder, else a legacy folder an
    older install left (Codex's retired standalone plugin name). The tap
    resolves the same row from its own copy of the registry."""
    from probe.foundation.harness_registry import get_registry

    selected = source or agent_source()
    capture = get_registry().get(selected).capture
    if capture is None:
        raise ValueError(f"{selected!r} has no capture tap")
    return capture.state_dir()


def probe_config_path() -> Path:
    env = os.environ.get(ENV_CONFIG_PATH)
    if env:
        return Path(env)
    xdg = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg) if xdg else Path.home() / ".config"
    return base / "probe" / "config.json"


def _read_json(path: Path) -> dict:
    try:
        loaded = json.loads(path.read_text())
    except (OSError, ValueError):
        return {}
    return loaded if isinstance(loaded, dict) else {}


def probe_config_credentials() -> dict:
    """The probe CLI config flattened the way the UPLOADER reads it.

    This MUST mirror `tap/config.py:_read_probe_config()` exactly. The CLI writes
    v2 (named contexts) as of the workspace-context pass, and when `contexts`
    exists the uploader reads ONLY the active context -- it does not fall back to
    the top level.

    Reading just the top-level key would therefore miss the credential on every
    modern config, and this function backs the off switch: a miss means we clear
    nothing, re-verify nothing, and report "capture is off" while it keeps
    shipping. The parity test in tests/test_setup_wizard.py guards the pairing.
    """
    raw = _read_json(probe_config_path())
    contexts = raw.get("contexts")
    if isinstance(contexts, dict):
        active = contexts.get(raw.get("current_context") or "default")
        return active if isinstance(active, dict) else {}
    return raw


def consumes_cli_capture_token(source: str) -> bool:
    """Does this agent's uploader fall back to the probe CLI config's
    `ingest_token`? Only Claude Code: that token is the capture token minted
    for Claude Code, and the server refuses a paired token on any other
    agent's route. Mirrors tap/config.py::load_token() and the pi extension's
    pairing.ts (decision D3, 2026-09-09). Read from the harness registry
    (`capture.cli_token_fallback`)."""
    from probe.foundation.harness_registry import get_registry

    harness = get_registry().find(source)
    return bool(harness and harness.capture and harness.capture.cli_token_fallback)


def capture_token_sources(source: str | None = None) -> tuple[TokenSource, ...]:
    """Every place a capture credential currently resolves from, in the
    uploader's own precedence order.

    Mirrors `tap/config.py:load_token()`. It is duplicated rather than imported
    because the tap is a separate plugin package living in Claude Code's plugin
    cache -- the CLI cannot import it. Any change there must change here, which
    is what the parity tests in tests/test_setup_wizard.py exist to catch.
    """
    found: list[TokenSource] = []
    selected = source or agent_source()
    token_file = tap_plugin_dir(selected) / ".token"
    try:
        if token_file.read_text().strip():
            found.append(TokenSource.PAIRED_FILE)
    except OSError:
        pass
    token_env = _TAP_TOKEN_ENV_BY_SOURCE.get(selected, ENV_INGEST_TOKEN)
    if (os.environ.get(token_env) or "").strip():
        found.append(TokenSource.ENVIRONMENT)
    if (
        # Mirrors tap/config.py::load_token(): the probe CLI config's
        # `ingest_token` is the capture token minted for Claude Code, and the
        # server refuses it on every other agent's route (a paired device
        # token is bound to its source). So only Claude Code falls back to it;
        # Codex and pi resolve their own paired token or env var, or nothing.
        consumes_cli_capture_token(selected)
        and str(probe_config_credentials().get("ingest_token") or "").strip()
    ):
        found.append(TokenSource.PROBE_CONFIG)
    return tuple(found)


def resolved_capture_credential(source: str | None = None) -> tuple[str, str] | None:
    """The uploader's winning (token, base URL), or None when incomplete."""
    selected = source or agent_source()
    token = ""
    token_file = tap_plugin_dir(selected) / ".token"
    try:
        token = token_file.read_text(encoding="utf-8").strip()
    except OSError:
        pass
    if not token:
        token_env = _TAP_TOKEN_ENV_BY_SOURCE.get(selected, ENV_INGEST_TOKEN)
        token = (os.environ.get(token_env) or "").strip()
    if not token and consumes_cli_capture_token(selected):
        token = str(probe_config_credentials().get("ingest_token") or "").strip()

    base_url = (os.environ.get("PROBE_BASE_URL") or "").strip().rstrip("/")
    if not base_url:
        plugin_config = _read_json(tap_plugin_dir(selected) / ".config")
        base_url = str(plugin_config.get("api_base_url") or "").strip().rstrip("/")
    if not base_url:
        base_url = str(probe_config_credentials().get("base_url") or "").strip().rstrip("/")
    return (token, base_url) if token and base_url else None


def revoke_capture_device(source: str | None = None, *, timeout: float = 5.0) -> bool | None:
    """Tell the server this device is done, BEFORE the local credential is wiped.

    True = the server revoked it. False = it answered, and there was nothing
    live to revoke (an already-revoked or unknown token). None = we could not
    ask (no credential, no base URL, offline, timeout, server error).

    ORDER IS THE WHOLE POINT. The bearer this authenticates with is the same
    `<plugin>/.token` that `turn_off` deletes one step later, so this has to run
    first or it can never run at all -- not here, and not from a later
    `python -m tap revoke` either, which reads the same file and skips the
    server call when it finds nothing. Without this the row keeps
    `revoked_at IS NULL` forever: the machine lingers in the dashboard's device
    list and its capture credential stays valid on a token nobody holds.

    `reason` is what stops this being read as a re-pair. The same endpoint
    serves both flows, and the churn channel counts an uninstall as a departure
    (see `DisconnectReason` in app/core/analytics.py).

    NEVER RAISES, and never blocks the teardown. Turning capture off is a
    consent guarantee about THIS machine, and it is satisfied by the local work
    that follows whether or not the network is reachable -- an unreachable
    server must not leave a user unable to turn capture off.
    """
    resolved = resolved_capture_credential(source)
    if resolved is None:
        return None
    return revoke_capture_token(*resolved, timeout=timeout)


def revoke_capture_token(token: str, base_url: str, *, timeout: float = 5.0) -> bool | None:
    """`revoke_capture_device`'s server call for a token already in hand.
    Same answers, and it never raises either."""
    try:
        request = urllib.request.Request(
            f"{base_url}/agent-tap/revoke",
            data=json.dumps({"reason": "uninstall"}).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "probe-capture-off/1"},
            method="POST",
        )
        request.add_unredirected_header("Authorization", f"Bearer {token}")
        with _credential_opener().open(request, timeout=timeout) as response:
            return response.status == 200
    except urllib.error.HTTPError as exc:
        # 401 is the documented benign case: already revoked, or unknown.
        return False if exc.code in {401, 403, 404} else None
    # ValueError: a base URL with no scheme or a bad port (http.client.InvalidURL);
    # HTTPException: a malformed answer (a proxy's BadStatusLine).
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, http.client.HTTPException):
        return None


def verify_capture_credential(source: str | None = None, *, timeout: float = 5.0) -> bool | None:
    """Ask the ingest status endpoint whether the resolved token is accepted.

    False is reserved for an authoritative 401/403. Offline, timeouts, and
    server errors stay unknown so `probe doctor` remains fail-soft and does not
    turn capture off merely because a laptop has no network.
    """
    resolved = resolved_capture_credential(source)
    if resolved is None:
        return None
    token, base_url = resolved
    request = urllib.request.Request(
        f"{base_url}/ingest/v1/sessions/status", headers={"User-Agent": "probe-doctor/1"}
    )
    # Never redirected: urllib would carry the bearer to the Location host, and
    # an SSO login page's 200 would read as "accepted".
    request.add_unredirected_header("Authorization", f"Bearer {token}")
    try:
        with _credential_opener().open(request, timeout=timeout) as response:
            return True if response.status == 200 else None
    except urllib.error.HTTPError as exc:
        return False if exc.code in {401, 403} else None
    except (urllib.error.URLError, TimeoutError, OSError):
        return None


def capture_device_id(source: str | None = None) -> str | None:
    """The paired device id the uploader recorded, if any.

    Read straight from the tap's SQLite state rather than shelling out to it:
    `probe doctor` must work when the plugin's Python cannot run at all, which
    is exactly the situation someone runs a doctor command in.
    """
    db = tap_plugin_dir(source) / "state.db"
    if not db.exists():
        return None
    import sqlite3

    try:
        with sqlite3.connect(f"file:{db}?mode=ro", uri=True) as connection:
            row = connection.execute("SELECT v FROM meta WHERE k = 'device_id'").fetchone()
    except sqlite3.Error:
        return None
    return str(row[0]) if row and row[0] else None
from probe.cli.wizard.state.agent_identity import agent_source  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.state.credential_http import _credential_opener  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.state.state import TokenSource  # noqa: E402 -- pieces need each other; the front door loads this one first
