"""Share of voice (OPENSEO-TOOLS-SPEC §5.6, T7): no data is never zero.

The provider rows come from a REAL persisted DataForSEO response
(``fixtures/dataforseo/llm_mentions_cross_aggregated_live.json`` — core's live
one-task proof, run c06ee4f3). Where a rule needs a case the provider did not
happen to return (a brand with no row, a failed platform, an unrequested row),
the test derives it from that real payload by removing or relabelling rows —
never by inventing numbers.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

from matrx_seo.share_of_voice import (
    PlatformOutcome,
    compute_share_of_voice,
    detect_target,
    resolve_competitor_groups,
    sum_nullable,
)

_FIXTURE = (
    Path(__file__).parent / "fixtures" / "dataforseo" / "llm_mentions_cross_aggregated_live.json"
)


def _live_items() -> list[dict]:
    payload = json.loads(_FIXTURE.read_text())["payload"]
    return payload["tasks"][0]["result"][0]["items"]


def _ok(items, platform="google") -> PlatformOutcome:
    return PlatformOutcome(platform=platform, status="ok", items=items)


def test_live_payload_gives_real_shares():
    items = _live_items()  # dataforseo 308, semrush 27180
    sov, reason = compute_share_of_voice([_ok(items)], "dataforseo", ["semrush"])
    assert reason is None
    by_name = {e.name: e for e in sov.entries}
    assert by_name["semrush"].mentions == 27180
    assert by_name["dataforseo"].mentions == 308
    assert by_name["dataforseo"].is_target is True
    assert by_name["semrush"].share_pct == round(27180 / (27180 + 308) * 100, 2)
    assert [e.name for e in sov.entries] == ["semrush", "dataforseo"]


def test_every_requested_key_is_seeded_null_and_sorts_last():
    items = _live_items()
    sov, _ = compute_share_of_voice([_ok(items)], "dataforseo", ["semrush", "moz.com"])
    names = [e.name for e in sov.entries]
    assert names == ["semrush", "dataforseo", "moz.com"]
    moz = sov.entries[-1]
    assert moz.mentions is None and moz.share_pct is None


def test_null_is_not_counted_in_the_denominator_but_zero_is():
    items = _live_items()
    zeroed = copy.deepcopy(items)
    for row in zeroed[1]["platform"]:
        row["mentions"] = 0  # semrush known-zero
    sov, _ = compute_share_of_voice([_ok(zeroed)], "dataforseo", ["semrush", "moz.com"])
    by_name = {e.name: e for e in sov.entries}
    assert by_name["semrush"].mentions == 0
    assert by_name["semrush"].share_pct == 0.0  # a known zero is a real 0%
    assert by_name["dataforseo"].share_pct == 100.0  # 308 / (308 + 0); moz (null) excluded
    assert by_name["moz.com"].mentions is None


def test_provider_null_mentions_stay_null():
    items = copy.deepcopy(_live_items())
    for row in items[1]["platform"]:
        row["mentions"] = None
    sov, _ = compute_share_of_voice([_ok(items)], "dataforseo", ["semrush"])
    by_name = {e.name: e for e in sov.entries}
    assert by_name["semrush"].mentions is None
    assert by_name["dataforseo"].share_pct == 100.0


def test_unrequested_rows_are_ignored():
    items = copy.deepcopy(_live_items())
    items[1]["key"] = "ahrefs"  # a row nobody asked for
    sov, _ = compute_share_of_voice([_ok(items)], "dataforseo", ["semrush"])
    by_name = {e.name: e for e in sov.entries}
    assert "ahrefs" not in by_name
    assert by_name["semrush"].mentions is None
    assert by_name["dataforseo"].share_pct == 100.0


def test_keys_match_case_insensitively_and_keep_the_requested_label():
    items = copy.deepcopy(_live_items())
    items[0]["key"] = "DataForSEO"
    sov, _ = compute_share_of_voice([_ok(items)], "dataforseo", ["Semrush"])
    by_name = {e.name: e for e in sov.entries}
    assert by_name["dataforseo"].mentions == 308 and by_name["dataforseo"].is_target
    assert by_name["Semrush"].mentions == 27180


def test_platforms_sum_null_aware_and_a_failed_platform_adds_nothing():
    items = _live_items()
    chat = copy.deepcopy(items)
    for item in chat:
        for row in item["platform"]:
            row["key"] = "chat_gpt"
    chat[0]["platform"][0]["mentions"] = None  # dataforseo unknown on chat_gpt
    outcomes = [
        _ok(items, "google"),
        _ok(chat, "chat_gpt"),
        PlatformOutcome(platform="chat_gpt", status="failed", error="provider 50000"),
    ]
    sov, _ = compute_share_of_voice(outcomes, "dataforseo", ["semrush"])
    by_name = {e.name: e for e in sov.entries}
    assert by_name["dataforseo"].mentions == 308  # null + 308 = 308
    assert by_name["semrush"].mentions == 27180 * 2
    assert {"platform": "chat_gpt", "status": "failed", "error": "provider 50000"} in sov.platforms


def test_no_competitors_or_every_platform_failed_is_a_null_section_with_a_reason():
    sov, reason = compute_share_of_voice([_ok(_live_items())], "dataforseo", [])
    assert sov is None and "no competitors" in reason
    sov, reason = compute_share_of_voice(
        [PlatformOutcome(platform="google", status="failed", error="x")], "dataforseo", ["semrush"]
    )
    assert sov is None and "unknown (not zero)" in reason


def test_competitor_dedupe_is_case_insensitive_and_drops_target_collisions():
    groups = resolve_competitor_groups(
        "Nike", ["nike", "Adidas", "ADIDAS", "puma.com", "https://www.PUMA.com/shoes", "  "]
    )
    assert [g.label for g in groups] == ["Adidas", "puma.com"]
    assert groups[1].detected.type == "domain"


def test_detect_target():
    assert detect_target("https://www.W3.org/TR/").value == "w3.org"
    assert detect_target("w3.org").type == "domain"
    assert detect_target("World Wide Web Consortium").type == "keyword"
    assert detect_target("W3C").type == "keyword"


def test_sum_nullable():
    assert sum_nullable([None, None]) is None
    assert sum_nullable([None, 0]) == 0
    assert sum_nullable([2, None, 3]) == 5
