"""testmu.run(fn) — session lifecycle.

Detects environment (cloud vs local), launches browser,
creates page, calls fn(page=page), tears down.

Module-level `state` holds references needed by helpers like
execute_kane_cli that perform browser handoff mid-test:
- state.pw:        async_playwright() handle (for reconnect)
- state.relay:     PlaywrightRelayProxy instance (cloud only)
- state.relay_url: ws://127.0.0.1:{port} (cloud only)
Local runs leave relay/relay_url as None.
"""
import asyncio
import logging
import os
import platform
from types import SimpleNamespace

from testmu import _config
from testmu import _configure
from testmu._capability import (
    _sanitize_lt_options,
    get_capabilities,
    get_cdp_url,
    get_cdp_url_for_log,
    get_viewport,
)
from testmu._downloads_path import _resolve_downloads_dir
from testmu._reporter import reporter

_log = logging.getLogger("testmu")

# Session-wide mutable state accessible to helpers.
state = SimpleNamespace(pw=None, relay=None, relay_task=None, relay_url=None)


def _export_smart_env_from_session(browser, caps: dict) -> None:
    """V3-only: override smart_* env vars from the LIVE browser session.

    Gated on kane_version == "v3" (the shared testmu binding defaults to "v4").
    For V4/V16 this is a no-op — those keep the requested-caps smart_* set by
    get_capabilities(). For V3 we override post-connect/launch so browser.version
    is the real running instance (not the requested "latest") and os_* come from
    the runtime host (V2 add_smart_var parity).

    Args:
        browser: Live Playwright Browser object (returned by connect or launch).
        caps: Capabilities dict from get_capabilities() for cloud runs; pass {}
              for local runs where there are no requested caps (browser_name → "").
    """
    if _configure.get("kane_version", "v4") != "v3":
        return
    os.environ["smart_browser_version"] = str(browser.version or "")
    os.environ["smart_browser_name"] = str(caps.get("browserName") or "")
    os.environ["smart_os"] = platform.system()
    os.environ["smart_os_version"] = platform.version()


def _assert_sse_browser_supported(page) -> None:
    """SSE capture is CDP-based (Chromium-only). If a run configures
    devtools={'sse': True} on Firefox/WebKit, warn and hard-fail — never
    silently pass. WebSocket capture is cross-browser, so this gate is
    SSE-specific and leaves WS untouched. Defensive: if browser-type
    introspection fails, do not break the run."""
    cfg = _configure.get("devtools") or {}
    if not cfg.get("sse"):
        return
    try:
        name = page.context.browser.browser_type.name
        name = name() if callable(name) else name
    except Exception:
        name = None
    if name and name != "chromium":
        from testmu._errors import TestmuConfigError
        _log.warning("SSE capture is Chromium-only; got %s. Failing the run.", name)
        raise TestmuConfigError(
            f"SSE network assertions require Chromium; this run targets {name}."
        )


def _apply_page_timeouts(page) -> None:
    """Apply page defaults: env > configure > 10s action / 30s navigation."""
    env_action = os.environ.get("TESTMU_ACTION_TIMEOUT_MS")
    env_nav = os.environ.get("TESTMU_NAVIGATION_TIMEOUT_MS")
    action_timeout = int(env_action) if env_action else int(_configure.get("default_action_timeout_ms", 10000))
    nav_timeout = int(env_nav) if env_nav else int(_configure.get("default_navigation_timeout_ms", 30000))
    page.set_default_timeout(action_timeout)
    page.set_default_navigation_timeout(nav_timeout)


async def _create_page():
    """Create a Playwright page — cloud CDP or local browser."""
    from playwright.async_api import async_playwright

    pw = await async_playwright().start()
    state.pw = pw

    raw_headers = _configure.get("custom_headers", {})
    if raw_headers:
        from testmu._vars import var
        headers = {k: var(v) for k, v in raw_headers.items()}
    else:
        headers = {}

    if _config.run_target == "cloud":
        _log.info("Connecting to LT cloud...")
        caps = get_capabilities()
        lt_opts = caps.get("LT:Options", {})
        _log.info(
            "Capabilities: browser=%s %s, platform=%s, build=%s, name=%s",
            caps.get("browserName", "?"), caps.get("browserVersion", "?"),
            lt_opts.get("platform", "?"), lt_opts.get("build", "?"),
            lt_opts.get("name", "?"),
        )
        # Dump full LT:Options + CDP URL so every cap reaching the grid is
        # visible for debugging. Credentials (accessKey/user) are masked.
        import json as _json
        _log.info(
            "Full LT:Options: %s",
            _json.dumps(_sanitize_lt_options(lt_opts), default=str),
        )
        cdp_url = get_cdp_url(caps)
        _log.info(
            "CDP URL (capabilities URL-encoded): %s", get_cdp_url_for_log(caps)
        )
        viewport = get_viewport()

        # Cloud sessions route through a local relay proxy so kane-cli
        # can take over the browser mid-test and the main session can
        # reconnect with state replay. Port legacy behavior verbatim.
        from testmu._relay_proxy import PlaywrightRelayProxy
        state.relay = PlaywrightRelayProxy(cdp_url, local_port=0)
        state.relay_task = asyncio.create_task(state.relay.start())
        await state.relay.wait_ready()
        state.relay_url = f"ws://127.0.0.1:{state.relay.local_port}"
        _log.info("Relay proxy listening at %s", state.relay_url)

        browser = await pw.chromium.connect(state.relay_url, timeout=120000)
        _export_smart_env_from_session(browser, caps)
        _log.info("Connected to LT cloud via relay proxy")
        context_kwargs = {"viewport": viewport}
        if headers:
            context_kwargs["extra_http_headers"] = headers
        context = await browser.new_context(**context_kwargs)
        page = await context.new_page()
        _apply_page_timeouts(page)
        _log.info("Page created (viewport=%sx%s)", viewport.get("width"), viewport.get("height"))
    else:
        # Local: direct chromium.launch, no relay proxy.
        headless = os.getenv("TESTMU_HEADLESS", "true").lower() == "true"
        _log.info("Launching local browser (headless=%s)...", headless)
        browser = await pw.chromium.launch(headless=headless)
        _export_smart_env_from_session(browser, {})
        context_kwargs = {"viewport": None}
        if headers:
            context_kwargs["extra_http_headers"] = headers
        context = await browser.new_context(**context_kwargs)
        page = await context.new_page()
        _apply_page_timeouts(page)
        _log.info("Page created")

    # Wire LT reporter with page reference
    rep = reporter()
    if hasattr(rep, "set_page"):
        rep.set_page(page)

    return pw, browser, context, page


async def _download_files(files):
    """Download uploaded test files to ~/Downloads/ using LT auth."""
    import aiohttp
    import base64
    username = os.getenv("LT_USERNAME", "")
    access_key = os.getenv("LT_ACCESS_KEY", "")
    if not username or not access_key:
        _log.warning("Cannot download files — no LT credentials")
        return
    auth = base64.b64encode(f"{username}:{access_key}".encode()).decode()
    auth_headers = {"Authorization": f"Basic {auth}"}
    dl_dir = _resolve_downloads_dir()
    os.makedirs(dl_dir, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        for f in files:
            url = f.get("media_url", "")
            name = f.get("name", "")
            if not url or not name:
                continue
            if not url.startswith("http"):
                url = f"https://{url}"
            try:
                async with session.get(url, headers=auth_headers) as resp:
                    resp.raise_for_status()
                    dest = os.path.join(dl_dir, name)
                    with open(dest, "wb") as out:
                        async for chunk in resp.content.iter_chunked(8192):
                            out.write(chunk)
                    _log.info(f"Downloaded: {name} -> {dest}")
            except Exception as e:
                _log.warning(f"Failed to download {name}: {e}")


async def _async_run(fn):
    """Async session lifecycle."""
    # Log config summary
    _log.info("Mode: run_target=%s, lt_auth=%s, smart=%s",
              _config.run_target, _config.lt_auth, _config.smart)
    vars_count = len(_configure.get("variables", {}))
    params_count = len(_configure.get("test_params", {}))
    globals_count = len(_configure.get("global_variables", []))
    if vars_count or params_count or globals_count:
        _log.info("Variables: %d test-level, %d params, %d globals",
                  vars_count, params_count, globals_count)

    pw, browser, context, page = await _create_page()
    try:
        # Start DevTools capture BEFORE user code (captures from first navigation)
        from testmu._devtools_capture import (
            start_capture, stop_capture, stop_sse_capture, reset as _devtools_reset,
        )
        from testmu._helpers.execute_api import clear_api_call_log
        _devtools_reset()
        clear_api_call_log()  # api_calls log is per-run, like devtools capture
        # Hard-fail SSE on non-Chromium BEFORE starting capture (teardown-protected).
        _assert_sse_browser_supported(page)
        await start_capture(page, context)

        # Download uploaded files if any
        uploaded_files = _configure.get("uploaded_files", [])
        if uploaded_files:
            _log.info("Downloading %d uploaded file(s)...", len(uploaded_files))
            await _download_files(uploaded_files)

        # Apply HE test-run config overrides (dataset params, capability overrides)
        from testmu._test_config import get_test_params_override
        param_overrides = get_test_params_override()
        if param_overrides:
            from testmu._vars import _test_params
            _test_params.update(param_overrides)
            _log.info("Applied %d test param overrides from HE config", len(param_overrides))

        await fn(page=page)
    finally:
        _log.info("Tearing down session...")
        # Stop DevTools capture. stop_capture (sync) flips _sse_active off and
        # removes the new-page listener first; stop_sse_capture (async) then
        # drains pending tasks and detaches every CDP session.
        try:
            stop_capture(page)
        except Exception:
            pass
        try:
            await stop_sse_capture()
        except Exception:
            pass
        try:
            await browser.close()
        except Exception:
            pass
        if state.relay is not None:
            try:
                state.relay.shutdown()
                if state.relay_task is not None:
                    await asyncio.wait_for(state.relay_task, timeout=5)
            except (asyncio.TimeoutError, Exception):
                pass
        try:
            await pw.stop()
        except Exception:
            pass
        # Reset state for next run (pytest/asyncio test isolation)
        state.pw = None
        state.relay = None
        state.relay_task = None
        state.relay_url = None
        _log.info("Session closed")


def run(fn):
    """Session entry point — detect sync/async, launch browser, call fn, teardown."""
    # .env is loaded at testmu package import (see testmu/__init__.py) so that
    # module-level os.getenv() reads in _config / _helpers already see its values.

    # Configure logging so testmu messages are visible on stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Fail-fast: smart helpers require LT creds (vision/heal/kane-cli all need LT infra)
    if _config.smart and not _config.lt_auth:
        from testmu._errors import TestmuConfigError
        raise TestmuConfigError(
            "TESTMU_SMART=1 requires LT_USERNAME and LT_ACCESS_KEY. "
            "Smart helpers (vision, heal, kane-cli, SmartUI) need LT infrastructure."
        )

    if asyncio.iscoroutinefunction(fn):
        asyncio.run(_async_run(fn))
    else:
        raise NotImplementedError("Sync mode not yet supported. Use async def.")
