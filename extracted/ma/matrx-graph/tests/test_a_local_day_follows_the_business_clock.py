"""``datetime.local_day`` answers by the business's clock, DST-correct, and never guesses UTC."""

from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace

import pytest
from matrx_graph.actions import ActionFailed
from matrx_graph.nodes.datetime_ import configure_organization_time_zone, datetime_local_day
from matrx_graph.nodes.datetime_.local_day import NO_TIME_ZONE_MESSAGE, LocalDayInput

APP = SimpleNamespace(organization_id="org-1")


@pytest.fixture(autouse=True)
def _reset():
    yield
    configure_organization_time_zone(None)


def _org_zone(name):
    async def resolver(org):
        assert org == "org-1"
        return name

    configure_organization_time_zone(resolver)


async def _day(offset, at, zone=None, app=APP):
    return await datetime_local_day(app, LocalDayInput(offset_days=offset, at=at, time_zone=zone))


async def test_ten_pm_mountain_saturday_tomorrow_is_sunday():
    _org_zone("America/Denver")
    out = await _day(1, "2026-11-15T05:24:00+00:00")  # 22:24 MST Sat Nov 14
    assert out.date == "2026-11-15"
    assert out.start == "2026-11-15T00:00:00-07:00"
    assert out.end == "2026-11-16T00:00:00-07:00"
    assert out.time_zone == "America/Denver"


async def test_one_am_mountain_sunday_tomorrow_is_monday():
    _org_zone("America/Denver")
    assert (await _day(1, "2026-11-15T08:00:00+00:00")).date == "2026-11-16"


async def test_spring_forward_day_is_23_hours():
    out = await _day(0, "2026-03-08T12:00:00+00:00", "America/Denver")
    assert out.start == "2026-03-08T00:00:00-07:00"
    assert out.end == "2026-03-09T00:00:00-06:00"
    assert (datetime.fromisoformat(out.end) - datetime.fromisoformat(out.start)).total_seconds() == 23 * 3600


async def test_fall_back_day_is_25_hours():
    out = await _day(0, "2026-11-01T12:00:00+00:00", "America/Denver")
    assert out.start == "2026-11-01T00:00:00-06:00"
    assert out.end == "2026-11-02T00:00:00-07:00"
    assert (datetime.fromisoformat(out.end) - datetime.fromisoformat(out.start)).total_seconds() == 25 * 3600


async def test_no_org_zone_refuses_in_plain_words():
    _org_zone(None)
    with pytest.raises(ActionFailed) as e:
        await _day(1, "2026-11-15T05:24:00+00:00")
    assert e.value.code == "no_time_zone"
    assert NO_TIME_ZONE_MESSAGE == "Set your business's time zone in your organization's Settings (Configuration) to use local days."
    assert NO_TIME_ZONE_MESSAGE in str(e.value)


async def test_no_resolver_installed_also_refuses():
    with pytest.raises(ActionFailed):
        await _day(0, "2026-11-15T05:24:00+00:00")


async def test_explicit_zone_wins_over_org_zone():
    _org_zone("America/Denver")
    out = await _day(0, "2026-11-15T05:24:00+00:00", "Europe/London")
    assert out.time_zone == "Europe/London" and out.date == "2026-11-15"


async def test_unknown_zone_is_said_plainly():
    with pytest.raises(ActionFailed) as e:
        await _day(0, "2026-11-15T05:24:00+00:00", "Mars/Olympus")
    assert e.value.code == "invalid_time_zone"


async def test_now_default_runs():
    out = await _day(0, None, "UTC")
    assert out.date == datetime.now(UTC).date().isoformat()


async def test_registered_as_a_step_and_action():
    from matrx_graph.executor.registry import default_registry

    assert default_registry().get("datetime.local_day") is not None


async def test_add_and_format_take_a_zone_and_default_stays_utc():
    from matrx_graph.nodes.datetime_.ops import (
        AddConfig, AddInput, DatetimeAddExecutor, DatetimeFormatExecutor, FormatConfig, FormatInput,
    )

    ctx = SimpleNamespace()
    f = await DatetimeFormatExecutor().execute(
        ctx, FormatInput(iso="2026-11-15T05:24:00+00:00"), FormatConfig(format="%Y-%m-%d", time_zone="America/Denver")
    )
    assert f.result.text == "2026-11-14"
    f0 = await DatetimeFormatExecutor().execute(
        ctx, FormatInput(iso="2026-11-15T05:24:00+00:00"), FormatConfig(format="%Y-%m-%d")
    )
    assert f0.result.text == "2026-11-15"
    a = await DatetimeAddExecutor().execute(
        ctx, AddInput(iso="2026-03-07T12:00:00-07:00"), AddConfig(days=1, time_zone="America/Denver")
    )
    assert a.result.iso == "2026-03-08T12:00:00-06:00"
