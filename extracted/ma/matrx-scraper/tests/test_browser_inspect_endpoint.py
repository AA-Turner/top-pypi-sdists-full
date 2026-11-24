"""`POST /api/scraper/browser-inspect` — the stateless render CHECK.

Same threat surface as `/browser-fetch` (an arbitrary-URL, JS-executing
navigation from INSIDE the scraper network) plus pixels, so it carries the same
contract: publicly-routable targets only, the FINAL url re-validated after the
browser follows redirects with the WHOLE result withheld when it isn't public,
and a structured `success=false` instead of a 500 on any failure.

It also pins the two things that make it worth a third endpoint at all: the
console/failed-request evidence reaches the caller, and the caller's device
identity (`user_agent_suffix`) is passed through rather than dropped.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest

from matrx_scraper.browser_pool import (
    BrowserInspectTimeout,
    CapturedScreenshot,
    PageInspection,
    ScreenshotCaptureFailure,
)

# `matrx_scraper.api.__init__` rebinds the name `scrape_router` to the router
# OBJECT, so a plain `import ... as mod` yields an APIRouter. Reach the module.
mod = importlib.import_module("matrx_scraper.api.scrape_router")

_PNG = b"\x89PNG\r\n\x1a\nfake"


class _FakePool:
    """Records the inspect call and returns a canned inspection."""

    def __init__(self, *, result: Any = None, raises: BaseException | None = None):
        self.calls: list[dict[str, Any]] = []
        self._raises = raises
        self._result = result or PageInspection(
            http_status=200,
            final_url="https://example.com/a",
            title="Title",
            console_errors=["Uncaught: Error: boom"],
            failed_requests=["GET https://cdn/x.js — net::ERR_ABORTED"],
            dom_text_found=True,
            dom_selector_found=False,
            screenshots=[
                CapturedScreenshot(kind="viewport_desktop", width=1440, height=900, bytes=_PNG)
            ],
            screenshot_failures=[
                ScreenshotCaptureFailure(
                    kind="viewport_mobile", error_class="TimeoutError", error_message="slow"
                )
            ],
        )

    async def inspect_url(self, url: str, **kwargs: Any):
        self.calls.append({"url": url, **kwargs})
        if self._raises is not None:
            raise self._raises
        return self._result


def _install(monkeypatch: pytest.MonkeyPatch, pool: Any, *, allow: set[str] | None = None) -> None:
    import matrx_scraper._ext as ext
    import matrx_scraper.utils.url as url_mod

    monkeypatch.setattr(ext, "has_ext", lambda name: name == "browser_pool")
    monkeypatch.setattr(ext, "get_ext", lambda name: pool)

    async def fake_validate(url: str) -> str:
        if allow is not None and url not in allow:
            raise ValueError("URL host resolves to a non-public IP address: h (10.1.2.3)")
        return url

    monkeypatch.setattr(url_mod, "validate_public_http_url", fake_validate)
    monkeypatch.setattr("matrx_scraper.scraper.get_required_random_proxy", lambda: "http://p:1")


@pytest.mark.asyncio
async def test_returns_the_render_evidence_the_other_endpoints_cannot(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The console/pageerror + failed-request streams are the whole reason this
    endpoint exists — neither /browser-fetch nor /browser/* exposes them."""
    pool = _FakePool()
    _install(monkeypatch, pool)
    result = await mod.browser_inspect(
        mod.BrowserInspectRequest(
            url="https://example.com/a",
            kinds=["viewport_desktop"],
            expect_text="hello",
            expect_selector="#nope",
        ),
        ctx=None,
    )
    assert result.success is True
    assert result.http_status == 200
    assert result.console_errors == ["Uncaught: Error: boom"]
    assert result.failed_requests == ["GET https://cdn/x.js — net::ERR_ABORTED"]
    assert result.expect_text_found is True
    assert result.expect_selector_found is False
    assert [(s.kind, s.width) for s in result.screenshots] == [("viewport_desktop", 1440)]
    # A dropped frame is missing EVIDENCE — it must reach the caller, not a log.
    assert [f.kind for f in result.screenshot_failures] == ["viewport_mobile"]


@pytest.mark.asyncio
async def test_proxy_is_off_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """Unlike /browser-fetch: a render check targets a site the caller owns."""
    pool = _FakePool()
    _install(monkeypatch, pool)
    await mod.browser_inspect(mod.BrowserInspectRequest(url="https://example.com/a"), ctx=None)
    assert pool.calls[0]["proxy"] is None


@pytest.mark.asyncio
async def test_user_agent_suffix_is_forwarded(monkeypatch: pytest.MonkeyPatch) -> None:
    pool = _FakePool()
    _install(monkeypatch, pool)
    await mod.browser_inspect(
        mod.BrowserInspectRequest(url="https://example.com/a", user_agent_suffix="Bot/1.0"),
        ctx=None,
    )
    assert pool.calls[0]["user_agent_suffix"] == "Bot/1.0"


@pytest.mark.asyncio
async def test_non_public_target_is_rejected_without_leaking_the_address(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from fastapi import HTTPException

    pool = _FakePool()
    _install(monkeypatch, pool, allow=set())
    with pytest.raises(HTTPException) as excinfo:
        await mod.browser_inspect(mod.BrowserInspectRequest(url="http://10.1.2.3/admin"), ctx=None)
    assert excinfo.value.status_code == 422
    assert "10.1.2.3" not in str(excinfo.value.detail)
    assert not pool.calls


@pytest.mark.asyncio
async def test_redirect_onto_a_private_host_discards_everything(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The browser follows redirects, so the page actually rendered may be
    internal. By then we hold its pixels AND its DOM answers — withhold all."""
    pool = _FakePool(
        result=PageInspection(
            http_status=200,
            final_url="http://169.254.169.254/latest/meta-data",
            title="secrets",
            console_errors=["leak"],
            dom_text_found=True,
            screenshots=[
                CapturedScreenshot(kind="viewport_desktop", width=1, height=1, bytes=_PNG)
            ],
        )
    )
    _install(monkeypatch, pool, allow={"https://example.com/a"})
    result = await mod.browser_inspect(
        mod.BrowserInspectRequest(url="https://example.com/a", kinds=["viewport_desktop"]),
        ctx=None,
    )
    assert result.success is False
    assert result.screenshots == []
    assert result.console_errors == []
    assert result.title == ""
    assert "169.254" not in (result.error or "") and "169.254" not in result.final_url


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("raises", "expect_retryable"),
    [
        (BrowserInspectTimeout("budget blown"), True),
        (ValueError("unknown screenshot kind: 'nope'"), False),
        (RuntimeError("chromium exploded"), True),
    ],
)
async def test_a_render_failure_never_500s(
    monkeypatch: pytest.MonkeyPatch, raises: BaseException, expect_retryable: bool
) -> None:
    pool = _FakePool(raises=raises)
    _install(monkeypatch, pool)
    result = await mod.browser_inspect(
        mod.BrowserInspectRequest(url="https://example.com/a"), ctx=None
    )
    assert result.success is False
    assert result.error
    assert result.retryable is expect_retryable


@pytest.mark.asyncio
async def test_no_browser_pool_is_a_503(monkeypatch: pytest.MonkeyPatch) -> None:
    from fastapi import HTTPException

    import matrx_scraper._ext as ext

    monkeypatch.setattr(ext, "has_ext", lambda name: False)
    with pytest.raises(HTTPException) as excinfo:
        await mod.browser_inspect(mod.BrowserInspectRequest(url="https://example.com/a"), ctx=None)
    assert excinfo.value.status_code == 503


def test_kinds_are_capped() -> None:
    """Every device profile in `kinds` costs its own navigation and its own
    hold on a pooled browser shared with live crawls."""
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        mod.BrowserInspectRequest(
            url="https://example.com/a",
            kinds=["viewport_desktop"] * (mod.BROWSER_INSPECT_MAX_KINDS + 1),
        )


async def test_exact_capture_reaches_the_pool_as_the_viewers_render(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rendered-output standard: width/theme/pixel ratio arrive intact; absent → None."""
    from matrx_scraper.browser_pool import ExactCaptureSpec

    pool = _FakePool()
    _install(monkeypatch, pool)
    await mod.browser_inspect(
        mod.BrowserInspectRequest(
            url="https://example.com/a",
            exact={"width": 566, "color_scheme": "dark", "device_scale_factor": 2},
        ),
        ctx=None,
    )
    spec = pool.calls[0]["exact"]
    assert isinstance(spec, ExactCaptureSpec)
    assert (spec.width, spec.color_scheme, spec.device_scale_factor, spec.full_page) == (566, "dark", 2.0, True)
    assert spec.context_kwargs()["viewport"]["width"] == 566
    assert spec.context_kwargs()["color_scheme"] == "dark"

    await mod.browser_inspect(mod.BrowserInspectRequest(url="https://example.com/a"), ctx=None)
    assert pool.calls[1]["exact"] is None


def test_exact_capture_refuses_out_of_range_width() -> None:
    from matrx_scraper.browser_pool import ExactCaptureSpec

    with pytest.raises(ValueError):
        ExactCaptureSpec(width=100)
    with pytest.raises(ValueError):
        ExactCaptureSpec(width=800, color_scheme="sepia")


@pytest.mark.asyncio
async def test_url_mode_measure_script_reaches_the_pool_and_its_result_comes_back(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A url render check can await the page's own ready signal and return what the page reported."""
    pool = _FakePool(
        result=PageInspection(
            http_status=200,
            final_url="https://example.com/a",
            measurements={"done": True, "verdict": "fail"},
            measure_error=None,
        )
    )
    _install(monkeypatch, pool)
    result = await mod.browser_inspect(
        mod.BrowserInspectRequest(url="https://example.com/a", measure_script="return window.__report"),
        ctx=None,
    )
    assert pool.calls[0]["measure_script"] == "return window.__report"
    assert result.measurements == {"done": True, "verdict": "fail"}
    assert result.measure_error is None


@pytest.mark.asyncio
async def test_opens_as_a_visitor_and_returns_failed_reads_and_frame_text(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The page-open check (aidream `page_check`): the person's session cookie reaches the browser context, the
    settle the caller asked for is honored with a budget that covers it, and the two things a client-rendered page
    needs to be judged — failed READS (HTTP >= 400, which `requestfailed` never sees) and the visible text of every
    frame — come back."""
    pool = _FakePool(result=PageInspection(
        http_status=200, final_url="https://www.aimatrx.com/applets/x", title="X",
        http_errors=["GET https://db.example/rest/v1/x -> 400"], visible_text="Cake orders\nNo rows",
    ))
    _install(monkeypatch, pool)
    result = await mod.browser_inspect(
        mod.BrowserInspectRequest(
            url="https://www.aimatrx.com/applets/x",
            cookies=[mod.InspectCookie(name="sb-a", value="base64-xyz", domain=".aimatrx.com")],
            collect_text=True,
            settle_seconds=8,
        ),
        ctx=None,
    )
    call = pool.calls[0]
    assert call["cookies"] == [{"name": "sb-a", "value": "base64-xyz", "domain": ".aimatrx.com", "path": "/",
                                "secure": True, "httpOnly": False, "sameSite": "Lax"}]
    assert call["collect_text"] is True
    assert call["settle_seconds"] == 8
    assert call["hard_budget_seconds"] >= 8 + 5
    assert result.http_errors == ["GET https://db.example/rest/v1/x -> 400"]
    assert result.visible_text == "Cake orders\nNo rows"


@pytest.mark.asyncio
async def test_no_cookies_means_none_and_default_budget(monkeypatch: pytest.MonkeyPatch) -> None:
    pool = _FakePool()
    _install(monkeypatch, pool)
    await mod.browser_inspect(mod.BrowserInspectRequest(url="https://example.com/a"), ctx=None)
    assert pool.calls[0]["cookies"] is None
    assert "settle_seconds" not in pool.calls[0]


# --- press: one button, in any frame, and what the press did ------------------------------------------------------


@pytest.mark.asyncio
async def test_press_reaches_the_pool_and_its_result_comes_back_typed(monkeypatch: pytest.MonkeyPatch) -> None:
    """The page_check `press` door: the spec reaches the pool, the budget grows by the wait, and the outcome (the
    calls the press made, the text after, the errors after) comes back as the typed `press` result."""
    from matrx_scraper.page_press import PressCall, PressOutcome

    pool = _FakePool(result=PageInspection(
        http_status=200, final_url="https://www.aimatrx.com/applets/x",
        press=PressOutcome(found=True, pressed=True, pressed_label="Run", calls=[
            PressCall(method="POST", url="https://server/actions/cake.save/run", status=200, body_excerpt="{}")],
            text_before="Orders", text_after="Orders\nSaved", seconds=3.21),
    ))
    _install(monkeypatch, pool)
    result = await mod.browser_inspect(
        mod.BrowserInspectRequest(url="https://www.aimatrx.com/applets/x", press=mod.InspectPress(
            button="Run", within="Cake orders", until_text=["Saved"], wait_seconds=20, watch=["/runtime/operations"])),
        ctx=None,
    )
    spec = pool.calls[0]["press"]
    assert (spec.button, spec.within, spec.until_text, spec.wait_seconds, spec.watch) == (
        "Run", "Cake orders", ["Saved"], 20, ["/runtime/operations"])
    assert pool.calls[0]["hard_budget_seconds"] >= 20 + 10
    assert result.press is not None and result.press.pressed and result.press.seconds == 3.2
    assert result.press.calls[0].url.endswith("/actions/cake.save/run") and result.press.calls[0].status == 200


def test_press_wait_is_capped() -> None:
    with pytest.raises(Exception):
        mod.InspectPress(button="Run", wait_seconds=90)


@pytest.mark.asyncio
async def test_no_press_asked_means_none(monkeypatch: pytest.MonkeyPatch) -> None:
    pool = _FakePool()
    _install(monkeypatch, pool)
    result = await mod.browser_inspect(mod.BrowserInspectRequest(url="https://example.com/a"), ctx=None)
    assert pool.calls[0]["press"] is None and result.press is None


# --- press in a real browser, inside a cross-origin frame ----------------------------------------------------------

_APP_FRAME = """<!doctype html><html><body>
<div class=card><h3>Cake orders</h3><button onclick="go('cake')">Run</button></div>
<div class=card><h3>Pie orders</h3><button onclick="go('pie')">Run</button></div>
<div class=card><h3>Tart orders</h3><button onclick="flash()">Run</button></div>
<div class=card><h3>Boiler service</h3><button id=ai>Write text</button><span id=aiout></span></div>
<div class=card><h3>Old invoices</h3><button id=del>Delete</button><span id=delout></span></div>
<div id=out></div><div id=toasts></div>
<script>
// The platform run button's inline spend question (matrx.runButton's ask(): role=group, data-matrx-run-confirm),
// drawn a moment after the click, as the real one is after it asks the server what the job costs.
document.getElementById('ai').onclick = () => setTimeout(() => {
  const out = document.getElementById('aiout');
  const g = document.createElement('span'); g.setAttribute('role', 'group'); g.setAttribute('data-matrx-run-confirm', '');
  const w = document.createElement('span'); w.textContent = 'This runs an AI step.';
  const yes = document.createElement('button'); yes.setAttribute('data-matrx-run-confirm-run', ''); yes.textContent = 'Write text';
  const no = document.createElement('button'); no.textContent = 'Cancel';
  yes.onclick = async () => { g.remove(); await fetch('/ai/mandates/visit.arrival_text', {method: 'POST', body: '{}'}); out.textContent = 'Saved boiler text'; };
  no.onclick = () => g.remove();
  g.append(w, yes, no); out.appendChild(g);
}, 400);
// A page's own inline "are you sure" (no roles, no platform markers): new buttons with a Cancel beside them.
document.getElementById('del').onclick = () => {
  const out = document.getElementById('delout');
  const q = document.createElement('span'); q.textContent = 'Are you sure? ';
  const yes = document.createElement('button'); yes.textContent = 'Yes, delete';
  const no = document.createElement('button'); no.textContent = 'Cancel';
  yes.onclick = async () => { await fetch('/rest/v1/invoices?id=eq.1', {method: 'DELETE'}); out.textContent = 'Deleted'; };
  out.append(q, yes, no);
};
// An autosave the page sends on load; it answers AFTER the click, but it was never the press's.
fetch('/ui-state/autosave', {method: 'POST', body: '{}'});
async function flash() {
  await fetch('/actions/tart.save/run', {method: 'POST', body: '{}'});
  const t = document.createElement('div'); t.setAttribute('role', 'alert'); t.innerText = 'Could not save tart';
  document.getElementById('toasts').appendChild(t);
  setTimeout(() => t.remove(), 700);  // gone long before the final re-read
}
async function go(which) {
  if (!confirm('Run ' + which + '?')) return;
  const r = await fetch('/actions/' + which + '.save/run', {method: 'POST', body: '{}'});
  const t = await r.text();
  document.getElementById('out').innerText = r.ok ? 'Saved ' + which : 'Failed: ' + t;
  if (!r.ok) console.error('save failed ' + r.status);
}
</script></body></html>"""


def _serve(handler_body: Any) -> tuple[Any, int]:
    import http.server
    import threading

    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a: Any) -> None:
            pass

        def _send(self, code: int, body: str, ctype: str, extra: dict[str, str] | None = None) -> None:
            raw = body.encode()
            self.send_response(code)
            self.send_header("content-type", ctype)
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.send_header("content-length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self) -> None:  # noqa: N802
            self._send(*handler_body("GET", self.path))

        def do_DELETE(self) -> None:  # noqa: N802
            self._send(*handler_body("DELETE", self.path))

        def do_POST(self) -> None:  # noqa: N802
            self.rfile.read(int(self.headers.get("content-length") or 0))
            self._send(*handler_body("POST", self.path))

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


@pytest.fixture
async def real_pool(monkeypatch: pytest.MonkeyPatch):
    import matrx_scraper.browser_pool as bp

    async def _no_guard(context: Any) -> None:  # the test pages live on loopback, which the egress guard refuses
        return None

    monkeypatch.setattr(bp, "install_egress_guard", _no_guard)
    pool = bp.PlaywrightBrowserPool(pool_size=1)
    try:
        await pool.start()
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"chromium not available: {exc}")
    try:
        yield pool
    finally:
        await pool.stop()


@pytest.fixture
def two_origins():
    def app(method: str, path: str) -> tuple[Any, ...]:
        if path.startswith("/actions/cake.save/run"):
            return (200, '{"type":"status","status":"running"}\n{"type":"action_result","action":"cake.save","status":"done"}\n',
                    "application/x-ndjson", {"Content-Range": "0-0/*"})
        if path.startswith("/ui-state/autosave"):
            import time as _t
            _t.sleep(7.0)  # still in flight when the press happens (the network-quiet wait gives up at 5 s)
            return 200, "{}", "application/json"
        if path.startswith("/ai/mandates/"):
            return 200, '{"type":"status","status":"running"}\n{"type":"result","status":"done"}\n', "application/x-ndjson"
        if path.startswith("/rest/v1/invoices"):
            return 204, "", "application/json", {"Content-Range": "0-0/*"}
        if path.startswith("/actions/tart.save/run"):
            return 200, '{"type":"action_result","status":"done"}', "application/json"
        if path.startswith("/actions/pie.save/run"):
            return 422, '{"detail":{"message":"Pie orders has no column \\"flavor\\""}}', "application/json"
        return 200, _APP_FRAME, "text/html"

    app_srv, app_port = _serve(app)
    # A DIFFERENT origin (localhost vs 127.0.0.1, another port) frames the app: a cross-origin frame.
    host_srv, host_port = _serve(lambda m, p: (200, f'<!doctype html><body><h1>Orders</h1>'
                                               f'<iframe src="http://localhost:{app_port}/app" width=800 height=400>'
                                               f'</iframe></body>', "text/html"))
    try:
        yield f"http://127.0.0.1:{host_port}/"
    finally:
        app_srv.shutdown()
        host_srv.shutdown()


@pytest.mark.asyncio
async def test_real_press_inside_a_cross_origin_frame_records_the_call_and_the_text_after(
    real_pool: Any, two_origins: str,
) -> None:
    from matrx_scraper.page_press import PressSpec

    got = await real_pool.inspect_url(
        two_origins, collect_text=True, settle_seconds=0.5, hard_budget_seconds=40,
        press=PressSpec(button="Run", within="Cake orders", until_text=["Saved cake"], wait_seconds=8),
    )
    press = got.press
    assert press.found and press.pressed, press
    assert press.confirmed and "cake" in press.confirmed  # the native confirm() was accepted
    assert [(c.method, c.status) for c in press.calls] == [("POST", 200)]
    assert press.calls[0].url.endswith("/actions/cake.save/run")
    assert '"action_result"' in press.calls[0].body_excerpt  # the stream's telling event, not its first line
    assert press.calls[0].content_range == "0-0/*"  # a data-API write's row count rides along
    assert "Saved cake" in press.text_after and "Saved cake" not in press.text_before
    assert press.console_errors_after == []


@pytest.mark.asyncio
async def test_real_press_scoped_by_within_hits_the_other_card_and_reports_its_refusal(
    real_pool: Any, two_origins: str,
) -> None:
    from matrx_scraper.page_press import PressSpec

    got = await real_pool.inspect_url(
        two_origins, collect_text=True, settle_seconds=0.5, hard_budget_seconds=40,
        press=PressSpec(button="Run", within="Pie orders", until_text=["Failed"], wait_seconds=8),
    )
    press = got.press
    assert [(c.method, c.status) for c in press.calls] == [("POST", 422)]
    assert "no column" in press.calls[0].body_excerpt
    assert any("save failed 422" in line for line in press.console_errors_after)
    assert any("422" in line for line in press.http_errors_after)


@pytest.mark.asyncio
async def test_real_press_of_a_missing_button_names_the_buttons_that_are_there(
    real_pool: Any, two_origins: str,
) -> None:
    from matrx_scraper.page_press import PressSpec

    got = await real_pool.inspect_url(
        two_origins, collect_text=True, settle_seconds=0.5, hard_budget_seconds=40,
        press=PressSpec(button="Save order", wait_seconds=2),
    )
    assert got.press.found is False and got.press.pressed is False
    assert "Run" in got.press.visible_buttons


@pytest.mark.asyncio
async def test_real_press_catches_a_toast_that_vanished_before_the_re_read(real_pool: Any, two_origins: str) -> None:
    from matrx_scraper.page_press import PressSpec

    got = await real_pool.inspect_url(
        two_origins, collect_text=True, settle_seconds=0.5, hard_budget_seconds=40,
        press=PressSpec(button="Run", within="Tart orders", wait_seconds=4),
    )
    assert "Could not save tart" in got.press.notices
    assert "Could not save tart" not in got.press.text_after
    # The autosave the page sent on load answered during the wait, but it started before the click: never the press's.
    assert [c.url.rsplit("/", 2)[-2] for c in got.press.calls] == ["tart.save"], got.press.calls


def test_an_ndjson_stream_surfaces_its_first_error_not_its_last_completed_line() -> None:
    from matrx_scraper.page_press import _excerpt

    body = ('{"type":"status","status":"running"}\n{"type":"error","message":"step write_row failed"}\n'
            '{"type":"status","status":"completed"}\n')
    assert "write_row failed" in _excerpt(body, "application/x-ndjson")


@pytest.mark.asyncio
async def test_real_press_answers_the_platform_run_buttons_inline_spend_question(real_pool: Any, two_origins: str) -> None:
    """Live run D (/applets/todays-jobs): the AI button's inline "This runs an AI step." went unanswered, so the job
    never reached the server. The press answers its go-ahead button and the job's call is recorded."""
    from matrx_scraper.page_press import PressSpec

    got = await real_pool.inspect_url(
        two_origins, collect_text=True, settle_seconds=0.5, hard_budget_seconds=40,
        press=PressSpec(button="Write text", within="Boiler service", until_text=["Saved boiler text"], wait_seconds=8),
    )
    p = got.press
    assert p.confirmed == "Write text" and p.confirm_unanswered is None, p
    assert [(c.method, c.url.split("/ai/")[-1]) for c in p.calls] == [("POST", "mandates/visit.arrival_text")]
    assert "Saved boiler text" in p.text_after


@pytest.mark.asyncio
async def test_real_press_answers_a_pages_own_inline_are_you_sure(real_pool: Any, two_origins: str) -> None:
    from matrx_scraper.page_press import PressSpec

    got = await real_pool.inspect_url(
        two_origins, collect_text=True, settle_seconds=0.5, hard_budget_seconds=40,
        press=PressSpec(button="Delete", within="Old invoices", until_text=["Deleted"], wait_seconds=6),
    )
    assert got.press.confirmed == "Yes, delete"
    assert [(c.method, c.status, c.content_range) for c in got.press.calls] == [("DELETE", 204, "0-0/*")]


@pytest.mark.asyncio
async def test_real_press_names_a_confirm_step_it_could_not_answer(real_pool: Any, two_origins: str) -> None:
    from matrx_scraper.page_press import PressSpec

    got = await real_pool.inspect_url(
        two_origins, collect_text=True, settle_seconds=0.5, hard_budget_seconds=40,
        press=PressSpec(button="Write text", within="Boiler service", confirm="Send it now", wait_seconds=3),
    )
    p = got.press
    assert p.confirmed is None and p.calls == []
    assert p.confirm_unanswered and "This runs an AI step." in p.confirm_unanswered and "'Cancel'" in p.confirm_unanswered


@pytest.mark.asyncio
async def test_real_press_says_when_the_within_card_is_not_on_the_page(real_pool: Any, two_origins: str) -> None:
    """Live run D: the card was filtered off the page by its date; "no button named …" was the wrong reason."""
    from matrx_scraper.page_press import PressSpec

    got = await real_pool.inspect_url(
        two_origins, collect_text=True, settle_seconds=0.5, hard_budget_seconds=40,
        press=PressSpec(button="Run", within="Water heater flush", wait_seconds=2),
    )
    assert got.press.found is False and got.press.within_missing is True
    assert "Run" in got.press.visible_buttons
