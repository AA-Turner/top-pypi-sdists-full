"""Back revisits W&B decisions without approving or undoing remote work."""

import pytest

from probe.cli import backfill_wandb as wb
from tests.test_backfill_wandb import CONNECTION, OTHER, PROJECT, admit
from tests.test_backfill_wandb import harness as harness

TITLES = [
    "Add W&B history", "Choose a W&B account", "Choose W&B history",
    "Choose a Probe destination", "Review W&B history import",
]
FORWARD = ["wandb", 1, 1, 2]


def answers(monkeypatch, responses):
    pending = list(responses)
    seen = []

    def review(title, lines, choices, **kwargs):
        seen.append((title, lines, choices, kwargs))
        assert pending, f"Unexpected page: {title}"
        response = pending.pop(0)
        return choices[response][1] if isinstance(response, int) else response

    monkeypatch.setattr(wb.tui, "review", review)
    return seen, pending


def test_back_walks_every_previous_page_and_retains_selections(harness, monkeypatch):
    client, coverage, remote = harness
    seen, pending = answers(monkeypatch, [*FORWARD, *[wb.tui.BACK] * 5])

    assert wb.run(
        client, coverage, interactive=True, offer=True, back_to_selection=True,
    ) is wb.tui.BACK

    assert not pending
    assert [screen[0] for screen in seen] == [*TITLES, *reversed(TITLES[:-1])]
    assert seen[5][3]["default"] == OTHER
    assert seen[6][3]["default"]["external_id"] == "lab/training"
    assert seen[7][3]["default"]["id"] == CONNECTION
    assert coverage.meta(wb.KEY) is None
    assert not remote.attachments and not remote.jobs
    assert [request[0] for request in remote.requests] == ["GET", "GET"]


@pytest.mark.parametrize("stage", range(1, 5))
def test_back_then_forward_requires_review_before_one_admission(harness, monkeypatch, stage):
    client, coverage, remote = harness
    seen, pending = answers(monkeypatch, [
        *FORWARD[:stage], wb.tui.BACK, *FORWARD[stage - 1:], "import",
    ])

    lines = wb.run(client, coverage, interactive=True, offer=True, back_to_selection=True)

    assert not pending
    assert [screen[0] for screen in seen] == [
        *TITLES[:stage + 1], *TITLES[stage - 1:],
    ]
    assert "queued" in " ".join(lines)
    assert coverage.meta(wb.KEY)["imports"][0]["project_id"] == OTHER
    assert len(remote.attachments) == len(remote.jobs) == 1
    assert len([request for request in remote.requests if request[0] == "POST"]) == 2


def test_back_from_review_can_change_destination_before_approval(harness, monkeypatch):
    client, coverage, remote = harness
    seen, pending = answers(monkeypatch, [*FORWARD, wb.tui.BACK, 1, "import"])

    wb.run(client, coverage, interactive=True, offer=True, back_to_selection=True)

    assert not pending
    assert seen[5][3]["default"] == OTHER
    assert f"Probe destination: one · {PROJECT}" in seen[-1][1]
    assert coverage.meta(wb.KEY)["imports"][0]["project_id"] == PROJECT
    assert len(remote.attachments) == len(remote.jobs) == 1


@pytest.mark.parametrize("stage", range(5))
def test_explicit_skip_advances_without_approval(harness, monkeypatch, stage):
    client, coverage, remote = harness
    _, pending = answers(monkeypatch, [*FORWARD[:stage], 0])

    assert wb.run(
        client, coverage, interactive=True, offer=True, back_to_selection=True,
    ) == []

    assert not pending
    assert coverage.meta(wb.KEY) is None
    assert not remote.attachments and not remote.jobs
    assert all(request[0] == "GET" for request in remote.requests)


@pytest.mark.parametrize("stage", range(5))
def test_ctrl_c_still_interrupts_instead_of_navigating(harness, monkeypatch, stage):
    client, coverage, remote = harness
    _, pending = answers(monkeypatch, [*FORWARD[:stage], None])

    with pytest.raises(KeyboardInterrupt):
        wb.run(client, coverage, interactive=True, offer=True, back_to_selection=True)

    assert not pending
    assert coverage.meta(wb.KEY) is None
    assert not remote.attachments and not remote.jobs


def test_first_page_back_does_not_admit_existing_pending_selection(harness, monkeypatch):
    client, coverage, remote = harness
    saved = wb.record_reviewed_selection(
        coverage, project_id=PROJECT, connection_id=CONNECTION, external_id="lab/training",
    )
    answers(monkeypatch, [wb.tui.BACK])

    assert wb.run(
        client, coverage, interactive=True, offer=True, back_to_selection=True,
    ) is wb.tui.BACK

    assert coverage.meta(wb.KEY)["imports"] == [saved]
    assert not remote.requests


def test_retry_back_preserves_approved_job_and_returns_navigation(harness, monkeypatch):
    client, coverage, remote = harness
    original = admit(harness)
    remote.jobs[original["idempotency_key"]]["state"] = "failed"
    before = len(remote.requests)
    answers(monkeypatch, ["skip", wb.tui.BACK])

    assert wb.run(
        client, coverage, interactive=True, offer=True, back_to_selection=True,
    ) is wb.tui.BACK

    current = coverage.meta(wb.KEY)["imports"][0]
    assert current["job_id"] == original["job_id"]
    assert current["idempotency_key"] == original["idempotency_key"]
    assert current["receipt"]["state"] == "failed"
    assert len(remote.jobs) == 1
    assert [request[0] for request in remote.requests[before:]] == ["GET"]
