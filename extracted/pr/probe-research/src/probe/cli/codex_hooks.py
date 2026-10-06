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
doctor` and the wizard's Diagnose ask, never a hook.
"""

from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import threading
from dataclasses import dataclass, field

#: Probe's Codex plugins, by the name before `@<marketplace>` in a hook key.
PROBE_PLUGINS = ("probe-research", "probe-research-daemon", "probe-research-tap")

#: What `trustStatus` says for a hook Codex will run.
TRUSTED = "trusted"

#: Seconds to wait for the app-server's answer before giving up.
TIMEOUT_S = 8.0

#: Codex warnings about Probe that are by design, not a fault: the tap's
#: `--wait` SessionEnd entry keeps 20s for Claude Code's sake (session-end.sh),
#: and Codex says it clamps it to 3s.
_EXPECTED_WARNINGS = ("clamping SessionEnd hook timeout",)

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


def list_hooks(cwd: str | None = None, *, timeout: float = TIMEOUT_S) -> dict | None:
    """Codex's `hooks/list` result for `cwd`, or None when it cannot be had."""
    from probe.cli.plugin_cli import CODEX
    from probe.harness.registry import get_registry

    name = get_registry().get(CODEX).binary
    binary = shutil.which(name) if name else None
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


def status(cwd: str | None = None) -> HookStatus | None:
    """Probe's Codex hooks as Codex sees them now; None when unknown."""
    result = list_hooks(cwd)
    try:
        return None if result is None else summarize(result)
    except Exception:  # noqa: BLE001 - doctor must never be the thing that breaks
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
