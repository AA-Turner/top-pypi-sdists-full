"""Every `ai_browser` reader that cuts its payload must SAY so — in the payload.

A reader that slices silently hands a model a fragment that looks like the whole
page; the model then reasons confidently over half a document with nothing in
the result to contradict it. The contract these tests pin:

  * an inline `[truncated: showing X of Y characters]` marker in the CONTENT
    itself (a sibling boolean mid-payload is easy for a model to miss), with
    honest numbers — X is the cap that actually fired, Y the real pre-cut size;
  * `truncated=True` + `total_chars` = the real PRE-truncation size;
  * an untruncated read is still self-describing — `truncated=False`,
    `total_chars` = the real size, and NO marker anywhere;
  * the cap actually bounds the payload (the marker is not cosmetic padding on
    an uncut string);
  * every cap is a named constant — the AST guard at the bottom fails the build
    the moment a new reader slices on a bare literal again.

These run the real action functions against a fake Playwright page, through the
real SSRF landing gate, so a reader that stops calling `_cap_text` fails here.
"""

from __future__ import annotations

import ast
import importlib
import pathlib
import re
from typing import Any

import pytest

actions = importlib.import_module("matrx_scraper.ai_browser.actions")
url_guard = importlib.import_module("matrx_scraper.ai_browser.url_guard")

PUBLIC_URL = "https://example.com/page"
MARKER_RE = re.compile(r"\[truncated: showing ([\d,]+) of ([\d,]+) characters\]")


# ── Fakes ──────────────────────────────────────────────────────────────────


class FakeElement:
    def __init__(
        self,
        text: str = "",
        *,
        inner: str = "",
        outer: str = "",
        attrs: dict[str, str] | None = None,
    ) -> None:
        self._text = text
        self._inner = inner
        self._outer = outer
        self._attrs = attrs or {}

    async def text_content(self) -> str:
        return self._text

    async def inner_html(self) -> str:
        return self._inner

    async def evaluate(self, expression: str, *args: Any) -> Any:
        if "attributes" in expression:
            return dict(self._attrs)
        return self._outer

    async def get_attribute(self, name: str) -> str | None:
        return self._attrs.get(name)

    async def bounding_box(self) -> dict[str, float] | None:
        return None


class FakePage:
    def __init__(
        self,
        *,
        html: str = "",
        text: str = "",
        element: FakeElement | None = None,
        matches: dict[str, list[FakeElement]] | None = None,
    ) -> None:
        self.url = PUBLIC_URL
        self._html = html
        self._text = text
        self._element = element
        self._matches = matches or {}

    async def goto(self, url: str, **kwargs: Any) -> Any:
        self.url = url
        return None

    async def title(self) -> str:
        return "Title"

    async def content(self) -> str:
        return self._html

    async def inner_text(self, selector: str = "body") -> str:
        return self._text

    async def query_selector(self, selector: str) -> FakeElement | None:
        return self._element

    async def query_selector_all(self, selector: str) -> list[FakeElement]:
        return self._matches.get(selector, [])

    async def click(self, selector: str, **kwargs: Any) -> None:
        return None

    async def fill(self, selector: str, value: str, **kwargs: Any) -> None:
        return None

    async def type(self, selector: str, text: str, **kwargs: Any) -> None:
        return None

    async def wait_for_timeout(self, ms: int) -> None:
        return None


class FakeSession:
    def __init__(self, page: FakePage) -> None:
        self.session_id = "sess1"
        self.page = page


class FakeManager:
    def __init__(self, session: FakeSession) -> None:
        self.session = session

    async def get(self, session_id: str) -> FakeSession:
        return self.session

    async def create(self, **kwargs: Any) -> FakeSession:
        return self.session


@pytest.fixture(autouse=True)
def _public_landing(monkeypatch: pytest.MonkeyPatch) -> None:
    """The landing gate runs for real; the resolver treats our fake URL as public."""

    async def fake_validate(url: str) -> str:
        return url

    monkeypatch.setattr(url_guard, "validate_public_http_url", fake_validate)


def _mgr(**page_kwargs: Any) -> FakeManager:
    return FakeManager(FakeSession(FakePage(**page_kwargs)))


def _assert_marked(content: str, *, cap: int, total: int) -> None:
    """The marker exists, its numbers are the REAL ones, and the cap bound the payload."""
    match = MARKER_RE.search(content)
    assert match is not None, f"no truncation marker in content ending: {content[-120:]!r}"
    shown_str, total_str = match.groups()
    assert int(shown_str.replace(",", "")) == cap
    assert int(total_str.replace(",", "")) == total
    # The marker is not cosmetic: everything before it is exactly the capped head.
    assert (
        content[:cap] and len(content) == cap + len(match.group(0)) + 2
    )  # +2 = the "\n\n" lead-in


def _assert_clean(content: str) -> None:
    assert "[truncated" not in content


# ── get_html ───────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_html_over_cap_is_marked_and_declared() -> None:
    cap = actions.GET_HTML_CAP
    html = "<p>" + "h" * (cap + 4_321)
    result = await actions.get_html("sess1", mgr=_mgr(html=html))

    assert result.success is True
    assert result.truncated is True
    assert result.total_chars == len(html)
    assert result.html.startswith(html[:100])
    _assert_marked(result.html, cap=cap, total=len(html))


@pytest.mark.asyncio
async def test_get_html_under_cap_is_whole_and_unmarked() -> None:
    html = "<html><body>small</body></html>"
    result = await actions.get_html("sess1", mgr=_mgr(html=html))

    assert result.truncated is False
    assert result.total_chars == len(html)
    assert result.html == html
    _assert_clean(result.html)


@pytest.mark.asyncio
async def test_get_html_honours_a_caller_supplied_cap() -> None:
    html = "x" * 5_000
    result = await actions.get_html("sess1", cap=1_000, mgr=_mgr(html=html))

    assert result.truncated is True
    assert result.total_chars == 5_000
    _assert_marked(result.html, cap=1_000, total=5_000)


# ── get_text ───────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_text_over_cap_is_marked_and_declared() -> None:
    cap = actions.GET_TEXT_CAP
    text = "t" * (cap + 999)
    result = await actions.get_text("sess1", mgr=_mgr(text=text))

    assert result.truncated is True
    assert result.total_chars == len(text)
    _assert_marked(result.text, cap=cap, total=len(text))


@pytest.mark.asyncio
async def test_get_text_under_cap_is_whole_and_unmarked() -> None:
    text = "just a paragraph"
    result = await actions.get_text("sess1", mgr=_mgr(text=text))

    assert result.truncated is False
    assert result.total_chars == len(text)
    assert result.text == text
    _assert_clean(result.text)


# ── get_element ────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_element_text_over_cap_is_marked_and_declared() -> None:
    cap = actions.ELEMENT_TEXT_CAP
    text = "e" * (cap + 77)
    result = await actions.get_element("sess1", "div", mgr=_mgr(element=FakeElement(text=text)))

    assert result.found is True
    assert result.truncated is True
    assert result.total_chars == len(text)
    _assert_marked(result.text, cap=cap, total=len(text))


@pytest.mark.asyncio
async def test_get_element_html_fields_are_capped_and_summed() -> None:
    cap = actions.ELEMENT_HTML_CAP
    text = "short text"
    inner = "i" * (cap + 10)
    outer = "o" * (cap + 20)
    element = FakeElement(text=text, inner=inner, outer=outer, attrs={"id": "main"})

    result = await actions.get_element("sess1", "div", include_html=True, mgr=_mgr(element=element))

    assert result.truncated is True
    # Multi-field result: total_chars is the summed pre-truncation size.
    assert result.total_chars == len(text) + len(inner) + len(outer)
    _assert_marked(result.inner_html, cap=cap, total=len(inner))
    _assert_marked(result.outer_html, cap=cap, total=len(outer))
    _assert_clean(result.text)  # this field was under its own cap
    assert result.attributes == {"id": "main"}


@pytest.mark.asyncio
async def test_get_element_under_cap_is_whole_and_unmarked() -> None:
    element = FakeElement(text="hello", inner="<b>hi</b>", outer="<div><b>hi</b></div>")
    result = await actions.get_element("sess1", "div", include_html=True, mgr=_mgr(element=element))

    assert result.truncated is False
    assert result.total_chars == len("hello") + len("<b>hi</b>") + len("<div><b>hi</b></div>")
    assert result.text == "hello"
    assert result.inner_html == "<b>hi</b>"
    _assert_clean(result.text + (result.inner_html or "") + (result.outer_html or ""))


# ── query_selectors ────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_query_selectors_row_text_over_cap_is_marked_and_declared() -> None:
    cap = actions.ROW_TEXT_CAP
    long_text = "r" * (cap + 55)
    short_text = "row two"
    matches = {"a": [FakeElement(text=long_text), FakeElement(text=short_text)]}

    result = await actions.query_selectors("sess1", ["a"], mgr=_mgr(matches=matches))

    assert result.truncated is True
    assert result.total_chars == len(long_text) + len(short_text)
    assert result.match_counts == {"a": 2}
    rows = result.results["a"]
    assert len(rows) == 2
    _assert_marked(rows[0]["text"], cap=cap, total=len(long_text))
    assert rows[1]["text"] == short_text


@pytest.mark.asyncio
async def test_query_selectors_row_count_cap_appends_an_inline_notice() -> None:
    total_matches = actions.ROW_COUNT_CAP + 7
    matches = {"a": [FakeElement(text="link", attrs={"href": "/x"}) for _ in range(total_matches)]}

    result = await actions.query_selectors("sess1", ["a"], mgr=_mgr(matches=matches))

    assert result.truncated is True
    assert result.match_counts == {"a": total_matches}
    rows = result.results["a"]
    # The capped rows PLUS one notice row the model reads in the same place.
    assert len(rows) == actions.ROW_COUNT_CAP + 1
    notice = rows[-1]["text"]
    assert "[truncated:" in notice
    assert f"{actions.ROW_COUNT_CAP:,}" in notice and f"{total_matches:,}" in notice
    # The notice keeps the row shape so a consumer iterating attributes survives.
    assert set(notice_keys := rows[-1].keys()) == set(rows[0].keys()), notice_keys


@pytest.mark.asyncio
async def test_query_selectors_under_caps_is_whole_and_unmarked() -> None:
    matches = {
        "a": [
            FakeElement(text="one", attrs={"href": "/1"}),
            FakeElement(text="two", attrs={"href": "/2"}),
        ]
    }

    result = await actions.query_selectors("sess1", ["a"], mgr=_mgr(matches=matches))

    assert result.truncated is False
    assert result.total_chars == len("one") + len("two")
    assert result.match_counts == {"a": 2}
    rows = result.results["a"]
    assert [r["text"] for r in rows] == ["one", "two"]
    _assert_clean("".join(str(r["text"]) for r in rows))


# ── body-text previews (navigate / click / type_text) ──────────────────────


@pytest.mark.asyncio
async def test_navigate_text_preview_over_cap_is_marked_and_declared() -> None:
    cap = actions.TEXT_PREVIEW_CAP
    text = "n" * (cap + 3)
    result = await actions.navigate(PUBLIC_URL, extract_text=True, mgr=_mgr(text=text))

    assert result.success is True, result.error_message
    assert result.truncated is True
    assert result.total_chars == len(text)
    _assert_marked(result.text_preview, cap=cap, total=len(text))


@pytest.mark.asyncio
async def test_click_text_preview_over_cap_is_marked_and_declared() -> None:
    cap = actions.TEXT_PREVIEW_CAP
    text = "c" * (cap + 12)
    result = await actions.click("sess1", "button", mgr=_mgr(text=text))

    assert result.success is True, result.error_message
    assert result.truncated is True
    assert result.total_chars == len(text)
    _assert_marked(result.text_preview, cap=cap, total=len(text))


@pytest.mark.asyncio
async def test_type_text_preview_over_cap_is_marked_and_declared() -> None:
    cap = actions.TEXT_PREVIEW_CAP
    text = "y" * (cap + 12)
    result = await actions.type_text("sess1", "input", "hello", mgr=_mgr(text=text))

    assert result.success is True, result.error_message
    assert result.truncated is True
    assert result.total_chars == len(text)
    _assert_marked(result.text_preview, cap=cap, total=len(text))


@pytest.mark.asyncio
async def test_previews_under_cap_are_whole_and_unmarked() -> None:
    text = "a short page"
    nav = await actions.navigate(PUBLIC_URL, extract_text=True, mgr=_mgr(text=text))
    clicked = await actions.click("sess1", "button", mgr=_mgr(text=text))
    typed = await actions.type_text("sess1", "input", "hi", mgr=_mgr(text=text))

    for result in (nav, clicked, typed):
        assert result.truncated is False
        assert result.total_chars == len(text)
        assert result.text_preview == text


@pytest.mark.asyncio
async def test_navigate_without_text_extraction_reports_no_truncation() -> None:
    result = await actions.navigate(PUBLIC_URL, mgr=_mgr(text="x" * 999_999))

    assert result.text_preview is None
    assert result.truncated is False
    assert result.total_chars == 0


# ── Structural guard — no reader may slice on a bare literal again ──────────


def test_no_numeric_literal_slice_bounds_remain_in_actions() -> None:
    """Every cap is a NAMED constant, declared once at the top of the module.

    An inline `html[:500_000]` is how the silent-truncation defect was written
    the first time: the number is invisible to the caller, un-referenceable by
    the router/client/tool-spec, and trivially forgotten when a reader is added.
    """
    source = pathlib.Path(actions.__file__).read_text()
    offenders: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Slice):
            for bound in (node.slice.lower, node.slice.upper):
                if isinstance(bound, ast.Constant) and isinstance(bound.value, int):
                    offenders.append(f"line {node.lineno}: slice bound {bound.value}")
    assert not offenders, "name these caps as module constants: " + "; ".join(offenders)


def test_every_reader_result_model_declares_the_truncation_contract() -> None:
    """A reader model that skips the mixin can truncate silently — pin the set."""
    for name in (
        "NavigateResult",
        "ClickResult",
        "TypeResult",
        "GetElementResult",
        "QuerySelectorsResult",
        "GetHtmlResult",
        "GetTextResult",
    ):
        model = getattr(actions, name)
        fields = model.model_fields
        assert "truncated" in fields and "total_chars" in fields, name
        blank = model(success=True)
        assert blank.truncated is False and blank.total_chars == 0, name
