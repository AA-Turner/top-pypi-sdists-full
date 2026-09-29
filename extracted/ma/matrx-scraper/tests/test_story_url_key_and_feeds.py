"""``story_url_key`` (the one tracking-stripped article key) and ``feeds.parse_feed`` (pure RSS/Atom)."""

from __future__ import annotations

from datetime import UTC, datetime
import traceback

import pytest

from matrx_scraper.canonical import story_url_key
from matrx_scraper.feeds import FeedParseError, normalize_feed_date, parse_feed

URLS = [
    "https://www.Reuters.com/legal/ftc-broker/?utm_source=x&b=2&a=1#top",
    "http://reuters.com/legal/ftc-broker?fbclid=abc&a=1&b=2",
    "techcrunch.com/2026/05/25/story/",
    "https://example.com",
    "https://example.com/path?ref_=nav&gclid=1&mc_cid=2&mc_eid=3&igshid=4&keep=yes",
]


def test_story_url_key_strips_tracking_host_case_www_fragment_and_slash() -> None:
    assert (
        story_url_key(URLS[0])
        == story_url_key(URLS[1])
        == "https://reuters.com/legal/ftc-broker?a=1&b=2"
    )
    assert story_url_key(URLS[2]) == "https://techcrunch.com/2026/05/25/story"
    assert story_url_key(URLS[3]) == "https://example.com/"
    assert story_url_key(URLS[4]) == "https://example.com/path?keep=yes"
    for blank in ("", "   ", "https:///nohost"):
        with pytest.raises(ValueError):
            story_url_key(blank)


def test_coverage_has_no_second_article_key() -> None:
    # Lane F retired matrx_seo.coverage.normalize_url: a coverage mention is keyed on this story key.
    coverage = pytest.importorskip("matrx_seo.coverage")
    assert not hasattr(coverage, "normalize_url")
    assert coverage.domain_of(URLS[0]) == "reuters.com"


RSS = b"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/"><channel>
<title>Google News - Business</title>
<item><title>Fed holds rates - Reuters</title><link>https://news.google.com/rss/articles/CBMi1</link>
<guid isPermaLink="false">CBMi1</guid><pubDate>Mon, 25 May 2026 12:30:00 GMT</pubDate>
<description>&lt;a href="https://news.google.com/x"&gt;Fed holds rates&lt;/a&gt;&amp;nbsp;Reuters</description>
<source url="https://www.reuters.com">Reuters</source></item>
<item><title></title><description></description></item>
<item><title>Second story</title><link>https://example.com/two</link><dc:date>2026-05-24</dc:date>
<dc:creator>Jane Doe</dc:creator></item>
</channel></rss>"""

ATOM = b"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"><title>GOV.UK News</title>
<entry><title>New rule for landlords</title><id>tag:gov.uk,2026:1</id>
<link rel="self" href="https://www.gov.uk/api/1"/><link rel="alternate" href="https://www.gov.uk/news/rule"/>
<updated>2026-05-25T09:15:00+01:00</updated><summary type="html">&lt;p&gt;A &lt;b&gt;new&lt;/b&gt; rule.&lt;/p&gt;</summary>
<author><name>Department X</name></author></entry>
</feed>"""


def test_rss_reads_pubdate_and_keeps_the_google_news_publisher() -> None:
    feed = parse_feed(RSS, "https://news.google.com/rss/headlines/section/topic/BUSINESS")
    assert feed.title == "Google News - Business"
    assert [e.feed_position for e in feed.entries] == [1, 2]
    first, second = feed.entries
    # newsjack lower-cased element names and then looked up "pubDate", so RSS dates were always lost.
    assert (first.published_at, first.published_precision) == ("2026-05-25T12:30:00Z", "time")
    assert first.source_url == "https://www.reuters.com" and first.source_name == "Reuters"
    assert first.container == "Reuters"
    assert first.excerpt == "Fed holds rates Reuters"
    assert first.id == "CBMi1" and first.url == "https://news.google.com/rss/articles/CBMi1"
    assert (second.published_at, second.published_precision) == ("2026-05-24", "date")
    assert second.author == "Jane Doe" and second.container == "Google News - Business"


def test_atom_prefers_the_alternate_link_and_normalizes_time() -> None:
    [entry] = parse_feed(ATOM, "https://www.gov.uk/search/news-and-communications.atom").entries
    assert entry.url == "https://www.gov.uk/news/rule"
    assert (entry.published_at, entry.published_precision) == ("2026-05-25T08:15:00Z", "time")
    assert entry.excerpt == "A new rule."
    assert entry.author == "Department X" and entry.id == "tag:gov.uk,2026:1"


def test_limit_counts_kept_entries_only() -> None:
    assert [e.title for e in parse_feed(RSS, "u", limit=1).entries] == ["Fed holds rates - Reuters"]


def test_hostile_or_broken_documents_are_refused_loudly() -> None:
    bomb = b'<?xml version="1.0"?><!DOCTYPE lolz [<!ENTITY lol "lol">]><rss><channel><title>&lol;</title></channel></rss>'
    with pytest.raises(FeedParseError, match="entities"):
        parse_feed(bomb, "u")
    with pytest.raises(FeedParseError, match="well-formed"):
        parse_feed(b"<rss><channel>", "u")
    with pytest.raises(FeedParseError, match="not RSS or Atom"):
        parse_feed(b"<html><body>hi</body></html>", "u")


def test_malformed_feed_error_redacts_the_exception_chain() -> None:
    """Parser diagnostics stay useful without preserving a signed feed URL in a traceback."""
    secret = "feed-traceback-secret"
    feed_url = f"https://example.test/feed?api_key={secret}"

    with pytest.raises(FeedParseError) as caught:
        parse_feed(b"<rss><channel>", feed_url)

    rendered = "".join(traceback.format_exception(caught.type, caught.value, caught.tb))
    assert "not well-formed XML" in rendered
    assert "line" in rendered and "column" in rendered
    assert secret not in rendered


def test_relative_dates_resolve_only_against_a_given_clock() -> None:
    now = datetime(2026, 5, 25, 18, 0, tzinfo=UTC)
    assert normalize_feed_date("3 hours ago", now=now) == ("2026-05-25T15:00:00Z", "time")
    assert normalize_feed_date("3 hours ago") == (None, "none")
    assert normalize_feed_date("not a date") == (None, "none")


def test_story_url_key_is_the_union_of_the_article_keys_it_replaced() -> None:
    # One tracker list for every article key (coverage, the blog adapter, the corpus key).
    base = "https://example.com/post"
    for tracker in (
        "ref=hn",
        "source=rss----abc",
        "s=20",
        "msclkid=x",
        "yclid=1",
        "spm=a.b",
        "s_kwcid=k",
        "ref_src=tw",
        "utm_medium=x",
        "fbclid=q",
    ):
        assert story_url_key(f"{base}?{tracker}") == base, tracker
    assert (
        story_url_key(f"{base}?s=climate") == f"{base}?s=climate"
    )  # a site search, not a share code
    # A default port is noise; any other port is a different server.
    assert (
        story_url_key("https://example.com:443/a")
        == story_url_key("http://example.com:80/a")
        == "https://example.com/a"
    )
    assert story_url_key("https://example.com:8443/a") == "https://example.com:8443/a"
