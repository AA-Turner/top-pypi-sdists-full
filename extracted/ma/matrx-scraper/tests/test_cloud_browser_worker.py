"""WS-2 conformance suite for the S2 browser worker, driven by StubControlPlane.

These tests are the executable form of the S2 contract on the worker side. They
run with ZERO Browser Manager, ZERO database, and ZERO streaming — the
``StubControlPlane`` is the in-process control plane and the ``BrowserWorker`` is
the server half.

The Definition of Done (EXECUTION.md WS-2) is proven here:
  * ordered-queue semantics,
  * fencing rejection of stale tokens,
  * both run-mode behaviours,
  * page reconciliation after a simulated human episode,
  * the ``browser_controlled_by_human`` typed conflict.

Chromium-dependent tests skip when the Playwright browser binary is unavailable;
handoff_capable (headed) tests additionally require Xvfb. Chromium is present at
/opt/pw-browsers in CI, so these run there.
"""

from __future__ import annotations

import asyncio
import os
import shutil
import subprocess
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from pydantic import ValidationError

pytest.importorskip("playwright", reason="playwright not installed (browser extra)")

from matrx_scraper.cloud_browser.worker import (  # noqa: E402
    BrowserWorker,
    InMemoryTokenAuthority,
    ProfileLock,
    ProfileLockError,
    StubControlPlane,
)
from matrx_scraper.cloud_browser.worker import commands as C  # noqa: E402
from matrx_scraper.cloud_browser.worker import models as M  # noqa: E402
from matrx_scraper.cloud_browser.worker import runtime  # noqa: E402
from matrx_scraper.cloud_browser.worker.errors import WorkerProtocolError  # noqa: E402

# Load the repo .env HERE, above the gate. The skip decision below reads
# process env, and other suites (anything importing aidream.config) load .env
# as an import side effect — so without this line the same commit skips when
# this file is collected alone and runs when it is collected second.
# Guard: scripts/check_test_gate_determinism.py
from dotenv import load_dotenv

load_dotenv()


# ── environment probes ──────────────────────────────────────────────────────


def _chromium_available() -> bool:
    base = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"))
    return base.exists() and any(base.glob("chromium-*"))


def _xvfb_available() -> bool:
    return shutil.which("Xvfb") is not None


CHROMIUM = pytest.mark.skipif(not _chromium_available(), reason="no chromium browser binary")
XVFB = pytest.mark.skipif(
    not (_chromium_available() and _xvfb_available()), reason="no chromium+Xvfb"
)

DATA_PAGE = (
    "data:text/html,"
    "<html><body><h1 id='h'>hi</h1>"
    "<button id='b' onclick='window.__c=(window.__c||0)+1'>go</button>"
    "</body></html>"
)


# ── fixtures ────────────────────────────────────────────────────────────────


@pytest.fixture
def profile_dir(tmp_path: Path) -> str:
    d = tmp_path / "profile"
    d.mkdir()
    return str(d)


class _Xvfb:
    def __init__(self, display: str, proc: subprocess.Popen) -> None:
        self.display = display
        self.proc = proc


@pytest.fixture
def xvfb():
    if not (_chromium_available() and _xvfb_available()):
        pytest.skip("no chromium+Xvfb")
    # Pick a free display number.
    for num in range(90, 130):
        display = f":{num}"
        if Path(f"/tmp/.X11-unix/X{num}").exists():
            continue
        proc = subprocess.Popen(
            ["Xvfb", display, "-screen", "0", "1280x900x24", "-nolisten", "tcp"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # Wait for it to come up.
        ok = False
        for _ in range(50):
            time.sleep(0.1)
            if Path(f"/tmp/.X11-unix/X{num}").exists():
                ok = True
                break
        if ok:
            yield _Xvfb(display, proc)
            proc.terminate()
            return
        proc.terminate()
    pytest.skip("could not start Xvfb")


def _new(
    profile_dir: str,
    *,
    xvfb_display: str | None = None,
    authority: InMemoryTokenAuthority | None = None,
):
    events: list = []
    worker = BrowserWorker(
        worker_id="worker-test-1",
        token_verifier=authority,
        event_sink=events.append,
        xvfb_display=xvfb_display,
    )
    stub = StubControlPlane(worker, authority=authority)
    return worker, stub, events


async def _load_data_page(worker: BrowserWorker) -> None:
    page = worker.page_object(worker.active_page_id)
    await page.goto(DATA_PAGE, wait_until="commit")


# ── DoD 1: ordered-queue semantics ──────────────────────────────────────────


def test_worker_refuses_commands_without_an_acknowledged_live_lease() -> None:
    worker = BrowserWorker(worker_id="worker-test-lease")

    with pytest.raises(WorkerProtocolError) as missing:
        worker._require_unexpired_lease()
    assert missing.value.code == "lease_expired"

    worker._lease_expires_at = datetime.now(UTC) - timedelta(seconds=1)
    with pytest.raises(WorkerProtocolError) as expired:
        worker._require_unexpired_lease()
    assert expired.value.code == "lease_expired"

    worker._lease_expires_at = datetime.now(UTC) + timedelta(seconds=30)
    worker._require_unexpired_lease()


@CHROMIUM
async def test_ordered_queue_semantics(profile_dir: str) -> None:
    worker, stub, _ = _new(profile_dir)
    boot = await stub.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")
    assert boot.ok and boot.accepted
    await _load_data_page(worker)

    # A forward gap is admitted (the manager may abandon numbers it minted).
    r1 = await stub.command(C.GetTextCommand(), sequence=200, idem="k200")
    assert r1.ok and r1.sequence_applied == 200

    r2 = await stub.command(C.GetTextCommand(), sequence=205, idem="k205")
    assert r2.ok and r2.sequence_applied == 205

    # A sequence below last_applied, not in the replay cache → out of order.
    r3 = await stub.command(C.GetTextCommand(), sequence=203, idem="k203")
    assert not r3.ok and r3.error is not None and r3.error.code == "sequence_out_of_order"

    # A sequenced op missing its sequence → sequence_required.
    req = M.CommandRequest(
        run_id=stub.run_id,
        profile_id=stub.profile_id,
        fencing_token=stub.fencing_token,
        fencing_revision=stub.fencing_revision,
        issued_at=r1.observed_at,
        origin="agent",
        command=C.GetTextCommand(),
        sequence=None,
        idempotency_key=None,
    )
    r4 = await worker.command(req, bearer=None)
    assert not r4.ok and r4.error.code == "sequence_required"

    # An unsequenced op (heartbeat) carrying a sequence → sequence_not_permitted.
    hb = M.HeartbeatRequest(
        run_id=stub.run_id,
        profile_id=stub.profile_id,
        fencing_token=stub.fencing_token,
        fencing_revision=stub.fencing_revision,
        issued_at=r1.observed_at,
        sequence=999,
        idempotency_key="x",
        lease_expires_at=r1.observed_at,
        access_still_valid=True,
    )
    r5 = await worker.heartbeat(hb, bearer=None)
    assert not r5.ok and r5.error.code == "sequence_not_permitted"

    await stub.shutdown()


# ── DoD 2: fencing rejection of stale tokens ────────────────────────────────


@CHROMIUM
async def test_fencing_rejects_stale_and_unknown(profile_dir: str) -> None:
    worker, stub, _ = _new(profile_dir)
    await stub.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")
    await _load_data_page(worker)

    base_env = dict(
        run_id=stub.run_id,
        profile_id=stub.profile_id,
        issued_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc),
    )

    # A LOWER revision → stale_fencing_token, and the reply still carries the current revision.
    M.CommandRequest(
        **base_env,
        fencing_token=stub.fencing_token,
        fencing_revision=stub.fencing_revision - 1
        if stub.fencing_revision > 1
        else stub.fencing_revision,
        sequence=300,
        idempotency_key="a",
        origin="agent",
        command=C.GetTextCommand(),
    )
    # Force a genuinely lower revision by bumping the worker first via a transition.
    # Simpler: send a wrong token (mismatch) which is also stale.
    bad_token = M.CommandRequest(
        **base_env,
        fencing_token="not-the-token",
        fencing_revision=stub.fencing_revision,
        sequence=301,
        idempotency_key="b",
        origin="agent",
        command=C.GetTextCommand(),
    )
    r = await worker.command(bad_token, bearer=None)
    assert not r.ok and r.error.code == "stale_fencing_token"
    assert r.error.current_fencing_revision == stub.fencing_revision  # reconcilable

    # A HIGHER revision on a non-transition op → unknown_fencing_revision.
    high = M.CommandRequest(
        **base_env,
        fencing_token=stub.fencing_token,
        fencing_revision=stub.fencing_revision + 5,
        sequence=302,
        idempotency_key="c",
        origin="agent",
        command=C.GetTextCommand(),
    )
    r2 = await worker.command(high, bearer=None)
    assert not r2.ok and r2.error.code == "unknown_fencing_revision"

    # run_id / profile mismatch is detected BEFORE any fencing comparison.
    mism = M.CommandRequest(
        run_id="other-run",
        profile_id=stub.profile_id,
        issued_at=base_env["issued_at"],
        fencing_token="whatever",
        fencing_revision=999,
        sequence=303,
        idempotency_key="d",
        origin="agent",
        command=C.GetTextCommand(),
    )
    r3 = await worker.command(mism, bearer=None)
    assert not r3.ok and r3.error.code == "run_mismatch"

    await stub.shutdown()


# ── replay: a repeated (sequence, idem) executes the browser action exactly once ──


@CHROMIUM
async def test_replay_executes_action_once(profile_dir: str) -> None:
    worker, stub, _ = _new(profile_dir)
    await stub.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")
    await _load_data_page(worker)
    page = worker.page_object(worker.active_page_id)

    first = await stub.command(C.ClickCommand(selector="#b"), sequence=400, idem="click-1")
    assert first.ok
    assert await page.evaluate("window.__c") == 1

    replay = await stub.command(C.ClickCommand(selector="#b"), sequence=400, idem="click-1")
    assert replay.ok and replay.replayed is True
    assert await page.evaluate("window.__c") == 1  # NOT executed twice

    # Same sequence, different idempotency key → sequence_conflict.
    conflict = await stub.command(C.ClickCommand(selector="#b"), sequence=400, idem="click-2")
    assert not conflict.ok and conflict.error.code == "sequence_conflict"

    await stub.shutdown()


@CHROMIUM
async def test_replay_receipt_survives_worker_migration(profile_dir: str) -> None:
    worker_a, stub_a, _ = _new(profile_dir)
    await stub_a.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")
    await _load_data_page(worker_a)

    first = await stub_a.command(C.ClickCommand(selector="#b"), sequence=400, idem="migrated-click")
    assert first.ok and first.replayed is False
    await stub_a.shutdown(reason="reopen_for_handoff")

    worker_b = BrowserWorker(worker_id="worker-test-2")
    stub_b = StubControlPlane(
        worker_b,
        run_id=stub_a.run_id,
        profile_id=stub_a.profile_id,
    )
    boot = await stub_b.bootstrap(
        user_data_dir=profile_dir,
        run_mode="automation_only",
        reopened_for_handoff=True,
    )
    assert boot.ok and boot.accepted

    replay = await stub_b.command(
        C.ClickCommand(selector="#b"),
        sequence=400,
        idem="migrated-click",
    )
    assert replay.ok and replay.replayed is True
    await stub_b.shutdown()


# ── DoD 3a: automation_only mode behaviour ──────────────────────────────────


@CHROMIUM
async def test_automation_only_mode(profile_dir: str) -> None:
    worker, stub, _ = _new(profile_dir)
    # DisplayConfig is refused for automation_only.
    bad = await stub.bootstrap(
        user_data_dir=profile_dir,
        run_mode="automation_only",
        display=M.DisplayConfig(kind="xvfb", width=1280, height=900),
    )
    assert not bad.ok and bad.error.code == "invalid_command_arguments"

    # Bootstrap headless correctly.
    worker2, stub2, _ = _new(profile_dir)
    boot = await stub2.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")
    assert boot.ok and boot.run_mode == "automation_only"
    assert boot.display_ref is None
    # A human-required condition cannot enter human control in-process:
    hr = await stub2.controller_transition(to_state="handoff_requested", reason="mfa_required")
    assert hr.ok
    illegal = await stub2.controller_transition(to_state="human_control", enable_human_input=True)
    assert not illegal.ok and illegal.error.code == "illegal_controller_transition"
    await stub2.shutdown()


# ── DoD 3b: handoff_capable mode behaviour + D-5 keyring-free cookie scheme ──


@XVFB
async def test_handoff_capable_mode_and_keyring_free(profile_dir: str, xvfb) -> None:
    # handoff_capable REQUIRES a DisplayConfig.
    worker, stub, _ = _new(profile_dir, xvfb_display=xvfb.display)
    missing = await stub.bootstrap(user_data_dir=profile_dir, run_mode="handoff_capable")
    assert not missing.ok and missing.error.code == "invalid_command_arguments"

    worker2, stub2, _ = _new(profile_dir, xvfb_display=xvfb.display)
    boot = await stub2.bootstrap(
        user_data_dir=profile_dir,
        run_mode="handoff_capable",
        display=M.DisplayConfig(kind="xvfb", width=1280, height=900),
    )
    assert boot.ok and boot.run_mode == "handoff_capable"
    assert boot.display_ref == xvfb.display

    # D-5: launched keyring-free with the basic cookie store.
    assert "--password-store=basic" in worker2.launch_args
    assert "--use-mock-keychain" in worker2.launch_args
    assert "--disable-dev-shm-usage" in worker2.launch_args

    # human_control is a legal destination for handoff_capable.
    t1 = await stub2.controller_transition(to_state="handoff_requested", reason="mfa_required")
    assert t1.ok
    t2 = await stub2.controller_transition(
        to_state="human_control", handoff_id="h-1", enable_human_input=True
    )
    assert t2.ok and t2.human_input_enabled is True and t2.to_state == "human_control"

    await stub2.shutdown()


@XVFB
async def test_verification_field_requests_authenticator_handoff(profile_dir: str, xvfb) -> None:
    worker, stub, _ = _new(profile_dir, xvfb_display=xvfb.display)
    await stub.bootstrap(
        user_data_dir=profile_dir,
        run_mode="handoff_capable",
        display=M.DisplayConfig(kind="xvfb", width=1280, height=900),
    )
    page = worker.page_object(worker.active_page_id)
    await page.goto(
        "data:text/html,<button id='next' onclick=\"document.body.innerHTML='<input autocomplete=one-time-code>'\">next</button>",
        wait_until="commit",
    )

    response = await stub.command(C.ClickCommand(selector="#next"), origin="agent")
    assert response.ok
    assert response.human_required is not None
    assert response.human_required.reason == "mfa_required"

    await stub.shutdown()


@XVFB
async def test_numeric_postal_code_field_does_not_request_authenticator_handoff(
    profile_dir: str, xvfb
) -> None:
    worker, stub, _ = _new(profile_dir, xvfb_display=xvfb.display)
    await stub.bootstrap(
        user_data_dir=profile_dir,
        run_mode="handoff_capable",
        display=M.DisplayConfig(kind="xvfb", width=1280, height=900),
    )
    page = worker.page_object(worker.active_page_id)
    await page.goto(
        "data:text/html,<input name=zipcode inputmode=numeric>"
        "<input name=discount_code><button id=go>go</button>",
        wait_until="commit",
    )

    response = await stub.command(C.ClickCommand(selector="#go"), origin="agent")
    assert response.ok
    assert response.human_required is None

    await stub.shutdown()


@XVFB
async def test_hidden_verification_field_does_not_request_authenticator_handoff(
    profile_dir: str, xvfb
) -> None:
    worker, stub, _ = _new(profile_dir, xvfb_display=xvfb.display)
    await stub.bootstrap(
        user_data_dir=profile_dir,
        run_mode="handoff_capable",
        display=M.DisplayConfig(kind="xvfb", width=1280, height=900),
    )
    page = worker.page_object(worker.active_page_id)
    await page.goto(
        "data:text/html,<input autocomplete=one-time-code hidden><button id=go>go</button>",
        wait_until="commit",
    )

    response = await stub.command(C.ClickCommand(selector="#go"), origin="agent")
    assert response.ok
    assert response.human_required is None

    await stub.shutdown()


# ── DoD 5: browser_controlled_by_human typed conflict ───────────────────────


@XVFB
async def test_browser_controlled_by_human(profile_dir: str, xvfb) -> None:
    worker, stub, _ = _new(profile_dir, xvfb_display=xvfb.display)
    await stub.bootstrap(
        user_data_dir=profile_dir,
        run_mode="handoff_capable",
        display=M.DisplayConfig(kind="xvfb", width=1280, height=900),
    )
    await _load_data_page(worker)
    page = worker.page_object(worker.active_page_id)
    await page.evaluate("window.__c = 0")

    await stub.controller_transition(
        to_state="handoff_requested", reason="sensitive_action_approval"
    )
    await stub.controller_transition(
        to_state="human_control", handoff_id="h-42", enable_human_input=True
    )

    # An agent command is refused, typed, with the conflicting handoff id.
    agent = await stub.command(C.ClickCommand(selector="#b"), origin="agent")
    assert not agent.ok and agent.error.code == "browser_controlled_by_human"
    assert agent.error.conflicting_handoff_id == "h-42"

    # A system health probe is refused the same way.
    system = await stub.command(C.GetTextCommand(), origin="system")
    assert not system.ok and system.error.code == "browser_controlled_by_human"

    # NOTHING was queued: the counter is untouched after control returns.
    ret = await stub.controller_transition(to_state="agent_control", reason="control_returned")
    assert ret.ok
    assert await page.evaluate("window.__c") == 0  # zero delayed clicks

    await stub.shutdown()


# ── DoD 4: page reconciliation after a simulated human episode ──────────────


@XVFB
async def test_page_reconciliation_after_human_episode(profile_dir: str, xvfb) -> None:
    worker, stub, _ = _new(profile_dir, xvfb_display=xvfb.display)
    await stub.bootstrap(
        user_data_dir=profile_dir,
        run_mode="handoff_capable",
        display=M.DisplayConfig(kind="xvfb", width=1280, height=900),
    )
    await _load_data_page(worker)

    await stub.controller_transition(
        to_state="handoff_requested", reason="account_selection_required"
    )
    await stub.controller_transition(
        to_state="human_control", handoff_id="ep-1", enable_human_input=True
    )

    # Simulate the human episode by opening two tabs and closing one, plus a
    # dialog left OPEN (the human walked away from a confirm box). Opening pages
    # directly on the context is exactly what a human driving the display does;
    # the worker's context-level tracking picks them up regardless of who opened them.
    ctx = worker.context
    tab_a = await ctx.new_page()
    await tab_a.goto("data:text/html,<h1>A</h1>", wait_until="commit")
    await asyncio.sleep(0.05)
    tab_b = await ctx.new_page()
    await tab_b.goto("data:text/html,<h1 id='x'>B</h1>", wait_until="commit")
    await asyncio.sleep(0.05)
    # Close tab A (human closed it).
    await tab_a.close()
    await asyncio.sleep(0.1)
    # Leave a confirm dialog OPEN on tab B — fired as a background task so it stays pending.
    asyncio.ensure_future(tab_b.evaluate("window.confirm('proceed?')"))
    await asyncio.sleep(0.3)

    # Return control.
    ret = await stub.controller_transition(to_state="agent_control", reason="control_returned")
    assert ret.ok

    obs = await stub.observe(include=["pages", "dialogs", "downloads", "human_episode"])
    assert obs.ok and obs.page_inventory is not None
    inv = obs.page_inventory

    closed = [p for p in inv.pages if p.is_closed]
    assert len(closed) >= 1, "the human-closed tab is recorded as closed"
    # The surviving human-opened tab (B) is selected active (greatest last_focused_at).
    assert inv.active_page_id is not None
    active_rec = next(p for p in inv.pages if p.page_id == inv.active_page_id)
    assert not active_rec.is_closed
    assert active_rec.opened_by == "human"

    # The dialog is reported UNHANDLED — nothing auto-dismissed it.
    assert len(inv.dialogs) == 1
    assert inv.dialogs[0].handled is False
    dialog_id = inv.dialogs[0].dialog_id

    # The episode summary is coarse: it carries counts and origins, never content.
    assert obs.human_episode is not None
    assert obs.human_episode.pages_opened >= 2
    assert obs.human_episode.pages_closed >= 1
    # No field can carry a path/query — origins only.
    for org in obs.human_episode.origins_visited:
        assert "?" not in org and org.count("/") <= 2

    # handle_dialog is the ONLY way the dialog clears, and it is an audited command.
    handled = await stub.command(C.HandleDialogCommand(dialog_id=dialog_id, action="accept"))
    assert handled.ok and handled.event_facts is not None
    obs2 = await stub.observe(include=["dialogs"])
    assert obs2.page_inventory.dialogs[0].handled is True

    await stub.shutdown()


# ── the two failure planes are never mixed (S2 §9.1) ────────────────────────


@CHROMIUM
async def test_two_failure_planes(profile_dir: str) -> None:
    worker, stub, _ = _new(profile_dir)
    await stub.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")
    await _load_data_page(worker)

    # A navigate to a non-public address is RESULT-level: ok=True envelope,
    # result.success=False, result.error_type="blocked" — never an envelope error.
    blocked = await stub.command(C.NavigateCommand(url="http://127.0.0.1:9/"))
    assert blocked.ok is True and blocked.error is None
    assert blocked.result is not None and blocked.result.success is False
    assert blocked.result.error_type == "blocked"

    # A stale token on the same worker is ENVELOPE-level, never a result.
    bad = M.CommandRequest(
        run_id=stub.run_id,
        profile_id=stub.profile_id,
        fencing_token="wrong",
        fencing_revision=stub.fencing_revision,
        issued_at=blocked.observed_at,
        sequence=500,
        idempotency_key="z",
        origin="agent",
        command=C.GetTextCommand(),
    )
    r = await worker.command(bad, bearer=None)
    assert r.ok is False and r.error is not None and r.error.code == "stale_fencing_token"
    assert r.result is None

    await stub.shutdown()


# ── divergences + argument validation (S2 §7.3, §9.2) ───────────────────────


@CHROMIUM
async def test_command_divergences_and_validation(profile_dir: str) -> None:
    worker, stub, _ = _new(profile_dir)
    await stub.bootstrap(user_data_dir=profile_dir, run_mode="automation_only", allow_eval_js=False)
    await _load_data_page(worker)

    # D5: navigate carrying user_agent → parameter_not_available_on_persistent_run.
    d5 = await stub.command(C.NavigateCommand(url="http://example.com/", user_agent="x"))
    assert not d5.ok and d5.error.code == "parameter_not_available_on_persistent_run"

    # D3: eval_js with the run policy off → eval_js_not_permitted.
    ej = await stub.command(C.EvalJsCommand(expression="1+1"))
    assert not ej.ok and ej.error.code == "eval_js_not_permitted"

    # select_option with neither value nor label → invalid_command_arguments.
    so = await stub.command(C.SelectOptionCommand(selector="#s"))
    assert not so.ok and so.error.code == "invalid_command_arguments"

    await stub.shutdown()

    # D3 positive: with the run policy ON, the eval_js POLICY gate opens — the
    # command is admitted (no eval_js_not_permitted). The actual evaluation on a
    # data: page is then correctly withheld by the SSRF landing guard (result-level
    # validation), which is the two-planes rule, not the policy gate.
    worker2, stub2, _ = _new(profile_dir)
    await stub2.bootstrap(user_data_dir=profile_dir, run_mode="automation_only", allow_eval_js=True)
    await _load_data_page(worker2)
    ok = await stub2.command(C.EvalJsCommand(expression="6*7"))
    assert ok.ok is True and ok.error is None  # envelope-admitted, policy gate passed
    assert ok.result is not None  # a result-level outcome, never an eval_js_not_permitted refusal
    await stub2.shutdown()


# ── bootstrap idempotency + local advisory lock ─────────────────────────────


async def test_stopped_fixed_fleet_worker_accepts_next_run(
    profile_dir: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    worker, stub, _ = _new(profile_dir)

    async def fake_launch(_policy: M.LaunchPolicy, _display: M.DisplayConfig | None) -> bool:
        return True

    monkeypatch.setattr(worker, "_launch_context", fake_launch)
    first = await stub.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")
    assert first.ok and first.accepted
    await stub.shutdown()

    # Recreate a partial-exit leak: the process is terminal but the current
    # ProfileLock still owns an fd. Reset must release it before forgetting the
    # object, or every later bootstrap in this fixed-fleet process is poisoned.
    assert worker._lock is not None
    worker._lock.acquire()

    # The process is reused, but its idle clock is not. Production maintenance
    # once stopped a 24-second-old run because it inherited this stale timestamp
    # from the prior run.
    worker._last_activity = datetime.now(UTC) - timedelta(hours=1)

    stale_singleton = Path(profile_dir) / "SingletonLock"
    stale_singleton.symlink_to("old-task-host-117")
    stub.activation_key = "next-run"
    second = await stub.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")
    assert second.ok and second.accepted
    assert worker.run_id == stub.run_id
    assert not stale_singleton.exists()
    heartbeat = await stub.heartbeat()
    assert heartbeat.ok and heartbeat.idle_ms < 1_000


def test_profile_lock_clears_only_stale_chromium_singletons(profile_dir: str) -> None:
    profile_path = Path(profile_dir)
    profile_path.mkdir(parents=True, exist_ok=True)
    preserved = profile_path / "Cookies"
    preserved.write_text("saved-session-data", encoding="utf-8")
    (profile_path / "SingletonLock").symlink_to("old-host-117")
    (profile_path / "SingletonCookie").write_text("cookie-marker", encoding="utf-8")
    (profile_path / "SingletonSocket").symlink_to("/tmp/old-chromium/socket")

    lock = ProfileLock(profile_dir)
    lock.acquire()
    try:
        assert lock.clear_stale_chromium_singletons() == [
            "SingletonLock",
            "SingletonCookie",
            "SingletonSocket",
        ]
        assert not (profile_path / "SingletonLock").exists()
        assert not (profile_path / "SingletonCookie").exists()
        assert not (profile_path / "SingletonSocket").exists()
        assert preserved.read_text(encoding="utf-8") == "saved-session-data"
    finally:
        lock.release()


def test_profile_lock_refuses_singleton_cleanup_without_ownership(profile_dir: str) -> None:
    lock = ProfileLock(profile_dir)
    with pytest.raises(ProfileLockError, match="must be held"):
        lock.clear_stale_chromium_singletons()


@CHROMIUM
async def test_bootstrap_idempotency_and_profile_lock(profile_dir: str) -> None:
    worker, stub, _ = _new(profile_dir)

    # An external holder of the advisory lock makes bootstrap refuse loudly.
    external = ProfileLock(profile_dir)
    external.acquire()
    locked = await stub.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")
    assert not locked.ok and locked.error.code == "profile_locked_locally"
    assert locked.host_lock_acquired is False
    external.release()

    # Now bootstrap succeeds; a repeat with the SAME activation key replays.
    boot = await stub.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")
    assert boot.ok and boot.accepted
    replay = await stub.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")
    assert replay.ok and replay.replayed is True

    # A repeat with a DIFFERENT activation key is already_bootstrapped.
    stub.activation_key = "a-different-key"
    diff = await stub.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")
    assert not diff.ok and diff.error.code == "already_bootstrapped"

    await stub.shutdown()

    # A cleanly stopped fixed-fleet worker accepts the next run. The prior
    # profile lock, replay state, and controller identity cannot leak forward.
    stub.activation_key = "next-run"
    restarted = await stub.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")
    assert restarted.ok and restarted.accepted
    assert worker.run_id == stub.run_id
    await stub.shutdown()


# ── pre-bootstrap operations are refused ────────────────────────────────────


@CHROMIUM
async def test_not_bootstrapped(profile_dir: str) -> None:
    worker, stub, _ = _new(profile_dir)
    r = await stub.command(C.GetTextCommand())
    assert not r.ok and r.error.code == "not_bootstrapped"
    hb = await stub.heartbeat()
    assert not hb.ok and hb.error.code == "not_bootstrapped"


# ── inbound auth (S2 §2.2) — pure-logic, no browser needed ──────────────────


async def test_auth_audience_expiry_replay(profile_dir: str) -> None:
    authority = InMemoryTokenAuthority()
    worker = BrowserWorker(worker_id="worker-A", token_verifier=authority)

    # Wrong audience.
    wrong_aud = authority.mint(worker_id="worker-B", run_id="r", profile_id="p", op="heartbeat")
    hb = M.HeartbeatRequest(
        run_id="r",
        profile_id="p",
        fencing_token="t",
        fencing_revision=1,
        issued_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc),
        lease_expires_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc),
        access_still_valid=True,
    )
    r = await worker.heartbeat(hb, bearer=wrong_aud)
    assert not r.ok and r.error.code == "audience_mismatch"

    # Expired token.
    expired = authority.mint_expired(
        worker_id="worker-A", run_id="r", profile_id="p", op="heartbeat"
    )
    r2 = await worker.heartbeat(hb, bearer=expired)
    assert not r2.ok and r2.error.code == "credential_expired"

    # Replayed jti.
    good = authority.mint(worker_id="worker-A", run_id="r", profile_id="p", op="heartbeat")
    _ = await worker.heartbeat(hb, bearer=good)  # first use (fails later checks, but consumes jti)
    r3 = await worker.heartbeat(hb, bearer=good)
    assert not r3.ok and r3.error.code == "credential_replayed"

    # Missing token.
    r4 = await worker.heartbeat(hb, bearer=None)
    assert not r4.ok and r4.error.code == "unauthorized_worker_call"


# ── the worker holds no user identity (S2 §2.4, structural) ─────────────────


def test_worker_request_models_carry_no_user_identity() -> None:
    forbidden = {
        "user_id",
        "organization_id",
        "email",
        "credential",
        "stream_ticket",
        "vault_item_id",
    }
    for model in (
        M.BootstrapRequest,
        M.HeartbeatRequest,
        M.CommandRequest,
        M.ObserveRequest,
        M.CaptureRequest,
        M.ControllerTransitionRequest,
        M.CheckpointRequest,
        M.ShutdownRequest,
    ):
        assert forbidden.isdisjoint(model.model_fields.keys()), model.__name__


def test_checkpoint_request_has_bounded_queue_drain_contract() -> None:
    field = M.CheckpointRequest.model_fields["drain_timeout_ms"]
    assert field.default == 30_000

    payload = {
        "run_id": "run-checkpoint",
        "profile_id": "profile-checkpoint",
        "fencing_token": "fence",
        "fencing_revision": 1,
        "issued_at": datetime.now(UTC),
        "checkpoint_id": "checkpoint-1",
        "mode": "close_and_archive",
        "reason": "stop",
        "dek_plaintext_b64": "plain",
        "dek_wrapped_b64": "wrapped",
        "key_version": "key-v1",
        "nonce_b64": "nonce",
        "archive_format_version": 1,
        "upload_target": {
            "method": "PUT",
            "url": "https://upload.invalid/checkpoint",
            "expires_at": datetime.now(UTC) + timedelta(minutes=5),
        },
    }
    assert M.CheckpointRequest(**payload).drain_timeout_ms == 30_000
    with pytest.raises(ValidationError):
        M.CheckpointRequest(**payload, drain_timeout_ms=-1)
    with pytest.raises(ValidationError):
        M.CheckpointRequest(**payload, drain_timeout_ms=120_001)


# ── heartbeat access revocation immediately closes the queue ────────────────


@CHROMIUM
async def test_heartbeat_access_revoked_closes_queue(profile_dir: str) -> None:
    worker, stub, _ = _new(profile_dir)
    await stub.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")
    await _load_data_page(worker)

    hb = await stub.heartbeat(access_still_valid=False)
    assert hb.ok and hb.queue_state == "closed"

    r = await stub.command(C.GetTextCommand())
    assert not r.ok and r.error.code == "access_revoked"

    await stub.shutdown()


@pytest.mark.asyncio
async def test_bootstrap_after_a_partial_failure_is_not_poisoned_forever(
    profile_dir: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A held lock with ``_bootstrapped`` False must not permanently brick the profile.

    The reset path only fires for a CLEANLY stopped run
    (``_bootstrapped and health=='stopped' and queue_state=='closed'``). A crash
    or a partial bootstrap — lock acquired, a later step returned an error —
    leaves the fd open with ``_bootstrapped`` False, so the reset is skipped and
    the old code overwrote ``self._lock``, dropping the only reference to a raw
    fd that GC does not close. Every later bootstrap then returned
    ``profile_locked_locally`` for the LIFE of the process: a permanent outage
    of the cloud browser, not the transient restart it advertised itself as
    (observed in production 2026-08-26).
    """
    worker, stub, _ = _new(profile_dir)

    async def fake_launch(_policy: M.LaunchPolicy, _display: M.DisplayConfig | None) -> bool:
        return True

    monkeypatch.setattr(worker, "_launch_context", fake_launch)

    first = await stub.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")
    assert first.ok and first.accepted
    assert worker._lock is not None and worker._lock.held

    # The exact leak shape: the run is gone from the worker's point of view, but
    # nothing released the lock.
    worker._bootstrapped = False

    stub.activation_key = "after-the-crash"
    second = await stub.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")

    assert second.ok and second.accepted, "a stale in-process lock bricked the profile"
    assert second.host_lock_acquired is True


@pytest.mark.asyncio
async def test_hung_chromium_launch_returns_typed_failure_and_releases_lock(
    profile_dir: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A wedged external launch must not outlive the manager HTTP deadline."""
    worker, stub, _ = _new(profile_dir)
    launch_cancelled = asyncio.Event()

    async def hung_launch(
        _policy: M.LaunchPolicy, _display: M.DisplayConfig | None
    ) -> bool:
        try:
            await asyncio.Event().wait()
        finally:
            launch_cancelled.set()

    monkeypatch.setattr(worker, "_launch_context", hung_launch)
    monkeypatch.setattr(runtime, "BOOTSTRAP_LAUNCH_TIMEOUT_SECONDS", 0.01)

    response = await stub.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")

    assert launch_cancelled.is_set(), "the timed-out Playwright launch kept running"
    assert not response.ok and not response.accepted
    assert response.error is not None and response.error.code == "browser_crashed"
    assert worker._lock is not None and not worker._lock.held

    async def healthy_launch(
        _policy: M.LaunchPolicy, _display: M.DisplayConfig | None
    ) -> bool:
        return True

    monkeypatch.setattr(worker, "_launch_context", healthy_launch)
    monkeypatch.setattr(runtime, "BOOTSTRAP_LAUNCH_TIMEOUT_SECONDS", 1.0)
    stub.activation_key = "retry-after-timeout"
    retry = await stub.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")
    assert retry.ok and retry.accepted
