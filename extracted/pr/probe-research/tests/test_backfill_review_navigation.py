"""Back unwinds folder reviews; quitting and approval remain separate actions."""

from contextlib import nullcontext
import json

import pytest

from probe.cli import backfill as bf, backfill_import as imp, backfill_run as runner
from probe.cli import import_jobs_ui, tui
from tests import test_backfill_background as fixtures

background_harness = fixtures.background_harness
_CLASSIFY = runner.classify


@pytest.mark.parametrize("form", ["recovery", "plan", "changed", "code_sources"])
@pytest.mark.parametrize("selection", [tui.BACK, None])
def test_back_returns_to_folder_choices_and_ctrl_c_still_quits(
    background_harness, monkeypatch, form, selection,
):
    h, queued = background_harness
    titles = {
        "recovery": "Recover an earlier import?",
        "plan": "Review the import plan",
        "changed": "Review changed files",
        "code_sources": "Review Code sources",
    }
    if form in {"changed", "code_sources"}:
        h.run()
        h.drain()
    if form == "changed":
        (h.folder / "a.py").write_text("value = 2\n")
    elif form == "code_sources":
        with h.coverage().writer() as coverage:
            coverage.put_meta("reviewed_sources", {})
        h.git = imp.github.GitEvidenceBundle([
            imp.github.GitEvidence("org/repo", "main", local_folder=str(h.folder), state="ok"),
        ])
    elif form == "recovery":
        monkeypatch.setattr(imp.Coverage, "recovery_candidates", lambda *a, **kw: [
            {"source_id": "previous", "paths": ["/previous/folder"]},
        ])
        monkeypatch.setattr(runner, "_index", lambda *a: pytest.fail("Back must precede scanning"))
    prompts = []

    def review(title, lines, choices):
        prompts.append(title)
        assert title == titles[form]
        return selection

    monkeypatch.setattr(tui, "review", review)
    monkeypatch.setattr(runner, "_run_transcript_lane", lambda **kw: pytest.fail("Do not advance imports"))
    before = len(h.created), len(h.manifested), len(h.remote.calls)
    options = dict(
        client_factory=lambda: nullcontext(h.client), folder=h.folder,
        agent=bf.Agent.CLAUDE, interactive=True, yes=False, background=True,
        back_to_selection=True, transcripts=True,
    )
    if selection is tui.BACK:
        assert runner.execute(**options) is tui.BACK
    else:
        with pytest.raises(KeyboardInterrupt):
            runner.execute(**options)
    assert prompts == [titles[form]]
    assert queued == []
    assert (len(h.created), len(h.manifested), len(h.remote.calls)) == before


def test_returning_to_scanned_plan_reuses_analysis_but_still_requires_approval(
    background_harness, monkeypatch,
):
    h, queued = background_harness
    monkeypatch.setattr(runner, "classify", _CLASSIFY)
    reads, reviews = [], []

    def launch(folder, prompt, **kwargs):
        reads.append((folder / "a.py").read_text())
        plan = {"projects": [{"slug": "project"}],
                "assignments": [{"path": "a.py", "project": "project"}]}
        return True, json.dumps({"type": "result", "result": json.dumps(plan)})

    def review(title, lines, choices):
        if title != "Review the import plan":
            return choices[0][1]
        reviews.append(title)
        return tui.BACK if len(reviews) == 1 else "import"

    monkeypatch.setattr(bf, "launch_agent", launch)
    monkeypatch.setattr(bf, "git_context", lambda *a: None)
    monkeypatch.setattr(tui, "review", review)
    monkeypatch.setattr(import_jobs_ui, "show_started_import", lambda job: job)
    options = dict(background=True, interactive=True, yes=False, back_to_selection=True)
    assert h.run(**options) is tui.BACK
    assert queued == h.created == h.manifested == h.remote.calls == []
    assert isinstance(h.run(**options), list)
    assert len(reads) == 1 and len(reviews) == 2
    assert len(queued) == len(h.created) == 1
    assert h.manifested == h.remote.calls == []


def test_back_from_revision_text_returns_to_same_plan_without_rescanning(
    background_harness, monkeypatch,
):
    h, queued = background_harness
    reviews = []

    def review(title, lines, choices):
        if title != "Review the import plan":
            return choices[0][1]
        reviews.append(title)
        return "revise" if len(reviews) == 1 else "import"

    monkeypatch.setattr(tui, "review", review)
    monkeypatch.setattr(tui, "text", lambda *a, **kw: tui.BACK)
    monkeypatch.setattr(import_jobs_ui, "show_started_import", lambda job: job)
    assert isinstance(h.run(background=True, interactive=True, yes=False, back_to_selection=True), list)
    assert len(reviews) == 2 and len(h.classified) == len(queued) == 1
    assert h.manifested == h.remote.calls == []


def test_cancel_import_returns_to_choices_without_becoming_ctrl_c(background_harness, monkeypatch):
    h, queued = background_harness
    monkeypatch.setattr(tui, "review", lambda *a, **kw: "cancel")
    assert h.run(background=True, interactive=True, yes=False, back_to_selection=True) is tui.BACK
    assert queued == h.created == h.manifested == h.remote.calls == []


def test_wandb_back_returns_before_folder_delivery_is_enqueued(background_harness, monkeypatch):
    h, queued = background_harness
    prompts = []

    def review(title, lines, choices):
        prompts.append(title)
        assert title in {"Review the import plan", "Add W&B history"}
        return "import" if title == "Review the import plan" else tui.BACK

    monkeypatch.setattr(tui, "review", review)
    assert h.run(background=True, interactive=True, yes=False, back_to_selection=True) is tui.BACK
    assert prompts == ["Review the import plan", "Add W&B history"]
    assert queued == h.manifested == h.remote.calls == []
