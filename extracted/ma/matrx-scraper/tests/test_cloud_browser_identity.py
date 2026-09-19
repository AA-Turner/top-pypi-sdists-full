"""CB-013 — the Cloud Browser presents a person's Chrome, not an automation rig.

Pure tests (no browser): identity resolution, the WebGL init script, pointer /
keystroke shaping bounds, and the probe's judge over the 2026-09-18 production
fingerprint (which must FAIL) and a clean one (which must PASS). The live proof
is ``detection_probe.py`` inside the worker image; the CHROMIUM-gated test below
asserts the launch flags on a real headless launch when a Playwright Chromium is
present.
"""

from __future__ import annotations

import math
import os
from pathlib import Path

import pytest

pytest.importorskip("playwright", reason="playwright not installed (browser extra)")

from matrx_scraper.ai_browser import humanize  # noqa: E402
from matrx_scraper.cloud_browser.worker import detection_probe, identity  # noqa: E402
from matrx_scraper.cloud_browser.worker import models as M  # noqa: E402

# ── identity resolution ─────────────────────────────────────────────────────


def test_policy_wins_then_environment_then_defaults(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv(identity.CHROME_BINARY_ENV, raising=False)
    monkeypatch.setenv(identity.TIMEZONE_ENV, "Europe/Berlin")
    monkeypatch.delenv(identity.LOCALE_ENV, raising=False)
    monkeypatch.setenv(identity.WEBGL_RENDERER_ENV, "")
    monkeypatch.delenv(identity.WEBGL_VENDOR_ENV, raising=False)

    policy = M.LaunchPolicy(run_mode="automation_only", locale="fr-FR")
    ident = identity.resolve_identity(policy, chromium_fallback="/pw/chrome")
    assert ident.locale == "fr-FR"  # policy
    assert ident.timezone_id == "Europe/Berlin"  # environment
    assert ident.webgl_vendor == identity.DEFAULT_WEBGL_VENDOR  # default
    assert ident.webgl_renderer == ""  # environment says: patch off
    assert ident.humanize_input is True
    # No Google Chrome installed → Playwright's Chromium, announced as such.
    assert ident.executable_path == "/pw/chrome"
    assert ident.binary_kind == "playwright-chromium"


def test_google_chrome_is_preferred_when_installed(monkeypatch, tmp_path) -> None:
    chrome = tmp_path / "chrome"
    chrome.write_text("", encoding="utf-8")
    monkeypatch.setenv(identity.CHROME_BINARY_ENV, str(chrome))
    ident = identity.resolve_identity(
        M.LaunchPolicy(run_mode="handoff_capable"), chromium_fallback="/pw/chrome"
    )
    assert ident.executable_path == str(chrome)
    assert ident.binary_kind == "google-chrome"


def test_defaults_are_a_person_not_a_server(monkeypatch) -> None:
    for name in (
        identity.TIMEZONE_ENV,
        identity.LOCALE_ENV,
        identity.WEBGL_VENDOR_ENV,
        identity.WEBGL_RENDERER_ENV,
        identity.CHROME_BINARY_ENV,
    ):
        monkeypatch.delenv(name, raising=False)
    ident = identity.resolve_identity(
        M.LaunchPolicy(run_mode="handoff_capable"), chromium_fallback=None
    )
    assert ident.timezone_id not in ("UTC", "Etc/UTC")
    assert "SwiftShader" not in ident.webgl_renderer
    assert ident.binary_kind == "playwright-default"
    assert "--disable-blink-features=AutomationControlled" in identity.STEALTH_ARGS
    assert "--enable-automation" in identity.IGNORED_DEFAULT_ARGS


def test_policy_empty_string_turns_webgl_patch_off() -> None:
    policy = M.LaunchPolicy(run_mode="handoff_capable", webgl_vendor="", webgl_renderer="")
    ident = identity.resolve_identity(policy, chromium_fallback=None)
    assert identity.webgl_init_script(ident.webgl_vendor, ident.webgl_renderer) is None


def test_webgl_init_script_answers_both_unmasked_parameters_and_masks_itself() -> None:
    script = identity.webgl_init_script("Google Inc. (Intel)", "ANGLE (Intel, X, OpenGL 4.6)")
    assert script is not None
    assert "37445" in script and "37446" in script  # 0x9245 / 0x9246
    assert '"Google Inc. (Intel)"' in script
    assert "WebGL2RenderingContext" in script
    assert "[native code]" in script  # toString mask


def test_proxy_credentials_never_repr() -> None:
    policy = M.LaunchPolicy(
        run_mode="handoff_capable",
        proxy="http://proxy.example:8080",
        proxy_username="u",
        proxy_password="hunter2",
    )
    assert "hunter2" not in repr(policy)


# ── humanize: shape bounds ──────────────────────────────────────────────────


def test_bezier_path_is_curved_bounded_and_lands_exactly() -> None:
    start, end = (100.0, 100.0), (700.0, 400.0)
    path = humanize.bezier_path(start, end)
    assert path[-1] == end
    assert 10 <= len(path) <= 80
    # Not a straight line: some sample lies off the segment by more than a pixel.
    dx, dy = end[0] - start[0], end[1] - start[1]
    norm = math.hypot(dx, dy)
    off = max(abs((p[0] - start[0]) * dy - (p[1] - start[1]) * dx) / norm for p in path[:-1])
    assert off > 1.0
    # Every sample stays within a sane envelope of the move.
    for x, y in path:
        assert -100 <= x <= 900 and -100 <= y <= 600
    # Two moves never share a path.
    assert humanize.bezier_path(start, end) != path
    # A no-op move is just the destination.
    assert humanize.bezier_path(end, end) == [end]


def test_move_duration_grows_with_distance_and_stays_bounded() -> None:
    assert humanize.move_duration(0.5) == 0.0
    short = sum(humanize.move_duration(30) for _ in range(50)) / 50
    long = sum(humanize.move_duration(1200) for _ in range(50)) / 50
    assert short < long
    for d in (5, 80, 500, 3000):
        assert humanize.MOVE_MIN_DURATION <= humanize.move_duration(d) <= humanize.MOVE_MAX_DURATION


def test_aim_point_lands_inside_never_on_the_edge_and_varies() -> None:
    box = {"x": 200.0, "y": 300.0, "width": 100.0, "height": 40.0}
    points = {humanize.aim_point(box) for _ in range(200)}
    assert len(points) > 150
    for x, y in points:
        assert 212.0 <= x <= 288.0
        assert 304.8 <= y <= 335.2


def test_key_delay_bounds_and_word_breaks() -> None:
    plain = [humanize.key_delay("a") for _ in range(500)]
    assert min(plain) >= humanize.KEY_DELAY_MIN
    assert max(plain) <= humanize.KEY_DELAY_MAX + humanize.THINK_PAUSE[1]
    after_space = sum(humanize.key_delay(" ") for _ in range(500)) / 500
    after_letter = sum(plain) / 500
    assert after_space > after_letter


# ── the probe's judge ───────────────────────────────────────────────────────

PRODUCTION_2026_09_18 = {
    "webdriver": True,
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
    "brands": ["Chromium", "Not_A Brand"],
    "timezone": "UTC",
    "screen": {"w": 1280, "h": 720},
    "window": {"ow": 1288, "oh": 851, "iw": 1280, "ih": 720},
    "webgl": {
        "unmaskedVendor": "Google Inc. (Google)",
        "unmaskedRenderer": "ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver)",
        "getParameterNative": True,
    },
}

CLEAN = {
    "webdriver": False,
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
    "brands": ["Google Chrome", "Chromium", "Not_A Brand"],
    "timezone": "America/Los_Angeles",
    "screen": {"w": 1440, "h": 900},
    "window": {"ow": 1440, "oh": 900, "iw": 1440, "ih": 813},
    "webgl": {
        "unmaskedVendor": "Google Inc. (Intel)",
        "unmaskedRenderer": "ANGLE (Intel, Mesa Intel(R) UHD Graphics 630 (CFL GT2), OpenGL 4.6)",
        "getParameterNative": True,
    },
}


def test_judge_fails_the_2026_09_18_production_fingerprint() -> None:
    failures = detection_probe.judge(
        PRODUCTION_2026_09_18, [["WebDriver (New)", "present (failed)"]]
    )
    joined = "\n".join(failures)
    assert "webdriver" in joined
    assert "Google Chrome" in joined
    assert "UTC" in joined
    assert "SwiftShader" in joined
    assert "1280×720" in joined
    assert "sannysoft" in joined


def test_judge_passes_a_clean_fingerprint() -> None:
    assert detection_probe.judge(CLEAN, []) == []


# ── real launch flags (Playwright Chromium present) ─────────────────────────


def _chromium_available() -> bool:
    base = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"))
    return base.exists() and any(base.glob("chromium-*"))


@pytest.mark.skipif(not _chromium_available(), reason="no chromium browser binary")
async def test_headless_launch_hides_webdriver_and_sets_clock(tmp_path, monkeypatch) -> None:
    from matrx_scraper.cloud_browser.worker.runtime import BrowserWorker

    monkeypatch.delenv(identity.CHROME_BINARY_ENV, raising=False)
    monkeypatch.setenv(identity.TIMEZONE_ENV, "America/Chicago")
    monkeypatch.setenv(identity.LOCALE_ENV, "en-US")
    worker = BrowserWorker(worker_id="identity-test")
    worker.run_mode = "automation_only"
    worker.run_id = "identity-test"
    worker._user_data_dir = str(tmp_path / "profile")
    policy = M.LaunchPolicy(run_mode="automation_only")
    worker._policy = policy
    await worker._launch_context(policy, None)
    try:
        assert "--disable-blink-features=AutomationControlled" in worker.launch_args
        assert "--lang=en-US" in worker.launch_args
        page = worker._context.pages[0]
        await page.goto("data:text/html,<canvas id=c></canvas>")
        seen = await page.evaluate(
            """() => { const g = document.getElementById('c').getContext('webgl');
                      const d = g && g.getExtension('WEBGL_debug_renderer_info');
                      return { webdriver: navigator.webdriver,
                               tz: Intl.DateTimeFormat().resolvedOptions().timeZone,
                               lang: navigator.language,
                               renderer: d ? g.getParameter(d.UNMASKED_RENDERER_WEBGL) : 'no-webgl',
                               native: /native code/.test(Function.prototype.toString.call(g ? g.getParameter : Object)) }; }"""
        )
        assert seen["webdriver"] is False
        assert seen["tz"] == "America/Chicago"
        assert seen["lang"] == "en-US"
        if seen["renderer"] != "no-webgl":
            assert seen["renderer"] == identity.DEFAULT_WEBGL_RENDERER
            assert seen["native"] is True
    finally:
        await worker._context.close()
        await worker._pw.stop()
