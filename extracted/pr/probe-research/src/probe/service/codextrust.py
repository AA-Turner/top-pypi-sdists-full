"""The Probe service keeps Codex running Probe's hooks (#3617).

Codex's copies of Probe's plugins are rebuilt from Probe's marketplace, which
serves main: merging is the plugins' release. Any rewrite of a copy, a new
version or the same one written again, reads every hook in it as changed
("plugin contents changed; hook approval required"), and Codex runs none of
them and says nothing, so its sessions record nothing. Approving them again
came only with an update (`probe.cli.updater.update_codex_plugins`), which a
live run holds off for up to a day: a training box stayed off.

    every TICK_S     a stat of each file of Probe's plugin copies in Codex's
                     cache (`<Codex home>/plugins/cache/<MARKETPLACE>/<plugin>/`),
                     on a thread: the fingerprint. The bytecode Probe's own hooks
                     write there (`__pycache__`) is no change. No copy: nothing
                     to keep.
    a new one        (not the one this machine last settled, kept in RECORD_NAME,
                     so a new service asks only about a change it has not seen)
                     one `probe.core.run codex_trust` child: the update's own
                     approval (`codex_hooks.heal` -> `approve`: Probe's own hooks
                     only, through Codex's app-server). Never while an update
                     cycle, an action, a desktop change or a `probe wizard` from
                     a terminal runs (they write Codex's config too): the next
                     tick asks. An ask in flight keeps the service up.
    settled          Codex trusts every hook Probe may approve, and the copies
                     did not move while it was asked: nothing is asked again
                     until they change.
    not settled      Codex refused or did not answer: asked again BACKOFF_S later
                     (1, 2, 5, 10, then every 15 min) for as long as it takes.
                     Copies that moved while it was asked, or a new change, are
                     asked about at the next tick. No codex on the login PATH
                     asks nothing more about those copies until the login
                     shell is read again (LOGIN_TTL_S) or they change.
    at most          MAX_ASKS_PER_HOUR children in any hour, whatever changes.
    off              automatic updates turned off: nothing is approved without
                     the person (`probe doctor --fix`, or `/hooks` in Codex), as
                     no update approves anything for them either.

Where Codex is and where it keeps its files come from the login shell
(`loginenv`, as the update cycle reads them): an nvm, volta or Homebrew codex
and a `CODEX_HOME` set in a profile are not in the service's own clean
environment. Only PATH and CODEX_HOME are kept (LOGIN_NAMES), never a variable
that could carry a password.

Codex reads approvals when a session starts, so a session that starts before
the heal (the one whose start rewrote the copies, and any in the minute
after) stays unrecorded; the ones after it run Probe's hooks. `probe doctor
--fix` makes the same approval on demand, and an update still makes it.

Its own timer, as `statepost`'s: one stat walk a minute while the service runs
(and it runs only while something uses it). The approval needs `probe.cli` and
Codex's app-server, so it runs in the child, never here: a plain child
(`children.run_once`), never killed, since it writes.

Stdlib only (the start path; plan S1).
"""

from __future__ import annotations

import asyncio
import contextlib
import hashlib
import json
import os
import time
from collections.abc import Awaitable, Callable, Mapping
from pathlib import Path

from . import children, loginenv, paths

#: `probe.cli.codex_hooks.PROBE_PLUGINS` and `probe.cli.capabilities.MARKETPLACE`
#: (tests/test_service_codex_trust.py holds them equal): the copies whose hooks
#: `approve` may approve.
PLUGINS = ("probe-research", "probe-research-daemon", "probe-research-tap")
MARKETPLACE = "research-os-agent"

#: How often the copies are looked at; the first look comes FIRST_S after the
#: start, inside the discovery window, when no update cycle runs yet.
TICK_S = 60.0
FIRST_S = 5.0
#: After an ask Codex refused or did not answer, the wait before the next, by
#: how many in a row did not settle; the last one repeats.
BACKOFF_S = (60.0, 120.0, 300.0, 600.0, 900.0)
#: Children in any hour, at most: a Codex that rewrote its copies at every ask
#: would otherwise be asked every tick.
MAX_ASKS_PER_HOUR = 8
#: One child is waited for this long: `approve` makes three app-server calls of
#: up to 8 s each (`codex_hooks.TIMEOUT_S`), after the interpreter's own start.
#: One still running then goes on by itself; its answer is not read.
TIMEOUT_S = 60.0
#: The most of its answer read.
MAX_ANSWER = 64 * 1024
#: The login shell is read again after this long.
LOGIN_TTL_S = 1800.0
#: What is kept of the login shell's environment, and handed to the child.
LOGIN_NAMES = ("PATH", "CODEX_HOME")
#: Files one fingerprint reads at most (a real copy holds a few hundred).
MAX_FILES = 20_000
#: Written into the copies by Probe's own hooks (`dispatch.sh`, `python -m tap`).
BYTECODE_DIR = "__pycache__"
BYTECODE_SUFFIXES = (".pyc", ".pyo")
#: The fingerprint this machine last settled, in the service's own folder.
RECORD_NAME = "codex-trust.json"
_RECORD_VERSION = 1
#: The `probe.core.run` read the child runs.
READ = "codex_trust"


class Trust:
    """`codex_trust`'s `outcome`: what the child found (`probe.cli.codex_hooks.heal`)."""

    #: Codex trusts every hook `approve` may approve (`approved`: those it
    #: approved just now; none when none waited).
    SETTLED = "settled"
    #: Some still waits: Codex refused the write, did not confirm it, or a hook
    #: stayed untrusted (`error` says which).
    WAITING = "waiting"
    #: Codex is installed but did not answer.
    UNASKED = "unasked"
    #: No codex on this PATH: nothing to ask.
    NO_CODEX = "no_codex"


OUTCOMES = frozenset({Trust.SETTLED, Trust.WAITING, Trust.UNASKED, Trust.NO_CODEX})


class Healing:
    """`service.status`'s `codex_trust.state`."""

    #: No copy of Probe's plugins in Codex's cache: nothing to keep.
    NONE = "none"
    #: Not looked yet.
    STARTING = "starting"
    #: The copies as they are now were settled.
    SETTLED = "settled"
    #: A child is asking Codex.
    ASKING = "asking"
    #: Codex is to be asked again: at `retry_at` after an ask it refused or did
    #: not answer, else at the next tick (something held it off, or the copies moved).
    WAITING = "waiting"
    #: No codex on the login PATH.
    NO_CODEX = "no_codex"
    #: Automatic updates are off: the person approves (`probe doctor --fix`).
    OFF = "off"


def codex_home(env: Mapping | None = None) -> Path:
    """`CODEX_HOME` (from `env`, else this process's), else `~/.codex`: Codex's
    own rule, as `probe.cli.codex_config` reads it in the child."""
    configured = (env if env is not None else os.environ).get("CODEX_HOME")
    return Path(configured).expanduser() if configured else paths.home() / ".codex"


def fingerprint(home: Path | None = None) -> str | None:
    """One digest of every file of Probe's plugin copies in Codex's cache: its
    path, size and mtime, bytecode left out. None when there is no copy. A
    version folder named with a dot (Codex's own staging) is no copy
    (`codex_hooks.installed_copies`). Never follows a link out; never raises."""
    cache = (home or codex_home()) / "plugins" / "cache" / MARKETPLACE
    digest = hashlib.sha256(str(cache).encode("utf-8", "surrogateescape"))
    count = 0
    for plugin in PLUGINS:
        try:
            versions = sorted(e.name for e in os.scandir(cache / plugin) if e.is_dir(follow_symlinks=False)
                              and not e.name.startswith("."))
        except OSError:
            continue
        for version in versions:
            digest.update(f"{plugin}/{version}\n".encode())
            for root, dirs, files in os.walk(cache / plugin / version):
                dirs[:] = sorted(d for d in dirs if d != BYTECODE_DIR)
                for name in sorted(files):
                    if name.endswith(BYTECODE_SUFFIXES):
                        continue
                    path = os.path.join(root, name)
                    try:
                        st = os.lstat(path)
                    except OSError:
                        continue
                    count += 1
                    if count > MAX_FILES:
                        return digest.hexdigest()
                    rel = os.path.relpath(path, cache)
                    digest.update(f"{rel}\0{st.st_size}\0{st.st_mtime_ns}\n".encode("utf-8", "surrogateescape"))
            count += 1  # an empty copy is still one
    return digest.hexdigest() if count else None


async def login_env() -> dict:
    """PATH and CODEX_HOME as the login shell has them (LOGIN_NAMES only)."""
    env = await loginenv.child_env(vars=True)
    return {name: env[name] for name in LOGIN_NAMES if env.get(name)}


async def ask(env: dict) -> dict | None:
    """The child's answer (`codex_hooks.heal`), run with `env` over the
    service's own, or None when it gave none: it could not start, was still
    running after TIMEOUT_S, or wrote no answer."""
    try:
        _code, out, _more = await children.run_once(
            READ, b"{}", env_extra=env, timeout=TIMEOUT_S, kill=False, max_output=MAX_ANSWER
        )
        answer = json.loads(out.decode("utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        return None
    return answer if isinstance(answer, dict) and answer.get("outcome") in OUTCOMES else None


class CodexTrust:
    """The healer: `start` its timer, `public` for `service.status`, `close` at the stop."""

    def __init__(
        self,
        *,
        log: Callable[[str], None],
        held: Callable[[], bool] = lambda: False,
        changed: Callable[[], None] = lambda: None,
        enabled: Callable[[], bool] = lambda: True,
        login: Callable[[], Awaitable[dict]] = login_env,
        fingerprint: Callable[[Path], str | None] = fingerprint,
        ask: Callable[[dict], Awaitable[dict | None]] = ask,
        clock: Callable[[], float] = time.time,
        record: Path | None = None,
        tick_s: float = TICK_S,
        first_s: float = FIRST_S,
    ) -> None:
        self.log = log
        #: True while something else writes Codex's config: no child starts.
        self.held = held
        #: Called when an ask starts and ends: it holds the service meanwhile.
        self._changed = changed
        #: Automatic updates are on (the updater's own reading).
        self.enabled = enabled
        self._login = login
        self._fingerprint = fingerprint
        self._ask = ask
        self.clock = clock
        self.record = record if record is not None else paths.service_dir() / RECORD_NAME
        self.tick_s = tick_s
        self.first_s = first_s
        self._task: asyncio.Task | None = None
        self._closed = False
        self.state = Healing.STARTING
        #: The login shell's PATH and CODEX_HOME, and when they were read (monotonic).
        self._env: dict | None = None
        self._env_at = 0.0
        #: The fingerprint whose hooks Codex was found to trust (from disk at the start).
        self.settled: str | None = self._load()
        #: The fingerprint the last unsettled ask was about, how many in a row
        #: did not settle, and when it may be asked again (epoch seconds).
        self.unsettled: str | None = None
        self.failures = 0
        self.retry_at: float | None = None
        #: The fingerprint a child found no codex for (never written to disk;
        #: forgotten when the login shell is read again).
        self.no_codex: str | None = None
        #: When each child of the last hour started.
        self._asked: list[float] = []
        #: Children so far, hooks they approved, and the last one's answer.
        self.asks = 0
        self.approved = 0
        self.last: dict | None = None

    # -- the record --------------------------------------------------------

    def _load(self) -> str | None:
        try:
            data = json.loads(self.record.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        if not isinstance(data, dict) or data.get("v") != _RECORD_VERSION:
            return None
        value = data.get("fingerprint")
        return value if isinstance(value, str) and value else None

    def _save(self, value: str) -> None:
        tmp = self.record.with_name(f"{self.record.name}.{os.getpid()}.tmp")
        try:
            with open(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w", encoding="utf-8") as handle:
                json.dump({"v": _RECORD_VERSION, "fingerprint": value, "settled_at": self.clock()}, handle)
            paths.replace(tmp, self.record)
        except OSError:
            pass  # kept in memory: the next service asks once more
        finally:
            with contextlib.suppress(OSError):
                os.unlink(tmp)

    # -- the timer ---------------------------------------------------------

    def start(self) -> None:
        if self._task is None and not self._closed:
            self._task = asyncio.get_running_loop().create_task(self._run())

    async def _run(self) -> None:
        await asyncio.sleep(self.first_s)
        while not self._closed:
            try:
                await self.look()
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # noqa: BLE001 -- the next tick looks again
                self.log(f"codex trust: the look failed: {type(exc).__name__}: {exc}")
            await asyncio.sleep(self.tick_s)

    def asking(self) -> bool:
        """A child is asking Codex now (it keeps the service up: `Service.holds`)."""
        return self.state == Healing.ASKING

    def close(self) -> None:
        """The service stops. A child still asking goes on by itself (`run_once`
        never kills it); what it found is not recorded, so the next service
        asks once more."""
        self._closed = True
        if self._task is not None:
            self._task.cancel()
            self._task = None

    # -- one look ----------------------------------------------------------

    async def _login_now(self) -> dict:
        """The login shell's PATH and CODEX_HOME, read again after LOGIN_TTL_S.
        A new reading may find a codex the last one did not."""
        now = time.monotonic()
        if self._env is None or now - self._env_at >= LOGIN_TTL_S:
            try:
                self._env = await self._login()
            except Exception:  # noqa: BLE001 -- loginenv never raises; the service's own then
                self._env = {}
            self._env_at = now
            self.no_codex = None
        return dict(self._env)

    async def _fingerprint_now(self, home: Path) -> str | None:
        return await asyncio.get_running_loop().run_in_executor(None, self._fingerprint, home)

    def _room(self, now: float) -> bool:
        self._asked = [at for at in self._asked if 0 <= now - at < 3600.0]
        return len(self._asked) < MAX_ASKS_PER_HOUR

    async def look(self) -> None:
        """One tick: ask Codex when Probe's copies are not the ones last settled
        and nothing holds it off (automatic updates off, a backoff, the hour's
        limit, an update or a setup)."""
        if not self.enabled():
            self.state = Healing.OFF
            return
        now = self.clock()
        env = await self._login_now()
        home = codex_home(env)
        current = await self._fingerprint_now(home)
        if current is None:
            self.state = Healing.NONE
            return
        if current == self.settled:
            self.state = Healing.SETTLED
            return
        if current == self.no_codex:
            self.state = Healing.NO_CODEX
            return
        if current == self.unsettled and self.retry_at is not None and now < self.retry_at:
            self.state = Healing.WAITING
            return
        if current != self.unsettled:
            self.failures = 0
        if self.held() or not self._room(now):
            self.state = Healing.WAITING
            return
        self._asked.append(now)
        self.asks += 1
        self.state = Healing.ASKING
        self._changed()
        try:
            answer = await self._ask(env)
            after = await self._fingerprint_now(home)
            self._settle(current, after, answer)
        finally:
            if self.state == Healing.ASKING:
                self.state = Healing.WAITING  # cancelled, or the look failed: the next tick asks
            self._changed()

    def _settle(self, before: str, after: str | None, answer: dict | None) -> None:
        now = self.clock()
        outcome = answer.get("outcome") if answer is not None else None
        approved = answer.get("approved") if answer is not None else None
        approved = [key for key in approved if isinstance(key, str)] if isinstance(approved, list) else []
        error = answer.get("error") if answer is not None and isinstance(answer.get("error"), str) else None
        self.approved += len(approved)
        self.last = {"at": now, "outcome": outcome, "approved": len(approved), "error": error and error[:200]}
        if approved:
            self.log(f"codex trust: approved {len(approved)} of Probe's hooks in Codex (its copies changed)")
        if outcome == Trust.NO_CODEX:
            self.no_codex, self.unsettled, self.retry_at = before, None, None
            self.state = Healing.NO_CODEX
            self.log("codex trust: Probe's plugins are in Codex's cache, but no codex is on the login PATH")
            return
        if after != before:
            # Codex rewrote the copies while it was asked: the new ones are a new
            # change, asked about at the next tick.
            self.unsettled = after if after is not None else before
            self.failures, self.retry_at = 0, None
            self.state = Healing.WAITING
            return
        if outcome == Trust.SETTLED:
            self.settled, self.unsettled, self.retry_at, self.failures = before, None, None, 0
            self.state = Healing.SETTLED
            self._save(before)
            return
        # Codex refused or did not answer.
        self.unsettled = before
        self.failures += 1
        self.retry_at = now + BACKOFF_S[min(self.failures, len(BACKOFF_S)) - 1]
        self.state = Healing.WAITING
        why = error or ("Codex did not answer" if outcome == Trust.UNASKED else "no answer")
        self.log(f"codex trust: not settled ({why}); asking again in {int(self.retry_at - now)}s")

    def public(self) -> dict:
        return {
            "state": self.state,
            "asks": self.asks,
            "approved": self.approved,
            "retry_at": self.retry_at,
            "last": dict(self.last) if self.last else None,
        }
