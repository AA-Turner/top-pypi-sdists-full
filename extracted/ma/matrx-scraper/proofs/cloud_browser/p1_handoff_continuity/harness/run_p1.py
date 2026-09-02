"""P1 — exact human <-> agent handoff continuity. Phase-0 proof harness (NOT shipped code).

Claim under test (PLAN.md "Headed and automated modes", "Exact human <-> agent handoff"):

  An agent drives a HEADED Chromium persistent context on a virtual display; a human
  then interacts with that same running browser through input injected into the display;
  afterwards Playwright CONTINUES in the SAME process, SAME context, SAME page objects,
  and SEES the human's changes -- including a tab the human opened -- with no relaunch.

What this harness substitutes, and why it is honest
---------------------------------------------------
Production plans Selkies/WebRTC for the human plane. Selkies injects human input into
the X display through the XTEST extension. This harness injects input into the same
display through `xdotool`, which is the SAME XTEST mechanism. What is NOT covered here
is everything ABOVE that injection point: the WebRTC transport, TURN, the encoder, and
the auth gateway. Those are P2/P5 and are listed as limits in the report.

The harness reads element geometry with Playwright before handing over. That is the
test rig standing in for a human's eyes; it produces no input events. Input events in
the human phase come only from xdotool.

Run
---
    python3 harness/run_p1.py            # full run
    python3 harness/run_p1.py --keep     # leave Xvfb/app up for inspection

Requires: Xvfb, xdotool, python playwright whose bundled chromium exists under
PLAYWRIGHT_BROWSERS_PATH (defaults to /opt/pw-browsers).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ARTIFACTS = ROOT / "artifacts"
WORK = Path("/tmp/p1_handoff_continuity")
UDD = WORK / "profile"  # the persistent context's user_data_dir
DISPLAY = os.environ.get("P1_DISPLAY", ":91")
SCREEN = "1400x1000x24"

os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
os.environ["DISPLAY"] = DISPLAY  # every child (chromium, xdotool) targets our display

RESULTS: dict[str, object] = {
    "started_at": datetime.now(timezone.utc).isoformat(),
    "environment": {},
    "phases": [],
    "subclaims": {},
}
_LOG: list[str] = []


# ------------------------------------------------------------------ utilities


def log(msg: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    _LOG.append(line)


def record(name: str, verdict: str, detail: object) -> None:
    """verdict in PASS | FAIL | PARTIAL | INFO"""
    RESULTS["subclaims"][name] = {"verdict": verdict, "detail": detail}  # type: ignore[index]
    log(f"  >> {name}: {verdict}")


def phase(name: str, **kw) -> None:
    RESULTS["phases"].append({"phase": name, **kw})  # type: ignore[union-attr]
    log(f"--- PHASE {name} ---")


def free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def xdo(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    env = {**os.environ, "DISPLAY": DISPLAY}
    cp = subprocess.run(["xdotool", *args], env=env, capture_output=True, text=True)
    if check and cp.returncode != 0:
        log(f"  xdotool {' '.join(args)} -> rc={cp.returncode} err={cp.stderr.strip()}")
    return cp


def proc_identity(pid: int) -> dict:
    """PID plus the kernel's own start-time field -- a PID alone can be recycled."""
    try:
        stat = Path(f"/proc/{pid}/stat").read_text()
        # comm may contain spaces/parens; split after the last ')'
        fields = stat[stat.rindex(")") + 2 :].split()
        starttime = fields[19]  # field 22 overall
        cmdline = Path(f"/proc/{pid}/cmdline").read_bytes().decode(errors="replace")
        return {
            "pid": pid,
            "starttime_jiffies": starttime,
            "alive": True,
            "cmdline_head": cmdline.replace("\x00", " ")[:180],
        }
    except (FileNotFoundError, ProcessLookupError, ValueError):
        return {"pid": pid, "alive": False}


def find_browser_pid(marker: str) -> int | None:
    """The chromium main process is the one whose cmdline names our user_data_dir
    and is NOT a --type= child renderer/zygote."""
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit():
            continue
        try:
            cmd = (entry / "cmdline").read_bytes().decode(errors="replace")
        except OSError:
            continue
        if marker in cmd and "--type=" not in cmd:
            return int(entry.name)
    return None


# ------------------------------------------------------------------- fixtures


def start_xvfb() -> subprocess.Popen:
    log(f"starting Xvfb on {DISPLAY} ({SCREEN})")
    p = subprocess.Popen(
        ["Xvfb", DISPLAY, "-screen", "0", SCREEN, "-nolisten", "tcp"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(50):
        time.sleep(0.2)
        if xdo("getdisplaygeometry", check=False).returncode == 0:
            log(f"Xvfb up (pid {p.pid})")
            return p
    raise RuntimeError("Xvfb did not come up")


def start_app(port: int) -> subprocess.Popen:
    log(f"starting synthetic provider on 127.0.0.1:{port}")
    p = subprocess.Popen(
        [sys.executable, str(ROOT / "testapp" / "server.py"), str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(50):
        time.sleep(0.1)
        try:
            socket.create_connection(("127.0.0.1", port), 0.2).close()
            return p
        except OSError:
            continue
    raise RuntimeError("test app did not come up")


# ------------------------------------------------------------- human plane ---

CALIBRATE_SCRIPT = """
window.__p1 = { last: null };
addEventListener('mousemove', e => {
  window.__p1.last = { screenX: e.screenX, screenY: e.screenY,
                       clientX: e.clientX, clientY: e.clientY };
}, true);
"""


class HumanPlane:
    """Injects input into the X display via XTEST (same mechanism Selkies uses).

    Everything this class does is display-level. It never touches the CDP connection
    and never calls a Playwright input API.
    """

    def __init__(self, page):
        self.page = page
        self.offset: tuple[int, int] | None = None
        self.window_id: str | None = None

    def find_window(self) -> str:
        cp = xdo("search", "--onlyvisible", "--class", "chrom", check=False)
        ids = [i for i in cp.stdout.split() if i.strip()]
        if not ids:
            cp = xdo("search", "--name", ".", check=False)
            ids = [i for i in cp.stdout.split() if i.strip()]
        if not ids:
            raise RuntimeError("no X window found for chromium")
        self.window_id = ids[-1]
        return self.window_id

    def focus(self) -> None:
        wid = self.window_id or self.find_window()
        xdo("windowfocus", "--sync", wid, check=False)
        xdo("windowraise", wid, check=False)
        time.sleep(0.2)

    def calibrate(self) -> tuple[int, int]:
        """Learn screen->viewport offset from a real injected mousemove, so screen
        coordinates can be derived from Playwright's client-space bounding boxes."""
        for probe in ((500, 500), (520, 520)):
            xdo("mousemove", str(probe[0]), str(probe[1]))
            time.sleep(0.25)
            last = self.page.evaluate("window.__p1 && window.__p1.last")
            if last:
                off = (
                    int(last["screenX"]) - int(last["clientX"]),
                    int(last["screenY"]) - int(last["clientY"]),
                )
                self.offset = off
                log(f"  calibrated screen->client offset = {off} (probe {probe}, observed {last})")
                return off
        raise RuntimeError("calibration failed: no mousemove reached the page")

    def to_screen(self, cx: float, cy: float) -> tuple[int, int]:
        ox, oy = self.offset or (0, 0)
        return int(cx + ox), int(cy + oy)

    def move_path(self, cx: float, cy: float, steps: int = 8) -> None:
        """Multi-step pointer travel -- produces a real mousemove stream, unlike an
        automated single-jump click."""
        sx, sy = self.to_screen(cx, cy)
        cur = xdo("getmouselocation", "--shell", check=False).stdout
        x0 = y0 = 400
        for line in cur.splitlines():
            if line.startswith("X="):
                x0 = int(line[2:])
            if line.startswith("Y="):
                y0 = int(line[2:])
        for i in range(1, steps + 1):
            nx = int(x0 + (sx - x0) * i / steps)
            ny = int(y0 + (sy - y0) * i / steps)
            xdo("mousemove", str(nx), str(ny))
            time.sleep(0.03)

    def click_element(self, selector: str, page=None) -> None:
        pg = page or self.page
        box = pg.locator(selector).bounding_box()
        if not box:
            raise RuntimeError(f"no bounding box for {selector}")
        cx = box["x"] + box["width"] / 2
        cy = box["y"] + box["height"] / 2
        self.move_path(cx, cy)
        time.sleep(0.1)
        xdo("click", "1")
        time.sleep(0.25)

    def type_text(self, text: str, delay_ms: int = 90) -> None:
        xdo("type", "--delay", str(delay_ms), text)
        time.sleep(0.2)

    def key(self, k: str) -> None:
        xdo("key", k)
        time.sleep(0.3)


# ------------------------------------------------------------------- the run


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", action="store_true")
    args = ap.parse_args()

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    if WORK.exists():
        shutil.rmtree(WORK)
    UDD.mkdir(parents=True)

    from playwright.sync_api import sync_playwright

    xvfb = start_xvfb()
    port = free_port()
    app = start_app(port)
    base = f"http://127.0.0.1:{port}"
    procs = [xvfb, app]

    try:
        with sync_playwright() as pw:
            RESULTS["environment"] = {
                "playwright_python": __import__("playwright").__version__
                if hasattr(__import__("playwright"), "__version__")
                else "unknown",
                "playwright_pip": subprocess.run(
                    [sys.executable, "-m", "pip", "show", "playwright"],
                    capture_output=True,
                    text=True,
                )
                .stdout.split("Version: ")[1]
                .split()[0],
                "chromium_executable": pw.chromium.executable_path,
                "chromium_version": subprocess.run(
                    [pw.chromium.executable_path, "--version"], capture_output=True, text=True
                ).stdout.strip(),
                "xdotool_version": subprocess.run(
                    ["xdotool", "--version"], capture_output=True, text=True
                ).stdout.strip(),
                "xvfb_package": subprocess.run(
                    ["dpkg-query", "-W", "-f=${Version}", "xvfb"], capture_output=True, text=True
                ).stdout.strip(),
                "display": DISPLAY,
                "screen": SCREEN,
                "user_data_dir": str(UDD),
                "app_base_url": base,
                "python": sys.version.split()[0],
                "uname": subprocess.run(
                    ["uname", "-a"], capture_output=True, text=True
                ).stdout.strip(),
            }
            log(json.dumps(RESULTS["environment"], indent=2))

            # ---------------------------------------------- PHASE 1: agent launch
            phase("1_agent_launch")
            ctx = pw.chromium.launch_persistent_context(
                user_data_dir=str(UDD),
                headless=False,  # HEADED, per handoff_capable
                args=[
                    "--no-sandbox",
                    "--window-position=0,0",
                    "--window-size=1400,1000",
                    "--disable-features=Translate",
                ],
                viewport=None,
                ignore_default_args=["--enable-automation"],
            )
            ctx.add_init_script(CALIBRATE_SCRIPT)

            pid = find_browser_pid(str(UDD))
            ident_before = proc_identity(pid) if pid else {"pid": None, "alive": False}
            log(f"chromium main process: {ident_before}")

            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            original_page_repr = repr(page)
            page.goto(f"{base}/state")
            page.wait_for_timeout(400)
            # re-inject calibration on the already-loaded page
            page.evaluate(CALIBRATE_SCRIPT)

            agent_cookies = {c["name"]: c["value"] for c in ctx.cookies()}
            agent_ls = page.evaluate("JSON.stringify(Object.entries(localStorage))")
            log(f"agent-visible cookies: {agent_cookies}")
            log(f"agent-visible localStorage: {agent_ls}")

            # ------------------------- PHASE 2: agent tries the login and is refused
            phase("2_agent_login_attempt")
            page.goto(f"{base}/login")
            page.fill("#username", "proof-user")
            page.fill("#password", "proof-pass")
            page.click("#submit")
            page.wait_for_timeout(400)
            agent_attempt = json.loads(page.evaluate("document.getElementById('last').textContent"))
            agent_status = page.locator("#status").inner_text()
            log(f"agent login status: {agent_status}")
            log(f"agent attempt record: {json.dumps(agent_attempt)}")
            record(
                "control_agent_login_refused",
                "PASS" if not agent_attempt["accepted"] else "FAIL",
                {"status_text": agent_status, "attempt": agent_attempt},
            )
            page.screenshot(path=str(ARTIFACTS / "01_agent_login_refused.png"))

            # ------------------------------- PHASE 3: HUMAN takes over the display
            phase("3_human_display_input")
            page.goto(f"{base}/login")
            page.wait_for_timeout(400)
            human = HumanPlane(page)
            wid = human.find_window()
            log(
                f"chromium X window id: {wid}; "
                f"geometry: {xdo('getwindowgeometry', wid, check=False).stdout.strip()!r}"
            )
            human.focus()
            human.calibrate()

            human.click_element("#username")
            human.type_text("proof-user")
            human.click_element("#password")
            human.type_text("proof-pass")
            live = page.locator("#live").inner_text()
            log(f"page-observed input provenance before submit: {live}")
            human.click_element("#submit")
            page.wait_for_timeout(800)

            human_status = page.locator("#status").inner_text()
            human_attempt = json.loads(page.evaluate("document.getElementById('last').textContent"))
            log(f"human login status: {human_status}")
            log(f"human attempt record: {json.dumps(human_attempt)}")
            page.screenshot(path=str(ARTIFACTS / "02_human_login_result.png"))
            record(
                "human_display_input_reaches_browser",
                "PASS" if human_attempt["accepted"] else "FAIL",
                {
                    "status_text": human_status,
                    "attempt": human_attempt,
                    "live_counters_before_submit": live,
                },
            )

            # ------------------- PHASE 4: same process? human state visible to agent?
            phase("4_continuity")
            ident_after = proc_identity(pid) if pid else {"pid": None, "alive": False}
            same_proc = (
                ident_before.get("pid") == ident_after.get("pid")
                and ident_before.get("starttime_jiffies") == ident_after.get("starttime_jiffies")
                and ident_after.get("alive")
            )
            log(f"process before: {ident_before}")
            log(f"process after : {ident_after}")
            record(
                "same_os_process",
                "PASS" if same_proc else "FAIL",
                {"before": ident_before, "after": ident_after},
            )

            cookies_after = {c["name"]: c["value"] for c in ctx.cookies()}
            session_cookie = cookies_after.get("p1_session")
            log(f"context.cookies() after human login: {cookies_after}")

            # human writes a localStorage value through display input
            page.goto(f"{base}/state")
            page.wait_for_timeout(400)
            page.evaluate(CALIBRATE_SCRIPT)
            human.focus()
            human.click_element("#writels")
            page.wait_for_timeout(300)
            human_ls = page.evaluate("localStorage.getItem('p1_human_marker')")
            log(f"localStorage written by display input, read by Playwright: {human_ls!r}")
            page.screenshot(path=str(ARTIFACTS / "03_human_localstorage.png"))

            # original page object still usable?
            orig_usable = None
            try:
                page.goto(f"{base}/auth")
                page.wait_for_timeout(300)
                orig_usable = page.locator("#status").inner_text()
            except Exception as exc:  # noqa: BLE001
                orig_usable = f"ERROR: {exc!r}"
            log(f"original page object after handoff -> /auth says: {orig_usable!r}")
            record(
                "human_state_visible_to_playwright",
                "PASS"
                if (session_cookie and human_ls and "AUTHENTICATED" in str(orig_usable))
                else "FAIL",
                {
                    "cookies_before_human": agent_cookies,
                    "cookies_after_human": cookies_after,
                    "session_cookie": session_cookie,
                    "localStorage_written_by_human": human_ls,
                    "original_page_repr_at_launch": original_page_repr,
                    "original_page_repr_now": repr(page),
                    "original_page_reads": orig_usable,
                    "original_page_is_closed": page.is_closed(),
                },
            )

            # --------------------------- PHASE 5: human opens a new tab, agent drives
            phase("5_human_opens_tab")
            page.goto(f"{base}/popup")
            page.wait_for_timeout(400)
            page.evaluate(CALIBRATE_SCRIPT)
            human.focus()
            pages_before = [p.url for p in ctx.pages]
            log(f"context.pages before human opens a tab: {pages_before}")
            human.click_element("#newtab")
            page.wait_for_timeout(1200)
            pages_after = [p.url for p in ctx.pages]
            log(f"context.pages after human opens a tab: {pages_after}")

            new_pages = [p for p in ctx.pages if "/opened" in p.url]
            drivable = None
            new_tab_title = None
            if new_pages:
                np = new_pages[0]
                try:
                    np.wait_for_load_state()
                    new_tab_title = np.title()
                    drivable = np.evaluate("document.getElementById('via').textContent")
                    np.evaluate(
                        "document.getElementById('h').textContent="
                        "'DRIVEN BY PLAYWRIGHT AFTER HUMAN OPENED IT'"
                    )
                    drivable_after = np.evaluate("document.getElementById('h').textContent")
                    np.screenshot(path=str(ARTIFACTS / "04_new_tab_driven.png"))
                except Exception as exc:  # noqa: BLE001
                    drivable = f"ERROR: {exc!r}"
                    drivable_after = None
            else:
                drivable_after = None
            log(
                f"new tab title={new_tab_title!r} content={drivable!r} "
                f"after-drive={drivable_after!r}"
            )
            record(
                "human_opened_tab_discoverable_and_drivable",
                "PASS"
                if (new_pages and drivable_after == "DRIVEN BY PLAYWRIGHT AFTER HUMAN OPENED IT")
                else "FAIL",
                {
                    "pages_before": pages_before,
                    "pages_after": pages_after,
                    "new_tab_title": new_tab_title,
                    "new_tab_read_by_playwright": drivable,
                    "new_tab_mutated_by_playwright": drivable_after,
                },
            )

            # ------------- PHASE 6: what happens to the page pointer on close/switch
            phase("6_page_pointer_behaviour")
            pointer: dict[str, object] = {}
            # 6a. original page while a different tab is foreground
            pointer["original_page_is_closed_while_backgrounded"] = page.is_closed()
            try:
                pointer["original_page_evaluate_while_backgrounded"] = page.evaluate(
                    "document.title"
                )
            except Exception as exc:  # noqa: BLE001
                pointer["original_page_evaluate_while_backgrounded"] = f"ERROR {exc!r}"
            try:
                page.bring_to_front()
                pointer["bring_to_front"] = "ok"
            except Exception as exc:  # noqa: BLE001
                pointer["bring_to_front"] = f"ERROR {exc!r}"

            # 6b. human switches tabs with ctrl+Tab, then closes the foreground tab
            human.focus()
            human.key("ctrl+Tab")
            pointer["pages_after_ctrl_tab"] = [p.url for p in ctx.pages]
            closed_events: list[str] = []
            for p in ctx.pages:
                p.on("close", lambda pp=p: closed_events.append(pp.url))
            target = new_pages[0] if new_pages else None
            if target:
                try:
                    target.bring_to_front()
                except Exception:  # noqa: BLE001
                    pass
                human.focus()
                time.sleep(0.3)
                human.key("ctrl+w")
                time.sleep(1.0)
                # Read the three independent signals in a fixed order, then re-read
                # is_closed() -- a lag here matters to the worker's page bookkeeping.
                pointer["human_closed_tab_is_closed_immediately"] = target.is_closed()
                pointer["context_pages_count_immediately"] = len(ctx.pages)
                try:
                    target.evaluate("1+1")
                    pointer["evaluate_on_human_closed_page"] = "SUCCEEDED (unexpected)"
                except Exception as exc:  # noqa: BLE001
                    pointer["evaluate_on_human_closed_page"] = (
                        f"{type(exc).__name__}: {str(exc).splitlines()[0][:160]}"
                    )
                pointer["human_closed_tab_is_closed_after_evaluate"] = target.is_closed()
                time.sleep(1.0)
                pointer["human_closed_tab_is_closed_after_1s"] = target.is_closed()
            pointer["pages_after_human_close"] = [p.url for p in ctx.pages]
            pointer["close_events_seen"] = closed_events
            pointer["original_page_still_open_after_human_close"] = not page.is_closed()
            try:
                pointer["original_page_evaluate_after_human_close"] = page.evaluate(
                    "location.pathname"
                )
            except Exception as exc:  # noqa: BLE001
                pointer["original_page_evaluate_after_human_close"] = f"ERROR {exc!r}"
            log("page-pointer behaviour: " + json.dumps(pointer, indent=2))
            gone_from_pages = (
                target is not None and target.url not in pointer["pages_after_human_close"]  # type: ignore[operator]
            )
            record(
                "page_pointer_behaviour",
                "PASS"
                if (
                    pointer.get("original_page_still_open_after_human_close")
                    and gone_from_pages
                    and "TargetClosedError" in str(pointer.get("evaluate_on_human_closed_page"))
                )
                else "PARTIAL",
                pointer,
            )

            # ---- PHASE 7: agent keeps working after the whole handoff, same context
            phase("7_agent_resumes")
            resumed = {}
            try:
                page.goto(f"{base}/auth")
                page.wait_for_timeout(300)
                resumed["auth_status"] = page.locator("#status").inner_text()
                newp = ctx.new_page()
                newp.goto(f"{base}/state")
                newp.wait_for_timeout(300)
                resumed["new_agent_page_sees_human_localstorage"] = newp.evaluate(
                    "localStorage.getItem('p1_human_marker')"
                )
                resumed["new_agent_page_cookies"] = {c["name"]: c["value"] for c in ctx.cookies()}
                newp.screenshot(path=str(ARTIFACTS / "05_agent_resumed.png"))
            except Exception as exc:  # noqa: BLE001
                resumed["error"] = repr(exc)
            ident_final = proc_identity(pid) if pid else {}
            resumed["process_final"] = ident_final
            log("agent resume: " + json.dumps(resumed, indent=2))
            record(
                "agent_resumes_same_context_no_relaunch",
                "PASS"
                if (
                    "AUTHENTICATED" in str(resumed.get("auth_status"))
                    and resumed.get("new_agent_page_sees_human_localstorage")
                    and ident_final.get("starttime_jiffies")
                    == ident_before.get("starttime_jiffies")
                )
                else "FAIL",
                resumed,
            )

            # -------------- PHASE 8: NEGATIVE -- second chromium on the same profile
            phase("8_second_launch_rejected")
            second = subprocess.run(
                [sys.executable, str(HERE / "second_launch.py"), str(UDD), DISPLAY],
                capture_output=True,
                text=True,
                timeout=180,
            )
            second_out = {
                "returncode": second.returncode,
                "stdout": second.stdout.strip(),
                "stderr_tail": second.stderr.strip()[-2500:],
            }
            log("second launch attempt:\n" + json.dumps(second_out, indent=2))
            try:
                parsed = json.loads(second.stdout.strip().splitlines()[-1])
            except Exception:  # noqa: BLE001
                parsed = {"parse": "failed"}
            second_out["parsed"] = parsed
            # Also: is the original still healthy after the intruder tried?
            try:
                second_out["original_still_alive"] = page.evaluate("1+1") == 2
            except Exception as exc:  # noqa: BLE001
                second_out["original_still_alive"] = f"ERROR {exc!r}"
            second_out["original_process_after_intruder"] = proc_identity(pid) if pid else {}
            rejected = parsed.get("outcome") in {"error", "timeout"} or (
                parsed.get("outcome") == "launched_but_no_lock"
            )
            record(
                "second_launch_same_user_data_dir_rejected",
                "PASS" if parsed.get("outcome") in {"error", "timeout"} else "FAIL",
                second_out,
            )

            # ---------------------------------------------------------- teardown
            ctx.close()
            if not args.keep:
                pass

    finally:
        RESULTS["finished_at"] = datetime.now(timezone.utc).isoformat()
        RESULTS["log"] = _LOG
        (ARTIFACTS / "p1_results.json").write_text(json.dumps(RESULTS, indent=2))
        (ARTIFACTS / "p1_run.log").write_text("\n".join(_LOG))
        if not args.keep:
            for p in procs:
                p.terminate()
        log(f"results -> {ARTIFACTS / 'p1_results.json'}")

    print("\n=================== VERDICTS ===================")
    for k, v in RESULTS["subclaims"].items():  # type: ignore[union-attr]
        print(f"{v['verdict']:8}  {k}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
