"""The portal steps through Chromium on pi5-2 (``--browser pi``), driven from this machine.

Only Chromium runs on the Pi. The vault command, the agent and the secrets stay here.
A changed login is kept in one tar per vault account (:func:`login_slug`), and only a start for that
account unpacks it. A start with no account gets a fresh profile and saves nothing.
Code does every step that touches a secret over CDP, and holds the adapter's secret lock meanwhile.
The agent has only the ``computer`` MCP server (no shell, no file or web tool), so it cannot reach CDP.
The agent's goal ends before a secret shows, so its run is over before code reads one.
A redirect leg (a 3xx) never reaches a Playwright route: the route answers with a page that navigates
again, and a ``request`` listener forwards a server-side redirect. docs/exploration/vault-app.md has the parts.
"""

from __future__ import annotations

import asyncio
import concurrent.futures
import json
import logging
import os
import queue
import re
import shutil
import signal
import socket
import subprocess
import tempfile
import threading
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager, suppress
from enum import StrEnum
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol, TypeVar
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel, ConfigDict, SecretStr

from plato.chronos.login_vault import normalize_key
from plato.cli.vault import pi_desktop_adapter
from plato.cli.vault.app_models import ConsentBrowser, PortalSecretFile, VaultLine, VendorRecipe
from plato.cli.vault.app_portal import (
    AGENT_TIMEOUT_S,
    CONSENT_BUTTON_WAIT_MS,
    CONSENT_CLICKS,
    CONSENT_MATCH_JS,
    CONSENT_REDIRECT_WAIT_MS,
    GENERATE_COUNT_JS,
    SECRET_READY_JS,
    SECRET_VALUES_JS,
    NeedPerson,
    PortalError,
    PortalTools,
    PortalUnavailable,
    _text,
    agent_env,
    log_hint,
    parse_lines,
    redact,
    write_agent_log,
)
from plato.cli.vault.totp_models import BackupCodesFile, CodeResult, KeyCandidates, TotpKey, TotpRecipe
from plato.cli.vault.totp_portal import (
    BACKUP_FIND_JS,
    BACKUP_WAIT_MS,
    BY_NAME_JS,
    CODE_STATE_JS,
    CONFIRM_SETTLE_MS,
    CONFIRM_WAIT_MS,
    FIND_KEY_JS,
    IDENTITY_SETTLE_MS,
    IDENTITY_WAIT_MS,
    KEY_WAIT_MS,
    OTPAUTH_IN_PAGE_JS,
    SIGNED_IN_EMAILS_JS,
    TYPE_CODE_JS,
    EmailReadFailed,
    pick_key,
)

if TYPE_CHECKING:
    from plato.cli.vault.pi_desktop_adapter import VncClient

T = TypeVar("T")

# FIND_KEY_JS, but only whether it found a key: the seed itself stays in the page.
# The screen gate's seed check (a bool only: the seed stays in the page). key_pattern alone also
# matches ordinary words such as "Continue with email", so the gate
# counts a text as a seed only when it looks like one: a base32 digit (2-7) in it, even groups of
# four ("abcd efgh ijkl mnop ..."), or one unbroken run of 16+ base32 letters (an all-letter
# seed such as ABCDEFGHIJKLMNOP is valid). Words with uneven gaps between them are no seed.
KEY_SHOWS_JS = (
    "(cfg) => { const got = (" + FIND_KEY_JS + ")(cfg);"
    " const seedLike = (k) => { const t = String(k).trim(); return /[2-7]/.test(t)"
    " || /^[A-Za-z2-7]{4}(?:[ -][A-Za-z2-7]{4}){3,}$/.test(t) || /^[A-Za-z2-7]{16,}=*$/.test(t); };"
    " return got.uris.length + got.keys.filter(seedLike).length > 0; }"
)

LAUNCHER_TAG = "@@PIMINT "
# The launcher's exit codes (assets/pi-mint-browser.sh).
LAUNCHER_BUSY = 3  # a pi-mint Chromium of another command runs
LAUNCHER_NO_CDP = 4  # Chromium did not open its CDP port in time
SSH_FAILED = 255  # ssh itself failed (connect, auth): the remote command did not run
GOTO_TIMEOUT_MS = 60_000
CLICK_TIMEOUT_MS = 5_000
SECRET_WAIT_MS = 30_000
CALLBACK_FORWARD_TIMEOUT_S = 15.0
# The wall clock for one Playwright call (limited()). page.evaluate has no time limit of its own,
# and a call with a Playwright timeout gets that timeout plus PAGE_CALL_MARGIN_S.
PAGE_CALL_TIMEOUT_S = 30.0
PAGE_CALL_MARGIN_S = 15.0
PUMP_MS = 250  # how often the main thread lets Playwright handle events during an agent run
TUNNEL_STOP_S = 5.0
PIPE_DRAIN_S = 5.0  # after the agent exits, how long its pipes may stay open (a child that escaped)
_APP_ID = re.compile(r"/apps/([A-Za-z0-9_-]{6,})")
_TOKEN = re.compile(r"[^A-Za-z0-9_.-]")
_LOGIN = re.compile(r"[^a-z0-9._-]")
LOGIN_MAX = 120  # the launcher refuses a longer slug

# The `computer` tools the agent may use: every one except bash.
PI_AGENT_TOOLS = (
    "screenshot",
    "click",
    "type_text",
    "key",
    "scroll",
    "drag",
    "mouse_move",
    "cursor_position",
    "wait",
)
PI_DISALLOWED_TOOLS = ("mcp__computer__bash",)

PI_COMPUTER_INSTRUCTIONS = """## Remote desktop (`computer` MCP server)

The `computer` MCP tools control the screen of a remote desktop (a Raspberry Pi)
that shows one Chromium window. You have no shell and no file tools, and the
`bash` tool is off. Only `screenshot` returns an image; every other action answers
with a short text acknowledgement. You may issue several actions in one turn -
they run in order - and should end each group with `screenshot` to verify the
result before continuing. Coordinates are real pixels in the most recent
screenshot."""


class LauncherMode(StrEnum):
    """The launcher's modes (the first argument it gets)."""

    start = "--start"
    stop = "--stop"
    save_login = "--save-login"
    mark_handoff = "--mark-handoff"
    clear_handoff = "--clear-handoff"
    status = "--status"


class LauncherBusy(PortalError):
    """Another command's Chromium runs on the Pi (launcher exit 3)."""


class PiPageLost(PortalError):
    """The Pi page closed (or navigated away) during a read: no answer, not an empty one.
    A default here read as "the person finished" and as "the page shows no prompt"."""


class PiPageNavigated(PiPageLost):
    """A navigation replaced the page's context during a call that must not run again."""


class PiPageTimeout(PiPageLost):
    """A Playwright call on the Pi page gave no reply within its time limit (:func:`limited`)."""


class _NoAnswer(Exception):
    """The time limit of one call in :func:`limited` ran out."""


def limited(owner: Any, limit_s: float, what: str, call: Callable[[], T]) -> T:
    """Run ``call()``, one playwright.sync_api call on ``owner``, with a wall clock of ``limit_s``.

    The sync API runs each call as a task on its event loop through ``owner._sync``, and
    page.evaluate waits with no limit for the page's main-world context. After the code
    sign-in in PR #2487 run c, a read got no reply, and the command waited 17 min with no
    output. Here ``_sync`` runs that task under asyncio.wait_for: no reply in time raises
    :class:`PiPageTimeout`. An owner with no ``_sync`` (a test fake) runs the call as it is."""
    base = getattr(owner, "_sync", None)
    if base is None:
        return call()

    async def bounded(coro: Any) -> Any:
        try:
            return await asyncio.wait_for(coro, limit_s)
        except TimeoutError:
            raise _NoAnswer from None

    own = vars(owner)
    had, prev = "_sync" in own, own.get("_sync")
    owner._sync = lambda coro: base(bounded(coro))
    try:
        return call()
    except _NoAnswer:
        raise PiPageTimeout(
            f"the Pi page gave no answer to {what} in {limit_s:g} s: Playwright got no reply from the Chromium on "
            "the Pi, so code stopped here and did not wait on. Run the command again"
        ) from None
    finally:
        if had:
            owner._sync = prev
        else:
            del owner._sync


class PageLoss(StrEnum):
    """Why a Playwright call on the Pi page failed when it was not the script's own error."""

    closed = "closed"
    navigated = "navigated"


# Playwright raises one Error type for all of these, so the message tells them apart.
_PAGE_CLOSED_MARKERS = (
    "has been closed",
    "target closed",
    "page closed",
    "browser closed",
    "connection closed",
    "has been disconnected",
)
_PAGE_NAVIGATED_MARKERS = (
    "execution context was destroyed",
    "cannot find context with specified id",
    "frame was detached",
    "frame got detached",
)
NAVIGATION_RETRY_MS = 500  # one more try after a navigation replaced the page's context


def page_loss(error: BaseException) -> PageLoss | None:
    """The page is gone or navigated (not a JS error in the script): which one, else None."""
    if type(error).__name__ == "TargetClosedError":
        return PageLoss.closed
    text = str(error).lower()
    if any(m in text for m in _PAGE_CLOSED_MARKERS):
        return PageLoss.closed
    if any(m in text for m in _PAGE_NAVIGATED_MARKERS):
        return PageLoss.navigated
    return None


class PiUnreachable(PortalError):
    """ssh to the Pi failed every time: the launcher did not run."""


class PiBrowserConfig(BaseModel):
    """Where the Pi browser is and how to reach it. Env overrides: ``PLATO_VAULT_PI_HOST``,
    ``PLATO_VAULT_PI_USER``, ``PLATO_VAULT_PI_LAUNCHER``, ``PLATO_VAULT_PI_NOVNC_URL``."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    host: str = "100.122.241.99"  # pi5-2 on the tailnet
    user: str = "plato"
    # Run by the remote shell, so a leading ~ expands there.
    launcher: str = "~/.local/bin/pi-mint-browser"
    cdp_port: int = 9222
    vnc_socket: str = "/run/user/1000/wayvnc-novnc.sock"
    novnc_url: str = "https://pi5-2.local:6080/vnc.html"
    ssh_connect_timeout_s: int = 15
    # The first ssh connection to the Pi can time out and the next one works.
    ssh_attempts: int = 3
    ssh_retry_s: float = 2.0
    tunnel_ready_s: float = 20.0
    launcher_timeout_s: float = 90.0
    screen_max_width: int = pi_desktop_adapter.DEFAULT_MAX_WIDTH

    @property
    def target(self) -> str:
        return f"{self.user}@{self.host}"

    @classmethod
    def from_env(cls, environ: dict[str, str] | None = None) -> PiBrowserConfig:
        env = os.environ if environ is None else environ
        names = {
            "host": "PLATO_VAULT_PI_HOST",
            "user": "PLATO_VAULT_PI_USER",
            "launcher": "PLATO_VAULT_PI_LAUNCHER",
            "novnc_url": "PLATO_VAULT_PI_NOVNC_URL",
        }
        return cls.model_validate({field: env[name] for field, name in names.items() if env.get(name)})


class LauncherReply(BaseModel):
    """The launcher's ``@@PIMINT {json}`` line."""

    model_config = ConfigDict(extra="ignore")

    pid: int | None = None
    restored_login: bool | None = None
    cdp_port: int | None = None
    stopped: bool | None = None
    saved: bool | None = None
    running: bool | None = None
    handed_off: bool | None = None
    # --start: the account slug whose login the run restores and saves (None: a fresh profile).
    login: str | None = None
    error: str | None = None
    # A busy reply: the token of the run that holds the browser (a stop needs it).
    token: str | None = None


class AgentRun(BaseModel):
    """One ``claude -p`` run: its exit and its output (logged redacted, never printed)."""

    model_config = ConfigDict(extra="forbid")

    returncode: int | None
    stdout: str
    stderr: str
    timed_out: bool = False


class AgentServer(Protocol):
    """A second MCP server for the agent (the mint's ``vault`` tools), started next to `computer`."""

    name: str

    @property
    def url(self) -> str: ...

    async def start(self) -> None: ...

    async def close(self) -> None: ...


class AgentExtras(BaseModel):
    """What a goal adds to the screen-only agent: built-in tools (``WebSearch``), the
    tools of a second MCP server, a model and a system-prompt block."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    server: Callable[[], AgentServer] | None = None
    server_tools: tuple[str, ...] = ()
    builtin_tools: tuple[str, ...] = ()
    model: str | None = None
    instructions: str = ""


def pi_mcp_config(mcp_url: str, servers: dict[str, str] | None = None) -> str:
    entries = {"computer": {"type": "http", "url": mcp_url}}
    entries.update({name: {"type": "http", "url": url} for name, url in (servers or {}).items()})
    return json.dumps({"mcpServers": entries})


def pi_agent_command(
    agent: str,
    goal: str,
    mcp_url: str,
    extras: AgentExtras | None = None,
    server_url: str | None = None,
    server_name: str | None = None,
) -> list[str]:
    """``claude -p`` with no built-in tool (``--tools ""``), one MCP server (the
    `computer` server, ``--strict-mcp-config``), its tools minus ``bash`` allowed,
    ``bash`` disallowed, and ``dontAsk`` so any other tool is refused. No session
    file (``--no-session-persistence``): a frame must not stay on disk. ``extras``
    adds its built-in tools, the second server's tools and a model."""
    extras = extras or AgentExtras()
    allowed = [f"mcp__computer__{t}" for t in PI_AGENT_TOOLS]
    servers: dict[str, str] = {}
    if server_url is not None and server_name is not None:
        servers[server_name] = server_url
        allowed += [f"mcp__{server_name}__{t}" for t in extras.server_tools]
    allowed += list(extras.builtin_tools)
    command = [
        agent,
        "-p",
        goal,
        "--no-session-persistence",
        "--tools",
        ",".join(extras.builtin_tools),
        "--allowedTools",
        ",".join(allowed),
        "--disallowedTools",
        ",".join(PI_DISALLOWED_TOOLS),
        "--permission-mode",
        "dontAsk",
        "--strict-mcp-config",
        "--mcp-config",
        pi_mcp_config(mcp_url, servers),
        "--append-system-prompt",
        "\n\n".join(p for p in (PI_COMPUTER_INSTRUCTIONS, extras.instructions) if p),
    ]
    if extras.model:
        command += ["--model", extras.model]
    return command


async def _drain(stream: asyncio.StreamReader | None, sink: list[bytes]) -> None:
    if stream is None:
        return
    while chunk := await stream.read(65536):
        sink.append(chunk)


class _LiveAgents:
    """The process groups of the agents that run now. The agent runs in its own
    session, so a Ctrl-C on the terminal does not reach it: :func:`_in_thread` kills
    these groups when the main thread stops."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._pgids: set[int] = set()

    def add(self, pgid: int) -> None:
        with self._lock:
            self._pgids.add(pgid)

    def discard(self, pgid: int) -> None:
        with self._lock:
            self._pgids.discard(pgid)

    def kill_all(self) -> None:
        with self._lock:
            pgids, self._pgids = self._pgids, set()
        for pgid in pgids:
            with suppress(ProcessLookupError, PermissionError):
                os.killpg(pgid, signal.SIGKILL)


LIVE_AGENTS = _LiveAgents()


def _kill_group(proc: asyncio.subprocess.Process) -> None:
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass
    except OSError:
        with suppress(ProcessLookupError):
            proc.kill()


def run_pi_agent(
    agent: str, goal: str, desktop_url: str, workdir: str, timeout_s: float, extras: AgentExtras | None = None
) -> AgentRun:
    """Start the `computer` MCP server on the adapter at ``desktop_url`` (and the
    ``extras`` server), run the agent against them, then stop the servers. Call it off
    the Playwright thread: it runs its own event loop (:meth:`PiDriver.agent` runs it in
    a worker thread)."""

    async def main() -> AgentRun:
        import fastmcp

        from plato.agents.computer_use_mcp import ComputerUseMcp

        # No FastMCP banner, no request log and no shutdown traceback (the server task is
        # cancelled on close) in the vault command's output.
        fastmcp.settings.show_server_banner = False
        fastmcp.settings.log_level = "WARNING"
        _quiet_server_logs()
        mcp = ComputerUseMcp(desktop_url, port=free_local_port(), screenshots="on_request")
        await mcp.start()
        server = extras.server() if extras is not None and extras.server is not None else None
        try:
            if server is not None:
                await server.start()
            proc = await asyncio.create_subprocess_exec(
                *pi_agent_command(
                    agent,
                    goal,
                    mcp.url,
                    extras,
                    server.url if server is not None else None,
                    server.name if server is not None else None,
                ),
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=workdir,
                env=agent_env(),
                start_new_session=True,  # a timeout kills claude-seat and claude together
            )
            LIVE_AGENTS.add(proc.pid)  # new session: the pgid is the pid
            out: list[bytes] = []
            err: list[bytes] = []
            # Read both pipes into lists, so a timeout keeps what the agent printed so far.
            readers = asyncio.gather(_drain(proc.stdout, out), _drain(proc.stderr, err))
            timed_out = False
            try:
                await asyncio.wait_for(proc.wait(), timeout_s)
            except TimeoutError:
                timed_out = True
                _kill_group(proc)
                await proc.wait()
            LIVE_AGENTS.discard(proc.pid)
            with suppress(TimeoutError):
                await asyncio.wait_for(readers, PIPE_DRAIN_S)
            return AgentRun(
                returncode=None if timed_out else proc.returncode,
                stdout=b"".join(out).decode(errors="replace"),
                stderr=b"".join(err).decode(errors="replace"),
                timed_out=timed_out,
            )
        finally:
            _quiet_server_logs()  # uvicorn set its own levels at start
            if server is not None:
                with suppress(Exception):
                    await server.close()
            await mcp.close()

    return asyncio.run(main())


def _quiet_server_logs() -> None:
    for name in ("fastmcp", "uvicorn", "uvicorn.error", "uvicorn.access"):
        logging.getLogger(name).setLevel(logging.CRITICAL)


def _in_thread(
    fn: Callable[[], T],
    pump: Callable[[], None] | None = None,
    on_abort: Callable[[], None] | None = None,
) -> T:
    """Run ``fn`` in a new thread and wait for it; ``pump`` runs on this thread meanwhile
    (it does the waiting). If this thread stops (Ctrl-C), ``on_abort`` runs first."""
    box: dict[str, Any] = {}

    def target() -> None:
        try:
            box["value"] = fn()
        except BaseException as e:
            box["error"] = e

    thread = threading.Thread(target=target, name="pi-agent", daemon=True)
    thread.start()
    try:
        while thread.is_alive():
            if pump is not None:
                pump()
            thread.join(timeout=0 if pump is not None else PUMP_MS / 1000)
    except BaseException:
        if on_abort is not None:
            on_abort()
        raise
    if "error" in box:
        raise box["error"]
    return box["value"]


class PageJobs:
    """Calls from another thread (an agent's MCP tool) that must run on the page thread:
    Playwright's sync API belongs to one thread. :meth:`serve` runs in the page thread's
    wait loop (:meth:`PiDriver.agent`)."""

    def __init__(self) -> None:
        self._queue: queue.Queue[tuple[Callable[[], Any], concurrent.futures.Future[Any]]] = queue.Queue()

    def call(self, fn: Callable[[], T], timeout_s: float) -> T:
        future: concurrent.futures.Future[T] = concurrent.futures.Future()
        self._queue.put((fn, future))
        try:
            return future.result(timeout_s)
        except concurrent.futures.TimeoutError:
            future.cancel()
            raise PortalError(f"the page step did not run within {timeout_s:.0f} s") from None

    def serve(self) -> None:
        while True:
            try:
                fn, future = self._queue.get_nowait()
            except queue.Empty:
                return
            if not future.set_running_or_notify_cancel():
                continue
            try:
                future.set_result(fn())
            except BaseException as e:
                future.set_exception(e)


def free_local_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def port_open(port: int, timeout_s: float = 0.5) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=timeout_s):
            return True
    except OSError:
        return False


def ssh_base(config: PiBrowserConfig) -> list[str]:
    return [
        "ssh",
        "-o",
        "BatchMode=yes",
        "-o",
        f"ConnectTimeout={config.ssh_connect_timeout_s}",
        "-o",
        "ServerAliveInterval=15",
        "-o",
        "ServerAliveCountMax=3",
        "-o",
        "ExitOnForwardFailure=yes",
        "-o",
        "LogLevel=ERROR",
    ]


class SshTunnel:
    """``ssh -N -L 127.0.0.1:<free port>:<remote>`` to the Pi. ``remote`` is
    ``host:port`` or a unix socket path. :meth:`start` retries a failed connect;
    :meth:`stop` is idempotent. Use it as a context manager, so it always stops."""

    def __init__(
        self,
        config: PiBrowserConfig,
        remote: str,
        *,
        popen: Callable[..., Any] = subprocess.Popen,
        ready: Callable[[int], bool] = port_open,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.config = config
        self.remote = remote
        self._popen = popen
        self._ready = ready
        self._sleep = sleep
        self._clock = clock
        self.proc: Any = None
        self.port: int | None = None

    def command(self, port: int) -> list[str]:
        return [*ssh_base(self.config), "-N", "-L", f"127.0.0.1:{port}:{self.remote}", self.config.target]

    def start(self) -> int:
        why = "no attempt"
        for attempt in range(self.config.ssh_attempts):
            if attempt:
                self._sleep(self.config.ssh_retry_s)
            port = free_local_port()
            self.proc = self._popen(
                self.command(port), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
            )
            deadline = self._clock() + self.config.tunnel_ready_s
            while True:
                code = self.proc.poll()
                if code is not None:
                    err = _text(self.proc.stderr.read() if self.proc.stderr else b"")
                    why = f"ssh exit {code}: {redact(err.strip()[-200:]) or 'no message'}"
                    break
                if self._ready(port):
                    self.port = port
                    return port
                if self._clock() >= deadline:
                    why = f"the tunnel did not open in {self.config.tunnel_ready_s:.0f} s"
                    break
                self._sleep(0.2)
            self.stop()
        raise PortalError(
            f"the ssh tunnel to {self.config.target} ({self.remote}) failed after "
            f"{self.config.ssh_attempts} attempt(s): {why}"
        )

    def stop(self) -> None:
        proc, self.proc, self.port = self.proc, None, None
        if proc is None:
            return
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=TUNNEL_STOP_S)
            except subprocess.TimeoutExpired:
                proc.kill()
                with suppress(subprocess.TimeoutExpired):
                    proc.wait(timeout=TUNNEL_STOP_S)
        if proc.stderr is not None:
            with suppress(Exception):
                proc.stderr.close()

    def __enter__(self) -> SshTunnel:
        self.start()
        return self

    def __exit__(self, *exc: object) -> None:
        self.stop()


class PiLauncher:
    """The launcher script on the Pi, run over ssh. Each mode prints one ``@@PIMINT`` line."""

    def __init__(
        self,
        config: PiBrowserConfig,
        *,
        runner: Callable[..., Any] = subprocess.run,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.config = config
        self._runner = runner
        self._sleep = sleep

    def command(self, mode: LauncherMode, *args: str) -> list[str]:
        remote = " ".join([self.config.launcher, mode.value, *(_quote(a) for a in args)])
        return [*ssh_base(self.config), self.config.target, remote]

    def run(self, mode: LauncherMode, *args: str) -> LauncherReply:
        proc: Any = None
        for attempt in range(self.config.ssh_attempts):
            if attempt:
                self._sleep(self.config.ssh_retry_s)
            try:
                proc = self._runner(
                    self.command(mode, *args),
                    text=True,
                    capture_output=True,
                    timeout=self.config.launcher_timeout_s,
                    stdin=subprocess.DEVNULL,
                )
            except subprocess.TimeoutExpired:
                raise PortalError(
                    f"the Pi launcher ({mode.value}) ran over {self.config.launcher_timeout_s:.0f} s"
                ) from None
            if proc.returncode != SSH_FAILED:
                break
        assert proc is not None
        reply = _launcher_reply(proc.stdout or "")
        if proc.returncode == 0 and reply is not None:
            return reply
        detail = (reply.error if reply and reply.error else None) or redact((proc.stderr or "").strip()[-300:])
        if proc.returncode == LAUNCHER_BUSY:
            # The launcher refuses a stop with no token while a run holds one.
            token = f" --token {_quote(reply.token)}" if reply and reply.token else ""
            raise LauncherBusy(
                f"the Pi browser is in use by another command ({detail}). When that command has ended, run "
                f"`ssh {self.config.target} {self.config.launcher} --stop --save-login{token}`"
            )
        if proc.returncode == SSH_FAILED:
            raise PiUnreachable(f"ssh to {self.config.target} failed {self.config.ssh_attempts} time(s): {detail}")
        raise PortalError(f"the Pi launcher ({mode.value}) failed (exit {proc.returncode}): {detail or 'no message'}")

    def start(self, token: str, login: str | None = None) -> LauncherReply:
        """Start Chromium with the saved login of ``login`` (an account slug,
        :func:`login_slug`). None: a fresh profile, and the run saves no login."""
        args = ["--token", launcher_token(token)]
        if login:
            args += ["--login", launcher_login(login)]
        reply = self.run(LauncherMode.start, *args)
        if reply.pid is None:
            raise PortalError("the Pi launcher reported no Chromium pid")
        # A run with no slug restores nothing: a restore then came from an old launcher's shared tar.
        if (reply.login or None) != (launcher_login(login) if login else None) or (not login and reply.restored_login):
            # An old launcher, or a run of another account: its cookies are not this account's.
            raise PortalError(
                f"the Pi launcher started Chromium with the login {reply.login!r}, not {login!r}: "
                "install the current assets/pi-mint-browser.sh on the Pi"
            )
        return reply

    def stop(self, save_login: bool, token: str | None = None, login: str | None = None) -> LauncherReply:
        """Stop Chromium. With ``token``: only the run that this token started. With
        ``login``: the launcher saves only when the run started with this slug."""
        args = ["--save-login"] if save_login else []
        args += _token_args(token)
        if login:
            args += ["--login", launcher_login(login)]
        return self.run(LauncherMode.stop, *args)

    def mark_handoff(self, token: str | None = None) -> LauncherReply:
        return self.run(LauncherMode.mark_handoff, *_token_args(token))

    def clear_handoff(self, token: str | None = None) -> LauncherReply:
        """With ``token``: exit 3 (:class:`LauncherBusy`) when the run is another command's."""
        return self.run(LauncherMode.clear_handoff, *_token_args(token))


def _token_args(token: str | None) -> list[str]:
    return ["--token", launcher_token(token)] if token is not None else []


def launcher_token(name: str) -> str:
    """The run's token as the launcher takes it (``[A-Za-z0-9_.-]``, 120 characters)."""
    return _TOKEN.sub("_", name)[:120]


def login_slug(login_key: str, account: str) -> str:
    """The vault account's slug for its saved login on the Pi: ``<login_key>.<account>``,
    both normalized (``canva.jim``). :func:`normalize_key` keeps ``[a-z0-9_]`` only, so
    the dot cannot come from either part and two accounts never share a slug."""
    lk, ac = normalize_key(login_key), normalize_key(account)
    if not lk or not ac:
        raise PortalError("the Pi browser needs a login_key and an account for the saved login")
    return launcher_login(f"{lk}.{ac}")


def launcher_login(slug: str) -> str:
    """A slug as the launcher takes it: ``[a-z0-9._-]``, a letter or digit first, at most
    :data:`LOGIN_MAX` characters. It names a file on the Pi, so a bad one is an error, not
    a guess."""
    clean = _LOGIN.sub("_", slug.lower())
    if not clean or not clean[0].isalnum() or len(clean) > LOGIN_MAX:
        raise PortalError(f"the login slug {slug!r} is not one the Pi launcher takes")
    return clean


def _quote(arg: str) -> str:
    import shlex

    return shlex.quote(arg)


def _launcher_reply(output: str) -> LauncherReply | None:
    reply = None
    for raw in output.splitlines():
        idx = raw.find(LAUNCHER_TAG)
        if idx >= 0:
            with suppress(ValueError):
                reply = LauncherReply.model_validate_json(raw[idx + len(LAUNCHER_TAG) :])
    return reply


def follow_tab(page: Any) -> Any:
    """``page`` while it is the only open tab; else the newest open tab that is visible, else
    the newest open one. ``page`` itself when its context cannot be read."""
    try:
        tabs = [p for p in page.context.pages if not p.is_closed()]
    except Exception:
        return page
    if not tabs or tabs == [page]:
        return page
    for tab in reversed(tabs):
        with suppress(Exception):
            if (
                limited(tab, PAGE_CALL_TIMEOUT_S, "the tab check", lambda t=tab: t.evaluate("document.visibilityState"))
                == "visible"
            ):
                return tab
    return tabs[-1]


class CdpSession:
    """A Playwright connection to the Pi's Chromium. :meth:`close` stops Playwright and
    leaves Chromium running (the launcher stops it)."""

    def __init__(self, playwright: Any, page: Any) -> None:
        self._playwright = playwright
        self.page = page

    def close(self) -> None:
        pw, self._playwright = self._playwright, None
        if pw is not None:
            pw.stop()


def connect_cdp(url: str, timeout_ms: int = GOTO_TIMEOUT_MS) -> CdpSession:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise PortalUnavailable("Playwright is not installed here: install plato-sdk-v2[pi]") from None
    pw = sync_playwright().start()
    try:
        browser = pw.chromium.connect_over_cdp(url, timeout=timeout_ms)
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.pages[0] if context.pages else context.new_page()
    except BaseException:
        pw.stop()
        raise
    return CdpSession(pw, page)


class PiScreen:
    """The adapter stack for the agent: a tunnel to the wayvnc socket, a VNC client,
    :class:`pi_desktop_adapter.PiDesktop` and its HTTP server. One for each driver."""

    def __init__(
        self,
        config: PiBrowserConfig,
        *,
        tunnel_factory: Callable[[PiBrowserConfig, str], SshTunnel] = SshTunnel,
        vnc_connect: Callable[[str, int], VncClient] = pi_desktop_adapter.connect_vncdotool,
    ) -> None:
        self.config = config
        self._tunnel_factory = tunnel_factory
        self._vnc_connect = vnc_connect
        self.tunnel: SshTunnel | None = None
        self.vnc: VncClient | None = None
        self.desktop: pi_desktop_adapter.PiDesktop | None = None
        self.server: pi_desktop_adapter.DesktopHttpServer | None = None

    def start(self) -> str:
        try:
            last: Exception | None = None
            for _ in range(2):  # a dead tunnel shows only at the RFB handshake: one new tunnel
                self.tunnel = self._tunnel_factory(self.config, self.config.vnc_socket)
                port = self.tunnel.start()
                try:
                    self.vnc = self._vnc_connect("127.0.0.1", port)
                    break
                except Exception as e:
                    last = e
                    self.tunnel.stop()
                    self.tunnel = None
            if self.vnc is None:
                raise PortalError(f"the VNC connection to the Pi screen failed: {type(last).__name__}: {last}")
            self.desktop = pi_desktop_adapter.PiDesktop(self.vnc, max_width=self.config.screen_max_width)
            self.server = pi_desktop_adapter.DesktopHttpServer(self.desktop)
            return self.server.start()
        except BaseException:
            self.close()
            raise

    @contextmanager
    def secret_lock(self) -> Iterator[None]:
        if self.desktop is None:
            yield
            return
        with self.desktop.secret_lock():
            yield

    def set_gate(self, gate: pi_desktop_adapter.ScreenGate | None) -> None:
        if self.desktop is not None:
            self.desktop.gate = gate

    def seal(self) -> None:
        if self.desktop is not None:
            self.desktop.seal()

    def close(self) -> None:
        server, self.server = self.server, None
        vnc, self.vnc = self.vnc, None
        tunnel, self.tunnel = self.tunnel, None
        self.desktop = None
        if server is not None:
            with suppress(Exception):
                server.close()
        if vnc is not None:
            with suppress(Exception):
                vnc.close()
        if tunnel is not None:
            tunnel.stop()


class PiDriver:
    """The same surface as :class:`app_portal.EgoDriver`, on the Pi's Chromium.
    ``space_id`` is the Chromium pid (the messages of the callers name it).

    ``login`` is the slug of the vault account that the command works on
    (:func:`login_slug`): the start restores that account's saved login and the stop
    saves into it. None: a fresh profile that is never saved."""

    browser = ConsentBrowser.pi

    def __init__(
        self,
        tools: PortalTools,
        config: PiBrowserConfig | None = None,
        *,
        launcher: PiLauncher | None = None,
        tunnel_factory: Callable[[PiBrowserConfig, str], SshTunnel] = SshTunnel,
        cdp_connect: Callable[[str], CdpSession] = connect_cdp,
        screen_factory: Callable[[PiBrowserConfig], PiScreen] = PiScreen,
        agent_runner: Callable[..., AgentRun] = run_pi_agent,
        callback_get: Callable[[str], httpx.Response] | None = None,
        clock: Callable[[], float] = time.monotonic,
        login: str | None = None,
    ) -> None:
        if shutil.which("ssh") is None:
            raise PortalUnavailable("no `ssh` binary here, so the Pi browser cannot be reached")
        self.tools = tools
        self.config = config or PiBrowserConfig.from_env()
        self.launcher = launcher or PiLauncher(self.config)
        self._tunnel_factory = tunnel_factory
        self._cdp_connect = cdp_connect
        self._screen_factory = screen_factory
        self._agent_runner = agent_runner
        self._callback_get = callback_get or _callback_get
        self._clock = clock
        self.space_id: int | None = None
        self.notice = False
        self.handed_off = False
        self.last_agent_log: Path | None = None
        self.login = launcher_login(login) if login else None
        self.restored_login = False
        self.login_saved: bool | None = None
        # False after a wrong-account check: finish() stops Chromium without a save, so
        # another account's cookies never go into this account's tar.
        self.keep_login = True
        self.page: Any = None
        self._cdp: CdpSession | None = None
        self._cdp_tunnel: SshTunnel | None = None
        self._screen: PiScreen | None = None
        self._started = False
        self._token: str | None = None
        self._routed: set[str] = set()
        self._forwarded: dict[str, httpx.Response] = {}
        self._callback_seen = False

    @property
    def person_hint(self) -> str:
        return f"the Pi browser (open {self.config.novnc_url})"

    def open_space(self, name: str) -> int:
        """Start Chromium on the Pi and connect to it. On any failure everything is
        stopped again before the error goes up (the caller has no driver to finish yet)."""
        self._token = name
        try:
            reply = self.launcher.start(name, login=self.login)
            self._started = True
            assert reply.pid is not None
            self.space_id = reply.pid
            self.restored_login = bool(reply.restored_login)
            self._cdp_tunnel = self._tunnel_factory(self.config, f"127.0.0.1:{reply.cdp_port or self.config.cdp_port}")
            port = self._cdp_tunnel.start()
            self._cdp = self._cdp_connect(f"http://127.0.0.1:{port}")
            self.page = self._cdp.page
            with suppress(Exception):
                page = self.page
                limited(page, PAGE_CALL_TIMEOUT_S, "bring to front", page.bring_to_front)
            return reply.pid
        except BaseException as e:
            if not self._started and not isinstance(e, LauncherBusy | PiUnreachable):
                # The start may have worked on the Pi while this side gave up (an ssh
                # timeout): stop the Chromium that this token started, and only that one.
                with suppress(Exception):
                    self.launcher.stop(save_login=True, token=name, login=self.login)
            with suppress(Exception):
                self.finish()
            raise

    def goto(self, url: str) -> None:
        try:
            page = self._page()
            limited(
                page,
                GOTO_TIMEOUT_MS / 1000 + PAGE_CALL_MARGIN_S,
                "a page open",
                lambda: page.goto(url, wait_until="domcontentloaded", timeout=GOTO_TIMEOUT_MS),
            )
        except PortalError:
            raise
        except Exception as e:
            raise PortalError(f"the Pi browser could not open the page: {type(e).__name__}") from None

    def hand_off(self) -> None:
        """Leave Chromium running for a person in noVNC. The next start keeps its login."""
        self.handed_off = True
        self.launcher.mark_handoff(token=self._token)

    def reclaim(self) -> bool:
        """Code takes the window back after a person's step (a password), so
        :meth:`finish` stops Chromium again. If the launcher call fails, the window
        stays with the person (False)."""
        if not self.handed_off or not self._started:
            return False
        try:
            # The token: after a crash another command's run may hold the browser now.
            self.launcher.clear_handoff(token=self._token)
        except PortalError:
            return False
        self.handed_off = False
        return True

    def discard_login(self) -> None:
        """The browser is signed in as another account (or one code cannot name): the
        stop must not save its cookies into this account's tar."""
        self.keep_login = False

    def finish(self) -> None:
        """Close every local link (screen adapter, Playwright, tunnels), then stop
        Chromium and keep a changed login. Not the stop after a hand-off: the person
        owns the window then. Runs every step, then raises the first error."""
        errors: list[str] = []
        screen, self._screen = self._screen, None
        if screen is not None:
            screen.close()
        cdp, self._cdp, self.page = self._cdp, None, None
        if cdp is not None:
            try:
                cdp.close()
            except Exception as e:
                errors.append(f"Playwright stop: {type(e).__name__}")
        tunnel, self._cdp_tunnel = self._cdp_tunnel, None
        if tunnel is not None:
            tunnel.stop()
        if self._started and not self.handed_off:
            try:
                # The token: a late finish must not stop the Chromium of a command that
                # started since (this run's Chromium crashed, or a person closed it).
                reply = self.launcher.stop(save_login=self.keep_login, token=self._token, login=self.login)
                self.login_saved = bool(reply.saved)
                self._started = False
                self.space_id = None
            except PortalError as e:
                errors.append(str(e))
        if errors:
            raise PortalError(f"the Pi browser did not stop cleanly: {'; '.join(errors)}")

    def _page(self) -> Any:
        """The tab on screen. A sign-in can open a new tab (Slack's workspace list) and the old
        one can be closed: then the context's open tab the person sees takes over (the mask
        script and the callback route are on the context, so they cover it too)."""
        if self.page is None:
            raise PortalError("the Pi browser is not connected")
        self.page = follow_tab(self.page)
        return self.page

    def pump(self) -> None:
        """One short wait in which Playwright handles events (the callback route): the
        consent listener calls it while it waits for the redirect."""
        self.wait_ms(PUMP_MS)

    def wait_ms(self, ms: int) -> None:
        """Sleep, and let Playwright handle events meanwhile (the callback route)."""
        page = self.page
        if page is not None:
            try:
                limited(page, ms / 1000 + PAGE_CALL_MARGIN_S, "a wait", lambda: page.wait_for_timeout(ms))
                return
            except Exception:
                pass
        time.sleep(ms / 1000)

    def now_ms(self) -> float:
        return self._clock() * 1000

    def wait_for(self, ms: int, test: Callable[[], bool]) -> bool:
        end = self.now_ms() + ms
        while self.now_ms() < end:
            if test():
                return True
            self.wait_ms(500)
        return test()

    @contextmanager
    def secret_lock(self) -> Iterator[None]:
        """No frame and no input on the agent's screen while code works with a secret."""
        if self._screen is None:
            yield
            return
        with self._screen.secret_lock():
            yield

    def evaluate(
        self, js: str, arg: Any = None, default: Any = None, *, strict: bool = False, retry_on_navigation: bool = True
    ) -> Any:
        """``page.evaluate``. A JS error in the script returns ``default`` (``strict``:
        raises :class:`PortalError`). A closed page raises :class:`PiPageLost`, and so
        does a navigation that replaced the page's context twice in a row. With
        ``retry_on_navigation`` false, the first navigation raises :class:`PiPageNavigated`
        (a script that acts on the page runs one time only)."""
        page = self._page()
        for attempt in range(2):
            try:
                return limited(page, PAGE_CALL_TIMEOUT_S, "a read", lambda: page.evaluate(js, arg))
            except PortalError:
                raise
            except Exception as e:
                # Only the type name goes into a message: the error text can quote the page.
                loss = page_loss(e)
                if loss is PageLoss.navigated and not retry_on_navigation:
                    raise PiPageNavigated("the Pi page navigated during a call that runs one time only") from None
                if loss is PageLoss.navigated and attempt == 0:
                    self.wait_ms(NAVIGATION_RETRY_MS)
                    continue
                if loss is not None:
                    raise PiPageLost(f"the Pi browser lost the page during a read ({loss.value})") from None
                if strict:
                    raise PortalError(f"a read of the Pi page failed ({type(e).__name__})") from None
                return default
        raise AssertionError("unreachable")  # pragma: no cover

    def click_button(self, name: str) -> bool:
        """Click the button with this accessible name (exact). If the role locator finds
        none or several, click the one exact match in the DOM instead."""
        page = self._page()
        try:
            locator = page.get_by_role("button", name=name, exact=True)
            limited(
                locator,
                CLICK_TIMEOUT_MS / 1000 + PAGE_CALL_MARGIN_S,
                "a click",
                lambda: locator.click(timeout=CLICK_TIMEOUT_MS),
            )
            return True
        except PortalError:
            raise  # no reply: the click may have run, so no second click in the DOM
        except Exception:
            return self.evaluate(CONSENT_MATCH_JS, {"want": name.lower(), "click": True}, 0) == 1

    def _blank(self) -> None:
        with suppress(Exception):
            page = self._page()
            limited(
                page,
                GOTO_TIMEOUT_MS / 1000 + PAGE_CALL_MARGIN_S,
                "a page open",
                lambda: page.goto("about:blank", timeout=GOTO_TIMEOUT_MS),
            )

    def _ensure_screen(self) -> str:
        if self._screen is None or self._screen.server is None:
            screen = self._screen_factory(self.config)
            url = screen.start()
            self._screen = screen
            return url
        return self._screen.server.url

    def agent(
        self,
        goal: str,
        timeout_s: float = AGENT_TIMEOUT_S,
        secret_visible: Callable[[], bool] | None = None,
        *,
        hand_off_on_need: bool = True,
        gate: pi_desktop_adapter.ScreenGate | None = None,
        jobs: PageJobs | None = None,
        extras: AgentExtras | None = None,
    ) -> VaultLine:
        """Run the click agent on the Pi screen; its last ``@@VAULT`` line. Its output
        goes to :func:`app_portal.write_agent_log` (redacted), never to the terminal.

        ``secret_visible`` (a page check, run on this thread): each frame goes to the
        agent only after this check says no secret shows, and the check also runs
        every :data:`PUMP_MS`. Once it is true, the screen stays sealed for the rest
        of the command.

        ``hand_off_on_need`` False: a ``need_person`` line raises :class:`NeedPerson` but
        leaves the window with code, so code can sign in first (:mod:`sign_in`).

        ``gate`` is used instead of a :class:`ScreenGate` on ``secret_visible`` (the mint's
        :class:`pi_desktop_adapter.MaskGate`). ``jobs``: the page steps of the ``extras``
        server's tools, run on this thread while the agent runs."""
        if self.tools.agent is None:
            raise PortalUnavailable("no `claude` binary here for the portal agent")
        desktop_url = self._ensure_screen()
        screen = self._screen
        assert screen is not None
        workdir = tempfile.mkdtemp(prefix="vault-agent-")  # empty: no project files to read
        header = f"# portal agent, Pi browser (Chromium pid {self.space_id})\n## goal\n{goal}"
        agent = self.tools.agent
        if gate is None and secret_visible is not None:
            gate = pi_desktop_adapter.ScreenGate(secret_visible)
        pump: Callable[[], None] | None = self.pump if self.page is not None else None
        if gate is not None:
            screen.set_gate(gate)
            # Answer each frame check (the check runs Playwright, which handles events too).
            pump = partial(gate.serve, PUMP_MS / 1000)
        if jobs is not None:
            pump = _with_jobs(pump or self.pump, jobs)
        runner_args: dict[str, Any] = {"extras": extras} if extras is not None else {}
        try:
            run = _in_thread(
                lambda: self._agent_runner(agent, goal, desktop_url, workdir, timeout_s, **runner_args),
                pump=pump,
                on_abort=LIVE_AGENTS.kill_all,
            )
        finally:
            shutil.rmtree(workdir, ignore_errors=True)
            if gate is not None:
                gate.close()
                if gate.latched:
                    screen.seal()
                screen.set_gate(None)
        if run.timed_out:
            self.last_agent_log = write_agent_log(
                self.space_id, f"{header}\n## exit: timeout after {timeout_s:.0f} s", run.stdout, run.stderr
            )
            raise PortalError(f"the portal agent ran over {timeout_s:.0f} s{log_hint(self.last_agent_log)}")
        self.last_agent_log = write_agent_log(
            self.space_id, f"{header}\n## exit: {run.returncode}", run.stdout, run.stderr
        )
        lines = parse_lines(run.stdout)
        if not lines:
            raise PortalError(
                f"the portal agent ended (exit {run.returncode}) without a result line{log_hint(self.last_agent_log)}"
            )
        last = lines[-1]
        if last.need_person:
            if hand_off_on_need:
                with suppress(PortalError):
                    self.hand_off()
                self.handed_off = True
            raise NeedPerson(
                f"the browser needs a person ({last.need_person}): finish it in {self.person_hint}, "
                f"then run the command again{log_hint(self.last_agent_log)}",
                reason=last.need_person,
            )
        return last

    def _forward(self, url: str, callback: str) -> httpx.Response:
        """Send one redirect-origin URL to the listener on this machine, once: the
        route and the ``request`` listener can both see the same URL."""
        got = self._forwarded.get(url)
        if got is None:
            got = self._callback_get(url)
            self._forwarded[url] = got
        if url.startswith(callback):
            self._callback_seen = True  # the code reached the listener
        return got

    def route_callback(self, redirect_uri: str) -> None:
        """Send the browser's requests for the redirect origin to the listener on THIS
        machine. On the Pi, 127.0.0.1:8765 has no listener; the request never leaves
        the browser: Playwright answers it with the listener's reply.

        Playwright routes only the first URL of a redirect chain. So the listener's
        302 to ``/done`` goes back as a 200 page that calls ``location.replace``
        (a new navigation, which the route sees), and a ``request`` listener
        forwards a redirect leg (``redirected_from``) to the callback, for a vendor
        that answers the Allow click with a server-side 302."""
        origin = redirect_uri.split("/callback")[0].rstrip("/") + "/"
        if origin in self._routed:
            return
        callback = redirect_uri.split("?")[0]

        def handle(route: Any) -> None:
            try:
                url = route.request.url
                r = self._forward(url, callback)
                location = r.headers.get("location")
                if 300 <= r.status_code < 400 and location:
                    target = urljoin(url, location)
                    if not target.startswith(origin):
                        raise ValueError("the listener redirected off its origin")
                    route.fulfill(
                        status=200,
                        headers={"content-type": "text/html; charset=utf-8", "cache-control": "no-store"},
                        body=_navigate_page(target),
                    )
                    return
                headers = {k: v for k, v in r.headers.items() if k.lower() in ("content-type", "cache-control")}
                route.fulfill(status=r.status_code, headers=headers, body=r.content)
            except Exception:
                with suppress(Exception):
                    route.fulfill(status=502, body="the plato vault command is not listening")

        def on_request(request: Any) -> None:
            try:
                if request.redirected_from is not None and request.url.startswith(origin):
                    self._forward(request.url, callback)
            except Exception:
                pass  # the listener times out and says so

        context = self._page().context
        limited(
            context,
            PAGE_CALL_TIMEOUT_S,
            "the callback route",
            # A regex: Playwright matches it in the browser and does not hold each request for Python.
            lambda: context.route(re.compile("^" + re.escape(origin)), handle),
        )
        context.on("request", on_request)
        self._routed.add(origin)

    def click_consent(self, recipe: VendorRecipe) -> VaultLine:
        """The same steps as ``app_portal._consent_script``: wait for exactly one grant
        button, click it, wait for the redirect, a second click if needed."""
        self.route_callback(recipe.redirect_uri)  # added before the first page by app._consent
        base = recipe.redirect_uri.split("/callback")[0]
        want = recipe.consent_button.lower()

        def at_base() -> bool:
            if self._callback_seen:
                return True
            href = self.evaluate("() => location.href", None, "") or ""
            return str(href).startswith(base)

        def count() -> int:
            return int(self.evaluate(CONSENT_MATCH_JS, {"want": want, "click": False}, 0) or 0)

        with self.secret_lock():
            if at_base():
                return VaultLine(allowed=True, allow_buttons=0, clicks=0)
            seen = {"n": 0}

            def ready() -> bool:
                if at_base():
                    return True
                seen["n"] = count()
                return seen["n"] >= 1

            self.wait_for(CONSENT_BUTTON_WAIT_MS, ready)
            if at_base():
                return VaultLine(allowed=True, allow_buttons=0, clicks=0)
            if seen["n"] != 1:
                return VaultLine(allowed=False, error="allow_buttons", allow_buttons=seen["n"], clicks=0)
            self.wait_ms(1000)  # let the page's script attach its click handler
            clicks = 0
            done = False
            while not done and clicks < CONSENT_CLICKS:
                if count() != 1:
                    break
                if not self.click_button(recipe.consent_button):
                    return VaultLine(allowed=False, error="click_failed", allow_buttons=count(), clicks=clicks)
                clicks += 1
                done = self.wait_for(CONSENT_REDIRECT_WAIT_MS, at_base)
            if done:
                href = str(self.evaluate("() => location.href", None, "") or "")
                if not href.startswith(base):
                    self._blank()  # the error page of a forwarded redirect leg shows the code URL
                return VaultLine(allowed=True, allow_buttons=1, clicks=clicks)
            return VaultLine(allowed=False, error="no_redirect", allow_buttons=count(), clicks=clicks)

    def count_generate_buttons(self) -> int:
        return int(self.evaluate(GENERATE_COUNT_JS, None, 0) or 0)

    def read_secret(self, recipe: VendorRecipe) -> tuple[PortalSecretFile, VaultLine]:
        """Click "Generate secret" and read the values from the DOM into this process,
        with no model in the path and no file. Then blank the tab, also on an error.
        Canva shows a new secret ONE time: if this fails after the click, a person must
        generate another one."""
        page = self._page()
        with self.secret_lock():
            if self.count_generate_buttons() != 1:
                raise PortalError("the secret step did not write the secret (generate_buttons)")
            m = _APP_ID.search(str(page.url or ""))
            clicked = False
            try:
                if not self.click_button("Generate secret"):
                    raise PortalError("the secret step did not write the secret (click_failed)")
                clicked = True
                limited(
                    page,
                    SECRET_WAIT_MS / 1000 + PAGE_CALL_MARGIN_S,
                    "the secret wait",
                    lambda: page.wait_for_function(SECRET_READY_JS, timeout=SECRET_WAIT_MS),
                )
                got = limited(
                    page,
                    PAGE_CALL_TIMEOUT_S,
                    "the secret read",
                    lambda: page.evaluate(SECRET_VALUES_JS, recipe.client_id_prefix),
                )
            except PortalError:
                raise
            except Exception:
                why = "after_click" if clicked else "click_failed"
                raise PortalError(f"the secret step did not write the secret ({why})") from None
            finally:
                self._blank()
        values = got if isinstance(got, dict) else {}
        client_id = str(values.get("clientId") or "")
        secret = SecretStr(str(values.get("secret") or ""))
        del got, values
        line = VaultLine(
            written=True,
            client_id_prefix=client_id[:5],
            secret_len=len(secret.get_secret_value()),
            app_id=m.group(1) if m else None,
        )
        if not client_id.startswith(recipe.client_id_prefix) or not secret.get_secret_value():
            raise PortalError(
                f"the page gave no client id starting {recipe.client_id_prefix} or no secret "
                f"(client id prefix {line.client_id_prefix!r}, secret length {line.secret_len})"
            )
        return PortalSecretFile(client_id=client_id, client_secret=secret), line


def _with_jobs(pump: Callable[[], None], jobs: PageJobs) -> Callable[[], None]:
    def both() -> None:
        pump()
        jobs.serve()

    return both


def _navigate_page(target: str) -> bytes:
    """A page that goes on to ``target`` with no history entry for the code URL."""
    js_url = json.dumps(target).replace("<", "\\u003c")
    return f'<!doctype html><meta charset="utf-8"><script>location.replace({js_url})</script>'.encode()


def _callback_get(url: str) -> httpx.Response:
    """The listener's reply for one redirect, from this machine (no redirect follow:
    the route turns the listener's 302 to ``/done`` into a new navigation)."""
    with httpx.Client(timeout=CALLBACK_FORWARD_TIMEOUT_S, follow_redirects=False) as http:
        return http.get(url)


class PiTotpPage:
    """:class:`totp_portal.TotpPage` on the Pi browser: the same in-page functions,
    run with ``page.evaluate``, and clicks through Playwright's role locators. Every
    value comes back into this process; nothing is written to a file."""

    def __init__(self, driver: PiDriver, recipe: TotpRecipe) -> None:
        self.driver = driver
        self.recipe = recipe

    def _count(self, names: list[str]) -> int:
        return int(self.driver.evaluate(BY_NAME_JS, {"names": names, "click": False}, 0) or 0)

    def _click_name(self, name: str) -> bool:
        try:
            locator = self.driver._page().get_by_role("button", name=name, exact=True)
            limited(
                locator,
                CLICK_TIMEOUT_MS / 1000 + PAGE_CALL_MARGIN_S,
                "a click",
                lambda: locator.click(timeout=CLICK_TIMEOUT_MS),
            )
            return True
        except PortalError:
            raise
        except Exception:
            return int(self.driver.evaluate(BY_NAME_JS, {"names": [name], "click": True}, 0) or 0) >= 1

    def signed_in_emails(self) -> list[str]:
        """The account emails that the open page shows (the same steps as
        ``totp_portal._emails_script``): wait for one, look once more after a settle.
        ``[]``: the page was read and showed none. A failed last read with no email found
        raises :class:`EmailReadFailed`, so a failed check never looks like a page with no email."""
        d = self.driver
        cfg = {"ignore": self.recipe.vendor_email_domains}
        seen: set[str] = set()
        failed = False

        def look() -> bool:
            nonlocal failed
            try:
                got = d.evaluate(SIGNED_IN_EMAILS_JS, cfg, [], strict=True)
            except PiPageLost:
                raise
            except PortalError:
                failed = True  # a JS error: read again, like the ego script
                return bool(seen)
            failed = False
            if isinstance(got, list):
                seen.update(str(e) for e in got)
            return bool(seen)

        if d.wait_for(IDENTITY_WAIT_MS, look):
            d.wait_ms(IDENTITY_SETTLE_MS)
            look()
        if failed and not seen:
            raise EmailReadFailed("the account check could not read the page (read_failed)")
        return sorted(seen)

    def reveal_key(self) -> tuple[TotpKey, VaultLine]:
        d = self.driver
        cfg = {"keyPattern": self.recipe.key_pattern}
        empty: dict[str, list[str]] = {"uris": [], "keys": []}

        def look() -> dict[str, list[str]]:
            got = d.evaluate(FIND_KEY_JS, cfg, empty)
            return got if isinstance(got, dict) else empty

        with d.secret_lock():
            got = look()
            if not got.get("uris") and not got.get("keys"):
                for name in self.recipe.reveal_texts:
                    if self._count([name]) >= 1:
                        self._click_name(name)
                        break

                def found() -> bool:
                    nonlocal got
                    got = look()
                    return bool(got.get("uris") or got.get("keys"))

                d.wait_for(KEY_WAIT_MS, found)
            uris, keys = list(got.get("uris") or []), list(got.get("keys") or [])
            del got
        if not uris and not keys:
            raise PortalError("the read step wrote nothing (no_key)")
        candidates = KeyCandidates(uris=[SecretStr(u) for u in uris], keys=[SecretStr(k) for k in keys])
        line = VaultLine(written=True, uri_count=len(uris), key_count=len(keys))
        del uris, keys
        return pick_key(candidates, self.recipe), line

    def type_code(self, code: str) -> VaultLine:
        """The steps of ``totp_portal._code_script``: type, read the state, click the
        confirm button, and count only a NEW error as rejected."""
        d = self.driver
        r = self.recipe
        with d.secret_lock():
            try:
                typed = d.evaluate(
                    TYPE_CODE_JS,
                    {"code": code, "selectors": r.code_input_selectors, "digits": r.digits},
                    retry_on_navigation=False,
                )
            except PiPageNavigated:
                typed = None
            if typed is None:
                # No reply: the script may have typed before the page moved on, so the seed stays.
                return VaultLine(result=CodeResult.unknown.value, typed=True, inputs=-1)
            if not isinstance(typed, dict) or not typed.get("typed"):
                inputs = typed.get("inputs", 0) if isinstance(typed, dict) else -1
                return VaultLine(result="not_typed", typed=False, inputs=inputs)
            scfg = {"accepted": r.accepted_buttons, "errors": r.error_texts, "confirm": r.confirm_button}

            def look() -> dict[str, Any] | None:
                s = d.evaluate(CODE_STATE_JS, scfg, None)
                return s if isinstance(s, dict) else None

            d.wait_ms(500)
            before = look()
            result = CodeResult.unknown.value
            clicked = False
            if before and before.get("accepted"):
                result = CodeResult.accepted.value  # the page took the code by itself
            else:
                if self._count([r.confirm_button]) == 1:
                    clicked = self._click_name(r.confirm_button)
                d.wait_ms(CONFIRM_SETTLE_MS)
                cleared = not (before and before.get("error"))
                end = d.now_ms() + CONFIRM_WAIT_MS
                while d.now_ms() < end:
                    s = look()
                    if s and s.get("accepted"):
                        result = CodeResult.accepted.value
                        break
                    if s and not s.get("error"):
                        cleared = True
                    if s and s.get("error") and cleared and s.get("confirmOpen") and clicked:
                        d.wait_ms(CONFIRM_SETTLE_MS)
                        again = look()
                        if again and again.get("accepted"):
                            result = CodeResult.accepted.value
                        elif again and again.get("error") and again.get("confirmOpen"):
                            result = CodeResult.rejected.value
                        break
                    d.wait_ms(500)
        line = VaultLine(result=result, typed=True, clicked=clicked, inputs=typed.get("inputs"))
        if not clicked and result != CodeResult.accepted.value:
            line.error = "confirm_button"
        return line

    def key_ready(self) -> bool:
        """The setup key step shows: a reveal button, an otpauth URI, or a seed that matches
        ``key_pattern``. Every read is strict: the screen gate seals on an error, because a
        page that does not answer may show the QR code."""
        d = self.driver
        if int(d.evaluate(BY_NAME_JS, {"names": self.recipe.reveal_texts, "click": False}, strict=True) or 0) >= 1:
            return True
        if d.evaluate(OTPAUTH_IN_PAGE_JS, None, strict=True):
            return True
        # A page can show the seed as text with no otpauth URI (the "can't scan" view).
        return bool(d.evaluate(KEY_SHOWS_JS, {"keyPattern": self.recipe.key_pattern}, strict=True))

    def read_backup_codes(self) -> list[SecretStr]:
        d = self.driver
        codes: list[str] = []
        with d.secret_lock():

            def found() -> bool:
                nonlocal codes
                got = d.evaluate(BACKUP_FIND_JS, {"pattern": self.recipe.backup_code_pattern}, [])
                codes = [str(c) for c in got] if isinstance(got, list) else []
                return bool(codes)

            d.wait_for(BACKUP_WAIT_MS, found)
        record = BackupCodesFile(codes=[SecretStr(c) for c in codes])
        del codes
        kept = [c for c in record.codes if c.get_secret_value()]
        if not self.recipe.backup_codes_min <= len(kept) <= self.recipe.backup_codes_max:
            return []
        return kept

    def finish_setup(self) -> bool:
        d = self.driver
        finished = False
        with d.secret_lock():
            try:
                if self._count([self.recipe.finish_button]) >= 1:
                    finished = self._click_name(self.recipe.finish_button)
                    d.wait_ms(1500)
            finally:
                d._blank()
        return finished
