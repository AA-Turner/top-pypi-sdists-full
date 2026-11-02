"""The debug-off screen view of a step's output (Arman, 2026-10-15: the client gets only what it renders).

Creativity Warehouse, 2026-10-16: one Identify run's debug-off events were 609 KB — agent transcripts, request and
search ledgers, every engine object of every hit — and ``GET /runs/{id}`` sent its whole 2.4 MB output."""

from __future__ import annotations

import json

from matrx_graph.checkpoint.value_store import _screen_trim, screen_value

_ENGINE = {"title": "Creativity Warehouse - Yelp", "cluster": [{"url": "https://www.yelp.com/la"}] * 40}


def _evidence() -> dict:
    return {
        "key": "listing:yelp.com/biz/creativity-warehouse",
        "field": "listing",
        "value": "https://www.yelp.com/biz/creativity-warehouse",
        "raw_results": [{"rank": 3, "engine": "brave", "result": _ENGINE},
                        {"rank": 1, "engine": "google", "result": _ENGINE},
                        {"rank": 2, "engine": "brave", "result": _ENGINE}],
    }


def test_ledgers_and_transcripts_never_ship():
    out = screen_value({
        "evidence": [_evidence()],
        "requests": [{"url": "https://api.search.brave.com", "body": "x" * 5000}],
        "searches": [{"q": "x"}],
        "results_by_engine": {"brave": ["x" * 5000]},
        "html": "<html>" + "x" * 10000,
        "messages": [{"role": "system", "content": "the full prompt"}],
        "final_text": "answer",
    })
    assert set(out) == {"evidence", "messages", "final_text"}
    assert out["messages"] == []
    raw = out["evidence"][0]["raw_results"]
    assert len(raw) == 1 and raw[0]["rank"] == 1  # the one result the screen draws


def test_agent_result_kind_keeps_its_content_but_never_its_transcript():
    kind = {"__kind": "agent_result", "final_text": "hi", "structured_output": {"a": 1},
            "messages": [{"role": "user", "content": "secret prompt"}], "html": "<b>rendered</b>"}
    out = screen_value({"content": [kind]})
    assert out["content"][0]["messages"] == []
    assert out["content"][0]["html"] == "<b>rendered</b>"  # a kind's own field is rendered content
    assert out["content"][0]["structured_output"] == {"a": 1}


def test_event_payloads_are_screened_and_shrink():
    payload = {"event": "node_emitted", "node_id": "web", "payload": {"brand_evidence": [_evidence()] * 10}}
    before = len(json.dumps(payload))
    after = _screen_trim(payload)
    assert len(json.dumps(after)) < before / 2
    done = _screen_trim({"event": "node_completed", "output": {"requests": [1], "messages": [{"c": "x"}], "ok": 1}})
    assert done["output"] == {"messages": [], "ok": 1}


# --- Debug-off bytes, round 2 (Creativity Warehouse, 2026-10-16: 1.3 MB of events + 1.2 MB of run records for
# four runs after round 1; the target is under 0.5 MB per run). Each piece is sent once and only what renders. ---

from matrx_graph.checkpoint import value_store  # noqa: E402


def test_search_rows_keep_only_the_fields_the_web_result_draws():
    engine = {"title": "Yelp", "url": "https://y", "description": "d", "extra_snippets": ["e"],
              "profile": {"name": "Yelp", "img": "https://i", "long_name": "yelp.com", "url": "https://y"},
              "thumbnail": {"src": "https://t", "original": "https://o", "logo": True},
              "cluster": [{"url": "https://www.yelp.com/la"}] * 40, "language": "en", "family_friendly": True}
    out = screen_value({"evidence": [{"key": "k", "raw_results": [{"rank": 1, "engine": "brave", "result": engine}]}]})
    row = out["evidence"][0]["raw_results"][0]
    assert row["rank"] == 1 and row["engine"] == "brave"
    assert set(row["result"]) == {"title", "url", "description", "extra_snippets", "profile", "thumbnail"}
    assert row["result"]["profile"] == {"name": "Yelp", "img": "https://i"}
    assert row["result"]["thumbnail"] == {"src": "https://t"}


def test_agent_answer_is_sent_once_in_content():
    content = [{"__kind": "brand_basics", "brand_name": "Creativity Warehouse", "facts": [{"field": "name"}]}]
    agent = {"__kind": "agent_result", "content": content, "final_text": "x" * 9000, "final_message": {"text": "x" * 9000},
             "structured_output": {"facts": ["x" * 9000]}, "usage": {"total_tokens": 9}, "messages": []}
    out = screen_value({"facts": agent})["facts"]
    assert out["content"] == content
    assert out["final_text"] == "" and "final_message" not in out and "structured_output" not in out
    assert out["usage"] == {"total_tokens": 9}
    # No content: the answer fields are the answer and stay.
    bare = screen_value({"__kind": "agent_result", "content": [], "final_text": "hi", "structured_output": {"a": 1}})
    assert bare["final_text"] == "hi" and bare["structured_output"] == {"a": 1}


def _finding(key: str) -> dict:
    return {"key": key, "field": "listing", "value": f"https://{key}", "confidence": 0.9}


def test_findings_already_emitted_are_a_marker_on_node_completed():
    seen: dict = {}
    items = [_finding("a.com"), _finding("b.com")]
    emitted = {"event": "node_emitted", "node_id": "probe", "payload": {"brand_evidence": items}}
    assert value_store.mark_emitted(emitted, seen) == emitted
    done = {"event": "node_completed", "node_id": "probe",
            "output": {"evidence": [*items, _finding("c.com")], "notes": ["n"]}}
    out = value_store.mark_emitted(done, seen)
    assert out["output"]["evidence"] == [{value_store.EMITTED_KEY: "a.com"}, {value_store.EMITTED_KEY: "b.com"}, _finding("c.com")]
    assert out["output"]["notes"] == ["n"]
    # Another node, or a response that never carried the emitted event, gets the full items.
    assert value_store.mark_emitted({**done, "node_id": "page"}, seen)["output"]["evidence"][0] == items[0]
    assert value_store.mark_emitted(done, {})["output"]["evidence"][0] == items[0]


async def test_screen_views_marks_emitted_findings_per_response_and_per_stream():
    items = [_finding("a.com")]
    events = [{"event": "node_emitted", "node_id": "probe", "payload": {"brand_evidence": items}},
              {"event": "node_completed", "node_id": "probe", "output": {"evidence": items}}]
    views = await value_store.screen_views("bytes-r2", events)
    assert views[1]["output"]["evidence"] == [{value_store.EMITTED_KEY: "a.com"}]
    stream: dict = {}
    await value_store.screen_views("bytes-r2", events[:1], stream)
    later = await value_store.screen_views("bytes-r2", events[1:], stream)
    assert later[0]["output"]["evidence"] == [{value_store.EMITTED_KEY: "a.com"}]


def test_run_record_withholds_large_non_kind_step_values_like_events():
    kinds = [{"__kind": "brand_basics", "brand_name": "x" * 6000}]
    output = {
        "web": {"evidence": [_finding(f"{i}.com") for i in range(200)], "domain": "cw.com", "requests": [1]},
        "facts": {"__kind": "agent_result", "content": kinds, "final_text": "y" * 9000, "metadata": {"m": 1}},
        "page": "z" * 5000,
    }
    out = value_store.screen_run_output(output, 4096)
    assert out["web"] == {"domain": "cw.com"}
    assert out["facts"]["content"] == kinds and out["facts"]["final_text"] == "" and out["facts"]["metadata"] == {"m": 1}
    assert "page" not in out


def test_run_record_describes_each_value_it_withholds_without_changing_its_shape():
    """2026-10-29: the record keeps the drop, and a collector says what was cut, where, and how big."""
    output = {"web": {"evidence": [_finding(f"{i}.com") for i in range(200)], "domain": "cw.com"}, "page": "z" * 5000}
    cut: list = []
    out = value_store.screen_run_output(output, 4096, cut)
    assert out == {"web": {"domain": "cw.com"}}
    by_path = {tuple(c["path"]): c for c in cut}
    assert by_path[("web", "evidence")]["value_type"] == "list" and by_path[("web", "evidence")]["items"] == 200
    assert by_path[("page",)] == {"path": ["page"], "value_type": "text", "bytes": 5002, "items": None,
                                  "chars": 5000, "ref": None}


def test_every_screen_cut_is_described_where_it_was():
    """2026-10-29: a debug-only field, a transcript and the engine rows past the first were cut with nothing to
    say so. The screened value is unchanged; the collector names each cut, its type and its size."""
    value = {
        "html": "<p>" + "h" * 500 + "</p>",
        "messages": [{"role": "user", "content": "hi"}],
        "raw_results": [{"rank": 2, "result": {"title": "b"}}, {"rank": 1, "result": {"title": "a"}}],
        "kept": 1,
    }
    cut: list = []
    out = value_store.screen_value(value, cut, ["output"])
    assert out == value_store.screen_value(value)
    assert "html" not in out and out["messages"] == [] and len(out["raw_results"]) == 1
    by_path = {tuple(c["path"]): c for c in cut}
    assert by_path[("output", "html")]["value_type"] == "text" and by_path[("output", "html")]["chars"] == 507
    assert by_path[("output", "messages")]["items"] == 1
    assert by_path[("output", "raw_results")]["items"] == 1
    assert ("output", "kept") not in by_path
