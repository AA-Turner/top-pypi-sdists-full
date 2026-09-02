"""The robots.txt parser — the primitive `robots_txt_health` is scored from.

Two properties matter and are pinned here:

1. **It never raises.** A robots.txt so broken it crashes the parser is exactly
   the file the check exists to report; a crash would turn "your robots.txt is
   malformed" into "the check failed".
2. **It fails OPEN.** robots.txt is a deny list — anything it does not address
   is crawlable. A parser that invents a block would make the platform report a
   site-wide catastrophe that isn't happening.
"""

from __future__ import annotations

import pytest

from matrx_scraper.robots_txt import ROBOTS_MAX_BYTES, parse_robots_txt


def test_empty_file_blocks_nothing():
    doc = parse_robots_txt("")
    assert doc.groups == []
    assert doc.is_allowed("/anything")
    assert doc.blanket_disallow_agents() == []


def test_disallow_and_allow_longest_match_wins():
    doc = parse_robots_txt("User-agent: *\nDisallow: /admin/\nAllow: /admin/public/\n")
    assert not doc.is_allowed("/admin/secret")
    # The longer Allow pattern beats the shorter Disallow — Google's rule.
    assert doc.is_allowed("/admin/public/page")
    assert doc.is_allowed("/")


def test_decision_names_the_winning_directive_and_line():
    doc = parse_robots_txt("User-agent: *\nDisallow: /admin/\nAllow: /admin/public/\n")

    blocked = doc.decision_for("/admin/secret")
    assert blocked.allowed is False
    assert blocked.matched_rule is not None
    assert blocked.matched_rule.directive == "Disallow: /admin/"
    assert blocked.matched_rule.line_number == 2

    allowed = doc.decision_for("/admin/public/page")
    assert allowed.allowed is True
    assert allowed.matched_rule is not None
    assert allowed.matched_rule.directive == "Allow: /admin/public/"
    assert allowed.matched_rule.line_number == 3

    default_allowed = doc.decision_for("/unmatched")
    assert default_allowed.allowed is True
    assert default_allowed.matched_rule is None


def test_empty_disallow_value_means_allow_everything():
    doc = parse_robots_txt("User-agent: *\nDisallow:\n")
    assert doc.is_allowed("/anything")
    assert doc.blanket_disallow_agents() == []


def test_wildcard_and_end_anchor():
    doc = parse_robots_txt("User-agent: *\nDisallow: /*.pdf$\nDisallow: /tmp/*/logs\n")
    assert not doc.is_allowed("/files/report.pdf")
    assert doc.is_allowed("/files/report.pdf?v=2")  # `$` anchors the end
    assert not doc.is_allowed("/tmp/a/logs")
    assert doc.is_allowed("/tmp/a/data")


def test_full_urls_and_paths_match_the_same_way():
    doc = parse_robots_txt("User-agent: *\nDisallow: /private\n")
    assert not doc.is_allowed("https://example.com/private/x")
    assert not doc.is_allowed("/private/x")
    # Percent-encoding is not significant.
    assert not doc.is_allowed("https://example.com/private%20area")


def test_blanket_disallow_names_the_major_agents_only():
    doc = parse_robots_txt("User-agent: *\nDisallow: /\n\nUser-agent: AhrefsBot\nDisallow: /\n")
    blocked = doc.blanket_disallow_agents()
    assert blocked == ["*"], "blocking one scraper is a choice; blocking Google is the defect"
    assert not doc.is_allowed("/")


def test_disallow_root_with_an_allow_carve_out_is_not_a_blanket_block():
    doc = parse_robots_txt("User-agent: Googlebot\nDisallow: /\nAllow: /public/\n")
    assert doc.blanket_disallow_agents() == []
    assert doc.is_allowed("/public/x", "Googlebot")
    assert not doc.is_allowed("/other", "Googlebot")


def test_agent_specific_group_beats_the_wildcard_group():
    doc = parse_robots_txt(
        "User-agent: *\nDisallow: /\n\nUser-agent: Googlebot\nDisallow: /private\n"
    )
    assert doc.is_allowed("/anything", "Googlebot-News")
    assert not doc.is_allowed("/private/x", "Googlebot")
    assert not doc.is_allowed("/anything", "SomeOtherBot")


def test_consecutive_user_agents_share_one_rule_set():
    doc = parse_robots_txt("User-agent: a\nUser-agent: b\nDisallow: /x\n")
    assert len(doc.groups) == 1
    assert not doc.is_allowed("/x", "a")
    assert not doc.is_allowed("/x", "b")


def test_sitemap_directives_are_collected_anywhere_in_the_file():
    doc = parse_robots_txt(
        "Sitemap: https://e.com/a.xml\nUser-agent: *\nDisallow:\nSitemap: https://e.com/b.xml\n"
    )
    assert doc.sitemaps == ["https://e.com/a.xml", "https://e.com/b.xml"]
    assert doc.syntax_errors == []


@pytest.mark.parametrize(
    ("text", "fragment"),
    [
        ("User-agent: *\nDisallow /admin\n", "not a `field: value`"),
        ("Disallow: /admin\n", "before any `User-agent:`"),
        ("User-agent:\nDisallow: /\n", "has no value"),
        ("User-agent: *\nDissalow: /admin\n", "not a robots.txt directive"),
    ],
)
def test_malformed_lines_are_reported_with_their_line_number(text, fragment):
    doc = parse_robots_txt(text)
    assert doc.syntax_errors, f"expected a syntax error for {text!r}"
    assert fragment in doc.syntax_errors[0]
    assert doc.syntax_errors[0].startswith("line ")


def test_widely_used_non_standard_directives_are_not_syntax_errors():
    """Flagging `Crawl-delay:`/`Host:` would fail half the web for nothing."""
    doc = parse_robots_txt("User-agent: *\nCrawl-delay: 10\nHost: example.com\nDisallow: /x\n")
    assert doc.syntax_errors == []
    assert not doc.is_allowed("/x")


def test_comments_are_stripped_not_parsed():
    doc = parse_robots_txt("# a comment\nUser-agent: *  # trailing\nDisallow: /x # why\n")
    assert doc.syntax_errors == []
    assert doc.user_agents == ["*"]
    assert not doc.is_allowed("/x")


def test_oversized_file_is_truncated_and_says_so():
    text = "User-agent: *\nDisallow: /x\n" + ("# pad\n" * (ROBOTS_MAX_BYTES // 6 + 10))
    doc = parse_robots_txt(text)
    assert doc.truncated
    assert not doc.is_allowed("/x")


def test_a_hostile_file_never_raises():
    doc = parse_robots_txt("\x00\n:::\nUser-agent\nAllow\n" + "*" * 5_000)
    assert isinstance(doc.syntax_errors, list)
    assert doc.is_allowed("/anything")
