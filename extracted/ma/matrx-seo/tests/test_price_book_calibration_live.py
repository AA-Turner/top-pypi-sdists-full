"""Live calibration: the DataForSEO price book against what the provider billed.

For every DataForSEO operation with reported cost (``seo.provider_call`` joined to
its ``seo.collection_run``), the median per-run estimate from
``pricing.estimate(run.operation, run.settings)`` must sit within ``seo`` knob
``spend.price_book_tolerance`` of the median per-run reported cost. An operation
that ran but has no price fails too — the book must price everything the
platform actually buys.

THE WINDOW is per operation: its runs of the last 30 days, or its most recent
``_MIN_RUNS`` runs when the 30 days hold fewer. A bare 30-day window let an
operation that simply had not run lately calibrate against nothing — which is how
backlinks.core sat 2.4x over every run it ever made while this test was green.

Read-only. Runs only when the platform database credentials exist
(``SUPABASE_MATRIX_*``). ``matrx_orm``'s live-DB guard repoints those to an
unreachable placeholder unless the run passes ``--live-db --live-db-reason``;
an unreachable host SKIPS as ``UNMEASURED`` — never a pass, never a failure.
"""

from __future__ import annotations

import json
import os
import statistics
from decimal import Decimal

import pytest

from matrx_seo.providers.dataforseo.pricing import UnpricedOperationError, estimate

_ENV_KEYS = (
    "SUPABASE_MATRIX_HOST",
    "SUPABASE_MATRIX_PORT",
    "SUPABASE_MATRIX_DATABASE_NAME",
    "SUPABASE_MATRIX_USER",
    "SUPABASE_MATRIX_PASSWORD",
)

#: Used only while the ``seo`` / ``spend.price_book_tolerance`` knob row does not
#: exist yet; the test reads that row (the same ``platform.feature_knob`` row
#: ``matrx_seo.knobs`` serves) whenever it is present.
_DEFAULT_TOLERANCE = Decimal("0.25")

#: An operation with fewer runs than this in the last 30 days is calibrated
#: against its most recent ``_MIN_RUNS`` runs instead.
_MIN_RUNS = 20

RUNS_SQL = f"""
with runs as (
  select r.id::text as run_id, r.operation, r.settings,
         sum(pc.reported_cost) as reported, max(pc.fetched_at) as fetched_at
  from seo.provider_call pc
  join seo.collection_run r on r.id = pc.run_id
  where r.provider = 'dataforseo' and pc.reported_cost is not null
  group by r.id, r.operation, r.settings
), ranked as (
  select *, row_number() over (partition by operation order by fetched_at desc) as rn
  from runs
)
select run_id, operation, settings, reported from ranked
where fetched_at > now() - interval '30 days' or rn <= {_MIN_RUNS}
"""


def calibration_failures(rows, tolerance: Decimal) -> list[str]:
    """Every operation whose book median drifts past ``tolerance`` from its billed
    median, plus every operation the book cannot price. Pure: rows in, sentences out."""
    estimates: dict[str, list[Decimal]] = {}
    reported: dict[str, list[Decimal]] = {}
    unpriced: set[str] = set()
    for row in rows:
        settings = row["settings"]
        if isinstance(settings, str):
            settings = json.loads(settings)
        try:
            estimated = estimate(row["operation"], settings)
        except UnpricedOperationError:
            unpriced.add(row["operation"])
            continue
        estimates.setdefault(row["operation"], []).append(estimated)
        reported.setdefault(row["operation"], []).append(Decimal(str(row["reported"])))

    failures = [f"{operation}: no price in the book" for operation in sorted(unpriced)]
    for operation in sorted(estimates):
        book = statistics.median(estimates[operation])
        billed = statistics.median(reported[operation])
        if billed == 0:
            if book != 0:
                failures.append(f"{operation}: book {book} but the provider billed 0")
            continue
        drift = abs(book - billed) / billed
        if drift > tolerance:
            failures.append(
                f"{operation}: book median {book} vs billed median {billed} "
                f"({drift:.0%} > {tolerance:.0%}; {len(reported[operation])} runs)"
            )
    return failures

_KNOB_SQL = """
select value from platform.feature_knob
where feature = 'seo' and key = 'spend.price_book_tolerance'
"""


def _db_env() -> dict[str, str] | None:
    values = {key: os.environ.get(key, "") for key in _ENV_KEYS}
    return values if all(values.values()) else None


@pytest.mark.live
@pytest.mark.asyncio
async def test_price_book_matches_last_30_days_of_reported_cost() -> None:
    env = _db_env()
    if env is None:
        pytest.skip("platform database credentials (SUPABASE_MATRIX_*) are not configured")
    import asyncpg

    try:
        connection = await asyncpg.connect(
            host=env["SUPABASE_MATRIX_HOST"],
            port=int(env["SUPABASE_MATRIX_PORT"]),
            database=env["SUPABASE_MATRIX_DATABASE_NAME"],
            user=env["SUPABASE_MATRIX_USER"],
            password=env["SUPABASE_MATRIX_PASSWORD"],
            statement_cache_size=0,  # pgbouncer: prepared statements break the 2nd query
            timeout=30,
        )
    except (TimeoutError, OSError) as exc:
        pytest.skip(f"UNMEASURED: live database unreachable ({type(exc).__name__}: {exc})")
    try:
        knob = await connection.fetchval(_KNOB_SQL)
        rows = await connection.fetch(RUNS_SQL)
    finally:
        await connection.close()

    if knob is not None:
        tolerance = Decimal(str(json.loads(knob) if isinstance(knob, str) else knob))
    else:
        tolerance = _DEFAULT_TOLERANCE
    assert rows, "no DataForSEO reported cost in the last 30 days — nothing to calibrate against"

    failures = calibration_failures(rows, tolerance)
    assert not failures, "price book is off the reported cost:\n" + "\n".join(failures)
