"""The humanised input path must degrade LOUDLY, exactly as its docstring says.

``humanize.py`` promises: "when a target has no box to aim at (detached,
zero-size), the caller falls back to the plain Playwright action and the fallback
is logged at WARNING with the selector, so a run that stops looking human is
visible in the worker log rather than silently regressing."

The break these guard: that promise only held when ``_target_box`` returned
None. On the COMMONEST failure — the ``wait_for`` inside it TIMING OUT, which is
what a field that is slow to appear, or that disappears between the probe and
the aim, actually does — the exception propagated out of ``HumanInput.type_text``
and was swallowed by the blanket ``except Exception`` in ``actions.type_text``.
So the plain-Playwright fallback never ran, the promised WARNING was never
logged, and the caller got "Type failed: Timeout 1500ms exceeded" with no hint
that the humanised path had anything to do with it.

The scenario is real: a dental practice's intake form reveals the policy-number
field only while an insurance plan is selected, and the selection can be reset by
the page's own validation between the moment the agent probes the field and the
moment it aims the pointer at it.
"""

from __future__ import annotations

import importlib
import logging

import pytest

actions = importlib.import_module("matrx_scraper.ai_browser.actions")
humanize = importlib.import_module("matrx_scraper.ai_browser.humanize")

FIELD = "#policy-number"
POLICY_NUMBER = "HD-4417-20931"


class _Keyboard:
    def __init__(self) -> None:
        self.events: list[str] = []

    async def type(self, ch: str) -> None:
        self.events.append(ch)

    async def press(self, key: str) -> None:
        self.events.append(f"<{key}>")


class _Mouse:
    async def move(self, x: float, y: float) -> None:
        return None

    async def down(self) -> None:
        return None

    async def up(self) -> None:
        return None


class _VanishingLocator:
    """Visible when the readiness gate looks, gone by the time the pointer aims —
    the real race, reported by Playwright as a ``wait_for`` TimeoutError."""

    def __init__(self, page: "_Page") -> None:
        self._page = page

    @property
    def first(self) -> _VanishingLocator:
        return self

    async def wait_for(self, *, state: str, timeout: float) -> None:
        self._page.visibility_checks += 1
        if self._page.visibility_checks > 1:
            raise TimeoutError(f"Timeout {timeout}ms exceeded waiting for {state}")

    async def scroll_into_view_if_needed(self, *, timeout: float) -> None:
        return None

    async def bounding_box(self) -> dict[str, float] | None:
        return {"x": 24.0, "y": 180.0, "width": 210.0, "height": 26.0}


class _Page:
    def __init__(self) -> None:
        self.url = "https://harbordental.invalid/intake"
        self.viewport_size = {"width": 1280, "height": 800}
        self.keyboard = _Keyboard()
        self.mouse = _Mouse()
        self.visibility_checks = 0
        #: What the PLAIN Playwright fallback did, if it ran at all.
        self.plain_typed: list[tuple[str, str]] = []

    def locator(self, selector: str) -> _VanishingLocator:
        return _VanishingLocator(self)

    async def query_selector(self, selector: str) -> object | None:
        return object()

    async def type(self, selector: str, text: str, **kwargs: object) -> None:
        self.plain_typed.append((selector, text))

    async def fill(self, selector: str, text: str, **kwargs: object) -> None:
        self.plain_typed.append((selector, text))

    async def inner_text(self, selector: str = "body") -> str:
        return "Harbor Dental — new patient intake"


class _Session:
    def __init__(self, page: _Page) -> None:
        self.page = page


class _Registry:
    def __init__(self, session: _Session) -> None:
        self._session = session

    async def get(self, session_id: str) -> _Session:
        return self._session


@pytest.fixture
def intake(monkeypatch):
    page = _Page()
    monkeypatch.setattr(actions, "guard_landing", _allow_landing)
    return page, _Registry(_Session(page))


async def _allow_landing(page):  # noqa: ANN001
    return None


@pytest.mark.asyncio
async def test_a_wait_for_timeout_makes_the_plain_playwright_fallback_run(
    intake, caplog
) -> None:
    """Break caught: the timeout escaped ``_target_box`` and was swallowed by
    ``actions.type_text``'s blanket except, so the fallback never ran."""
    page, registry = intake
    with caplog.at_level(logging.WARNING, logger="matrx_scraper.ai_browser.humanize"):
        result = await actions.type_text(
            "intake", FIELD, POLICY_NUMBER, timeout_ms=1_500, human=True, mgr=registry
        )

    assert page.plain_typed == [(FIELD, POLICY_NUMBER)], (
        "the plain Playwright action is the documented fallback and must actually run"
    )
    assert result.success is True
    assert result.typed == POLICY_NUMBER


@pytest.mark.asyncio
async def test_the_fallback_says_so_at_warning_with_the_selector(intake, caplog) -> None:
    """Break caught: the promised WARNING. A run that silently stops looking
    human is exactly the regression this log line exists to make visible."""
    page, registry = intake
    with caplog.at_level(logging.WARNING, logger="matrx_scraper.ai_browser.humanize"):
        await actions.type_text(
            "intake", FIELD, POLICY_NUMBER, timeout_ms=1_500, human=True, mgr=registry
        )

    warnings = [r for r in caplog.records if r.levelno >= logging.WARNING]
    assert warnings, "the humanised path fell back without saying a word"
    said = " ".join(r.getMessage() for r in warnings)
    assert FIELD in said, f"the WARNING must name the selector; got: {said}"
    assert "fall" in said.lower() or "plain" in said.lower()
    # And it never leaks what was being typed.
    assert POLICY_NUMBER not in said


@pytest.mark.asyncio
async def test_the_humanised_path_still_runs_when_the_field_stays_put(intake) -> None:
    """The second forcing input: nothing falls back when nothing goes wrong.
    A ``_target_box`` that just returned None always would pass the two tests
    above and fail this one."""
    page, registry = intake

    class _SteadyLocator(_VanishingLocator):
        async def wait_for(self, *, state: str, timeout: float) -> None:
            return None

    page.locator = lambda selector: _SteadyLocator(page)  # type: ignore[method-assign]

    result = await actions.type_text(
        "intake", FIELD, POLICY_NUMBER, timeout_ms=1_500, human=True, mgr=registry
    )

    assert result.success is True
    assert page.plain_typed == [], "nothing was wrong; the plain fallback must not fire"
    assert "".join(page.keyboard.events) == POLICY_NUMBER


def test_humanize_holds_no_readiness_definition_of_its_own() -> None:
    """Census: the humanised path asks ``readiness.element_readiness`` and
    nothing else. Its own ``state="visible"`` wait WAS the second definition,
    and it is what made the two answers disagree."""
    import pathlib

    source = pathlib.Path(humanize.__file__).read_text(encoding="utf-8")
    assert 'state="visible"' not in source
    assert "bounding_box()" not in source
    assert "element_readiness" in source
