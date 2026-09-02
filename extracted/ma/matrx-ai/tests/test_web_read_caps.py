"""web read/batch_read paging + whole-result budget (tool self-cap)."""

from __future__ import annotations

import json

from matrx_ai.tools.implementations._web_read_caps import (
    DEFAULT_CHARS,
    RESULT_BUDGET_CHARS,
    SHORT_PAGE_FULL_CHARS,
    enforce_result_budget,
    extract_page_text,
    per_url_budget,
    resolve_chars,
    window_page_content,
)


def test_short_page_returns_all_on_default_first_read() -> None:
    text = "x" * 12_000  # < 16k
    page = window_page_content(text, url="https://example.com", offset=0, chars=DEFAULT_CHARS)
    assert page["chars_returned"] == 12_000
    assert page["total_chars"] == 12_000
    assert page["has_more"] is False
    assert page["next_offset"] is None
    assert page["truncation_notice"] is None


def test_long_page_defaults_to_8k_window() -> None:
    text = "y" * 50_000
    page = window_page_content(text, url="https://example.com", offset=0, chars=DEFAULT_CHARS)
    assert page["chars_returned"] == DEFAULT_CHARS
    assert page["has_more"] is True
    assert page["next_offset"] == DEFAULT_CHARS
    assert page["truncation_notice"]


def test_offset_continues_from_next_offset() -> None:
    text = "z" * 20_000
    first = window_page_content(text, url="u", offset=0, chars=DEFAULT_CHARS)
    second = window_page_content(text, url="u", offset=first["next_offset"], chars=DEFAULT_CHARS)
    assert (
        first["content"] + second["content"]
        == text[: first["chars_returned"] + second["chars_returned"]]
    )
    assert second["offset"] == DEFAULT_CHARS


def test_explicit_small_chars_not_auto_expanded() -> None:
    text = "a" * 10_000
    page = window_page_content(text, url="u", offset=0, chars=1_000)
    assert page["chars_returned"] == 1_000
    assert page["has_more"] is True


def test_short_page_respects_batch_budget() -> None:
    text = "b" * 15_000
    page = window_page_content(text, url="u", offset=0, chars=DEFAULT_CHARS, per_url_budget=4_000)
    assert page["chars_returned"] == 4_000
    assert page["has_more"] is True


def test_resolve_chars_prefers_explicit_chars() -> None:
    assert (
        resolve_chars(
            chars=12_000,
            max_content_length=8_000,
            fields_set={"chars", "max_content_length"},
        )
        == 12_000
    )


def test_resolve_chars_legacy_max_content_length() -> None:
    assert (
        resolve_chars(
            chars=DEFAULT_CHARS,
            max_content_length=20_000,
            fields_set={"max_content_length"},
        )
        == 20_000
    )


def test_extract_page_text_prefers_raw_text() -> None:
    assert (
        extract_page_text(
            {
                "status": "success",
                "text": "raw",
                "result": 'Here is the content from page x: """\nwrapped\n"""',
            }
        )
        == "raw"
    )


def test_per_url_budget_splits_result_budget() -> None:
    assert per_url_budget(4) == RESULT_BUDGET_CHARS // 4


def test_enforce_result_budget_shrinks_oversized_batch() -> None:
    pages = [
        window_page_content("c" * 40_000, url=f"https://ex/{i}", offset=0, chars=40_000)
        for i in range(4)
    ]
    output = {"pages": pages, "count": 4, "succeeded": 4, "failed": 0}
    # Force over budget even after per-url windowing by using huge chars.
    assert len(json.dumps(output)) > RESULT_BUDGET_CHARS
    enforce_result_budget(output, budget=RESULT_BUDGET_CHARS)
    assert len(json.dumps(output, default=str)) <= RESULT_BUDGET_CHARS
    assert output.get("result_truncated") is True


def test_boundary_exactly_two_pages_is_short() -> None:
    text = "d" * SHORT_PAGE_FULL_CHARS
    page = window_page_content(text, url="u", offset=0, chars=DEFAULT_CHARS)
    assert page["chars_returned"] == SHORT_PAGE_FULL_CHARS
    assert page["has_more"] is False


def test_just_over_two_pages_is_windowed() -> None:
    text = "e" * (SHORT_PAGE_FULL_CHARS + 1)
    page = window_page_content(text, url="u", offset=0, chars=DEFAULT_CHARS)
    assert page["chars_returned"] == DEFAULT_CHARS
    assert page["has_more"] is True
