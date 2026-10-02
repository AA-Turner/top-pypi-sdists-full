"""The scrubber skips only EXACT ISO timestamps on metric points (PR #2002 review).

`Run.log` stamps every point's `wall_clock` (plan 1.4); scrubbing each stamp at
five boundaries made `log()` 8-26% slower. `probe.sdk.stamp_scrub` lifts such a
timestamp out, scrubs the rest with the unchanged shared scrubber, and puts it
back. These tests pin the three things that must hold: it saves the calls, it
never skips a string that could hold a credential, and its output is exactly
`default_scrub`'s.
"""

from __future__ import annotations

import json

import pytest

import probe.sdk.run as run_module
from probe.sdk import redaction
from probe.sdk.redaction import default_scrub
from probe.sdk.stamp_scrub import scrub_body, scrub_op
from tests.conftest import make_client, open_run

_TOKEN = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"


def _count_scrubs(monkeypatch, fn) -> int:
    calls = {"n": 0}
    real = redaction.scrub_string

    def counting(value, **kw):
        calls["n"] += 1
        return real(value, **kw)

    monkeypatch.setattr(redaction, "scrub_string", counting)
    try:
        fn()
    finally:
        monkeypatch.setattr(redaction, "scrub_string", real)
    return calls["n"]


@pytest.mark.parametrize("keys", [5, 20])
def test_a_stamped_log_costs_the_same_scrubs_as_an_unstamped_one(app, tmp_path, monkeypatch, keys):
    """The review's measure, on the async path production defaults to: before
    the fix a stamp added 6 scrub_string calls per point (the `wall_clock` key
    and value at three enqueue boundaries), 154 -> 184 at 5 keys."""
    client = make_client(app, tmp_spool=tmp_path / "spool", async_writes=True)
    run = open_run(client, experiment="e", name="r")
    metrics = {f"key_{i}": 0.5 + i for i in range(keys)}
    run.log(metrics, step=0)  # warm any first-call work

    stamped = _count_scrubs(monkeypatch, lambda: run.log(metrics, step=1))
    monkeypatch.setattr(run_module, "_log_stamp", lambda: None)  # no wall_clock at all
    unstamped = _count_scrubs(monkeypatch, lambda: run.log(metrics, step=2))

    assert stamped == unstamped


def _stamped_body() -> dict:
    return {
        "points": [
            {"dimensions": {}, "key": f"k{i}", "kind": "model", "step_index": 3, "value": 0.5,
             "wall_clock": "2026-09-27T01:02:03.456789Z"}
            for i in range(3)
        ],
        "session_id": "00000000-0000-4000-8000-000000000000",
        "write_epoch": 1,
    }


def test_the_output_is_byte_identical_to_the_plain_scrubber():
    body = _stamped_body()
    assert json.dumps(scrub_body(body)) == json.dumps(default_scrub(body))
    op = {"kind": "http", "method": "POST", "path": "/v1/runs/x/metrics", "body": body}
    assert json.dumps(scrub_op(op)) == json.dumps(default_scrub(op))


def test_it_does_not_mutate_its_input():
    body = _stamped_body()
    before = json.dumps(body)
    scrub_body(body)
    scrub_op({"body": body})
    assert json.dumps(body) == before


@pytest.mark.parametrize(
    "value",
    [
        _TOKEN,  # a credential where a timestamp should be
        f"2026-09-27T00:00:00+00:00 {_TOKEN}",  # a timestamp PREFIX is not a timestamp
        f"2026-09-27T00:00:00+00:00\n{_TOKEN}",
    ],
)
def test_anything_but_an_exact_timestamp_is_still_scrubbed(value):
    body = {"points": [{"key": "k", "value": 1.0, "wall_clock": value}]}
    for scrubbed in (scrub_body(body)["points"][0], scrub_op({"body": body})["body"]["points"][0]):
        assert _TOKEN not in scrubbed["wall_clock"]
        assert scrubbed == default_scrub(body)["points"][0]


def test_a_credential_elsewhere_in_a_stamped_body_is_still_scrubbed():
    body = _stamped_body()
    body["points"][0]["labels"] = {"note": _TOKEN}
    assert _TOKEN not in json.dumps(scrub_body(body))
    assert _TOKEN not in json.dumps(scrub_op({"body": body}))


# -- read-capture rows (plan (k) review) ---------------------------------------------
#
# `inputs._typed_row` checks a read row's hash, fingerprint, size, `stable` and
# timestamp by SHAPE; only the path and host are free text. Lifting the checked
# fields past the scrubber must change nothing but the cost.



def _read_rows(n: int = 50) -> list[dict]:
    import hashlib

    from probe.sdk import inputs

    rows = []
    for i in range(n):
        sha = hashlib.sha256(str(i).encode()).hexdigest()
        path = f"/data/{_TOKEN}/x-{i}.bin" if i == 7 else f"/data/shards/train-{i}.parquet"
        rows.append(inputs._typed_row(path, sha if i % 3 else None, f"{i}:{1727300000 + i}:{sha}" if i % 2 else None,
                                      i, f"host-{i % 2}", bool(i % 5), f"2026-09-26T00:00:{i % 60:02d}.{i:06d}+00:00"))
    return rows


def test_read_rows_scrub_byte_identical_to_the_plain_scrubber():
    rows = _read_rows()
    body = {"inputs": rows, "coverage": {"recorder": "python-audit-hook", "count": len(rows)}}
    op = {"id": "op-1", "method": "POST", "path": "/v1/runs/r/inputs", "body": body}
    assert json.dumps(scrub_body(body)) == json.dumps(default_scrub(body))
    assert json.dumps(scrub_op(op)) == json.dumps(default_scrub(op))
    assert _TOKEN not in json.dumps(scrub_body(body)), "the path is still scrubbed"


def test_read_rows_skip_only_their_shape_checked_fields(monkeypatch):
    """The lift is what keeps 10k rows inside the scrub cache: hashes,
    fingerprints and timestamps never reach `scrub_string`. Negative control: a
    row that is NOT exactly `_typed_row`'s shape is scrubbed whole."""
    rows = _read_rows(20)
    seen: list[str] = []
    real = redaction.scrub_string
    monkeypatch.setattr(redaction, "scrub_string", lambda v, **k: seen.append(v) or real(v, **k))
    scrub_body({"inputs": rows})
    checked = {r["content_hash"] for r in rows} | {r["fingerprint"] for r in rows} | {r["first_seen_at"] for r in rows}
    assert not checked & set(seen)
    assert {r["path"] for r in rows} <= set(seen)
    seen.clear()
    odd = [{**rows[0], "extra": "x"}]
    scrub_body({"inputs": odd})
    assert odd[0]["first_seen_at"] in seen, "an unrecognised row goes through the scrubber whole"


@pytest.mark.parametrize(
    "field,value",
    [("content_hash", "api_key=" + "a" * 56), ("fingerprint", "token " + _TOKEN), ("first_seen_at", "password=hunter2"),
     ("size_bytes", "12"), ("stable", "yes")],
)
def test_a_read_field_that_is_not_its_shape_is_scrubbed(field, value):
    rows = _read_rows(3)
    rows[1] = {**rows[1], field: value}
    body = {"inputs": rows}
    assert json.dumps(scrub_body(body)) == json.dumps(default_scrub(body))
