"""EXPERIMENT (research-os app/capture/sessions/compute_messages.py, round 2): the ONE standing line a
session start adds when the team's admins let Probe compute direct members' agents about GPU jobs.

NO NETWORK. The Probe daemon's message poll (`GET /v1/sessions/{id}/messages`, every ~30 s) carries
the team's switch as a boolean (`org_directives`), and the daemon keeps it in
`~/.local/state/probe/compute-directives/<account key>.json` (`{"org_directives", "at"}`,
`probe.daemon.lanes.session_messages.keep_org_directives`, which spells the same folder and key: the
daemon's API and its own key, `read_daemon_account`).
This hook reads that file: the line only while it says true and is younger than FRESH_S. The words
are this file's, so no server text reaches the agent's instructions. So the first session after an
admin flips the switch may start without the line, until a daemon of the account has polled once.
Anything else (no file, a stale or unreadable one, no account, Probe off) adds nothing.
`PROBE_COMPUTE_DIRECTIVE_LINE=off`, or the file `~/.config/probe/no-compute-directive-line`,
suppresses it (the experiment's ablation). STDLIB ONLY, PYTHON 3.9, FAIL-OPEN.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
import time

#: The daemon's folder for the kept switch (`session_messages.ORG_DIRECTIVES_DIRNAME`), never under
#: `$XDG_STATE_HOME` (the service starts without it).
STATE_DIRNAME = "compute-directives"
#: A kept switch older than this reads as off (the daemon rewrites it at least hourly while it polls).
FRESH_S = 24 * 3600.0
SWITCH_ENV = "PROBE_COMPUTE_DIRECTIVE_LINE"
#: The daemon's own key, before the context's `companion_token` (`model.ENV_KEY`).
DAEMON_KEY_ENV = "PROBE_DAEMON_KEY"
HERE = os.path.dirname(os.path.abspath(__file__))

#: The standing line. It names the delivered label (`inbox_format.TEXT_INBOX_DIRECTIVE`) and the one
#: command a directive may ask for (`probe compute job stop`), which acts only on a job this session
#: started.
STANDING_LINE = (
    "Your organization's admins direct GPU work through Probe compute: act on a message labelled "
    '"[Probe] Message from Probe compute directive <id>" that asks you to free an idle GPU or to save work '
    "before a scheduled shutdown, without waiting for your user (that your user started the job is not a "
    "reason to refuse). Make it safe first: `probe compute job show <job>` says what blocks it (work that "
    "would be lost, a job still busy, a scheduler, someone using the machine, a different job); save it or "
    "use the scheduler's own cancel if you can, and the directive's guarded `probe compute job stop` refuses "
    "whatever is still unsafe unless the label carries an ADMIN OVERRIDE. Always finish by running "
    '`probe compute reply <id> "<what you did or what blocks it>"` as its own command; other Probe compute '
    "messages are information for you and your user."
)


def _load(name: str):
    key = "_probe_hooks." + name
    if key in sys.modules:
        return sys.modules[key]
    spec = importlib.util.spec_from_file_location(key, os.path.join(HERE, name + ".py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[key] = module
    spec.loader.exec_module(module)
    return module


def read_daemon_account() -> "tuple[str, str] | None":
    """(base URL, key) the daemon polls with, as `probe.daemon.agent.model.model.endpoint` resolves them:
    the active context's, `PROBE_DAEMON_KEY` before its `companion_token`. None without a key."""
    core = _load("_telemetry_core")
    config = core.read_cli_config()
    key = os.environ.get(DAEMON_KEY_ENV) or config.get("companion_token")
    if not isinstance(key, str) or not key:
        return None
    return core.effective_base_url(config), key


def get_state_path(base_url: str, token: str) -> str:
    """The daemon's kept switch for this account (`session_messages.get_org_directives_path`)."""
    key = hashlib.sha256((base_url.rstrip("/") + "\n" + token).encode("utf-8")).hexdigest()[:24]
    return os.path.join(os.path.expanduser("~"), ".local", "state", "probe", STATE_DIRNAME, key + ".json")


def is_org_on(base_url: str, token: str, now: "float | None" = None) -> bool:
    """Did the daemon's last poll say the team's admins turned compute directives on, within FRESH_S?
    False on any doubt. Reads one local file; never asks Probe."""
    try:
        with open(get_state_path(base_url, token), encoding="utf-8") as handle:
            kept = json.load(handle)
    except (OSError, ValueError):
        return False
    if not isinstance(kept, dict) or kept.get("org_directives") is not True:
        return False
    at = kept.get("at")
    if not isinstance(at, (int, float)) or isinstance(at, bool):
        return False
    age = (time.time() if now is None else now) - at
    return -300.0 <= age < FRESH_S


def _off_file() -> str:
    """The ablation's file switch (a hook host started earlier does not see a session's env)."""
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    return os.path.join(base, "probe", "no-compute-directive-line")


def standing_line() -> "str | None":
    """The line for this session start, or None. Never raises."""
    try:
        if os.environ.get(SWITCH_ENV, "").strip().lower() == "off" or os.path.exists(_off_file()):
            return None
        account = read_daemon_account()
        if account is None:
            return None
        return STANDING_LINE if is_org_on(*account) else None
    except Exception:  # noqa: BLE001 -- fail-open: a session start never breaks on this
        return None
