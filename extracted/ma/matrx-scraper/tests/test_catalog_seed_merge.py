from pathlib import Path

from matrx_scraper.vendors.catalog_seed import build_rows, merge_fields, merge_list


def test_output_fields_union_keeps_live_extras():
    assert merge_list(["a", "b"], ["b", "z", "a"]) == ["a", "b", "z"]
    ch = merge_fields({"output_fields": ["a", "b"]}, {"output_fields": ["b", "x"]})
    assert ch["output_fields"] == ["a", "b", "x"]


def test_fill_only_never_overwrites_set_values():
    seed = {"featured": False, "known_issue": "seed", "sort_order": 5, "label": "New"}
    live = {"featured": True, "known_issue": None, "sort_order": 9, "label": "Old"}
    assert merge_fields(seed, live) == {"known_issue": "seed", "label": "New"}


def test_metadata_merges_key_by_key():
    seed = {"metadata": {"records_are": "items", "new": 1}}
    ch = merge_fields(seed, {"metadata": {"records_are": "entity", "mine": 2}})
    assert ch["metadata"] == {"records_are": "entity", "new": 1, "mine": 2}
    assert merge_fields({"metadata": {"records_are": "x"}}, {"metadata": {"records_are": "x"}}) == {}


def test_records_are_rule_reproduces_live_split():
    live_items = set(Path(__file__).with_name("fixtures").joinpath("records_are_items.txt").read_text().split())
    rows = build_rows()
    assert len(live_items) == 60 and len(rows) == 1229
    assert {r["key"] for r in rows if r["metadata"]["records_are"] == "items"} == live_items
    assert sum(r["metadata"]["records_are"] == "entity" for r in rows) == 1169


def test_trustpilot_extras_in_seed():
    row = next(r for r in build_rows() if r["key"] == "trustpilot_reviews")
    assert row["output_fields"][-3:] == ["company_overall_rating", "company_rating_name", "company_total_reviews"]
    assert len(row["output_fields"]) == len(set(row["output_fields"]))


def test_verified_live_never_downgraded_but_can_be_filled():
    assert merge_fields({"verified_live": False}, {"verified_live": True}) == {}
    assert merge_fields({"verified_live": True}, {"verified_live": False}) == {"verified_live": True}


def test_dead_examples_are_replaced_in_the_seed_so_a_reseed_keeps_them() -> None:
    from matrx_scraper.vendors.catalog_seed import EXAMPLE_OVERRIDES, build_rows

    rows = {r["key"]: r for r in build_rows()}
    for key, url in EXAMPLE_OVERRIDES.items():
        spec_urls = [f["example"] for f in rows[key]["input_spec"]["fields"] if f["name"] == "url"]
        assert spec_urls == [url], key
        assert rows[key]["example_url"] == url, key
    assert "5113183757" not in rows["walmart_product"]["example_url"]
