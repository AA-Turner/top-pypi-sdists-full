"""Reads of a run whose metric POINTS live at another tool (W&B live sync).

Such a run stores a passport, not a copy: the provider read paths refuse any
caller that has not declared which coverage contract it understands, and the
raw-row route refuses it outright because a raw row cannot carry a coverage
receipt. Neither refusal is an error the caller should surface -- together they
are the routing rules for reaching the points. Getting this wrong is not
theoretical: every MCP metric view reported mirrored runs as having no metrics
at all while the same data returned fine over HTTP.
"""

from __future__ import annotations

import json

import httpx
import pytest

from probe.mcp.service import ResearchReadService
from probe.sdk import errors
from probe.sdk.client import SOURCE_READ_CONTRACT, Client
from probe.sdk.config import Settings
from probe.sdk.reader import Reader
from probe.sdk.transport import Transport

_TOKEN = "probe_pat_" + "a" * 32
_SVC = "probe_svc_" + "a" * 32
_RUN = "11111111-2222-3333-4444-555555555555"


def _client(handler) -> Client:
    settings = Settings(base_url="http://test", token=_TOKEN)
    http = httpx.Client(base_url="http://test", transport=httpx.MockTransport(handler))
    return Client(settings=settings, transport=Transport(settings, client=http))


def _reader(handler) -> Reader:
    http = httpx.Client(base_url="http://test", transport=httpx.MockTransport(handler))
    return Reader(Transport(Settings(base_url="http://test", service_token=_SVC), client=http))


def _capture(payload):
    """Record the outgoing request and answer with `payload`."""
    seen: dict = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["params"] = dict(req.url.params)
        seen["body"] = json.loads(req.content) if req.content else None
        return httpx.Response(200, json=payload)

    return seen, handler


# -- the four contract-gated doors ------------------------------------------


def test_run_series_declares_the_contract() -> None:
    seen, handler = _capture([])
    _client(handler).run_series(_RUN)
    assert seen["params"]["source_read_contract"] == SOURCE_READ_CONTRACT


def test_query_series_declares_the_contract() -> None:
    seen, handler = _capture({"series": []})
    _client(handler).query_series([_RUN], keys=["train/loss"])
    assert seen["body"]["source_read_contract"] == SOURCE_READ_CONTRACT


def test_latest_scalars_declares_the_contract() -> None:
    seen, handler = _capture({"rows": []})
    _client(handler).latest_scalars([_RUN])
    assert seen["body"]["source_read_contract"] == SOURCE_READ_CONTRACT


def test_metrics_wide_declares_the_contract() -> None:
    seen, handler = _capture({"columns": [], "rows": [], "truncated": False, "next_step": None})
    _client(handler).get_metrics_wide(_RUN)
    assert seen["params"]["source_read_contract"] == SOURCE_READ_CONTRACT


def test_reader_declares_the_contract_on_both_doors() -> None:
    seen, handler = _capture([])
    _reader(handler).series(_RUN)
    assert seen["params"]["source_read_contract"] == SOURCE_READ_CONTRACT

    seen, handler = _capture({"series": []})
    _reader(handler).series_query([_RUN])
    assert seen["body"]["source_read_contract"] == SOURCE_READ_CONTRACT


def test_an_explicit_contract_is_not_overwritten() -> None:
    """setdefault, not assignment: a caller pinning a contract keeps it."""
    seen, handler = _capture({"series": []})
    _client(handler).query_series([_RUN], source_read_contract="coverage-v9")
    assert seen["body"]["source_read_contract"] == "coverage-v9"


# -- the raw-row refusal is a routing instruction, not a failure -------------


class _Source:
    """Stands in for the MCP's backend wrapper. `run_metrics` refuses the way the
    real route does; `query_series` answers the way the real one does."""

    def __init__(self, *, refuse: bool, detail=None):
        self.refuse = refuse
        self.detail = detail
        self.query_calls: list[tuple] = []

    def run_metrics(self, run_id, **kw):
        if self.refuse:
            raise errors.ValidationError("refused", status=422, detail=self.detail)
        return [{"key": "train/loss", "value": 1.0, "step_index": 1}]

    def query_series(self, run_ids, **body):
        self.query_calls.append((tuple(run_ids), body))
        return {
            "series": [
                {
                    "run_id": run_ids[0],
                    "kind": "model",
                    "key": "train/loss",
                    "dimensions": {},
                    "points": [
                        {"step_index": 1, "wall_clock": "2026-09-18T00:00:00Z", "value": 0.5},
                        {"step_index": 2, "wall_clock": "2026-09-18T00:01:00Z", "value": 0.4},
                    ],
                }
            ]
        }


def _points(source, **filters):
    return ResearchReadService._metric_points(source_holder(source), _RUN, limit=10, **filters)


def source_holder(source):
    class _Holder:
        pass

    holder = _Holder()
    holder.source = source
    return holder


def test_a_refused_raw_read_falls_through_to_the_series_door() -> None:
    source = _Source(
        refuse=True,
        detail={"code": "unsupported_source_query", "message": "use /v1/series/query"},
    )
    rows = _points(source, key="train/loss")
    assert [r["value"] for r in rows] == [0.5, 0.4]
    assert [r["step_index"] for r in rows] == [1, 2]
    assert all(r["key"] == "train/loss" and r["kind"] == "model" for r in rows)
    # the key filter has to survive the reroute, or the fallback reads the whole run
    assert source.query_calls == [((_RUN,), {"keys": ["train/loss"]})]


def test_the_kind_filter_survives_the_reroute() -> None:
    source = _Source(refuse=True, detail={"code": "unsupported_source_query"})
    _points(source, key="train/loss", kind="model")
    assert source.query_calls[0][1] == {"keys": ["train/loss"], "kind": "model"}


def test_the_fallback_respects_the_caller_limit() -> None:
    source = _Source(refuse=True, detail={"code": "unsupported_source_query"})
    rows = ResearchReadService._metric_points(
        source_holder(source), _RUN, limit=1, key="train/loss"
    )
    assert len(rows) == 1


def test_an_unrelated_validation_error_still_raises() -> None:
    """Only THIS refusal is a routing instruction. Swallowing every 422 would
    turn a genuine bad request into a silent empty read."""
    source = _Source(refuse=True, detail={"code": "some_other_problem"})
    with pytest.raises(errors.ValidationError):
        _points(source, key="train/loss")


def test_a_local_run_is_untouched_by_any_of_this() -> None:
    source = _Source(refuse=False)
    rows = _points(source, key="train/loss")
    assert rows == [{"key": "train/loss", "value": 1.0, "step_index": 1}]
    assert source.query_calls == []
