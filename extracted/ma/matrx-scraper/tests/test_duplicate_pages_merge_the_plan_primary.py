"""Merging duplicate pages keeps the target keyword, which lives in the SEO plan.

The target keyword's one home is ``desired_values.keyword_plan.primary_keyword_id``.
The old merge copied the retired ``target_keyword`` column and merged
``desired_values`` only at the top level, so a canonical page whose plan had no
primary silently dropped the duplicate's whole plan, primary included.
"""

from matrx_scraper.web_crawl.url_identity import merge_page_desired_values


def test_empty_canonical_primary_takes_the_duplicates():
    merged, conflicts = merge_page_desired_values(
        {"keyword_plan": {"page_role": "money"}, "social_card": {"og_title": "C"}},
        {"keyword_plan": {"primary_keyword_id": "kw-a", "page_role": "hub"}, "headings": {"notes": "A"}},
    )
    assert conflicts == 0
    assert merged["keyword_plan"] == {"primary_keyword_id": "kw-a", "page_role": "money"}
    assert merged["social_card"] == {"og_title": "C"}
    assert merged["headings"] == {"notes": "A"}


def test_two_primaries_keep_the_canonical_and_never_lose_the_duplicate():
    merged, conflicts = merge_page_desired_values(
        {"keyword_plan": {"primary_keyword_id": "kw-c", "secondary_keyword_ids": ["kw-s"]}},
        {"keyword_plan": {"primary_keyword_id": "kw-a", "secondary_keyword_ids": ["kw-s", "kw-c"]}},
    )
    assert conflicts == 1
    assert merged["keyword_plan"]["primary_keyword_id"] == "kw-c"
    assert merged["keyword_plan"]["secondary_keyword_ids"] == ["kw-s", "kw-a"]


def test_no_plans_is_the_plain_top_level_merge():
    merged, conflicts = merge_page_desired_values({"a": 1}, {"a": 2, "b": 3})
    assert (merged, conflicts) == ({"a": 1, "b": 3}, 0)
