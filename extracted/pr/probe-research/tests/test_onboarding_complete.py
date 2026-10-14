"""The final setup page opens the dashboard without stopping imports."""

import pytest

from probe.cli import import_jobs, onboarding_complete
from tests.test_tui_review import _run

pytestmark = pytest.mark.tui


@pytest.fixture
def completion(monkeypatch):
    jobs, opened = [], []
    monkeypatch.delenv("PROBE_DASHBOARD_URL", raising=False)
    monkeypatch.setattr(import_jobs, "list_jobs", lambda: jobs)
    monkeypatch.setattr(onboarding_complete.webbrowser, "open", lambda url: opened.append(url) or True)
    return jobs, opened


@pytest.mark.parametrize("job", [
    {"kind": import_jobs.Kind.FOLDER, "state": import_jobs.State.FAILED},
    {"kind": import_jobs.Kind.FOLDER, "state": import_jobs.State.SUCCEEDED,
     "progress": {"completion_completed": 1, "completion_total": 4}},
])
def test_unfinished_import_does_not_block_dashboard_handoff(monkeypatch, completion, job):
    jobs, opened = completion
    jobs.append(job)
    result, frames = _run(
        monkeypatch, ["\r"], height=40,
        render=lambda: onboarding_complete.show("https://api.research.prbe.ai"),
    )
    assert result is True and opened
    text = "\n".join(frames[0])
    assert "Some imports need attention." in text
    assert "Your imports are running" not in text


def test_browser_failure_keeps_the_link_visible_and_allows_retry(monkeypatch, completion):
    _, opened = completion

    def browser(url):
        opened.append(url)
        return len(opened) > 1

    monkeypatch.setattr(onboarding_complete.webbrowser, "open", browser)
    result, frames = _run(
        monkeypatch, ["\r", "\r"],
        render=lambda: onboarding_complete.show("https://api.research.prbe.ai"),
    )
    assert result is True and opened == ["https://research.prbe.ai/projects"] * 2
    assert "Couldn't open your browser." in "\n".join(frames[1])
    assert "https://research.prbe.ai/projects" in "\n".join(frames[1])


def test_back_returns_to_menu_without_opening_dashboard(monkeypatch, completion):
    result, _ = _run(
        monkeypatch, ["\x1b"],
        render=lambda: onboarding_complete.show("https://api.research.prbe.ai"),
    )
    assert result is False and not completion[1]


def test_self_hosted_dashboard_override_is_used(monkeypatch, completion):
    monkeypatch.setenv("PROBE_DASHBOARD_URL", "https://research.example.test/team/")
    result, _ = _run(
        monkeypatch, ["\r"],
        render=lambda: onboarding_complete.show("http://api.internal:8000"),
    )
    assert result is True and completion[1] == ["https://research.example.test/team/projects"]


def test_unknown_dashboard_does_not_open_an_unrelated_public_host(monkeypatch, completion):
    result, frames = _run(
        monkeypatch, ["\r"],
        render=lambda: onboarding_complete.show("http://api.internal:8000"),
    )
    assert result is False and not completion[1]
    assert "Open your Probe dashboard in your browser." in "\n".join(frames[0])


def test_later_completed_import_settles_an_older_partial_warning(monkeypatch, completion):
    from tests.test_import_progress import session

    jobs, _ = completion
    jobs.extend([
        session("partial", ["a", "b"], 1, state="succeeded"),
        session("complete", ["a", "b"], 2, state="succeeded"),
    ])
    jobs[-1]["created_at"] = "2026-09-11T09:00:00Z"
    result, frames = _run(
        monkeypatch, ["\r"],
        render=lambda: onboarding_complete.show("https://api.research.prbe.ai"),
    )
    assert result is True
    assert "need attention" not in "\n".join(frames[0])




def test_an_app_opens_only_when_chosen_and_the_page_says_how_it_went(monkeypatch, completion):
    """Capy's step stays on the page; "Open Capy >" opens it on that screen
    only when chosen (its box defaults to Organization, and the step, read
    first, says Only me). A failure keeps the page, and the step, up."""
    from probe.cli import tui

    _, opened_dashboard = completion
    calls, pages = [], []

    def opener():
        calls.append("capy")
        return len(calls) > 1

    def review(title, lines, choices, **_kwargs):
        pages.append(("\n".join(lines()), [label for label, _ in choices]))
        assert len(calls) == len(pages) - 1, "nothing opens until it is chosen"
        if len(pages) <= 2:
            return next(value for label, value in choices if label == "Open Capy >")
        return "menu"

    monkeypatch.setattr(tui, "review", review)
    result = onboarding_complete.show(
        "https://api.research.prbe.ai", next_steps=["One step in Capy"], open_apps=[("Capy", opener)]
    )
    assert result is False and calls == ["capy", "capy"] and not opened_dashboard
    assert pages[0][1][:2] == ["Open Capy >", "Open dashboard >"]
    assert "One step in Capy" in pages[0][0] and "Capy" not in pages[0][0].replace("One step in Capy", "")
    assert "Couldn't open Capy." in pages[1][0]
    assert "Capy is open on that screen" in pages[2][0] and "Couldn't open" not in pages[2][0]
