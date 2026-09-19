"""Detection probe — does the Cloud Browser look like a person's Chrome? (CB-013)

Launches Chromium through the worker's OWN ``_launch_context`` (so it measures
exactly what a run gets, not a hand-built browser), visits the public
bot-detection pages, and prints one JSON report plus a PASS/FAIL verdict over the
checks a site actually uses:

* ``navigator.webdriver`` is false;
* the client-hint brands include ``Google Chrome`` (real Chrome, not
  Chromium-for-testing);
* the timezone is not UTC and agrees with the locale the run declared;
* WebGL does not report SwiftShader;
* ``screen`` is the X screen and the window is not the emulated 1280×720;
* bot.sannysoft.com shows no ``failed`` row.

Run inside the browser-worker image with Xvfb up (the image entrypoint does that):

    Xvfb :99 -screen 0 1440x900x24 & \\
    uv run --no-sync python -m matrx_scraper.cloud_browser.worker.detection_probe /out --extra

``--extra`` adds browserscan.net's bot-detection page. Screenshots land in the
output directory. Exit status 0 = PASS, 1 = FAIL, 2 = the probe itself broke.

This is the guard for CB-013: it FAILED on the 2026-09-18 production image
(webdriver present, Chromium brand, UTC, SwiftShader, 1280×720 emulation) and
passes on the image that ships identity.py + Google Chrome. Re-run it after any
change to the launch path, the Dockerfile, or a Playwright upgrade.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import tempfile

from matrx_scraper.cloud_browser.worker import models as M
from matrx_scraper.cloud_browser.worker.runtime import BrowserWorker

FINGERPRINT_JS = r"""
(() => {
  const gl = (() => {
    try {
      const c = document.createElement('canvas');
      const g = c.getContext('webgl') || c.getContext('experimental-webgl');
      if (!g) return {webgl: null};
      const d = g.getExtension('WEBGL_debug_renderer_info');
      return {
        vendor: g.getParameter(g.VENDOR), renderer: g.getParameter(g.RENDERER),
        unmaskedVendor: d ? g.getParameter(d.UNMASKED_VENDOR_WEBGL) : null,
        unmaskedRenderer: d ? g.getParameter(d.UNMASKED_RENDERER_WEBGL) : null,
        getParameterNative: /\[native code\]/.test(Function.prototype.toString.call(g.getParameter)),
      };
    } catch (e) { return {webglError: String(e)}; }
  })();
  const v = document.createElement('video');
  return {
    webdriver: navigator.webdriver,
    ua: navigator.userAgent,
    platform: navigator.platform,
    brands: navigator.userAgentData ? navigator.userAgentData.brands.map(b => b.brand) : null,
    languages: navigator.languages, language: navigator.language,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    tzOffsetMinutes: new Date().getTimezoneOffset(),
    screen: {w: screen.width, h: screen.height, aw: screen.availWidth, ah: screen.availHeight,
             cd: screen.colorDepth, dpr: devicePixelRatio},
    window: {ow: outerWidth, oh: outerHeight, iw: innerWidth, ih: innerHeight},
    plugins: navigator.plugins.length,
    hardwareConcurrency: navigator.hardwareConcurrency, deviceMemory: navigator.deviceMemory,
    chromeObj: !!window.chrome,
    h264: v.canPlayType('video/mp4; codecs="avc1.42E01E"'),
    aac: v.canPlayType('audio/mp4; codecs="mp4a.40.2"'),
    webgl: gl,
  };
})()
"""

# A page that records the input events it receives, so the probe can judge the
# SHAPE of a click and of typing (humanize.py) through the worker's own actions.
# Served through a route on a REAL public host (the actions' landing guard resolves
# the host and treats a ``data:`` URL as "no page loaded"; the guard is part of what
# the probe exercises). The route fulfils before any request leaves the browser.
INPUT_PAGE_URL = "https://example.com/matrx-input-probe/"
INPUT_PAGE = (
    "<html><body style='margin:0'>"
    "<div style='height:300px'></div>"
    "<input id='f' style='margin-left:400px;width:300px;height:30px'>"
    "<button id='b' style='display:block;margin:200px 0 0 600px;width:160px;height:40px'>go</button>"
    "<script>window.__ev=[];const T=performance.now.bind(performance);"
    "for(const n of ['mousemove','mousedown','mouseup','click','keydown','keyup','input'])"
    "document.addEventListener(n,e=>__ev.push({t:T(),n,x:e.clientX,y:e.clientY,k:e.key,id:e.target&&e.target.id}),true);"
    "</script></body></html>"
)

INPUT_SUMMARY_JS = """() => {
  const ev = window.__ev;
  const moves = ev.filter(e => e.n === 'mousemove');
  const downs = ev.filter(e => e.n === 'mousedown');
  const ups = ev.filter(e => e.n === 'mouseup');
  const keys = ev.filter(e => e.n === 'keydown').map(e => e.t);
  const gaps = keys.slice(1).map((t, i) => t - keys[i]);
  const b = document.getElementById('b').getBoundingClientRect();
  const last = downs[downs.length - 1];
  return {
    mousemoves: moves.length,
    distinct_move_points: new Set(moves.map(e => e.x + ',' + e.y)).size,
    press_hold_ms: downs.length && ups.length ? ups[ups.length - 1].t - last.t : null,
    click_off_centre_px: last ? Math.hypot(last.x - (b.left + b.width / 2), last.y - (b.top + b.height / 2)) : null,
    keydowns: keys.length,
    key_gap_min_ms: gaps.length ? Math.min(...gaps) : null,
    key_gap_max_ms: gaps.length ? Math.max(...gaps) : null,
    key_gap_distinct: new Set(gaps.map(g => Math.round(g))).size,
    field_value: document.getElementById('f').value,
    button_clicks: ev.filter(e => e.n === 'click' && e.id === 'b').length,
  };
}"""


def judge_input(summary: dict, typed: str) -> list[str]:
    """Failures in the SHAPE of input events. Empty = the events look human."""
    failures: list[str] = []
    if summary.get("field_value") != typed:
        failures.append(f"typed text did not arrive intact: {summary.get('field_value')!r}")
    if (summary.get("keydowns") or 0) < len(typed):
        failures.append(
            f"only {summary.get('keydowns')} keydowns for {len(typed)} characters (fill, not typing)"
        )
    if (summary.get("key_gap_min_ms") or 0) < 15:
        failures.append(f"keystrokes {summary.get('key_gap_min_ms')} ms apart (instant typing)")
    if (summary.get("key_gap_distinct") or 0) < 5:
        failures.append("keystroke timing is uniform (machine rhythm)")
    if (summary.get("distinct_move_points") or 0) < 8:
        failures.append(
            f"pointer teleported ({summary.get('distinct_move_points')} move points before clicking)"
        )
    if (summary.get("press_hold_ms") or 0) < 20:
        failures.append(f"mouse button held {summary.get('press_hold_ms')} ms (instant click)")
    if summary.get("click_off_centre_px") is not None and summary["click_off_centre_px"] < 0.5:
        failures.append("click landed on the exact element centre")
    if summary.get("button_clicks") != 1:
        failures.append(f"button received {summary.get('button_clicks')} clicks, expected 1")
    return failures


SANNYSOFT_ROWS_JS = """() => Array.from(document.querySelectorAll('table tr')).map(tr => ({
  cells: [...tr.children].map(td => td.innerText.trim().slice(0, 90)),
  cls: [...tr.children].map(td => td.className).join(' '),
})).filter(r => r.cells.length >= 2)"""


def judge(fp: dict, sannysoft_failed: list) -> list[str]:
    """The failures a site could act on. Empty = PASS. Pure, so a test can feed it."""
    failures: list[str] = []
    if fp.get("webdriver") is not False:
        failures.append(f"navigator.webdriver is {fp.get('webdriver')!r}, must be false")
    brands = fp.get("brands") or []
    if "Google Chrome" not in brands:
        failures.append(f"client-hint brands {brands} lack 'Google Chrome' (not real Chrome)")
    if "HeadlessChrome" in (fp.get("ua") or ""):
        failures.append("user agent says HeadlessChrome")
    if fp.get("timezone") in (None, "UTC", "Etc/UTC"):
        failures.append(f"timezone is {fp.get('timezone')!r} (a server's clock)")
    gl = fp.get("webgl") or {}
    for key in ("renderer", "unmaskedRenderer", "unmaskedVendor"):
        if "SwiftShader" in str(gl.get(key) or ""):
            failures.append(f"WebGL {key} reports SwiftShader: {gl.get(key)}")
    if gl.get("getParameterNative") is False:
        failures.append("WebGLRenderingContext.getParameter no longer reads as native code")
    scr, win = fp.get("screen") or {}, fp.get("window") or {}
    if (win.get("iw"), win.get("ih")) == (1280, 720) and (scr.get("w"), scr.get("h")) == (
        1280,
        720,
    ):
        failures.append("viewport and screen are both exactly 1280×720 (Playwright emulation)")
    if scr.get("w") and win.get("ow") and win["ow"] > scr["w"]:
        failures.append(f"window outerWidth {win['ow']} exceeds screen width {scr['w']}")
    if sannysoft_failed:
        failures.append(f"bot.sannysoft.com failed rows: {sannysoft_failed}")
    return failures


async def run(out_dir: str, *, extra: bool) -> int:
    os.makedirs(out_dir, exist_ok=True)
    width = int(os.environ.get("BROWSER_WORKER_WIDTH", "1440"))
    height = int(os.environ.get("BROWSER_WORKER_HEIGHT", "900"))
    worker = BrowserWorker(
        worker_id="detection-probe", xvfb_display=os.environ.get("DISPLAY", ":99")
    )
    worker.run_mode = "handoff_capable"
    worker.run_id = "detection-probe"
    worker._user_data_dir = tempfile.mkdtemp(prefix="detection-probe-profile-")
    policy = M.LaunchPolicy(run_mode="handoff_capable")
    display = M.DisplayConfig(kind="xvfb", width=width, height=height)
    worker._policy, worker._display = policy, display
    await worker._launch_context(policy, display)
    assert worker._context is not None and worker._pw is not None
    page = worker._context.pages[0]
    report: dict = {
        "binary": worker.identity.binary_kind if worker.identity else None,
        "chromium_version": worker.chromium_version,
        "launch_args": worker.launch_args,
    }
    try:
        # Input shape first, through the worker's own actions (humanize on by policy).
        from matrx_scraper.ai_browser import actions as A

        async def _serve_input_page(route) -> None:  # noqa: ANN001
            await route.fulfill(status=200, content_type="text/html", body=INPUT_PAGE)

        await worker._context.route(INPUT_PAGE_URL + "**", _serve_input_page)
        await page.goto(INPUT_PAGE_URL, wait_until="load")
        typed = "Hello from a person, typing."
        r1 = await A.type_text(worker.run_id, "#f", typed, human=True, mgr=worker._session_mgr)
        r2 = await A.click(worker.run_id, "#b", human=True, mgr=worker._session_mgr)
        report["input"] = await page.evaluate(INPUT_SUMMARY_JS)
        report["input"]["actions_ok"] = bool(r1.success and r2.success)
        report["input_failures"] = judge_input(report["input"], typed)
        if not report["input"]["actions_ok"]:
            report["input_failures"].append(
                f"actions failed: {r1.error_message} / {r2.error_message}"
            )

        await page.goto("https://bot.sannysoft.com/", wait_until="load", timeout=60_000)
        await page.wait_for_timeout(4_000)
        report["fingerprint"] = await page.evaluate(FINGERPRINT_JS)
        rows = await page.evaluate(SANNYSOFT_ROWS_JS)
        report["sannysoft_failed"] = [r["cells"] for r in rows if "failed" in r["cls"]]
        report["sannysoft_warn"] = [r["cells"] for r in rows if "warn" in r["cls"]]
        await page.screenshot(path=os.path.join(out_dir, "sannysoft.png"), full_page=True)
        if extra:
            await page.goto(
                "https://www.browserscan.net/bot-detection", wait_until="load", timeout=60_000
            )
            await page.wait_for_timeout(9_000)
            text = await page.inner_text("body")
            verdict = (
                text.split("Test Results:", 1)[-1].strip().split("\n", 1)[0]
                if "Test Results:" in text
                else "?"
            )
            report["browserscan_verdict"] = verdict
            report["browserscan_text"] = text[:2500]
            await page.screenshot(path=os.path.join(out_dir, "browserscan.png"), full_page=True)
        report["failures"] = (
            judge(report["fingerprint"], report["sannysoft_failed"]) + report["input_failures"]
        )
        if extra and report.get("browserscan_verdict") not in ("Normal", "?"):
            report["failures"].append(f"browserscan verdict: {report['browserscan_verdict']}")
    finally:
        await worker._context.close()
        await worker._pw.stop()
    _write_report(os.path.join(out_dir, "report.json"), report)
    print(json.dumps(report, indent=1, default=str))
    print("VERDICT:", "PASS" if not report["failures"] else "FAIL")
    return 0 if not report["failures"] else 1


def _write_report(path: str, report: dict) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1, default=str)


def main(argv: list[str]) -> int:
    out_dir = next((a for a in argv[1:] if not a.startswith("--")), "/probe-out")
    try:
        return asyncio.run(run(out_dir, extra="--extra" in argv))
    except Exception as exc:  # noqa: BLE001 — the probe's own failure is exit 2, said plainly
        print(f"PROBE BROKE: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
