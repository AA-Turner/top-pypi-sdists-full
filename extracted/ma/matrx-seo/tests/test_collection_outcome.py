"""The silent-zero guard: a collection that lands nothing must be classified
as a problem, and the seam must never break a run.

Regression for the 2026-08-04 outage: GSC ingestion was dead for five days
while every layer reported success — a "completed" run persisting zero rows
was indistinguishable from a healthy one.
"""

from __future__ import annotations

import pytest

from matrx_seo.collection_outcome import (
    CollectionOutcomeEvent,
    classify_outcome,
    emit_collection_outcome,
    register_collection_outcome_sink,
    reset_collection_outcome_sinks,
)


def _event(**overrides) -> CollectionOutcomeEvent:
    base = {
        "provider": "gsc",
        "capability": "search_performance",
        "operation": "gsc.search_analytics",
        "run_id": "run-1",
        "site_id": "site-1",
        "status": "completed",
        "window_start": "2026-07-01",
        "window_end": "2026-07-07",
        "expected_days": 7,
        "observation_count": 100,
        "created": 100,
        "existing": 0,
        "distinct_dates": 7,
        "site_has_prior_data": True,
    }
    base.update(overrides)
    return CollectionOutcomeEvent(**base)


class TestClassify:
    def test_healthy_run_is_not_a_problem(self) -> None:
        assert classify_outcome(_event()) is None

    def test_zero_rows_is_the_headline_problem(self) -> None:
        """THE outage shape: status completed, nothing persisted."""
        event = _event(observation_count=0, created=0, existing=0, distinct_dates=0)
        assert classify_outcome(event) == "zero_rows"

    def test_a_rerun_that_creates_nothing_new_is_healthy(self) -> None:
        """created=0 with existing rows is a legitimate idempotent re-run."""
        assert classify_outcome(_event(created=0, existing=100)) is None

    def test_cache_reuse_never_alarms(self) -> None:
        event = _event(created=0, existing=0, observation_count=0, reused=True)
        assert classify_outcome(event) is None

    def test_raw_provider_metadata_command_never_alarms_on_zero_observations(self) -> None:
        """Raw evidence is persisted without normalized observation rows."""
        event = _event(
            provider="bing_webmaster",
            capability="raw_provider",
            operation="bing_webmaster.sites.list",
            observation_count=0,
            created=0,
            existing=0,
            distinct_dates=0,
            site_has_prior_data=True,
        )
        assert classify_outcome(event) is None

    def test_failed_status_wins_over_everything(self) -> None:
        event = _event(status="failed", created=0, existing=0, error={"type": "X"})
        assert classify_outcome(event) == "failed"

    def test_failed_raw_provider_command_still_alarms(self) -> None:
        event = _event(
            status="failed",
            capability="raw_provider",
            created=0,
            existing=0,
            error={"type": "ProviderFailure"},
        )
        assert classify_outcome(event) == "failed"

    def test_fewer_dates_than_days_is_NOT_an_alarm(self) -> None:
        """GSC returns no row for a zero-traffic day, and the freshest day
        inside the 2-day lag often hasn't landed. Alarming on this fired on
        healthy runs nightly — cry-wolf is how the next real outage gets
        ignored. Coverage gaps are measured over full history by
        `seo.gsc_ingestion_health` instead."""
        assert classify_outcome(_event(expected_days=7, distinct_dates=3)) is None

    def test_full_coverage_passes(self) -> None:
        assert classify_outcome(_event(expected_days=7, distinct_dates=7)) is None

    def test_empty_backfill_window_never_alarms(self) -> None:
        """A backfill window may predate the site entirely, and an empty
        window still counts as covered BY DESIGN so the frontier can't
        stall. Alarming here fires on every backfill window, forever."""
        event = _event(
            observation_count=0, created=0, existing=0, distinct_dates=0, is_backfill=True
        )
        assert classify_outcome(event) is None

    def test_parked_site_with_no_history_never_alarms(self) -> None:
        """A brand-new or zero-traffic property returns nothing every night
        and is not broken."""
        event = _event(
            observation_count=0,
            created=0,
            existing=0,
            distinct_dates=0,
            site_has_prior_data=False,
        )
        assert classify_outcome(event) is None

    def test_zero_rows_on_a_site_WITH_history_is_the_alarm(self) -> None:
        event = _event(
            observation_count=0,
            created=0,
            existing=0,
            distinct_dates=0,
            site_has_prior_data=True,
        )
        assert classify_outcome(event) == "zero_rows"


class TestEmit:
    def setup_method(self) -> None:
        reset_collection_outcome_sinks()

    def teardown_method(self) -> None:
        reset_collection_outcome_sinks()

    def test_sink_receives_the_classified_event(self) -> None:
        seen: list[CollectionOutcomeEvent] = []
        register_collection_outcome_sink(seen.append)
        emit_collection_outcome(_event(created=0, existing=0, distinct_dates=0))
        assert len(seen) == 1
        assert seen[0].problem == "zero_rows"
        assert seen[0].is_alarming is True

    def test_healthy_runs_still_reach_the_sink_unflagged(self) -> None:
        seen: list[CollectionOutcomeEvent] = []
        register_collection_outcome_sink(seen.append)
        emit_collection_outcome(_event())
        assert len(seen) == 1
        assert seen[0].problem is None

    def test_a_raising_sink_never_breaks_the_run(self) -> None:
        """Observability must never take down ingestion."""

        def boom(_event: CollectionOutcomeEvent) -> None:
            raise RuntimeError("sink exploded")

        good: list[CollectionOutcomeEvent] = []
        register_collection_outcome_sink(boom)
        register_collection_outcome_sink(good.append)
        emit_collection_outcome(_event())  # must not raise
        assert len(good) == 1

    def test_registration_is_idempotent(self) -> None:
        seen: list[CollectionOutcomeEvent] = []
        register_collection_outcome_sink(seen.append)
        register_collection_outcome_sink(seen.append)
        emit_collection_outcome(_event())
        assert len(seen) == 1


@pytest.mark.parametrize(
    ("expected_days", "distinct_dates", "problem"),
    [
        (30, 30, None),
        (30, 29, None),  # zero-traffic days are normal, not a defect
        (30, 0, "zero_rows"),
    ],
)
def test_coverage_matrix(expected_days: int, distinct_dates: int, problem: str | None) -> None:
    created = 0 if distinct_dates == 0 else 10
    event = _event(
        expected_days=expected_days,
        distinct_dates=distinct_dates,
        created=created,
        existing=0,
        observation_count=created,
        site_has_prior_data=True,
    )
    assert classify_outcome(event) == problem


class TestCustomerReconnectIsNotAPlatformFailure:
    """`seo_collection_failed:gsc:search_performance` (2026-09-26): 16 of the
    19 failures it counted in 30 days were two organizations' Google
    connections (a property no longer discovered under the connection, a
    disconnected account) — states only that organization can repair, which
    the site's ingestion banner already names. They are classified apart from
    platform failures so the platform alarm means OUR defect again."""

    @pytest.mark.parametrize(
        "error",
        [
            {
                "type": "ResourceBindingError",
                "message": "connection d33d… has no live discovered search_console_property "
                "resource 'sc-domain:example.com' — … or the connection needs re-authentication",
            },
            {
                "type": "LookupError",
                "message": "Google connection 608f… does not exist or was disconnected, and no "
                "other live connection for the same Google account is available — reconnect",
            },
            {
                "type": "GscPartialCollectionError",
                "message": "12 GSC profile page(s) failed",
                "failures": [{"message": "GSC token refresh failed: HTTP 400 invalid_grant"}],
            },
        ],
    )
    def test_access_failures_need_the_organization(self, error: dict) -> None:
        event = _event(status="failed", error=error)
        assert classify_outcome(event) == "needs_reconnect"
        event.problem = classify_outcome(event)
        assert event.needs_customer_action
        assert not event.is_alarming

    @pytest.mark.parametrize(
        "error",
        [
            {"type": "QueryTimeoutError", "message": "Query timed out during execute_query"},
            # OUR OAuth client configuration — a platform defect, never the customer's.
            {
                "type": "CanonicalGoogleOAuthError",
                "message": "GSC token refresh failed: invalid_client",
            },
            {"type": "ValueError", "message": "GSC could not resolve 1 page URL(s)"},
        ],
    )
    def test_platform_failures_still_alarm(self, error: dict) -> None:
        event = _event(status="failed", error=error)
        assert classify_outcome(event) == "failed"
        event.problem = "failed"
        assert event.is_alarming
