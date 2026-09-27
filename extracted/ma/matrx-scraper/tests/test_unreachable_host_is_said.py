"""A host we never reached is said in words — never "answered 500", never an empty Source.

Web-app walk, 2026-09-26: a nonexistent host was reported as "answered 500". The HTTP fetch
recorded a transport exception as ``status_code=500`` with the bare reason ``request_error``.
Breaks these tests name: a DNS failure carrying a status code, or carrying no sentence naming the
host and what to do; a DNS failure landing a Source.
"""

from __future__ import annotations

from matrx_scraper.orchestrator import scrape_many_stream
from matrx_scraper.unreachable import unreachable_kind, unreachable_sentence

HOST = "no-such-host-matrx-guard.invalid"


def test_the_sentence_names_the_host_the_failure_and_the_remedy() -> None:
    s = unreachable_sentence(f"https://{HOST}/a?b=1", [{"request_error": "[Errno 8] nodename nor servname provided"}])
    assert s and HOST in s and "does not exist" in s and "typo" in s and s.endswith(".")
    c = unreachable_sentence("https://a.example/", [{"request_error": "Connection refused"}])
    assert c and "did not accept a connection" in c
    assert unreachable_kind([{"bad_status": "Status code 404"}]) is None


async def test_a_dns_failure_has_no_status_and_says_why() -> None:
    # ``.invalid`` never resolves (RFC 6761), so this is a real resolver failure, no stand-in.
    results = [r async for r in scrape_many_stream([f"https://{HOST}/page"], use_proxy=False)]
    [r] = results
    assert r.success is False
    assert r.status_code == 0, f"a host that never answered reported status {r.status_code}"
    assert r.failure_message and HOST in r.failure_message and "does not exist" in r.failure_message
