"""The podcast fields of ``matrx_scraper.feeds``, one test per field, on recorded real feeds.

Expected values are read straight from the same bytes with ElementTree and explicit namespaces,
so each test checks the parser against the document, not against itself.
(fixtures/feeds/manifest.json names each feed's URL and fetch time.)
"""

from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree

from matrx_scraper.feeds import clean_text, duration_seconds, normalize_feed_date, parse_feed

FEEDS = Path(__file__).parent / "fixtures" / "feeds"
TWIT = (FEEDS / "twit_podcast__2026-09-27.xml").read_bytes()
PAGED = (FEEDS / "soundcloud_paged_podcast__2026-09-27.xml").read_bytes()
NS = {
    "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
    "atom": "http://www.w3.org/2005/Atom",
    "podcast": "https://podcastindex.org/namespace/1.0",
}
CHANNEL = ElementTree.fromstring(TWIT).find("channel")
ITEMS = CHANNEL.findall("item")
FEED = parse_feed(TWIT, "https://feeds.twit.tv/twit.xml")


def test_every_episode_is_kept_in_order() -> None:
    assert len(FEED.entries) == len(ITEMS) == 20 and FEED.format == "rss"


# ── per entry ──


def test_enclosure() -> None:
    for entry, item in zip(FEED.entries, ITEMS, strict=True):
        enclosure = item.find("enclosure")
        assert entry.enclosure_url == enclosure.get("url")
        assert entry.enclosure_type == enclosure.get("type") == "audio/mpeg"
        assert entry.enclosure_length == int(enclosure.get("length"))


def test_itunes_duration() -> None:
    for entry, item in zip(FEED.entries, ITEMS, strict=True):
        raw = item.findtext("itunes:duration", namespaces=NS)
        assert entry.itunes_duration == raw
        h, m, s = (int(x) for x in raw.split(":"))
        assert entry.duration_seconds == h * 3600 + m * 60 + s
    assert duration_seconds("1:02:03") == 3723 and duration_seconds("59:07") == 3547
    assert duration_seconds("3723") == 3723 and duration_seconds("soon") is None


def test_itunes_image() -> None:
    for entry, item in zip(FEED.entries, ITEMS, strict=True):
        assert entry.image_url == item.find("itunes:image", NS).get("href")


def test_podcast_transcript() -> None:
    for entry, item in zip(FEED.entries, ITEMS, strict=True):
        transcript = item.find("podcast:transcript", NS)
        assert entry.transcript_url == transcript.get("url")
        assert entry.transcript_type == transcript.get("type")


def test_an_ordinary_feed_entry_has_no_podcast_fields() -> None:
    rss = b"<rss><channel><title>t</title><item><title>a</title><link>https://x.test/a</link></item></channel></rss>"
    entry = parse_feed(rss, "https://x.test/feed").entries[0]
    assert (entry.enclosure_url, entry.duration_seconds, entry.image_url, entry.transcript_url) == (None,) * 4


def test_an_episode_with_only_an_enclosure_is_kept() -> None:
    rss = b'<rss><channel><title>t</title><item><enclosure url="https://c.test/1.mp3" type="audio/mpeg"/></item></channel></rss>'
    entries = parse_feed(rss, "https://x.test/feed").entries
    assert len(entries) == 1 and entries[0].enclosure_url == "https://c.test/1.mp3"


# ── per feed ──


def test_channel_description() -> None:
    raw = CHANNEL.findtext("description")
    assert "<p>" in raw  # the feed ships HTML
    assert FEED.description == clean_text(raw) and FEED.description.startswith("This Week in Tech is")


def test_channel_image() -> None:
    assert FEED.image_url == CHANNEL.find("itunes:image", NS).get("href")


def test_channel_author() -> None:
    assert FEED.author == CHANNEL.findtext("itunes:author", namespaces=NS) == "TWiT"


def test_channel_language() -> None:
    assert FEED.language == CHANNEL.findtext("language") == "en-US"


def test_channel_last_build_date() -> None:
    raw = CHANNEL.findtext("lastBuildDate")
    assert FEED.raw_last_build_date == raw
    assert FEED.last_build_date == normalize_feed_date(raw)[0] == "2026-09-25T20:35:32Z"  # PDT → UTC


def test_channel_link() -> None:
    assert FEED.link == CHANNEL.findtext("link")


def test_next_page_link() -> None:
    channel = ElementTree.fromstring(PAGED).find("channel")
    expected = next(link.get("href") for link in channel.findall("atom:link", NS) if link.get("rel") == "next")
    paged = parse_feed(PAGED, "https://feeds.soundcloud.com/users/soundcloud:users:211911700/sounds.rss")
    assert paged.next_url == expected and "before=" in expected
    assert FEED.next_url is None  # an unpaged feed has none
