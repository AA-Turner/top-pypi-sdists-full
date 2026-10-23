"""Which of Probe's Codex hooks Codex will actually run, from Codex itself.

Codex trusts each hooks.json entry by a hash of the whole entry and silently
skips one it has not approved, so a Probe update that changes an entry turns
that hook off with nothing in the session to say so. Codex's own
`hooks/list` call (its app-server JSON-RPC, the data behind `/hooks`) answers
it exactly: every hook's key, whether it is trusted, whether it is enabled,
and the load warnings `/hooks` shows as "N issues loading hooks".

Read-only and fail-soft: no Codex binary, an older Codex without `hooks/list`, a
timeout or an unexpected shape all return None, which `probe doctor` prints
as "unknown". Spawning the app-server costs about 0.2s, so only `probe
doctor`, the wizard's Diagnose and `probe status` ask, never a hook; `probe
status` asks at most once per STATUS_TTL_S and keeps the answer on disk
(`status_snapshot`).

`probe status` reads one more signal, from files alone: the heartbeat the
tracking plugins' dispatcher leaves for each Codex session it runs in
(`$XDG_STATE_HOME/probe/hooks/alive/<session>`), against the capture plugin's
record of whether that session expected one (`hooks/expect/<session>`, written
by probe-research-tap's hooks/probe-hooks-trust.sh). A session that expected
Probe's hooks and never heard them means they are not approved.
"""

from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

from probe._compat import StrEnum

#: Probe's Codex plugins, by the name before `@<marketplace>` in a hook key.
PROBE_PLUGINS = ("probe-research", "probe-research-daemon", "probe-research-tap")

#: What `trustStatus` says for a hook Codex will run.
TRUSTED = "trusted"

#: Seconds to wait for the app-server's answer before giving up.
TIMEOUT_S = 8.0

#: `probe status`: how long Codex's answer is kept, and how long a fresh ask may
#: wait. The desktop app reads status on every focus; a hung Codex costs at most
#: STATUS_TIMEOUT_S once per STATUS_TTL_S.
STATUS_TTL_S = 600.0
STATUS_TIMEOUT_S = 2.0
#: The cached answer, under the CLI's state folder.
STATUS_CACHE = "codex-hooks.json"
_CACHE_VERSION = 1

#: A session's SessionStart hooks run in parallel, so its heartbeat may land a
#: little after the capture plugin's record: a record younger than this is not
#: read yet. One older than HEARTBEAT_WINDOW_S (the files' own retention) is
#: not read at all.
HEARTBEAT_GRACE_S = 60.0
HEARTBEAT_WINDOW_S = 14 * 24 * 3600.0

#: Codex warnings about Probe that are by design, not a fault: the tap's
#: SessionEnd entry (`--wait`) keeps 20s for Claude Code's sake
#: (session-end.sh), and Codex says it clamps it to 3s.
_EXPECTED_WARNINGS = ("clamping SessionEnd hook timeout",)


class HooksState(StrEnum):
    """`probe status`'s `codex_hooks.state`."""

    #: Codex will run every enabled Probe hook.
    APPROVED = "approved"
    #: Codex skips some Probe hook until the person approves it in `/hooks`.
    NEEDS_APPROVAL = "needs_approval"
    #: Probe's Codex plugins are installed, and Codex could not be asked.
    UNKNOWN = "unknown"
    #: No Probe hook in Codex: no Probe plugin installed, or none enabled.
    NONE = "none"

_REQUESTS = (
    {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"clientInfo": {"name": "probe-doctor", "version": "1"}}},
    {"jsonrpc": "2.0", "method": "initialized"},
)
_LIST_ID = 2


@dataclass(frozen=True)
class HookStatus:
    """Probe's enabled Codex hooks, and which of them still need approval."""

    total: int
    #: Keys (`<plugin>@<marketplace>:hooks/hooks.json:<event>:<group>:<index>`)
    #: of enabled Probe hooks Codex will not run until approved.
    untrusted: tuple[str, ...] = ()
    #: Codex's load warnings that name a Probe plugin.
    warnings: tuple[str, ...] = field(default=())


def _plugin(key: str) -> str:
    return key.split("@", 1)[0]


def summarize(result: dict) -> HookStatus | None:
    """A `hooks/list` result -> Probe's share of it. None for an unknown shape."""
    data = result.get("data") if isinstance(result, dict) else None
    if not isinstance(data, list):
        return None
    seen: dict[str, str] = {}
    warnings: list[str] = []
    for scope in data:
        if not isinstance(scope, dict):
            return None
        hooks = scope.get("hooks") or []
        notes = scope.get("warnings") or []
        if not isinstance(hooks, list) or not isinstance(notes, list):
            return None
        for hook in hooks:
            if not isinstance(hook, dict) or not isinstance(hook.get("key"), str):
                return None
            if _plugin(hook["key"]) not in PROBE_PLUGINS or hook.get("enabled") is False:
                continue
            seen[hook["key"]] = str(hook.get("trustStatus") or "")
        for warning in notes:
            text = str(warning)
            if any(expected in text for expected in _EXPECTED_WARNINGS):
                continue
            if any(f"/{name}/" in text for name in PROBE_PLUGINS) and text not in warnings:
                warnings.append(text)
    untrusted = tuple(sorted(key for key, trust in seen.items() if trust != TRUSTED))
    return HookStatus(total=len(seen), untrusted=untrusted, warnings=tuple(warnings))


def codex_binary() -> str | None:
    """The Codex binary on PATH, or None."""
    from probe.cli.plugin_cli import CODEX
    from probe.harness.registry import get_registry

    name = get_registry().get(CODEX).binary
    return shutil.which(name) if name else None


def list_hooks(cwd: str | None = None, *, timeout: float = TIMEOUT_S) -> dict | None:
    """Codex's `hooks/list` result for `cwd`, or None when it cannot be had."""
    binary = codex_binary()
    if binary is None:
        return None
    try:
        where = cwd or os.getcwd()
    except OSError:
        where = os.path.expanduser("~")
    requests = [*_REQUESTS, {"jsonrpc": "2.0", "id": _LIST_ID, "method": "hooks/list", "params": {"cwds": [where]}}]
    try:
        proc = subprocess.Popen(  # noqa: S603 - the user's own codex binary
            [binary, "app-server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            # Its own group, so giving up ends a launcher script AND the
            # app-server it started, not the launcher alone.
            start_new_session=True,
        )
    except OSError:
        return None
    answer: dict = {}

    def read() -> None:
        assert proc.stdout is not None
        for line in proc.stdout:
            try:
                message = json.loads(line)
            except ValueError:
                continue
            if isinstance(message, dict) and message.get("id") == _LIST_ID:
                answer.update(message)
                return

    reader = threading.Thread(target=read, daemon=True)
    reader.start()
    try:
        assert proc.stdin is not None
        for request in requests:
            proc.stdin.write(json.dumps(request) + "\n")
        proc.stdin.flush()
        reader.join(timeout)
    except OSError:
        pass
    finally:
        try:
            if proc.stdin is not None:
                proc.stdin.close()
        except OSError:
            pass
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except OSError:
            proc.kill()
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            pass
    result = answer.get("result")
    return result if isinstance(result, dict) else None


def status(cwd: str | None = None, *, timeout: float = TIMEOUT_S) -> HookStatus | None:
    """Probe's Codex hooks as Codex sees them now; None when unknown."""
    result = list_hooks(cwd, timeout=timeout)
    try:
        return None if result is None else summarize(result)
    except Exception:  # noqa: BLE001 - doctor must never be the thing that breaks
        return None


# -- `probe status` ------------------------------------------------------------


def installed_copies() -> tuple[str, ...]:
    """`<marketplace>/<plugin>/<version>` for every Probe plugin copy in Codex's
    plugin cache (`$CODEX_HOME/plugins/cache`), sorted. Empty when there is none:
    then Codex runs no Probe hook, and nothing is asked."""
    from probe.cli import codex_config

    cache = codex_config.codex_home() / "plugins" / "cache"
    found: list[str] = []
    for marketplace in _names(cache):
        for plugin in PROBE_PLUGINS:
            found.extend(f"{marketplace}/{plugin}/{version}" for version in _names(cache / marketplace / plugin))
    return tuple(sorted(found))


def _names(folder: Path) -> list[str]:
    try:
        return [entry.name for entry in os.scandir(folder) if entry.is_dir() and not entry.name.startswith(".")]
    except OSError:
        return []


def _cache_path() -> Path:
    from probe.sdk import session_marker

    return session_marker.state_dir() / STATUS_CACHE


def _config_mtime() -> float | None:
    """Codex's config.toml's mtime: it holds the approvals (`[hooks.state]`), so
    a change since the cached answer makes that answer stale. Recorded after
    the ask, so a Codex that wrote it while answering is not asked again."""
    from probe.cli import codex_config

    try:
        return codex_config.config_path().stat().st_mtime
    except OSError:
        return None


def _cached(installed: tuple[str, ...], now: float) -> dict | None:
    """The cached answer, when it is for these installed copies, younger than
    STATUS_TTL_S and Codex's config has not changed since. Else None."""
    try:
        cached = json.loads(_cache_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(cached, dict) or cached.get("v") != _CACHE_VERSION or cached.get("installed") != list(installed):
        return None
    checked = cached.get("checked_at")
    if not isinstance(checked, (int, float)) or isinstance(checked, bool) or not 0 <= now - checked < STATUS_TTL_S:
        return None
    if cached.get("config_mtime") != _config_mtime():
        return None
    untrusted = cached.get("untrusted")
    total = cached.get("total")
    if untrusted is not None and not (isinstance(untrusted, list) and all(isinstance(k, str) for k in untrusted)):
        return None
    if total is not None and (not isinstance(total, int) or isinstance(total, bool)):
        return None
    return cached


def _remember(installed: tuple[str, ...], now: float, found: HookStatus | None) -> dict:
    """Codex's answer (None: it could not be asked) as the cache keeps it. An
    unknown answer is kept too, so a hung Codex is waited on once per TTL."""
    answer = {
        "v": _CACHE_VERSION,
        "installed": list(installed),
        "checked_at": now,
        "config_mtime": _config_mtime(),
        "total": None if found is None else found.total,
        "untrusted": None if found is None else list(found.untrusted),
    }
    try:
        from probe.sdk.durable import write_text_atomic

        path = _cache_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        write_text_atomic(path, json.dumps(answer), mode=0o600, sync="none")
    except (OSError, ValueError):
        pass
    return answer


def unheard_session(now: float | None = None) -> str | None:
    """The newest Codex session that expected Probe's hooks and has no heartbeat,
    or None: from probe-hooks-trust.sh's records (`hooks/expect/<sid>`, "1" when
    the session should hear them) and dispatch.py's heartbeats
    (`hooks/alive/<sid>`). Files only. Only the newest expecting record counts:
    it speaks for the approvals as they are now."""
    from probe.sdk import session_marker

    now = time.time() if now is None else now
    hooks = session_marker.state_dir() / "hooks"
    records = []
    try:
        for entry in os.scandir(hooks / "expect"):
            if entry.name.endswith(".shown") or not entry.is_file():
                continue
            age = now - entry.stat().st_mtime
            if HEARTBEAT_GRACE_S <= age <= HEARTBEAT_WINDOW_S:
                records.append((age, entry.name, entry.path))
    except OSError:
        return None
    for _age, name, path in sorted(records):
        try:
            with open(path, encoding="utf-8") as handle:
                flag = handle.readline().strip()
        except OSError:
            continue
        if flag != "1":
            continue
        return None if (hooks / "alive" / name).exists() else name
    return None


def blank_snapshot(state: HooksState) -> dict:
    """`codex_hooks` saying only `state`: nothing asked, no session read."""
    return {"state": state.value, "untrusted": [], "checked_at": None, "unheard_session": None}


def status_snapshot(*, now: float | None = None) -> dict:
    """`probe status`'s `codex_hooks` (its schema is `probe.cli.status`'s).

    Probe's Codex plugins not installed: `none`, nothing asked. Otherwise Codex's
    own answer, cached for STATUS_TTL_S (keyed by the installed copies, so an
    update asks again, and dropped when Codex's config changes, so an approval
    shows at once), asked afresh within STATUS_TIMEOUT_S only when a Codex binary
    is on PATH. Codex's answer decides; without one, a session that never heard
    Probe's hooks (`unheard_session`) says they need approval. Never raises."""
    now = time.time() if now is None else now
    snapshot = blank_snapshot(HooksState.NONE)
    try:
        installed = installed_copies()
        if not installed:
            return snapshot
        answer = _cached(installed, now)
        if answer is None and codex_binary() is not None:
            answer = _remember(installed, now, status(timeout=STATUS_TIMEOUT_S))
        unheard = unheard_session(now)
    except Exception:  # noqa: BLE001 - a status read never raises
        return blank_snapshot(HooksState.UNKNOWN)
    snapshot["unheard_session"] = unheard
    if answer is not None:
        snapshot["checked_at"] = int(answer["checked_at"])
    if answer is not None and answer.get("total") is not None:
        snapshot["untrusted"] = list(answer.get("untrusted") or [])
        if snapshot["untrusted"]:
            state = HooksState.NEEDS_APPROVAL
        else:
            state = HooksState.APPROVED if answer["total"] else HooksState.NONE
    else:
        state = HooksState.NEEDS_APPROVAL if unheard else HooksState.UNKNOWN
    snapshot["state"] = state.value
    return snapshot


def status_line(snapshot: dict | None) -> str | None:
    """`probe status`'s one line for a person, or None when there is nothing to say."""
    state = (snapshot or {}).get("state")
    if state == HooksState.NEEDS_APPROVAL:
        waiting = len((snapshot or {}).get("untrusted") or [])
        what = f"{waiting} Probe hook{'s' if waiting != 1 else ''} switched off" if waiting else "Probe's hooks are off"
        return f"{what} until approved: in Codex, type /hooks and approve the Probe Research hooks"
    if state == HooksState.APPROVED:
        return "all approved"
    if state == HooksState.UNKNOWN:
        return "unknown (in Codex, type /hooks to check)"
    return None


def rows(found: HookStatus | None, row) -> list[str]:
    """`probe doctor`'s "Codex hooks" section; `row` is doctor's row formatter."""
    lines = ["Codex hooks"]
    if found is None:
        lines.append(row("Probe hooks", "unknown (Codex could not be asked; open /hooks in Codex)"))
        return lines
    if found.total == 0:
        lines.append(row("Probe hooks", "none enabled in Codex"))
    elif not found.untrusted:
        lines.append(row("Probe hooks", f"all {found.total} approved"))
    else:
        lines.append(
            row(
                "Probe hooks",
                f"{len(found.untrusted)} of {found.total} switched off until approved -- "
                "in Codex, type /hooks and approve the Probe Research hooks",
            )
        )
        plugins = sorted({_plugin(key) for key in found.untrusted})
        lines.append(row("", "waiting: " + ", ".join(plugins)))
    for warning in found.warnings:
        lines.append(row("Codex warns", warning[:200]))
    return lines
