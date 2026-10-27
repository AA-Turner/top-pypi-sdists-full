"""Which of Probe's Codex hooks Codex will actually run, from Codex itself.

Codex trusts each hooks.json entry by a hash of the whole entry and silently
skips one it has not approved, so a Probe update that changes an entry turns
that hook off with nothing in the session to say so. Codex's own
`hooks/list` call (its app-server JSON-RPC, the data behind `/hooks`) answers
it exactly: every hook's key, whether it is trusted, whether it is enabled,
and the load warnings `/hooks` shows as "N issues loading hooks".

Fail-soft: no Codex binary, an older Codex without `hooks/list`, a timeout or
an unexpected shape all return None, which `probe doctor` prints as
"unknown". Spawning the app-server costs about 0.2s, so it is asked by `probe
doctor`, the wizard's Diagnose and `probe status` (at most once per
STATUS_TTL_S, the answer kept on disk: `status_snapshot`), and never by a hook.

It also WRITES, through `approve` alone: the wizard, a recorder switch and every
Codex plugin update approve Probe's own hooks in Codex's config.toml the way
`/hooks` does (see the section above `approve`).

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


class _AppServer:
    """One `codex app-server` over stdio: `call` sends a request and waits up to
    `timeout` for its answer, `close` ends the server and whatever a launcher
    script started with it."""

    def __init__(self, binary: str, timeout: float) -> None:
        self.timeout = timeout
        self.proc = subprocess.Popen(  # noqa: S603 - the user's own codex binary
            [binary, "app-server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            # Codex writes UTF-8 on every platform; Windows' default would read
            # it as cp1252 (a non-ASCII profile path garbled, or the reader dead).
            text=True,
            encoding="utf-8",
            errors="replace",
            # Its own group (POSIX), so giving up ends a launcher script AND the
            # app-server it started, not the launcher alone.
            start_new_session=True,
        )
        self.answers: dict[int, dict] = {}
        #: The last answer that was a JSON-RPC error, for the caller to name.
        self.error: dict | None = None
        #: The server closed its output: nothing more will be answered.
        self.ended = False
        #: A config write was sent: `close` lets the server finish it.
        self.wrote = False
        self.arrived = threading.Condition()
        try:
            threading.Thread(target=self._read, daemon=True).start()
        except BaseException:
            self.close()
            raise

    def _read(self) -> None:
        assert self.proc.stdout is not None
        try:
            for line in self.proc.stdout:
                try:
                    message = json.loads(line)
                except ValueError:
                    continue
                if isinstance(message, dict) and isinstance(message.get("id"), int):
                    with self.arrived:
                        self.answers[message["id"]] = message
                        self.arrived.notify_all()
        except (OSError, ValueError):
            pass
        with self.arrived:
            self.ended = True
            self.arrived.notify_all()

    def send(self, *messages: dict) -> bool:
        try:
            assert self.proc.stdin is not None
            for message in messages:
                self.proc.stdin.write(json.dumps(message) + "\n")
            self.proc.stdin.flush()
        except (OSError, ValueError):
            return False
        return True

    def call(self, request_id: int, method: str, params: dict) -> dict | None:
        """The answer's `result`, or None for an error, a timeout or a dead server."""
        self.wrote = self.wrote or method.startswith("config/")
        if not self.send({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}):
            return None
        with self.arrived:
            self.arrived.wait_for(lambda: request_id in self.answers or self.ended, timeout=self.timeout)
            answer = self.answers.get(request_id, {})
            result = answer.get("result")
            error = answer.get("error")
        if isinstance(error, dict):
            self.error = error
        return result if isinstance(result, dict) else None

    def close(self) -> None:
        """End the server. Never raises. Closing its input ends a real app-server
        within milliseconds (measured 0.03s, codex-cli 0.164.0); one that sent a
        config write gets up to 2s to finish it before anything is killed."""
        try:
            if self.proc.stdin is not None:
                self.proc.stdin.close()
        except Exception:  # noqa: BLE001 - closing is best effort
            pass
        try:
            self.proc.wait(timeout=2.0 if self.wrote else 0.2)
            return
        except Exception:  # noqa: BLE001 - still running: kill it below
            pass
        # Windows has no process groups or SIGKILL: `taskkill /T` ends the tree
        # an npm launcher starts (codex.cmd -> node -> codex.exe).
        killpg, sigkill = getattr(os, "killpg", None), getattr(signal, "SIGKILL", None)
        try:
            if killpg is not None and sigkill is not None:
                killpg(self.proc.pid, sigkill)
            elif _on_windows():
                subprocess.run(  # noqa: S603, S607 - Windows' own taskkill
                    ["taskkill", "/T", "/F", "/PID", str(self.proc.pid)], capture_output=True, timeout=5
                )
            else:
                self.proc.kill()
        except Exception:  # noqa: BLE001 - already gone, or not ours to kill
            try:
                self.proc.kill()
            except Exception:  # noqa: BLE001
                pass
        try:
            self.proc.wait(timeout=2)
        except Exception:  # noqa: BLE001
            pass


def _on_windows() -> bool:
    return os.name == "nt"


def _open(timeout: float) -> _AppServer | None:
    """A started and initialized app-server, or None without a Codex to start."""
    binary = codex_binary()
    if binary is None:
        return None
    try:
        server = _AppServer(binary, timeout)
    except Exception:  # noqa: BLE001 - no server is "Codex could not be asked"
        return None
    server.send(*_REQUESTS)
    return server


def _where(cwd: str | None) -> str:
    try:
        return cwd or os.getcwd()
    except OSError:
        return os.path.expanduser("~")


def list_hooks(cwd: str | None = None, *, timeout: float = TIMEOUT_S) -> dict | None:
    """Codex's `hooks/list` result for `cwd`, or None when it cannot be had."""
    server = _open(timeout)
    if server is None:
        return None
    try:
        return server.call(_LIST_ID, "hooks/list", {"cwds": [_where(cwd)]})
    finally:
        server.close()


def status(cwd: str | None = None, *, timeout: float = TIMEOUT_S) -> HookStatus | None:
    """Probe's Codex hooks as Codex sees them now; None when unknown."""
    result = list_hooks(cwd, timeout=timeout)
    try:
        return None if result is None else summarize(result)
    except Exception:  # noqa: BLE001 - doctor must never be the thing that breaks
        return None


# -- approving Probe's own hooks -------------------------------------------------
#
# Codex writes an approval as `[hooks.state."<key>"] trusted_hash = "<hash>"` in
# the user's config.toml, and its app-server's `config/batchWrite` is how it does
# so itself: `/hooks` in the app, and the automatic approval of plugins shared
# through a ChatGPT workspace (codex-rs/app-server/src/effective_plugin_change.rs,
# which a git marketplace like Probe's never qualifies for). Probe makes the same
# write for its own plugins' hooks, so they run without a trip to `/hooks`.

#: The trust states `approve` writes over. `modified` is an approved entry whose
#: text changed since, which is what a Probe update that edits one leaves.
_UNAPPROVED = ("untrusted", "modified")
_APPROVE_LIST_ID = 2
_WRITE_ID = 3
_CHECK_ID = 4


@dataclass(frozen=True)
class Approval:
    """What `approve` did."""

    #: Keys Codex now reads as trusted that it did not before.
    approved: tuple[str, ...] = ()
    #: Why some Probe hook still waits, when one does.
    error: str | None = None
    #: No Probe hook waits for approval now, by `summarize`'s count: every enabled
    #: hook of a Probe-named plugin. Stricter than "nothing `approve` may touch":
    #: a Probe hook it must not approve (another marketplace's) still waits.
    done: bool = False


def approvable(result: dict, cache: Path, marketplace: str) -> list[tuple[str, str]]:
    """(key, currentHash) of each enabled hook in a `hooks/list` result that is
    Probe's own and not approved: a hook of one of PROBE_PLUGINS from
    `marketplace`, loaded from that plugin's copy under Codex's plugin `cache`.
    Anything else -- another plugin's, a project's, a user's, a managed one, a
    Probe-named plugin from another marketplace -- is never touched."""
    found: dict[str, str] = {}
    data = result.get("data") if isinstance(result, dict) else None
    for scope in data if isinstance(data, list) else []:
        hooks = scope.get("hooks") if isinstance(scope, dict) else None
        for hook in hooks if isinstance(hooks, list) else []:
            if not isinstance(hook, dict) or hook.get("source") != "plugin" or hook.get("isManaged"):
                continue
            key, plugin_id, digest = hook.get("key"), hook.get("pluginId"), hook.get("currentHash")
            if not (isinstance(key, str) and isinstance(digest, str) and digest):
                continue
            plugin = _plugin(key)
            if plugin not in PROBE_PLUGINS or plugin_id != f"{plugin}@{marketplace}":
                continue
            if not key.startswith(f"{plugin_id}:") or hook.get("enabled") is False:
                continue
            if hook.get("trustStatus") not in _UNAPPROVED:
                continue
            if not _inside(hook.get("sourcePath"), cache / marketplace / plugin):
                continue
            found[key] = digest
    return sorted(found.items())


def _inside(path: object, folder: Path) -> bool:
    if not isinstance(path, str) or not path:
        return False
    try:
        return _plain(Path(path).resolve()).is_relative_to(_plain(folder.resolve()))
    except (OSError, ValueError):
        return False


def _plain(path: Path) -> Path:
    r"""`path` without Windows' extended-length prefix: Codex reports a set
    CODEX_HOME as `\\?\C:\...`, which `resolve` keeps and a plain path never matches."""
    text = str(path)
    for prefix in ("\\\\?\\UNC\\", "\\\\?\\"):
        if text.startswith(prefix):
            return Path(("\\\\" if "UNC" in prefix else "") + text[len(prefix):])
    return path


def _trust_states(result: dict | None) -> dict[str, str]:
    """`key -> trustStatus` for every hook a `hooks/list` result names."""
    states: dict[str, str] = {}
    data = result.get("data") if isinstance(result, dict) else None
    for scope in data if isinstance(data, list) else []:
        hooks = scope.get("hooks") if isinstance(scope, dict) else None
        for hook in hooks if isinstance(hooks, list) else []:
            if isinstance(hook, dict) and isinstance(hook.get("key"), str):
                states[hook["key"]] = str(hook.get("trustStatus") or "")
    return states


def _none_waiting(result: dict | None, only: frozenset[str] | None = None) -> bool:
    try:
        found = summarize(result) if isinstance(result, dict) else None
    except Exception:  # noqa: BLE001 - an unknown shape is "not known to be done"
        return False
    return found is not None and not [key for key in found.untrusted if only is None or _plugin(key) in only]


def _refusal(error: dict | None) -> str:
    """Why Codex did not take the write, in its own words where it gave some."""
    if not error:
        return "Codex did not answer"
    if error.get("code") == -32601:
        return "this Codex is too old to take it"
    message = " ".join(str(error.get("message") or "").split())[:200]
    return f"Codex refused it: {message}" if message else "Codex refused it"


def _trust_edit(key: str, digest: str) -> dict:
    """The config edit `/hooks` makes to approve `key` at `digest`."""
    quoted = key.replace("\\", "\\\\").replace('"', '\\"')
    return {"keyPath": f'hooks.state."{quoted}".trusted_hash', "value": digest, "mergeStrategy": "replace"}


def _cache() -> Path:
    from probe.cli import codex_config

    return codex_config.codex_home() / "plugins" / "cache"


def waiting(cwd: str | None = None, *, timeout: float = TIMEOUT_S) -> bool:
    """Some hook `approve` would approve is waiting: the same rule, so a hook
    Probe may not approve (another marketplace's Probe-named plugin) never
    reads as work for it. False when Codex cannot be asked. Never raises."""
    from probe.cli.capabilities import MARKETPLACE

    try:
        result = list_hooks(cwd, timeout=timeout)
        return bool(result is not None and approvable(result, _cache(), MARKETPLACE))
    except Exception:  # noqa: BLE001 - a question asked before the plan never fails it
        return False


def approve(
    cwd: str | None = None, *, timeout: float = TIMEOUT_S, only: frozenset[str] | None = None
) -> Approval | None:
    """Approve Probe's own Codex hooks that Codex would skip, and check that it
    took. None when Codex could not be asked at all (no binary, no answer). An
    Approval with nothing approved and no error means none of the hooks it may
    approve (`approvable`) was waiting. Never raises: an install or an update
    never fails on this. `only` narrows it to those Probe plugins (the wizard's
    selection: a capability turned off is never approved in the same run).

    Each call to the app-server gets `timeout` of its own, so a slow start
    cannot leave the write without time. Codex reads approvals when a session
    starts, so a session already open keeps skipping them until the next one."""
    server = None
    try:
        from probe.cli.capabilities import MARKETPLACE

        server = _open(timeout)
        if server is None:
            return None
        params = {"cwds": [_where(cwd)]}
        listed = server.call(_APPROVE_LIST_ID, "hooks/list", params)
        if listed is None:
            return None
        found = [
            (key, digest)
            for key, digest in approvable(listed, _cache(), MARKETPLACE)
            if only is None or _plugin(key) in only
        ]
        if not found:
            return Approval(done=_none_waiting(listed, only))
        edits = [_trust_edit(key, digest) for key, digest in found]
        if server.call(_WRITE_ID, "config/batchWrite", {"edits": edits, "reloadUserConfig": True}) is None:
            return Approval(error=_refusal(server.error))
        checked = server.call(_CHECK_ID, "hooks/list", params)
        if checked is None:
            return Approval(error="Codex did not confirm the approval")
        # Approved means Codex now SAYS trusted: a key the re-list drops, or reads in
        # any other state, is not.
        states = _trust_states(checked)
        approved = tuple(key for key, _ in found if states.get(key) == TRUSTED)
        waiting = len(found) - len(approved)
        return Approval(
            approved=approved,
            error=f"{waiting} still waiting" if waiting else None,
            done=not waiting and _none_waiting(checked, only),
        )
    except Exception:  # noqa: BLE001 - an install or an update never fails on this
        return Approval(error="could not approve them")
    finally:
        if server is not None:
            server.close()


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
