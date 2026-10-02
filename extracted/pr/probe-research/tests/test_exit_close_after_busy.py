"""A script that simply ends must close its run even when the exit drain hits a 503.

Live, 2026-09-27 (probe-research 0.186.1): scripts launched from Claude Code
that ended without ``finish()`` were left ``running`` until the reaper called
them ``crashed``, and a crash email went out about runs that had succeeded. The
same script from a plain shell closed ``completed``.

What happened, in order:

1. ``probe.log`` queued the point, and the detached outbox worker was started.
2. The script ended. The atexit hook (``fluent._finish_at_exit``) called
   ``finish()``, whose close drained the run's ops once.
3. That metric POST got 503 ``concurrent telemetry write``: the hardware
   inventory thread's ``PATCH /v1/runs/{id}`` held the run row, and the metric
   insert takes it ``NOWAIT``. Under a coding-agent session that PATCH also
   records the session in the same transaction, so it holds the row longer and
   the collision became the common case.
4. ``finish()`` raised ``run ... not closed``, and the hook swallowed it. No
   terminal status was sent, and none was queued.
5. The detached worker then delivered the point, so the outbox read empty and
   nothing looked wrong locally.

Plan item 0.2 (``finish()`` retries to one deadline, then queues the close
behind the data) is the fix. These tests pin the shipped symptom, the exit hook
under a Claude Code environment, which the ``finish()``-level tests do not
reach.
"""

from __future__ import annotations

import json

import pytest

import probe
from probe.sdk import fluent
from tests.conftest import make_client

_SESSION_ID = "0b9a2c6e-3f41-4d8e-9a57-1c2d3e4f5a6b"

#: What every process a Claude Code session launches inherits.
_CLAUDE_CODE_ENV = {
    "CLAUDECODE": "1",
    "CLAUDE_CODE_ENTRYPOINT": "cli",
    "CLAUDE_CODE_SESSION_ID": _SESSION_ID,
    "CLAUDE_CODE_CHILD_SESSION": "1",
    "CLAUDE_CODE_SESSION_ATTENDED": "1",
}

_TERMINAL = {"completed", "failed", "canceled", "crashed"}


@pytest.fixture(autouse=True)
def _clean_binding():
    """The fluent layer keeps process state on purpose; tests must not inherit it."""
    fluent._current.set(None)
    fluent._process_default = None
    fluent._exit_status = "completed"
    yield
    fluent._current.set(None)
    fluent._process_default = None


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    """A bare ``probe.init()`` builds a client on the fake backend with the
    production write mode: async, so the point is journaled and the FIRST
    attempt to deliver it is the exit drain's."""

    def factory(*_a, **_kw):
        return make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)

    monkeypatch.setattr(fluent, "Client", factory)
    app.seed_experiment("e1")


def _terminal_patches(app, run_id: str) -> list[str]:
    statuses = []
    for request in app.requests:
        if request.method == "PATCH" and request.url.path == f"/v1/runs/{run_id}":
            status = json.loads(request.content or b"{}").get("status")
            if status in _TERMINAL:
                statuses.append(status)
    return statuses


@pytest.mark.parametrize("launched_from", ["shell", "claude_code"])
def test_a_script_that_just_ends_closes_its_run_after_a_busy_503(
    app, wired, monkeypatch, launched_from
):
    if launched_from == "claude_code":
        for key, value in _CLAUDE_CODE_ENV.items():
            monkeypatch.setenv(key, value)
    run = probe.init(experiment="e1", name="r1")
    app.metrics_busy_next = 1  # the exit drain's first metric POST
    probe.log({"loss": 1.0}, step=0)

    fluent._finish_at_exit()  # what atexit runs when the script simply ends

    assert app.metrics_busy_next == 0, "the 503 was served"
    assert _terminal_patches(app, run.id) == ["completed"]
    assert app.runs[run.id]["status"] == "completed"
    assert app.metric_points_posted[run.id], "the point landed on the retry"
    create = next(r for r in app.requests if r.url.path.endswith("/runs"))
    session = create.headers.get("X-Probe-Agent-Session")
    assert session == (_SESSION_ID if launched_from == "claude_code" else None), (
        "the run was written under the session this case claims to cover"
    )
