"""ONE definition of "this element is ready", shared by every browser action.

The break these guard: the package carried TWO readiness definitions that
disagreed.

  * ``actions.get_element`` did ``query_selector`` + ``bounding_box()`` with NO
    visibility check, so a ``visibility:hidden`` input came back
    ``found=True`` with a full bounding box — "present and usable";
  * ``humanize._target_box`` required Playwright ``state="visible"``, so the
    very same element made ``type_text`` sit there until it timed out.

An agent that probes with ``get_element``, is told the field is there, and then
cannot type into it has been lied to. These tests run BOTH entry points against
the SAME real Chromium page and require them to agree, field by field.

The page is the new-patient intake form a dental practice's front desk fills in:
one ordinary visible field, one field the form hides until insurance is chosen,
one field hidden by ``display:none``, and one selector that matches nothing.
"""

from __future__ import annotations

import importlib

import pytest

pytest.importorskip("playwright", reason="playwright not installed (browser extra)")

from playwright.async_api import async_playwright  # noqa: E402

actions = importlib.import_module("matrx_scraper.ai_browser.actions")
readiness = importlib.import_module("matrx_scraper.ai_browser.readiness")

INTAKE_FORM = """
<html><body>
  <h1>Harbor Dental — new patient intake</h1>
  <form>
    <label>Preferred name <input id="preferred-name" name="preferred_name"></label>
    <label style="visibility:hidden">Policy number
      <input id="policy-number" name="policy_number"></label>
    <label style="display:none">Referring dentist
      <input id="referring-dentist" name="referring_dentist"></label>
    <label>Insurance carrier
      <select id="carrier" name="carrier">
        <option value="">Choose…</option>
        <option value="delta">Delta Dental</option>
      </select></label>
    <label style="visibility:hidden">Secondary carrier
      <select id="secondary-carrier" name="secondary_carrier">
        <option value="">Choose…</option>
        <option value="delta">Delta Dental</option>
      </select></label>
    <button id="submit-intake" type="button">Submit intake</button>
    <button id="cancel-intake" type="button" style="visibility:hidden">Cancel</button>
  </form>
</body></html>
"""


class _Session:
    def __init__(self, page) -> None:  # noqa: ANN001
        self.page = page


class _Registry:
    def __init__(self, session: _Session) -> None:
        self._session = session

    async def get(self, session_id: str) -> _Session:
        return self._session


@pytest.fixture
async def intake_page(monkeypatch):
    async with async_playwright() as pw:
        try:
            browser = await pw.chromium.launch()
        except Exception as exc:  # pragma: no cover - environment probe
            pytest.skip(f"no chromium browser binary: {exc}")
        page = await browser.new_page()
        await page.set_content(INTAKE_FORM)
        # The SSRF landing gate resolves DNS and is not what these guards are
        # about; set_content leaves the page at about:blank.
        monkeypatch.setattr(actions, "guard_landing", _allow_landing)
        yield page
        await browser.close()


async def _allow_landing(page):  # noqa: ANN001
    return None


# (selector, is it really usable by a person typing into this form?)
FIELDS = [
    ("#preferred-name", True),
    ("#policy-number", False),
    ("#referring-dentist", False),
    ("#emergency-contact", False),
]


@pytest.mark.parametrize(("selector", "usable"), FIELDS)
@pytest.mark.asyncio
async def test_get_element_and_type_text_agree_on_every_field(
    intake_page, selector: str, usable: bool
) -> None:
    """Break caught: the two readiness definitions disagreed. Before the shared
    definition, ``#policy-number`` was ``found=True`` here and a timeout there."""
    registry = _Registry(_Session(intake_page))

    probed = await actions.get_element("intake", selector, mgr=registry)
    assert probed.success is True
    assert probed.found is usable, (
        f"get_element reported found={probed.found} for {selector}, "
        f"but a person can{'' if usable else 'not'} type into it"
    )

    typed = await actions.type_text(
        "intake", selector, "Marisol Tran", timeout_ms=1_500, human=True, mgr=registry
    )
    assert typed.success is usable
    assert probed.found is typed.success, (
        "get_element and type_text must share ONE readiness definition; "
        f"{selector} was found={probed.found} but typed={typed.success}"
    )


@pytest.mark.asyncio
async def test_a_hidden_field_is_reported_as_present_but_not_usable(intake_page) -> None:
    """A hidden field is not absent, and saying so is the honest answer: the
    agent needs to know the field EXISTS and needs revealing, not that its
    selector was wrong."""
    registry = _Registry(_Session(intake_page))
    probed = await actions.get_element("intake", "#policy-number", mgr=registry)

    assert probed.found is False
    assert probed.present is True
    assert probed.readiness == "not_visible"
    # No box is offered for something nothing can be aimed at.
    assert probed.bounding_box is None

    missing = await actions.get_element("intake", "#emergency-contact", mgr=registry)
    assert missing.found is False
    assert missing.present is False
    assert missing.readiness == "absent"


@pytest.mark.asyncio
async def test_the_readiness_definition_lives_in_exactly_one_place(intake_page) -> None:
    """Census: every readiness verdict in the package comes from
    ``readiness.element_readiness``. A second ``state="visible"`` wait or a
    second bare ``bounding_box`` readiness check re-opens the whole class."""
    verdict = await readiness.element_readiness(intake_page, "#policy-number", timeout_ms=1_000)
    assert verdict.present is True
    assert verdict.usable is False
    assert verdict.reason == "not_visible"
    assert verdict.box is None

    ok = await readiness.element_readiness(intake_page, "#preferred-name", timeout_ms=1_000)
    assert ok.usable is True and ok.box is not None and ok.box["width"] > 1

    source = importlib.import_module("pathlib").Path(actions.__file__).read_text(encoding="utf-8")
    assert 'state="visible"' not in source, (
        "a visibility wait outside readiness.py is a second readiness definition"
    )
    assert "bounding_box()" not in source, (
        "a bare bounding_box readiness check outside readiness.py is a second definition"
    )


# ── EVERY action that aims at an element, not only type_text ────────────────
#
# The hole these close: `type_text` and `get_element` were brought onto the one
# readiness definition, and `click`, `fill` and `select_option` were left on
# Playwright's own actionability wait. That is the SAME class, one step to the
# left: `get_element` told the agent the Cancel button / Secondary-carrier
# select / Policy-number field was there, and the action then sat on the page
# for its whole timeout and returned a raw Playwright message naming nothing.
# The front desk sees "Submit intake" work and "Cancel" hang.

#: (selector, is a person able to act on it?, action name)
CLICK_TARGETS = [("#submit-intake", True), ("#cancel-intake", False)]
FILL_TARGETS = [("#preferred-name", True), ("#policy-number", False), ("#nope", False)]
SELECT_TARGETS = [("#carrier", True), ("#secondary-carrier", False)]


@pytest.mark.parametrize(("selector", "usable"), CLICK_TARGETS)
@pytest.mark.asyncio
async def test_click_agrees_with_get_element(intake_page, selector: str, usable: bool) -> None:
    registry = _Registry(_Session(intake_page))

    probed = await actions.get_element("intake", selector, mgr=registry)
    clicked = await actions.click("intake", selector, timeout_ms=1_500, mgr=registry)

    assert probed.found is usable
    assert clicked.success is usable, (
        f"click({selector}) returned success={clicked.success} while get_element "
        f"said found={probed.found}: {clicked.error_message}"
    )
    if not usable:
        assert "hidden" in (clicked.error_message or ""), (
            "an unusable target must be named and explained, not reported as a raw "
            f"Playwright timeout: {clicked.error_message!r}"
        )


@pytest.mark.parametrize(("selector", "usable"), FILL_TARGETS)
@pytest.mark.asyncio
async def test_fill_agrees_with_get_element(intake_page, selector: str, usable: bool) -> None:
    registry = _Registry(_Session(intake_page))

    probed = await actions.get_element("intake", selector, mgr=registry)
    filled = await actions.fill("intake", selector, "Marisol Tran", timeout_ms=1_500, mgr=registry)

    assert probed.found is usable
    assert filled.success is usable, (
        f"fill({selector}) returned success={filled.success} while get_element "
        f"said found={probed.found}: {filled.error_message}"
    )


@pytest.mark.parametrize(("selector", "usable"), SELECT_TARGETS)
@pytest.mark.asyncio
async def test_select_option_agrees_with_get_element(
    intake_page, selector: str, usable: bool
) -> None:
    registry = _Registry(_Session(intake_page))

    probed = await actions.get_element("intake", selector, mgr=registry)
    chose = await actions.select_option(
        "intake", selector, value="delta", timeout_ms=1_500, mgr=registry
    )

    assert probed.found is usable
    assert chose.success is usable, (
        f"select_option({selector}) returned success={chose.success} while "
        f"get_element said found={probed.found}: {chose.error_message}"
    )


@pytest.mark.asyncio
async def test_the_gate_still_waits_for_a_target_the_page_reveals_late(intake_page) -> None:
    """The honest cost of one shared verdict, pinned.

    The gate must NOT be made cheap by shortening its wait: a field the page
    reveals a moment later — an insurance section opening, a modal finishing its
    animation — is a normal page, not an unusable target. A previous draft of
    this guard asserted "refuse fast", which would have been satisfied by
    probing for a second and calling every slow form hidden. This asserts the
    opposite and is the one that protects real pages.
    """
    registry = _Registry(_Session(intake_page))
    await intake_page.evaluate(
        "setTimeout(() => "
        "document.querySelector('#policy-number').parentElement.style.visibility = 'visible',"
        " 1500)"
    )

    typed = await actions.type_text(
        "intake", "#policy-number", "DD-4417", timeout_ms=6_000, mgr=registry
    )

    assert typed.success is True, (
        "a field revealed 1.5 s in was refused; the shared gate must wait out the "
        f"caller's timeout, not a probe-sized slice of it: {typed.error_message}"
    )


@pytest.mark.asyncio
async def test_an_unusable_target_is_named_by_every_action_not_only_type_text(
    intake_page,
) -> None:
    """The message an agent can act on, from all four doors."""
    registry = _Registry(_Session(intake_page))

    results = {
        "click": await actions.click("intake", "#cancel-intake", timeout_ms=1_200, mgr=registry),
        "fill": await actions.fill(
            "intake", "#policy-number", "x", timeout_ms=1_200, mgr=registry
        ),
        "type_text": await actions.type_text(
            "intake", "#policy-number", "x", timeout_ms=1_200, mgr=registry
        ),
        "select_option": await actions.select_option(
            "intake", "#secondary-carrier", value="delta", timeout_ms=1_200, mgr=registry
        ),
    }

    for name, result in results.items():
        assert result.success is False, name
        message = result.error_message or ""
        assert "is hidden" in message, f"{name} did not say the target is hidden: {message!r}"
        assert "Reveal it first" in message, f"{name} gave no remedy: {message!r}"
        assert "Timeout" not in message, (
            f"{name} leaked a raw Playwright message instead of a sentence: {message!r}"
        )
