"""GUARD: provider-vs-catalog cost drift reaches the ops issue-class surface.

Before 2026-09-11 `requests.to_storage_dict` computed `catalog_cost_usd`,
`provider_charge_usd` and `provider_catalog_variance_usd` into
`chat.request.metadata` and NOTHING read them. This guard fails if that silence
comes back: the routing call must exist at the seam, past-tolerance drift must
file one issue-class event carrying BOTH numbers and the offering id, and it
must file at most one per model per day.
"""

from __future__ import annotations

import asyncio

import pytest
from matrx_utils.source_guard import stable_source

from matrx_ai.ops import pricing_drift


@pytest.fixture(autouse=True)
def _clean_day_guard():
    pricing_drift._reset_day_guard_for_tests()
    yield
    pricing_drift._reset_day_guard_for_tests()


class _Recorder:
    """Stands in for the whole filing tail: dedupe read + capture_issue."""

    def __init__(self, monkeypatch, *, already_filed=False):
        self.captured: list[dict] = []
        self.already_filed = already_filed

        async def _already(model, offering_id):
            return self.already_filed

        async def _capture(key, **kwargs):
            self.captured.append({"key": key, **kwargs})

        monkeypatch.setattr(pricing_drift, "_already_filed_today", _already)
        import matrx_ai.ops.issue_capture as issue_capture

        monkeypatch.setattr(issue_capture, "capture_issue", _capture)

        # detached_task drops the caller's context by design; run it inline so
        # the assertion sees the filing in this test's loop.
        def _inline(coro, name=None):
            return asyncio.get_running_loop().create_task(coro)

        monkeypatch.setattr(pricing_drift, "detached_task", _inline)


async def _settle():
    for _ in range(6):
        await asyncio.sleep(0)


def test_the_call_site_still_exists_at_the_one_seam_that_holds_both_numbers():
    """The routing is wired where the variance is computed — not merely importable."""
    from matrx_ai.orchestrator import requests as requests_module

    source = stable_source(requests_module.CompletedRequest.to_storage_dict)
    assert "note_pricing_drift(" in source, (
        "to_storage_dict no longer routes pricing drift — the variance is being "
        "written to chat.request.metadata and read by nobody again."
    )
    assert "provider_catalog_variance_usd" in source


def test_tolerance_ignores_rounding_but_not_a_real_price_change():
    # 2% relative, $0.0005 absolute floor.
    assert pricing_drift.exceeds_tolerance(1.0, 1.01) is False  # 1% — noise
    assert pricing_drift.exceeds_tolerance(1.0, 1.05) is True  # 5% — drift
    assert pricing_drift.exceeds_tolerance(0.00001, 0.00020) is False  # under the floor
    assert pricing_drift.exceeds_tolerance(0.0, 0.01) is True  # priced at zero, billed


@pytest.mark.asyncio
async def test_past_tolerance_drift_files_one_issue_with_both_numbers_and_the_offering(monkeypatch):
    rec = _Recorder(monkeypatch)

    dispatched = pricing_drift.note_pricing_drift(
        catalog_cost_usd=0.10,
        provider_cost_usd=0.16,
        offering_id="5dcade2f-0b28-4235-9752-bc866cca9f13",
        model="gpt-4o",
        provider="openai",
    )
    assert dispatched is True
    await _settle()

    assert len(rec.captured) == 1
    event = rec.captured[0]
    assert event["key"] == pricing_drift.PRICING_DRIFT_ISSUE_KEY
    assert event["error_type"] == pricing_drift.PRICING_DRIFT_ERROR_TYPE
    assert event["model"] == "gpt-4o"
    assert event["provider"] == "openai"
    detail = event["detail"]
    assert detail["offering_id"] == "5dcade2f-0b28-4235-9752-bc866cca9f13"
    assert detail["catalog_cost_usd"] == 0.1
    assert detail["provider_cost_usd"] == 0.16
    assert detail["variance_usd"] == 0.06
    assert "pricing_verified_at" in detail["remedy"]


@pytest.mark.asyncio
async def test_within_tolerance_files_nothing(monkeypatch):
    rec = _Recorder(monkeypatch)
    assert (
        pricing_drift.note_pricing_drift(
            catalog_cost_usd=0.10, provider_cost_usd=0.1005, offering_id="o", model="gpt-4o"
        )
        is False
    )
    await _settle()
    assert rec.captured == []


@pytest.mark.asyncio
async def test_a_missing_provider_cost_is_not_drift(monkeypatch):
    rec = _Recorder(monkeypatch)
    assert (
        pricing_drift.note_pricing_drift(
            catalog_cost_usd=0.10, provider_cost_usd=None, offering_id="o", model="gpt-4o"
        )
        is False
    )
    await _settle()
    assert rec.captured == []


@pytest.mark.asyncio
async def test_one_event_per_model_per_day_however_many_calls_drift(monkeypatch):
    rec = _Recorder(monkeypatch)

    filed = [
        pricing_drift.note_pricing_drift(
            catalog_cost_usd=0.10, provider_cost_usd=0.20, offering_id="o1", model="gpt-4o"
        )
        for _ in range(25)
    ]
    await _settle()

    assert filed.count(True) == 1
    assert len(rec.captured) == 1


@pytest.mark.asyncio
async def test_a_second_model_files_its_own_event(monkeypatch):
    rec = _Recorder(monkeypatch)
    pricing_drift.note_pricing_drift(
        catalog_cost_usd=0.10, provider_cost_usd=0.20, offering_id="o1", model="gpt-4o"
    )
    pricing_drift.note_pricing_drift(
        catalog_cost_usd=0.10, provider_cost_usd=0.20, offering_id="o2", model="claude-sonnet-4-5"
    )
    await _settle()
    assert sorted(e["model"] for e in rec.captured) == ["claude-sonnet-4-5", "gpt-4o"]


@pytest.mark.asyncio
async def test_a_row_already_filed_today_by_another_process_is_not_duplicated(monkeypatch):
    rec = _Recorder(monkeypatch, already_filed=True)
    pricing_drift.note_pricing_drift(
        catalog_cost_usd=0.10, provider_cost_usd=0.20, offering_id="o1", model="gpt-4o"
    )
    await _settle()
    assert rec.captured == []


@pytest.mark.asyncio
async def test_a_failure_in_the_filing_tail_never_escapes_into_the_request_path(monkeypatch):
    _Recorder(monkeypatch)

    async def _boom(key, **kwargs):
        raise RuntimeError("issue surface is down")

    import matrx_ai.ops.issue_capture as issue_capture

    monkeypatch.setattr(issue_capture, "capture_issue", _boom)

    assert (
        pricing_drift.note_pricing_drift(
            catalog_cost_usd=0.10, provider_cost_usd=0.20, offering_id="o1", model="gpt-4o"
        )
        is True
    )
    await _settle()  # swallowed and screamed, not raised
