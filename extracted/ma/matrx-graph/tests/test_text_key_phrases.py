"""text.key_phrases: phrases per item, appended to an entity list, stop words, ids/urls skipped, feeds spread_rank."""

from __future__ import annotations

from matrx_graph.nodes.text.key_phrases import mine_phrases, STOP_WORDS
from tests.test_text_nodes import _run_single_node

NODE = "text.key_phrases"


def test_runs_between_stop_words_become_phrases() -> None:
    got = mine_phrases(
        "We planned the sensory garden with raised beds. Maria's sensory garden needs shade.",
        max_chars=10_000, min_words=2, max_words=4, stop_words=STOP_WORDS,
    )
    assert "sensory garden" in got and "raised beds" in got
    assert "maria sensory garden" in got  # possessive dropped, not a separate phrase boundary
    assert all(len(p.split()) >= 2 for p in got)


def test_urls_ids_and_snake_case_are_never_phrases() -> None:
    got = mine_phrases(
        "See https://example.com/kitchen-plan and kitchen_plan_v2 and deadbeefcafe1234 kitchen plan.",
        max_chars=10_000, min_words=1, max_words=4, stop_words=STOP_WORDS,
    )
    assert not any("http" in p or "_" in p or "deadbeef" in p for p in got)
    assert "kitchen plan" in got


def test_long_runs_give_their_two_and_three_word_windows() -> None:
    got = mine_phrases("Riverside community greenhouse volunteer schedule draft",
                       max_chars=10_000, min_words=2, max_words=4, stop_words=STOP_WORDS)
    assert "riverside community" in got and "community greenhouse volunteer" in got
    assert "riverside community greenhouse volunteer schedule draft" not in got


async def test_records_get_phrases_appended_to_their_terms() -> None:
    items = [
        {"id": "n1", "title": "Bathroom remodel", "text": "Tile quote for the bathroom remodel.",
         "terms": [{"term": "Delgado Construction", "backed": True}]},
        {"id": "n2", "title": "", "text": ""},
        "Bathroom remodel budget and tile quote.",
    ]
    out = await _run_single_node(NODE, {"items": items}, {"text_paths": ["title", "text"]})
    assert out["__kind"] == "key_phrases_result"
    first = out["items"][0]
    assert first["terms"][0] == {"term": "Delgado Construction", "backed": True}
    assert "bathroom remodel" in first["terms"] and "tile quote" in first["terms"]
    assert first["terms"].count("bathroom remodel") == 1  # title and body give it once
    assert out["empty_items"] == [1] and out["items"][1]["terms"] == []
    assert out["items"][2]["text"].startswith("Bathroom") and "tile quote" in out["items"][2]["terms"]
    assert out["item_count"] == 3


async def test_settings_ignore_and_extra_stop_words() -> None:
    items = [{"text": "Quarterly board deck and quarterly board notes"}]
    out = await _run_single_node(NODE, {"items": items},
                                 {"extra_stop_words": ["notes"], "ignore_phrases": ["Quarterly Board Deck"]})
    terms = out["items"][0]["terms"]
    assert "quarterly board deck" not in terms and "quarterly board" in terms
    assert not any(t.endswith("notes") for t in terms)


async def test_a_non_text_field_fails_with_a_sentence() -> None:
    from matrx_graph.nodes.text.key_phrases import KeyPhrasesConfig, KeyPhrasesExecutor, KeyPhrasesInput
    from matrx_graph.types.result import Failure

    result = await KeyPhrasesExecutor().execute(
        None, KeyPhrasesInput(items=[{"text": 42}]), KeyPhrasesConfig()  # type: ignore[arg-type]
    )
    assert isinstance(result, Failure) and "not text" in str(result)


async def test_phrases_feed_spread_rank() -> None:
    items = [
        {"home": f"note-{i}", "kind": "notes", "text": f"Sensory garden visit {i}. Tile order."}
        for i in range(3)
    ]
    phrased = await _run_single_node(NODE, {"items": items}, {})
    ranked = await _run_single_node("data.spread_rank", {"items": phrased["items"]},
                                    {"min_homes": 2, "date_path": "", "top_n": 10})
    assert ranked["terms"][0]["key"].startswith("sensory garden")


async def test_mining_never_holds_the_event_loop(monkeypatch) -> None:
    """A big corpus mines off the loop: a concurrent DB round trip keeps getting turns.

    Run 40a1144a (2026-10-31): this step held the loop 82 s over 20,000 records, and the
    work queue's statement — Parsed, its Bind never sent — hit the server's statement
    timeout. The heartbeat stands in for that awaited round trip.
    """
    import asyncio
    import time

    words = ("riverside community greenhouse volunteer schedule draft budget tile quote "
             "bathroom remodel sensory garden raised beds shade planting").split()
    items = [
        {"id": f"n{i}", "text": " and ".join(" ".join(words[(i + k) % len(words)] for k in range(3))
                                            for _ in range(60))}
        for i in range(3_000)
    ]
    solo_started = time.perf_counter()
    for item in items:
        mine_phrases(item["text"], max_chars=40_000, min_words=2, max_words=4, stop_words=STOP_WORDS)
    solo = time.perf_counter() - solo_started
    assert solo > 0.5, f"corpus too small to prove anything (mining took {solo:.2f}s)"

    # The window the mining itself runs in, read off the thread that does it. The scheduler's
    # own validation of 3,000 inputs and outputs (and the helper's graph build) sit outside it
    # and pause the loop on any machine; they are not the mining and are not measured here.
    from matrx_graph.nodes.text import key_phrases

    window: list[float] = []
    real_mine_items = key_phrases._mine_items

    def timed_mine_items(*args, **kwargs):
        window.append(time.perf_counter())
        try:
            return real_mine_items(*args, **kwargs)
        finally:
            window.append(time.perf_counter())

    monkeypatch.setattr(key_phrases, "_mine_items", timed_mine_items)

    ticks: list[float] = []
    stop = asyncio.Event()

    async def heartbeat() -> None:
        while not stop.is_set():
            await asyncio.sleep(0.005)
            ticks.append(time.perf_counter())

    beat = asyncio.create_task(heartbeat())
    await asyncio.sleep(0.02)
    out = await _run_single_node(NODE, {"items": items})
    stop.set()
    await beat
    assert out["item_count"] == 3_000
    assert len(window) == 2, "the node never ran its mining through the timed hook"
    began, ended = window
    # Held on the loop, no tick lands between the first record and the last: the longest
    # pause inside the window is the whole mining time. Off it, ticks keep arriving.
    inside = [t for t in ticks if began <= t <= ended]
    longest = max(b - a for a, b in zip([began, *inside], [*inside, ended]))
    # The bar is 3/4 of the solo time, measured over the mining window only (runs 43736... and 43805837892, 2026-11-15/16,
    # failed on pauses OUTSIDE the mining: input/output validation and the helper's graph build). Mining ON the
    # loop leaves the window with no tick at all, so its longest pause is the full mining time.
    assert longest < solo * 0.75, f"the loop was held {longest:.2f}s; mining alone takes {solo:.2f}s"
