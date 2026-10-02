"""Reading stays local to the flow; only an approved plan can be detached."""

import json

import pytest

from probe.cli import backfill as bf, backfill_run as runner, import_jobs_ui, tui
from tests.test_backfill_background import background_harness as background_harness

_CLASSIFY = runner.classify


@pytest.mark.parametrize("choice", [tui.BACK, tui.SKIP])
def test_leaving_folder_picker_does_not_read_or_enqueue(monkeypatch, choice):
    monkeypatch.setattr(bf, "choose_directory", lambda _: choice)
    monkeypatch.setattr(bf, "resolve_agent", lambda *a, **kw: pytest.fail("No agent should start"))
    assert bf.run(client_factory=lambda: pytest.fail("No credentials needed"), background=True) is None


def test_approval_precedes_background_delivery_and_live_handoff(background_harness, monkeypatch):
    h, queued = background_harness
    order = []

    def review(title, lines, choices):
        if title == "Review the import plan":
            assert h.classified == [["a.py"]]
            assert queued == [] and h.manifested == [] and h.remote.calls == []
            assert "Reading is complete" in lines[0] and "background" in lines[0]
            order.append("approved")
            return "import"
        return choices[0][1]

    def handoff(job):
        assert order == ["approved"] and len(queued) == 1
        assert h.manifested == [] and h.remote.calls == []
        order.append("watching")
        return {**job, "state": "succeeded"}

    monkeypatch.setattr(tui, "review", review)
    monkeypatch.setattr(import_jobs_ui, "show_started_import", handoff)
    lines = h.run(background=True, interactive=True, yes=False)
    assert order == ["approved", "watching"]
    assert any("already complete" in line for line in lines)


def test_cancelled_read_is_cached_but_never_replaces_explicit_approval(
    background_harness, monkeypatch,
):
    h, queued = background_harness
    # The harness normally substitutes classification; restore the real cache
    # and parser while keeping model calls synthetic and entirely local.
    monkeypatch.setattr(runner, "classify", _CLASSIFY)
    reads, reviews = [], []

    def launch(folder, prompt, **kwargs):
        reads.append((folder / "a.py").read_text())
        plan = {"projects": [{"slug": "project"}],
                "assignments": [{"path": "a.py", "project": "project"}]}
        return True, json.dumps({"type": "result", "result": json.dumps(plan)})

    def cancel(title, lines, choices):
        assert title == "Review the import plan"
        reviews.append(title)
        return "cancel"

    monkeypatch.setattr(bf, "launch_agent", launch)
    monkeypatch.setattr(bf, "git_context", lambda *args: None)
    monkeypatch.setattr(tui, "review", cancel)
    for _ in range(2):
        with pytest.raises(KeyboardInterrupt):
            h.run(background=True, interactive=True, yes=False)
    assert len(reads) == 1 and len(reviews) == 2
    assert queued == h.created == h.manifested == h.remote.calls == []

    (h.folder / "a.py").write_text("changed = True\n")
    with pytest.raises(KeyboardInterrupt):
        h.run(background=True, interactive=True, yes=False)
    assert len(reads) == 2 and len(reviews) == 3
    assert queued == h.created == h.manifested == h.remote.calls == []
