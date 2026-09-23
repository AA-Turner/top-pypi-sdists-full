"""The worker's command plane must have a CEILING, and say what it was doing.

The break these guard: ``BrowserWorker.command`` held ``self._command_lock``
around the WHOLE of ``_execute_command`` with no deadline at all. The humanised
keystroke loop is O(len(text)) with no ceiling (~138 ms/char measured on real
Chromium), so a 1078-character ``type_text`` held that lock for 149 seconds —
while the aidream client's per-operation deadline is 65 s
(``aidream/services/cloud_browser/worker_client.py``). The caller therefore got
a transport timeout instead of an answer, and every other command on that
browser queued behind a lock nobody could take.

These run the REAL ``BrowserWorker.command`` and the REAL humanised type loop in
``matrx_scraper.ai_browser.humanize``. Only Playwright itself is replaced — the
page, mouse and keyboard are doubles that record keystrokes — so a command path
that stops enforcing its own ceiling fails here.
"""

from __future__ import annotations

import asyncio
import time
from datetime import UTC, datetime

import pytest

pytest.importorskip("playwright", reason="playwright not installed (browser extra)")

from matrx_scraper.cloud_browser.worker import BrowserWorker  # noqa: E402
from matrx_scraper.cloud_browser.worker import commands as C  # noqa: E402
from matrx_scraper.cloud_browser.worker import models as M  # noqa: E402
from matrx_scraper.cloud_browser.worker import runtime  # noqa: E402

# A real sentence a person would type into a support form — the Harbor Dental
# front desk asking about a patient's insurance claim. Long enough that the
# humanised loop cannot finish inside the test's ceiling.
CLAIM_NOTE = (
    "Our patient Marisol Tran came in for a crown seat on the fourteenth and her "
    "insurance still shows the claim as pending review, please advise."
)


class _Keyboard:
    def __init__(self) -> None:
        self.typed: list[str] = []

    async def type(self, ch: str) -> None:
        self.typed.append(ch)

    async def press(self, key: str) -> None:
        self.typed.append(f"<{key}>")


class _Mouse:
    async def move(self, x: float, y: float) -> None:
        return None

    async def down(self) -> None:
        return None

    async def up(self) -> None:
        return None


class _Locator:
    def __init__(self, box: dict[str, float] | None) -> None:
        self._box = box

    @property
    def first(self) -> _Locator:
        return self

    async def wait_for(self, *, state: str, timeout: float) -> None:
        return None

    async def scroll_into_view_if_needed(self, *, timeout: float) -> None:
        return None

    async def bounding_box(self) -> dict[str, float] | None:
        return self._box


class _Page:
    """A Playwright page stand-in. Everything the humanised loop calls is here;
    none of the loop's own logic (delays, ordering, per-character keystrokes) is."""

    def __init__(self) -> None:
        self.url = "https://dental-portal.invalid/claims/new"
        self.viewport_size = {"width": 1280, "height": 800}
        self.keyboard = _Keyboard()
        self.mouse = _Mouse()
        self._box = {"x": 40.0, "y": 120.0, "width": 320.0, "height": 34.0}

    def locator(self, selector: str) -> _Locator:
        return _Locator(self._box)

    async def inner_text(self, selector: str = "body") -> str:
        return "Claim submitted"


class _Session:
    def __init__(self, page: _Page) -> None:
        self.page = page


class _SessionRegistry:
    def __init__(self, session: _Session) -> None:
        self._session = session

    async def get(self, session_id: str) -> _Session:
        return self._session


def _admit(worker: BrowserWorker, monkeypatch) -> None:
    for name in (
        "_verify_bearer",
        "_require_bootstrapped",
        "_check_identity",
        "_check_fencing",
        "_require_unexpired_lease",
        "_guard_command_admission",
    ):
        monkeypatch.setattr(worker, name, lambda *a, **k: None)
    monkeypatch.setattr(worker, "_check_sequence", lambda req: None)
    monkeypatch.setattr(worker, "_admit_sequenced", lambda req, resp: None, raising=False)
    worker.run_id = "run-harbor-dental"
    worker.profile_id = "profile-harbor-dental"
    worker.fencing_revision = 1
    worker.run_mode = "automation_only"
    worker.health = "healthy"
    worker.queue_state = "open"
    worker.chromium_version = "test"


def _humanised_type_worker(monkeypatch) -> tuple[BrowserWorker, _Page]:
    worker = BrowserWorker(worker_id="worker-command-deadline")
    _admit(worker, monkeypatch)
    page = _Page()
    session = _Session(page)
    worker._session = session
    worker._session_mgr = _SessionRegistry(session)  # type: ignore[assignment]
    tracked = runtime._TrackedPage(
        "page-1", page, opener_page_id=None, kind="tab", opened_by="agent"
    )
    worker._pages = {"page-1": tracked}
    worker._active_page_id = "page-1"
    worker._policy = M.LaunchPolicy(run_mode="automation_only", humanize_input=True)
    # The landing gate resolves DNS; it is not what these guards are about.
    monkeypatch.setattr(runtime.A, "guard_landing", lambda page: _none())
    return worker, page


async def _none():
    return None


def _type_request(text: str) -> M.CommandRequest:
    return M.CommandRequest(
        run_id="run-harbor-dental",
        profile_id="profile-harbor-dental",
        fencing_token="fence",
        fencing_revision=1,
        sequence=1,
        issued_at=datetime.now(UTC),
        origin="agent",
        command=C.TypeTextCommand(selector="#claim-note", text=text),
    )


def test_the_command_ceiling_is_shorter_than_the_aidream_client_deadline() -> None:
    """65 s is the aidream client's per-operation timeout (worker_client.py:210).
    A worker ceiling at or above it means the caller times out in transport and
    never learns what the browser was doing."""
    assert M.COMMAND_TOTAL_TIMEOUT_SECONDS < 65.0


@pytest.mark.asyncio
async def test_a_runaway_humanised_type_is_ended_by_the_command_deadline(monkeypatch) -> None:
    """Break caught: no deadline anywhere on the command path. Without one this
    returns ok=True after the whole 150-character sentence is typed one key at a
    time, long past the ceiling."""
    monkeypatch.setattr(M, "COMMAND_TOTAL_TIMEOUT_SECONDS", 1.0)
    worker, page = _humanised_type_worker(monkeypatch)

    started = time.monotonic()
    response = await worker.command(_type_request(CLAIM_NOTE))
    elapsed = time.monotonic() - started

    assert response.ok is False, "a command that blew its ceiling must not report success"
    assert response.error is not None
    assert response.error.code == "command_deadline_exceeded"
    # The caller is told WHAT was running, not merely that time passed.
    assert response.error.stage == "humanize_type"
    assert elapsed < 4.0, f"the ceiling did not fire: the command ran {elapsed:.1f}s"
    # It really was typing: the loop got some way into the sentence and stopped.
    assert 0 < len(page.keyboard.typed) < len(CLAIM_NOTE)


@pytest.mark.asyncio
async def test_the_command_lock_is_free_after_a_deadline_so_the_browser_stays_usable(
    monkeypatch,
) -> None:
    """Break caught: the deadline releases the lock. A ceiling that leaves
    ``_command_lock`` held turns one slow type into a dead browser."""
    monkeypatch.setattr(M, "COMMAND_TOTAL_TIMEOUT_SECONDS", 1.0)
    worker, page = _humanised_type_worker(monkeypatch)

    timed_out = await worker.command(_type_request(CLAIM_NOTE))
    assert timed_out.ok is False

    assert worker._command_lock.locked() is False
    assert worker._in_flight == 0

    # And the very next command goes through: acquiring the lock does not hang.
    page.keyboard.typed.clear()
    follow_up = await asyncio.wait_for(worker.command(_type_request("ok")), timeout=5.0)
    assert follow_up.ok is True
    assert "".join(follow_up.result.typed if follow_up.result else "") == "ok"
