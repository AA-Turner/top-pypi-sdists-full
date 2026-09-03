"""The per-call cap on xpworkspace-context-retrieve.

Encryption makes retrieve the only channel plaintext reaches the model, so it never inherited
the caps a bash/read tool gets for free: a call with neither query nor semantic_query returned
the whole decrypted file, and a 5.7MB payload went to the provider in one piece. The cap runs
after decrypt and filtering, for every retrieve, and hands back a page plus how to ask for the
next one.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from xpander_sdk.core.context_optimizer.search import (
    RETRIEVE_PAGE_CHARS,
    _RETRY_NUDGE,
    page_text,
)


def _lines(n: int, width: int = 99) -> str:
    return "".join(f"{'x' * width}\n" for _ in range(n))


# ---- the page window ---------------------------------------------------- #


def test_a_payload_under_budget_is_returned_whole_and_unannotated():
    text = _lines(10)
    page, notice = page_text(text, budget=RETRIEVE_PAGE_CHARS)
    assert page == text
    assert notice == ""


def test_an_oversized_payload_is_cut_to_the_budget():
    text = _lines(200_000)  # 20MB
    page, notice = page_text(text, budget=100_000)
    assert len(page) <= 100_000
    assert notice.startswith("[PARTIAL: showing chars 0-")


def test_the_notice_names_the_real_total_and_the_next_offset():
    text = _lines(2_000)
    page, notice = page_text(text, budget=50_000)
    assert f"of {len(text):,}" in notice
    assert f"offset={len(page)}" in notice


def test_a_page_ends_on_a_line_boundary():
    text = _lines(2_000)
    page, _ = page_text(text, budget=50_000)
    assert page.endswith("\n")


def test_a_blob_with_no_newline_is_still_capped():
    """One-line JSON is the shape that motivated the cap - it must not slip through."""
    text = "y" * 500_000
    page, notice = page_text(text, budget=100_000)
    assert len(page) == 100_000
    assert notice


# ---- paging ------------------------------------------------------------- #


def test_offset_returns_the_next_window():
    text = _lines(2_000)
    first, notice = page_text(text, budget=50_000)
    nxt = int(notice.split("offset=")[1].split()[0])
    second, _ = page_text(text, offset=nxt, budget=50_000)
    assert second
    assert first + second == text[: len(first) + len(second)]


def test_sequential_pages_reconstruct_the_whole_payload():
    text = _lines(500)
    out, offset, guard = "", 0, 0
    while guard < 100:
        guard += 1
        page, notice = page_text(text, offset=offset, budget=10_000)
        out += page
        if "offset=" not in notice:
            break
        offset = int(notice.split("offset=")[1].split()[0])
    assert out == text


def test_the_final_page_says_so_and_offers_no_next_offset():
    text = _lines(2_000)
    _, notice = page_text(text, offset=len(text) - 100, budget=50_000)
    assert "final page" in notice
    assert "offset=" not in notice


def test_an_offset_past_the_end_yields_an_empty_page():
    text = _lines(10)
    page, notice = page_text(text, offset=10**9, budget=1_000)
    assert page == ""
    assert "final page" in notice


@pytest.mark.parametrize("offset", [None, -5, "not-a-number"])
def test_a_junk_offset_does_not_raise(offset):
    text = _lines(10)
    try:
        value = max(0, int(offset or 0))
    except (TypeError, ValueError):
        value = 0
    page, _ = page_text(text, offset=value, budget=1_000)
    assert isinstance(page, str)


# ---- the headroom clamp -------------------------------------------------- #


def _budget_for(free_tokens: int) -> int:
    from xpander_sdk.modules.backend.frameworks.agno import _retrieve_page_budget

    optimizer = SimpleNamespace(
        _auto_compact_threshold=free_tokens, _last_estimated_tokens=0
    )
    return _retrieve_page_budget(SimpleNamespace(_xp_context_optimizer=optimizer))


def test_a_roomy_window_gets_the_full_page():
    assert _budget_for(500_000) == RETRIEVE_PAGE_CHARS


def test_a_nearly_full_window_shrinks_the_page():
    """A legal first page must not itself trigger the compaction it exists to avoid."""
    assert _budget_for(6_000) < RETRIEVE_PAGE_CHARS


def test_a_full_window_still_returns_something_readable():
    assert _budget_for(0) >= 1


def test_no_optimizer_falls_back_to_the_flat_page():
    from xpander_sdk.modules.backend.frameworks.agno import _retrieve_page_budget

    assert _retrieve_page_budget(SimpleNamespace()) == RETRIEVE_PAGE_CHARS
    assert _retrieve_page_budget(None) == RETRIEVE_PAGE_CHARS


def test_a_broken_optimizer_never_breaks_the_retrieve():
    from xpander_sdk.modules.backend.frameworks.agno import _retrieve_page_budget

    class _Broken:
        @property
        def _auto_compact_threshold(self):
            raise RuntimeError("no window")

    assert _retrieve_page_budget(SimpleNamespace(_xp_context_optimizer=_Broken())) > 0


# ---- the prompt that invited the full pull -------------------------------- #


def test_the_search_miss_nudge_no_longer_advertises_a_full_pull():
    assert "omit both query and semantic_query" not in _RETRY_NUDGE
    assert "offset" in _RETRY_NUDGE


def test_the_retrieve_guidance_teaches_paging():
    from xpander_sdk.modules.backend.frameworks.agno import (
        CONTEXT_OPTIMIZATION_INSTRUCTIONS as guidance,
    )

    assert "omit both query and semantic_query for the full result" not in guidance
    assert "[PARTIAL" in guidance and "offset" in guidance


# ---- every result shape the hook can be handed --------------------------- #
#
# The cap reads and writes the payload through one pair of helpers. They were closures
# nested inside the query branch until the cap had to cover the no-query path too, so each
# branch here is a shape that would otherwise slip through uncapped.


def _tool_invocation_result(content: str):
    from xpander_sdk.modules.tools_repository.models.tool_invocation_result import (
        ToolInvocationResult,
    )

    return ToolInvocationResult(
        function_name="xpworkspace-context-retrieve", tool_id="wt1", payload={},
        tool_call_id="t1", is_success=True, result={"content": content},
    )


class _WithContent:
    def __init__(self, content):
        self.content = content


def _shapes(content: str):
    return {
        "ToolInvocationResult": _tool_invocation_result(content),
        "object.content": _WithContent(content),
        "plain dict": {"content": content},
    }


@pytest.mark.parametrize("shape", ["ToolInvocationResult", "object.content", "plain dict"])
def test_the_payload_is_readable_from_every_shape(shape):
    from xpander_sdk.modules.backend.frameworks.agno import retrieve_plain_text

    assert retrieve_plain_text(_shapes("hello")[shape]) == "hello"


@pytest.mark.parametrize("shape", ["ToolInvocationResult", "object.content", "plain dict"])
def test_a_capped_page_is_written_back_into_every_shape(shape):
    """A shape the setter misses returns the full payload - the exact bug being fixed."""
    from xpander_sdk.modules.backend.frameworks.agno import (
        retrieve_plain_text,
        set_retrieve_plain_text,
    )

    payload = _lines(200_000)  # ~20MB
    result = _shapes(payload)[shape]
    page, notice = page_text(retrieve_plain_text(result), budget=RETRIEVE_PAGE_CHARS)
    set_retrieve_plain_text(result, page)

    assert notice
    written = retrieve_plain_text(result)
    assert len(written) <= RETRIEVE_PAGE_CHARS
    assert written != payload
    assert payload.startswith(written)


def test_a_non_dict_tool_invocation_result_round_trips():
    """result.result is not always a dict; the setter has a separate branch for that."""
    from xpander_sdk.modules.backend.frameworks.agno import (
        retrieve_plain_text,
        set_retrieve_plain_text,
    )

    r = _tool_invocation_result("x")
    r.result = "raw string payload"
    assert retrieve_plain_text(r) == "raw string payload"
    set_retrieve_plain_text(r, "capped")
    assert retrieve_plain_text(r) == "capped"


def test_an_unknown_shape_is_reported_as_absent_and_never_raises():
    from xpander_sdk.modules.backend.frameworks.agno import (
        retrieve_plain_text,
        set_retrieve_plain_text,
    )

    assert retrieve_plain_text(object()) is None
    set_retrieve_plain_text(object(), "ignored")  # must not raise


def test_the_notice_is_appended_to_the_result_the_model_sees():
    """Capping without the notice would silently truncate - the model must learn it can page."""
    from xpander_sdk.core.steering import append_to_tool_result
    from xpander_sdk.modules.backend.frameworks.agno import (
        retrieve_plain_text,
        set_retrieve_plain_text,
    )

    result = _tool_invocation_result(_lines(200_000))
    page, notice = page_text(retrieve_plain_text(result), budget=RETRIEVE_PAGE_CHARS)
    set_retrieve_plain_text(result, page)
    result = append_to_tool_result(result, notice)

    assert "[PARTIAL: showing chars" in str(retrieve_plain_text(result))
