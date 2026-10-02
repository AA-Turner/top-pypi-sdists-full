"""Install confirmation uses the same two-ended navigation as the other steps."""

import pytest

from probe.cli import setup, tui
from tests.test_tui_review import _run

pytestmark = pytest.mark.tui
_DOWN = "\x1b[B"
_APPROVAL = "One browser approval covers everything above."


def _confirm():
    return setup.run_confirm_install(("claude_code", "codex"), step=setup.STEP_CONFIRM)


@pytest.mark.parametrize("keys,expected", [
    (["\r"], True),
    (["\x1b[C"], True),
    ([_DOWN, "\r"], tui.BACK),
    (["\x1b[D"], tui.BACK),
    (["\x1b"], tui.BACK),
    (["\x03"], None),
], ids=["enter-installs", "right-installs", "back-row", "left-back", "escape-back", "cancel"])
def test_confirmation_navigation_returns_only_install_back_or_cancel(monkeypatch, keys, expected):
    answer, _frames = _run(monkeypatch, keys, render=_confirm)
    assert answer is expected


@pytest.mark.parametrize("keys,expected", [
    (["\r"], True),
    ([_DOWN, "\r"], tui.BACK),
    (["\x1b"], tui.BACK),
], ids=["install", "back", "escape"])
def test_unavailable_picker_falls_back_to_explicit_install_and_back_choices(monkeypatch, keys, expected):
    import questionary

    monkeypatch.setattr(setup, "_wire_picker", lambda *args, **kwargs: None)
    select = tui.select
    prompts = []

    def capture(message, **kwargs):
        prompts.append((message, kwargs["choices"]))
        return select(message, **kwargs)

    monkeypatch.setattr(tui, "select", capture)
    answer, _frames = _run(monkeypatch, keys, render=_confirm)
    assert answer is expected
    message, choices = prompts[-1]
    answers = [choice for choice in choices if isinstance(choice, questionary.Choice)
               and not isinstance(choice, questionary.Separator)]
    assert len(answers) == 2
    assert answers[0].value is True and "Install" in str(answers[0].title)
    assert answers[1].value is tui.BACK and "Back" in str(answers[1].title)
    assert all(choice.value != setup.NAV_BAND for choice in answers)
    assert all(_APPROVAL not in str(choice.title) for choice in answers)
    assert any(_APPROVAL in line for line in message.sections["lines"])
