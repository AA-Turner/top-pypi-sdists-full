"""Kane CLI helper — execute_kane_cli with relay-proxy handoff.

Cloud-only: kane-cli takes over the browser via the in-process relay
proxy's --ws-endpoint. The main test disconnects, kane-cli drives the
browser, then the main test reconnects via the same relay URL. The
proxy replays the cached object tree so the reconnected test sees the
same browser state.

On local runs or with smart OFF, logs a warning and returns the
existing page unchanged (branch unresolved).
"""
import asyncio
import logging
import os
import shutil

from testmu import _config
from testmu._errors import TestmuConfigError

_log = logging.getLogger("testmu")


async def execute_kane_cli(objective: str, *, page):
    """Execute a test objective via kane-cli subprocess with browser handoff.

    Handoff sequence (cloud + smart only):
      1. Disconnect the main test's PW connection so kane-cli can take over.
      2. Spawn `kane-cli run <objective> --ws-endpoint <relay_url> ...`.
      3. Wait for kane-cli to finish.
      4. Reconnect via chromium.connect(relay_url). Proxy replays state.
      5. Return the new page; generator emits `page = await execute_kane_cli(...)`
         so the reassignment is visible to subsequent statements.

    Uses env vars:
        LT_USERNAME    — required by kane-cli auth
        LT_ACCESS_KEY  — required by kane-cli auth
        TESTMUAI_ENV   — deployment environment (default: "prod")

    Args:
        objective: Natural-language objective for kane-cli.
        page: Current Playwright page (for URL capture + reconnect).

    Returns:
        The (possibly new) page. On skip, returns the original page
        unchanged.
    """
    if not _config.smart:
        _log.info(
            "    [execute_kane_cli] smart is OFF — branch unresolved, skipping"
        )
        return page
    if _config.run_target != "cloud":
        _log.warning(
            "    [execute_kane_cli] run_target is not 'cloud' — kane-cli needs "
            "the relay proxy, skipping (branch unresolved)"
        )
        return page

    from testmu import _session
    relay_url = _session.state.relay_url
    pw = _session.state.pw
    if relay_url is None or pw is None:
        raise TestmuConfigError(
            "execute_kane_cli: relay proxy not initialized; "
            "ensure testmu.run(test) started the cloud session"
        )

    browser = page.context.browser

    username = os.getenv("LT_USERNAME", "")
    access_key = os.getenv("LT_ACCESS_KEY", "")
    env_name = os.getenv("TESTMUAI_ENV", "prod")

    # shutil.which resolves PATHEXT on Windows (e.g. an npm-installed "kane-cli"
    # is a kane-cli.cmd shim there) — create_subprocess_exec's underlying Win32
    # CreateProcess has no shell to do that resolution itself and fails the
    # bare name with WinError 2. Falls back to the bare name if not found so
    # the failure mode is unchanged when kane-cli truly isn't installed.
    kane_cli_bin = shutil.which("kane-cli") or "kane-cli"

    _log.info("    [execute_kane_cli] objective=%s", objective[:80])
    try:
        v_proc = await asyncio.create_subprocess_exec(
            kane_cli_bin, "--version",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        v_stdout, v_stderr = await asyncio.wait_for(v_proc.communicate(), timeout=10)
        v_out = (v_stdout.decode() if v_stdout else "") or (v_stderr.decode() if v_stderr else "")
        _log.info("    [execute_kane_cli] kane-cli --version: %s (exit %s)",
                  v_out.strip() or "(empty)", v_proc.returncode)
    except Exception as e:
        _log.info("    [execute_kane_cli] kane-cli --version failed: %s", e)
    _log.info("    [execute_kane_cli] handing off browser to kane-cli...")

    # Steps 1-2 (disconnect + spawn) may raise; step 3 (reconnect) must run
    # either way so the LT reporter has a live page for lambdahook updates
    # (lambda-testCase-end, setTestStatus) on the failure path.
    body_error: BaseException | None = None
    try:
        # 1. Release the PW connection so the relay can accept kane-cli.
        #    Using the Playwright-private _connection.stop_async — matches legacy.
        try:
            await browser._impl_obj._connection.stop_async()
        except Exception as e:
            _log.warning("    [execute_kane_cli] disconnect warning: %s", e)

        # 2. Spawn kane-cli pointing at our relay URL.
        cmd = [
            kane_cli_bin, "run", objective,
            "--ws-endpoint", relay_url,
            "--username", username,
            "--access-key", access_key,
            "--env", env_name,
            "--local",
            "--agent",
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=600)
        stdout_text = stdout.decode() if stdout else ""
        stderr_text = stderr.decode() if stderr else ""

        if stdout_text:
            _log.info("    [execute_kane_cli] stdout: %s", stdout_text[:2000])
        if stderr_text:
            _log.info("    [execute_kane_cli] stderr: %s", stderr_text[:2000])

        if proc.returncode != 0:
            raise RuntimeError(
                f"kane-cli failed (exit {proc.returncode}): {stderr_text}"
            )
    except BaseException as e:
        body_error = e

    # 3. Reconnect via the relay (best-effort — runs even if kane-cli failed,
    #    so downstream step-end/test-end can reach lambdahook).
    new_page = None
    try:
        _log.info("    [execute_kane_cli] reconnecting test to relay...")
        new_browser = await pw.chromium.connect(relay_url, timeout=120000)

        if new_browser.contexts:
            new_context = new_browser.contexts[0]
            if new_context.pages:
                new_page = new_context.pages[-1]
            else:
                new_page = await new_context.new_page()
        else:
            new_context = await new_browser.new_context()
            new_page = await new_context.new_page()

        from testmu._session import _apply_page_timeouts
        _apply_page_timeouts(new_page)

        _log.info("    [execute_kane_cli] reconnected — page URL: %s", new_page.url)

        # Re-wire LT reporter so step-end/test-end land on the live page.
        from testmu._reporter import reporter
        rep = reporter()
        if hasattr(rep, "set_page"):
            rep.set_page(new_page)
    except Exception as reconnect_err:
        _log.warning("    [execute_kane_cli] reconnect failed: %s", reconnect_err)

    if body_error is not None:
        raise body_error
    if new_page is None:
        raise RuntimeError(
            "execute_kane_cli: reconnect failed and no live page available"
        )
    return new_page
