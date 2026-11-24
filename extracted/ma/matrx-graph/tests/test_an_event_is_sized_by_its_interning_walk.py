"""An event's large data values are interned in ONE walk (L-SPEED round 2, 2026-11-09).

``event_payload_row`` first measured each field with ``_leaf_bytes`` — a sorted JSON dump of the whole
multi-MB step input/output — and then walked it again to intern it: every large ``node_started`` /
``node_completed`` / ``run_completed`` serialized its values twice. It now sizes by the interning walk (the
outcome rule, ``outcome_input_row``). Red with the old function: ~2x the value's bytes dumped.
"""

import json

from matrx_graph.checkpoint import values as V

LIMIT = 32 * 1024


def _sources(n: int) -> list[dict]:
    return [{"id": f"s{i}", "title": f"Source {i} " + "word " * 40, "score": i % 7, "links": [f"https://x/{i}/{j}" for j in range(5)]}
            for i in range(n)]


def _dumped_bytes(monkeypatch, fn):
    seen = [0]
    real = V._dumps

    def counting(value):
        text = real(value)
        seen[0] += len(text)
        return text

    monkeypatch.setattr(V, "_dumps", counting)
    out = fn()
    monkeypatch.setattr(V, "_dumps", real)
    return out, seen[0]


def test_a_large_event_is_dumped_about_once(monkeypatch):
    items = _sources(2000)
    size = len(V._dumps(items))
    assert size > 10 * LIMIT
    for payload in ({"event": "node_completed", "output": items},
                    {"event": "node_started", "inputs": {"items": items, "topic": "t"}}):
        (out, store), dumped = _dumped_bytes(monkeypatch, lambda p=payload: V.event_payload_row(p, LIMIT))
        assert dumped < 1.2 * size, (payload["event"], dumped, size)
        assert V.resolve_values(out, store) == payload
        assert len(json.dumps(out)) < LIMIT


def test_a_mapping_keeps_its_keys_and_a_small_event_is_untouched():
    items = _sources(2000)
    payload = {"event": "node_started", "inputs": {"items": items, "topic": "t"}, "node_id": "n"}
    out, store = V.event_payload_row(payload, LIMIT)
    assert out["inputs"]["topic"] == "t" and V.REF_KEY in out["inputs"]["items"]
    assert out["node_id"] == "n" and payload["inputs"]["items"] is items
    small = {"event": "node_completed", "output": {"a": 1}}
    assert V.event_payload_row(small, LIMIT) == (small, {})
    assert V.event_payload_row(small, LIMIT)[0] is small
