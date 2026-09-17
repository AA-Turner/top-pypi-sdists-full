"""Kane CLI helper — execute_kane_cli with relay-proxy handoff.

Cloud-only: kane-cli takes over the browser via the in-process relay
proxy's --ws-endpoint. The main test disconnects, kane-cli drives the
browser, then the main test reconnects via the same relay URL. The
proxy replays the cached object tree so the reconnected test sees the
same browser state.

On local runs or with smart OFF, logs a warning and returns the
existing page unchanged (branch unresolved).

Evaluate form — ``execute_kane_cli(page=page, evaluate_conditions=[...])``:
an exported if/elif ladder whose late branches never got a replay recipe
hands every such condition to ``kane-cli run --analyzer-only`` in one batch
and gets one verdict back per condition, in order. Anything that is not a
completed judgement (smart off, local run, missing binary, non-zero exit,
timeout, unparseable output, a null verdict) reads FALSE with a warning; the
ladder then falls through to its else, the same way a condition-evidence miss
reads false at replay.
"""
import asyncio
import json
import logging
import os
import shutil
import tempfile

from testmu import _config
from testmu._errors import TestmuConfigError

_log = logging.getLogger("testmu")


async def execute_kane_cli(
    objective: str | None = None,
    *,
    page,
    evaluate_conditions: list[str] | None = None,
):
    """Execute a test objective via kane-cli subprocess with browser handoff.

    With ``evaluate_conditions`` instead of an objective, judge those
    conditions on the current page (``--analyzer-only``) and return
    ``(page, verdicts)`` — see ``_evaluate_conditions``.

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
    if evaluate_conditions is not None:
        if objective:
            raise ValueError(
                "execute_kane_cli takes an objective or evaluate_conditions, not both"
            )
        return await _evaluate_conditions(list(evaluate_conditions), page=page)
    if objective is None:
        raise ValueError("execute_kane_cli needs an objective or evaluate_conditions")
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


# ---------------------------------------------------------------------------
# Evaluate form
# ---------------------------------------------------------------------------

_EVALUATE_CLI_TIMEOUT_S = "120"   # kane-cli's own --timeout (exit 3 past it)
_EVALUATE_WAIT_S = 150            # our hard stop if the process never answers


async def _evaluate_conditions(conditions: list[str], *, page):
    """Judge ``conditions`` on the current page through one kane-cli handoff.

    Returns ``(page, verdicts)``: the reconnected page and one bool per
    condition, in order. Never raises for a judgement problem — only the
    relay reconnect can fail the test, exactly as the objective form.
    """
    count = len(conditions)
    unjudged = [False] * count
    if not conditions:
        return page, []
    if not _config.smart:
        _log.info("    [execute_kane_cli] smart is OFF — %d condition(s) read false", count)
        return page, unjudged
    if _config.run_target != "cloud":
        _log.warning(
            "    [execute_kane_cli] run_target is not 'cloud' — kane-cli needs the "
            "relay proxy; %d condition(s) read false", count,
        )
        return page, unjudged

    from testmu import _session
    relay_url = _session.state.relay_url
    pw = _session.state.pw
    if relay_url is None or pw is None:
        raise TestmuConfigError(
            "execute_kane_cli: relay proxy not initialized; "
            "ensure testmu.run(test) started the cloud session"
        )

    browser = page.context.browser
    rewritten, variables = _prepare_conditions(conditions)
    vars_path = _write_variables_file(variables) if variables else None
    argv = [shutil.which("kane-cli") or "kane-cli", "run", "--analyzer-only"]
    for condition in rewritten:
        argv += ["--condition", condition]
    argv += [
        "--ws-endpoint", relay_url,
        "--username", os.getenv("LT_USERNAME", ""),
        "--access-key", os.getenv("LT_ACCESS_KEY", ""),
        "--env", os.getenv("TESTMUAI_ENV", "prod"),
        "--local",
        "--agent",
        "--timeout", _EVALUATE_CLI_TIMEOUT_S,
    ]
    if vars_path:
        argv += ["--variables-file", vars_path]
    _log.info("    [execute_kane_cli] judging %d condition(s) via --analyzer-only", count)

    verdicts = unjudged
    try:
        # 1. Release the PW connection so the relay can accept kane-cli.
        try:
            await browser._impl_obj._connection.stop_async()
        except Exception as e:  # noqa: BLE001
            _log.warning("    [execute_kane_cli] disconnect warning: %s", e)
        # 2. Spawn, wait, parse. Every failure mode reads false.
        verdicts = await _judge(argv, count)
    finally:
        if vars_path:
            try:
                os.unlink(vars_path)
            except OSError:
                pass

    # 3. Reconnect via the relay — the one step that may still fail the test.
    new_page = await _reconnect(pw, relay_url)
    return new_page, verdicts


async def _judge(argv: list[str], count: int) -> list[bool]:
    """Run kane-cli and read ``run_end.condition_results``; false on any miss."""
    unjudged = [False] * count
    try:
        proc = await asyncio.create_subprocess_exec(
            *argv,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    except Exception as e:  # noqa: BLE001
        _log.warning("    [execute_kane_cli] could not start kane-cli (%s); conditions read false", e)
        return unjudged
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=_EVALUATE_WAIT_S)
    except asyncio.TimeoutError:
        _log.warning(
            "    [execute_kane_cli] kane-cli gave no verdict within %ss; killing it, "
            "conditions read false", _EVALUATE_WAIT_S,
        )
        try:
            proc.kill()
        except Exception:  # noqa: BLE001
            pass
        return unjudged
    stdout_text = stdout.decode(errors="replace") if stdout else ""
    stderr_text = stderr.decode(errors="replace") if stderr else ""
    if stderr_text:
        _log.info("    [execute_kane_cli] stderr: %s", stderr_text[:2000])
    run_end = _last_run_end(stdout_text)
    if proc.returncode != 0:
        _log.warning(
            "    [execute_kane_cli] kane-cli exited %s (%s); conditions read false",
            proc.returncode, (run_end or {}).get("reason") or stderr_text[-300:].strip(),
        )
        return unjudged
    if run_end is None:
        _log.warning("    [execute_kane_cli] no run_end in kane-cli output; conditions read false")
        return unjudged
    results = run_end.get("condition_results")
    if not isinstance(results, list):
        results = []
    verdicts = []
    for index in range(count):
        value = results[index] if index < len(results) else None
        if isinstance(value, bool):
            verdicts.append(value)
        else:
            reasons = run_end.get("condition_reasons") or []
            why = reasons[index] if index < len(reasons) else "no verdict"
            _log.warning("    [execute_kane_cli] condition #%d could not be judged (%s); reads false", index + 1, why)
            verdicts.append(False)
    _log.info("    [execute_kane_cli] verdicts=%s", verdicts)
    return verdicts


def _last_run_end(stdout_text: str) -> dict | None:
    run_end = None
    for line in stdout_text.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if isinstance(event, dict) and event.get("type") == "run_end":
            run_end = event
    return run_end


def _prepare_conditions(conditions: list[str]) -> tuple[list[str], dict[str, dict]]:
    """Resolve every ``{{name}}`` / ``${name}`` a condition references.

    kane-cli only knows the ``{{name}}`` form, so ``${name}`` is rewritten;
    values travel in a variables file, never on the command line, with
    secret and TOTP templates flagged so kane-cli masks them.
    """
    from testmu._vars import _DOLLAR_RE, _MUSTACHE_RE, _is_sensitive_template, var

    variables: dict[str, dict] = {}
    rewritten: list[str] = []
    for condition in conditions:
        names = [m.group(1).strip() for m in _MUSTACHE_RE.finditer(condition)]
        names += [m.group(1).strip() for m in _DOLLAR_RE.finditer(condition)]
        for name in names:
            if name in variables:
                continue
            template = "{{" + name + "}}"
            try:
                value = var(template)
            except Exception as e:  # noqa: BLE001
                _log.warning("    [execute_kane_cli] %s did not resolve (%s); sent empty", template, e)
                value = ""
            variables[name] = {
                "value": "" if value is None else str(value),
                "secret": _is_sensitive_template(template),
            }
        rewritten.append(_DOLLAR_RE.sub(lambda m: "{{" + m.group(1).strip() + "}}", condition))
    return rewritten, variables


def _write_variables_file(variables: dict[str, dict]) -> str:
    fd, path = tempfile.mkstemp(prefix="testmu-vars-", suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(variables, fh)
    return path


async def _reconnect(pw, relay_url: str):
    """Reconnect the test to the relay after a handoff (mirrors the objective form)."""
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
        from testmu._reporter import reporter
        rep = reporter()
        if hasattr(rep, "set_page"):
            rep.set_page(new_page)
    except Exception as reconnect_err:  # noqa: BLE001
        _log.warning("    [execute_kane_cli] reconnect failed: %s", reconnect_err)
    if new_page is None:
        raise RuntimeError("execute_kane_cli: reconnect failed and no live page available")
    return new_page
