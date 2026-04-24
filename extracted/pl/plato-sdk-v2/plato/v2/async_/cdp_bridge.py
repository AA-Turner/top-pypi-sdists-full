"""Shared-chromium CDP bridge for agent-browser login flows.

agent-browser's own chromium launches with ``--remote-debugging-pipe`` so it
isn't Playwright-connectable. To keep running the Plato-hosted Playwright
login flows against an agent-browser-managed session, we spawn chromium
ourselves on the remote host with ``--remote-debugging-port``, SSH-forward
the port, let Playwright drive login through :class:`FlowExecutor`, then
hand the same chromium to an ``agent-browser --session <alias>`` daemon via
its ``connect <port>`` subcommand. The daemon inherits the authenticated
state — cookies, storage, open tabs — because both clients attach to the
same browser over CDP.

Only ``shared_cdp_chromium`` is public. Everything else is internal.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import shlex
from collections.abc import AsyncIterator
from pathlib import Path
from urllib.parse import urlparse, urlunparse

import httpx

from plato.utils.subprocess import build_ssh_command
from plato.v2.async_.flow_backends import RunCmd

logger = logging.getLogger(__name__)

_CHROMIUM_READY_TIMEOUT_S = 30.0
_CHROMIUM_READY_POLL_S = 0.5
_TUNNEL_READY_TIMEOUT_S = 8.0
_TUNNEL_READY_POLL_S = 0.2

CDP_PORT_BASE = 9320
"""Default base port for per-env CDP chromium. Env at index ``i`` uses
``CDP_PORT_BASE + i``. Kept low-enough to avoid ephemeral-port clashes and
high-enough to not collide with app defaults."""


async def _resolve_chrome_bin(run_cmd: RunCmd) -> str:
    """Resolve a chromium binary path on the remote host.

    Priority order, biased toward what's most reliably present on Plato
    agent images:

    1. Playwright's browser cache — ``$PLAYWRIGHT_BROWSERS_PATH`` when
       set (it typically is on agent images, e.g. ``/opt/playwright-
       browsers`` on claude-code via Dockerfile ``ENV``), then the same
       well-known path as a fallback since non-interactive SSH doesn't
       inherit container-level env vars, then the default user cache at
       ``~/.cache/ms-playwright``. Playwright pins a specific chromium
       version via its Python package, so this is the most deterministic
       source.
    2. agent-browser's private browser cache (``~/.agent-browser/
       browsers/chrome-*``) in case a future image ships only that.
    3. System ``google-chrome`` / ``chromium`` as a last resort.

    ``agent-browser --session <alias> connect <port>`` *attaches* to
    whichever chromium we spawn via CDP — it does not launch its own
    browser. So the binary choice here is about "what runs" on the
    image, not about matching any other chromium's version.
    """
    # ``PLAYWRIGHT_BROWSERS_PATH`` is typically set as a Dockerfile ``ENV``
    # (e.g. ``/opt/playwright-browsers`` on the claude-code agent image),
    # but non-interactive SSH shells don't inherit container-level env
    # vars. Fall back to the well-known path used by the agent base images
    # plus the default user cache location.
    script = r"""
for dir in "${PLAYWRIGHT_BROWSERS_PATH:-}" /opt/playwright-browsers "$HOME/.cache/ms-playwright"; do
  [ -n "$dir" ] || continue
  for cand in "$dir"/chromium-*/chrome-linux/chrome \
              "$dir"/chromium-*/chrome-linux64/chrome \
              "$dir"/chromium_headless_shell-*/chrome-linux/headless_shell; do
    if [ -x "$cand" ]; then printf '%s' "$cand"; exit 0; fi
  done
done
# agent-browser's own cache uses either ``chrome-<ver>/chrome`` (flat,
# recent) or ``chrome-<ver>/chrome-linux64/chrome`` (nested, older/other
# archives) depending on how its installer extracted the zip. Check both,
# matching the dual-layout probe in ``cli/src/install.rs::chrome_binary_in_dir``.
for cand in "$HOME"/.agent-browser/browsers/chrome-*/chrome \
            "$HOME"/.agent-browser/browsers/chrome-*/chrome-linux64/chrome \
            "$HOME"/.agent-browser/browsers/chrome-*/chrome-linux/chrome; do
  if [ -x "$cand" ]; then printf '%s' "$cand"; exit 0; fi
done
for name in google-chrome google-chrome-stable chromium chromium-browser; do
  p=$(command -v "$name" 2>/dev/null) || true
  if [ -n "$p" ]; then printf '%s' "$p"; exit 0; fi
done
# Nothing matched. Dump an inventory to stderr so a future failure tells us
# exactly what's present instead of "rc=1 stderr=''".
{
  echo "no chromium found; inventory follows:"
  echo "  HOME=$HOME PLAYWRIGHT_BROWSERS_PATH=${PLAYWRIGHT_BROWSERS_PATH:-UNSET}"
  for d in "${PLAYWRIGHT_BROWSERS_PATH:-}" /opt/playwright-browsers \
           "$HOME/.cache/ms-playwright" "$HOME/.agent-browser/browsers"; do
    [ -n "$d" ] || continue
    if [ -d "$d" ]; then
      echo "  $d:"
      ls -la "$d" 2>&1 | sed 's/^/    /' | head -20
    else
      echo "  $d: MISSING"
    fi
  done
} 1>&2
exit 1
"""
    rc, out, err = await run_cmd(["bash", "-c", script])
    resolved = out.strip()
    if rc != 0 or not resolved:
        raise RuntimeError(
            "Could not locate a chromium binary on the remote host. Checked "
            "Playwright's cache ($PLAYWRIGHT_BROWSERS_PATH, "
            "/opt/playwright-browsers, ~/.cache/ms-playwright), agent-browser's "
            "cache (~/.agent-browser/browsers/chrome-*/{chrome,chrome-linux64/chrome,"
            "chrome-linux/chrome}), and system google-chrome/chromium. "
            f"rc={rc} stdout={out[-200:]!r} stderr={err[-600:]!r}"
        )
    return resolved


async def kill_stale_chromium(
    run_cmd: RunCmd,
    *,
    port: int,
    profile_dir: str,
    log: logging.Logger | None = None,
) -> None:
    """Kill any chromium on ``port`` or rooted in ``profile_dir`` on the remote.

    Warm-pool VMs can carry over leftover chromium from a previous session
    — either bound to the same CDP port (blocks our spawn) or squatting on
    the same user-data-dir (locks the profile). Both are fatal, so clean
    them up idempotently before launching.

    Matches by ``--remote-debugging-port=<port>`` and ``--user-data-dir=<dir>``
    on the chromium cmdline. Both patterns are unique enough not to false-
    positive against other workloads.
    """
    active_log = log or logger
    profile_dir_clean = profile_dir.rstrip("/")
    script = (
        f"pkill -9 -f 'remote-debugging-port={port}' 2>/dev/null || true; "
        f"pkill -9 -f 'user-data-dir={profile_dir_clean}' 2>/dev/null || true; "
        f"sleep 0.2; "
        f"rm -rf {shlex.quote(profile_dir_clean)} 2>/dev/null || true"
    )
    rc, _, err = await run_cmd(["bash", "-c", script])
    if rc != 0:
        active_log.debug(
            "stale-chromium cleanup on :%d rc=%d (non-fatal): %s",
            port,
            rc,
            err[-200:] if err else "",
        )


async def _spawn_chromium(
    run_cmd: RunCmd,
    *,
    chrome_bin: str,
    port: int,
    profile_dir: str,
    log: logging.Logger,
) -> None:
    """Spawn chromium detached on the remote and wait for CDP readiness.

    SSH keeps the session channel open as long as any descendant holds the
    stdout/stderr pipes, so ``nohup … &`` alone blocks until its own
    timeout. Wrapping the spawn in a subshell ``( … & )`` lets the outer
    shell exit immediately; ``setsid`` + explicit ``</dev/null`` redirection
    of all three FDs ensures the backgrounded chromium never holds the
    parent's pipes.
    """
    # Match the computer-use agent's chromium launch (``agents/computer-use/
    # Dockerfile``, DISPLAY_WIDTH/HEIGHT = 1280/800). Flows like zulip's hide
    # elements below a CSS breakpoint on narrow viewports — headless chromium
    # with no ``--window-size`` defaults small enough that those elements
    # resolve as ``hidden`` and Playwright's ``wait_for_selector`` (visible-
    # by-default) times out. ``login_via_cdp`` has been running the same
    # flows against the computer-use 1280×800 chrome for months, so pin the
    # same dimensions here.
    log_path = f"/tmp/plato-cdp-chromium-{port}.log"
    script = (
        f"mkdir -p {shlex.quote(profile_dir)} && "
        f"( setsid {shlex.quote(chrome_bin)} "
        f"--headless --no-sandbox "
        f"--window-size=1280,800 "
        f"--remote-debugging-port={port} "
        f"--remote-allow-origins=* "
        f"--user-data-dir={shlex.quote(profile_dir)} "
        f"about:blank </dev/null >>{shlex.quote(log_path)} 2>&1 & )"
    )
    rc, _, err = await run_cmd(["bash", "-c", script])
    if rc != 0:
        raise RuntimeError(f"chromium spawn on :{port} failed: rc={rc} stderr={err[-400:]!r}")

    loop = asyncio.get_event_loop()
    deadline = loop.time() + _CHROMIUM_READY_TIMEOUT_S
    last_diag = ""
    while loop.time() < deadline:
        rc, out, err = await run_cmd(
            [
                "curl",
                "-fsS",
                "--max-time",
                "2",
                f"http://127.0.0.1:{port}/json/version",
            ]
        )
        if rc == 0 and '"webSocketDebuggerUrl"' in out:
            log.debug("chromium on :%d ready", port)
            return
        last_diag = (err or out)[-200:]
        await asyncio.sleep(_CHROMIUM_READY_POLL_S)
    raise RuntimeError(
        f"chromium on :{port} never became ready within {_CHROMIUM_READY_TIMEOUT_S}s (last diag: {last_diag!r})"
    )


async def _open_ssh_tunnel(
    *,
    ssh_key_path: Path,
    hostname: str,
    extra_ssh_opts: list[tuple[str, str]] | None,
    local_port: int,
    remote_port: int,
    log: logging.Logger,
) -> asyncio.subprocess.Process:
    """Open ``ssh -L local_port:127.0.0.1:remote_port -N``; caller terminates.

    Uses ``127.0.0.1`` (not ``localhost``) for the remote bind: SSH resolves
    the forward target on the *remote* side, and some rootfs images resolve
    ``localhost`` to ``::1`` first. Chromium binds IPv4-only by default, so
    an IPv6 forward lands on a dead socket and the tunnel looks open locally
    but every HTTP read through it gets an immediate RST.
    """
    ssh_cmd = build_ssh_command(ssh_key_path, hostname, extra_opts=extra_ssh_opts)
    tunnel_argv = [
        *ssh_cmd,
        "-N",
        "-L",
        f"{local_port}:127.0.0.1:{remote_port}",
    ]
    proc = await asyncio.create_subprocess_exec(
        *tunnel_argv,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.PIPE,
    )

    loop = asyncio.get_event_loop()
    deadline = loop.time() + _TUNNEL_READY_TIMEOUT_S
    while loop.time() < deadline:
        if proc.returncode is not None:
            err = (await proc.stderr.read()).decode("utf-8", errors="replace") if proc.stderr else ""
            raise RuntimeError(f"SSH -L {local_port}:127.0.0.1:{remote_port} exited early: {err[-400:]!r}")
        try:
            _, writer = await asyncio.open_connection("127.0.0.1", local_port)
            writer.close()
            await writer.wait_closed()
            log.debug("SSH tunnel to :%d ready", local_port)
            return proc
        except OSError:
            await asyncio.sleep(_TUNNEL_READY_POLL_S)

    proc.terminate()
    try:
        await asyncio.wait_for(proc.wait(), timeout=3)
    except asyncio.TimeoutError:
        proc.kill()
        await proc.wait()
    raise RuntimeError(f"SSH -L tunnel to localhost:{local_port} never bound within {_TUNNEL_READY_TIMEOUT_S}s")


async def resolve_cdp_ws_url(cdp_url: str, *, ready_timeout: float = 60.0) -> str:
    """Fetch ``/json/version`` at ``cdp_url`` and rewrite the WS URL for use.

    Chrome always reports ``webSocketDebuggerUrl: ws://localhost:<chrome_port>/...``
    regardless of which host/interface the caller used to reach it. Two
    failure modes fall out of that if you pass the raw URL straight to
    Playwright:

    - container rootfs without ``localhost`` in ``/etc/hosts``
      (``ENOTFOUND localhost``).
    - cross-host callers (e.g. mesh-IP to another VM) where ``localhost``
      resolves to the caller's loopback instead of Chrome's.

    Fix: poll ``/json/version`` ourselves, then substitute the scheme +
    netloc of the reported WS URL with ``ws://<host>:<port>`` parsed from
    the input ``cdp_url`` so Playwright connects back through the same
    endpoint we used. Path and query are preserved.

    Playwright ``connect_over_cdp`` accepts ``ws://`` directly and skips
    its own ``/json/version`` round-trip, so handing it the rewritten URL
    sidesteps the bug entirely.
    """
    parsed = urlparse(cdp_url)
    if not parsed.hostname or not parsed.port:
        raise ValueError(f"cdp_url must include host:port; got {cdp_url!r}")
    host = parsed.hostname
    port = parsed.port
    version_url = f"{cdp_url.rstrip('/')}/json/version"

    loop = asyncio.get_event_loop()
    deadline = loop.time() + ready_timeout
    last_error = ""
    info: dict | None = None
    async with httpx.AsyncClient(timeout=2.0) as client:
        while True:
            try:
                resp = await client.get(version_url)
                if resp.status_code == 200:
                    info = resp.json()
                    break
                last_error = f"HTTP {resp.status_code}"
            except Exception as e:
                last_error = repr(e)
            if loop.time() >= deadline:
                raise TimeoutError(
                    f"Chrome /json/version not reachable at {version_url} within {ready_timeout:.0f}s: {last_error}"
                )
            await asyncio.sleep(0.5)

    assert info is not None
    ws_parsed = urlparse(info["webSocketDebuggerUrl"])
    return urlunparse(("ws", f"{host}:{port}", ws_parsed.path, ws_parsed.params, ws_parsed.query, ws_parsed.fragment))


async def _terminate_tunnel(proc: asyncio.subprocess.Process) -> None:
    if proc.returncode is not None:
        return
    proc.terminate()
    try:
        await asyncio.wait_for(proc.wait(), timeout=5)
    except asyncio.TimeoutError:
        proc.kill()
        await proc.wait()


@contextlib.asynccontextmanager
async def shared_cdp_chromium(
    *,
    run_cmd: RunCmd,
    ssh_key_path: Path,
    hostname: str,
    extra_ssh_opts: list[tuple[str, str]] | None,
    port: int,
    profile_dir: str,
    log: logging.Logger | None = None,
) -> AsyncIterator[str]:
    """Launch chromium on the remote host with a CDP port and forward it back.

    Yields a ``ws://127.0.0.1:<port>/devtools/browser/<id>`` URL, directly
    consumable by ``playwright.chromium.connect_over_cdp``. The remote
    chromium is left running on exit so a subsequent
    ``agent-browser --session <alias> connect <port>`` call inherits the
    authenticated browser state.

    The URL uses ``127.0.0.1`` explicitly because chromium emits
    ``ws://localhost:<port>/...`` in its ``webSocketDebuggerUrl`` regardless
    of caller, and some container images (e.g. Plato world rootfs) ship
    without a ``localhost`` entry in ``/etc/hosts`` — which causes
    Playwright's WebSocket upgrade to fail DNS. :func:`_resolve_ws_url`
    does the rewrite.

    Parameters
    ----------
    run_cmd:
        SSH-backed command runner (typically from :func:`make_ssh_run_cmd`).
    ssh_key_path, hostname, extra_ssh_opts:
        Forwarded to ``build_ssh_command`` for the ``ssh -L`` tunnel. Must
        point at the same host as ``run_cmd``.
    port:
        Remote CDP port; also used as the local forwarded port.
    profile_dir:
        Remote user-data-dir for chromium. Should be stable per ``(session,
        env)`` so repeated logins reuse cached artifacts, and distinct per
        env so cookies don't cross-contaminate.
    log:
        Optional logger; defaults to the module logger.
    """
    active_log = log or logger

    await kill_stale_chromium(run_cmd, port=port, profile_dir=profile_dir, log=active_log)
    chrome_bin = await _resolve_chrome_bin(run_cmd)
    await _spawn_chromium(
        run_cmd,
        chrome_bin=chrome_bin,
        port=port,
        profile_dir=profile_dir,
        log=active_log,
    )

    tunnel = await _open_ssh_tunnel(
        ssh_key_path=ssh_key_path,
        hostname=hostname,
        extra_ssh_opts=extra_ssh_opts,
        local_port=port,
        remote_port=port,
        log=active_log,
    )
    try:
        ws_url = await resolve_cdp_ws_url(f"http://127.0.0.1:{port}")
        yield ws_url
    finally:
        await _terminate_tunnel(tunnel)
        # Remote chromium is intentionally left running — agent-browser
        # attaches to it via `connect <port>` and inherits the session.


__all__ = [
    "CDP_PORT_BASE",
    "kill_stale_chromium",
    "resolve_cdp_ws_url",
    "shared_cdp_chromium",
]
