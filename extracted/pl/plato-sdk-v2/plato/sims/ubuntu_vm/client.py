"""HTTP client for Desktop Agent API."""

from __future__ import annotations

import asyncio
import json as _json
import logging
import os
import re
import threading
import time
import warnings
from collections.abc import Callable
from typing import Any
from urllib.parse import urlparse

import httpx

from plato.v2.env_utils import is_proctor_env

from .api.bash.bash import asyncio as _bash_async
from .api.bash.bash import sync as _bash_sync
from .api.computer.computer import asyncio as _computer_async
from .api.computer.computer import sync as _computer_sync
from .api.edit.edit import asyncio as _edit_async
from .api.edit.edit import sync as _edit_sync
from .api.status.get_status import asyncio as _status_async
from .api.status.get_status import sync as _status_sync
from .models import BashRequest, ComputerRequest, EditRequest, StatusResponse, ToolResult

logger = logging.getLogger(__name__)

# Environment variable prefix for this client
ENV_PREFIX = "UBUNTU_VM"

LIVEVIEW_PORT = 6080
DESKTOP_AGENT_PORT = 9000
# Both ubuntu and Windows expose Chrome CDP on 9224 via an nginx reverse proxy
# (Host rewrite -> localhost:9225) — one port, one connection path for both.
CDP_PORT = 9224

# Pattern: https://{job_id}--{port}.sims.plato.so or https://{job_id}.sims.plato.so
_JOB_ID_RE = re.compile(r"https?://([a-f0-9-]+?)(?:--\d+)?\..*sims\.plato\.so")


def _base_url_from_job_id(job_id: str, port: int = DESKTOP_AGENT_PORT, gateway_host: str = "sims.plato.so") -> str:
    """Build a sims base URL from a job ID and port for the given gateway host.

    ``gateway_host`` defaults to the prod ``sims.plato.so`` gateway. Pass a
    per-deployment host (e.g. ``testing.sims.plato.so``) to target another
    deployment — see :func:`_deployment_sims_gateway`.
    """
    return f"https://{job_id}--{port}.{gateway_host}"


def _extract_job_id(base_url: str) -> str:
    """Extract the job ID from a sims.plato.so base URL."""
    m = _JOB_ID_RE.match(base_url)
    if m:
        return m.group(1)
    raise ValueError(
        f"Cannot extract job_id from base_url '{base_url}'. "
        "Expected format: https://{{job_id}}--{{port}}.sims.plato.so"
    )


def _gateway_from_base_url(base_url: str) -> str:
    """Return the sims gateway host embedded in a ``{job}--{port}.{gateway}`` URL.

    Preserves whatever deployment gateway the client's base URL already targets
    (prod ``sims.plato.so`` or a per-deployment host like ``testing.sims.plato.so``)
    so CDP/liveview URLs follow the same deployment. Falls back to prod when the
    host can't be parsed.
    """
    host = urlparse(base_url).hostname or ""
    _, _, gateway = host.partition(".")  # strip the "{job}--{port}" first label
    return gateway or "sims.plato.so"


def _deployment_sims_gateway(api_base_url: str | None) -> str:
    """Map an API base URL (PLATO_BASE_URL) to its sims gateway host.

    ``https://plato.so`` -> ``sims.plato.so``;
    ``https://testing.plato.so`` -> ``testing.sims.plato.so``. Mirrors the
    proxy-host derivation in ``plato.v2.utils.proxy_tunnel``. Defaults to prod
    ``sims.plato.so`` when the deployment can't be determined.
    """
    hostname = urlparse(api_base_url or os.getenv("PLATO_BASE_URL", "https://plato.so")).hostname
    if not hostname or hostname == "plato.so" or hostname == "localhost" or hostname.startswith("127."):
        return "sims.plato.so"
    subdomain, _, domain = hostname.partition(".")
    if domain:
        return f"{subdomain}.sims.{domain}"
    return "sims.plato.so"


def _api_base_url_from_environment(environment: Any) -> str | None:
    """Best-effort read of the deployment API base URL from a v2 Environment.

    The Environment exposes the session's httpx client via ``._http``; its
    ``base_url`` is the ``PLATO_BASE_URL`` the session was created against.
    """
    http = getattr(environment, "_http", None)
    base = getattr(http, "base_url", None)
    return str(base) if base else None


# API base path suffix (e.g., "/api/v1")
BASE_PATH = ""

# Default credentials (configured during generation)


def _get_env_config() -> tuple[str | None, dict[str, str]]:
    """Get base URL and headers from environment variables.

    Looks for:
    - {PREFIX}_BASE_URL: Base URL for API requests
    - {PREFIX}_API_TOKEN: Bearer token for Authorization header

    Returns:
        Tuple of (base_url, headers)
    """
    base_url = os.environ.get(f"{ENV_PREFIX}_BASE_URL")
    headers: dict[str, str] = {}

    # Check for bearer token
    token = os.environ.get(f"{ENV_PREFIX}_API_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    return base_url, headers


# computer-use drives the desktop_agent as: request -> multi-second LLM wait ->
# next request. Idle connections therefore sit in the pool long enough for the
# server to close them on its idle timeout; reusing one then raises
# RemoteProtocolError ("Server disconnected without sending a response"). Don't
# keep idle connections around — open a fresh one per request. The extra TCP
# setup is negligible for this low-rate, plain-HTTP-over-mesh workload, and
# pooling bought nothing across the long idle gaps anyway.
_NO_KEEPALIVE = httpx.Limits(max_keepalive_connections=0)

# Best-effort startup command that disables the XFCE screensaver on ubuntu
# desktops. The Xvfb ``xfce4-screensaver`` daemon blanks the framebuffer to
# solid black after idle and only wakes on an *input* event — never on a
# screenshot read — so a run that opens with screenshot-only calls gets black
# frames until the first click/keypress (the classic "first few screenshots are
# black"). We turn off idle activation, disable X11 blanking, deactivate any
# active blank, and kill the daemon. Every step is guarded (``|| true``) so the
# command is a no-op on images without the screensaver; ``timeout 1`` caps the
# only step that talks over D-Bus in case the session bus is wedged. Ubuntu
# (firecracker) only — Windows/QEMU has no XFCE screensaver.
_DISABLE_SCREENSAVER_CMD = (
    "export DISPLAY=:0; "
    "xfconf-query -c xfce4-screensaver -p /saver/enabled -n -t bool -s false 2>/dev/null || true; "
    "xfconf-query -c xfce4-screensaver -p /saver/idle-activation/enabled -n -t bool -s false 2>/dev/null || true; "
    "xfconf-query -c xfce4-screensaver -p /lock/enabled -n -t bool -s false 2>/dev/null || true; "
    "xset s off 2>/dev/null || true; xset s noblank 2>/dev/null || true; "
    "timeout 1 xfce4-screensaver-command --deactivate 2>/dev/null || true; "
    "pkill -x xfce4-screensaver 2>/dev/null || true"
)

# -- Timezone offset setup ----------------------------------------------------
# Pin the VM clock to a whole-hour UTC offset. The two providers need different
# commands, so the OS branch (via ``_is_qemu``) picks the right one:
#
# * Ubuntu (firecracker) uses the tz database. Note the POSIX sign inversion —
#   ``UTC+4`` is the zone ``Etc/GMT-4`` and ``UTC-3`` is ``Etc/GMT+3``. We try
#   ``timedatectl`` first and fall back to symlinking ``/etc/localtime`` for
#   images where systemd isn't managing the clock.
# * Windows (qemu) has no tz database / symlink path, so we set the zone by its
#   Windows registry ID via ``tzutil``. Windows lacks a pure ``UTC±NN`` ID for
#   most offsets, so each offset maps to a representative *non-DST* regional
#   zone — that keeps the offset fixed year-round instead of jumping with DST.
#
# Supported offsets span the Windows table below (-12..+14), which is also the
# range of valid ``Etc/GMT`` zones; anything outside raises ``ValueError``.
_WINDOWS_TZID_BY_OFFSET: dict[int, str] = {
    -12: "Dateline Standard Time",
    -11: "UTC-11",
    -10: "Hawaiian Standard Time",
    -9: "UTC-09",
    -8: "UTC-08",
    -7: "US Mountain Standard Time",
    -6: "Central America Standard Time",
    -5: "SA Pacific Standard Time",
    -4: "SA Western Standard Time",
    -3: "SA Eastern Standard Time",
    -2: "UTC-02",
    -1: "Cape Verde Standard Time",
    0: "UTC",
    1: "W. Central Africa Standard Time",
    2: "South Africa Standard Time",
    3: "E. Africa Standard Time",
    4: "Arabian Standard Time",
    5: "West Asia Standard Time",
    6: "Central Asia Standard Time",
    7: "SE Asia Standard Time",
    8: "Singapore Standard Time",
    9: "Tokyo Standard Time",
    10: "West Pacific Standard Time",
    11: "Central Pacific Standard Time",
    12: "UTC+12",
    13: "UTC+13",
    14: "Line Islands Standard Time",
}

_MIN_UTC_OFFSET = min(_WINDOWS_TZID_BY_OFFSET)
_MAX_UTC_OFFSET = max(_WINDOWS_TZID_BY_OFFSET)


def _validate_utc_offset(utc_offset: int) -> None:
    if not isinstance(utc_offset, int) or isinstance(utc_offset, bool):
        raise ValueError(f"utc_offset must be an int (whole hours), got {utc_offset!r}")
    if not _MIN_UTC_OFFSET <= utc_offset <= _MAX_UTC_OFFSET:
        raise ValueError(f"utc_offset {utc_offset:+d} out of range [{_MIN_UTC_OFFSET:+d}, {_MAX_UTC_OFFSET:+d}]")


def _ubuntu_set_timezone_cmd(utc_offset: int) -> str:
    """Bash to set an Ubuntu VM to a whole-hour UTC offset (POSIX sign inverted)."""
    _validate_utc_offset(utc_offset)
    zone = f"Etc/GMT{-utc_offset:+d}"  # UTC+4 -> Etc/GMT-4, UTC-3 -> Etc/GMT+3
    return (
        f'timedatectl set-timezone "{zone}" 2>/dev/null || '
        f'{{ ln -sf "/usr/share/zoneinfo/{zone}" /etc/localtime && '
        f"printf '%s\\n' \"{zone}\" > /etc/timezone; }}"
    )


def _windows_set_timezone_cmd(utc_offset: int) -> str:
    """Command to set a Windows (qemu) VM to a whole-hour UTC offset via tzutil."""
    _validate_utc_offset(utc_offset)
    return f'tzutil /s "{_WINDOWS_TZID_BY_OFFSET[utc_offset]}"'


# -- Windows (qemu) Chrome CDP launch helpers ---------------------------------
#
# Windows Chrome is launched directly over the agent's POST /bash endpoint
# (PowerShell) instead of the agent's POST /browser/start (which schtasks-runs
# the baked C:\plato\start-edge-cdp.cmd launcher). The baked launcher does not
# pass --ignore-certificate-errors, and it can't be updated in already-baked
# snapshots — see _windows_chrome_launch_cmd for why the flag is required.

_WINDOWS_CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
_WINDOWS_CHROME_PROFILE_DIR = r"C:\plato\chrome-cdp-profile"

# One-shot limited-token scheduled task the SDK registers on demand to launch
# Chrome. Deliberately NOT the baked "PlatoChromeCDP" task: we must not
# overwrite the baked task's action (its flags feed /browser/start), only
# replicate its RunLevel Limited principal under our own name.
_WINDOWS_CHROME_TASK_NAME = "PlatoChromeCDPDirect"

# Sentinels printed by the probe so callers don't parse localized PS errors.
_CDP_UP = "__CDP_UP__"
_NO_CDP = "__NO_CDP__"

_WINDOWS_CHROME_KILL_CMD = "Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2"


def _windows_cdp_probe_cmd(internal_port: int) -> str:
    """PowerShell probe of the loopback Chrome CDP port inside a Windows VM.

    A raw ``TcpClient`` connect (not ``Test-NetConnection``, which is slow and
    chatty) that prints ``__CDP_UP__`` / ``__NO_CDP__`` sentinels.
    """
    return (
        f"try {{ $c = New-Object System.Net.Sockets.TcpClient('127.0.0.1', {internal_port}); "
        f"$c.Close(); Write-Output '{_CDP_UP}' }} catch {{ Write-Output '{_NO_CDP}' }}"
    )


def _windows_chrome_launch_cmd(internal_port: int) -> str:
    """PowerShell to launch Chrome with CDP on *internal_port* inside a Windows VM.

    Mirrors the flags of the baked ``C:\\plato\\start-edge-cdp.cmd`` launcher,
    plus two additions:

    * ``--ignore-certificate-errors`` — Windows snapshots resume with a frozen
      clock, and the sims proxy's (sims.plato.so) TLS cert rotates; once the
      cert's notBefore postdates the frozen clock, every page load fails with
      ``ERR_CERT_DATE_INVALID``. Certs rotate routinely so this can't be fixed
      server-side, and Playwright's ``ignoreHTTPSErrors`` is opt-in, so the
      flag must be on the browser process itself.
    * ``--test-type`` — ``--ignore-certificate-errors`` is on Chromium's
      bad-flags list, and without ``--test-type`` Chrome pins a persistent
      "unsupported command-line flag" warning bubble over the window, which
      shifts layout and contaminates pixel-driven screenshots/trajectories.
      The ubuntu launch passes it for the same reason.

    Chrome is started via a one-shot ``RunLevel Limited`` scheduled task, not
    a bare ``Start-Process``: the desktop agent's uvicorn runs elevated
    (``RunLevel Highest``), so a direct child would inherit the elevated
    token. The baked ``PlatoChromeCDP`` task that ``/browser/start`` ran is
    ``RunLevel Limited`` precisely so Chrome gets a normal desktop token
    (UIPI interactions with non-elevated processes, file ownership of
    downloads/profile artifacts, in-VM integrity-level checks all match the
    snapshot-baked environment). This replicates that principal shape under a
    separate task name so the baked task itself is left untouched.
    ``ExecutionTimeLimit`` is 0 because the task action is chrome.exe itself
    (no ``cmd /c start`` indirection like the baked launcher), so any finite
    limit would have Task Scheduler kill Chrome mid-session.

    Single quotes throughout: the command travels as a JSON string into
    ``powershell.exe -NoProfile -NonInteractive -Command``, where embedded
    double quotes would be stripped by argument parsing. (None of the flag
    values contain spaces, so the -Argument string needs no inner quoting.)
    """
    flags = " ".join(
        (
            f"--remote-debugging-port={internal_port}",
            "--remote-allow-origins=*",
            f"--user-data-dir={_WINDOWS_CHROME_PROFILE_DIR}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-default-apps",
            "--disable-popup-blocking",
            "--disable-session-crashed-bubble",
            "--hide-crash-restore-bubble",
            "--ignore-certificate-errors",
            "--test-type",
            "--start-maximized",
            "about:blank",
        )
    )
    return (
        f"$action = New-ScheduledTaskAction -Execute '{_WINDOWS_CHROME_EXE}' -Argument '{flags}'; "
        "$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited; "
        "$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries "
        "-ExecutionTimeLimit (New-TimeSpan -Seconds 0) -MultipleInstances Parallel; "
        f"Register-ScheduledTask -TaskName '{_WINDOWS_CHROME_TASK_NAME}' "
        "-Action $action -Principal $principal -Settings $settings -Force | Out-Null; "
        f"Start-ScheduledTask -TaskName '{_WINDOWS_CHROME_TASK_NAME}'"
    )


class Client:
    """Sync HTTP client for Desktop Agent API."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 120.0,
        headers: dict[str, str] | None = None,
        max_retries: int = 3,
        retry_on_status: tuple[int, ...] = (429, 500, 502, 503, 504),
        on_request: Callable[[httpx.Request], None] | None = None,
        on_response: Callable[[httpx.Response], None] | None = None,
        provider: str | None = None,
        cdp_port: int | None = None,
        **kwargs: Any,
    ):
        """Initialize the HTTP client.

        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds (matches Desktop Agent API's 120s bash timeout)
            headers: Default headers to include in all requests
            max_retries: Maximum number of retry attempts for failed requests
            retry_on_status: HTTP status codes that trigger a retry
            on_request: Hook called before each request
            on_response: Hook called after each response
            **kwargs: Additional arguments passed to httpx.Client
        """
        self._base_url = base_url.rstrip("/")
        # Always include Accept header for JSON APIs
        self._headers = {"Accept": "application/json", **(headers or {})}
        self._max_retries = max_retries
        self._retry_on_status = retry_on_status
        self._provider = provider
        self._cdp_port = cdp_port if cdp_port is not None else CDP_PORT
        self._closed = False

        event_hooks: dict[str, list[Callable]] = {"request": [], "response": []}
        if on_request:
            event_hooks["request"].append(on_request)
        if on_response:
            event_hooks["response"].append(on_response)

        self._timeout = timeout
        self._initialized = False
        self._screensaver_kicked = False
        self._screensaver_task: threading.Thread | None = None
        self._client = httpx.Client(
            base_url=self._base_url,
            timeout=timeout,
            headers=self._headers,
            follow_redirects=False,
            limits=_NO_KEEPALIVE,
            event_hooks=event_hooks if any(event_hooks.values()) else None,
            **kwargs,
        )

    def _resolve_cdp_port(self, port: int | None) -> int:
        return self._cdp_port if port is None else port

    def _is_qemu(self) -> bool:
        return self._provider == "qemu"

    def _kick_screensaver(self) -> None:
        """Fire-and-forget, best-effort disable of the desktop screensaver.

        Runs :data:`_DISABLE_SCREENSAVER_CMD` once, at startup, in a daemon
        thread so it never blocks the caller. Skipped on Windows/QEMU and after
        the first invocation. Any error is swallowed — this is purely a quality
        fix for the "first few screenshots are black" symptom, never load-bearing.
        """
        if self._screensaver_kicked or self._is_qemu():
            return
        self._screensaver_kicked = True

        def _run() -> None:
            try:
                self.bash(BashRequest(command=_DISABLE_SCREENSAVER_CMD))
            except Exception as exc:  # best-effort: never surface to the caller
                logger.debug("screensaver disable failed (ignored): %s", exc)

        self._screensaver_task = threading.Thread(target=_run, name="ubuntu-vm-disable-screensaver", daemon=True)
        self._screensaver_task.start()

    def _ensure_init(self) -> None:
        """Complete the sims proxy redirect/cookie dance on first use.

        The sims proxy has two routing modes:

        * **Web routing** (``_plato/init``): redirects to a per-simulator
          web proxy domain via a multi-step init chain.
        * **Sims routing** (default for ``*.sims.plato.so``): the app
          nginx always proxies subdomain requests to FastAPI which returns
          a 302 to the base domain (``sims.plato.so``) with a signed
          ``plato-sims-session`` cookie.  The sims router on the base
          domain reads the cookie and proxies to the correct VM.

        This method fires a probe GET, follows any redirects with a
        temporary client to capture routing cookies, then reconfigures
        the underlying ``httpx.Client`` to target the post-redirect host
        with the captured cookies.
        """
        if self._initialized:
            return

        response = self._client.request(method="GET", url="/status")
        if response.status_code not in (301, 302, 307, 308):
            self._initialized = True
            self._kick_screensaver()
            return

        location = response.headers.get("location", "")

        if "_plato/init" in location:
            logger.debug("Performing _plato/init redirect dance")
            with httpx.Client(follow_redirects=True, timeout=self._timeout) as tmp:
                tmp.get(location)
                cookies = dict(tmp.cookies)
            parsed = urlparse(location)
            new_base_url = f"{parsed.scheme}://{parsed.hostname}"
        else:
            logger.debug("Performing sims routing cookie dance")
            with httpx.Client(follow_redirects=True, timeout=self._timeout) as tmp:
                resp = tmp.get(f"{self._base_url}/status")
                cookies = dict(tmp.cookies)
            new_base_url = f"https://{resp.url.host}"

        self._initialized = True
        old_client = self._client
        self._client = httpx.Client(
            base_url=new_base_url,
            timeout=self._timeout,
            headers=self._headers,
            follow_redirects=False,
            limits=_NO_KEEPALIVE,
            cookies=cookies,
        )
        old_client.close()
        # Client is now reconfigured/stable — safe to fire the background task.
        self._kick_screensaver()

    @property
    def httpx(self) -> httpx.Client:
        """Access the underlying httpx client."""
        return self._client

    @property
    def max_retries(self) -> int:
        """Maximum number of retry attempts."""
        return self._max_retries

    @property
    def retry_on_status(self) -> tuple[int, ...]:
        """HTTP status codes that trigger a retry."""
        return self._retry_on_status

    def get_liveview_url(self) -> str:
        """Get the noVNC liveview URL for this VM."""
        job_id = _extract_job_id(self._base_url)
        gateway = _gateway_from_base_url(self._base_url)
        return f"https://{job_id}--{LIVEVIEW_PORT}.{gateway}?resize=scale&autoconnect=true"

    def bash(self, body: BashRequest) -> ToolResult:
        """Execute a shell command."""
        self._ensure_init()
        return _bash_sync(self._client, body=body)

    def _try_bash(self, command: str) -> ToolResult | None:
        """Run *command* over /bash, returning ``None`` on any transport error.

        The Windows ``ensure_chrome_cdp`` path must tolerate transient
        failures — 502s from the sims proxy while the desktop agent's
        post-logon scheduled task is still coming up on a cold boot, timeouts
        mid-poll — the way the old ``/browser/start`` retry loop did. Callers
        treat ``None`` as "agent not ready yet" and keep polling until their
        deadline.
        """
        try:
            return self.bash(BashRequest(command=command))
        except Exception as exc:
            logger.debug("bash call failed (tolerated, will retry): %s", exc)
            return None

    def computer(self, body: ComputerRequest) -> ToolResult:
        """Execute computer actions (mouse, keyboard, screenshot)."""
        self._ensure_init()
        return _computer_sync(self._client, body=body)

    def edit(self, body: EditRequest) -> ToolResult:
        """File operations (view, create, str_replace, insert, undo_edit)."""
        self._ensure_init()
        return _edit_sync(self._client, body=body)

    def status(self) -> StatusResponse:
        """Health check and display info."""
        self._ensure_init()
        return _status_sync(self._client)

    def set_timezone_offset(self, utc_offset: int, timeout: int = 30) -> ToolResult:
        """Pin the VM clock to a whole-hour UTC offset.

        Runs the OS-appropriate command over the desktop_agent bash endpoint,
        branching on provider: Ubuntu (firecracker) sets the ``Etc/GMT`` zone via
        ``timedatectl`` (with a symlink fallback); Windows (qemu) sets the zone by
        its registry ID via ``tzutil``. See the module-level timezone helpers for
        the sign-inversion and Windows-mapping details.

        Args:
            utc_offset: Signed whole-hour offset from UTC, e.g. ``4`` for UTC+4,
                ``-3`` for UTC-3. Must be within ``[-12, +14]``.
            timeout: Bash command timeout in seconds.

        Returns:
            The bash :class:`ToolResult`.

        Raises:
            ValueError: If ``utc_offset`` is not a whole hour in range.
        """
        command = _windows_set_timezone_cmd(utc_offset) if self._is_qemu() else _ubuntu_set_timezone_cmd(utc_offset)
        return self.bash(BashRequest(command=command, timeout=timeout))

    # -- CDP helpers ----------------------------------------------------------

    def get_cdp_url(self, port: int | None = None) -> str:
        """Return the sims proxy URL for the Chrome CDP port."""
        port = self._resolve_cdp_port(port)
        job_id = _extract_job_id(self._base_url)
        gateway = _gateway_from_base_url(self._base_url)
        return f"https://{job_id}--{port}.{gateway}"

    def ensure_chrome_cdp(self, port: int | None = None, timeout: int = 60) -> str:
        """Ensure Chrome CDP is reachable on *port* inside the VM.

        First polls for an already-responsive CDP endpoint.  If it doesn't
        come up within a short window (snapshot restore can leave Chrome
        processes alive but with dead TCP sockets), kills Chrome and
        restarts it so the CDP debug port is re-bound.

        Returns:
            The external sims-proxy CDP URL.

        Raises:
            TimeoutError: If Chrome CDP does not respond within *timeout*.
        """
        port = self._resolve_cdp_port(port)
        if self._is_qemu():
            self._ensure_init()
            # Windows Chrome is launched directly over the agent's /bash
            # endpoint (PowerShell) instead of POST /browser/start: the baked
            # launcher /browser/start runs lacks --ignore-certificate-errors,
            # which is required because snapshots resume with a frozen clock
            # that predates the sims proxy's rotating TLS cert (notBefore),
            # making every page load fail with ERR_CERT_DATE_INVALID (see
            # _windows_chrome_launch_cmd). Structure mirrors the ubuntu branch
            # below: probe the loopback CDP port, kill + relaunch Chrome if
            # unresponsive, then poll until CDP answers. Once up, CDP is
            # reachable over the sims proxy on 9224 (nginx Host rewrite),
            # same as ubuntu. Every /bash call here is failure-tolerant
            # (_try_bash): on a cold boot the agent's post-logon task may not
            # be listening yet, so transient 502s/timeouts count as "not
            # ready" and we keep retrying until the deadline — matching the
            # old /browser/start retry loop.
            effective_timeout = max(timeout, 90)
            internal_port = 9225 if port == 9224 else port
            cdp_probe = _windows_cdp_probe_cmd(internal_port)
            deadline = time.monotonic() + effective_timeout

            check = self._try_bash(cdp_probe)
            if check is None:
                logger.debug("First bash call failed; warming up client via status()")
                try:
                    self.status()
                except Exception as exc:
                    logger.debug("status() warmup failed (tolerated): %s", exc)
                check = self._try_bash(cdp_probe)
            if check is not None and _CDP_UP in (check.output or ""):
                logger.info("Windows Chrome CDP already responding on port %s", port)
                return self.get_cdp_url(port)

            # Quick poll — if the snapshot restored cleanly Chrome may just
            # need a moment for the socket to come back.
            logger.info("Waiting for Windows Chrome CDP on port %s ...", port)
            for _ in range(5):
                time.sleep(1)
                probe = self._try_bash(cdp_probe)
                if probe is not None and _CDP_UP in (probe.output or ""):
                    logger.info("Windows Chrome CDP ready on port %s", port)
                    return self.get_cdp_url(port)

            # Snapshot restore likely left Chrome with dead sockets — restart.
            # Kill + relaunch retry until the deadline too: the probes above
            # failing may just mean the agent itself is still coming up.
            logger.info("Windows Chrome CDP unresponsive; restarting Chrome")
            launch_cmd = _windows_chrome_launch_cmd(internal_port)
            launched = False
            last_err = ""
            while time.monotonic() < deadline:
                kill = self._try_bash(_WINDOWS_CHROME_KILL_CMD)
                launch = self._try_bash(launch_cmd) if kill is not None else None
                if launch is not None and not launch.error:
                    launched = True
                    break
                last_err = launch.error if launch is not None and launch.error else "agent unreachable"
                time.sleep(2)
            if not launched:
                raise TimeoutError(
                    f"Windows Chrome CDP not ready on port {port} after {effective_timeout}s: "
                    f"could not restart Chrome ({last_err})"
                )

            while time.monotonic() < deadline:
                time.sleep(2)
                probe = self._try_bash(cdp_probe)
                if probe is not None and _CDP_UP in (probe.output or ""):
                    logger.info("Windows Chrome CDP ready on port %s after restart", port)
                    return self.get_cdp_url(port)
                last_err = (probe.output or "").strip() if probe is not None else "agent unreachable"
            raise TimeoutError(
                f"Windows Chrome CDP not ready on port {port} after {effective_timeout}s. Last probe: {last_err}"
            )

        cdp_probe = f"curl -sf --max-time 2 http://localhost:{port}/json/version 2>/dev/null || echo __NO_CDP__"
        try:
            check = self.bash(BashRequest(command=cdp_probe))
        except Exception:
            logger.debug("First bash call failed; warming up client via status()")
            self.status()
            check = self.bash(BashRequest(command=cdp_probe))
        if "__NO_CDP__" not in (check.output or ""):
            logger.info("Chrome CDP already responding on port %s", port)
            return self.get_cdp_url(port)

        # Quick poll — if the snapshot restored cleanly Chrome may just
        # need a moment for the socket to come back.
        logger.info("Waiting for Chrome CDP on port %s ...", port)
        for _ in range(5):
            time.sleep(1)
            probe = self.bash(BashRequest(command=cdp_probe))
            if "__NO_CDP__" not in (probe.output or ""):
                logger.info("Chrome CDP ready on port %s", port)
                return self.get_cdp_url(port)

        # Snapshot restore likely left Chrome with dead sockets — restart.
        logger.info("Chrome CDP unresponsive; restarting Chrome")
        self.bash(BashRequest(command="pkill -9 -f 'chrome' 2>/dev/null; sleep 2"))

        chrome_internal_port = 9225 if port == 9224 else port
        self.bash(
            BashRequest(
                command=(
                    f"DISPLAY=:0 nohup google-chrome-stable "
                    f"--no-sandbox --disable-gpu --disable-dev-shm-usage "
                    f"--disable-features=PasswordManager,PasswordManagerOnboarding,PasswordLeakDetection "
                    f"--no-first-run --no-default-browser-check --disable-default-apps "
                    f"--disable-popup-blocking --disable-translate --disable-infobars "
                    # Snapshots resume with a frozen clock that can predate the
                    # sims proxy's rotating TLS cert -> ERR_CERT_DATE_INVALID.
                    f"--ignore-certificate-errors "
                    f"--test-type --start-maximized --window-size=1280,720 "
                    f"--user-data-dir=/tmp/chrome-cdp-profile "
                    f"--remote-debugging-port={chrome_internal_port} "
                    f"about:blank >/dev/null 2>&1 &"
                )
            )
        )

        deadline = time.monotonic() + timeout
        last_err = ""
        while time.monotonic() < deadline:
            time.sleep(2)
            probe = self.bash(BashRequest(command=cdp_probe))
            if "__NO_CDP__" not in (probe.output or ""):
                logger.info("Chrome CDP ready on port %s after restart", port)
                return self.get_cdp_url(port)
            last_err = (probe.output or "").strip()

        raise TimeoutError(f"Chrome CDP not ready on port {port} after {timeout}s. Last probe: {last_err}")

    def get_cdp_ws_url(self, port: int | None = None) -> str:
        """Return a Playwright-ready WebSocket URL for the VM's Chrome CDP.

        Thin wrapper over :meth:`prepare_cdp_connection` that drops the
        routing headers. Prefer :meth:`prepare_cdp_connection` directly: the
        returned ws URL needs the accompanying ``Cookie`` header to connect
        through the sims proxy.
        """
        ws_url, _ = self.prepare_cdp_connection(port)
        return ws_url

    def prepare_cdp_connection(self, port: int | None = None) -> tuple[str, dict[str, str]]:
        """Get the WebSocket URL **and** headers for Playwright ``connect_over_cdp``.

        Single path for both ubuntu and Windows (both expose Chrome CDP via an
        nginx Host-rewrite proxy on the same port). The sims proxy is two-tier:

        * **Subdomain** (``{job}--{port}.sims.plato.so``) — app nginx always
          302s to the base domain with a signed ``plato-sims-session`` cookie.
          A WebSocket client can't follow that 302.
        * **Base domain** (``sims.plato.so``) — the OpenResty sims router reads
          the cookie and proxies directly to the VM; WebSocket upgrades work.

        We GET ``/json/version`` through the subdomain following redirects (which
        completes the cookie dance and lands on the base host), then build the
        ws URL on that base host from the reported ``webSocketDebuggerUrl`` path.

        Returns:
            ``(ws_url, headers)`` -- pass both to
            ``chromium.connect_over_cdp(ws_url, headers=headers)``.
        """
        port = self._resolve_cdp_port(port)
        cdp_proxy_url = self.get_cdp_url(port)

        with httpx.Client(follow_redirects=True, timeout=30) as tmp:
            resp = tmp.get(f"{cdp_proxy_url}/json/version")
            resp.raise_for_status()
            cookies = dict(tmp.cookies)
            version_info = resp.json()

        ws_host = resp.url.host
        if ws_host is None:
            raise RuntimeError(f"Failed to resolve CDP proxy host from {resp.url}")

        ws_path = urlparse(version_info["webSocketDebuggerUrl"]).path
        ws_url = f"wss://{ws_host}{ws_path}"

        headers: dict[str, str] = {}
        if cookies:
            headers["Cookie"] = "; ".join(f"{k}={v}" for k, v in cookies.items())

        logger.info(
            "CDP connection prepared — ws=%s cookies=%d (redirected from %s)",
            ws_url,
            len(cookies),
            cdp_proxy_url,
        )
        return ws_url, headers

    def open_url(self, url: str, port: int | None = None) -> dict:
        """Open *url* in a new Chrome tab via CDP."""
        port = self._resolve_cdp_port(port)
        if self._is_qemu():
            # The CDP endpoint sits behind the two-tier sims proxy: the
            # {job}--{port} subdomain 302s to the base host to complete the
            # routing/cookie dance (see prepare_cdp_connection). A bare PUT that
            # blindly follows that 302 lands on web routing and 405s — and a
            # target URL carrying its own query (e.g. ?_plato_router_target=...)
            # makes it worse by re-triggering web routing. So prime the cookie +
            # resolve the base host with GET /json/version first, then PUT there.
            cdp_proxy_url = self.get_cdp_url(port)
            with httpx.Client(follow_redirects=True, timeout=30) as tmp:
                primer = tmp.get(f"{cdp_proxy_url}/json/version")
                primer.raise_for_status()
                base_url = f"{primer.url.scheme}://{primer.url.host}"
                response = tmp.put(f"{base_url}/json/new?{url}")
                response.raise_for_status()
                return response.json()

        result = self.bash(BashRequest(command=f"curl -s --max-time 5 -X PUT 'http://localhost:{port}/json/new?{url}'"))
        try:
            return _json.loads(result.output or "")
        except _json.JSONDecodeError:
            return {"url": url, "raw": (result.output or "").strip()}

    def list_tabs(self, port: int | None = None) -> list[dict]:
        """Return the list of open Chrome tabs from CDP."""
        port = self._resolve_cdp_port(port)
        if self._is_qemu():
            with httpx.Client(follow_redirects=True, timeout=30) as tmp:
                response = tmp.get(f"{self.get_cdp_url(port)}/json/list")
                response.raise_for_status()
                payload = response.json()
            if isinstance(payload, list):
                return payload
            return []

        result = self.bash(BashRequest(command=f"curl -s --max-time 5 http://localhost:{port}/json/list"))
        try:
            return _json.loads(result.output or "[]")
        except _json.JSONDecodeError:
            return []

    def login(
        self,
        session: Any,
        cdp_port: int | None = None,
        retries: int = 3,
        retry_delay: float = 2.0,
    ) -> list[str]:
        """Open simulator URLs in the VM's Chrome and run login flows.

        Connects Playwright to Chrome via CDP, then for each simulator env
        in *session* that has an ``artifact_id`` (i.e. not the desktop
        runtime), navigates to its public URL and executes the ``login``
        flow with retries.

        Follows the same pattern as
        ``CuaBenchmarkWorld._run_v2_login_flow`` and
        ``Session.login``, but targets Chrome running inside the VM
        rather than a local browser.

        Args:
            session: A ``plato.v2.sync.Session`` with ``.envs``,
                ``._http``, and ``._api_key``.
            cdp_port: Chrome DevTools Protocol port on the VM.
            retries: Number of retry attempts per login flow.
            retry_delay: Seconds between retries.

        Returns:
            List of environment aliases that were successfully logged in.

        Raises:
            ImportError: If playwright is not installed.
            RuntimeError: If a public URL or flows cannot be fetched, or
                if login fails after all retries.
        """
        import importlib.util

        if importlib.util.find_spec("playwright") is None:
            raise ImportError("login() requires playwright. Install with: pip install playwright")

        from playwright.sync_api import sync_playwright

        from plato._generated.api.v2.jobs import get_flows as jobs_get_flows
        from plato._generated.api.v2.jobs import public_url as jobs_public_url
        from plato._generated.models import Flow
        from plato.v2.sync.flow_executor import FlowExecutor

        self.ensure_chrome_cdp(cdp_port)
        ws_url, cdp_headers = self.prepare_cdp_connection(cdp_port)
        logger.info("Connecting Playwright to CDP: %s", ws_url)

        pages_logged_in: list[str] = []

        with sync_playwright() as pw:
            browser = pw.chromium.connect_over_cdp(ws_url, headers=cdp_headers)
            default_context = browser.contexts[0]
            logger.info(
                "Connected – %d existing page(s): %s",
                len(default_context.pages),
                [p.url for p in default_context.pages],
            )

            # Pick an about:blank page or create one as the starting tab
            first_page = None
            for p in default_context.pages:
                if not p.is_closed() and (p.url or "") == "about:blank":
                    first_page = p
                    break
            if first_page is None:
                first_page = default_context.new_page()
                first_page.goto("about:blank")

            my_job_id = _extract_job_id(self._base_url)
            login_count = 0
            for env in session.envs:
                if not getattr(env, "artifact_id", None):
                    logger.info("Skipping login for %s (no artifact_id)", env.alias)
                    continue
                if getattr(env, "job_id", None) == my_job_id:
                    logger.info("Skipping login for %s (desktop env)", env.alias)
                    continue
                if is_proctor_env(env):
                    logger.info("Skipping login for %s (proctor service)", env.alias)
                    continue

                page = first_page if login_count == 0 else default_context.new_page()
                login_count += 1

                # Get public URL
                public_url_result = jobs_public_url.sync(
                    client=session._http,
                    job_id=env.job_id,
                    x_api_key=session._api_key,
                )
                if public_url_result.error or not public_url_result.url:
                    raise RuntimeError(f"Failed to get public URL for {env.alias}: {public_url_result.error}")

                public_url = public_url_result.url
                logger.info("Navigating to %s for %s", public_url, env.alias)
                print(f"  [{env.alias}] Navigating to {public_url}", flush=True)
                page.goto(public_url, timeout=120_000)
                print(f"  [{env.alias}] Page loaded: {page.url}", flush=True)

                # Fetch flows
                try:
                    flows_response = jobs_get_flows.sync(
                        client=session._http,
                        job_id=env.job_id,
                        x_api_key=session._api_key,
                    )
                except Exception as exc:
                    raise RuntimeError(f"Failed to get flows for {env.alias}: {exc}") from exc

                if not flows_response:
                    raise RuntimeError(f"No flows found for {env.alias}")

                flows_list = [Flow.model_validate(f) for f in flows_response]
                login_flow = next((f for f in flows_list if f.name == "login"), None)
                if not login_flow:
                    raise RuntimeError(f"No 'login' flow found for {env.alias}")

                flow_executor = FlowExecutor(page, login_flow, log=logger)

                last_error: Exception | None = None
                for attempt in range(1 + retries):
                    try:
                        flow_executor.execute()
                        last_error = None
                        break
                    except Exception as exc:
                        last_error = exc
                        if attempt < retries:
                            print(
                                f"  [{env.alias}] Login attempt {attempt + 1}/{1 + retries} "
                                f"failed, retrying in {retry_delay}s: {exc}",
                                flush=True,
                            )
                            time.sleep(retry_delay)
                            page.goto(public_url, timeout=120_000)

                if last_error is not None:
                    raise RuntimeError(
                        f"Login failed for {env.alias} after {1 + retries} attempts: {last_error}"
                    ) from last_error

                print(f"  [{env.alias}] Login successful", flush=True)
                pages_logged_in.append(env.alias)

            # Clean up stray about:blank tabs and focus the last real page
            target_page = None
            for p in list(default_context.pages):
                if p.is_closed():
                    continue
                if p.url and p.url != "about:blank" and not p.url.startswith("chrome://"):
                    target_page = p

            for p in list(default_context.pages):
                if not p.is_closed() and p != target_page and p.url == "about:blank":
                    try:
                        p.close()
                    except Exception:
                        pass

            if target_page:
                try:
                    target_page.bring_to_front()
                except Exception:
                    pass

        logger.info("Login complete for: %s", pages_logged_in)
        return pages_logged_in

    # -- /CDP helpers ---------------------------------------------------------

    def close(self) -> None:
        """Close the client."""
        self._closed = True
        self._client.close()

    def __enter__(self) -> Client:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def __del__(self) -> None:
        if not self._closed:
            warnings.warn(
                f"{self.__class__.__name__} was not closed. Use 'with' statement or call 'client.close()'",
                ResourceWarning,
                stacklevel=2,
            )

    @classmethod
    def from_env(cls, **kwargs: Any) -> Client:
        """Create client from environment variables.

        Reads {ENV_PREFIX}_BASE_URL and auth credentials.

        Args:
            **kwargs: Additional arguments passed to Client.__init__

        Returns:
            Configured Client instance

        Raises:
            ValueError: If {ENV_PREFIX}_BASE_URL is not set
        """
        base_url, env_headers = _get_env_config()
        if not base_url:
            raise ValueError(f"{ENV_PREFIX}_BASE_URL environment variable is required")

        # Merge env headers with any provided headers
        headers = kwargs.pop("headers", None) or {}
        headers = {**env_headers, **headers}

        return cls(base_url=base_url, headers=headers, **kwargs)

    @classmethod
    def create(
        cls,
        base_url: str | None = None,
        api_token: str | None = None,
        **kwargs: Any,
    ) -> Client:
        """Create an authenticated client.

        Args:
            base_url: Base URL (uses {ENV_PREFIX}_BASE_URL if not provided)
            api_token: API token (uses default if not provided)
            **kwargs: Additional arguments passed to Client.__init__

        Returns:
            Authenticated Client instance
        """
        base_url = base_url or os.environ.get(f"{ENV_PREFIX}_BASE_URL")
        if not base_url:
            raise ValueError(f"base_url required or set {ENV_PREFIX}_BASE_URL")

        token = api_token or os.environ.get(f"{ENV_PREFIX}_API_TOKEN")

        headers = kwargs.pop("headers", None) or {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        return cls(base_url=base_url, headers=headers, **kwargs)

    @classmethod
    def from_environment(cls, environment: Any, **kwargs: Any) -> Client:
        """Create a client from a Plato v2 Environment object.

        Args:
            environment: A plato.v2 Environment with a .job_id attribute.
            **kwargs: Additional arguments passed to Client.__init__
        """
        provider = getattr(environment, "provider", None)
        gateway = _deployment_sims_gateway(_api_base_url_from_environment(environment))
        base_url = _base_url_from_job_id(environment.job_id, gateway_host=gateway)
        return cls(base_url=base_url, provider=provider, **kwargs)


class AsyncClient:
    """Async HTTP client for Desktop Agent API."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 120.0,
        headers: dict[str, str] | None = None,
        max_retries: int = 3,
        retry_on_status: tuple[int, ...] = (429, 500, 502, 503, 504),
        on_request: Callable[[httpx.Request], None] | None = None,
        on_response: Callable[[httpx.Response], None] | None = None,
        provider: str | None = None,
        cdp_port: int | None = None,
        **kwargs: Any,
    ):
        """Initialize the async HTTP client."""
        self._base_url = base_url.rstrip("/")
        # Always include Accept header for JSON APIs
        self._headers = {"Accept": "application/json", **(headers or {})}
        self._max_retries = max_retries
        self._retry_on_status = retry_on_status
        self._provider = provider
        self._cdp_port = cdp_port if cdp_port is not None else CDP_PORT
        self._closed = False

        event_hooks: dict[str, list[Callable]] = {"request": [], "response": []}
        if on_request:
            event_hooks["request"].append(on_request)
        if on_response:
            event_hooks["response"].append(on_response)

        self._timeout = timeout
        self._initialized = False
        self._screensaver_kicked = False
        self._screensaver_task: asyncio.Future[None] | None = None
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=timeout,
            headers=self._headers,
            follow_redirects=False,
            limits=_NO_KEEPALIVE,
            event_hooks=event_hooks if any(event_hooks.values()) else None,
            **kwargs,
        )

    def _resolve_cdp_port(self, port: int | None) -> int:
        return self._cdp_port if port is None else port

    def _is_qemu(self) -> bool:
        return self._provider == "qemu"

    def _kick_screensaver(self) -> None:
        """Async version of :meth:`Client._kick_screensaver`.

        Schedules a fire-and-forget task on the running loop (``_ensure_init``
        is always awaited, so a loop exists). Skipped on Windows/QEMU and after
        the first invocation; all errors are swallowed.
        """
        if self._screensaver_kicked or self._is_qemu():
            return
        self._screensaver_kicked = True

        async def _run() -> None:
            try:
                await self.bash(BashRequest(command=_DISABLE_SCREENSAVER_CMD))
            except Exception as exc:  # best-effort: never surface to the caller
                logger.debug("screensaver disable failed (ignored): %s", exc)

        try:
            self._screensaver_task = asyncio.ensure_future(_run())
        except RuntimeError:  # no running loop — nothing to schedule onto
            logger.debug("no running loop; skipping screensaver disable")

    async def _ensure_init(self) -> None:
        """Complete the sims proxy redirect/cookie dance on first use.

        See :meth:`Client._ensure_init` for details.
        """
        if self._initialized:
            return

        response = await self._client.request(method="GET", url="/status")
        if response.status_code not in (301, 302, 307, 308):
            self._initialized = True
            self._kick_screensaver()
            return

        location = response.headers.get("location", "")

        if "_plato/init" in location:
            logger.debug("Performing _plato/init redirect dance")
            async with httpx.AsyncClient(follow_redirects=True, timeout=self._timeout) as tmp:
                await tmp.get(location)
                cookies = dict(tmp.cookies)
            parsed = urlparse(location)
            new_base_url = f"{parsed.scheme}://{parsed.hostname}"
        else:
            logger.debug("Performing sims routing cookie dance")
            async with httpx.AsyncClient(follow_redirects=True, timeout=self._timeout) as tmp:
                resp = await tmp.get(f"{self._base_url}/status")
                cookies = dict(tmp.cookies)
            new_base_url = f"https://{resp.url.host}"

        self._initialized = True
        old_client = self._client
        self._client = httpx.AsyncClient(
            base_url=new_base_url,
            timeout=self._timeout,
            headers=self._headers,
            follow_redirects=False,
            limits=_NO_KEEPALIVE,
            cookies=cookies,
        )
        await old_client.aclose()
        # Client is now reconfigured/stable — safe to fire the background task.
        self._kick_screensaver()

    @property
    def httpx(self) -> httpx.AsyncClient:
        """Access the underlying httpx client."""
        return self._client

    @property
    def max_retries(self) -> int:
        """Maximum number of retry attempts."""
        return self._max_retries

    @property
    def retry_on_status(self) -> tuple[int, ...]:
        """HTTP status codes that trigger a retry."""
        return self._retry_on_status

    def get_liveview_url(self) -> str:
        """Get the noVNC liveview URL for this VM."""
        job_id = _extract_job_id(self._base_url)
        gateway = _gateway_from_base_url(self._base_url)
        return f"https://{job_id}--{LIVEVIEW_PORT}.{gateway}?resize=scale&autoconnect=true"

    async def bash(self, body: BashRequest) -> ToolResult:
        """Execute a shell command."""
        await self._ensure_init()
        return await _bash_async(self._client, body=body)

    async def _try_bash(self, command: str) -> ToolResult | None:
        """Async version of :meth:`Client._try_bash` — ``None`` on transport error."""
        try:
            return await self.bash(BashRequest(command=command))
        except Exception as exc:
            logger.debug("bash call failed (tolerated, will retry): %s", exc)
            return None

    async def computer(self, body: ComputerRequest) -> ToolResult:
        """Execute computer actions (mouse, keyboard, screenshot)."""
        await self._ensure_init()
        return await _computer_async(self._client, body=body)

    async def edit(self, body: EditRequest) -> ToolResult:
        """File operations (view, create, str_replace, insert, undo_edit)."""
        await self._ensure_init()
        return await _edit_async(self._client, body=body)

    async def status(self) -> StatusResponse:
        """Health check and display info."""
        await self._ensure_init()
        return await _status_async(self._client)

    async def set_timezone_offset(self, utc_offset: int, timeout: int = 30) -> ToolResult:
        """Async version of :meth:`Client.set_timezone_offset`."""
        command = _windows_set_timezone_cmd(utc_offset) if self._is_qemu() else _ubuntu_set_timezone_cmd(utc_offset)
        return await self.bash(BashRequest(command=command, timeout=timeout))

    # -- CDP helpers ----------------------------------------------------------

    def get_cdp_url(self, port: int | None = None) -> str:
        """Return the sims proxy URL for the Chrome CDP port."""
        port = self._resolve_cdp_port(port)
        job_id = _extract_job_id(self._base_url)
        gateway = _gateway_from_base_url(self._base_url)
        return f"https://{job_id}--{port}.{gateway}"

    async def ensure_chrome_cdp(self, port: int | None = None, timeout: int = 60) -> str:
        """Ensure Chrome CDP is reachable on *port* inside the VM.

        See :meth:`Client.ensure_chrome_cdp` for details.
        """

        port = self._resolve_cdp_port(port)
        if self._is_qemu():
            await self._ensure_init()
            # Windows Chrome is launched directly over the agent's /bash
            # endpoint (PowerShell) instead of POST /browser/start: the baked
            # launcher /browser/start runs lacks --ignore-certificate-errors,
            # which is required because snapshots resume with a frozen clock
            # that predates the sims proxy's rotating TLS cert (notBefore),
            # making every page load fail with ERR_CERT_DATE_INVALID (see
            # _windows_chrome_launch_cmd). Structure mirrors the ubuntu branch
            # below: probe the loopback CDP port, kill + relaunch Chrome if
            # unresponsive, then poll until CDP answers. Once up, CDP is
            # reachable over the sims proxy on 9224 (nginx Host rewrite),
            # same as ubuntu. Every /bash call here is failure-tolerant
            # (_try_bash): on a cold boot the agent's post-logon task may not
            # be listening yet, so transient 502s/timeouts count as "not
            # ready" and we keep retrying until the deadline — matching the
            # old /browser/start retry loop.
            effective_timeout = max(timeout, 90)
            internal_port = 9225 if port == 9224 else port
            cdp_probe = _windows_cdp_probe_cmd(internal_port)
            deadline = time.monotonic() + effective_timeout

            check = await self._try_bash(cdp_probe)
            if check is None:
                logger.debug("First bash call failed; warming up client via status()")
                try:
                    await self.status()
                except Exception as exc:
                    logger.debug("status() warmup failed (tolerated): %s", exc)
                check = await self._try_bash(cdp_probe)
            if check is not None and _CDP_UP in (check.output or ""):
                logger.info("Windows Chrome CDP already responding on port %s", port)
                return self.get_cdp_url(port)

            logger.info("Waiting for Windows Chrome CDP on port %s ...", port)
            for _ in range(5):
                await asyncio.sleep(1)
                probe = await self._try_bash(cdp_probe)
                if probe is not None and _CDP_UP in (probe.output or ""):
                    logger.info("Windows Chrome CDP ready on port %s", port)
                    return self.get_cdp_url(port)

            # Kill + relaunch retry until the deadline too: the probes above
            # failing may just mean the agent itself is still coming up.
            logger.info("Windows Chrome CDP unresponsive; restarting Chrome")
            launch_cmd = _windows_chrome_launch_cmd(internal_port)
            launched = False
            last_err = ""
            while time.monotonic() < deadline:
                kill = await self._try_bash(_WINDOWS_CHROME_KILL_CMD)
                launch = await self._try_bash(launch_cmd) if kill is not None else None
                if launch is not None and not launch.error:
                    launched = True
                    break
                last_err = launch.error if launch is not None and launch.error else "agent unreachable"
                await asyncio.sleep(2)
            if not launched:
                raise TimeoutError(
                    f"Windows Chrome CDP not ready on port {port} after {effective_timeout}s: "
                    f"could not restart Chrome ({last_err})"
                )

            while time.monotonic() < deadline:
                await asyncio.sleep(2)
                probe = await self._try_bash(cdp_probe)
                if probe is not None and _CDP_UP in (probe.output or ""):
                    logger.info("Windows Chrome CDP ready on port %s after restart", port)
                    return self.get_cdp_url(port)
                last_err = (probe.output or "").strip() if probe is not None else "agent unreachable"
            raise TimeoutError(
                f"Windows Chrome CDP not ready on port {port} after {effective_timeout}s. Last probe: {last_err}"
            )

        cdp_probe = f"curl -sf --max-time 2 http://localhost:{port}/json/version 2>/dev/null || echo __NO_CDP__"
        try:
            check = await self.bash(BashRequest(command=cdp_probe))
        except Exception:
            logger.debug("First bash call failed; warming up client via status()")
            await self.status()
            check = await self.bash(BashRequest(command=cdp_probe))
        if "__NO_CDP__" not in (check.output or ""):
            logger.info("Chrome CDP already responding on port %s", port)
            return self.get_cdp_url(port)

        logger.info("Waiting for Chrome CDP on port %s ...", port)
        for _ in range(5):
            await asyncio.sleep(1)
            probe = await self.bash(BashRequest(command=cdp_probe))
            if "__NO_CDP__" not in (probe.output or ""):
                logger.info("Chrome CDP ready on port %s", port)
                return self.get_cdp_url(port)

        logger.info("Chrome CDP unresponsive; restarting Chrome")
        await self.bash(BashRequest(command="pkill -9 -f 'chrome' 2>/dev/null; sleep 2"))

        chrome_internal_port = 9225 if port == 9224 else port
        await self.bash(
            BashRequest(
                command=(
                    f"DISPLAY=:0 nohup google-chrome-stable "
                    f"--no-sandbox --disable-gpu --disable-dev-shm-usage "
                    f"--disable-features=PasswordManager,PasswordManagerOnboarding,PasswordLeakDetection "
                    f"--no-first-run --no-default-browser-check --disable-default-apps "
                    f"--disable-popup-blocking --disable-translate --disable-infobars "
                    # Snapshots resume with a frozen clock that can predate the
                    # sims proxy's rotating TLS cert -> ERR_CERT_DATE_INVALID.
                    f"--ignore-certificate-errors "
                    f"--test-type --start-maximized --window-size=1280,720 "
                    f"--user-data-dir=/tmp/chrome-cdp-profile "
                    f"--remote-debugging-port={chrome_internal_port} "
                    f"about:blank >/dev/null 2>&1 &"
                )
            )
        )

        deadline = time.monotonic() + timeout
        last_err = ""
        while time.monotonic() < deadline:
            await asyncio.sleep(2)
            probe = await self.bash(BashRequest(command=cdp_probe))
            if "__NO_CDP__" not in (probe.output or ""):
                logger.info("Chrome CDP ready on port %s after restart", port)
                return self.get_cdp_url(port)
            last_err = (probe.output or "").strip()

        raise TimeoutError(f"Chrome CDP not ready on port {port} after {timeout}s. Last probe: {last_err}")

    async def get_cdp_ws_url(self, port: int | None = None) -> str:
        """Return a Playwright-ready WebSocket URL for the VM's Chrome CDP.

        See :meth:`Client.get_cdp_ws_url` for details.
        """
        ws_url, _ = await self.prepare_cdp_connection(port)
        return ws_url

    async def prepare_cdp_connection(self, port: int | None = None) -> tuple[str, dict[str, str]]:
        """Async version of :meth:`Client.prepare_cdp_connection`."""
        port = self._resolve_cdp_port(port)
        cdp_proxy_url = self.get_cdp_url(port)

        async with httpx.AsyncClient(follow_redirects=True, timeout=30) as tmp:
            resp = await tmp.get(f"{cdp_proxy_url}/json/version")
            resp.raise_for_status()
            cookies = dict(tmp.cookies)
            version_info = resp.json()

        ws_host = resp.url.host
        if ws_host is None:
            raise RuntimeError(f"Failed to resolve CDP proxy host from {resp.url}")

        ws_path = urlparse(version_info["webSocketDebuggerUrl"]).path
        ws_url = f"wss://{ws_host}{ws_path}"

        headers: dict[str, str] = {}
        if cookies:
            headers["Cookie"] = "; ".join(f"{k}={v}" for k, v in cookies.items())

        logger.info(
            "CDP connection prepared — ws=%s cookies=%d (redirected from %s)",
            ws_url,
            len(cookies),
            cdp_proxy_url,
        )
        return ws_url, headers

    async def open_url(self, url: str, port: int | None = None) -> dict:
        """Open *url* in a new Chrome tab via CDP."""
        port = self._resolve_cdp_port(port)
        if self._is_qemu():
            # See the sync open_url for why we prime the cookie / base host
            # first instead of firing a bare PUT that follows the proxy 302.
            cdp_proxy_url = self.get_cdp_url(port)
            async with httpx.AsyncClient(follow_redirects=True, timeout=30) as tmp:
                primer = await tmp.get(f"{cdp_proxy_url}/json/version")
                primer.raise_for_status()
                base_url = f"{primer.url.scheme}://{primer.url.host}"
                response = await tmp.put(f"{base_url}/json/new?{url}")
                response.raise_for_status()
                return response.json()

        result = await self.bash(
            BashRequest(command=f"curl -s --max-time 5 -X PUT 'http://localhost:{port}/json/new?{url}'")
        )
        try:
            return _json.loads(result.output or "")
        except _json.JSONDecodeError:
            return {"url": url, "raw": (result.output or "").strip()}

    async def list_tabs(self, port: int | None = None) -> list[dict]:
        """Return the list of open Chrome tabs from CDP."""
        port = self._resolve_cdp_port(port)
        if self._is_qemu():
            async with httpx.AsyncClient(follow_redirects=True, timeout=30) as tmp:
                response = await tmp.get(f"{self.get_cdp_url(port)}/json/list")
                response.raise_for_status()
                payload = response.json()
            if isinstance(payload, list):
                return payload
            return []

        result = await self.bash(BashRequest(command=f"curl -s --max-time 5 http://localhost:{port}/json/list"))
        try:
            return _json.loads(result.output or "[]")
        except _json.JSONDecodeError:
            return []

    async def login(
        self,
        session: Any,
        cdp_port: int | None = None,
        retries: int = 3,
        retry_delay: float = 2.0,
    ) -> list[str]:
        """Async version of :meth:`Client.login`.

        See the sync docstring for full details.
        """
        import importlib.util

        from plato._generated.api.v2.jobs import get_flows as jobs_get_flows
        from plato._generated.api.v2.jobs import public_url as jobs_public_url
        from plato._generated.models import Flow
        from plato.v2.async_.flow_executor import FlowExecutor

        # Check playwright before starting Chrome CDP — ensure_chrome_cdp can
        # poll a remote VM for up to 90s on qemu, so fail fast if the import
        # is missing (mirrors the sync login ordering).
        if importlib.util.find_spec("playwright") is None:
            raise ImportError("login() requires playwright. Install with: pip install playwright")

        from playwright.async_api import async_playwright

        await self.ensure_chrome_cdp(cdp_port)

        pages_logged_in: list[str] = []

        ws_url, cdp_headers = await self.prepare_cdp_connection(cdp_port)
        logger.info("Connecting Playwright to CDP: %s", ws_url)

        async with async_playwright() as pw:
            browser = await pw.chromium.connect_over_cdp(ws_url, headers=cdp_headers)
            default_context = browser.contexts[0]
            logger.info(
                "Connected – %d existing page(s): %s",
                len(default_context.pages),
                [p.url for p in default_context.pages],
            )

            first_page = None
            for p in default_context.pages:
                if not p.is_closed() and (p.url or "") == "about:blank":
                    first_page = p
                    break
            if first_page is None:
                first_page = await default_context.new_page()
                await first_page.goto("about:blank")

            my_job_id = _extract_job_id(self._base_url)
            login_count = 0
            for env in session.envs:
                if not getattr(env, "artifact_id", None):
                    logger.info("Skipping login for %s (no artifact_id)", env.alias)
                    continue
                if getattr(env, "job_id", None) == my_job_id:
                    logger.info("Skipping login for %s (desktop env)", env.alias)
                    continue
                if is_proctor_env(env):
                    logger.info("Skipping login for %s (proctor service)", env.alias)
                    continue

                page = first_page if login_count == 0 else await default_context.new_page()
                login_count += 1

                public_url_result = await jobs_public_url.asyncio(
                    client=session._http,
                    job_id=env.job_id,
                    x_api_key=session._api_key,
                )
                if public_url_result.error or not public_url_result.url:
                    raise RuntimeError(f"Failed to get public URL for {env.alias}: {public_url_result.error}")

                public_url = public_url_result.url
                logger.info("Navigating to %s for %s", public_url, env.alias)
                await page.goto(public_url, timeout=120_000)

                try:
                    flows_response = await jobs_get_flows.asyncio(
                        client=session._http,
                        job_id=env.job_id,
                        x_api_key=session._api_key,
                    )
                except Exception as exc:
                    raise RuntimeError(f"Failed to get flows for {env.alias}: {exc}") from exc

                if not flows_response:
                    raise RuntimeError(f"No flows found for {env.alias}")

                flows_list = [Flow.model_validate(f) for f in flows_response]
                login_flow = next((f for f in flows_list if f.name == "login"), None)
                if not login_flow:
                    raise RuntimeError(f"No 'login' flow found for {env.alias}")

                flow_executor = FlowExecutor(page, login_flow, log=logger)

                last_error: Exception | None = None
                for attempt in range(1 + retries):
                    try:
                        await flow_executor.execute()
                        last_error = None
                        break
                    except Exception as exc:
                        last_error = exc
                        if attempt < retries:
                            logger.warning(
                                "Login flow failed for %s (attempt %d/%d), retrying in %.1fs: %s",
                                env.alias,
                                attempt + 1,
                                1 + retries,
                                retry_delay,
                                exc,
                            )
                            await asyncio.sleep(retry_delay)
                            await page.goto(public_url, timeout=120_000)

                if last_error is not None:
                    raise RuntimeError(
                        f"Login failed for {env.alias} after {1 + retries} attempts: {last_error}"
                    ) from last_error

                logger.info("Login successful for %s", env.alias)
                pages_logged_in.append(env.alias)

            target_page = None
            for p in list(default_context.pages):
                if p.is_closed():
                    continue
                if p.url and p.url != "about:blank" and not p.url.startswith("chrome://"):
                    target_page = p

            for p in list(default_context.pages):
                if not p.is_closed() and p != target_page and p.url == "about:blank":
                    try:
                        await p.close()
                    except Exception:
                        pass

            if target_page:
                try:
                    await target_page.bring_to_front()
                except Exception:
                    pass

        logger.info("Login complete for: %s", pages_logged_in)
        return pages_logged_in

    # -- /CDP helpers ---------------------------------------------------------

    async def close(self) -> None:
        """Close the client."""
        self._closed = True
        await self._client.aclose()

    async def __aenter__(self) -> AsyncClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    def __del__(self) -> None:
        if not self._closed:
            warnings.warn(
                f"{self.__class__.__name__} was not closed. Use 'async with' statement or call 'await client.close()'",
                ResourceWarning,
                stacklevel=2,
            )

    @classmethod
    def from_env(cls, **kwargs: Any) -> AsyncClient:
        """Create client from environment variables."""
        base_url, env_headers = _get_env_config()
        if not base_url:
            raise ValueError(f"{ENV_PREFIX}_BASE_URL environment variable is required")

        headers = kwargs.pop("headers", None) or {}
        headers = {**env_headers, **headers}

        return cls(base_url=base_url, headers=headers, **kwargs)

    @classmethod
    async def create(
        cls,
        base_url: str | None = None,
        api_token: str | None = None,
        **kwargs: Any,
    ) -> AsyncClient:
        """Create an authenticated client."""
        base_url = base_url or os.environ.get(f"{ENV_PREFIX}_BASE_URL")
        if not base_url:
            raise ValueError(f"base_url required or set {ENV_PREFIX}_BASE_URL")

        token = api_token or os.environ.get(f"{ENV_PREFIX}_API_TOKEN")

        headers = kwargs.pop("headers", None) or {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        return cls(base_url=base_url, headers=headers, **kwargs)

    @classmethod
    def from_environment(cls, environment: Any, **kwargs: Any) -> AsyncClient:
        """Create a client from a Plato v2 Environment object.

        Args:
            environment: A plato.v2 Environment with a .job_id attribute.
            **kwargs: Additional arguments passed to AsyncClient.__init__
        """
        provider = getattr(environment, "provider", None)
        gateway = _deployment_sims_gateway(_api_base_url_from_environment(environment))
        base_url = _base_url_from_job_id(environment.job_id, gateway_host=gateway)
        return cls(base_url=base_url, provider=provider, **kwargs)
