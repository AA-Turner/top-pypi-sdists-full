"""The cross-family translation helpers — the code that unifies spellings.

These are the functions that decide whether a downstream consumer can count on
a field. Each assertion here is a claim about REAL provider text we measured
(Brave's ``<strong>`` wrapping and ``&#x27;`` escaping, Google News' relative
dates, the scraper's 19-digit simhash), not a synthetic round-trip.
"""

from __future__ import annotations

from datetime import UTC, datetime

from matrx_graph.content_ir.translate import (
    big_int_to_string,
    displayed_url_from,
    is_relative_age,
    parse_duration_seconds,
    parse_published_at,
    plain_text,
    site_name_from_url,
    strip_html,
)

NOW = datetime(2026, 8, 24, 12, 0, tzinfo=UTC)


# --- dates -----------------------------------------------------------------


def test_iso_text_survives_unchanged() -> None:
    assert parse_published_at("2025-12-16T08:00:00") == "2025-12-16T08:00:00"
    assert parse_published_at("2025-12-16") == "2025-12-16"


def test_an_absolute_us_date_becomes_iso() -> None:
    assert parse_published_at("Mar 5, 2024") == "2024-03-05"
    assert parse_published_at("September 5, 2024") == "2024-09-05"


def test_a_relative_age_is_an_approximation_anchored_to_now() -> None:
    """Google News dates are RELATIVE — the approximation is declared, not hidden."""
    assert parse_published_at("3 hours ago", now=NOW) == "2026-08-24"
    assert parse_published_at("2 weeks ago", now=NOW) == "2026-08-10"
    assert parse_published_at("1 year ago", now=NOW) == "2025-08-24"


def test_text_with_no_honest_date_yields_none() -> None:
    """Never synthesize precision the source did not give."""
    for junk in ("last Tuesday-ish", "", None, "sometime", 5):
        assert parse_published_at(junk) is None  # type: ignore[arg-type]


def test_is_relative_age_marks_exactly_what_the_parser_approximated() -> None:
    assert is_relative_age("3 hours ago")
    assert is_relative_age("  10 Minutes Ago ")
    assert not is_relative_age("Mar 5, 2024")
    assert not is_relative_age(None)


# --- HTML ------------------------------------------------------------------


def test_strip_html_returns_text_and_the_links_it_removed() -> None:
    text, links = strip_html("<a href='https://x.com/a'>Public</a> company")
    assert text == "Public company"
    assert links == ["https://x.com/a"]


def test_plain_text_decodes_the_entities_a_reader_actually_saw() -> None:
    """A literal ``I&#x27;m`` reached a reader on /search before this existed."""
    assert plain_text("<strong>I&#x27;m</strong> here") == "I'm here"


def test_plain_text_drops_straight_into_an_optional_field() -> None:
    assert plain_text(None) is None
    assert plain_text("") is None
    assert plain_text("<b></b>") is None
    assert plain_text(42) is None  # type: ignore[arg-type]


# --- durations -------------------------------------------------------------


def test_duration_text_becomes_seconds() -> None:
    assert parse_duration_seconds("12:38") == 758
    assert parse_duration_seconds("1:02:03") == 3723
    assert parse_duration_seconds("45") == 45


def test_unparseable_duration_yields_none_rather_than_a_guess() -> None:
    for junk in ("about 3 min", "1:2:3:4", "", None, ":", "12:ab"):
        assert parse_duration_seconds(junk) is None  # type: ignore[arg-type]


# --- URLs ------------------------------------------------------------------


def test_site_name_strips_the_www_prefix() -> None:
    assert site_name_from_url("https://www.example.com/a/b") == "example.com"
    assert site_name_from_url("https://news.example.co.uk/x") == "news.example.co.uk"


def test_site_name_is_case_insensitive_like_a_hostname() -> None:
    assert site_name_from_url("https://WWW.Example.COM/a") == "example.com"


def test_site_name_reports_none_rather_than_inventing_one() -> None:
    """The reconciled signature (2026-08-24): ``str | None -> str | None``.

    Returning the unparsed input as a "site name" is the quiet dishonesty the
    translation law exists to stop. A caller whose kind field is a required
    ``str`` supplies its own fallback in the open.
    """
    assert site_name_from_url(None) is None
    assert site_name_from_url("") is None
    assert site_name_from_url("not a url at all") is None


def test_displayed_url_is_the_breadcrumb_a_serp_shows() -> None:
    assert displayed_url_from("https://www.example.com/docs/api") == "example.com › docs › api"
    assert displayed_url_from("https://example.com") == "example.com"


# --- big integers ----------------------------------------------------------


def test_a_64_bit_hash_becomes_a_string_javascript_cannot_round() -> None:
    """Measured simhash ``7046352583261510909`` is past Number.MAX_SAFE_INTEGER.

    Sent as a JSON number every JS consumer silently rounds it and distinct
    pages start comparing equal — the exact bug this function prevents.
    """
    simhash = 7046352583261510909
    assert simhash > 2**53 - 1
    assert big_int_to_string(simhash) == "7046352583261510909"
    assert int(big_int_to_string(simhash)) == simhash


def test_an_absent_hash_is_none_not_the_string_none() -> None:
    assert big_int_to_string(None) is None
    assert big_int_to_string("") is None
    assert big_int_to_string(0) == "0"
