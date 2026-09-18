"""The capture ladder's two laws, as tests that can actually fail.

Law 1 — NEVER SKIP A RUNG. A capture goes http → browser → own_browser →
human_drive, one step at a time, or it stops with a reason.

Law 2 — NEVER STOP SILENTLY. An unusable result always names either the rung
that comes next or why nothing does.

Both are proven against the real `orchestrator.scrape()` sealing path, not
against a toy, because the defect these exist to catch is precisely a result
that leaves the orchestrator without them.
"""

from __future__ import annotations

import pytest

from matrx_scraper.ladder import (
    RUNGS,
    LadderOrderError,
    LadderPolicy,
    LadderTrail,
    LadderVerdict,
    assert_no_skipped_rung,
    classify_login_wall,
    decide,
    next_rung,
    trail_entry,
)
from matrx_scraper.orchestrator import ScrapeResult, _seal_ladder
from matrx_scraper.scraper import RequestType


def _failed(reason: str = "bad_status", **kwargs) -> ScrapeResult:
    return ScrapeResult(
        url=kwargs.pop("url", "https://example.com/a"),
        response_url=kwargs.pop("response_url", "https://example.com/a"),
        success=False,
        content_type="html",
        failure_reason=reason,
        **kwargs,
    )


# ── Law 1: never skip a rung ────────────────────────────────────────────────


def test_the_ladder_is_the_four_rungs_in_order():
    assert RUNGS == ("http", "browser", "own_browser", "human_drive")
    assert next_rung("http") == "browser"
    assert next_rung("browser") == "own_browser"
    assert next_rung("own_browser") == "human_drive"
    assert next_rung("human_drive") is None


def test_a_trail_that_jumps_a_rung_is_refused():
    jumped = [
        trail_entry(rung="http", ok=False, reason="bad_status"),
        trail_entry(rung="own_browser", ok=False, reason="bad_status"),
    ]
    with pytest.raises(LadderOrderError) as caught:
        assert_no_skipped_rung(jumped)
    # The message must name both rungs — a guard nobody can act on is a log line.
    assert "'http' → 'own_browser'" in str(caught.value)
    assert "'browser'" in str(caught.value)


def test_a_trail_that_does_not_start_at_the_scraper_is_refused():
    with pytest.raises(LadderOrderError):
        assert_no_skipped_rung([trail_entry(rung="browser", ok=False)])


def test_the_trail_refuses_the_skip_at_the_moment_it_happens():
    trail = LadderTrail()
    trail.record("http", ok=False, reason="bad_status")
    with pytest.raises(LadderOrderError):
        trail.record("own_browser", ok=False, reason="bad_status")
    # And the illegal entry is not left behind on a half-written trail.
    assert [entry["rung"] for entry in trail.entries] == ["http"]


def test_asking_for_the_server_browser_directly_still_records_rung_one():
    """A caller may skip rung 1 — but it is SAID, never silently absent."""
    result = _failed("cloudflare_block")
    _seal_ladder(
        result,
        request_type=RequestType.BROWSER,
        http_ok=False,
        http_reason=None,
        http_chars=0,
        policy=LadderPolicy(),
    )
    assert [entry["rung"] for entry in result.rung_trail] == ["http", "browser"]
    assert result.rung_trail[0]["ok"] is False
    assert "asked for our server browser directly" in result.rung_trail[0]["note"]


# ── Law 2: never stop silently ──────────────────────────────────────────────


def test_a_verdict_cannot_be_silent():
    with pytest.raises(LadderOrderError):
        LadderVerdict()  # neither a next rung nor a reason for stopping
    with pytest.raises(LadderOrderError):
        LadderVerdict(next_rung="own_browser", stopped_because="exhausted")


def test_a_login_wall_after_the_server_browser_reaches_for_the_persons_own_browser():
    result = _failed(
        "bad_status",
        url="https://www.instagram.com/nasa/",
        response_url="https://www.instagram.com/accounts/login/",
    )
    result.browser_attempted = True
    _seal_ladder(
        result,
        request_type=RequestType.NORMAL,
        http_ok=False,
        http_reason="bad_status",
        http_chars=0,
        policy=LadderPolicy(),
    )
    assert result.next_rung == "own_browser"
    assert result.next_rung_reason == "login_wall"
    assert result.stopped_because is None
    assert "already signed in" in result.next_rung_note


def test_turning_the_own_browser_rung_off_is_announced_not_silent():
    result = _failed("cloudflare_block")
    result.browser_attempted = True
    _seal_ladder(
        result,
        request_type=RequestType.NORMAL,
        http_ok=False,
        http_reason="cloudflare_block",
        http_chars=0,
        policy=LadderPolicy(own_browser_enabled=False),
    )
    assert result.next_rung is None
    assert result.stopped_because == "rung_disabled"
    assert "turned off for your organization" in result.next_rung_note


def test_a_real_404_never_asks_a_person_for_their_browser():
    result = _failed("not_found")
    result.browser_attempted = True
    _seal_ladder(
        result,
        request_type=RequestType.NORMAL,
        http_ok=False,
        http_reason="not_found",
        http_chars=0,
        policy=LadderPolicy(),
    )
    assert result.next_rung is None
    assert result.stopped_because == "not_escalatable"


def test_every_unusable_result_names_a_next_rung_or_a_reason_for_stopping():
    """The silent-failure sweep: no failure class may leave both fields empty."""
    classes = [
        "bad_status",
        "cloudflare_block",
        "empty_content",
        "thin_content",
        "low_text_content",
        "wrong_resource",
        "request_error",
        "proxy_error",
        "not_found",
        "domain_blocked",
        "pdf_extraction_failed",
        None,
    ]
    for failure in classes:
        for own_browser in (True, False):
            result = _failed(failure) if failure else _failed()
            if not failure:
                result.failure_reason = None
            result.browser_attempted = True
            _seal_ladder(
                result,
                request_type=RequestType.NORMAL,
                http_ok=False,
                http_reason=failure,
                http_chars=0,
                policy=LadderPolicy(own_browser_enabled=own_browser),
            )
            assert bool(result.next_rung) != bool(result.stopped_because), (
                f"{failure!r} (own_browser={own_browser}) left the ladder silent: "
                f"next_rung={result.next_rung!r} stopped_because={result.stopped_because!r}"
            )
            assert result.next_rung_note, f"{failure!r} produced no sentence for a person"


def test_a_usable_result_asks_nobody_for_anything():
    ok = ScrapeResult(
        url="https://example.com/a",
        response_url="https://example.com/a",
        success=True,
        content_type="html",
    )
    ok.content_chars = 4000
    _seal_ladder(
        ok,
        request_type=RequestType.NORMAL,
        http_ok=True,
        http_reason=None,
        http_chars=4000,
        policy=LadderPolicy(),
    )
    assert ok.next_rung is None
    assert ok.stopped_because is None
    assert [entry["rung"] for entry in ok.rung_trail] == ["http"]
    assert ok.rung_trail[0]["ok"] is True


# ── The login-wall classifier: evidence only, never a guess ─────────────────


@pytest.mark.parametrize(
    "status,response,requested,expected",
    [
        (403, "https://a.com/x", "https://a.com/x", True),
        (401, "https://a.com/x", "https://a.com/x", True),
        (200, "https://a.com/accounts/login/", "https://a.com/nasa/", True),
        (200, "https://a.com/authwall", "https://a.com/in/someone", True),
        # Asking FOR a login page is not a login wall.
        (200, "https://a.com/login", "https://a.com/login", False),
        (404, "https://a.com/x", "https://a.com/x", False),
        (200, "https://a.com/x", "https://a.com/x", False),
    ],
)
def test_login_wall_is_classified_from_evidence(status, response, requested, expected):
    assert (
        classify_login_wall(
            status_code=status, response_url=response, requested_url=requested
        )
        is expected
    )


def test_the_last_rung_says_the_ladder_is_exhausted():
    trail = LadderTrail()
    trail.record("http", ok=False, reason="login_wall")
    trail.record("browser", ok=False, reason="login_wall")
    trail.record("own_browser", ok=False, reason="login_wall")
    trail.record("human_drive", ok=False, reason="login_wall")
    verdict = decide(trail.entries, reason="login_wall")
    assert verdict.next_rung is None
    assert verdict.stopped_because == "exhausted"
    assert "including opening the page yourself" in verdict.note


def test_a_rung_nobody_will_run_is_never_the_next_rung():
    """The LinkedIn class, 2026-09-17, found by running the real internet.

    `linkedin.com/feed/` answers a stranger with its sign-in page, which the
    content-sanity gate calls `wrong_resource` — a class the browser leg
    deliberately does not take. The trail therefore held only `http`, and the
    verdict pointed at `browser`: a rung on a scrape that had already finished,
    which nothing would ever run. A dead end is a silent failure wearing a
    next step, so the declined rung is now RECORDED as declined.
    """
    result = _failed(
        "bad_status",
        url="https://www.linkedin.com/feed/",
        response_url="https://www.linkedin.com/authwall",
    )
    result.success = True
    result.content_chars = 1516
    result.content_warning = "wrong_resource"
    result.browser_attempted = False  # escalation declined this class
    _seal_ladder(
        result,
        request_type=RequestType.NORMAL,
        http_ok=False,
        http_reason="wrong_resource",
        http_chars=1516,
        policy=LadderPolicy(),
    )
    assert [entry["rung"] for entry in result.rung_trail] == ["http", "browser"]
    assert result.rung_trail[1]["ok"] is False
    assert result.rung_trail[1]["note"]
    assert result.next_rung == "own_browser", (
        "the next rung must be one somebody will actually run; 'browser' on a "
        "finished scrape is a dead end"
    )
